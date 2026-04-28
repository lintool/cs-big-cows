#!/usr/bin/env python3
"""Validate ACM Fellows Google Scholar profile links against Scholar profile titles.

The script is intentionally conservative:

- cached URLs, including cached HTML pages, are never fetched again unless --refresh is passed
- each uncached request waits --delay seconds before the next one
- every --batch-size uncached requests, the script pauses for --batch-pause seconds
- cache and report files are written after every request so runs can be resumed

The script does not modify the app data files. It only writes validation output.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = APP_ROOT / "data" / "acm-fellows.csv"
DEFAULT_CACHE = APP_ROOT / ".cache" / "google-scholar-validation-cache.json"
DEFAULT_REPORT = APP_ROOT / ".cache" / "google-scholar-validation-report.json"

SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv"}
PARTICLES = {"al", "bin", "da", "de", "del", "den", "der", "di", "du", "la", "le", "van", "von"}


@dataclass(frozen=True)
class ScholarProfile:
    index: int
    name: str
    url: str
    acm_profile: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="Path to data/acm-fellows.csv or a bundled *-data.js file.")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="JSON cache path.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="JSON report path.")
    parser.add_argument("--delay", type=float, default=5.0, help="Seconds to wait between uncached requests.")
    parser.add_argument("--batch-size", type=int, default=20, help="Uncached requests per batch.")
    parser.add_argument("--batch-pause", type=float, default=120.0, help="Seconds to pause after each batch.")
    parser.add_argument("--limit-new", type=int, default=None, help="Optional cap on uncached requests this run.")
    parser.add_argument("--refresh", action="store_true", help="Refetch URLs even when cached.")
    return parser.parse_args()


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_rows(data_path: Path) -> list[dict[str, Any]]:
    if data_path.suffix.lower() == ".csv":
        with data_path.open(newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    source = data_path.read_text(encoding="utf-8")
    match = re.search(r"window\.[A-Z0-9_]+\s*=\s*(.*);\s*$", source, re.S)
    if not match:
        raise ValueError(f"Could not parse data array from {data_path}")
    return json.loads(match.group(1))


def row_name(row: dict[str, Any]) -> str:
    if row.get("Full Name"):
        return str(row["Full Name"]).strip()

    given_name = str(row.get("Given Name") or "").strip()
    last_name_value = str(row.get("Last Name") or "").strip()
    return " ".join(part for part in [given_name, last_name_value] if part)


def unique_profiles(rows: list[dict[str, Any]]) -> list[ScholarProfile]:
    seen: set[str] = set()
    profiles: list[ScholarProfile] = []
    for row in rows:
        url = (row.get("Google Scholar Profile") or "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        profiles.append(
            ScholarProfile(
                index=int(row["Index"]),
                name=row_name(row),
                url=url,
                acm_profile=str(row.get("ACM Fellow Profile") or "").strip(),
            )
        )
    return profiles


def normalize_tokens(value: str) -> list[str]:
    text = html.unescape(value or "").lower()
    text = re.sub(r"[^a-z0-9\s.-]", " ", text)
    tokens = []
    for token in re.split(r"\s+", text):
        token = token.strip(".-")
        if token and token not in SUFFIXES:
            tokens.append(token)
    return tokens


def last_name(tokens: list[str]) -> str:
    useful = [token for token in tokens if len(token) > 1 and token not in PARTICLES]
    if useful:
        return useful[-1]
    return tokens[-1] if tokens else ""


def compatible_name(expected: str, observed: str) -> bool:
    expected_tokens = normalize_tokens(expected)
    observed_tokens = normalize_tokens(observed)
    if not expected_tokens or not observed_tokens:
        return False

    if last_name(expected_tokens) == last_name(observed_tokens):
        expected_first = expected_tokens[0]
        observed_first = observed_tokens[0]
        return (
            expected_first == observed_first
            or expected_first[:1] == observed_first[:1]
            or any(token in observed_tokens for token in expected_tokens[:-1] if len(token) > 1)
        )

    expected_set = {token for token in expected_tokens if len(token) > 1}
    observed_set = {token for token in observed_tokens if len(token) > 1}
    return len(expected_set & observed_set) >= 2


def extract_title(body: str) -> str:
    og_match = re.search(r'<meta property="og:title" content="([^"]+)"', body, re.I)
    if og_match:
        return html.unescape(og_match.group(1)).strip()

    title_match = re.search(r"<title>(.*?)</title>", body, re.I | re.S)
    if title_match:
        title = html.unescape(re.sub(r"\s+", " ", title_match.group(1))).strip()
        return re.sub(r"\s*-\s*Google Scholar\s*$", "", title).strip()

    return ""


def is_blocked_page(body: str) -> bool:
    lowered = body.lower()
    return (
        "not a robot" in lowered
        or "unusual traffic" in lowered
        or "/sorry/" in lowered
        or "our systems have detected unusual traffic" in lowered
    )


def decode_body(body: bytes, headers: Any) -> str:
    charset = headers.get_content_charset() if headers else None
    return body.decode(charset or "latin1", errors="replace")


def fetch_profile(url: str) -> dict[str, Any]:
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        return {
            "status": "invalid_url",
            "status_code": None,
            "title": "",
            "html": "",
            "error": f"Not an HTTP URL: {url}",
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 Chrome/124 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = decode_body(response.read(), response.headers)
            status_code = response.status
    except urllib.error.HTTPError as error:
        return {
            "status": "http_error",
            "status_code": error.code,
            "title": "",
            "html": decode_body(error.read(), error.headers),
            "fetched_at": fetched_at,
        }
    except urllib.error.URLError as error:
        return {"status": "url_error", "error": str(error.reason), "title": "", "html": "", "fetched_at": fetched_at}
    except TimeoutError:
        return {"status": "timeout", "title": "", "html": "", "fetched_at": fetched_at}

    title = extract_title(body)
    if is_blocked_page(body):
        status = "blocked"
    elif not title:
        status = "no_title"
    else:
        status = "ok"

    return {"status": status, "status_code": status_code, "title": title, "html": body, "fetched_at": fetched_at}


def build_report(profiles: list[ScholarProfile], cache: dict[str, Any]) -> dict[str, Any]:
    entries = []
    status_counts: dict[str, int] = {}
    for profile in profiles:
        cached = cache.get(profile.url)
        if not cached:
            entries.append(
                {
                    "index": profile.index,
                    "name": profile.name,
                    "url": profile.url,
                    "acm_profile": profile.acm_profile,
                    "status": "missing",
                    "title": "",
                    "match": None,
                }
            )
            status_counts["missing"] = status_counts.get("missing", 0) + 1
            continue

        status = cached.get("status", "unknown")
        title = cached.get("title", "")
        match = compatible_name(profile.name, title) if status == "ok" else None
        entries.append(
            {
                "index": profile.index,
                "name": profile.name,
                "url": profile.url,
                "acm_profile": profile.acm_profile,
                "status": status,
                "title": title,
                "match": match,
                "fetched_at": cached.get("fetched_at"),
            }
        )
        status_counts[status] = status_counts.get(status, 0) + 1

    mismatches = [entry for entry in entries if entry["match"] is False]
    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_profiles": len(profiles),
        "cached_profiles": sum(1 for profile in profiles if profile.url in cache),
        "status_counts": status_counts,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "entries": entries,
    }


def main() -> int:
    args = parse_args()
    rows = load_rows(args.data)
    profiles = unique_profiles(rows)
    cache: dict[str, Any] = load_json(args.cache, {})

    new_requests = 0
    batch_requests = 0

    for position, profile in enumerate(profiles, start=1):
        if not args.refresh and profile.url in cache:
            continue

        if args.limit_new is not None and new_requests >= args.limit_new:
            break

        if batch_requests >= args.batch_size:
            print(f"Pausing {args.batch_pause:.0f}s after {batch_requests} uncached requests.", flush=True)
            time.sleep(args.batch_pause)
            batch_requests = 0

        print(f"[{position}/{len(profiles)}] fetching {profile.name}: {profile.url}", flush=True)
        cache[profile.url] = fetch_profile(profile.url)
        new_requests += 1
        batch_requests += 1

        atomic_write_json(args.cache, cache)
        atomic_write_json(args.report, build_report(profiles, cache))

        if args.delay > 0:
            time.sleep(args.delay)

    atomic_write_json(args.cache, cache)
    report = build_report(profiles, cache)
    atomic_write_json(args.report, report)

    print(
        f"Done. profiles={report['total_profiles']} cached={report['cached_profiles']} "
        f"mismatches={report['mismatch_count']} report={args.report}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

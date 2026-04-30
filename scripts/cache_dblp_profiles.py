#!/usr/bin/env python3
"""Cache DBLP profile pages and report parsed profile titles.

The script is intentionally conservative:

- cached URLs, including cached HTML pages, are never fetched again unless --refresh is passed
- each uncached request waits --delay seconds, plus optional --delay-jitter
- every jittered batch of uncached requests, the script pauses for --batch-pause seconds, plus optional jitter
- transient fetch failures are retried with exponential backoff
- cache and report files are written after every request so runs can be resumed

The script does not modify the app data files. It only writes validation output.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import random
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = APP_ROOT / "data" / "acm_fellows.csv"
DEFAULT_CACHE = APP_ROOT / ".cache" / "dblp-profile-cache.json"
DEFAULT_REPORT = APP_ROOT / ".cache" / "dblp-profile-report.json"

SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv"}
PARTICLES = {"al", "bin", "da", "de", "del", "den", "der", "di", "du", "la", "le", "van", "von"}
TRANSIENT_HTTP_STATUS = {408, 425, 429, 500, 502, 503, 504}


@dataclass(frozen=True)
class DblpProfile:
    index: int
    name: str
    url: str
    acm_profile: str = ""


class DblpProfileParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict[str, str]]] = []
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.og_title = ""
        self._in_title = False
        self._h1_depth: int | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_dict = {key.lower(): value or "" for key, value in attrs}
        self.stack.append((tag, attr_dict))

        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._h1_depth = len(self.stack)
        elif tag == "meta":
            property_value = attr_dict.get("property", "").lower()
            name_value = attr_dict.get("name", "").lower()
            if property_value == "og:title" or name_value == "citation_author":
                self.og_title = attr_dict.get("content", "").strip()

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

        if self._h1_depth is not None and len(self.stack) == self._h1_depth and tag == "h1":
            self._h1_depth = None

        if self.stack:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._h1_depth is not None:
            self.h1_parts.append(data)

    def parsed(self) -> dict[str, str]:
        title = clean_dblp_title(self.og_title or " ".join(self.h1_parts) or " ".join(self.title_parts))
        return {"title": title}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="Path to data/acm_fellows.csv.")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="JSON cache path.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="JSON report path.")
    parser.add_argument("--delay", type=float, default=2.0, help="Base seconds to wait between uncached requests.")
    parser.add_argument("--delay-jitter", type=float, default=1.0, help="Random extra seconds added to --delay.")
    parser.add_argument("--batch-size", type=int, default=50, help="Base uncached requests per batch.")
    parser.add_argument("--batch-size-jitter", type=int, default=5, help="Random +/- adjustment to --batch-size.")
    parser.add_argument("--batch-pause", type=float, default=60.0, help="Base seconds to pause after each batch.")
    parser.add_argument("--batch-pause-jitter", type=float, default=15.0, help="Random extra seconds added to --batch-pause.")
    parser.add_argument("--max-retries", type=int, default=2, help="Retries for transient fetch failures.")
    parser.add_argument("--backoff", type=float, default=10.0, help="Base seconds for exponential retry backoff.")
    parser.add_argument("--backoff-jitter", type=float, default=5.0, help="Random extra seconds added to retry backoff.")
    parser.add_argument("--limit-new", type=int, default=None, help="Optional cap on uncached requests this run.")
    parser.add_argument(
        "--retry-status",
        action="append",
        default=[],
        help="Refetch cached URLs whose status matches this value. May be passed multiple times.",
    )
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


def load_rows(data_path: Path) -> list[dict[str, str]]:
    with data_path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def row_name(row: dict[str, str]) -> str:
    return clean_person_name(str(row.get("name") or ""))


def row_value(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return str(value).strip()
    return ""


def unique_profiles(rows: list[dict[str, str]]) -> list[DblpProfile]:
    seen: set[str] = set()
    profiles: list[DblpProfile] = []
    for row_number, row in enumerate(rows, start=1):
        url = row_value(row, "DBLP Profile", "dblp_profile")
        if not url or url in seen:
            continue
        seen.add(url)
        profiles.append(
            DblpProfile(
                index=row_number,
                name=row_name(row),
                url=url,
                acm_profile=row_value(row, "ACM Fellow Profile", "acm_fellow_profile"),
            )
        )
    return profiles


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def clean_dblp_title(value: str) -> str:
    title = normalize_space(value)
    title = re.sub(r"\s*\|\s*dblp.*$", "", title, flags=re.IGNORECASE).strip()
    title = re.sub(r"^dblp:\s*", "", title, flags=re.IGNORECASE).strip()
    return clean_person_name(title)


def clean_person_name(value: str) -> str:
    name = normalize_space(value)
    name = re.sub(
        r"^(?:prof\.dr\.ir\.|prof\.\s*dr\.-ing\.?|prof\.\s*dr\.?|professor|pofessor|prof\.?|doctor|dr\.?|mr\.?|ms\.?|mrs\.?)\s+",
        "",
        name,
        flags=re.IGNORECASE,
    )
    name = re.sub(r"^(?:dame|sir)\s+", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+(?:ph\.?\s*d\.?|phd|dphil|ccp)\.?$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+\d{4,}$", "", name)
    return normalize_space(name)


def normalize_tokens(value: str) -> list[str]:
    text = clean_person_name(value).lower()
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

    if last_name(expected_tokens) != last_name(observed_tokens):
        return False

    expected_first = expected_tokens[0]
    observed_first = observed_tokens[0]
    return (
        expected_first == observed_first
        or expected_first[:1] == observed_first[:1]
        or any(token in observed_tokens for token in expected_tokens[:-1] if len(token) > 1)
    )


def decode_body(body: bytes, headers: Any) -> str:
    charset = headers.get_content_charset() if headers else None
    return body.decode(charset or "utf-8", errors="replace")


def read_error_body(error: urllib.error.HTTPError) -> str:
    try:
        return decode_body(error.read(), error.headers)
    except (ConnectionError, OSError) as read_error:
        return f"Could not read HTTP error body: {read_error}"


def looks_blocked(body: str) -> bool:
    text = body.lower()
    return (
        "captcha" in text
        or "cf-browser-verification" in text
        or "cloudflare ray id" in text
        or "our systems have detected unusual traffic" in text
    )


def parse_profile_html(body: str) -> dict[str, str]:
    parser = DblpProfileParser()
    parser.feed(body)
    return parser.parsed()


def fetch_profile_once(url: str) -> dict[str, Any]:
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
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = decode_body(response.read(), response.headers)
            status_code = response.status
    except urllib.error.HTTPError as error:
        body = read_error_body(error)
        return {
            "status": "blocked" if looks_blocked(body) else "http_error",
            "status_code": error.code,
            "title": "",
            "html": body,
            "fetched_at": fetched_at,
        }
    except urllib.error.URLError as error:
        return {"status": "url_error", "error": str(error.reason), "title": "", "html": "", "fetched_at": fetched_at}
    except (ConnectionError, OSError) as error:
        status = "timeout" if isinstance(error, (TimeoutError, socket.timeout)) else "url_error"
        return {"status": status, "error": str(error), "title": "", "html": "", "fetched_at": fetched_at}

    parsed = parse_profile_html(body)
    if looks_blocked(body):
        status = "blocked"
    elif not parsed.get("title"):
        status = "no_title"
    else:
        status = "ok"

    return {"status": status, "status_code": status_code, "html": body, "fetched_at": fetched_at, **parsed}


def should_retry(result: dict[str, Any]) -> bool:
    status = result.get("status")
    status_code = result.get("status_code")
    return (
        status in {"url_error", "timeout"}
        or status_code in TRANSIENT_HTTP_STATUS
        or status == "blocked"
    )


def is_transient_failure(result: dict[str, Any]) -> bool:
    return should_retry(result)


def fetch_profile(url: str, max_retries: int, backoff: float, backoff_jitter: float) -> dict[str, Any]:
    attempts = []
    for attempt in range(max_retries + 1):
        result = fetch_profile_once(url)
        attempts.append(
            {
                "status": result.get("status"),
                "status_code": result.get("status_code"),
                "fetched_at": result.get("fetched_at"),
                "error": result.get("error", ""),
            }
        )
        if attempt >= max_retries or not should_retry(result):
            if len(attempts) > 1:
                result["attempts"] = attempts
            return result

        wait = max(0.0, backoff * (2**attempt)) + random.uniform(0.0, max(0.0, backoff_jitter))
        print(f"Retrying after {wait:.1f}s due to status={result.get('status')}", flush=True)
        time.sleep(wait)

    return result


def jittered_batch_size(batch_size: int, jitter: int) -> int:
    if jitter <= 0:
        return max(1, batch_size)
    return max(1, batch_size + random.randint(-jitter, jitter))


def jittered_pause(base: float, jitter: float) -> float:
    return max(0.0, base) + random.uniform(0.0, max(0.0, jitter))


def build_report(profiles: list[DblpProfile], cache: dict[str, Any]) -> dict[str, Any]:
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
                "status_code": cached.get("status_code"),
                "title": title,
                "match": match,
                "fetched_at": cached.get("fetched_at"),
            }
        )
        status_counts[status] = status_counts.get(status, 0) + 1

    review_candidates = [entry for entry in entries if entry["status"] != "missing" and (entry["status"] != "ok" or entry["match"] is False)]
    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_profiles": len(profiles),
        "cached_profiles": sum(1 for profile in profiles if profile.url in cache),
        "status_counts": status_counts,
        "review_candidate_count": len(review_candidates),
        "review_candidates": review_candidates,
        "entries": entries,
    }


def main() -> int:
    args = parse_args()
    rows = load_rows(args.data)
    profiles = unique_profiles(rows)
    cache: dict[str, Any] = load_json(args.cache, {})

    new_requests = 0
    batch_requests = 0
    current_batch_size = jittered_batch_size(args.batch_size, args.batch_size_jitter)

    for position, profile in enumerate(profiles, start=1):
        cached = cache.get(profile.url)
        should_refetch_status = cached is not None and cached.get("status") in set(args.retry_status)
        if args.retry_status and not should_refetch_status:
            continue
        if not args.refresh and not should_refetch_status and profile.url in cache:
            continue

        if args.limit_new is not None and new_requests >= args.limit_new:
            break

        if batch_requests >= current_batch_size:
            pause = jittered_pause(args.batch_pause, args.batch_pause_jitter)
            print(f"Pausing {pause:.1f}s after {batch_requests} uncached requests.", flush=True)
            time.sleep(pause)
            batch_requests = 0
            current_batch_size = jittered_batch_size(args.batch_size, args.batch_size_jitter)

        print(f"[{position}/{len(profiles)}] fetching {profile.name}: {profile.url}", flush=True)
        result = fetch_profile(profile.url, args.max_retries, args.backoff, args.backoff_jitter)
        if is_transient_failure(result):
            print(f"Not caching transient failure for {profile.url}: status={result.get('status')}", flush=True)
        else:
            cache[profile.url] = result
        new_requests += 1
        batch_requests += 1

        atomic_write_json(args.cache, cache)
        atomic_write_json(args.report, build_report(profiles, cache))

        delay = jittered_pause(args.delay, args.delay_jitter)
        if delay > 0:
            time.sleep(delay)

    atomic_write_json(args.cache, cache)
    report = build_report(profiles, cache)
    atomic_write_json(args.report, report)

    print(
        f"Done. profiles={report['total_profiles']} cached={report['cached_profiles']} "
        f"review_candidates={report['review_candidate_count']} report={args.report}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

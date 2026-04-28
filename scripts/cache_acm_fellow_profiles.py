#!/usr/bin/env python3
"""Cache ACM Fellow profile pages and report parsed profile fields.

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
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = APP_ROOT / "data" / "acm_fellows.csv"
DEFAULT_CACHE = APP_ROOT / ".cache" / "acm-fellow-profile-cache.json"
DEFAULT_REPORT = APP_ROOT / ".cache" / "acm-fellow-profile-report.json"

SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv"}
PARTICLES = {"al", "bin", "da", "de", "del", "den", "der", "di", "du", "la", "le", "van", "von"}


@dataclass(frozen=True)
class AcmProfile:
    index: int
    name: str
    url: str
    year: str = ""
    location: str = ""
    citation: str = ""


class AcmProfileParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict[str, str]]] = []
        self.h1_parts: list[str] = []
        self.title_parts: list[str] = []
        self.sections: list[dict[str, str]] = []
        self._in_title = False
        self._h1_depth: int | None = None
        self._section_depth: int | None = None
        self._current_section: dict[str, list[str]] | None = None
        self._current_field: str | None = None
        self._field_depth: int | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_dict = {key: value or "" for key, value in attrs}
        self.stack.append((tag, attr_dict))

        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._h1_depth = len(self.stack)
        elif tag == "section" and "awards-winners__citation" in attr_dict.get("class", ""):
            self._section_depth = len(self.stack)
            self._current_section = {"heading": [], "location_year": [], "citation": []}
        elif self._current_section is not None and tag in {"h2", "h3", "p"}:
            classes = attr_dict.get("class", "")
            if tag == "h2":
                self._current_field = "heading"
                self._field_depth = len(self.stack)
            elif tag == "h3" and "awards-winners__location" in classes:
                self._current_field = "location_year"
                self._field_depth = len(self.stack)
            elif tag == "p" and "awards-winners__citation-short" in classes:
                self._current_field = "citation"
                self._field_depth = len(self.stack)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

        if self._h1_depth is not None and len(self.stack) == self._h1_depth and tag == "h1":
            self._h1_depth = None

        if self._field_depth is not None and len(self.stack) == self._field_depth and self.stack[-1][0] == tag:
            self._current_field = None
            self._field_depth = None

        if self._section_depth is not None and len(self.stack) == self._section_depth and tag == "section":
            if self._current_section is not None:
                self.sections.append({key: clean_text(" ".join(value)) for key, value in self._current_section.items()})
            self._section_depth = None
            self._current_section = None
            self._current_field = None
            self._field_depth = None

        if self.stack:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._h1_depth is not None:
            self.h1_parts.append(data)
        if self._current_section is not None and self._current_field is not None:
            self._current_section[self._current_field].append(data)

    def parsed(self) -> dict[str, str]:
        section = next(
            (item for item in self.sections if normalize_space(item.get("heading", "")).lower() == "acm fellows"),
            {},
        )
        location, year = split_location_year(section.get("location_year", ""))
        return {
            "title": clean_title(" ".join(self.title_parts)),
            "page_name": clean_text(" ".join(self.h1_parts)),
            "award_heading": section.get("heading", ""),
            "location": location,
            "year": year,
            "citation": section.get("citation", ""),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="Path to data/acm_fellows.csv.")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="JSON cache path.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="JSON report path.")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds to wait between uncached requests.")
    parser.add_argument("--batch-size", type=int, default=50, help="Uncached requests per batch.")
    parser.add_argument("--batch-pause", type=float, default=60.0, help="Seconds to pause after each batch.")
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


def load_rows(data_path: Path) -> list[dict[str, str]]:
    with data_path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def row_name(row: dict[str, str]) -> str:
    return str(row.get("name") or "").strip()


def unique_profiles(rows: list[dict[str, str]]) -> list[AcmProfile]:
    seen: set[str] = set()
    profiles: list[AcmProfile] = []
    for row_number, row in enumerate(rows, start=1):
        url = (row.get("ACM Fellow Profile") or "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        profiles.append(
            AcmProfile(
                index=row_number,
                name=row_name(row),
                url=url,
                year=str(row.get("Year") or "").strip(),
                location=str(row.get("Location") or "").strip(),
                citation=str(row.get("Citation") or "").strip(),
            )
        )
    return profiles


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def clean_text(value: str) -> str:
    return normalize_space(value)


def clean_person_name(value: str) -> str:
    name = normalize_space(value)
    name = re.sub(
        r"^(?:prof\.dr\.ir\.|prof\.\s*dr\.-ing\.?|prof\.\s*dr\.?|professor|prof\.?|dr\.?|mr\.?|ms\.?|mrs\.?)\s+",
        "",
        name,
        flags=re.IGNORECASE,
    )
    name = re.sub(r"^(?:dame|sir)\s+", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+(?:ph\.?\s*d\.?|phd|dphil|ccp)\.?$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+\d{4,}$", "", name)
    return normalize_space(name)


def clean_title(value: str) -> str:
    title = normalize_space(value)
    return re.sub(r"\s*-\s*ACM Award Winner\s*$", "", title).strip()


def split_location_year(value: str) -> tuple[str, str]:
    text = clean_text(value)
    if " - " not in text:
        return "", ""
    location, year = text.rsplit(" - ", 1)
    return location.strip(), year.strip()


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


def decode_body(body: bytes, headers: Any) -> str:
    charset = headers.get_content_charset() if headers else None
    return body.decode(charset or "utf-8", errors="replace")


def parse_profile_html(body: str) -> dict[str, str]:
    parser = AcmProfileParser()
    parser.feed(body)
    parsed = parser.parsed()
    parsed["page_name"] = clean_person_name(parsed.get("page_name", ""))
    parsed["title"] = clean_person_name(parsed.get("title", ""))
    return parsed


def fetch_profile(url: str) -> dict[str, Any]:
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        return {
            "status": "invalid_url",
            "status_code": None,
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
            "html": decode_body(error.read(), error.headers),
            "fetched_at": fetched_at,
        }
    except urllib.error.URLError as error:
        return {"status": "url_error", "error": str(error.reason), "html": "", "fetched_at": fetched_at}
    except TimeoutError:
        return {"status": "timeout", "html": "", "fetched_at": fetched_at}

    parsed = parse_profile_html(body)
    if not parsed.get("page_name"):
        status = "no_name"
    elif not parsed.get("award_heading"):
        status = "no_fellow_award"
    else:
        status = "ok"

    return {"status": status, "status_code": status_code, "html": body, "fetched_at": fetched_at, **parsed}


def build_report(profiles: list[AcmProfile], cache: dict[str, Any]) -> dict[str, Any]:
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
                    "status": "missing",
                    "page_name": "",
                    "name_match": None,
                    "year_match": None,
                    "location_match": None,
                    "citation_match": None,
                }
            )
            status_counts["missing"] = status_counts.get("missing", 0) + 1
            continue

        status = cached.get("status", "unknown")
        page_name = clean_person_name(str(cached.get("page_name") or ""))
        parsed_year = str(cached.get("year") or "").strip()
        parsed_location = str(cached.get("location") or "").strip()
        parsed_citation = str(cached.get("citation") or "").strip()
        entry = {
            "index": profile.index,
            "name": profile.name,
            "url": profile.url,
            "status": status,
            "page_name": page_name,
            "title": cached.get("title", ""),
            "award_heading": cached.get("award_heading", ""),
            "year": parsed_year,
            "location": parsed_location,
            "citation": parsed_citation,
            "name_match": compatible_name(profile.name, page_name) if status == "ok" else None,
            "year_match": parsed_year == profile.year if status == "ok" else None,
            "location_match": parsed_location == profile.location if status == "ok" else None,
            "citation_match": normalize_space(parsed_citation) == normalize_space(profile.citation) if status == "ok" else None,
            "fetched_at": cached.get("fetched_at"),
        }
        entries.append(entry)
        status_counts[status] = status_counts.get(status, 0) + 1

    review_candidates = [
        entry
        for entry in entries
        if entry["status"] != "missing"
        and (
            entry["status"] != "ok"
            or entry["name_match"] is False
            or entry["year_match"] is False
            or entry["location_match"] is False
            or entry["citation_match"] is False
        )
    ]
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
        f"review_candidates={report['review_candidate_count']} report={args.report}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

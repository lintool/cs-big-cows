#!/usr/bin/env python3
"""Validate ACM Fellows Google Scholar profile links against Scholar profile titles.

The script is intentionally conservative:

- cached URLs, including cached HTML pages, are never fetched again unless --refresh is passed
- cached entries without a stored HTML page are treated as incomplete and fetched again
- each uncached request waits --delay seconds, plus optional --delay-jitter
- every jittered batch of uncached requests, the script pauses for --batch-pause seconds, plus optional jitter
- transient fetch failures are retried with exponential backoff
- cache and report files are written after every request so runs can be resumed

The script does not modify the app data files. It only writes cache and report output.
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
DEFAULT_OUTPUT = APP_ROOT / "data" / "google_scholar_profiles.csv"
DEFAULT_CACHE = APP_ROOT / ".cache" / "google-scholar-profile-cache.json"
DEFAULT_REPORT = APP_ROOT / ".cache" / "google-scholar-profile-report.json"

SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv"}
PARTICLES = {"al", "bin", "da", "de", "del", "den", "der", "di", "du", "la", "le", "van", "von"}
TRANSIENT_HTTP_STATUS = {408, 425, 429, 500, 502, 503, 504}
HTML_REQUIRED_STATUSES = {"ok", "blocked", "http_error", "no_title"}
PROFILE_CSV_COLUMNS = [
    "name",
    "profile",
    "crawl_date",
    "affiliation",
    "interests",
    "citations",
    "h_index",
    "i10_index",
    "citations_since_5y_ago",
    "h_index_since_5y_ago",
    "i10_index_since_5y_ago",
    "first_citation_year",
    "citation_by_year",
]
STAT_COLUMNS = PROFILE_CSV_COLUMNS[5:11]


@dataclass(frozen=True)
class ScholarProfile:
    index: int
    name: str
    url: str
    acm_profile: str = ""


class ScholarProfileParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict[str, str]]] = []
        self.title_parts: list[str] = []
        self.affiliation_parts: list[str] = []
        self.interest_parts: list[str] = []
        self.interests: list[str] = []
        self.og_title = ""
        self._in_title = False
        self._current_field: str | None = None
        self._field_depth: int | None = None
        self._seen_affiliation = False
        self._interest_depth: int | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_dict = {key.lower(): value or "" for key, value in attrs}
        self.stack.append((tag, attr_dict))
        classes = set(attr_dict.get("class", "").split())
        element_id = attr_dict.get("id", "")

        if tag == "title":
            self._in_title = True
        elif tag == "meta" and attr_dict.get("property", "").lower() == "og:title":
            self.og_title = attr_dict.get("content", "").strip()
        elif element_id == "gsc_prf_int":
            self._interest_depth = len(self.stack)
        elif (
            tag == "div"
            and "gsc_prf_il" in classes
            and element_id != "gsc_prf_ivh"
            and self._interest_depth is None
            and not self._seen_affiliation
        ):
            self._current_field = "affiliation"
            self._field_depth = len(self.stack)
            self._seen_affiliation = True
        elif tag == "a" and self._interest_depth is not None and "gsc_prf_inta" in classes:
            self._current_field = "interest"
            self._field_depth = len(self.stack)
            self.interest_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

        if self._current_field == "interest" and self._field_depth == len(self.stack):
            interest = normalize_space("".join(self.interest_parts))
            if interest:
                self.interests.append(interest)
            self.interest_parts = []
            self._current_field = None
            self._field_depth = None
        elif self._current_field == "affiliation" and self._field_depth == len(self.stack):
            self._current_field = None
            self._field_depth = None

        if self._interest_depth == len(self.stack):
            self._interest_depth = None

        if self.stack:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        elif self._current_field == "affiliation":
            self.affiliation_parts.append(data)
        elif self._current_field == "interest":
            self.interest_parts.append(data)

    def parsed(self) -> dict[str, Any]:
        title = self.og_title or " ".join(self.title_parts)
        return {
            "title": clean_scholar_name(title),
            "affiliation": clean_affiliation("".join(self.affiliation_parts)),
            "interests": self.interests,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="Path to data/acm_fellows.csv or a bundled *-data.js file.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="CSV path to write enriched Scholar profile rows.")
    parser.add_argument("--no-write-csv", action="store_true", help="Skip writing the enriched Scholar profile CSV.")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="JSON cache path.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="JSON report path.")
    parser.add_argument("--delay", type=float, default=5.0, help="Base seconds to wait between uncached requests.")
    parser.add_argument("--delay-jitter", type=float, default=2.0, help="Random extra seconds added to --delay.")
    parser.add_argument("--batch-size", type=int, default=25, help="Base uncached requests per batch.")
    parser.add_argument("--batch-size-jitter", type=int, default=0, help="Random +/- adjustment to --batch-size.")
    parser.add_argument("--batch-pause", type=float, default=120.0, help="Base seconds to pause after each batch.")
    parser.add_argument("--batch-pause-jitter", type=float, default=30.0, help="Random extra seconds added to --batch-pause.")
    parser.add_argument("--max-retries", type=int, default=1, help="Retries for transient fetch failures.")
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
    return str(row.get("name") or "").strip()


def row_value(row: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return str(value).strip()
    return ""


def canonical_scholar_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url.strip())
    query = urllib.parse.parse_qs(parsed.query)
    user = (query.get("user") or [""])[0].strip()
    if "scholar.google." in parsed.netloc.lower() and parsed.path == "/citations" and user:
        return f"https://scholar.google.com/citations?user={user}"
    return url.strip()


def normalize_cache_keys(cache: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for url, item in cache.items():
        key = canonical_scholar_url(url)
        existing = normalized.get(key)
        if existing is None or (not existing.get("html") and item.get("html")):
            normalized[key] = item
    return normalized


def unique_profiles(rows: list[dict[str, Any]]) -> list[ScholarProfile]:
    seen: set[str] = set()
    profiles: list[ScholarProfile] = []
    for row_number, row in enumerate(rows, start=1):
        url = canonical_scholar_url(row_value(row, "Google Scholar Profile", "google_scholar_profile"))
        if not url or url in seen:
            continue
        seen.add(url)
        profiles.append(
            ScholarProfile(
                index=row_number,
                name=row_name(row),
                url=url,
                acm_profile=row_value(row, "ACM Fellow Profile", "acm_fellow_profile"),
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


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def has_non_ascii(value: str) -> bool:
    return any(ord(char) > 127 for char in value)


def clean_scholar_name(value: str) -> str:
    name = normalize_space(value)
    name = re.sub(r"\s*-\s*Google Scholar\s*$", "", name, flags=re.IGNORECASE).strip()
    name = re.sub(
        r"^(?:prof\.dr\.ir\.|prof\.\s*dr\.-ing\.?|prof\.\s*dr\.?|professor|prof\.?|doctor|dr\.?)\s+",
        "",
        name,
        flags=re.IGNORECASE,
    )

    name = name.replace("（", "(").replace("）", ")")
    name = re.sub(r"\s+fellow\b.*$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+e-agi\b.*$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+(?:ph\.?\s*d\.?|phd|dphil)\.?$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s*,\s*(?:jr\.?|sr\.?|ph\.?\s*d\.?|phd|dphil|aka\b.*|fellow\b.*|.*:.*)$", "", name, flags=re.IGNORECASE)

    if "," in name:
        name = name.split(",", 1)[0]

    def strip_non_ascii_parenthetical(match: re.Match[str]) -> str:
        text = match.group(0)
        return "" if has_non_ascii(text) else text

    name = re.sub(r"\s*\([^()]*\)", strip_non_ascii_parenthetical, name)
    name = re.sub(r"(?<=[a-z])fellow\b.*$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s+fellow\b.*$", "", name, flags=re.IGNORECASE)
    return normalize_space(name)


def clean_affiliation(value: str) -> str:
    affiliation = normalize_space(value)
    affiliation = re.sub(r"(?<=[a-z.]),(?=[A-Z])", ", ", affiliation)
    affiliation = re.sub(r"\s+,", ",", affiliation)
    return affiliation.strip()


def parse_profile_html(body: str) -> dict[str, Any]:
    parser = ScholarProfileParser()
    parser.feed(body)
    parsed = parser.parsed()
    parsed.update(parse_profile_stats(body))
    citation_by_year = parse_citation_by_year(body)
    parsed["first_citation_year"] = min(citation_by_year) if citation_by_year else ""
    parsed["citation_by_year"] = citation_by_year
    return parsed


def strip_tags(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(value or ""))).strip()


def parse_profile_stats(body: str) -> dict[str, str]:
    stats = {column: "" for column in STAT_COLUMNS}
    match = re.search(r'<table[^>]+id=["\']gsc_rsb_st["\'][^>]*>(.*?)</table>', body or "", re.S | re.I)
    if not match:
        return stats

    labels = {"Citations": "citations", "h-index": "h_index", "i10-index": "i10_index"}
    for row_html in re.findall(r"<tr[^>]*>(.*?)</tr>", match.group(1), re.S | re.I):
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, re.S | re.I)
        values = [strip_tags(cell).replace(",", "") for cell in cells]
        if len(values) >= 3 and values[0] in labels:
            base = labels[values[0]]
            stats[base] = values[1]
            stats[f"{base}_since_5y_ago"] = values[2]
    return stats


def parse_citation_by_year(body: str) -> dict[str, int]:
    match = re.search(r'<div class="gsc_md_hist_b">(.*?)</div>', body or "", re.S | re.I)
    if not match:
        return {}

    chart = match.group(1)
    years = [
        (int(right), year)
        for right, year in re.findall(r'<span class="gsc_g_t"[^>]*style="[^"]*right:(\d+)px[^"]*"[^>]*>(\d{4})</span>', chart)
    ]
    if not years:
        return {}

    counts_by_right: dict[int, int] = {}
    for right, bar in re.findall(r'<a[^>]+class="gsc_g_a"[^>]*style="[^"]*right:(\d+)px[^"]*"[^>]*>(.*?)</a>', chart, re.S | re.I):
        label = re.search(r'<span class="gsc_g_al">([^<]*)</span>', bar, re.S | re.I)
        value = strip_tags(label.group(1)).replace(",", "") if label else ""
        counts_by_right[int(right)] = int(value) if value.isdigit() else 0

    series: dict[str, int] = {}
    for year_right, year in years:
        nearby = [count for right, count in counts_by_right.items() if abs(right - year_right) <= 8]
        series[year] = nearby[0] if nearby else 0
    return series


def extract_title(body: str) -> str:
    return parse_profile_html(body).get("title", "")


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


def read_error_body(error: urllib.error.HTTPError) -> str:
    try:
        return decode_body(error.read(), error.headers)
    except (ConnectionError, OSError) as read_error:
        return f"Could not read HTTP error body: {read_error}"


def should_retry(result: dict[str, Any]) -> bool:
    status = result.get("status")
    return (
        status in {"url_error", "timeout"}
        or status == "http_error"
        and result.get("status_code") in TRANSIENT_HTTP_STATUS
    )


def is_transient_failure(result: dict[str, Any]) -> bool:
    return result.get("status") in {"url_error", "timeout"} or (
        result.get("status") == "http_error" and result.get("status_code") in TRANSIENT_HTTP_STATUS
    )


def sleep_seconds(base: float, jitter: float) -> float:
    return max(0.0, base + random.uniform(0, max(0.0, jitter)))


def batch_target(base: int, jitter: int) -> int:
    if jitter <= 0:
        return max(1, base)
    return max(1, base + random.randint(-jitter, jitter))


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
            "html": read_error_body(error),
            "fetched_at": fetched_at,
        }
    except urllib.error.URLError as error:
        return {
            "status": "url_error",
            "error": str(error.reason),
            "title": "",
            "html": "",
            "fetched_at": fetched_at,
        }
    except (TimeoutError, socket.timeout):
        return {"status": "timeout", "title": "", "html": "", "fetched_at": fetched_at}

    parsed = parse_profile_html(body)
    title = parsed.get("title", "")
    if is_blocked_page(body):
        status = "blocked"
    elif not title:
        status = "no_title"
    else:
        status = "ok"

    return {
        "status": status,
        "status_code": status_code,
        "title": title,
        "affiliation": parsed.get("affiliation", ""),
        "interests": parsed.get("interests", []),
        "citations": parsed.get("citations", ""),
        "h_index": parsed.get("h_index", ""),
        "i10_index": parsed.get("i10_index", ""),
        "citations_since_5y_ago": parsed.get("citations_since_5y_ago", ""),
        "h_index_since_5y_ago": parsed.get("h_index_since_5y_ago", ""),
        "i10_index_since_5y_ago": parsed.get("i10_index_since_5y_ago", ""),
        "first_citation_year": parsed.get("first_citation_year", ""),
        "citation_by_year": parsed.get("citation_by_year", {}),
        "html": body,
        "fetched_at": fetched_at,
    }


def fetch_profile(url: str, max_retries: int, backoff: float, backoff_jitter: float) -> dict[str, Any]:
    attempts = 0
    while True:
        result = fetch_profile_once(url)
        if attempts >= max_retries or not should_retry(result):
            if attempts:
                result["attempts"] = attempts + 1
            return result

        pause = sleep_seconds(backoff * (2**attempts), backoff_jitter)
        print(
            f"  transient {result.get('status')} {result.get('status_code') or ''}; "
            f"retrying in {pause:.1f}s",
            flush=True,
        )
        time.sleep(pause)
        attempts += 1


def needs_html_refetch(cached: dict[str, Any]) -> bool:
    return cached.get("status") in HTML_REQUIRED_STATUSES and not cached.get("html")


def enrich_cache_from_html(cache: dict[str, Any]) -> None:
    for cached in cache.values():
        body = cached.get("html")
        if not body:
            continue
        parsed = parse_profile_html(body)
        if parsed.get("title"):
            cached["title"] = parsed["title"]
        cached["affiliation"] = parsed.get("affiliation", "")
        cached["interests"] = parsed.get("interests", [])
        for column in STAT_COLUMNS:
            cached[column] = parsed.get(column, "")
        cached["first_citation_year"] = parsed.get("first_citation_year", "")
        cached["citation_by_year"] = parsed.get("citation_by_year", {})


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
        title = clean_scholar_name(cached.get("title", ""))
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
                "affiliation": cached.get("affiliation", ""),
                "interests": cached.get("interests", []),
                "citations": cached.get("citations", ""),
                "h_index": cached.get("h_index", ""),
                "i10_index": cached.get("i10_index", ""),
                "citations_since_5y_ago": cached.get("citations_since_5y_ago", ""),
                "h_index_since_5y_ago": cached.get("h_index_since_5y_ago", ""),
                "i10_index_since_5y_ago": cached.get("i10_index_since_5y_ago", ""),
                "first_citation_year": cached.get("first_citation_year", ""),
                "citation_by_year": cached.get("citation_by_year", {}),
                "html_cached": bool(cached.get("html")),
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
        "html_cached_profiles": sum(1 for profile in profiles if cache.get(profile.url, {}).get("html")),
        "incomplete_cached_profiles": sum(1 for profile in profiles if needs_html_refetch(cache.get(profile.url, {}))),
        "status_counts": status_counts,
        "mismatch_count": len(mismatches),
        "stats_profiles": sum(
            1
            for profile in profiles
            if cache.get(profile.url, {}).get("citations") and cache.get(profile.url, {}).get("h_index")
        ),
        "mismatches": mismatches,
        "entries": entries,
    }


def crawl_date(cached: dict[str, Any] | None, fallback: str = "") -> str:
    fetched_at = (cached or {}).get("fetched_at", "")
    if re.match(r"\d{4}-\d{2}-\d{2}", fetched_at):
        return fetched_at[:10]
    return fallback


def load_existing_profile_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def output_row_from_cache(name: str, profile_url: str, cached: dict[str, Any] | None, existing: dict[str, str] | None = None) -> dict[str, str]:
    existing = existing or {}
    row = {column: "" for column in PROFILE_CSV_COLUMNS}
    row["name"] = clean_scholar_name((cached or {}).get("title", "")) or existing.get("name", "") or name
    row["profile"] = profile_url
    row["crawl_date"] = crawl_date(cached, existing.get("crawl_date", ""))
    row["affiliation"] = (cached or {}).get("affiliation", existing.get("affiliation", ""))
    row["interests"] = json.dumps((cached or {}).get("interests", []), ensure_ascii=False)
    for column in STAT_COLUMNS:
        row[column] = str((cached or {}).get(column, existing.get(column, "")) or "")
    row["first_citation_year"] = str((cached or {}).get("first_citation_year", existing.get("first_citation_year", "")) or "")
    row["citation_by_year"] = json.dumps((cached or {}).get("citation_by_year", {}), ensure_ascii=False, separators=(",", ":"))
    return row


def write_profile_csv(path: Path, profiles: list[ScholarProfile], cache: dict[str, Any]) -> int:
    output_rows: list[dict[str, str]] = []
    seen: set[str] = set()

    for existing in load_existing_profile_rows(path):
        profile_url = canonical_scholar_url(existing.get("profile", ""))
        if not profile_url or profile_url in seen:
            continue
        cached = cache.get(profile_url)
        output_rows.append(output_row_from_cache(existing.get("name", ""), profile_url, cached, existing))
        seen.add(profile_url)

    for profile in profiles:
        if profile.url in seen:
            continue
        output_rows.append(output_row_from_cache(profile.name, profile.url, cache.get(profile.url)))
        seen.add(profile.url)

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=PROFILE_CSV_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)
    return len(output_rows)


def main() -> int:
    args = parse_args()
    rows = load_rows(args.data)
    profiles = unique_profiles(rows)
    cache: dict[str, Any] = normalize_cache_keys(load_json(args.cache, {}))
    enrich_cache_from_html(cache)
    retry_statuses = set(args.retry_status)

    new_requests = 0
    batch_requests = 0
    current_batch_target = batch_target(args.batch_size, args.batch_size_jitter)

    for position, profile in enumerate(profiles, start=1):
        cached = cache.get(profile.url)
        refetch_status = bool(cached and cached.get("status") in retry_statuses)
        incomplete_cache = bool(cached and needs_html_refetch(cached))
        if cached and not args.refresh and not refetch_status and not incomplete_cache:
            continue

        if args.limit_new is not None and new_requests >= args.limit_new:
            break

        if batch_requests >= current_batch_target:
            pause = sleep_seconds(args.batch_pause, args.batch_pause_jitter)
            print(f"Pausing {pause:.1f}s after {batch_requests} uncached requests.", flush=True)
            time.sleep(pause)
            batch_requests = 0
            current_batch_target = batch_target(args.batch_size, args.batch_size_jitter)

        print(f"[{position}/{len(profiles)}] fetching {profile.name}: {profile.url}", flush=True)
        result = fetch_profile(profile.url, args.max_retries, args.backoff, args.backoff_jitter)
        if cached and is_transient_failure(result):
            cached["last_fetch_error"] = result
            cache[profile.url] = cached
        else:
            cache[profile.url] = result
        new_requests += 1
        batch_requests += 1

        atomic_write_json(args.cache, cache)
        atomic_write_json(args.report, build_report(profiles, cache))

        delay = sleep_seconds(args.delay, args.delay_jitter)
        if delay > 0:
            time.sleep(delay)

    atomic_write_json(args.cache, cache)
    report = build_report(profiles, cache)
    atomic_write_json(args.report, report)
    output_rows = None
    if not args.no_write_csv:
        output_rows = write_profile_csv(args.output, profiles, cache)

    print(
        f"Done. profiles={report['total_profiles']} cached={report['cached_profiles']} "
        f"html_cached={report['html_cached_profiles']} incomplete={report['incomplete_cached_profiles']} "
        f"stats={report['stats_profiles']} mismatches={report['mismatch_count']} report={args.report}"
        + (f" output={args.output} output_rows={output_rows}" if output_rows is not None else ""),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

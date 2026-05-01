#!/usr/bin/env python3
"""Cache CSRankings faculty CSV shards from GitHub.

The script is intentionally conservative:

- cached shards are never fetched again unless --refresh is passed
- each uncached request waits --delay seconds, plus optional --delay-jitter
- every jittered batch of uncached requests, the script pauses for --batch-pause seconds, plus optional jitter
- transient fetch failures are retried with exponential backoff
- the report file is written after every attempted shard so runs can be resumed

The script does not modify the app data files. It only writes local cache and report output.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import socket
import string
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE_DIR = APP_ROOT / ".cache" / "csrankings"
DEFAULT_REPORT = APP_ROOT / ".cache" / "csrankings-report.json"
BASE_URL = "https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/csrankings-{letter}.csv"
EXPECTED_HEADER = ["name", "affiliation", "homepage", "scholarid", "orcid"]
TRANSIENT_HTTP_STATUS = {408, 425, 429, 500, 502, 503, 504}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR, help="Directory for cached csrankings-*.csv files.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="JSON report path.")
    parser.add_argument("--letters", default=",".join(string.ascii_lowercase), help="Comma-separated shard letters to fetch, e.g. a,b,c.")
    parser.add_argument("--refresh", action="store_true", help="Refetch cached shard files.")
    parser.add_argument("--limit-new", type=int, default=None, help="Optional cap on uncached requests this run.")
    parser.add_argument("--delay", type=float, default=0.5, help="Base seconds to wait between uncached requests.")
    parser.add_argument("--delay-jitter", type=float, default=0.5, help="Random extra seconds added to --delay.")
    parser.add_argument("--batch-size", type=int, default=10, help="Base uncached requests per batch.")
    parser.add_argument("--batch-size-jitter", type=int, default=2, help="Random +/- adjustment to --batch-size.")
    parser.add_argument("--batch-pause", type=float, default=10.0, help="Base seconds to pause after each batch.")
    parser.add_argument("--batch-pause-jitter", type=float, default=5.0, help="Random extra seconds added to --batch-pause.")
    parser.add_argument("--max-retries", type=int, default=2, help="Retries for transient fetch failures.")
    parser.add_argument("--backoff", type=float, default=5.0, help="Base seconds for exponential retry backoff.")
    parser.add_argument("--backoff-jitter", type=float, default=2.0, help="Random extra seconds added to retry backoff.")
    return parser.parse_args()


def parse_letters(value: str) -> list[str]:
    letters: list[str] = []
    seen: set[str] = set()
    for raw in value.split(","):
        letter = raw.strip().lower()
        if not letter:
            continue
        if len(letter) != 1 or letter not in string.ascii_lowercase:
            raise ValueError(f"Invalid shard letter: {raw!r}")
        if letter not in seen:
            seen.add(letter)
            letters.append(letter)
    if not letters:
        raise ValueError("At least one shard letter is required.")
    return letters


def atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(value, encoding="utf-8", newline="\n")
    tmp.replace(path)


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def decode_body(body: bytes, headers: Any) -> str:
    charset = headers.get_content_charset() if headers else None
    return body.decode(charset or "utf-8", errors="replace")


def read_error_body(error: urllib.error.HTTPError) -> str:
    try:
        return decode_body(error.read(), error.headers)
    except (ConnectionError, OSError) as read_error:
        return f"Could not read HTTP error body: {read_error}"


def validate_csv(text: str) -> tuple[str, int, str]:
    if not text.strip():
        return "empty", 0, "Downloaded shard is empty."

    try:
        rows = list(csv.reader(text.splitlines()))
    except csv.Error as error:
        return "bad_csv", 0, str(error)

    if not rows:
        return "empty", 0, "Downloaded shard has no CSV rows."
    if rows[0] != EXPECTED_HEADER:
        return "bad_header", max(0, len(rows) - 1), f"Expected {EXPECTED_HEADER!r}, found {rows[0]!r}."
    if len(rows) == 1:
        return "empty", 0, "Downloaded shard has a header but no data rows."
    return "ok", len(rows) - 1, ""


def fetch_shard_once(letter: str) -> dict[str, Any]:
    url = BASE_URL.format(letter=letter)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 Chrome/124 Safari/537.36"
            ),
            "Accept": "text/csv,text/plain,*/*;q=0.8",
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
            "letter": letter,
            "url": url,
            "status": "http_error",
            "status_code": error.code,
            "row_count": 0,
            "error": read_error_body(error)[:500],
            "fetched_at": fetched_at,
        }
    except urllib.error.URLError as error:
        return {
            "letter": letter,
            "url": url,
            "status": "url_error",
            "status_code": None,
            "row_count": 0,
            "error": str(error.reason),
            "fetched_at": fetched_at,
        }
    except (ConnectionError, OSError) as error:
        status = "timeout" if isinstance(error, (TimeoutError, socket.timeout)) else "url_error"
        return {
            "letter": letter,
            "url": url,
            "status": status,
            "status_code": None,
            "row_count": 0,
            "error": str(error),
            "fetched_at": fetched_at,
        }

    status, row_count, error = validate_csv(body)
    return {
        "letter": letter,
        "url": url,
        "status": status,
        "status_code": status_code,
        "row_count": row_count,
        "error": error,
        "body": body,
        "fetched_at": fetched_at,
    }


def should_retry(result: dict[str, Any]) -> bool:
    return result.get("status") in {"url_error", "timeout"} or result.get("status_code") in TRANSIENT_HTTP_STATUS


def fetch_shard(letter: str, max_retries: int, backoff: float, backoff_jitter: float) -> dict[str, Any]:
    attempts = []
    for attempt in range(max_retries + 1):
        result = fetch_shard_once(letter)
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

        wait = sleep_seconds(backoff * (2**attempt), backoff_jitter)
        print(f"Retrying shard {letter} after {wait:.1f}s due to status={result.get('status')}", flush=True)
        time.sleep(wait)

    return result


def sleep_seconds(base: float, jitter: float) -> float:
    return max(0.0, base) + random.uniform(0.0, max(0.0, jitter))


def batch_target(base: int, jitter: int) -> int:
    if jitter <= 0:
        return max(1, base)
    return max(1, base + random.randint(-jitter, jitter))


def cached_entry(letter: str, cache_dir: Path) -> dict[str, Any]:
    path = cache_dir / f"csrankings-{letter}.csv"
    if not path.exists():
        return {
            "letter": letter,
            "url": BASE_URL.format(letter=letter),
            "path": str(path),
            "status": "missing",
            "row_count": 0,
            "cached": False,
        }

    text = path.read_text(encoding="utf-8")
    status, row_count, error = validate_csv(text)
    return {
        "letter": letter,
        "url": BASE_URL.format(letter=letter),
        "path": str(path),
        "status": status,
        "status_code": None,
        "row_count": row_count,
        "error": error,
        "cached": True,
    }


def build_report(letters: list[str], cache_dir: Path, run_entries: dict[str, dict[str, Any]]) -> dict[str, Any]:
    entries = []
    status_counts: dict[str, int] = {}
    for letter in letters:
        entry = dict(run_entries.get(letter) or cached_entry(letter, cache_dir))
        entry.pop("body", None)
        status = entry.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
        entries.append(entry)

    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": "emeryberger/CSrankings gh-pages csrankings-[a-z].csv",
        "base_url": BASE_URL,
        "cache_dir": str(cache_dir),
        "total_shards": len(letters),
        "cached_shards": sum(1 for entry in entries if entry.get("status") == "ok" and Path(entry.get("path", "")).exists()),
        "status_counts": status_counts,
        "entries": entries,
    }


def main() -> int:
    args = parse_args()
    try:
        letters = parse_letters(args.letters)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    run_entries: dict[str, dict[str, Any]] = {}
    new_requests = 0
    batch_requests = 0
    current_batch_target = batch_target(args.batch_size, args.batch_size_jitter)

    for position, letter in enumerate(letters, start=1):
        path = args.cache_dir / f"csrankings-{letter}.csv"
        if path.exists() and not args.refresh:
            continue

        if args.limit_new is not None and new_requests >= args.limit_new:
            break

        if batch_requests >= current_batch_target:
            pause = sleep_seconds(args.batch_pause, args.batch_pause_jitter)
            print(f"Pausing {pause:.1f}s after {batch_requests} uncached requests.", flush=True)
            time.sleep(pause)
            batch_requests = 0
            current_batch_target = batch_target(args.batch_size, args.batch_size_jitter)

        print(f"[{position}/{len(letters)}] fetching csrankings-{letter}.csv", flush=True)
        result = fetch_shard(letter, args.max_retries, args.backoff, args.backoff_jitter)
        if result.get("status") == "ok":
            atomic_write_text(path, result["body"])
            result["path"] = str(path)
            result["cached"] = True
        else:
            result["path"] = str(path)
            result["cached"] = False
        result.pop("body", None)
        run_entries[letter] = result
        new_requests += 1
        batch_requests += 1

        atomic_write_json(args.report, build_report(letters, args.cache_dir, run_entries))

        delay = sleep_seconds(args.delay, args.delay_jitter)
        if delay > 0:
            time.sleep(delay)

    report = build_report(letters, args.cache_dir, run_entries)
    atomic_write_json(args.report, report)
    print(
        f"Done. shards={report['total_shards']} cached={report['cached_shards']} "
        f"statuses={report['status_counts']} report={args.report}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

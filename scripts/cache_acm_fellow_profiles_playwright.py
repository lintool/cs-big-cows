#!/usr/bin/env python3
"""Cache ACM Fellow profile pages with Playwright.

This is a browser-backed companion to cache_acm_fellow_profiles.py. It writes to
the same cache/report files, but fetches pages through Chromium so pages that
need browser JavaScript can be handled without changing the parser/report path.
"""

from __future__ import annotations

import argparse
import random
import sys
import time
from pathlib import Path
from typing import Any

from cache_acm_fellow_profiles import (
    DEFAULT_CACHE,
    DEFAULT_DATA,
    DEFAULT_REPORT,
    atomic_write_json,
    build_report,
    load_json,
    load_rows,
    looks_blocked,
    parse_profile_html,
    unique_profiles,
)


DEFAULT_USER_DATA_DIR = Path(__file__).resolve().parents[1] / ".cache" / "playwright-acm-profile"
RETRY_STATUSES = {"blocked", "http_error", "missing", "no_fellow_award", "no_name", "timeout", "url_error"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="Path to data/acm_fellows.csv.")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="JSON cache path.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="JSON report path.")
    parser.add_argument("--user-data-dir", type=Path, default=DEFAULT_USER_DATA_DIR, help="Persistent browser profile path.")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds to wait between uncached requests.")
    parser.add_argument(
        "--delay-jitter",
        type=float,
        default=0.0,
        help="Random +/- seconds to add around --delay. Sleep is clamped at zero.",
    )
    parser.add_argument("--batch-size", type=int, default=50, help="Uncached requests per batch.")
    parser.add_argument(
        "--batch-size-jitter",
        type=int,
        default=0,
        help="Random +/- requests to add around --batch-size for each batch. Batch size is clamped to at least 1.",
    )
    parser.add_argument("--batch-pause", type=float, default=60.0, help="Seconds to pause after each batch.")
    parser.add_argument(
        "--batch-pause-jitter",
        type=float,
        default=0.0,
        help="Random +/- seconds to add around --batch-pause. Sleep is clamped at zero.",
    )
    parser.add_argument("--limit-batches", type=int, default=None, help="Optional cap on completed batches this run.")
    parser.add_argument("--limit-new", type=int, default=None, help="Optional cap on fetched requests this run.")
    parser.add_argument("--refresh", action="store_true", help="Refetch URLs even when cached.")
    parser.add_argument(
        "--retry-status",
        action="append",
        choices=sorted(RETRY_STATUSES),
        help="Refetch cached entries with this status. Can be passed multiple times.",
    )
    parser.add_argument("--headed", action="store_true", help="Run Chromium visibly.")
    parser.add_argument("--channel", default=None, help="Optional browser channel, for example 'chrome'.")
    parser.add_argument("--cdp-url", default=None, help="Connect to an existing browser over CDP, for example http://127.0.0.1:9222.")
    parser.add_argument("--slow-mo", type=int, default=0, help="Playwright slow motion in milliseconds.")
    parser.add_argument("--timeout", type=int, default=30000, help="Navigation timeout in milliseconds.")
    parser.add_argument("--settle", type=float, default=1.0, help="Seconds to wait after navigation before reading HTML.")
    parser.add_argument("--pause-before-read", action="store_true", help="Wait for Enter before reading page HTML.")
    return parser.parse_args()


def jittered_seconds(base: float, jitter: float) -> float:
    if base <= 0:
        return 0.0
    if jitter <= 0:
        return base
    return max(0.0, base + random.uniform(-jitter, jitter))


def jittered_batch_size(base: int, jitter: int) -> int:
    if base <= 1:
        return 1
    if jitter <= 0:
        return base
    return max(1, base + random.randint(-jitter, jitter))


def import_playwright() -> Any:
    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise SystemExit(
            "Playwright is not installed. Install it with:\n"
            "  python -m pip install playwright\n"
            "  python -m playwright install chromium"
        ) from error
    return sync_playwright, PlaywrightTimeoutError


def cached_status(cache: dict[str, Any], url: str) -> str | None:
    cached = cache.get(url)
    if not cached:
        return None
    status = str(cached.get("status") or "unknown")
    if status == "http_error" and looks_blocked(str(cached.get("html") or "")):
        return "blocked"
    return status


def should_fetch(url: str, cache: dict[str, Any], refresh: bool, retry_statuses: set[str]) -> bool:
    if refresh:
        return True
    status = cached_status(cache, url)
    if status is None:
        return True
    return status in retry_statuses


def cache_entry_from_html(url: str, html: str, status_code: int | None) -> dict[str, Any]:
    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if looks_blocked(html):
        return {"status": "blocked", "status_code": status_code, "html": html, "fetched_at": fetched_at}

    parsed = parse_profile_html(html)
    if not parsed.get("page_name"):
        status = "no_name"
    elif not parsed.get("award_heading"):
        status = "no_fellow_award"
    else:
        status = "ok"

    return {"status": status, "status_code": status_code, "html": html, "fetched_at": fetched_at, **parsed}


def fetch_with_page(
    page: Any,
    url: str,
    timeout: int,
    settle: float,
    pause_before_read: bool,
    playwright_timeout_error: Any,
) -> dict[str, Any]:
    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        try:
            page.wait_for_load_state("networkidle", timeout=min(timeout, 10000))
        except playwright_timeout_error:
            pass
        if pause_before_read:
            print("Complete any browser challenge, then press Enter here to cache the current page.", flush=True)
            input()
        if settle > 0:
            time.sleep(settle)
        html = page.content()
    except playwright_timeout_error:
        return {"status": "timeout", "html": "", "fetched_at": fetched_at}
    except Exception as error:  # Playwright can raise browser-specific transport errors.
        return {"status": "url_error", "error": str(error), "html": "", "fetched_at": fetched_at}

    status_code = response.status if response is not None else None
    entry = cache_entry_from_html(url, html, status_code)
    if status_code is not None and status_code >= 400 and entry["status"] != "blocked":
        entry["status"] = "http_error"
    return entry


def main() -> int:
    args = parse_args()
    sync_playwright, playwright_timeout_error = import_playwright()

    rows = load_rows(args.data)
    profiles = unique_profiles(rows)
    cache: dict[str, Any] = load_json(args.cache, {})
    retry_statuses = set(args.retry_status or [])

    fetched = 0
    batch_requests = 0
    completed_batches = 0
    batch_target = jittered_batch_size(args.batch_size, args.batch_size_jitter)

    with sync_playwright() as playwright:
        browser = None
        if args.cdp_url:
            browser = playwright.chromium.connect_over_cdp(args.cdp_url)
            context = browser.contexts[0] if browser.contexts else browser.new_context(
                viewport={"width": 1440, "height": 1000},
                locale="en-US",
            )
        else:
            args.user_data_dir.mkdir(parents=True, exist_ok=True)
            context = playwright.chromium.launch_persistent_context(
                str(args.user_data_dir),
                channel=args.channel,
                headless=not args.headed,
                slow_mo=args.slow_mo,
                viewport={"width": 1440, "height": 1000},
                locale="en-US",
            )
        page = context.new_page()

        try:
            for position, profile in enumerate(profiles, start=1):
                if not should_fetch(profile.url, cache, args.refresh, retry_statuses):
                    continue

                if args.limit_new is not None and fetched >= args.limit_new:
                    break

                if batch_requests >= batch_target:
                    completed_batches += 1
                    if args.limit_batches is not None and completed_batches >= args.limit_batches:
                        break
                    pause = jittered_seconds(args.batch_pause, args.batch_pause_jitter)
                    print(f"Pausing {pause:.1f}s after {batch_requests} fetched requests.", flush=True)
                    time.sleep(pause)
                    batch_requests = 0
                    batch_target = jittered_batch_size(args.batch_size, args.batch_size_jitter)

                print(f"[{position}/{len(profiles)}] fetching {profile.name}: {profile.url}", flush=True)
                cache[profile.url] = fetch_with_page(
                    page,
                    profile.url,
                    timeout=args.timeout,
                    settle=args.settle,
                    pause_before_read=args.pause_before_read,
                    playwright_timeout_error=playwright_timeout_error,
                )
                fetched += 1
                batch_requests += 1

                atomic_write_json(args.cache, cache)
                atomic_write_json(args.report, build_report(profiles, cache))

                delay = jittered_seconds(args.delay, args.delay_jitter)
                if delay > 0:
                    time.sleep(delay)
        finally:
            if args.cdp_url:
                page.close()
                if browser is not None:
                    browser.close()
            else:
                context.close()

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

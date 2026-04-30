# README For Agents

This repository currently has four agent-oriented utility scripts under `scripts/`:

```text
scripts/cache_acm_fellow_profiles.py
scripts/cache_acm_fellow_profiles_playwright.py
scripts/cache_dblp_profiles.py
scripts/validate_google_scholar_profiles.py
```

Ignore the project `README.md` for these workflows. This file documents the local crawler/validator scripts and their local cache/report files.

## Local Python Environment

Use Python 3.10 or newer from the repository root. The default crawler/validator scripts only use the Python standard library. The Playwright crawler is optional and requires Playwright plus a browser install.

Recommended setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m py_compile scripts/cache_acm_fellow_profiles.py scripts/cache_dblp_profiles.py scripts/validate_google_scholar_profiles.py
```

After activation, run commands with `python ...` from the repo root. If you choose not to create a virtual environment, use `python3 ...` consistently.

`requirements.txt` is retained for now but includes dependencies from older removed experiments. Do not install it just to run the scripts documented here.

Optional Playwright setup:

```bash
python -m pip install playwright
python -m playwright install chromium
```

## Data Layout

Canonical CSV files live under `data/`:

```text
data/acm_fellows.csv
data/google_scholar_profiles.csv
data/turing_award_winners.csv
```

`data/acm_fellows.csv` is the canonical ACM Fellows table. Its current columns are:

```text
name,year,location,citation,acm_fellow_profile,dblp_profile,google_scholar_profile
```

The `name` field should be a clean person name. Do not include leading honorifics such as `Dr.`, `Prof.`, `Professor`, `Mr.`, `Dame`, or trailing credentials such as `PhD`, `Ph.D.`, `DPhil`, or `CCP`.

There is no separate `data/acm_fellow_profiles.csv`. ACM profile URLs and propagated ACM profile metadata belong in `data/acm_fellows.csv`.

Keep committed CSV files on Unix LF line endings. Python's `csv.DictWriter` defaults to CRLF unless `lineterminator="\n"` is supplied.

## ACM Fellows Directory

The ACM Fellows directory is the source list for all ACM Fellows:

```text
https://awards.acm.org/fellows/award-recipients
```

Use this page to discover new ACM Fellows before running profile-page enrichment. The directory provides:

- fellow name in `Last, Given` display order;
- ACM Fellow profile URL;
- ACM Fellows year;
- region.

It does not provide the full citation, DBLP profile, or Google Scholar profile. When adding directory-only rows to `data/acm_fellows.csv`, fill what is available:

- `name`: convert `Last, Given` to clean `Given Last`;
- `year`: directory year;
- `location`: directory region, until the individual profile page provides a more specific location;
- `acm_fellow_profile`: directory profile URL;
- leave `citation`, `dblp_profile`, and `google_scholar_profile` blank if unavailable.

Keep `data/acm_fellows.csv` sorted by `year` descending, then `name` ascending. Most recent Fellows should appear first.

Direct `curl` requests to `awards.acm.org` may return a Cloudflare block page. If that happens, use a browser-capable fetch path or a text-rendered mirror for inspection, and keep any temporary scan reports under `.cache/`. The current local scan report path is:

```text
.cache/acm-fellows-directory-scan.json
```

## ACM Fellow Profile Crawler

`scripts/cache_acm_fellow_profiles.py` caches the `acm_fellow_profile` URLs in the canonical ACM Fellows CSV:

```text
data/acm_fellows.csv
```

The script:

- reads ACM Fellows rows from `data/acm_fellows.csv` by default;
- extracts unique non-empty `acm_fellow_profile` URLs;
- fetches each ACM profile page conservatively;
- caches the complete fetched HTML page for reuse;
- parses the page name, ACM Fellows award heading, location, year, and citation when available;
- normalizes parsed page names by removing leading honorifics such as `Dr.`, `Prof.`, `Professor`, and trailing credentials such as `PhD` / `Ph.D.`;
- compares parsed fields against the CSV row;
- writes a JSON cache and a JSON report;
- does not modify CSV files.

Basic commands:

```bash
python scripts/cache_acm_fellow_profiles.py --limit-new 0
python scripts/cache_acm_fellow_profiles.py
python scripts/cache_acm_fellow_profiles.py --refresh
python scripts/cache_acm_fellow_profiles.py --data path/to/input.csv
```

Compile-check the script:

```bash
python -m py_compile scripts/cache_acm_fellow_profiles.py
```

Default cache path:

```text
.cache/acm-fellow-profile-cache.json
```

Default report path:

```text
.cache/acm-fellow-profile-report.json
```

Absolute paths in the current checkout:

```text
/Users/jimmylin/workspace/cs-big-cows/.cache/acm-fellow-profile-cache.json
/Users/jimmylin/workspace/cs-big-cows/.cache/acm-fellow-profile-report.json
```

The ACM cache is keyed by profile URL. Each value contains the full `html`, fetch metadata, and parsed fields such as:

```json
{
  "status": "ok",
  "status_code": 200,
  "title": "Fellow Name",
  "page_name": "Fellow Name",
  "award_heading": "ACM Fellows",
  "location": "USA",
  "year": "2022",
  "citation": "For contributions ...",
  "html": "<complete fetched HTML page>",
  "fetched_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

Other possible `status` values include:

- `ok`: page fetched and the ACM Fellows award section was parsed.
- `http_error`: ACM returned an HTTP error.
- `blocked`: ACM returned a Cloudflare/interstitial-style page instead of profile content.
- `url_error`: DNS/network/connection failure.
- `timeout`: request timed out.
- `invalid_url`: URL is not HTTP/HTTPS.
- `no_name`: page fetched but no page name was parsed.
- `no_fellow_award`: page fetched but no `ACM Fellows` award section was parsed.

The report contains `review_candidates` for rows where the page did not parse cleanly, or parsed name/year/location/citation differs from the CSV. Treat these as review candidates, not automatic CSV fixes.

When propagating ACM crawl results into `data/acm_fellows.csv`, use only entries whose `status` is `ok`, and do not overwrite existing CSV values with blank parsed fields. The crawled page is newer than the original CSV for `name`, `year`, `location`, and `citation`, but parsed names must remain clean names as described above.

Current ACM profile crawl notes:

- The 2026-04-29 browser/CDP retry resolved all previously cached `blocked` pages.
- The current report has 1,629 `ok` entries, 0 `blocked` entries, and 11 `http_error` entries.
- The 11 `http_error` entries are ACM 404 pages. They are documented in `data_notes.md`.

## DBLP Profile Crawler

`scripts/cache_dblp_profiles.py` caches the `dblp_profile` URLs in the canonical ACM Fellows CSV:

```text
data/acm_fellows.csv
```

The script:

- reads ACM Fellows rows from `data/acm_fellows.csv` by default;
- extracts unique non-empty `dblp_profile` URLs;
- fetches each DBLP profile page with plain Python `urllib`;
- caches the complete fetched HTML page for reuse;
- extracts the DBLP profile title from page metadata, `h1`, or `<title>`;
- compares the expected ACM fellow name against the DBLP title;
- writes a JSON cache and JSON report;
- does not modify CSV files.

Basic commands:

```bash
python scripts/cache_dblp_profiles.py --limit-new 0
python scripts/cache_dblp_profiles.py --limit-new 2
python scripts/cache_dblp_profiles.py
python scripts/cache_dblp_profiles.py --refresh
python scripts/cache_dblp_profiles.py --retry-status http_error --limit-new 3
python scripts/cache_dblp_profiles.py --data path/to/input.csv
```

Compile-check the script:

```bash
python -m py_compile scripts/cache_dblp_profiles.py
```

Default cache path:

```text
.cache/dblp-profile-cache.json
```

Default report path:

```text
.cache/dblp-profile-report.json
```

The DBLP cache is keyed by profile URL. Each value contains the full `html`, fetch metadata, and parsed fields such as:

```json
{
  "status": "ok",
  "status_code": 200,
  "title": "DBLP Profile Title",
  "html": "<complete fetched HTML page>",
  "fetched_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

Other possible `status` values include:

- `ok`: page fetched and a title was extracted.
- `http_error`: DBLP returned an HTTP error.
- `blocked`: fetched page appears to be a bot block/interstitial page.
- `url_error`: DNS/network/connection failure.
- `timeout`: request timed out.
- `invalid_url`: URL is not HTTP/HTTPS.
- `no_title`: page fetched but no usable title was found.

The report contains `review_candidates` for non-`ok` rows and title/name mismatches. Treat these as review candidates, not automatic CSV fixes. The title matcher is intentionally permissive because some DBLP author pages include fuller names than the ACM CSV.

Use `--retry-status STATUS` to retry cached entries with a specific status without refreshing the whole cache. This is useful for revisiting cached `http_error`, `blocked`, or transient failure entries.

## ACM Fellow Playwright Crawler

`scripts/cache_acm_fellow_profiles_playwright.py` is a browser-backed companion to `scripts/cache_acm_fellow_profiles.py`. Use it when direct Python requests return `blocked` pages but the public ACM profile page works in a browser.

It uses the same input CSV, cache, report, parser, and report builder:

```text
data/acm_fellows.csv
.cache/acm-fellow-profile-cache.json
.cache/acm-fellow-profile-report.json
```

Basic commands:

```bash
python scripts/cache_acm_fellow_profiles_playwright.py --limit-new 2
python scripts/cache_acm_fellow_profiles_playwright.py --retry-status blocked --limit-new 2
python scripts/cache_acm_fellow_profiles_playwright.py --headed --retry-status blocked --limit-new 2
python scripts/cache_acm_fellow_profiles_playwright.py --headed --channel chrome --retry-status blocked --limit-new 2
python scripts/cache_acm_fellow_profiles_playwright.py --headed --channel chrome --pause-before-read --retry-status blocked --limit-new 1
python scripts/cache_acm_fellow_profiles_playwright.py --cdp-url http://127.0.0.1:9222 --retry-status blocked --limit-new 2
python scripts/cache_acm_fellow_profiles_playwright.py --cdp-url http://127.0.0.1:9222 --retry-status blocked --delay 4 --delay-jitter 2 --batch-size 25 --batch-size-jitter 5 --batch-pause 90 --batch-pause-jitter 30
python scripts/cache_acm_fellow_profiles_playwright.py --cdp-url http://127.0.0.1:9222 --retry-status blocked --delay 4 --delay-jitter 2 --batch-size 25 --batch-size-jitter 5 --batch-pause 90 --batch-pause-jitter 30 --limit-batches 2
```

The script uses a persistent Chromium profile by default:

```text
.cache/playwright-acm-profile
```

Use `--headed` when ACM requires interactive browser state. If a manual challenge or cookie prompt appears, use `--pause-before-read`, complete the challenge in the opened browser window, then press Enter in the terminal so the script caches the final page HTML. Subsequent runs reuse the same local profile. `--channel chrome` uses an installed Chrome browser instead of the bundled Playwright Chromium when available. Keep the profile under `.cache/` and do not commit it.

If ACM works in a manually launched Chrome profile, connect to it over CDP:

```bash
open -na "Google Chrome" --args --remote-debugging-port=9222 --user-data-dir="$PWD/.cache/chrome-acm-cdp"
python scripts/cache_acm_fellow_profiles_playwright.py --cdp-url http://127.0.0.1:9222 --retry-status blocked --limit-new 2
```

## Google Scholar Validator

`scripts/validate_google_scholar_profiles.py` validates the `google_scholar_profile` URLs in the canonical ACM Fellows CSV:

```text
data/acm_fellows.csv
```

The script:

- reads ACM Fellows rows from `data/acm_fellows.csv` by default;
- extracts unique non-empty `google_scholar_profile` URLs;
- fetches each Scholar profile page conservatively;
- caches the complete fetched HTML page for reuse;
- extracts the Scholar page title;
- compares the expected ACM fellow name against the Scholar title;
- writes a JSON cache and a JSON validation report;
- does not modify CSV files.

The script also still supports the older bundled `*-data.js` format via `--data`, but the canonical input for this repo is now `data/acm_fellows.csv`.

## Basic Commands

Run a no-network report rebuild from existing cache:

```bash
python scripts/validate_google_scholar_profiles.py --limit-new 0
```

Run or resume validation with default pacing:

```bash
python scripts/validate_google_scholar_profiles.py
```

Force refetch of cached URLs:

```bash
python scripts/validate_google_scholar_profiles.py --refresh
```

Use a custom input file:

```bash
python scripts/validate_google_scholar_profiles.py --data path/to/input.csv
```

Compile-check the script:

```bash
python -m py_compile scripts/validate_google_scholar_profiles.py
```

## Cache

The validator uses repo-local cache files by default. From the repo root, the default cache path is:

```text
.cache/google-scholar-validation-cache.json
```

Absolute path in the current checkout:

```text
/Users/jimmylin/workspace/cs-big-cows/.cache/google-scholar-validation-cache.json
```

The cache is a JSON object keyed by Scholar profile URL. Each value contains fields such as:

```json
{
  "status": "ok",
  "status_code": 200,
  "title": "Scholar Profile Title",
  "html": "<complete fetched HTML page>",
  "fetched_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

Other possible `status` values include:

- `ok`: page fetched and a title was extracted.
- `http_error`: Scholar returned an HTTP error, commonly 404.
- `url_error`: DNS/network/connection failure.
- `timeout`: request timed out.
- `invalid_url`: URL is not HTTP/HTTPS.
- `blocked`: fetched page appears to be a Google block/interstitial page.
- `no_title`: page fetched but no usable title was found.

The cache is intentionally idempotent:

- if a URL exists in cache, the script will not fetch it again;
- pass `--refresh` to refetch cached URLs;
- interrupted runs can be resumed safely because the cache is written after every request.

The cache stores complete HTML, so it can become large. `.cache/` is local-only and ignored by Git. If `.cache/` is missing, the validator creates it automatically when it writes the cache/report. A cache-only run with `--limit-new 0` creates an empty cache plus a report without downloading pages.

## Report

Default repo-local report path:

```text
.cache/google-scholar-validation-report.json
```

Absolute path in the current checkout:

```text
/Users/jimmylin/workspace/cs-big-cows/.cache/google-scholar-validation-report.json
```

The report is derived from the input CSV plus the cache. It contains:

- `generated_at`
- `total_profiles`
- `cached_profiles`
- `status_counts`
- `mismatch_count`
- `mismatches`
- `entries`

Each report entry includes:

- `index`: ACM Fellows CSV row number.
- `name`: expected ACM fellow name.
- `url`: Scholar profile URL.
- `acm_profile`: ACM Fellow profile URL.
- `status`: cache status for the Scholar URL.
- `title`: extracted Scholar profile title.
- `match`: `true`, `false`, or `null`.
- `fetched_at`: cache timestamp, when available.

Use report mismatches as review candidates, not automatic fixes. Some mismatches are harmless diacritic or formatting differences, such as `Urs Hoelzle` versus `Urs Hölzle`.

## Cool-Off Strategy

The validator is deliberately slow:

- `--delay` defaults to `5.0` seconds between uncached requests.
- `--batch-size` defaults to `20` uncached requests.
- `--batch-pause` defaults to `120.0` seconds after each batch.
- `--limit-new N` caps uncached requests for one run.

Google Scholar default behavior is therefore:

1. Fetch up to 20 uncached profiles.
2. Wait 5 seconds after each fetch.
3. Pause for 120 seconds after the batch.
4. Write cache and report after every request.

The ACM Fellow profile crawler uses lighter defaults:

- `--delay` defaults to `2.0` seconds between uncached requests.
- `--delay-jitter` defaults to `0.0`; when set, the actual sleep is randomized by plus/minus that many seconds and clamped at zero.
- `--batch-size` defaults to `50` uncached requests.
- `--batch-size-jitter` defaults to `0`; when set, each batch target is randomized by plus/minus that many requests and clamped to at least 1.
- `--batch-pause` defaults to `60.0` seconds after each batch.
- `--batch-pause-jitter` defaults to `0.0`; when set, the actual cooldown is randomized by plus/minus that many seconds and clamped at zero.
- `--limit-new N` caps uncached requests for one run.
- `--limit-batches N` caps completed batches for one run.

The DBLP profile crawler uses plain HTTP by default and adds randomized pacing:

- `--delay` defaults to `2.0` base seconds between uncached requests.
- `--delay-jitter` defaults to `1.0`; the actual delay is `delay + random(0, jitter)`.
- `--batch-size` defaults to `50` uncached requests.
- `--batch-size-jitter` defaults to `5`; each batch target is randomized by plus/minus that many requests and clamped to at least 1.
- `--batch-pause` defaults to `60.0` base seconds after each batch.
- `--batch-pause-jitter` defaults to `15.0`; the actual pause is `batch-pause + random(0, jitter)`.
- `--max-retries` defaults to `2` for transient failures.
- `--backoff` defaults to `10.0` seconds with exponential growth between retries.
- `--backoff-jitter` defaults to `5.0`; retry waits add `random(0, jitter)`.
- `--limit-new N` caps uncached requests for one run.

If Google block markers appear while running the Scholar validator, stop the run and resume later without `--refresh`.

## Google Scholar Block Detection

The script marks a fetched page as `blocked` when the page looks like a Google block/interstitial page. It checks for markers such as:

- `not a robot`
- `unusual traffic`
- `/sorry/`
- `our systems have detected unusual traffic`

Do not flag every occurrence of the word `captcha`: Scholar profile pages can legitimately contain paper titles with that word.

## Git Hygiene

Do not commit these generated artifacts:

```text
.cache/
scripts/__pycache__/
*.pyc
```

The repository `.gitignore` already excludes `.cache/` and Python bytecode.

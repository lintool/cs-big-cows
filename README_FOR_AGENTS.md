# README For Agents

This repository currently has two agent-oriented utility scripts under `scripts/`:

```text
scripts/cache_acm_fellow_profiles.py
scripts/validate_google_scholar_profiles.py
```

Ignore the project `README.md` for these workflows. This file documents the local crawler/validator scripts and their local cache/report files.

## Local Python Environment

Use Python 3.10 or newer from the repository root. The active crawler/validator scripts only use the Python standard library, so no package install is required for the current workflow.

Recommended setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m py_compile scripts/cache_acm_fellow_profiles.py scripts/validate_google_scholar_profiles.py
```

After activation, run commands with `python ...` from the repo root. If you choose not to create a virtual environment, use `python3 ...` consistently.

`requirements.txt` is retained for now but includes dependencies from older removed experiments. Do not install it just to run the scripts documented here.

## ACM Fellow Profile Crawler

`scripts/cache_acm_fellow_profiles.py` caches the `ACM Fellow Profile` URLs in the canonical ACM Fellows CSV:

```text
data/acm-fellows.csv
```

The script:

- reads ACM Fellows rows from `data/acm-fellows.csv` by default;
- extracts unique non-empty `ACM Fellow Profile` URLs;
- fetches each ACM profile page conservatively;
- caches the complete fetched HTML page for reuse;
- parses the page name, ACM Fellows award heading, location, year, and citation when available;
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
  "title": "ACM Award Winner",
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
- `url_error`: DNS/network/connection failure.
- `timeout`: request timed out.
- `invalid_url`: URL is not HTTP/HTTPS.
- `no_name`: page fetched but no page name was parsed.
- `no_fellow_award`: page fetched but no `ACM Fellows` award section was parsed.

The report contains `review_candidates` for rows where the page did not parse cleanly, or parsed name/year/location/citation differs from the CSV. Treat these as review candidates, not automatic CSV fixes.

## ACM Fellow Profile Index

`data/acm-fellow-profiles.csv` is a compact index of ACM Fellow profile URLs derived from `data/acm-fellows.csv` and the ACM profile cache.

Columns:

- `name`: fellow name from the `name` column in `data/acm-fellows.csv`.
- `profile`: ACM Fellow profile URL from the `ACM Fellow Profile` column.
- `crawl_date`: date portion of the cache entry `fetched_at` timestamp.

Regenerate it from the repo root after an ACM profile crawl:

```bash
python - <<'PY'
import csv
import json
from pathlib import Path

input_path = Path("data/acm-fellows.csv")
cache_path = Path(".cache/acm-fellow-profile-cache.json")
output_path = Path("data/acm-fellow-profiles.csv")

cache = json.loads(cache_path.read_text(encoding="utf-8"))
with input_path.open(newline="", encoding="utf-8") as infile:
    rows = list(csv.DictReader(infile))

with output_path.open("w", newline="", encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=["name", "profile", "crawl_date"])
    writer.writeheader()
    for row in rows:
        profile = (row.get("ACM Fellow Profile") or "").strip()
        fetched_at = str(cache.get(profile, {}).get("fetched_at") or "")
        name = (row.get("name") or "").strip()
        writer.writerow({"name": name, "profile": profile, "crawl_date": fetched_at[:10]})
PY
```

## Google Scholar Validator

`scripts/validate_google_scholar_profiles.py` validates the `Google Scholar Profile` URLs in the canonical ACM Fellows CSV:

```text
data/acm-fellows.csv
```

The script:

- reads ACM Fellows rows from `data/acm-fellows.csv` by default;
- extracts unique non-empty `Google Scholar Profile` URLs;
- fetches each Scholar profile page conservatively;
- caches the complete fetched HTML page for reuse;
- extracts the Scholar page title;
- compares the expected ACM fellow name against the Scholar title;
- writes a JSON cache and a JSON validation report;
- does not modify CSV files.

The script also still supports the older bundled `*-data.js` format via `--data`, but the canonical input for this repo is now `data/acm-fellows.csv`.

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
- `--batch-size` defaults to `50` uncached requests.
- `--batch-pause` defaults to `60.0` seconds after each batch.
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

# README For Agents

This repository currently has one agent-oriented utility script under `scripts/`:

```text
scripts/validate_google_scholar_profiles.py
```

Ignore the project `README.md` for this workflow. This file documents only the Google Scholar validator and its local cache/report files.

## Local Python Environment

Use Python 3.10 or newer from the repository root. The active validator script only uses the Python standard library, so no package install is required for the current workflow.

Recommended setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m py_compile scripts/validate_google_scholar_profiles.py
```

After activation, run commands with `python ...` from the repo root. If you choose not to create a virtual environment, use `python3 ...` consistently.

`requirements.txt` is retained for now but includes dependencies from older removed experiments. Do not install it just to run `scripts/validate_google_scholar_profiles.py`.

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

- `index`: ACM Fellows row index.
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

Default behavior is therefore:

1. Fetch up to 20 uncached profiles.
2. Wait 5 seconds after each fetch.
3. Pause for 120 seconds after the batch.
4. Write cache and report after every request.

If block markers appear, stop the run and resume later without `--refresh`.

## Block Detection

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

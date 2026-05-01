---
name: refresh-csrankings
description: Refresh, check, validate, or inspect CSRankings data and rebuild DBLP-aligned CSRankings profiles for the cs-big-cows repository. Use when Codex is asked to refresh CSRankings, crawl CSRankings shards, join CSRankings people to DBLP profiles, create or update data/csrankings_profiles.csv, check or validate CSRankings profiles, or inspect CSRankings-to-DBLP alignment results.
---

# Refresh CSRankings

## Workflow

Use this skill only inside the `cs-big-cows` repository.

1. Check repository status before changing files:

   ```bash
   git status --short --branch
   ```

2. Refresh or inspect the CSRankings cache with `scripts/cache_csrankings.py`.

   - For a full refresh, use:

     ```bash
     python scripts/cache_csrankings.py --refresh
     ```

   - For a small test, use:

     ```bash
     python scripts/cache_csrankings.py --letters a,b --delay 0 --delay-jitter 0
     ```

   - The cache lives under `.cache/csrankings/` and must not be committed.
   - The cache report is `.cache/csrankings-report.json`.

3. Build the DBLP-aligned output:

   ```bash
   python scripts/build_csrankings_profiles.py
   ```

4. Review the printed counts and `.cache/csrankings-profiles-report.json`.

   - `included_rows`: rows written to `data/csrankings_profiles.csv`.
   - `unmatched_dblp_profiles`: DBLP profiles with no high-confidence CSRankings match.
   - `ambiguous_dblp_profiles`: DBLP profiles with multiple high-confidence CSRankings candidates.

5. Summarize suspicious or ambiguous cases for the user. Do not force weak matches into the CSV.

## Output Contract

`data/csrankings_profiles.csv` contains only known DBLP profile rows that align to exactly one CSRankings row. The build helper loops through `data/dblp_profiles.csv` and probes the cached CSRankings rows.

Columns must be:

```text
name,affiliation,homepage,scholarid,orcid,crawl_date,dblp_profile
```

Rules:

- Preserve the original CSRankings column values.
- Set `crawl_date` to the build date unless the user asks for another date.
- Set `dblp_profile` to the aligned DBLP profile URL.
- Exclude unmatched and ambiguous rows.
- Keep committed CSV files on Unix LF line endings with a final newline.

## Matching Policy

Use `scripts/build_csrankings_profiles.py` for deterministic matching.

The helper uses high-confidence matching only:

- normalized full-name exact match first;
- otherwise compatible first name or initial plus matching last name;
- middle initials may be missing;
- honorifics, suffixes, punctuation, diacritics, and excess whitespace are ignored.

If a DBLP profile has zero or multiple CSRankings candidates, leave it out of `data/csrankings_profiles.csv` and report it instead.

## Checking Or Validating Profiles

When the user asks to check or validate CSRankings profiles, join `data/csrankings_profiles.csv` with `data/dblp_profiles.csv` on `dblp_profile` and flag suspicious rows.

Validation means:

- Compare the CSRankings `name` against the joined DBLP `name`.
- Treat minor variations as acceptable, including accent characters, diacritics, periods, punctuation, initials, spacing, hyphens, and capitalization.
- Flag rows where the names appear to be different people after those minor variations are normalized.
- Include enough context for review: CSRankings name, DBLP name, affiliation, DBLP profile URL, and why it looks suspicious.
- Do not modify CSV files during validation unless the user explicitly asks for fixes.

## Guardrails

- Do not edit `data/dblp_profiles.csv` unless the user explicitly asks.
- Do not commit `.cache/` artifacts.
- Treat alignment counts as a review surface; investigate surprising drops in `included_rows`.
- If the CSRankings cache is incomplete and the user asked for a full refresh, run `scripts/cache_csrankings.py --refresh` before rebuilding the output.

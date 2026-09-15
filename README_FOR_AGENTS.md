# README for Agents

Follow [AGENTS.md](AGENTS.md) for documentation audiences.
[README.md](README.md) is the human entry point; this file owns application maintenance workflows and constraints.
Keep dataset provenance, reconciliation history, and deliberate source differences in [Data Notes](docs/data_notes.md).

This repository owns canonical data, application-specific joins, analysis, and visualization.
All crawlers live in [bigcows-crawler](https://github.com/lintool/bigcows-crawler).
Its [agent reference](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md) is authoritative for transport, pacing, retries, manifests, cache schemas, and troubleshooting.

## Crawlers

### Repository Layout

Use Python 3.10 or newer, available as `python`.
Run the commands below from `cs-big-cows`, with `bigcows-crawler` checked out beside it.
Crawl artifacts default to the shared crawler's `.cache/`, independent of the working directory; they are Git-ignored and absent from a fresh clone.
Explicit relative paths resolve from the working directory.
This application's `.cache/` holds derived analysis and alignment artifacts.
The CSRankings builder accepts `--cache-dir` if the shared shard cache is elsewhere.

### Review Existing ACM Captures

Select the date of an available local crawl.
The example date below is illustrative; [Data Notes](docs/data_notes.md) records each award's latest reviewed crawl and retained artifacts.
These commands reparse HTML without fetching or changing crawl records:

```bash
python ../bigcows-crawler/scripts/compare_acm_fellow_profiles.py --crawl-date 2026-09-13 --data data/acm_fellows.csv
python ../bigcows-crawler/scripts/compare_acm_fellow_profiles.py --award turing --crawl-date 2026-09-13 --data data/turing_award_winners.csv
```

The current CSV may differ from the crawl's original input snapshot.
Compare the current CSV, but resume fetching only with the original snapshot.
If no suitable cache is available locally, prepare and run a new crawl as described below.
To save comparison output, add `--output` with a new path under the shared `.cache/`; existing files cannot be overwritten.
Without it, JSON goes to stdout.
See [report interpretation](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md#reports-and-data-review) for exact differences, name compatibility, missing captures, and duplicate URLs.
The crawler's `--limit-new 0` mode writes crawl artifacts and is not this audit.

### Prepare, Start, and Resume an ACM Crawl

Read the shared [ACM workflow](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md#acm-fellow-and-turing-award-profile-crawler) and [Safari setup](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md#safari-setup-and-lifecycle) before fetching.
Both awards use the same runner; `--award turing` is required for Turing years and citations.
They can share a cache directory and start date because their artifact prefixes differ.

Choose an unused crawl start date and replace the example date in every path and argument.
Save a stable input snapshot before preparation.
`cp -n` preserves an existing snapshot if repeated.
Prepare only the award you intend to crawl:

```bash
mkdir -p ../bigcows-crawler/.cache
cp -n data/acm_fellows.csv ../bigcows-crawler/.cache/acm-fellow-profile-input-2026-09-14.csv
python ../bigcows-crawler/scripts/cache_acm_fellow_profiles_safari.py --crawl-date 2026-09-14 --data ../bigcows-crawler/.cache/acm-fellow-profile-input-2026-09-14.csv --prepare-only
```

For Turing Award winners:

```bash
mkdir -p ../bigcows-crawler/.cache
cp -n data/turing_award_winners.csv ../bigcows-crawler/.cache/acm-turing-profile-input-2026-09-14.csv
python ../bigcows-crawler/scripts/cache_acm_fellow_profiles_safari.py --award turing --crawl-date 2026-09-14 --data ../bigcows-crawler/.cache/acm-turing-profile-input-2026-09-14.csv --prepare-only
```

Preparation does not open Safari or fetch pages.
Remove `--prepare-only` to start, then repeat that command with the same date and snapshot to resume.
Keep the original date across midnight and retain all crawl artifacts.
Do not add `--refresh` when resuming.
If the start is postponed to a later date, prepare a new crawl for that date.
See the shared reference for pacing and progress; a completed invocation alone does not mean every profile succeeded or matched.

### Other Sources

These commands fetch pages or shards; the Scholar command also writes its explicitly selected export, and the builder writes the application's alignment:

```bash
python ../bigcows-crawler/scripts/cache_dblp_profiles.py --data data/acm_fellows.csv
python ../bigcows-crawler/scripts/cache_google_scholar_profiles.py --data data/acm_fellows.csv --output data/google_scholar_profiles.csv
python ../bigcows-crawler/scripts/cache_csrankings.py
python scripts/build_csrankings_profiles.py
```

For Turing Award Scholar profiles, use `--data data/turing_award_winners.csv` with the same export path.
Omit `--output` to update only the Scholar cache/report.
Add `--limit-new 0` for a cache-only rebuild; this still writes reports and any explicitly requested Scholar export.
Follow the shared reference for source pacing and retries.

### Apply Reviewed ACM Results

The ACM crawlers never update canonical CSVs.
Verify the person and award using the captured HTML, and inspect exact differences as well as name compatibility.
Use successful captures as evidence; preserve existing values when source fields are blank, truncated, malformed, or otherwise less accurate.
A recent fetch is not automatically more authoritative than the reviewed CSV.
Follow the data conventions below and record dataset-specific decisions in [Data Notes](docs/data_notes.md).

## Data Layout

Canonical CSV files live under `data/`:

```text
data/acm_fellows.csv
data/csrankings_profiles.csv
data/dblp_profiles.csv
data/google_scholar_profiles.csv
data/turing_award_winners.csv
```

`data/acm_fellows.csv` is the canonical ACM Fellows table.
Its current columns are:

```text
name,year,location,citation,acm_fellow_profile,dblp_profile,google_scholar_profile
```

The `name` field should be a clean person name.
Do not include leading honorifics such as `Dr.`, `Prof.`, `Professor`, `Mr.`, `Dame`, or trailing credentials such as `PhD`, `Ph.D.`, `DPhil`, or `CCP`.

There is no separate `data/acm_fellow_profiles.csv`.
ACM profile URLs and propagated ACM profile metadata belong in `data/acm_fellows.csv`.

`data/turing_award_winners.csv` uses the same columns.
Its `year` is the Turing Award year, not the announcement year or Fellowship year.
Its `acm_fellow_profile` column holds the ACM recipient URL for compatibility with the shared crawler; always select `--award turing` when crawling or comparing this dataset.

`data/csrankings_profiles.csv` contains CSRankings faculty rows that align to exactly one known DBLP profile from `data/dblp_profiles.csv`.
Its columns are:

```text
name,affiliation,homepage,scholarid,orcid,crawl_date,dblp_profile
```

Keep committed CSV files on Unix LF line endings.
Python's `csv.DictWriter` defaults to CRLF unless `lineterminator="\n"` is supplied.

## ACM Fellows Directory

The ACM Fellows directory is the source list for all ACM Fellows:

```text
https://awards.acm.org/fellows/award-recipients
```

Use this page to discover new ACM Fellows before running profile-page enrichment.
The directory provides:

- fellow name in `Last, Given` display order;
- ACM Fellow profile URL;
- ACM Fellows year;
- region.

It does not provide the full citation, DBLP profile, or Google Scholar profile.
When adding directory-only rows to `data/acm_fellows.csv`, fill what is available:

- `name`: convert `Last, Given` to clean `Given Last`;
- `year`: directory year;
- `location`: directory region, until the individual profile page provides a more specific location;
- `acm_fellow_profile`: directory profile URL;
- leave `citation`, `dblp_profile`, and `google_scholar_profile` blank if unavailable.

Keep `data/acm_fellows.csv` sorted by `year` descending, then `name` ascending.
Most recent Fellows should appear first.

The profile crawler consumes existing URLs; it does not discover Fellows from this directory.
Inspect the directory separately in regular Safari if direct HTTP requests are blocked, and keep any directory scan reports under `../bigcows-crawler/.cache/`, for example:

```text
../bigcows-crawler/.cache/acm-fellows-directory-scan-YYYY-MM-DD.json
```

## CSRankings DBLP Alignment

`scripts/build_csrankings_profiles.py` builds `data/csrankings_profiles.csv` from known DBLP profiles and cached CSRankings shards.

The script:

- reads `../bigcows-crawler/.cache/csrankings/csrankings-[a-z].csv`;
- reads `data/dblp_profiles.csv`;
- loops through DBLP profiles and includes only profiles that align to exactly one CSRankings row;
- preserves the original CSRankings columns;
- appends `crawl_date` and `dblp_profile`;
- writes `.cache/csrankings-profiles-report.json` with included, unmatched DBLP, and ambiguous DBLP counts.

Basic commands:

```bash
python scripts/build_csrankings_profiles.py
python scripts/build_csrankings_profiles.py --crawl-date 2026-05-01
python scripts/build_csrankings_profiles.py --cache-dir path/to/csrankings-cache --output data/csrankings_profiles.csv
```

Compile-check the script:

```bash
python -m py_compile scripts/build_csrankings_profiles.py
```

The output CSV columns are:

```text
name,affiliation,homepage,scholarid,orcid,crawl_date,dblp_profile
```

The matching policy is conservative.
The script normalizes names by ignoring case, punctuation, diacritics, common honorifics, suffixes, and excess whitespace.
It accepts exact normalized name matches and compatible first-name/initial plus last-name matches.
It excludes unmatched and ambiguous rows instead of writing weak guesses.

The alignment report is `.cache/csrankings-profiles-report.json`.
It contains:

- `generated_at`
- `cache_dir`
- `dblp_profiles`
- `output`
- `crawl_date`
- `csrankings_rows`
- `dblp_profiles_rows`
- `included_rows`
- `unmatched_dblp_profiles`
- `ambiguous_dblp_profiles`
- `unmatched_sample`
- `ambiguous`

When asked to check or validate CSRankings profiles, join `data/csrankings_profiles.csv` with `data/dblp_profiles.csv` on `dblp_profile` and flag suspicious name mismatches.
Names should match modulo minor variations such as accent characters, diacritics, periods, punctuation, initials, spacing, hyphens, and capitalization.
For suspicious rows, report the CSRankings name, DBLP name, affiliation, DBLP profile URL, and why it looks like a different person.
Do not modify CSV files during validation unless the user explicitly asks.

Use the repo-local skill `skills/refresh-csrankings` when asked to refresh CSRankings and rebuild this DBLP-aligned output.

## ACM Fellow University Analysis

`scripts/analyze_acm_fellow_universities.py` counts ACM Fellow university affiliations from joined Google Scholar and CSRankings profile data.

The script:

- reads `data/acm_fellows.csv`;
- joins Google Scholar affiliations through `google_scholar_profile`;
- joins CSRankings affiliations through `dblp_profile`;
- extracts university-like organizations from both affiliation fields;
- normalizes common university variants;
- counts every distinct normalized university found per fellow;
- prints a count-descending plain text table.

Basic commands:

```bash
python scripts/analyze_acm_fellow_universities.py
python scripts/analyze_acm_fellow_universities.py --min-count 5
python scripts/analyze_acm_fellow_universities.py --examples 3
python scripts/analyze_acm_fellow_universities.py --show-warnings
python scripts/analyze_acm_fellow_universities.py --show-warnings --warnings-limit 100
```

Compile-check the script:

```bash
python -m py_compile scripts/analyze_acm_fellow_universities.py
```

Counting semantics:

- A fellow can count toward multiple universities if Scholar and CSRankings provide distinct universities.
- The same normalized university from multiple sources counts once per fellow.
- Companies and generic job titles should not be counted as universities.
- Common variants such as `MIT`, `Massachusetts Inst. of Technology`, `CMU`, `UC Berkeley`, `UCLA`, `UIUC`, `Georgia Tech`, and `UBC` are normalized.
- Preserve `University of British Columbia` as distinct from `Columbia University`.
- The helper prints normalization warnings to stderr with `--show-warnings` when it suppresses ambiguous captures such as generic parent institutions or substring collisions.
  Use `--warnings-limit N` to control how many warnings are shown.

Use the repo-local skill `skills/analyze-acm-fellows` when asked about ACM Fellow university distribution or affiliation counts.

## Google Scholar Citation Visualization

`scripts/build_scholar_citation_visualization.py` regenerates the static ACM Fellow citation timeline:

```text
docs/scholar_citations.html
```

The generator:

- reads `data/acm_fellows.csv`;
- joins Scholar rows from `data/google_scholar_profiles.csv` by `google_scholar_profile`;
- embeds the joined data directly in the output HTML;
- sorts rows by ACM Fellows `year` descending, then `name` ascending;
- renders one row per ACM Fellow;
- hides rows without Scholar citation-by-year data by default;
- provides a `Show missing Scholar data` checkbox and author search box;
- shows citations and h-index as separate right-aligned columns;
- renders per-author citation-by-year bars with the most recent year at the right edge.

Regenerate the visualization after changing ACM Fellow rows or Scholar citation fields:

```bash
python scripts/build_scholar_citation_visualization.py
```

Use custom paths only for testing:

```bash
python scripts/build_scholar_citation_visualization.py --acm path/to/acm_fellows.csv --scholar path/to/google_scholar_profiles.csv --output path/to/scholar_citations.html
```

Compile-check the script:

```bash
python -m py_compile scripts/build_scholar_citation_visualization.py
```

The generated HTML is pure static HTML with embedded data, but it loads D3 v7 from a CDN.
Opening the file directly in a browser is enough for local inspection when network access to the CDN is available.
Commit the regenerated HTML when the source data or generator changes.

## Git Hygiene

Do not commit these generated artifacts:

```text
.cache/
scripts/__pycache__/
*.pyc
```

The repository `.gitignore` already excludes `.cache/` and Python bytecode.

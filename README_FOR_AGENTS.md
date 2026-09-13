# README For Agents

This repository owns the canonical data, application-specific joins, analysis,
and visualization. All crawlers live in the sibling `bigcows-crawler`
repository. See [its README](https://github.com/lintool/bigcows-crawler/blob/main/README.md) and
[crawler reference](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md) for fetch, retry,
browser, cache, and report behavior.

## Crawlers

Use Python 3.10 or newer. Run the following commands from `cs-big-cows`.
The ACM comparison requires the retained September 13 cache and manifest in
`../bigcows-crawler/.cache/`; these Git-ignored artifacts are not included in
either clone. In a fresh checkout, start with the fresh-crawl command below,
then compare using the date of that crawl.

```bash
python3 ../bigcows-crawler/scripts/compare_acm_fellow_profiles.py --crawl-date 2026-09-13 --data data/acm_fellows.csv
python3 ../bigcows-crawler/scripts/cache_dblp_profiles.py --data data/acm_fellows.csv
python3 ../bigcows-crawler/scripts/cache_google_scholar_profiles.py --data data/acm_fellows.csv --output data/google_scholar_profiles.csv
python3 ../bigcows-crawler/scripts/cache_csrankings.py
python3 scripts/build_csrankings_profiles.py
```

ACM profile fetching uses regular Safari through AppleScript on macOS. Allow the
launching app to control Safari when prompted; leave the crawler's dedicated
window open. See the shared reference for setup, pacing, retries, and progress.
For a fresh recrawl that preserves the existing cache:

```bash
python3 ../bigcows-crawler/scripts/cache_acm_fellow_profiles_safari.py --crawl-date 2026-09-14 --data data/acm_fellows.csv
```

The first ACM command above compares existing captures; it does not fetch or write
crawl artifacts. Use a new crawl start date for each fresh run; the date selects
matching cache, report, state, and manifest files under the shared `.cache/`.
Repeat the same fetch command with unchanged input contents to resume,
retaining the start date even across midnight;
`--refresh` would refetch successful entries again. Safari entries store HTML and
parsed metadata but have `status_code: null` because HTTP status is unavailable.
There is no undated default or automatic latest-crawl selection. Use the date in
[data_notes.md](data_notes.md) for the latest reviewed crawl. Explicit `--cache`,
`--report`, and `--state` overrides remain available; override all three for
independent runs on the same date. Each unspecified path still uses the date.
The manifest binds a crawl to its input checksum. For longer crawls, save and use
an input snapshot under the shared `.cache/`, named
`acm-fellow-profile-input-YYYY-MM-DD.csv`. Input snapshots and logs are caller-managed.
The retained September crawl is bound to its original snapshot, not the CSV after
the later name corrections. Compare the current CSV with it using the command above;
do not resume that crawl using the edited CSV.

Add `--limit-new 0` to a fetch command to rebuild its report from cache without
fetching. This still writes cache/report output, and the Scholar command above
also writes its explicitly requested CSV. Omit `--output` to only update the
Scholar cache/report. To crawl Google Scholar profiles for Turing Award winners,
pass `--data data/turing_award_winners.csv` to the Scholar crawler. The ACM Fellow
profile crawler only parses the ACM Fellows award section; it is not a Turing
Award crawler.

Crawl caches and crawl reports default to `../bigcows-crawler/.cache/`, independent
of the working directory. Explicit relative overrides resolve from the working
directory; keep them under the shared crawler's `.cache/`. This application's
`.cache/` only holds derived analysis/alignment artifacts. Both caches are ignored by Git. The CSRankings
builder defaults to the sibling crawler's shard cache; use `--cache-dir` if the
repositories are checked out elsewhere.

The ACM crawlers never update the canonical CSV. When applying reviewed ACM
results, verify the person and award using `status: ok` entries and the captured
HTML. Preserve existing values when ACM's fields are blank, truncated, malformed,
or otherwise less accurate, and keep names clean as described below. A recent
fetch is not automatically more authoritative than the reviewed CSV.

Use the comparison command to review exact name differences as well as name
compatibility, blank CSV URLs, missing cache entries, and duplicate URLs. It
reparses HTML and leaves original crawl records unchanged. The crawler's own
`--limit-new 0` mode still writes progress/report output for its bound input and
uses stored parsed fields; it is not the audit command. Keep dataset-specific decisions and
source reconciliation in [data_notes.md](data_notes.md).

With the retained September 13 artifacts available locally, save a comparison
to a new local file as follows. For another crawl, change both dates to its start
date. Existing files are never overwritten; omit `--output` to print JSON to stdout:

```bash
python3 ../bigcows-crawler/scripts/compare_acm_fellow_profiles.py --crawl-date 2026-09-13 --data data/acm_fellows.csv --output ../bigcows-crawler/.cache/acm-fellow-profile-comparison-2026-09-13.json
```

## Data Layout

Canonical CSV files live under `data/`:

```text
data/acm_fellows.csv
data/csrankings_profiles.csv
data/dblp_profiles.csv
data/google_scholar_profiles.csv
data/turing_award_winners.csv
```

`data/acm_fellows.csv` is the canonical ACM Fellows table. Its current columns are:

```text
name,year,location,citation,acm_fellow_profile,dblp_profile,google_scholar_profile
```

The `name` field should be a clean person name. Do not include leading honorifics such as `Dr.`, `Prof.`, `Professor`, `Mr.`, `Dame`, or trailing credentials such as `PhD`, `Ph.D.`, `DPhil`, or `CCP`.

There is no separate `data/acm_fellow_profiles.csv`. ACM profile URLs and propagated ACM profile metadata belong in `data/acm_fellows.csv`.

`data/csrankings_profiles.csv` contains CSRankings faculty rows that align to exactly one known DBLP profile from `data/dblp_profiles.csv`. Its columns are:

```text
name,affiliation,homepage,scholarid,orcid,crawl_date,dblp_profile
```

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

The profile crawler consumes existing URLs; it does not discover Fellows from
this directory. Inspect the directory separately in regular Safari if direct
HTTP requests are blocked, and keep any directory scan reports under
`../bigcows-crawler/.cache/`, for example:

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

The matching policy is conservative. The script normalizes names by ignoring case, punctuation, diacritics, common honorifics, suffixes, and excess whitespace. It accepts exact normalized name matches and compatible first-name/initial plus last-name matches. It excludes unmatched and ambiguous rows instead of writing weak guesses.

The alignment report is `.cache/csrankings-profiles-report.json`. It contains:

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

When asked to check or validate CSRankings profiles, join `data/csrankings_profiles.csv` with `data/dblp_profiles.csv` on `dblp_profile` and flag suspicious name mismatches. Names should match modulo minor variations such as accent characters, diacritics, periods, punctuation, initials, spacing, hyphens, and capitalization. For suspicious rows, report the CSRankings name, DBLP name, affiliation, DBLP profile URL, and why it looks like a different person. Do not modify CSV files during validation unless the user explicitly asks.

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
- The helper prints normalization warnings to stderr with `--show-warnings` when it suppresses ambiguous captures such as generic parent institutions or substring collisions. Use `--warnings-limit N` to control how many warnings are shown.

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

The generated HTML is pure static HTML with embedded data, but it loads D3 v7 from a CDN. Opening the file directly in a browser is enough for local inspection when network access to the CDN is available. Commit the regenerated HTML when the source data or generator changes.

## Git Hygiene

Do not commit these generated artifacts:

```text
.cache/
scripts/__pycache__/
*.pyc
```

The repository `.gitignore` already excludes `.cache/` and Python bytecode.

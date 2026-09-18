# README For Agents

Follow [AGENTS.md](AGENTS.md) for documentation audiences.
[README.md](README.md) is the human entry point; this file owns application maintenance workflows and constraints.
Keep dataset provenance, reconciliation history, and deliberate source differences in [Data Notes](docs/data_notes.md).

This repository owns canonical data, application-specific joins, analysis, and visualization.
All crawlers live in [bigcows-crawler](https://github.com/lintool/bigcows-crawler).
Its [agent reference](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md) is authoritative for transport, pacing, retries, manifests, cache schemas, and troubleshooting.

## Crawlers

### Repository Layout

Use Python 3.10 or newer, available as `python`.
Run the commands below from `acm-bigcows`, with `bigcows-crawler` checked out beside it.
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

These commands fetch DBLP pages or CSRankings shards; the builder writes the application's alignment:

```bash
python ../bigcows-crawler/scripts/cache_dblp_profiles.py --data data/acm_fellows.csv
python ../bigcows-crawler/scripts/cache_csrankings.py
python scripts/build_csrankings_profiles.py
```

Follow the shared reference for source pacing and retries.
For Scholar, use the reviewed workflow below rather than exporting directly into the canonical CSV.

### Review and Import Google Scholar Data

The shared crawler handles transport and parsing; this repository owns identity decisions and canonical imports.
Read its [Scholar workflow](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md#google-scholar-profile-crawler) for pacing, retries, cache fields, and blocking behavior.
The crawler's generic CSV exporter retains existing output rows and can reuse historical values; it does not enforce fresh-only acceptance or establish a person's identity.
Do not use `--output data/google_scholar_profiles.csv` as the review or import step.

1. **Define the refresh scope and retain inputs:** Create a new run directory under `../bigcows-crawler/.cache/` and snapshot both award rosters and the current shared statistics CSV there.
   Record which roster or rosters will be refreshed, the start time, and the selected commands in the run manifest.
   Keep original inputs stable for resuming; record newly discovered candidates in a separate input file.
2. **Crawl into a fresh cache without canonical output:** An unused cache makes this a fresh capture rather than reuse of the default historical cache.
   For both awards, share the new cache so a profile common to both is fetched once, and retain separate reports and logs.
   The following example starts a new combined run; replace the placeholder with a unique run label and create the directory only once:

   ```bash
   (
     set -e
     scholar_run=../bigcows-crawler/.cache/scholar-refresh-YYYY-MM-DD-HHMM
     mkdir -p ../bigcows-crawler/.cache
     mkdir "$scholar_run"
     cp data/acm_fellows.csv "$scholar_run/fellows-input.csv"
     cp data/turing_award_winners.csv "$scholar_run/turing-input.csv"
     cp data/google_scholar_profiles.csv "$scholar_run/statistics-before.csv"
     python -u ../bigcows-crawler/scripts/cache_google_scholar_profiles.py --data "$scholar_run/fellows-input.csv" --cache "$scholar_run/cache.json" --report "$scholar_run/fellows-report.json" > "$scholar_run/fellows.log" 2>&1
     python -u ../bigcows-crawler/scripts/cache_google_scholar_profiles.py --data "$scholar_run/turing-input.csv" --cache "$scholar_run/cache.json" --report "$scholar_run/turing-report.json" > "$scholar_run/turing.log" 2>&1
   )
   ```

   The subshell stops on command failure, including an existing run directory, before later commands can overwrite retained inputs or logs.
   Run only the selected award command for a single-roster refresh.
   Monitor the active run and stop on blocking; do not start the next award while a block is unresolved.
   Resume using the same snapshots and cache without `--refresh`, retaining previous logs and using a new log filename for each attempt.
   `--limit-new 0` rebuilds a report without fetching, but still writes cache/report artifacts and does not establish freshness.
3. **Review freshness and identity:** Require a successful capture from the selected run with complete HTML, parsed statistics, and a supported identity before accepting a profile.
   Check capture timestamps and recorded fetch errors; a retained older success is not evidence of a successful current refresh.
   Compare names, affiliations, research areas, and representative publications against ACM and primary institutional sources.
   A compatible name or HTTP 200 response alone is insufficient.
4. **Resolve missing and rejected links:** Search for replacement profiles when discovery is in scope, then freshly crawl and verify candidates before accepting them.
   Leave the Scholar field blank if no fresh, verified replacement can be found; do not fill the gap with historical statistics.
   Treat a blocked or interrupted run as incomplete, rather than clearing links solely because of a temporary access failure.
   Record accepted, rejected, unresolved, and deferred decisions with evidence and capture references.
5. **Reconcile and import across both rosters:** Build the accepted statistics set by unique Scholar URL, with one record for a person shared by the awards.
   Apply reviewed link changes without altering unrelated award fields, then replace or add statistics only from accepted captures.
   Remove rejected or obsolete statistics records only after confirming that neither roster still references them.
   Preserve reviewed records outside a single-award refresh's scope, with their original crawl dates; never describe those as newly refreshed.
   The generic exporter is not a reviewed importer: use a reviewed run-specific import script or prepare an explicit import for review, retaining it and the before/after evidence in the run directory.
6. **Validate and publish the data snapshot:** Check unique profile URLs, roster joins, accepted capture coverage, actual crawl dates, missing-value semantics, unchanged unrelated fields, canonical sort order, and LF line endings.
   Record results and unresolved issues in [Data Notes](docs/data_notes.md).
   Once the data refresh is ready for display, regenerate both award datasets and run the checks in the [visualization workflow](#google-scholar-citation-visualization), since shared statistics can affect both pages.

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
data/google_scholar_profiles.csv
data/turing_award_winners.csv
```

`data/acm_fellows.csv` is the canonical ACM Fellows table.
Its current columns are:

```text
name,year,location,citation,acm_fellow_profile,dblp_profile,dblp_crawl_date,google_scholar_profile
```

The `name` field should be a clean person name.
Do not include leading honorifics such as `Dr.`, `Prof.`, `Professor`, `Mr.`, `Dame`, or trailing credentials such as `PhD`, `Ph.D.`, `DPhil`, or `CCP`.

There is no separate `data/acm_fellow_profiles.csv`.
ACM profile URLs and propagated ACM profile metadata belong in `data/acm_fellows.csv`.

`data/turing_award_winners.csv` uses the same columns.
Its `year` is the Turing Award year, not the announcement year or Fellowship year.
Its `acm_fellow_profile` column holds the ACM recipient URL for compatibility with the shared crawler; always select `--award turing` when crawling or comparing this dataset.

Both award rosters store `dblp_crawl_date` beside `dblp_profile`.
It is the accepted successful capture's UTC date (`YYYY-MM-DD`), derived from `fetched_at`, not the import date.
Keep it blank when the DBLP URL is blank or no successful capture has been accepted for that URL.
When a DBLP URL changes or is cleared, clear its old crawl date and populate a new date only from an accepted capture of the new URL.
For URLs shared across the two rosters, update both dates together and keep them identical.
A crawl date records successful capture, not a guarantee of identity or publication attribution.
Full timestamps, HTML and validation evidence remain in the shared crawler cache.
The distinct nonempty DBLP URLs across both rosters define the known DBLP profiles; there is no separate canonical DBLP table.

`data/csrankings_profiles.csv` contains CSRankings faculty rows that align to exactly one known DBLP profile from the two award rosters.
Its columns are:

```text
name,affiliation,homepage,scholarid,orcid,crawl_date,dblp_profile
```

Keep committed CSV files on Unix LF line endings.
Python's `csv.DictWriter` defaults to CRLF unless `lineterminator="\n"` is supplied.

### Google Scholar Statistics

`data/google_scholar_profiles.csv` stores one row per unique Scholar `profile` URL across both award rosters.
Join each roster's `google_scholar_profile` to this `profile` field; names are descriptive fields, not join keys.

| Field | Meaning |
| --- | --- |
| `name` | Parsed Scholar display name; it may differ from the canonical award name. |
| `profile` | Canonical Scholar author URL, containing the `user` ID. |
| `crawl_date` | UTC capture date (`YYYY-MM-DD`), derived from the accepted capture's `fetched_at`; not the import date. |
| `affiliation` | Profile-reported affiliation text; not verified employment history. |
| `interests` | JSON array of research-interest strings stored inside a CSV cell. |
| `citations` | Scholar's reported all-time citation count. |
| `h_index` | Scholar's reported all-time h-index. |
| `i10_index` | Scholar's reported all-time count of publications with at least ten citations. |
| `citations_since_5y_ago`, `h_index_since_5y_ago`, `i10_index_since_5y_ago` | Values from Scholar's recent-period column at capture time; these are not recalculated from yearly bars. |
| `first_citation_year` | Earliest year in the captured citation histogram, not necessarily the first year of the person's career or citation history. |
| `citation_by_year` | JSON object mapping year strings to integer citation counts, such as `{"2024":125,"2025":140}`. |

The recent-period field names are legacy names; the parser does not store the exact “Since YYYY” column heading in the CSV.
Consult the retained HTML when the precise period matters, rather than deriving it from the current year.
Read the CSV with a CSV parser before decoding JSON-valued cells.
Blank scalar cells mean unavailable values, not zero; `[]` and `{}` mean no captured interests or yearly entries respectively.
An absent year key does not establish zero citations, and the histogram need not sum to the all-time total.
A blank Scholar link in an award roster means no accepted profile link is recorded, not proof that none exists.

The generated visualization data uses `null` for missing scalar metrics and dates and `{}` for missing histories.
Its `hasScholar` flag requires a joined, nonempty citation history; a URL alone does not satisfy it.
Its `generatedAt` timestamp records data-file generation, while each row's `crawlDate` retains the source capture date.
In contrast, `data/csrankings_profiles.csv` uses `crawl_date` for the alignment build's UTC date by default (or the explicit `--crawl-date` value), not necessarily the shard-fetch date.

### Award CSV Sort Order

Keep both `data/acm_fellows.csv` and `data/turing_award_winners.csv` sorted by numeric `year` descending, then by the full `name` field ascending using Python's `str.lower()` for case-insensitive comparison.
Compare the full name as stored, starting with the given name; do not extract or sort by surname.
Preserve spelling, capitalization, punctuation, and accents in the CSV cells; lowercasing is only part of the comparison key, with no other normalization or locale-specific collation.
Use a stable sort so rows with equal keys keep their relative order:

```python
rows.sort(key=lambda row: (-int(row["year"]), row["name"].lower()))
```

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
- leave `citation`, `dblp_profile`, `dblp_crawl_date`, and `google_scholar_profile` blank if unavailable.

Apply the [award CSV sort order](#award-csv-sort-order) after adding or renaming Fellows.

The profile crawler consumes existing URLs; it does not discover Fellows from this directory.
Inspect the directory separately in regular Safari if direct HTTP requests are blocked, and keep any directory scan reports under `../bigcows-crawler/.cache/`, for example:

```text
../bigcows-crawler/.cache/acm-fellows-directory-scan-YYYY-MM-DD.json
```

## CSRankings DBLP Alignment

`scripts/build_csrankings_profiles.py` builds `data/csrankings_profiles.csv` from known DBLP profiles and cached CSRankings shards.

The script:

- reads `../bigcows-crawler/.cache/csrankings/csrankings-[a-z].csv`;
- reads `data/acm_fellows.csv` and `data/turing_award_winners.csv`;
- normalizes DBLP links to HTTPS without `.html`, query strings or fragments, then deduplicates nonempty URLs, using the Fellows roster's name first for shared URLs;
- loops through DBLP profiles and includes only profiles that align to exactly one CSRankings row;
- preserves the original CSRankings columns;
- appends `crawl_date` and `dblp_profile`;
- writes `../bigcows-crawler/.cache/csrankings-profiles-report.json` with input roster paths, included, unmatched DBLP, and ambiguous DBLP counts.

Basic commands:

```bash
python scripts/build_csrankings_profiles.py
python scripts/build_csrankings_profiles.py --crawl-date 2026-05-01
python scripts/build_csrankings_profiles.py --cache-dir path/to/csrankings-cache --output data/csrankings_profiles.csv
python scripts/build_csrankings_profiles.py --fellows path/to/fellows.csv --turing path/to/turing.csv
```

For a full source refresh, run the shared crawler with `--refresh` before rebuilding:

```bash
python ../bigcows-crawler/scripts/cache_csrankings.py --refresh
python scripts/build_csrankings_profiles.py
```

Use the shared [CSRankings workflow](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md#csrankings-crawler) for partial runs, pacing, and cache/report details.
Inspect cache completeness before a full rebuild and investigate surprising drops in the included-row count.
Preserve original CSRankings fields and do not edit the award rosters unless the user requests it.
The alignment's `crawl_date` remains its build date; it does not reuse the rosters' `dblp_crawl_date`.

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

The alignment report is `../bigcows-crawler/.cache/csrankings-profiles-report.json`.
It contains:

- `generated_at`
- `cache_dir`
- `fellows`
- `turing`
- `output`
- `crawl_date`
- `csrankings_rows`
- `dblp_profiles_rows`
- `included_rows`
- `unmatched_dblp_profiles`
- `ambiguous_dblp_profiles`
- `unmatched_sample`
- `ambiguous`

When asked to check or validate CSRankings profiles, join `data/csrankings_profiles.csv` with the deduplicated union of both award rosters on `dblp_profile` and flag suspicious name mismatches.
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

- Profile affiliations are source evidence, not canonical employment history.
- A fellow can count toward multiple universities if Scholar and CSRankings provide distinct universities.
- The same normalized university from multiple sources counts once per fellow.
- Companies and generic job titles should not be counted as universities.
- Common variants such as `MIT`, `Massachusetts Inst. of Technology`, `CMU`, `UC Berkeley`, `UCLA`, `UIUC`, `Georgia Tech`, and `UBC` are normalized.
- Preserve `University of British Columbia` as distinct from `Columbia University`.
- The helper prints normalization warnings to stderr with `--show-warnings` when it suppresses ambiguous captures such as generic parent institutions or substring collisions.
  Use `--warnings-limit N` to control how many warnings are shown.

Use the repo-local skill `skills/analyze-acm-fellows` when asked about ACM Fellow university distribution or affiliation counts.
Analysis is read-only unless the user requests data changes; when stale sources matter, state the limitation and use the relevant refresh workflow only within the requested scope.

## Google Scholar Citation Visualization

The two static timelines separate presentation, rendering and generated data:

- `index.html` is the landing page linking to both visualizations.
- `acm_fellows.html` displays ACM Fellows and loads `scholar_data.js`.
- `turing_award_winners.html` displays Turing Award winners and loads `turing_scholar_data.js`.
- `scholar_visualization.js` and `scholar_visualization.css` provide shared filtering, rendering, and styles.
- Each data script assigns its award's joined dataset to `window.SCHOLAR_DATA`.

Each HTML page loads its data script before the renderer as classic scripts and links to the other award page.
It works on static hosting and when opened directly from disk; no fetch, module loader or backend is required.
D3 v7 still loads from a CDN, so network access to the CDN is needed.
Keep the landing page, both visualization pages, both data scripts, the renderer, and the stylesheet together at the repository root when copying or publishing the visualizations.
GitHub Pages publishes from the repository root (`/`); the root `.nojekyll` disables Jekyll processing.
The `docs/` directory retains review reports and data provenance.

Despite its retained command name, `scripts/build_scholar_citation_visualization.py` now generates only the data script:

```bash
python scripts/build_scholar_citation_visualization.py
python scripts/build_scholar_citation_visualization.py --award turing
```

The default `--award fellows` reads `data/acm_fellows.csv` and writes `scholar_data.js`.
With `--award turing`, it reads `data/turing_award_winners.csv` and writes `turing_scholar_data.js`.
Both join `data/google_scholar_profiles.csv` by Scholar URL without touching HTML, rendering code, or canonical CSVs.
It preserves the [award CSV sort order](#award-csv-sort-order).
The data object contains `schemaVersion`, `generatedAt` (UTC), `metadata` and `rows`.
Metadata includes `award` (`fellows` or `turing`), which the renderer checks against the page's `data-award` attribute to prevent displaying the wrong roster.
Each row includes recipient identity, award year, profile URLs, citations, h-index, yearly citation counts, missing-data status and `crawlDate` from the source Scholar record.
Generation time does not represent crawl freshness.
Unavailable metrics and crawl dates stay `null`, and missing citation histories stay empty objects.
`hasScholar` indicates a joined row with citation-by-year data, not merely the presence of a profile URL.
Do not hand-edit the generated data file.

Use a scratch output to inspect current CSV joins without updating the displayed snapshot:

```bash
python scripts/build_scholar_citation_visualization.py --output tmp/scholar_data.js
python scripts/build_scholar_citation_visualization.py --award turing --output tmp/turing_scholar_data.js
```

Custom input and output paths are supported:

```bash
python scripts/build_scholar_citation_visualization.py --award turing --roster path/to/turing_award_winners.csv --scholar path/to/google_scholar_profiles.csv --output tmp/turing_scholar_data.js
```

`--output` now names a JavaScript data file, not an HTML page.
`--acm` remains a legacy alias for `--roster`.
Generate data only when the underlying dataset refresh is ready to be reflected in the visualization.
Presentation changes do not require rebuilding data.
The September 16 extraction preserved the previously displayed snapshot, and the subsequent full import refreshed all 1,250 accepted ACM profiles.
See [Data Notes](docs/data_notes.md) for capture dates, missing profiles, retained Turing-only records and known attribution concerns.

The renderer keeps one row per recipient in the selected award roster, hides missing citation histories by default, and provides author search and a `Show missing Scholar data` checkbox.
Recipient names link directly to their Google Scholar profiles when available; names without a profile stay plain text.
Under each title, the source note is followed by an initially collapsed, keyboard-accessible About the Data panel containing total coverage counts, the filtered row count, the displayed year range, and links to the award CSV, shared Scholar statistics CSV, and data notes.
Search and the missing-data toggle remain visible outside the panel.
Display order defaults to award year descending, then last name ascending, without changing canonical CSV or generated data order.
Last-name sorting uses the final name token, excluding suffixes Jr., Sr., II, III, and IV, with the full name breaking ties.
Year, Name, Citations, and h-index headers toggle sorting; Name starts ascending, and numeric columns start descending.
Unavailable metrics remain last in either direction, and sorting persists while filtering.
Citations and h-index occupy separate right-aligned columns, followed by yearly bars with the latest year at the right.
Both pages use the shared renderer's 45-calendar-year window, ending in the current UTC year (1982–2026 in 2026), regardless of each dataset's coverage.
The renderer sets the CSS year count, keeping chart widths and year labels identical across awards.
Every year has a tick, with horizontal labels at five-year intervals.
Bar heights are normalized independently to each person's maximum within the displayed window; compare absolute counts using hover values and the metrics columns, not bar heights across people.
Years absent from a recipient's history appear as empty bars; the underlying data and its coverage metadata remain unchanged.
A missing or unsupported data script produces a visible error instead of an empty page.

Check award selection, canonical joins, missing-data semantics, renderer controls, and JavaScript syntax:

```bash
python -B -m unittest discover -s tests -p 'test_scholar_citation_data.py'
node tests/test_scholar_visualization.cjs
node --check scholar_data.js
node --check turing_scholar_data.js
node --check scholar_visualization.js
```

After changing data, verify the generated row counts, missing-data semantics and actual crawl dates, then inspect the page directly from disk.
After changing rendering, check author search, the missing-data toggle and the empty-result state.
Commit the generated data file when refreshing its source data; include HTML and rendering code only when those change.

## Git Hygiene

Do not commit these generated artifacts:

```text
.cache/
scripts/__pycache__/
*.pyc
```

The repository `.gitignore` already excludes `.cache/` and Python bytecode.

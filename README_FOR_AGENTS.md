# README for Agents

Follow [AGENTS.md](AGENTS.md) for documentation audiences.
Follow its [ACM source-of-truth policy](AGENTS.md#acm-source-of-truth) for award reconciliation and evidence-backed exceptions.
[README.md](README.md) is the human entry point; this file owns application maintenance workflows and constraints.
Keep dataset provenance, reconciliation history, and deliberate source differences in [Data Notes](docs/data_notes.md).

Use the [award field dictionary](#award-roster-fields) for CSV meaning, [missing-profile definitions](#missing-profiles-and-review-status) for coverage questions, and [quality criteria](#publication-profile-quality) for matching and rating decisions.
Canonical CSVs contain the current stored values; dated reports and Data Notes explain the evidence and decisions at each batch's completion.
Read later decisions before using an older report as an import source.
The [finalized-award-CSV instruction](AGENTS.md#finalized-award-csvs) limits the import workflows below to explicitly requested future data changes.

This repository owns canonical data, application-specific joins, analysis, and visualization.
All crawlers live in [bigcows-crawler](https://github.com/lintool/bigcows-crawler).
Its [agent reference](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md) is authoritative for transport, pacing, retries, manifests, cache schemas, and troubleshooting.

## Crawlers

### Repository Layout

Use Python 3.10 or newer, available as `python`.
Run the commands below from `acm-bigcows`, with `bigcows-crawler` checked out beside it.
Crawl artifacts default to the shared crawler's `.cache/`, independent of the working directory; they are Git-ignored and absent from a fresh clone.
Explicit relative paths resolve from the working directory.
The CSRankings shard cache and default alignment report also live in the shared crawler's `.cache/`.
Use this application's `tmp/` for disposable analysis output; retain crawl and import evidence in the shared cache.
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

### Review and Import DBLP Data

Use the shared [DBLP workflow](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md#dblp-profile-crawler) for transport and pacing.
For a fresh crawl, save both roster snapshots and the selected commands in a new run directory under `../bigcows-crawler/.cache/`, and use a new cache or Safari run directory instead of reusing historical successes.
Fetch the distinct nonempty URLs from the selected rosters, retaining the association to each award row.
The Safari runner binds a run directory to one stable input snapshot; for a combined crawl, prepare one deduplicated input CSV containing `name` and `dblp_profile`, or use separate run directories for the two rosters.
Begin with a paced pilot and resume with the original input.

Redirects do not pause the Safari crawl: inspect saved `redirect_review` captures afterward to determine whether the final page identifies the intended person.
A redirected author page, a namesake profile, and a name-disambiguation page require different identity decisions; a redirect alone neither validates nor rejects the link.
Persistent access challenges or transport failures leave the refresh incomplete and do not justify clearing stored links.

Before importing, check the retained HTML, capture timestamp and hash, final URL, ACM identity, and [publication quality criteria](#publication-profile-quality).
Update reviewed URLs, crawl dates and quality fields in the award rosters; there is no separate canonical DBLP CSV to rebuild.
Apply shared-URL decisions consistently across both rosters, even during a single-roster refresh.
Retain rejected URLs and rationale in the review evidence, and record removals or unresolved cases in Data Notes.
Check dependent CSRankings links after a URL change or removal.
Validate the [schema and ordering rules](#data-layout), preserve unrelated fields, and record coverage and inspection limits before describing the refresh as complete.

### Other Fetching Commands

These commands fetch DBLP pages or CSRankings shards:

```bash
python ../bigcows-crawler/scripts/cache_dblp_profiles.py --data data/acm_fellows.csv
python ../bigcows-crawler/scripts/cache_csrankings.py
```

The DBLP command above uses the HTTP transport and its default cache; it can reuse older captures and is not a fresh full-roster refresh by itself.
Use the reviewed DBLP workflow above when updating canonical data.
Follow the shared reference for source pacing and retries.
After refreshing CSRankings sources, follow [CSRankings Name Links](#csrankings-name-links) to synchronize the profile lookup table.
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
   The following example prepares a combined run and starts only the Fellows crawl; replace the placeholder with a unique run label and create the directory only once:

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
   )
   ```

   The subshell stops on command failure, including an existing run directory, before later commands can overwrite retained inputs or logs.
   The Scholar runner records blocked responses but does not automatically stop on them; monitor the log and cache and interrupt the run if blocking appears.
   Exit code 0 does not establish successful coverage, freshness or identity.
   Inspect the Fellows report and recorded fetch errors before starting Turing; do not continue while a block is unresolved.
   Start the second award separately with the same run label and shared cache:

   ```bash
   scholar_run=../bigcows-crawler/.cache/scholar-refresh-YYYY-MM-DD-HHMM
   python -u ../bigcows-crawler/scripts/cache_google_scholar_profiles.py --data "$scholar_run/turing-input.csv" --cache "$scholar_run/cache.json" --report "$scholar_run/turing-report.json" > "$scholar_run/turing.log" 2>&1
   ```

   For a single-roster refresh, snapshot both rosters for reconciliation but run only the selected award command, using `turing-input.csv`, `turing-report.json` and `turing.log` for a Turing-only run.
   Resume using the same snapshots and cache without `--refresh`, retaining previous logs and using a new log filename for each attempt.
   Ordinary resume usually skips cached failures; entries with an HTML-required status but no HTML are retried automatically.
   After inspecting failures and resolving any block, use the shared crawler's [resume and cache rules](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md#cache) to select the appropriate retry.
   `--limit-new 0` rebuilds a report without fetching, but still writes cache/report artifacts and does not establish freshness.
3. **Review freshness and identity:** Require a successful capture from the selected run with complete HTML, parsed statistics, and a supported identity before accepting a profile.
   Check capture timestamps and recorded fetch errors; a retained older success is not evidence of a successful current refresh.
   Inspect `last_fetch_error` in the cache itself: it is not exposed in the Scholar report and can accompany a retained `ok` status.
   Compare names, affiliations, research areas, and representative publications against ACM and primary institutional sources.
   A compatible name or HTTP 200 response alone is insufficient.
4. **Resolve missing and rejected links:** Search for replacement profiles when discovery is in scope, then freshly crawl and verify candidates before accepting them.
   If a link is missing or rejected and no fresh, verified replacement can be found, leave its Scholar URL and crawl date blank and set its quality to `N`; do not fill the gap with historical statistics.
   Treat a blocked or interrupted run as incomplete, rather than clearing links solely because of a temporary access failure.
   Record accepted, rejected, unresolved, and deferred decisions with evidence and capture references.
5. **Reconcile and import across both rosters:** Build the accepted statistics set by unique Scholar URL, with one record for a person shared by the awards.
   Apply reviewed link changes and reassess quality using the [profile-quality criteria](#publication-profile-quality), then replace or add statistics only from accepted captures.
   Update `google_scholar_profile_crawl_date` from the same accepted capture as the statistics row's `crawl_date`, synchronizing recipients shared by both rosters.
   Preserve unrelated award fields.
   Remove rejected or obsolete statistics records only after confirming that neither roster still references them.
   Preserve reviewed records outside a single-award refresh's scope, with their original crawl dates; never describe those as newly refreshed.
   The generic exporter is not a reviewed importer: use a reviewed run-specific import script or prepare an explicit import for review, retaining it and the before/after evidence in the run directory.
6. **Validate and publish the data snapshot:** Check unique profile URLs, roster joins, accepted capture coverage, actual crawl dates, missing-value semantics, unchanged unrelated fields, canonical sort order, and LF line endings.
   Record results and unresolved issues in [Data Notes](docs/data_notes.md).
   Once the data refresh is ready for display, regenerate both award datasets and run the checks in the [visualization workflow](#google-scholar-citation-visualization), since shared statistics can affect both pages.

### Apply Reviewed ACM Results

The ACM crawlers never update canonical CSVs.
Verify the person and award using the captured HTML, and inspect exact differences as well as name compatibility.
Profile headings often use given-name-first order; preserve the directory-based canonical name unless the [source policy](AGENTS.md#acm-source-of-truth) supports a documented correction.
Use successful captures as evidence; preserve existing values when source fields are blank, truncated, malformed, or otherwise less accurate.
A recent fetch is not automatically more authoritative than the reviewed CSV.
Set `acm_fellow_profile_crawl_date` from the accepted capture's UTC date, including when review confirms that the existing award fields should remain unchanged.
An inaccessible page leaves the refresh incomplete; do not clear a link solely because a request was blocked or timed out.
Follow the data conventions below and record dataset-specific decisions in [Data Notes](docs/data_notes.md).

## Data Layout

Canonical CSV files live under `data/`:

```text
data/acm_fellows.csv
data/csrankings_profiles.csv
data/google_scholar_profiles.csv
data/turing_award_winners.csv
```

### Award Roster Fields

`data/acm_fellows.csv` and `data/turing_award_winners.csv` use the same columns below, in this order.
Each row represents a recipient in that award roster; a person who received both awards appears once in each roster.

| Field | Meaning |
| --- | --- |
| `name` | Literal surname-first name from the corresponding ACM award directory unless a documented, evidence-backed exception applies. |
| `year` | Fellowship class year or Turing Award year, depending on the roster; not the announcement year. |
| `location` | Reviewed ACM location text; a directory region may remain when no more specific profile location is available. |
| `citation` | ACM award citation describing the recognized contributions; unrelated to Scholar citation counts. |
| `acm_fellow_profile` | ACM recipient URL for the award; the legacy field name also applies to Turing winners. |
| `acm_fellow_profile_crawl_date` | Accepted ACM profile capture's UTC date, or blank when unavailable. |
| `dblp_profile` | Stored DBLP author URL, or blank when no accepted link is recorded. |
| `dblp_profile_crawl_date` | Accepted capture's UTC date for the stored DBLP URL, or blank when unavailable. |
| `dblp_profile_quality` | Required `Y` or `N` under the publication-quality criteria below. |
| `google_scholar_profile` | Stored Scholar author URL, or blank when no accepted link is recorded. |
| `google_scholar_profile_crawl_date` | Accepted capture's UTC date for the stored Scholar URL, or blank when unavailable. |
| `google_scholar_profile_quality` | Required `Y` or `N` under the publication-quality criteria below. |
| `csrankings_name` | Exact CSRankings name key from the refreshed faculty sources or a documented retained historical profile, or blank when no accepted link is recorded. |
| `csrankings_name_alignment_date` | UTC date the stored CSRankings name association was established or explicitly revalidated; blank when the name link is blank. |

The `csrankings_name` field stores the exact `name` from a CSRankings faculty source row or documented retained `data/csrankings_profiles.csv` record, including spelling, punctuation and any disambiguation number.
Historical links absent from the latest upstream files require explicit provenance; a populated name does not establish current CSRankings inclusion or current faculty status.
It is an explicit name key, not a URL, and is independent of whether a DBLP URL is present or rated `Y`.
A blank means no accepted CSRankings name link is recorded, not proof that the person is absent from CSRankings.
The adjacent `csrankings_name_alignment_date` records the name-alignment decision date, independently of the CSRankings source download date.
See [CSRankings Name Links](#csrankings-name-links) for matching and manual-edit guidance.

For both award rosters, use the corresponding directory's literal surname-first display names by default, subject to the [ACM source-of-truth policy](AGENTS.md#acm-source-of-truth).
Convert HTML entities and rendered whitespace to ordinary text; override directory spelling, initials or name order only when cited evidence establishes an obvious error, and document the exception.
The eleven confirmed historical Fellows absent from the current directory retain their previously reviewed names as documented exceptions; see the [directory reconciliation](docs/acm_directory_reconciliation_2026-09-17.md).
The seven [supported name corrections](docs/acm_directory_reconciliation_2026-09-17.md#subsequent-review-of-obvious-name-errors) are accepted exceptions; preserve them on future imports, including the single-name form `Arvind`.
Do not substitute an individual profile's heading or honorifics for the directory display name.
For Turing rows, `acm_fellow_profile` and its crawl date refer to the Turing recipient's ACM page; always select `--award turing` when crawling or comparing this dataset.
There is no ACM profile quality field.
There is no separate canonical `data/acm_fellow_profiles.csv` or `data/dblp_profiles.csv`; profile links belong in the award rosters.
The distinct nonempty `csrankings_name` keys across both rosters define the current CSRankings profile lookup table.

### Historical Review Artifacts

Dated reports and row-audit CSVs under `docs/` retain the names, URLs, fields and counts used in their review batch.
Many precede the surname-first directory reconciliation, so differences from current roster names or profile links are expected.
Preserve that evidence instead of renaming historical rows or treating an old link as a current association.
Likewise, references to removed tables or former visualization paths describe the repository at the time of that work.
Use the canonical award CSVs for current values and later Data Notes entries for superseding decisions.

### Missing Profiles and Review Status

Specify the service whenever reporting a “missing profile”: ACM means a blank `acm_fellow_profile`, DBLP means a blank `dblp_profile`, and Scholar means a blank `google_scholar_profile`.
A blank URL means no accepted link is currently recorded; it does not prove that no public profile exists or that the recipient should be removed from the award roster.
The [unavailable ACM profile record](docs/data_notes.md#2026-09-13---unavailable-individual-acm-profiles) identifies the Fellows whose former ACM URLs were cleared and preserves the historical evidence.

| State | Interpretation |
| --- | --- |
| Blank URL | Missing stored link for that service; its crawl date is blank and its publication quality, where present, is `N`. |
| URL present, crawl date blank | A link is stored, but no successful capture has been accepted for that URL. |
| URL present, quality `N` | A linked profile judged poor, wrong, substantially mixed or inadequately covered; consult the review rationale. |
| URL present, quality `Y` | A reasonable profile under the reviewed scope; isolated attribution concerns may remain. |
| Failed latest fetch | An access or freshness problem; preserve the previous link, accepted date and rating until evidence justifies a change. |
| Review flag | A request to inspect evidence; independent of whether the link is present or its quality is `Y` or `N`. |

Count missing links directly from the relevant URL cells, not from quality ratings, blank dates, or review flags.
When combining awards, state whether the result counts award rows or distinct people; adding roster counts double-counts shared recipients.
Likewise, “missing any profile” means at least one of the three URL cells is blank, whereas “missing all profiles” means all three are blank.
A resolved review case can still have a missing URL or an `N` rating.
Dated audit CSVs preserve their batch's links and evidence; use the canonical rosters for current coverage.

### Profile Crawl Dates

Both award rosters store each `*_profile_crawl_date` immediately after its corresponding URL.
Each is the accepted successful capture's UTC date (`YYYY-MM-DD`), derived from `fetched_at`, not the run start, import or quality-review date.
For example, a capture at `2026-09-18T01:00:00Z` receives `2026-09-18`, even when the run and Data Notes entry are dated September 17 in Toronto.
Keep the date blank when the URL is blank or no successful capture has been accepted for that URL.
When a URL changes or is cleared, clear its old date and populate a new date only from an accepted capture of the new URL.
For URLs shared across the two rosters, update both dates together and keep them identical.
An unsuccessful refresh leaves the previous accepted date in place; report the refresh as incomplete rather than advancing the date.

Accepting a capture means accepting its page and timestamp as evidence; it does not certify the profile's identity or publication quality.
A retained publication profile rated `N` can therefore have a crawl date.
A quality reassessment using existing evidence does not advance that date.
Keep full timestamps, HTML, capture hashes and validation evidence in the shared crawler cache.

### Publication Profile Quality

Use the repo-local [Check Profiles skill](skills/check-profiles/SKILL.md) for a holistic review of Google Scholar, DBLP and CSRankings links across either or both award rosters.
`dblp_profile_quality` and `google_scholar_profile_quality` are required for every award row and must be `Y` or `N`.
Use the appropriate ACM Fellow or Turing recipient profile as the identity and research ground truth.
If the individual ACM URL is missing, use retained ACM roster/directory evidence and corroborating primary sources, state the limitation, and flag uncertain identity or coverage for review.
Do not claim an individual ACM page was inspected when no such capture exists.

| Finding | Rating And Action |
| --- | --- |
| Supported identity, substantial publication coverage and mostly matching or adjacent work without substantial unrelated contamination | `Y`, allowing a couple of questionable or misattributed papers. |
| Wrong person or substantial unrelated contamination | `N`; record the identity or contamination evidence. |
| Missing link | `N`, with URL and crawl date blank. |
| Obviously incomplete Scholar or DBLP bibliography | `N`, including incidental or split fragments omitting the established body of work. |
| Genuinely sparse Scholar or DBLP bibliography without positive identity and coverage evidence supporting an exception | `N` pending verification; record the actual count and coverage concern. |

Assess DBLP and Scholar independently.
The user expects substantial numbers of publications in both Scholar and DBLP for Fellows and Turing winners.
A short captured first page, filtered view or incomplete crawl alone does not establish that the underlying profile is sparse or poor; check pagination and capture completeness, and preserve the previous rating when access prevents a supported decision.
For both services, assess coverage against the ACM-recognized contributions and corroborating publication evidence.
Do not retain `Y` merely because a handful of titles fit the topic or the recipient has a historical or service-oriented career; any justified exception requires positive identity and coverage evidence.
There is no universal numerical cutoff; the nine one-to-four-record profiles in the September 17 reassessment describe that batch, not a general threshold.

Substantial contamination can warrant `N` despite a relevant majority; this is a profile-level judgment, not a percentage formula.
An isolated attribution error, abbreviated author list, name variant, contributor credit or interdisciplinary topic does not by itself justify `N`.
Cross-service title agreement is corroboration, not independent proof of authorship.
A rating does not certify every publication or aggregate citation total.
Record the evidence dates, inspection scope, rationale and any remaining review questions.

Link retention and quality are separate decisions.
An instruction to keep a URL does not establish `Y`, and an `N` rating does not by itself instruct removal of the link.
When a URL changes, reassess its quality instead of carrying the old URL's rating forward; clearing a URL requires `N` and a blank date.
Keep quality ratings consistent for the same publication-service URL shared across both rosters, preserving explicit user decisions.

The user explicitly rated the Scholar profiles of Arindam Banerjee, Ramesh C Jain, James H Morris and David S Johnson `N`; do not upgrade them solely because a majority of sampled papers are adjacent.
The user explicitly accepted Stephen David Crocker’s DBLP profile `https://dblp.org/pid/49/6744` as `Y` after reviewing its 15-record coverage and missing early RFC work; preserve this [documented coverage exception](docs/check_profiles_trial_100_2026-09-18.md) rather than reopening the same concern without new evidence.
The user rejected the stored DBLP profiles for David Patterson, Jim Gray, Richard Karp, J. H. Wilkinson, Seymour J. Wolfson, Roger R Bate and Karen Duncan; rejected URLs remain evidence only and must not be restored from older captures or snapshots.
The [September 18 user dispositions](docs/check_profiles_full_2026-09-18.md#explicit-user-decisions) additionally retain the reviewed Meenakshi Balakrishnan and Mihai Pop DBLP candidates as `N`, rate Sudipta Sengupta's Scholar profile `N`, and accept Aravind Srinivasan and Vishwani Agrawal's Scholar profiles as `Y`.
They accept George Varghese and Prithviraj Banerjee's DBLP profiles as `Y`, select Sung Mo Kang's `57/2381-1.html` bibliography as `Y`, and reject both reviewed Steven Scott DBLP candidates.
The same user disposition removes the sparse DBLP associations for Victor Miller, James Gosling, Charles H. House, Bryant York, Stephen Bourne, Sidney Karin, Joel Birnbaum and Charles Geschke; do not restore these rejected profiles from older evidence or reopen their coverage decisions without new evidence.
Consult the [DBLP review](docs/dblp_profile_quality_2026-09-17.md), [Fellows Scholar review](docs/acm_scholar_quality_2026-09-17.md), [Turing Scholar review](docs/turing_scholar_quality_2026-09-17.md) and later Data Notes entries for individual decisions and inspection limits.
The quality fields do not currently filter the citation visualization, CSRankings alignment or university-affiliation analysis, or alter shared Scholar metrics.

### CSV Storage Conventions

Keep committed CSV files on Unix LF line endings.
Python's `csv.DictWriter` defaults to CRLF unless `lineterminator="\n"` is supplied.
Apply the [award CSV sort order](#award-csv-sort-order) to both rosters.
The CSRankings output schema and matching behavior are documented in [CSRankings DBLP Alignment](#csrankings-dblp-alignment).

### Google Scholar Statistics

`data/google_scholar_profiles.csv` stores one row per unique Scholar `profile` URL with accepted imported statistics across both award rosters.
The [Check Profiles skill](skills/check-profiles/SKILL.md) can establish a new roster link through direct candidate inspection before a crawl is imported; such a link has a blank capture date and no statistics row until an approved crawl supplies accepted evidence.
The fresh-capture requirements in the reviewed refresh workflow apply to importing statistics; an identity review does not invent or restamp metrics.
Join each roster's `google_scholar_profile` to this `profile` field; names are descriptive fields, not join keys.
Use the canonical URL form `https://scholar.google.com/citations?user=...` in both tables; the visualization and affiliation helper use exact-string joins rather than normalizing URL variants at read time.
The row's `crawl_date` and each referring roster's `google_scholar_profile_crawl_date` should identify the same accepted capture.

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
The visualization's `joinedRows` and `missingRows` metadata count rows with and without that history, not rows with and without stored profile links.
Its `generatedAt` timestamp records data-file generation, while each row's `crawlDate` retains the source capture date.
`data/csrankings_profiles.csv` has no date column; record table synchronization in Data Notes and retain source-fetch timestamps in the crawler evidence.

### Award CSV Sort Order

Keep both `data/acm_fellows.csv` and `data/turing_award_winners.csv` sorted by numeric `year` descending, then by the full `name` field ascending using Python's `str.lower()` for case-insensitive comparison.
Compare the full name as stored: directory-listed names in both rosters generally start with the surname, `Arvind` is a single name, and the eleven historical Fellows exceptions retain given-name-first order.
Do not extract a separate surname sort key for the CSV.
Preserve spelling, capitalization, punctuation, and accents in the CSV cells; lowercasing is only part of the comparison key, with no other normalization or locale-specific collation.
Use a stable sort so rows with equal keys keep their relative order:

```python
rows.sort(key=lambda row: (-int(row["year"]), row["name"].lower()))
```

## ACM Award Directories

### ACM Fellows Directory

The ACM Fellows directory is the default source for recipient discovery and reconciliation:

```text
https://awards.acm.org/fellows/award-recipients?year=2025&award=158&region=&submit=Submit&isSpecialCategory=
```

Use this page to discover new ACM Fellows before running profile-page enrichment.
Select the requested class with `year`, keeping `award=158`, and work backward through 1994 for a full historical reconciliation.
The current directory omits eleven confirmed historical Fellows retained in the CSV; absence alone does not justify deleting a row.
It also lists deceased recipients, so do not assume that it is a directory of living Fellows only.
See the [Fellows reconciliation](docs/acm_directory_reconciliation_2026-09-17.md) for coverage and evidence-backed exceptions.
The directory provides:

- fellow name in `Last, Given` display order;
- ACM Fellow profile URL;
- ACM Fellows year;
- region.

It does not provide the full citation, DBLP profile, or Google Scholar profile.
When adding directory-only rows to `data/acm_fellows.csv`, fill what is available:

- `name`: preserve literal `Last, Given` directory text, subject to the documented source-policy exceptions;
- `year`: directory year;
- `location`: directory region, until the individual profile page provides a more specific location;
- `acm_fellow_profile`: directory profile URL;
- leave `citation`, `dblp_profile`, and `google_scholar_profile` blank if unavailable.
- leave each profile's crawl date blank until a successful capture of that profile has been accepted; a directory listing alone does not establish `acm_fellow_profile_crawl_date`.
- set `google_scholar_profile_quality` to `N` when the Scholar link is missing; otherwise assess the linked profile against the ACM identity.
- set `dblp_profile_quality` to `N` when the DBLP link is missing; otherwise assess it independently using the same criteria.

Apply the [award CSV sort order](#award-csv-sort-order) after adding or renaming Fellows.

The profile crawler consumes existing URLs; it does not discover Fellows from this directory.
Inspect the directory separately in regular Safari if direct HTTP requests are blocked, and keep any directory scan reports under `../bigcows-crawler/.cache/`, for example:

```text
../bigcows-crawler/.cache/acm-fellows-directory-scan-YYYY-MM-DD.json
```

### Turing Award Directory

Use the same directory endpoint with `award=140` for Turing Award winners:

```text
https://awards.acm.org/fellows/award-recipients?year=2025&award=140&region=&submit=Submit&isSpecialCategory=
```

Select each award year with `year` and work backward through 1966 for a full historical reconciliation.
Apply the same name, field, capture-date and ordering rules to `data/turing_award_winners.csv`; verify individual profiles with `--award turing`.
The [Turing reconciliation](docs/turing_directory_reconciliation_2026-09-17.md) matched all 81 recipients and years, with no missing directory entries or blank stored ACM links.
Match modern and legacy ACM recipient URLs using the final recipient ID, allowing alphanumeric IDs, case differences and the legacy `.cfm` suffix; verify the person and award before accepting a changed URL.

## CSRankings Name Links

Both award rosters record explicit links in `csrankings_name`.
The initial [Fellows audit](docs/csrankings_name_alignment_2026-09-18.csv) and [Turing audit](docs/turing_csrankings_name_alignment_2026-09-18.csv) record every recipient, the accepted links, match statuses and candidate names with affiliations for manual review.
Their row numbers and statuses describe those batches; use the rosters' current `csrankings_name` values after manual edits.

The initial pass used all 26 alphabetical faculty source files refreshed on September 18, 2026.
It accepted unique normalized name matches using the existing name normalization described below, then unique compatible initial expansions only when tokens aligned in order, the surname matched and the roster's first given token was spelled out.
Ambiguous names, initials-only given names, differing token counts and duplicate target assignments were left blank.
This is name-based alignment, not independent identity verification or a publication-profile quality assessment.
The combined alias-expanded CSV and alias/name-change helper files were retained but not used to populate this initial pass.

A subsequent [broader alignment review](docs/csrankings_broader_alignment_2026-09-18.md) added links using reviewed Scholar identifiers, alternate names, current or historical institutions, and selected institutional pages corroborating the award's research area.
Its [row audit](docs/csrankings_broader_alignment_2026-09-18.csv) covers all rows that were unlinked at the start of that pass.
The upstream DBLP alias file helped generate candidates; institution or research similarity alone was not sufficient to accept them.
Scholar IDs and existing DBLP links can also conflict with identity evidence, so inspect name and institution context rather than treating an identifier or a `Y` rating as conclusive.
When several source spellings represent the same person, prefer the exact reviewed DBLP or Scholar spelling, preserving source disambiguators and campus tags; document other choices.
The [local profile-table audit](docs/csrankings_profile_evidence_2026-09-18.csv) also checks `scholarid` and normalized `dblp_profile` against both rosters.
The table's DBLP association was inferred by the old name matcher, so it supplies a candidate rather than independent proof; that review rejected two misleading legacy associations and accepted five corroborated historical profiles absent from the fresh sources.

For manual corrections, copy the exact `name` from the appropriate source row into `csrankings_name`; preserve the ACM `name` and other reviewed roster fields.
Set `csrankings_name_alignment_date` to the UTC date of that correction or explicit revalidation; clear it when removing the link, and preserve it during unrelated source refreshes.
Check that the source key exists exactly once and is not already assigned to another recipient within the same roster, and record evidence for ambiguous identity decisions in the data notes.
For a documented historical link, validate the key against the retained profile-table record and preserve that source evidence through future rebuilds.
The same person may share a key across both award rosters; keep those shared recipients' links consistent.
Preserve manual assignments on future matching passes rather than overwriting them with inferred matches.

`data/csrankings_profiles.csv` contains exactly one row per distinct nonempty `csrankings_name` across both rosters.
To synchronize it, resolve each accepted key exactly against all 26 refreshed alphabetical faculty files and copy their original `name`, `affiliation`, `homepage`, `scholarid` and `orcid` values.
Preserve documented historical records absent from those sources using the retained profile table; investigate any other missing or duplicate key instead of inferring a replacement.
Remove unreferenced keys and sort by case-insensitive name with the exact name as a tie-breaker.
Record synchronization time in Data Notes; do not add a `crawl_date` column to this lookup table.
Profile capture dates and CSRankings name-alignment dates remain in the award rosters, while source-download timestamps remain in the crawler evidence.
Copy the linked recipient's normalized DBLP URL only after checking agreement across shared recipients and known identity conflicts; a quality flag alone does not determine whether to retain a URL.
Exclude exact URLs classified as `identity_mismatch` in the [DBLP review](docs/dblp_profile_quality_2026-09-17.csv), unless later documented identity evidence supersedes that finding.
Match reviewed URLs, not historical award-name spellings, and do not copy known wrong-person URLs into the lookup table even when the award roster retains them.
Other `N` categories do not automatically imply a different person or removal.
The accepted UCLA key `Wei Wang 0010` initially had a blank table DBLP field because the roster URL identified the HKUST namesake, as documented in the [broader review](docs/csrankings_broader_alignment_2026-09-18.md).
The [full profile review](docs/check_profiles_full_2026-09-18.md) subsequently accepted the UCLA bibliography `https://dblp.org/pid/w/WeiWang` for both the roster and lookup table.
Validate exact key coverage, uniqueness and source fields, retain input snapshots and a validation report in the shared cache, and preserve both award rosters and generated visualizations.

The corrected September 18 table contains 829 unique keys, including five retained historical profiles; see the [PR review corrections](docs/data_notes.md#2026-09-18-0742-edt---correct-csrankings-identity-links-from-pr-review).
University analysis joins through the exact `csrankings_name` key.
The separate legacy DBLP-based builder below still uses inferred names and must not replace the canonical table.

The [source-field manifest](docs/csrankings_source_fields.json) protects the five original CSRankings fields independently of the derived DBLP field.
Its per-name hashes were verified against all 26 retained September 18 source shards and an independent retained table for the five documented historical keys.
Tests compare the canonical table against those hashes without requiring a local crawler cache.
After an authorized source update, regenerate the manifest from independently retained inputs and inspect its changes; do not update hashes merely to make a failing test pass.
For the current retained evidence:

```bash
python scripts/build_csrankings_source_manifest.py \
  --historical-source ../bigcows-crawler/.cache/check-profiles-full-2026-09-18/csrankings_profiles.csv.before \
  --output docs/csrankings_source_fields.json
```

This command checks existing files only; it performs no crawl and rejects fields that differ from the supplied source evidence.
For each selected name, conflicting upstream rows are rejected even when one matches the local table; identical duplicate rows are harmless.
Conflicting duplicate names in historical input are also rejected instead of silently choosing the last row.
Record the selected source snapshots and any legitimate changes in Data Notes.

## CSRankings DBLP Alignment

`scripts/build_csrankings_profiles.py` is the legacy builder from known DBLP profiles and cached CSRankings shards.
It defaults to `../bigcows-crawler/.cache/csrankings-legacy-profiles.csv` and rejects the canonical profile table as either `--output` or `--report`, including symlink aliases.
It does not preserve explicit accepted name links or historical exceptions.
Use the synchronization procedure above for canonical updates; the following documents the legacy implementation for investigation and future migration.
It matches each DBLP-linked award recipient's roster name against CSRankings names; it does not fetch DBLP pages or read their parsed author names.

The script:

- reads `../bigcows-crawler/.cache/csrankings/csrankings-[a-z].csv`;
- reads `data/acm_fellows.csv` and `data/turing_award_winners.csv`;
- normalizes DBLP links to HTTPS without `.html`, query strings or fragments, then deduplicates nonempty URLs, using the Fellows roster's name first for shared URLs;
- loops through those roster names and includes a DBLP URL only when its name matches exactly one CSRankings row;
- preserves the original CSRankings columns;
- appends `dblp_profile`;
- writes `../bigcows-crawler/.cache/csrankings-profiles-report.json` with input roster paths, included, unmatched DBLP, and ambiguous DBLP counts.

Run the legacy builder only with a separate output and report under a retained cache run directory:

```bash
mkdir -p ../bigcows-crawler/.cache/csrankings-legacy-review
python scripts/build_csrankings_profiles.py \
  --output ../bigcows-crawler/.cache/csrankings-legacy-review/profiles.csv \
  --report ../bigcows-crawler/.cache/csrankings-legacy-review/report.json
```

For a full source refresh, run the shared crawler with `--refresh` before synchronizing accepted name keys:

```bash
python ../bigcows-crawler/scripts/cache_csrankings.py --refresh
```

Use the shared [CSRankings workflow](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md#csrankings-crawler) for partial runs, pacing, and cache/report details.
Inspect cache completeness before a full rebuild and investigate surprising drops in the included-row count.
The builder silently skips missing shard files and replaces its output; a successful exit does not establish that all 26 shards were available.
Preserve original CSRankings fields and do not edit the award rosters unless the user requests it.
The report's `generated_at` records the build time; the output CSV has no date column or `--crawl-date` option.
Changing `--cache-dir` or `--output` does not relocate the default report; set `--report` explicitly to retain a separate report under the shared cache.

Compile-check the script:

```bash
python -m py_compile scripts/build_csrankings_profiles.py
```

The output CSV columns are:

```text
name,affiliation,homepage,scholarid,orcid,dblp_profile
```

The matching policy is conservative.
The script normalizes names by ignoring case, punctuation, diacritics, common honorifics, suffixes, and excess whitespace.
It converts comma-separated surname-first directory names to given-name-first order for matching, while recognizing trailing suffixes such as `John Smith, Jr.`.
It removes a trailing degree such as `Ph.D.` as a complete credential, preserving standalone initials such as `D.` for identity matching.
It prefers exact normalized name matches, falling back to compatible first-name/initial, surname and middle-name checks.
The fallback rejects cases where only one name has middle tokens and checks spelled-out middle tokens for compatibility; it is stricter than matching just first and last initials.
It excludes unmatched and ambiguous rows instead of writing weak guesses.
Uniqueness is checked separately for each DBLP URL; the builder does not enforce a one-to-one mapping across all output rows or validate the linked DBLP identity.
Quality ratings do not filter this output.

The alignment report is `../bigcows-crawler/.cache/csrankings-profiles-report.json`.
It contains:

- `generated_at`
- `cache_dir`
- `fellows`
- `turing`
- `output`
- `csrankings_rows`
- `dblp_profiles_rows`
- `included_rows`
- `unmatched_dblp_profiles`
- `ambiguous_dblp_profiles`
- `unmatched_sample`
- `ambiguous`

`dblp_profiles_rows` is the count of distinct usable roster DBLP URLs, not rows from a separate DBLP table.
The total counts cover the whole input, but `unmatched_sample` includes at most 50 profiles, `ambiguous` at most 100 profiles, and each ambiguous entry at most ten candidates.
Output order follows the deduplicated roster traversal: Fellows first, then Turing-only URLs; it is not a global alphabetical sort.

When asked to check or validate CSRankings profiles, first join both rosters by exact `csrankings_name` and verify that every populated key resolves exactly once and every table row is referenced.
Then normalize DBLP URLs as the builder does and flag conflicting URLs or suspicious identity associations, allowing documented blank-field exceptions.
Names should match modulo minor variations such as accent characters, diacritics, periods, punctuation, initials, spacing, hyphens, and capitalization.
For suspicious rows, report the CSRankings name, award-roster name, affiliation, DBLP URL, and why the identity is doubtful.
Include the DBLP page's author name only when a retained capture or separate inspection supplies it, and label it distinctly from the roster name.
Do not modify CSV files during validation unless the user explicitly asks.

Use the repo-local skill `skills/refresh-csrankings` when asked to refresh CSRankings and rebuild this DBLP-aligned output.

## ACM Fellow University Analysis

`scripts/analyze_acm_fellow_universities.py` counts ACM Fellow university affiliations from joined Google Scholar and CSRankings profile data.

The script:

- reads `data/acm_fellows.csv`;
- joins Google Scholar affiliations through `google_scholar_profile`;
- joins CSRankings affiliations through the exact `csrankings_name` key;
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
- Counts use all linked source affiliations, including those whose publication profile quality is `N`; the helper does not apply quality filters.
- The Scholar join uses the exact stored profile URL; the CSRankings join uses the exact reviewed name key, including disambiguation numbers.
- Missing or unresolved CSRankings keys do not fall back to inferred names or DBLP URLs; duplicate source name keys are rejected instead of silently choosing a row.
- DBLP URL spelling, quality and missing derived DBLP fields do not affect an accepted CSRankings affiliation link.
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
The generated rows omit DBLP links and both quality fields; changing only those fields does not change the displayed snapshot.
Unavailable metrics and crawl dates stay `null`, and missing citation histories stay empty objects.
`hasScholar` indicates a joined row with citation-by-year data, not merely the presence of a profile URL.
The renderer also hides scalar metrics when `hasScholar` is false, even if a joined source record contains all-time totals.
Do not hand-edit the generated data file.
Newly generated files include a rebuild hint selecting the corresponding award and its default inputs; custom input or output paths must still be supplied explicitly.

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
See [Data Notes](docs/data_notes.md) for the history of imported Scholar statistics and displayed snapshots, capture dates, missing links and known attribution concerns.

The renderer keeps one row per recipient in the selected award roster, hides missing citation histories by default, and provides author search and a `Show missing Scholar data` checkbox.
Search accepts a directory name in its stored surname-first order or given-name-first order, ignoring case, commas and repeated whitespace.
Recipient names link directly to their Google Scholar profiles when available; names without a profile stay plain text.
Under each title, the source note is followed by an initially collapsed, keyboard-accessible About the Data panel containing total coverage counts, the filtered row count, the displayed year range, and links to the award CSV, shared Scholar statistics CSV, and data notes.
Search and the missing-data toggle remain visible outside the panel.
Display order defaults to award year descending, then last name ascending, without changing canonical CSV or generated data order.
Last-name sorting uses the text before the comma for surname-first directory names, or the final name token for given-name-first names, excluding suffixes Jr., Sr., II, III, and IV, with the full name breaking ties.
Year, Name, Citations, and h-index headers toggle sorting; Name starts ascending, and numeric columns start descending.
Unavailable metrics remain last in either direction, and sorting persists while filtering.
Citations and h-index occupy separate right-aligned columns, followed by yearly bars with the latest year at the right.
Both pages use the shared renderer's 45-calendar-year window, ending in the current UTC year (1982–2026 in 2026), regardless of each dataset's coverage.
The renderer sets the CSS year count, keeping chart widths and year labels identical across awards.
Every year has a tick, with horizontal labels at five-year intervals.
Bar heights are normalized independently to each person's maximum within the displayed window; compare absolute counts using hover values and the metrics columns, not bar heights across people.
Years absent from a recipient's history appear as empty bars; the underlying data and its coverage metadata remain unchanged.
The current hover text renders absent years as zero, so consult `citationByYear` to distinguish a recorded zero from a missing year.
A missing or unsupported data script produces a visible error instead of an empty page.

After authorized regeneration, check snapshot synchronization, award selection, canonical joins, renderer controls and JavaScript syntax:

```bash
python -B -m unittest discover -s tests -p 'test_scholar_citation_data.py'
node tests/test_scholar_visualization.cjs
node --check scholar_data.js
node --check turing_scholar_data.js
node --check scholar_visualization.js
```

When regeneration is authorized after changing data, verify the generated row counts, missing-data semantics and actual crawl dates, then inspect the page directly from disk.
After changing rendering, check author search, the missing-data toggle and the empty-result state.
Include regenerated data files when publishing a refreshed visualization; include HTML and rendering code only when those change.
While regeneration is deferred under [AGENTS.md](AGENTS.md#visualization-regeneration), preserve both generated datasets, use the [canonical-data validation](#repository-validation) below instead of the snapshot check, and run the JavaScript checks when rendering changes.

## Repository Validation

Run the full offline Python suite after changing roster schemas, joins or canonical data:

```bash
python -B -m unittest discover -s tests -v
```

It checks the current published snapshots as well as builder behavior, roster field order, quality values and shared-profile dates.
The snapshot check deliberately fails when generated datasets lag the CSVs; do not weaken it or regenerate files solely to make it pass while the user has deferred regeneration.
For canonical-data and builder validation during that deferral, run:

```bash
PYTHONPATH=tests python -B -m unittest test_csrankings_rosters test_scholar_citation_data.CitationDataTests test_university_analysis test_profile_provenance test_profile_validation -v
```

These checks build Scholar joins in memory without writing visualization files.
Run the full suite after authorized regeneration and report snapshot synchronization separately until then.
Accepted links without an imported capture may have blank capture dates and missing metrics; the tests verify those missing-data semantics rather than requiring every URL to have a date.
When a Scholar statistics row exists, its capture date must equal the referring roster's Scholar capture date.
The canonical checks also enforce roster and CSRankings ordering, original CSRankings source-field hashes, the current capture/import queue and exact-name affiliation joins.
Shared recipients are identified by normalized ACM recipient IDs before comparing publication URLs, quality flags, capture dates and CSRankings links/dates across awards; missing ACM identities are not inferred from names alone.
Derived CSRankings DBLP fields must agree with the normalized roster URLs, except that documented wrong-person URLs from the identity review require blank lookup fields, as with Kai Li.
CSRankings alignment dates must be valid `YYYY-MM-DD` values when a name link is present and blank when it is absent; a key cannot be assigned to two recipients within one roster.
For visualization changes, also run the JavaScript checks in the [visualization workflow](#google-scholar-citation-visualization).
Before completing an edit, check `git diff --check`, canonical ordering, preservation of unrelated data, and any applicable report totals.
For documentation-only changes, verify field names, local links, section anchors and commands against the existing files without refreshing datasets or starting crawls.

### Capture and Import Backlog

The [capture/import queue](docs/profile_capture_queue.json) lists accepted stored URLs without an accepted capture and Scholar URLs without an imported statistics record.
It excludes blank links and unadopted or unavailable discovery candidates; those remain in the [current review status](docs/profile_review_status.md).
Queue schema version 2 retains roster, name, award year, ACM profile reference and each recipient's exact `stored_url`.
DBLP task URLs are normalized to HTTPS without `.html`, query strings or fragments, so equivalent URL forms share one task without changing the roster URLs.
Other services retain their exact URL as the grouping key.
Regenerate the queue after changing accepted links, capture dates or imported statistics:

```bash
python scripts/build_profile_capture_queue.py --output docs/profile_capture_queue.json
```

The command only reads canonical CSVs and writes the queue; it does not fetch pages, accept captures or update metrics.
Entries await the user's refresh approval, and queue-generation timestamps never substitute for profile capture dates.
Keep this backlog distinct from the unfinished holistic review and the deferred visualization rebuild.

## Git Hygiene

Do not commit these generated artifacts:

```text
.cache/
scripts/__pycache__/
*.pyc
```

The repository `.gitignore` already excludes `.cache/` and Python bytecode.
Keep disposable `tmp/` files out of commits as well; this directory is not currently covered by `.gitignore`.

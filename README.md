# ACM Big Cows 🐮

Data about ACM Fellows and Turing Award winners: the "big cows" of CS.
“Big cows” is a playful translation of 大牛, an informal Chinese term for accomplished experts in a field.

## Data

**The ACM awards directory is the source of truth unless evidence shows it is obviously wrong.**
See the [source policy](AGENTS.md#acm-source-of-truth), [Fellows reconciliation and exceptions](docs/acm_directory_reconciliation_2026-09-17.md), and [Turing Award reconciliation](docs/turing_directory_reconciliation_2026-09-17.md).

- [ACM Fellows](data/acm_fellows.csv): canonical dataset, including ACM, DBLP, and Google Scholar profile links and crawl dates.
- [Turing Award winners](data/turing_award_winners.csv): canonical dataset with profile links and crawl dates, organized by award year.
- [Google Scholar profiles](data/google_scholar_profiles.csv): profile links, affiliations, interests, and citation statistics for ACM Fellows and Turing Award winners.
- [CSRankings profiles](data/csrankings_profiles.csv): faculty records referenced by the exact `csrankings_name` keys in either award roster, including documented historical records.
  Original source fields are preserved; `dblp_profile` reproduces CSRankings' own name-generated link, separately from our reviewed award-profile URLs.

The CSVs are ready to download or use from a clone.
Both award tables include Y/N quality assessments for DBLP and Google Scholar profiles; see the [DBLP review](docs/dblp_profile_quality_2026-09-17.md), [Fellows Scholar review](docs/acm_scholar_quality_2026-09-17.md), and [Turing Scholar review](docs/turing_scholar_quality_2026-09-17.md) for criteria, findings, and inspection limits.
Later [Fellows decisions](docs/check_profiles_full_2026-09-18.md#explicit-user-decisions) and the [full Turing review](docs/check_profiles_turing_2026-09-18.md) supersede those initial findings where documented.
See [Data Notes](docs/data_notes.md) for provenance, reconciliation history, and known source differences.
The [data dictionary](README_FOR_AGENTS.md#data-layout) explains both award schemas, Scholar statistics, joins, dates, and missing values.
A missing profile means the corresponding URL cell is blank; always distinguish ACM, DBLP, and Scholar when reporting coverage.
A quality rating of `N` can describe either a missing link or a poor linked profile.
Profile crawl dates record accepted page captures; `csrankings_name_alignment_date` records the name-link decision in each award roster.
The CSRankings lookup table has no date column.
See the [current profile-review status](docs/profile_review_status.md) for remaining verification and capture/import work.

## Visualizations

Start at the [visualization landing page](https://lintool.github.io/acm-bigcows/).
Explore separate citation timelines for [ACM Fellows](https://lintool.github.io/acm-bigcows/acm_fellows.html) and [Turing Award winners](https://lintool.github.io/acm-bigcows/turing_award_winners.html).
The timelines use generated snapshots and can lag the canonical CSVs; see [Data Notes](docs/data_notes.md) for imports and deferred regeneration.
Bars show citations received in each calendar year, not publications produced that year.
Each person's bars are scaled to their own highest year in the displayed window, so equal-height bars across people can represent different citation counts.
Cites and h-index show Scholar's reported all-time metrics, which may include known publication-attribution errors documented in the reviews.
Both timelines start in 1986 and end in the current UTC year.
Gray histograms indicate Scholar profiles rated `N` for quality; their citation counts remain visible.
Darker bars show years before the award; lighter bars show the award year and later years.
An empty bar can mean a reported zero or an absent year in the captured history; it does not establish zero citations.
Recipients without citation histories are hidden by default; use **Show missing Scholar data** to include them.
Click **Year**, **Name**, **Cites**, **cites at award**, or **h-index** to sort, and expand **About the Data** for coverage counts, the estimate's calculation and source links.
Use the small icons beside each name to open available ACM, Google Scholar and DBLP profiles; hover over an icon to identify its service.
Open `index.html` directly in a browser with the accompanying HTML, JavaScript, CSS and `assets/` directory in place; no server or network connection is required to view the timelines.

## Local Analysis

Use Python 3.10 or newer, available as `python`.
The scripts use the standard library.
From this repository, count university affiliations in the committed data:

```bash
python scripts/analyze_acm_fellow_universities.py --min-count 5
```

The [analysis reference](README_FOR_AGENTS.md#acm-fellow-university-analysis) explains the joins, normalization, and available options.
Maintainers can also [synchronize accepted CSRankings name links](README_FOR_AGENTS.md#csrankings-name-links) or [regenerate the visualization](README_FOR_AGENTS.md#google-scholar-citation-visualization).

## Updating the Data

Fetching is handled by the shared [bigcows-crawler repository](https://github.com/lintool/bigcows-crawler).
It stores pages and reports in its local, Git-ignored `.cache/`; this repository owns the reviewed datasets and analysis.
ACM profile fetching uses Safari on macOS and does not edit the CSVs automatically.
Scholar updates follow a [fresh-capture, identity-review, and import workflow](README_FOR_AGENTS.md#review-and-import-google-scholar-data) before the visualization data is regenerated.
DBLP updates follow a [separate reviewed import](README_FOR_AGENTS.md#review-and-import-dblp-data) into the award rosters.

See [README_FOR_AGENTS.md](README_FOR_AGENTS.md) for maintenance workflows, application-specific crawler commands, and data-review rules.
[AGENTS.md](AGENTS.md) defines the documentation policy.

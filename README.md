# ACM Big Cows 🐮

Data about ACM Fellows and Turing Award winners: the "big cows" of CS.
“Big cows” is a playful translation of 大牛, an informal Chinese term for accomplished experts in a field.

## Data

- [ACM Fellows](data/acm_fellows.csv): canonical dataset, including ACM, DBLP, and Google Scholar profile links and crawl dates.
- [Turing Award winners](data/turing_award_winners.csv): canonical dataset with profile links and crawl dates, organized by award year.
- [Google Scholar profiles](data/google_scholar_profiles.csv): profile links, affiliations, interests, and citation statistics for ACM Fellows and Turing Award winners.
- [CSRankings profiles](data/csrankings_profiles.csv): faculty rows matched by name to award recipients with stored DBLP links.

The CSVs are ready to download or use from a clone.
Both award tables include Y/N quality assessments for DBLP and Google Scholar profiles; see the [DBLP review](docs/dblp_profile_quality_2026-09-17.md), [Fellows Scholar review](docs/acm_scholar_quality_2026-09-17.md), and [Turing Scholar review](docs/turing_scholar_quality_2026-09-17.md) for criteria, findings, and inspection limits.
See [Data Notes](docs/data_notes.md) for provenance, reconciliation history, and known source differences.
The [data dictionary](README_FOR_AGENTS.md#data-layout) explains both award schemas, Scholar statistics, joins, dates, and missing values.
A missing profile means the corresponding URL cell is blank; always distinguish ACM, DBLP, and Scholar when reporting coverage.
A quality rating of `N` can describe either a missing link or a poor linked profile, while a crawl date records when a page was captured.

## Visualizations

Start at the [visualization landing page](https://lintool.github.io/acm-bigcows/).
Explore separate citation timelines for [ACM Fellows](https://lintool.github.io/acm-bigcows/acm_fellows.html) and [Turing Award winners](https://lintool.github.io/acm-bigcows/turing_award_winners.html).
Bars show citations received in each calendar year, not publications produced that year.
Each person's bars are scaled to their own highest year in the displayed window, so equal-height bars across people can represent different citation counts.
Citations and h-index show Scholar's reported all-time metrics, which may include known publication-attribution errors documented in the reviews.
Both timelines show the same 45-year window ending in the current year.
An empty bar can mean a reported zero or an absent year in the captured history; it does not establish zero citations.
Recipients without citation histories are hidden by default; use **Show missing Scholar data** to include them.
Click **Year**, **Name**, **Citations**, or **h-index** to sort, and expand **About the Data** for coverage counts and source links.
Open `index.html` directly in a browser with the accompanying HTML, JavaScript, and CSS files in place; no server is required, although the timelines load D3 from a CDN.

## Local Analysis

Use Python 3.10 or newer, available as `python`.
The scripts use the standard library.
From this repository, count university affiliations in the committed data:

```bash
python scripts/analyze_acm_fellow_universities.py --min-count 5
```

The [analysis reference](README_FOR_AGENTS.md#acm-fellow-university-analysis) explains the joins, normalization, and available options.
Maintainers can also [rebuild CSRankings alignments](README_FOR_AGENTS.md#csrankings-dblp-alignment) or [regenerate the visualization](README_FOR_AGENTS.md#google-scholar-citation-visualization).

## Updating The Data

Fetching is handled by the shared [bigcows-crawler repository](https://github.com/lintool/bigcows-crawler).
It stores pages and reports in its local, Git-ignored `.cache/`; this repository owns the reviewed datasets and analysis.
ACM profile fetching uses Safari on macOS and does not edit the CSVs automatically.
Scholar updates follow a [fresh-capture, identity-review, and import workflow](README_FOR_AGENTS.md#review-and-import-google-scholar-data) before the visualization data is regenerated.
DBLP updates follow a [separate reviewed import](README_FOR_AGENTS.md#review-and-import-dblp-data) into the award rosters.

See [README_FOR_AGENTS.md](README_FOR_AGENTS.md) for maintenance workflows, application-specific crawler commands, and data-review rules.
[AGENTS.md](AGENTS.md) defines the documentation policy.

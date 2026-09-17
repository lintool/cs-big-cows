# CS Big Cows 🐮

Data about ACM Fellows and Turing Award winners: the "big cows" of CS.

## Data

- [ACM Fellows](data/acm_fellows.csv): canonical dataset, including ACM profile, DBLP, and Google Scholar links.
- [Turing Award winners](data/turing_award_winners.csv): canonical dataset, organized by award year.
- [DBLP profiles](data/dblp_profiles.csv): known DBLP profile links for ACM Fellows.
- [Google Scholar profiles](data/google_scholar_profiles.csv): profile links, affiliations, interests, and citation statistics for ACM Fellows and Turing Award winners.
- [CSRankings profiles](data/csrankings_profiles.csv): faculty rows that align to known DBLP profiles.

The CSVs are ready to download or use from a clone.
See [Data Notes](docs/data_notes.md) for provenance, reconciliation history, and known source differences.

## Visualization

Explore the [ACM Fellow citation timelines](https://lintool.github.io/cs-big-cows/scholar_citations.html), which join Fellow records with Google Scholar citation-by-year data.
The page loads a separate generated `docs/scholar_data.js` file.
Open `docs/scholar_citations.html` directly in a browser with the accompanying JavaScript files in place; no server is required, although D3 loads from a CDN.

## Local Analysis

Use Python 3.10 or newer, available as `python`.
The scripts use the standard library.
From this repository, count university affiliations in the committed data:

```bash
python scripts/analyze_acm_fellow_universities.py --min-count 5
```

The [analysis reference](README_FOR_AGENTS.md#acm-fellow-university-analysis) explains the joins, normalization, and available options.
Maintainers can also [rebuild CSRankings alignments](README_FOR_AGENTS.md#csrankings-dblp-alignment) or [regenerate the visualization](README_FOR_AGENTS.md#google-scholar-citation-visualization).

## Updating the Data

Fetching is handled by the shared [bigcows-crawler repository](https://github.com/lintool/bigcows-crawler).
It stores pages and reports in its local, Git-ignored `.cache/`; this repository owns the reviewed datasets and analysis.
ACM profile fetching uses Safari on macOS and does not edit the CSVs automatically.

See [README_FOR_AGENTS.md](README_FOR_AGENTS.md) for maintenance workflows, application-specific crawler commands, and data-review rules.
[AGENTS.md](AGENTS.md) defines the documentation policy.

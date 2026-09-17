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

## Visualizations

Explore separate citation timelines for [ACM Fellows](https://lintool.github.io/cs-big-cows/acm_fellows.html) and [Turing Award winners](https://lintool.github.io/cs-big-cows/turing_award_winners.html).
Each page joins its award roster with Google Scholar citation-by-year data and links to the other visualization.
The pages load separate generated data files and share a renderer and stylesheet.
Open `docs/acm_fellows.html` or `docs/turing_award_winners.html` directly in a browser with the accompanying JavaScript and CSS files in place; no server is required, although D3 loads from a CDN.

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

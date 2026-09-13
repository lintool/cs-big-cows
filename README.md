# CS Big Cows 🐮

Data about ACM Fellows and Turing Award winners: the "big cows" of CS.

## Data

- [data/acm_fellows.csv](data/acm_fellows.csv): canonical ACM Fellows dataset, including ACM profile, DBLP, and Google Scholar links.
- [data/csrankings_profiles.csv](data/csrankings_profiles.csv): CSRankings faculty rows that align to known DBLP profiles.
- [data/dblp_profiles.csv](data/dblp_profiles.csv): known DBLP profile links for ACM Fellows.
- [data/google_scholar_profiles.csv](data/google_scholar_profiles.csv): known Google Scholar profile links, affiliations, keyword interests, citation stats, and citation-by-year data for ACM Fellows and Turing Award winners.
- [data/turing_award_winners.csv](data/turing_award_winners.csv): canonical ACM A. M. Turing Award winners dataset.

CSV files are kept in `data/` and use Unix LF line endings.

## Visualization

- [ACM Fellow citation timelines](https://lintool.github.io/cs-big-cows/scholar_citations.html): static visualization generated from ACM Fellow rows joined to Google Scholar citation-by-year data. The GitHub Pages source is `docs/`, where this is served from `scholar_citations.html`.

## Crawlers

Crawlers are shared from the sibling [bigcows-crawler](https://github.com/lintool/bigcows-crawler/blob/main/README.md)
repository. Its `.cache/` stores fetched pages, CSRankings shards, and crawl reports
locally and is ignored by Git. Profile crawlers require `--data`; Scholar CSV
exports require an explicit `--output`.

For a fresh checkout, first follow the
[fresh-crawl instructions](README_FOR_AGENTS.md#crawlers) to capture profiles,
then compare using that crawl's date.

Run this comparison from this directory only if the retained September 13
cache and manifest are already present in `../bigcows-crawler/.cache/`.
These local artifacts are Git-ignored and are not included in either clone:

```bash
python3 ../bigcows-crawler/scripts/compare_acm_fellow_profiles.py --crawl-date 2026-09-13 --data data/acm_fellows.csv
```

To fetch Scholar profiles:

```bash
python3 ../bigcows-crawler/scripts/cache_google_scholar_profiles.py --data data/acm_fellows.csv --output data/google_scholar_profiles.csv
```

ACM profiles use regular Safari through AppleScript on macOS, with 5–7 seconds
between profiles and 60–90 seconds every 25 attempts. See the
[shared crawler reference](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md) for setup, fresh
crawls, resuming, and troubleshooting. The ACM crawler never edits the CSV.
The ACM example is a read-only comparison with the September 13 captures; it
reparses HTML without changing the cache or completion records. Fetching requires
a new crawl date and a stable input snapshot; a manifest verifies the input on
resume. Use the original date when resuming. The latest reviewed crawl
is recorded in [data_notes.md](data_notes.md); no crawl is selected automatically.

## Scripts

- `scripts/build_csrankings_profiles.py`: builds `data/csrankings_profiles.csv` from the sibling crawler’s cached CSRankings shards and known DBLP profiles.
- `scripts/analyze_acm_fellow_universities.py`: counts normalized ACM Fellow university affiliations from joined Scholar and CSRankings data.
- `scripts/build_scholar_citation_visualization.py`: regenerates `docs/scholar_citations.html` from `data/acm_fellows.csv` and `data/google_scholar_profiles.csv`.

See [README_FOR_AGENTS.md](README_FOR_AGENTS.md) for crawler/cache details intended for future coding agents.
See [data_notes.md](data_notes.md) for current known data oddities.

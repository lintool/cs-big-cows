# CS Big Cows 🐮

Data about ACM Fellows and Turing Award winners: the "big cows" of CS.

## Data

- [data/acm_fellows.csv](data/acm_fellows.csv): canonical ACM Fellows dataset, including ACM profile, DBLP, and Google Scholar links.
- [data/csrankings_profiles.csv](data/csrankings_profiles.csv): CSRankings faculty rows that align to known DBLP profiles.
- [data/dblp_profiles.csv](data/dblp_profiles.csv): known DBLP profile links for ACM Fellows.
- [data/google_scholar_profiles.csv](data/google_scholar_profiles.csv): known Google Scholar profile links, affiliations, keyword interests, citation stats, and citation-by-year data for ACM Fellows and Turing Award winners.
- [data/turing_award_winners.csv](data/turing_award_winners.csv): canonical ACM A. M. Turing Award winners dataset.

CSV files are kept in `data/` and use Unix LF line endings.

## Scripts

- `scripts/cache_google_scholar_profiles.py`: validates Google Scholar profile links, caches fetched Scholar pages for reuse, and writes `data/google_scholar_profiles.csv`.
- `scripts/cache_acm_fellow_profiles.py`: caches ACM Fellow profile pages and reports parsed profile fields for comparison with `data/acm_fellows.csv`.
- `scripts/cache_acm_fellow_profiles_playwright.py`: browser-backed ACM profile crawler for pages that require a real browser session.
- `scripts/cache_dblp_profiles.py`: caches DBLP profile pages and reports parsed profile titles for comparison with `data/acm_fellows.csv`.
- `scripts/cache_csrankings.py`: caches CSRankings faculty CSV shards from GitHub under `.cache/`.
- `scripts/build_csrankings_profiles.py`: builds `data/csrankings_profiles.csv` from cached CSRankings shards and known DBLP profiles.
- `scripts/analyze_acm_fellow_universities.py`: counts normalized ACM Fellow university affiliations from joined Scholar and CSRankings data.

See [README_FOR_AGENTS.md](README_FOR_AGENTS.md) for crawler/cache details intended for future coding agents.
See [data_notes.md](data_notes.md) for current known data oddities.

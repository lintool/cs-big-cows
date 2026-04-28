# CS Big Cows 🐮

Data about major computer science award recipients and ACM Fellows: the "big cows" of CS.

## Data

- [data/acm-fellows.csv](data/acm-fellows.csv): canonical ACM Fellows dataset.
- [data/turing-award-winners.csv](data/turing-award-winners.csv): canonical ACM A. M. Turing Award winners dataset.
- [data/google-scholar-profiles.csv](data/google-scholar-profiles.csv): Google Scholar profile links for ACM Fellows.

## Scripts

- `scripts/validate_google_scholar_profiles.py`: validates ACM Fellows Google Scholar profile links and caches fetched Scholar pages for reuse.
- `scripts/cache_acm_fellow_profiles.py`: caches ACM Fellow profile pages and reports parsed profile fields.

See [README_FOR_AGENTS.md](README_FOR_AGENTS.md) for crawler/cache details intended for future coding agents.

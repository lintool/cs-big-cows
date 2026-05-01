---
name: analyze-acm-fellows
description: Analyze ACM Fellows in the cs-big-cows repository, especially university or institutional distribution across ACM Fellows. Use when Codex is asked questions about where ACM Fellows are distributed, university counts, affiliation counts, institutional tallies, or joins between ACM Fellows, Google Scholar profiles, and CSRankings profiles.
---

# Analyze ACM Fellows

## University Distribution

Use this skill inside the `cs-big-cows` repository when the user asks about ACM Fellow distribution across universities or institutions.

Default workflow:

1. Check repository status:

   ```bash
   git status --short --branch
   ```

2. Run the helper:

   ```bash
   python scripts/analyze_acm_fellow_universities.py
   ```

3. Report the count-descending university table.

The helper joins:

- `data/acm_fellows.csv` to `data/google_scholar_profiles.csv` by `google_scholar_profile`;
- `data/acm_fellows.csv` to `data/csrankings_profiles.csv` by `dblp_profile`.

It extracts universities from Google Scholar and CSRankings affiliation strings, normalizes common institution variants, and counts every distinct normalized university found for a fellow. If both sources say the same university, that fellow counts once for that university. If the sources provide different universities, that fellow contributes once to each distinct university.

Important normalization note: preserve `University of British Columbia` / `UBC` as its own university. Do not collapse it into `Columbia University`.

The helper can print normalization warnings to stderr with `--show-warnings` when it suppresses ambiguous captures, such as parent-system names or substring collisions. Review those warnings when counts look surprising.

## Commands

Show all universities:

```bash
python scripts/analyze_acm_fellow_universities.py
```

Show only universities with at least five fellows:

```bash
python scripts/analyze_acm_fellow_universities.py --min-count 5
```

Include example fellow names per university:

```bash
python scripts/analyze_acm_fellow_universities.py --examples 3
```

Review normalization warnings:

```bash
python scripts/analyze_acm_fellow_universities.py --show-warnings
python scripts/analyze_acm_fellow_universities.py --show-warnings --warnings-limit 100
```

## Guardrails

- Treat affiliations as evidence from profile sources, not canonical employment history.
- Do not count companies or generic job titles as universities.
- Do not modify CSV files during analysis unless the user explicitly asks.
- If results look stale, refresh Google Scholar or CSRankings data with their dedicated workflows before rerunning this analysis.

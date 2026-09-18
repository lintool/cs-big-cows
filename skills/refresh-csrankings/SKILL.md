---
name: refresh-csrankings
description: Refresh CSRankings data, synchronize accepted profile keys, or validate existing CSRankings matches in acm-bigcows.
---

# Refresh CSRankings

Use this skill only in `acm-bigcows` for CSRankings refresh, alignment, and profile-validation requests.
Read the [name-link reference](../../README_FOR_AGENTS.md#csrankings-name-links) for canonical synchronization and the [legacy alignment reference](../../README_FOR_AGENTS.md#csrankings-dblp-alignment) for output fields and validation criteria.
The shared [crawler reference](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md#csrankings-crawler) owns fetching and pacing.

## Refresh or Rebuild

1. Check repository status and distinguish a requested source refresh from a rebuild using existing shards.
2. Follow the name-link reference to refresh the requested source scope and synchronize accepted exact keys, retaining documented historical records.
   Do not overwrite the canonical table with the legacy `scripts/build_csrankings_profiles.py`, which does not consume explicit name links.
3. Validate exact key coverage, uniqueness, source fields and documented DBLP exceptions, retaining input snapshots and the validation report.
   Follow the name-link reference to verify and update the source-field manifest after authorized source changes; preserve original fields even when upstream identifiers are wrong.
4. Report changes, cache coverage, and unresolved matches with representative evidence.

## Validate Existing Profiles

Use the reference's read-only validation procedure when asked to check existing matches.
Report suspicious name associations with both source names, the affiliation, the profile URL, and the reason for concern.
Do not fetch or rebuild merely to perform a validation request, and do not modify CSVs unless fixes are requested.
Do not force weak matches into the output or edit the source award rosters without an explicit request.

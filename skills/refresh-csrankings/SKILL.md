---
name: refresh-csrankings
description: Refresh CSRankings data, rebuild its DBLP-aligned profiles, or validate existing CSRankings matches in acm-bigcows.
---

# Refresh CSRankings

Use this skill only in `acm-bigcows` for CSRankings refresh, alignment, and profile-validation requests.
Read the [alignment reference](../../README_FOR_AGENTS.md#csrankings-dblp-alignment) for commands, cache completeness, output fields, matching rules, and validation criteria.
The shared [crawler reference](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md#csrankings-crawler) owns fetching and pacing.

## Refresh or Rebuild

1. Check repository status and distinguish a requested source refresh from a rebuild using existing shards.
2. Follow the alignment reference to refresh the requested source scope and run `scripts/build_csrankings_profiles.py`.
3. Review included, unmatched, and ambiguous counts in the alignment report, investigating surprising drops before treating the update as complete.
4. Report changes, cache coverage, and unresolved matches with representative evidence.

## Validate Existing Profiles

Use the reference's read-only validation procedure when asked to check existing matches.
Report suspicious name associations with both source names, the affiliation, the profile URL, and the reason for concern.
Do not fetch or rebuild merely to perform a validation request, and do not modify CSVs unless fixes are requested.
Do not force weak matches into the output or edit the DBLP source dataset without an explicit request.

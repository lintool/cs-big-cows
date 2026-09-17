---
name: analyze-acm-fellows
description: Analyze university or institutional distribution among ACM Fellows in acm-bigcows using the joined Scholar and CSRankings affiliation data.
---

# Analyze ACM Fellows

Use this skill in `acm-bigcows` for university counts, institutional tallies, and affiliation-distribution questions.
Read the [analysis reference](../../README_FOR_AGENTS.md#acm-fellow-university-analysis) for helper commands, joins, counting semantics, and normalization rules.

## Workflow

1. Check repository status and run `scripts/analyze_acm_fellow_universities.py` with options appropriate to the requested counts or examples.
2. Investigate surprising counts using the helper's normalization warnings and representative Fellows.
3. Report the count-descending table, requested examples, and material coverage or ambiguity limits.
   Explain that a Fellow can count toward multiple institutions and that profile affiliations do not establish employment history.

## Scope

Analysis is read-only unless the user asks for data changes.
If source freshness limits the answer, state the limitation and follow the [reviewed Scholar workflow](../../README_FOR_AGENTS.md#review-and-import-google-scholar-data) or [CSRankings workflow](../../README_FOR_AGENTS.md#csrankings-dblp-alignment) only when a refresh is within the user's requested scope.

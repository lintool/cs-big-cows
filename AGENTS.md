# Repository Instructions

## ACM Source of Truth

**The ACM awards directory is the source of truth unless there is evidence that it is obviously wrong.**
Use its award-recipient records and displayed names by default; do not replace them based on preference, familiarity, a different abbreviation or capitalization alone.
An exception needs concrete, cited evidence identifying the error and the same recipient, preferably from ACM itself, the recipient or their institution.
Record the directory value, supported alternative, source links and reasoning in [Data Notes](docs/data_notes.md) or a linked review before applying an exception.
The [Fellows reconciliation](docs/acm_directory_reconciliation_2026-09-17.md) records confirmed historical omissions and the subsequent name-error review.
The [Turing Award reconciliation](docs/turing_directory_reconciliation_2026-09-17.md) records complete annual coverage and reviewed profile links.
This authority concerns award data, not independent DBLP or Google Scholar profile quality.

## Finalized Award CSVs

The user has confirmed that `data/acm_fellows.csv` and `data/turing_award_winners.csv` are finalized after reconciliation.
Do not change their rows, fields or ordering during consistency sweeps, documentation cleanup or code maintenance.
Further changes to either award CSV require an explicit user request to change that data; general requests to fix repository inconsistencies do not reopen the finalized rows.

## Visualization Regeneration

During the current data-reconciliation work, do not regenerate the visualization datasets unless the user explicitly requests it.
The user will regenerate them at the end; preserve the checked-in snapshots and distinguish data-validation results from snapshot-synchronization checks while they are deferred.

## Crawl Artifact Storage

Store all crawl captures and their input snapshots, manifests, state, reports, and logs under the sibling `bigcows-crawler/.cache/`, including custom runs and dry runs that write crawl artifacts.
Use a distinct run directory there when isolation is needed.
Crawl artifacts are retained evidence; the general rule to put disposable scratch files in `tmp/` does not apply to them.
Keep canonical datasets and published review documentation in this repository.
Before starting a crawl, read the [crawler workflow](README_FOR_AGENTS.md#crawlers) and the shared crawler's [authoritative instructions](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md).

## Publication Profile Quality

Before matching or rating DBLP or Google Scholar profiles for either award roster, follow the authoritative [publication profile quality criteria](README_FOR_AGENTS.md#publication-profile-quality), including the linked review reports and explicit user decisions.
Use [Check Profiles](skills/check-profiles/SKILL.md) for a holistic review of Scholar, DBLP and CSRankings identities, publication coverage and contamination.
Use the [missing-profile definitions](README_FOR_AGENTS.md#missing-profiles-and-review-status) when reporting coverage or review queues.
Consult the [current review status](docs/profile_review_status.md) before resuming verification; historical checkpoint prose is not the current open-case queue.

## Documentation Audiences

- README.md is for humans: project overview, setup, basic usage, and a few useful examples.
  Keep it concise.
- README_FOR_AGENTS.md is for agents: detailed workflows, implementation notes, constraints, validation, and troubleshooting.
- [docs/data_notes.md](docs/data_notes.md) records dataset provenance, reconciliation history, and deliberate source differences.
- Avoid duplicating detailed instructions across these files.
  Link to the authoritative location instead.

## Documentation Formatting

- Use Title Caps for headings, capitalizing major words while preserving acronyms and proper names.
  Leave articles, conjunctions and short prepositions lowercase unless they begin or end the heading, as in `Updating the Data` and `Linked N Profiles to Review`.
- Put each prose sentence on its own source line; do not hard-wrap sentences across lines or put multiple sentences on one line.
- Preserve paragraph breaks and Markdown structure, including list indentation, tables, code blocks, and YAML front matter.

## Data Notes

- Keep data notes in `docs/data_notes.md`.
- Give each review, reconciliation, or enrichment batch its own level-two entry headed `## YYYY-MM-DD HH:mm EDT - Descriptive Title`, using the actual completion time in `America/Toronto` and the applicable timezone abbreviation (`EDT` or `EST`).
- Record the completion time when finishing new work; do not use the time of a later documentation edit.
- Keep historical entries date-only (`## YYYY-MM-DD - Descriptive Title`) unless a reliable record establishes the completion time of the work described by the entry.
  Do not invent times or infer completion from file modification times or an earlier crawl's completion time.
- Keep entries in reverse chronological order, newest first; when timestamps are unavailable or equal, preserve the known order of completion.
- Prefix subsection headings with the entry's timestamp, or its date for date-only historical entries; the document title does not need a timestamp.
- Prepend new entries and preserve earlier provenance, source links, and deliberate differences.
- Keep Markdown links relative to the notes file; describe filesystem paths relative to the repository root unless stated otherwise.

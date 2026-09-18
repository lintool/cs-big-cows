# Repository Instructions

## Crawl Artifact Storage

Store all crawl captures and their input snapshots, manifests, state, reports, and logs under the sibling `bigcows-crawler/.cache/`, including custom runs and dry runs that write crawl artifacts.
Use a distinct run directory there when isolation is needed.
Crawl artifacts are retained evidence; the general rule to put disposable scratch files in `tmp/` does not apply to them.
Keep canonical datasets and published review documentation in this repository.
Before starting a crawl, read the [crawler workflow](README_FOR_AGENTS.md#crawlers) and the shared crawler's [authoritative instructions](https://github.com/lintool/bigcows-crawler/blob/main/README_FOR_AGENTS.md).

## Publication Profile Quality

Before matching or rating DBLP or Google Scholar profiles for either award roster, follow the authoritative [publication profile quality criteria](README_FOR_AGENTS.md#publication-profile-quality), including the linked review reports and explicit user decisions.
Use the [missing-profile definitions](README_FOR_AGENTS.md#missing-profiles-and-review-status) when reporting coverage or review queues.

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

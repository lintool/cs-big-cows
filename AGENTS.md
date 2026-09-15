# Repository Instructions

## Documentation Audiences

- README.md is for humans: project overview, setup, basic usage, and a few useful examples.
  Keep it concise.
- README_FOR_AGENTS.md is for agents: detailed workflows, implementation notes, constraints, validation, and troubleshooting.
- [docs/data_notes.md](docs/data_notes.md) records dataset provenance, reconciliation history, and deliberate source differences.
- Avoid duplicating detailed instructions across these files.
  Link to the authoritative location instead.

## Documentation Formatting

- Use Title Caps for headings, capitalizing major words while preserving acronyms and proper names.
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

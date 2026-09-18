# Historical CSRankings Link Recovery

Recovered and linked all six previously open historical-source cases on September 18, 2026.
These are historical CSRankings memberships, not claims of inclusion in the current faculty list.

## Source and Search Scope

Searched the retained 26 alphabetical faculty files, combined source and DBLP aliases by alternate names, surname, Scholar ID and institution context.
The alias data maps Larry S. Davis to Larry Davis 0001 and Laxmi Narayan Bhuyan to Laxmi N. Bhuyan, but those aliases did not produce current faculty rows for these recipients.
Inspected upstream Git snapshots through 2020, 2022, 2024, 2025 and 2026, including the older combined file from before the alphabetical split.
All six original rows occur together in [CSRankings commit 4b714f69c839ca538825054f94bdf57f5d4ea3da](https://github.com/emeryberger/CSrankings/blob/4b714f69c839ca538825054f94bdf57f5d4ea3da/csrankings.csv), dated December 30, 2020.
The commit-addressed file is the source for all six new lookup records; later snapshots were discovery evidence only.

That source has four columns: `name`, `affiliation`, `homepage` and `scholarid`.
It predates the ORCID column, so each new local `orcid` is blank to represent an absent source field; no ORCID was inferred or replaced with a synthetic identifier.
All four available upstream values are copied literally, including old HTTP homepages, institutional spellings, Scholar identifiers and `NOSCHOLARPAGE` placeholders.
The generated `dblp_profile` follows the existing CSRankings name-to-URL rule, independently of the award-roster DBLP links.

## Accepted Links

| ACM Recipient | Exact CSRankings Key | Historical Affiliation | Original Scholar ID | Identity Evidence |
| --- | --- | --- | --- | --- |
| Bartlett, Peter L | Peter L. Bartlett | University of California - Berkeley | UPVvV6kAAAAJ | ACM learning-theory identity, Berkeley affiliation and personal statistics-department homepage agree; differing reviewed Scholar ID is preserved separately. |
| Davis, Larry S | Larry S. Davis | University of Maryland - College Park | lc0ARagAAAAJ | ACM computer-vision identity, Maryland affiliation and reviewed Scholar ID agree; DBLP aliases explain the later Larry Davis 0001 spelling. |
| Hellerstein, Joseph M | Joseph M. Hellerstein | University of California - Berkeley | uFJi3IUAAAAJ | ACM database-systems identity, Berkeley affiliation and reviewed Scholar ID agree. |
| Gottlieb, Allan | Allan Gottlieb | New York University | NOSCHOLARPAGE | Exact name, NYU affiliation and personal NYU homepage identify the shared-memory-multiprocessing Fellow. |
| Bhuyan, Laxmi Narayan | Laxmi N. Bhuyan | University of California - Riverside | NOSCHOLARPAGE | Name expansion is explicitly supported by DBLP aliases; Riverside homepage and historical institutional CSRankings printout corroborate the identity. |
| Hopcroft, John E | John E. Hopcroft | Cornell University | NOSCHOLARPAGE | Exact name, Cornell affiliation and personal Cornell homepage agree with the recipient's retained Scholar and ACM identity. |

The source rows' original homepages are retained in `data/csrankings_profiles.csv`.
The Bartlett identifier and the three missing-Scholar placeholders were not replaced with our independently reviewed Scholar links.
These source values do not authorize changing publication-profile links or ratings in either award roster.

## Applied Changes and Validation

Added six Fellows name links and the shared Hopcroft Turing link, each with alignment date `2026-09-18`: 14 award-roster cells total.
Added six lookup rows, producing 835 distinct keys: 833 Fellows links and 18 Turing links with 16 shared keys.
Every previous lookup row and source-field hash is preserved.
The exact lookup-key union, shared-recipient ownership, alignment dates and generated DBLP URLs are validated.
ACM identities and award fields, publication-profile URLs and ratings, publication capture dates, Scholar statistics, the capture/import queue and visualization snapshots are unchanged by this batch.

The source-manifest builder now accepts an explicitly supplied four-column `--legacy-source` only for individually selected `--legacy-name` values.
It records the raw source hash and missing-ORCID representation and rejects repaired fields, invented ORCIDs, absent selected names, conflicting selected duplicates and malformed rows.
Current alphabetical shards and the earlier five-column historical input retain their strict schema checks; legacy evidence cannot override either source category.

Raw source files, commit responses, fetch timestamps and hashes, input snapshots, accepted source rows, field changes and validation results are retained under `../bigcows-crawler/.cache/csrankings-history-recovery-2026-09-18/`.
This source-recovery work did not crawl Scholar, DBLP or ACM profiles or regenerate visualizations.

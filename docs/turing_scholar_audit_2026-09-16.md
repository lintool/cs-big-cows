# Turing Award Google Scholar Review — September 16, 2026

Completed the import at 22:13 EDT on September 16, 2026, after web searches and a fresh crawl of all existing Turing Scholar links.
The [row-level audit](turing_scholar_audit_2026-09-16.csv) records all 81 recipients, decisions, identity evidence, sources, and available capture timestamps and hashes.

## Results

| Check | Result |
| --- | ---: |
| Recipients reviewed | 81 |
| Initially blank entries searched | 39 |
| Existing profile URLs fetched | 42 |
| Additional candidate URLs fetched | 2 |
| Matching profiles retained with fresh statistics | 40 |
| Wrong-person links cleared | 2 |
| Newly verified links from the missing-profile search | 0 |
| Final blank Scholar fields | 41 |

All 42 existing URLs returned HTTP 200, but two identified different people.
Both additional candidates returned HTTP 404.
The crawl made 44 requests, with no retries or blocking, using a 5–7 second delay and a 120–150 second pause after 25 requests.
Captures were fetched on September 17 UTC, corresponding to the evening of September 16 in Toronto.

## Identity Corrections

- **E. Allen Emerson:** `kTmc3LAAAAAJ` identifies Eric Emerson and lists disability-health publications.
  The [Lancaster University profile](https://www.lancaster.ac.uk/health-and-medicine/about-us/people/eric-emerson) supports that identity; the intended recipient's [University of Texas page](https://www.cs.utexas.edu/~emerson/) concerns formal verification and model checking.
  No replacement profile was verified, so the link and its unreferenced statistics record were removed.
- **Kenneth E. Iverson:** `RBb84VMAAAAJ` identifies Kenneth R. Iversen and lists cryptographic elections and Norwegian healthcare-security publications.
  [Springer's CRYPTO proceedings](https://link.springer.com/book/10.1007/3-540-46766-1?page=2) attribute the leading publication to Kenneth R. Iversen; the intended recipient's [Turing lecture](https://www.jsoftware.com/papers/tottoc.htm) concerns APL and notation.
  No replacement profile was verified, so the link and its unreferenced statistics record were removed.

## Missing-Profile Search

All 39 initially blank entries received general web searches and Scholar-profile site searches, including name variants where useful.
Institutional pages, candidate publications, prior review decisions, and coauthor links in the existing Fellows captures were used to assess leads.
No sufficiently supported, available new profile was found.
This is a best-effort search outcome, not proof that these people have no Scholar profile.

Herbert A. Simon's historical candidates `tk2qT34AAAAJ` and `9d7rMrkAAAAJ` both returned HTTP 404 and were not imported.
Namesakes for Frances Allen, Peter Naur, Manuel Blum, Andrew Yao, Robin Milner, and John McCarthy were rejected.
Generic Scholar search links for Tim Berners-Lee and Silvio Micali did not establish author profiles.
A page mentioning Juris Hartmanis linked to John Hopcroft's Scholar ID, which was not reassigned.
A Michael Stonebraker directory lead did not yield a usable profile ID.
Other unresolved entries remain blank, with individual outcomes recorded in the CSV audit.

## Identity and Publication Limits

Retained profiles were reviewed using their names, affiliations where available, and representative publications from the fetched profile page.
All 30 profiles shared with ACM Fellows retained the same Scholar name and affiliation as the earlier reviewed captures.
The review establishes supported profile identities; it does not validate every publication, paginate complete publication lists, or independently recalculate Scholar's totals.

David Patterson's previously documented attribution conflict remains: the profile includes *Clio and the Economics of QWERTY*, by Paul A. David.
Frederick Brooks's profile also has a possible attribution issue: *Computer architecture: a quantitative approach* lists Patterson, Hennessy, and Goldberg as authors, without Brooks.
These are retained as the correct people's profiles, with raw Scholar totals and explicit audit notes.
Sparse affiliation or missing verified-email metadata remains noted where applicable.

## Import and Validation

Replaced 36 existing statistics records with fresh captures and added four previously absent records for Charles H. Bennett, Gilles Brassard, Andrew Barto, and Richard Sutton.
Removed the two wrong-person records, leaving 1,260 unique profiles in `data/google_scholar_profiles.csv`.
Every retained Turing profile now has statistics from this crawl; no historical fallback was used.

Validated all imported records against the fresh cache, the 81-row roster and its canonical ordering, unique profile URLs, LF line endings, and preservation of non-Scholar recipient fields.
The earlier synchronization from ACM Fellows is preserved.
ACM Fellows, DBLP, CSRankings, and all Scholar visualization files, including `docs/scholar_data.js`, remain unchanged by this refresh.
The visualization's data snapshot has not been regenerated from the updated canonical CSVs.

Crawl and review artifacts are retained under `../bigcows-crawler/.cache/turing-scholar-refresh-2026-09-16/`: input snapshots, manifest, HTML cache, crawl report and state, search results, decisions, import script, and validation results.
These scratch files are not required by the application and are not intended for the PR.

## General Web Search Follow-Up

A subsequent pass searched all 41 remaining blank entries individually and followed candidate links from directories and bibliographies.
The [search review](turing_scholar_search_2026-09-16.csv) records all entries and supersedes the unresolved Stonebraker directory lead above: its Scholar link belongs to Samuel Madden.
No verified addition resulted; some live verification was limited by Scholar HTTP 429 responses, and old indexed content was not accepted as a fresh capture.
See the latest [data notes](data_notes.md) for candidate details and retained search evidence.

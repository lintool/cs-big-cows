# Check Profiles: First 100 Fellows Trial

Reviewed the first 100 data rows of `data/acm_fellows.csv`, from **Adar, Eytan** through **Kankanhalli, Mohan**, in their existing order: 71 Fellows from 2025 and 29 from 2024.
The [row audit](check_profiles_trial_100_2026-09-18.csv) contains 300 service assessments, one each for Scholar, DBLP and CSRankings per recipient.
All 100 have recorded outcomes; unresolved coverage is explicitly distinguished from a completed quality verification.
This trial does not review the remaining Fellows or Turing roster.

## Evidence and Limits

The user chose existing captures: ACM September 13, Scholar September 16–17, DBLP September 17 and CSRankings sources September 18, 2026.
Verified the retained HTML hashes for all 100 ACM, 100 DBLP and 95 linked Scholar captures before reviewing.
General web searches and ordinary public candidate-page inspection supplemented those captures; no bulk crawl or source refresh was run.
Availability findings for retained profiles refer to capture time, not live availability today.
No confirmed withdrawal or disappearance was established in this trial.

Every linked Scholar capture contains only 20 most-cited entries.
Reviewed all 20 titles for rows 1–30 and the expanded Arindam Banerjee and Michal Feldman cases; otherwise sampled positions 1, 2, 6, 10, 15 and 20.
Compared names, research areas, country/location, affiliation metadata and distinctive publications across services, with author/coauthor inspection in expanded cases.
The 20 records are a **lower bound**, not a total publication count.
Identity and the observed sample can be supported while recent work and broader bibliography coverage remain unresolved.
No Scholar rating or capture date changed merely because the first page was short.

DBLP sampling used six positions spread across the retained chronological sample, including recent and older work, with expanded inspection when titles, attribution or career chronology conflicted.
Expanded checks included all 65 Pei Cao records, the large older tail of Junfeng Yang’s bibliography, the oldest entries for Wolfgang Heidrich and Ke Yi, and all 15 Steve Crocker records.
Counts refer to bibliography records, including versions and other indexed publication types, not deduplicated research papers.

Checked all 75 existing CSRankings links against exact keys and original source fields in the September 18 faculty snapshot and the canonical profile table.
Searched the 25 missing associations in the cached faculty files, retained alias/name-change evidence and general web search.
No additional supported source key was established; this does not prove universal absence from CSRankings or withdrawal.
Local DBLP associations copied from the roster were not counted as independent corroboration.

## Results

| Service | Outcome Across 100 Fellows |
| --- | --- |
| Google Scholar | 95 supported identities; 94 retain `Y` with sampled-quality support and broader coverage unresolved; Arindam Banerjee retains the explicit user `N`; five missing links remain `N`. |
| DBLP | 97 supported quality assessments, including one accepted replacement; two contaminated bibliographies rated `N`; one user-accepted coverage exception retains `Y`. |
| CSRankings | 75 supported name associations revalidated; 25 missing links remain blank; no new key accepted. |

These categories are service assessments, not mutually exclusive groups of people.
The stored DBLP flags after the trial are 98 `Y` and two `N`; the 98 includes Crocker’s explicitly accepted coverage exception.
The 75 CSRankings alignment dates already read `2026-09-18`, the UTC revalidation date, so revalidation causes no cell changes.

## Applied Corrections

| Fellow | Change | Evidence |
| --- | --- | --- |
| Cao, Pei | DBLP quality `Y` → `N`; retain URL and September 17 date. | The 65-record capture combines caching/networking work with sustained gear-fault, protein-kinase, finite-element, switchgear and genomic clusters. The [DBLP page](https://dblp.org/pid/87/3674.html) identifies a disambiguation bibliography; the [recipient’s Wisconsin page](https://pages.cs.wisc.edu/~cao/cao.html) corroborates the systems career. No cleaner matching bibliography was established. |
| Yang, Junfeng | DBLP quality `Y` → `N`; retain URL and September 17 date. | Persistent classroom/education, electrical-power and mathematical-optimization clusters coexist with Columbia systems work. The [DBLP page](https://dblp.org/pid/71/3724.html) explicitly identifies a disambiguation bibliography; [Columbia’s recipient page](https://www.cs.columbia.edu/~junfeng/) corroborates the software/AI-systems identity. No cleaner matching bibliography was established. |
| Fu, Yun Raymond | Replace `https://dblp.org/pid/153/2294` with `https://dblp.org/pid/00/5815-1`; quality `N` → `Y`. Synchronize `Yun Fu 0001` in the CSRankings profile table. | The old capture has three records from 2014. Direct browser inspection of [Yun Fu 0001](https://dblp.org/pid/00/5815-1.html) showed 659 records spanning 2006–2026, Northeastern affiliation and UIUC PhD history. Recent, intermediate and older vision/representation-learning titles and early Thomas S. Huang/Guodong Guo coauthors agree with Scholar and [Northeastern’s profile](https://coe.northeastern.edu/people/fu-raymond/). |

Fu’s replacement was inspected through the public browser after the web tool timed out.
The candidate sample included recent trajectory prediction and multimodal work, intermediate clustering and low-rank representation work, and older face/age estimation and the 2008 UIUC thesis.
This is a sampled quality judgment, not inspection of all 659 records.
The previous URL’s crawl date was cleared: no successful crawler capture of the replacement was accepted, so its date remains blank rather than carrying forward September 17 or substituting the review date.
The CSRankings table’s synchronization date remains September 18; its original upstream fields and every other row are unchanged.

## Review Queue and Source Conflicts

| Case | Finding and Disposition |
| --- | --- |
| All 95 linked Scholar profiles | Broader and recent-work coverage is not established by the retained first pages. Preserve stored ratings; collect the expanded evidence on a future approved refresh. Arindam’s clear contamination is already sufficient for `N`. |
| Crocker, Stephen David — DBLP (Resolved) | Fifteen records support the Internet-protocol identity. The [IETF RFC bibliography](https://datatracker.ietf.org/doc/html/rfc1012) includes early work absent from the captured list. After reviewing the count and omissions, the user explicitly accepted `Y` on September 18. Retain the URL and September 17 capture date as a documented coverage exception; no verified fuller DBLP alternative was found. |
| Ma, Jian — CSRankings source Scholar ID | Source key `Jian Ma 0004`, CMU affiliation and homepage identify the Fellow, but `kDZcBhkAAAAJ` belongs to plant scientist Jian Feng Ma, as documented by the earlier [wrong-person correction](data_notes.md#2026-09-15-1627-edt---name-corrections-and-wrong-person-scholar-link-removal). Keep the roster’s independently accepted `nDw9v78AAAAJ`; preserve and flag the upstream source field. |
| Huang, Zi Helen; Müller, Peter; Feldman, Michal — CSRankings source Scholar IDs | Source IDs `PnBlwhgAAAAJ`, `iJ0qZckAAAAJ` and `IKjIhTwAAAAJ` differ from accepted roster IDs `iAWMsgEAAAAJ`, `ttxZRHEAAAAJ` and `VpLQu7oAAAAJ`. Earlier profile corrections and matching institutional/research evidence support the name associations. Preserve source fields and flag the conflicts; do not infer withdrawal from a stale identifier. |
| Bonifati, Angela — location | ACM lists Italy while retained Scholar/DBLP metadata identifies Lyon, France. Identity and database research converge. Preserve ACM; the location discrepancy does not establish an obvious source error. |
| Chen, Deming; Feldman, Michal — Scholar | Isolated handbook attribution and Stone Age plague entries respectively merit publication-level notes. They do not establish substantial contamination in the captured sample; preserve `Y`. |
| Heidrich, Wolfgang; Yi, Ke — DBLP | Isolated oldest finance/cybernetics and constrained-robot entries conflict with the surrounding careers. Preserve `Y` under the user’s isolated-error policy; no substantial cluster was established. |

Different affiliations were treated as dated evidence rather than automatic identity failures.
For example, primary sources confirm [Kohno’s 2025 Washington-to-Georgetown move](https://college.georgetown.edu/news-story/yoshi-kohno-mcdevitt-chair-computer-science/) and [Orso’s Georgia Tech-to-UGA move](https://www.computing.uga.edu/directory/people/alessandro-alex-orso).
`NOSCHOLARPAGE` values were ignored as identity evidence.
The two cached Wei Chen candidates were rejected: the Fellow is Microsoft Research Asia’s influence-maximization researcher, DBLP `Wei Chen 0013`, rather than the Zhejiang `0001` or Peking `0021` source entries.

The five missing Scholar links remain Eric Allman, Nandita Dukkipati, Athina Markopoulou, Stephen David Crocker and Russell Housley.
General searches, including name variants and institutional leads, did not establish a sufficiently supported exact profile URL.
Arindam Banerjee’s general search and Illinois homepage did not establish a cleaner Scholar alternative.
Missing-link search outcomes describe this search, not proof that no public profile exists.

## Process Decisions From the Trial

The user adopted both recommendations surfaced during the trial:

- On future approved Scholar refreshes, collect a larger most-cited page plus a recent-publications page before judging overall quality, expanding further when concerns arise.
- Preserve original CSRankings source fields and flag bad upstream identifiers; do not add reviewed override columns.

Updated the [skill](../skills/check-profiles/SKILL.md) accordingly.
The user subsequently resolved Crocker’s coverage question with “seems okay, Y.”
His DBLP review is closed as an explicitly accepted coverage exception, without changing its URL, rating or capture date.

## Validation and Retained Evidence

Retained input snapshots, source hashes, evidence packets, search results, field-level changes, authoring inputs and validation under `../bigcows-crawler/.cache/check-profiles-trial-100-2026-09-18/`.
The CSV audit links original URLs and capture paths; Fu’s candidate-page inspection is documented above separately from the old captured fragment.
Verified six canonical cell changes: five in three Fellows rows and one dependent CSRankings DBLP cell.
Award names, years, citations, ACM links, row order, Scholar fields and dates are preserved.
The Turing CSV, Scholar metrics CSV and both visualization datasets are byte-for-byte unchanged.
All 829 CSRankings table keys still exactly equal the union of both rosters’ populated keys, with no duplicates or unreferenced rows.
Adjusted the existing date validation to permit a linked URL without an accepted crawl date, matching the already documented capture-date rule; populated dates and shared-profile consistency remain checked.
All 12 targeted roster/citation tests and the skill validator pass.

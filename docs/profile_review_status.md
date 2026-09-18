# Current Profile Review Status

This is the current progress and open-work index for the September 18, 2026 review.
The [detailed report](check_profiles_full_2026-09-18.md) retains historical observations and the 18 explicit user dispositions.
The full roster review is incomplete; recorded initial inspection is not equivalent to a completed service audit or a fresh capture.
No new crawl or source refresh is authorized by maintaining this index.
The lookup table now preserves [CSRankings-generated DBLP links](../README_FOR_AGENTS.md#csrankings-dblp-link-generation), independently of reviewed award links.
Historical audits and saved resume scripts used roster-derived lookup URLs; update any such writer to regenerate from source names before applying another checkpoint.
Do not restore their old DBLP cells or blank exceptions, and do not treat their agreement with award URLs as independent corroboration.

## Progress

| Work | Current State | Next Step |
| --- | --- | --- |
| Fellows 1–100 | Trial audit recorded for 100 recipients and 300 services | Preserve the [trial outcomes and evidence limits](check_profiles_trial_100_2026-09-18.md). |
| Fellows 101–1,300 | Initial individual inspection notes saved for 1,200 recipients | Finish the service audit and remaining follow-ups. |
| Fellows 1,301–1,638 | 338 recipients lack a saved completed initial inspection | Continue the remaining review; preliminary sampling is not counted as completed. |
| Turing Award roster | All 81 rows have 243 service outcomes; all presented profile decisions and Hopcroft's historical CSRankings link are applied | Capture accepted replacement links; broader Scholar coverage remains unverified. |
| Explicit user dispositions | The earlier 18 cases, three DBLP quality decisions and five further profile decisions are resolved and applied | Preserve the [earlier decisions](check_profiles_full_2026-09-18.md#explicit-user-decisions) and all [subsequent Turing decisions](check_profiles_turing_2026-09-18.md#subsequent-user-decisions), including the rejected Manuel Blum Scholar ID. |
| Rob Cook DBLP candidate | Candidate inspection saved, but its proposed replacement is not applied | Reconcile the saved proposal when resuming profile review; this documentation cleanup does not change the roster. |
| Final service audit | The full 5,157-assessment audit is not assembled | Distinguish recorded trial outcomes, initial inspection, unresolved evidence and unreviewed rows. |
| Visualization | Regeneration remains deferred | Regenerate only when requested. |

The saved notes extend through Fellow 1,300, although the last bulk CSV checkpoint was through Fellow 1,285 before the subsequent user dispositions.
These are different milestones; the earlier checkpoint totals are historical.
Rob Cook's saved proposal is [c/RobertLCook](https://dblp.org/pid/c/RobertLCook), with 14 inspected records and a documented contextual coverage rationale.
It remains a proposal, not an accepted CSV value or imported capture.

## Capture and Import Backlog

The [machine-readable queue](profile_capture_queue.json) contains 89 distinct accepted service URLs: 84 DBLP links without accepted capture dates and five Scholar links without accepted captures or statistics imports.
All except J. H. Wilkinson's DBLP task refer to Fellows; Richard Karp, David Patterson and Jim Gray's DBLP tasks are shared with their Turing rows.
The five Scholar recipients are Paola Inverardi, David Abramson, Lawrence Paulson, Richard DeMillo and Vishwani Agrawal.
Blank dates are intentional pending an accepted capture; quality approval alone does not import metrics.
The queue is ready for a separately approved targeted refresh and contains no unadopted discovery candidates.
Equivalent DBLP URL spellings share one task; each recipient entry preserves its exact roster URL in `stored_url`.
Use the [queue-generation workflow](../README_FOR_AGENTS.md#capture-and-import-backlog) after relevant CSV updates, then update these counts.

## Resolved Unavailable Scholar Candidates

The user instructed removal of all failed Scholar candidates on September 18 at 16:01 EDT.
The 13 discovery cases below and the historical candidates for Herbert Simon, Edsger Dijkstra and John McCarthy are resolved: their award-roster links and dates remain blank with quality `N`.
All 19 affected award rows (16 Fellows and three Turing rows) already had those values, and none of the failed IDs occurs in the canonical Scholar statistics table, so no CSV edits were needed.
The links below are retained as historical evidence, not an active review queue or accepted associations.
Victor Vianu's original CSRankings `scholarid` remains untouched under the user's source-preservation policy.
The observations were made on September 18 and do not establish intentional withdrawal.
Do not restore an association from search-index text or treat retained evidence as proof of current availability.

| Person | Candidate | Recorded Finding |
| --- | --- | --- |
| Elena Ferrari | [kOc4beIAAAAJ](https://scholar.google.com/citations?user=kOc4beIAAAAJ) | Visible 404. |
| Steven Hand | [QE17xR4AAAAJ](https://scholar.google.com/citations?user=QE17xR4AAAAJ) | Redirected to unrelated Steven Hansen, despite historical search-index text for Hand. |
| Ramanathan Guha | [wMxEtKgAAAAJ](https://scholar.google.com/citations?user=wMxEtKgAAAAJ) | Visible 404. |
| Gaetano Borriello | [wUS-iRsAAAAJ](https://scholar.google.com/citations?user=wUS-iRsAAAAJ) | Visible 404. |
| Jeffrey Dean | [NMS69lQAAAAJ](https://scholar.google.com/citations?user=NMS69lQAAAAJ) | Visible 404. |
| Laurie Hendren | [uouHKIkAAAAJ](https://scholar.google.com/citations?user=uouHKIkAAAAJ) | Visible 404; the alternative 14-paper McLAB profile was rejected for inadequate coverage. |
| Chandramohan Thekkath | [B_uwswQAAAAJ](https://scholar.google.com/citations?user=B_uwswQAAAAJ) | Visible 404. |
| Guang Gao | [KYj0CvEAAAAJ](https://scholar.google.com/citations?user=KYj0CvEAAAAJ) | Visible 404. |
| Peter Norvig | [Ol0vcWgAAAAJ](https://scholar.google.com/citations?user=Ol0vcWgAAAAJ) | Visible 404. |
| Victor Vianu | [CK_GLC8AAAAJ](https://scholar.google.com/citations?user=CK_GLC8AAAAJ) | Visible 404. |
| Michael D. Schroeder | [mPzCK6EAAAAJ](https://scholar.google.com/citations?user=mPzCK6EAAAAJ) | Visible 404. |
| Richard Schlichting | [K2We_X0AAAAJ](https://scholar.google.com/citations?user=K2We_X0AAAAJ) | Visible 404. |
| Ralf Steinmetz | [S8m0ZkkAAAAJ](https://scholar.google.com/citations?user=S8m0ZkkAAAAJ) | Visible 404. |

Paola Inverardi is resolved and is not part of this availability list; her approved successor is in the capture/import queue.

## Resolved Historical CSRankings Source Gaps

All six associations below are now linked using original rows recovered from upstream commit `4b714f69c839ca538825054f94bdf57f5d4ea3da` of December 30, 2020.
The [recovery report](csrankings_historical_recovery_2026-09-18.md) records the exact source values, identity evidence, historical scope and applied changes.
The historical source predates ORCID; that unavailable field is explicitly represented as blank, and the four actual source values remain unmodified.
The following links retain the initial discovery leads; these cases no longer await source recovery.

| Person | Candidate Key | Existing Lead |
| --- | --- | --- |
| Peter Bartlett | Peter L. Bartlett | [Public historical mirror](https://csrankings.swag.cispa.de/). |
| Larry Davis | Larry S. Davis | [Historical CSRankings-related study](https://leonidk.com/pdfs/jcdl2019.pdf). |
| Joseph Hellerstein | Joseph M. Hellerstein | [Public historical mirror](https://csrankings.swag.cispa.de/). |
| Allan Gottlieb | Allan Gottlieb | [Historical source mirror](https://gitee.com/mirrors/CSrankings/blob/gh-pages/csrankings-a.csv). |
| Laxmi Bhuyan | Laxmi N. Bhuyan | [Institution-hosted 2019 printout](https://vsclab.engr.ucr.edu/media/261/download?attachment=). |
| John Hopcroft | John E. Hopcroft | [Public historical mirror](https://csrankings.swag.cispa.de/), identified during the [Turing sweep](check_profiles_turing_2026-09-18.md). |

Together with Donald Greenberg, Georg Gottlob, Judith S. Olson, Luca Cardelli and Ruby B. Lee, these make 11 accepted historical keys within the 835-row canonical lookup table.
The accepted historical fields are protected by the [source-field manifest](csrankings_source_fields.json).

## Evidence and Resume Point

The retained run is `../bigcows-crawler/.cache/check-profiles-full-2026-09-18/`.
It contains the input snapshots, `queue.json`, `inspection-notes-1286-1300.json`, `candidate-decisions-1286-1300.json`, earlier batch notes and `user-dispositions-2026-09-18.json`.
The public status index consolidates that progress without claiming the unfinished notes constitute a final audit.
The separate completed Turing audit and discovery follow-ups are retained in `../bigcows-crawler/.cache/check-profiles-turing-2026-09-18/` and summarized in the [Turing report](check_profiles_turing_2026-09-18.md).
On resumption, reconcile the saved Cook proposal, continue at Fellow 1,301, finish earlier Fellow follow-ups, and combine the completed Turing outcomes with the eventual full audit.
Preserve the explicit user dispositions, original CSRankings source fields, finalized ACM award data and deferred visualization snapshots.

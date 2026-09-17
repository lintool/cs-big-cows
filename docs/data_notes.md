# Data Notes

Entries are ordered newest first, including the order of work completed on the same date.
Timed headings use the work's completion time in `America/Toronto`, formatted as `YYYY-MM-DD HH:mm EDT` or `YYYY-MM-DD HH:mm EST` as applicable.
Historical entries retain date-only headings where a reliable completion time is unavailable.
Filesystem paths are relative to the repository root unless stated otherwise.

Each entry is a historical snapshot: counts, blank cells, and pending decisions describe the end of that batch unless stated otherwise.
Later entries supersede earlier decisions without erasing the original evidence or rationale.
Scholar entries concern `data/acm_fellows.csv` unless they explicitly name the Turing Award dataset.
Blank Scholar cells refer to `google_scholar_profile`; blank ACM profile cells refer to `acm_fellow_profile`.
A recorded Scholar URL alone does not establish current profile availability or validate every publication and citation metric.
Scholar links labeled as cached evidence identify the source profile URLs; the historical captures are in the local cache files named in the entry.

Start with the completed [Fellows statistics import](#2026-09-16-2121-edt---import-all-reviewed-fresh-acm-scholar-statistics) and [Turing refresh](#2026-09-16-2213-edt---refresh-turing-award-google-scholar-profiles), followed by the [combined visualization update](#2026-09-16-2238-edt---separate-fellows-and-turing-citation-visualizations).
These entries supersede earlier pending-import and historical-fallback statements.
For current file locations, display behavior, and maintenance commands, use the [visualization reference](../README_FOR_AGENTS.md#google-scholar-citation-visualization).
Paths in older entries describe the layout at that time and are retained as provenance.

Selected entries and reports:

- **Latest completed data updates:** [Fellows import](#2026-09-16-2121-edt---import-all-reviewed-fresh-acm-scholar-statistics), [Turing refresh](#2026-09-16-2213-edt---refresh-turing-award-google-scholar-profiles), and [both visualization datasets](#2026-09-16-2238-edt---separate-fellows-and-turing-citation-visualizations).
- **Fresh identity audits:** [Fellows report](acm_scholar_audit_2026-09-16.md) and [Turing report](turing_scholar_audit_2026-09-16.md), including publication-attribution concerns and links to row-level evidence.
- **Missing-profile searches:** [Turing follow-up](#2026-09-16-2219-edt---follow-up-missing-turing-scholar-profiles-with-general-web-search) and [remaining Fellows search outcomes](#2026-09-15-1349-edt---google-scholar-links-review-of-all-remaining-missing-entries).
- **Shared recipients:** [Fellows-to-Turing synchronization](#2026-09-16-2200-edt---synchronize-shared-turing-recipients-from-acm-fellows) and [earlier user resolutions](#2026-09-15-1821-edt---user-resolution-of-shared-recipient-scholar-links).
- **Rejected links and historical statistics:** [Broken-link resolution](#2026-09-16-2044-edt---resolve-45-broken-acm-fellow-scholar-links) and [historical-record removal](#2026-09-16-2049-edt---remove-unverified-historical-scholar-records).
- **Canonical ordering:** [Award CSV sorting decision](#2026-09-15-1822-edt---consistent-award-csv-sort-order).
- **ACM source reconciliation:** [Turing Award crawl](#2026-09-13---turing-award-reconciliation-and-profile-crawl) and [Fellows crawl](#2026-09-13---acm-fellows-profile-crawl-review).

## 2026-09-16 22:38 EDT - Separate Fellows and Turing Citation Visualizations

Added a dedicated Turing Award citation timeline alongside the existing Fellows page, with navigation between the two and shared rendering and styles.
Regenerated both JavaScript data snapshots from the current canonical CSVs: Fellows contains 1,638 recipients, 1,250 with Scholar histories and 388 missing; Turing contains 81 recipients, 40 with histories and 41 missing.
The shared statistics store contains 1,260 unique profiles, including the 30 shared by these award rosters.
Both pages now reflect the reviewed fresh crawls and the Turing profile corrections recorded below.
Canonical CSVs were not changed by this visualization work.

Validated award-specific generator defaults, every generated row against the current CSVs, missing-data handling, search and toggle behavior, empty results, dataset mismatch errors, dynamic year ranges, and local asset references.
Local-file browser preview was blocked by the browser tool's URL policy; visual inspection remains unverified.

## 2026-09-16 22:19 EDT - Follow Up Missing Turing Scholar Profiles with General Web Search

Ran individual general web searches for all 41 blank Turing Scholar entries, followed by 21 additional name-variant and candidate-ID searches and targeted source-page checks.
The [41-row search review](turing_scholar_search_2026-09-16.csv) records the queries and outcomes.
No additional profile was verified, so canonical datasets and visualization files remain unchanged.

Resolved Michael Stonebraker's Research.com link to Samuel Madden's existing profile (`a1ngrCIAAAAJ`), and rejected a Silvio Micali directory link assigned to Phillip Rogaway in CSRankings (`gUEkPQEAAAAJ`).
Dijkstra's Research.com link (`g875mLgAAAAJ`) remains unverified: this web check was rate-limited with HTTP 429, and the historical local capture returned 404.
John McCarthy's DBLP link (`SuVID2wAAAAJ`) yielded old indexed content through web search, but the fresh September 16 capture returned 404, so it was not restored.
Herbert Simon's rediscovered historical IDs remain unavailable according to the completed fresh crawl.
Scholar rate limiting and source-page access failures limit verification; a blank field does not establish that no profile exists.
Search results, fetched source pages, and review metadata are retained under `../bigcows-crawler/.cache/turing-scholar-web-followup-2026-09-16/`.

## 2026-09-16 22:13 EDT - Refresh Turing Award Google Scholar Profiles

Searched the web for all 39 Turing recipients with blank Scholar fields, then freshly fetched all 42 existing profile URLs and two historical Herbert A. Simon candidates at the agreed 5–7 second pace with a 120–150 second pause after 25 requests.
All existing URLs returned HTTP 200; both Simon candidates returned HTTP 404.
Identity review retained 40 profiles and cleared two wrong-person links: E. Allen Emerson pointed to Eric Emerson, and Kenneth E. Iverson pointed to Kenneth R. Iversen.
No missing or replacement profile was sufficiently verified, leaving 41 blank Scholar fields across the 81 recipients.

Imported fresh statistics for every retained profile into `data/google_scholar_profiles.csv`, replacing 36 records and adding four for Charles H. Bennett, Gilles Brassard, Andrew Barto, and Richard Sutton.
Removed both wrong-person statistics records, which were unreferenced by either award roster, leaving 1,260 unique shared metrics records.
All imported Turing captures are dated September 17 UTC, corresponding to September 16 EDT; no historical statistics fallback was retained for rejected links.
The [review report](turing_scholar_audit_2026-09-16.md) and [81-row audit](turing_scholar_audit_2026-09-16.csv) record decisions, evidence, failed candidates, metadata limits, and publication-attribution concerns for David Patterson and Frederick Brooks.

Validated the import against the fresh cache, preserved non-Scholar Turing fields and the preceding Fellows synchronization, and retained canonical row ordering and LF line endings.
ACM Fellows and the other datasets remain unchanged, except for the shared Scholar statistics import.
The visualization and its `docs/scholar_data.js` snapshot remain unchanged pending a later requested update.
Local crawl, search, and review artifacts are retained in `../bigcows-crawler/.cache/turing-scholar-refresh-2026-09-16/`.

## 2026-09-16 22:00 EDT - Synchronize Shared Turing Recipients from ACM Fellows

At the user's direction, copied person-level information from the newer [ACM Fellows dataset](../data/acm_fellows.csv) into matching [Turing Award records](../data/turing_award_winners.csv).
Matched 63 of 81 recipients using unique identical ACM recipient URLs, DBLP URLs or exact names, consistent with the previously documented shared-recipient review.
The copied fields are `name`, `location`, `dblp_profile` and `google_scholar_profile`, including reviewed blank values.
Locations follow the Fellows dataset as requested; this synchronization does not independently re-verify residence or nationality.
Preserved Turing Award years, award citations and recipient URLs, and left the 18 unmatched recipients unchanged.
Allen Newell was not matched to the distinct Fellow Alan Newell.

Updated 15 cells across 14 recipients:

| Recipient | Fields Copied from ACM Fellows |
| --- | --- |
| Avi Wigderson | Added DBLP profile `https://dblp.org/pid/w/AviWigderson`. |
| Shafi Goldwasser | Location: USA to Israel. |
| Charles P. Thacker | Name: Charles P Thacker to Charles P. Thacker. |
| Alan Kay | Location: USA to United Kingdom. |
| A J Milner | Added DBLP profile `https://dblp.org/pid/m/RobinMilner`. |
| Fernando Corbato | Name: Fernando J Corbato to Fernando Corbato. |
| Niklaus E. Wirth | Name: Niklaus E Wirth to Niklaus E. Wirth. |
| Kenneth Lane Thompson | Added DBLP profile `https://dblp.org/pid/t/KenThompson`. |
| Stephen A Cook | Location: USA to Canada. |
| Edgar F. Codd | Name: Edgar F Codd to Edgar F. Codd. |
| Herbert A. Simon | Name: Herbert A Simon to Herbert A. Simon. |
| Edsger W. Dijkstra | Name: Edsger W Dijkstra to Edsger W. Dijkstra; location: Netherlands to USA. |
| John McCarthy | Cleared the rejected Scholar link `SuVID2wAAAAJ`, matching the Fellows review. |
| Richard W. Hamming | Name: Richard W Hamming to Richard W. Hamming. |

The Turing dataset now has 42 Scholar links and 39 blank Scholar fields.
Citation statistics are already stored in the shared `google_scholar_profiles.csv`; no duplicate statistics import was needed.
Verified all 63 matched recipients agree on the copied fields, all 81 award records remain present, award-specific values and unmatched rows are unchanged, names remain unique, and the CSV retains the required sort order and LF line endings.
The Fellows dataset, shared profile tables and visualization files are unchanged.
The local before/after comparison is in `tmp/turing-fellows-sync/`.

## 2026-09-16 21:21 EDT - Import All Reviewed Fresh ACM Scholar Statistics

Imported the complete 1,250-profile fresh, identity-reviewed export into `data/google_scholar_profiles.csv` and regenerated `docs/scholar_data.js`.
Verified every field of all 1,250 imported records against its successful full-HTML capture, including the capture hash from the per-Fellow audit.
Replaced 831 existing ACM-linked records with the reviewed export and added 419 previously absent records.
Removed 31 obsolete metrics records referenced by neither the current ACM Fellows nor Turing Award datasets.
Retained eight Turing-only records unchanged at their original April 30 crawl date because they were outside the ACM crawl; they are not used as fallback data for any ACM Fellow.
The canonical metrics CSV now has 1,258 unique rows: 1,250 fresh ACM profiles and eight historical Turing-only profiles.

The imported captures are dated September 16, 2026 for 1,222 profiles and September 17 UTC for 28 profiles captured during the September 16 Toronto evening.
Preserved actual crawl dates instead of replacing them with the import or generation timestamp.
The visualization now displays all 1,250 accepted profiles with fresh statistics, up from 820 in the preceding snapshot.
All 1,638 Fellows remain available, with the 388 blank Scholar fields represented as missing data and null metrics.
The reviewed wrong-person removals and accepted replacement links now feed the displayed data.
The 11 previously recorded publication-attribution concerns remain; imported values reflect Scholar’s reported totals without attempted paper-level corrections.

Verified all citation totals, h-index values, yearly counts and crawl dates in the generated JavaScript against the reviewed export.
Verified the ACM roster, Turing roster, other canonical CSVs, HTML and rendering script byte-for-byte unchanged.
Chrome loaded the page directly from disk and passed checks for fresh-profile counts, author search, accepted replacement links, cleared links and missing-data display, with no browser errors.
The full fresh ACM metrics import and visualization data refresh are complete; earlier pending-import statements in the audit and extraction entries are historical.
The [September 16 audit](acm_scholar_audit_2026-09-16.md) and its row CSV retain the audit-time metrics status as provenance.
Import details, the removed and retained record lists, backups and validation results are in `tmp/scholar-full-import-2026-09-16/`.

## 2026-09-16 21:09 EDT - Separate Scholar Visualization Data and Rendering

Extracted the visualization’s complete existing dataset into `docs/scholar_data.js`, exposed as `window.SCHOLAR_DATA`, and moved rendering code into `docs/scholar_visualization.js`.
The HTML loads these files as classic scripts so the page continues to work when opened directly from disk, without a backend or local server.
D3 still loads from its existing CDN URL.
The generator `scripts/build_scholar_citation_visualization.py` now writes only the JavaScript data file; it no longer regenerates presentation code.

Preserved all 1,638 previously embedded rows, their values, their order and the existing metadata counts: 820 rows with displayed Scholar data and 818 without it.
Added schema version 1, a generation timestamp, and per-record crawl dates recovered only when the snapshot’s citation total, h-index and yearly counts exactly matched a source CSV record.
All 820 displayed metric records match the April 30, 2026 capture date; the new generation timestamp does not imply fresh citation statistics.
This structural extraction does not import the newly reviewed crawl or update the displayed snapshot to the latest canonical CSVs.
The pending full metrics refresh remains a separate step.

Verified every canonical CSV byte-for-byte unchanged.
Checked generator output against the current CSVs in a scratch file, preserving missing values, zero counts, sorting and source crawl dates.
Verified JavaScript syntax and serialization, including Unicode, quotes and markup in source strings.
A Chrome check using local file URLs confirmed identical rendered output before and after extraction for default, missing-data, author-search and empty-result states, with no browser errors.
Also verified a visible error when the data file is missing.
Updated the [visualization maintenance reference](../README_FOR_AGENTS.md#google-scholar-citation-visualization) to document the separate files and data-only rebuild command.

## 2026-09-16 20:58 EDT - Full ACM Fellow Scholar Freshness and Identity Sweep

Audited all 1,638 Fellows, including all 1,255 starting Scholar links and the 383 blank fields.
All starting links had fresh successful September 16 captures, but the broader identity review found seven additional bad or mixed-person associations.
Replaced Satish Rao and Manish Gupta with newly fetched, identity-verified profiles; cleared Carla Gomes, Roy Levin, Prithviraj Banerjee, Robin Williams and Ahmed Sameh because no verified replacement was found.
Removed the five rejected associations present in the historical metrics CSV and added both fresh replacement records, leaving 870 canonical metrics rows.
The Fellows CSV now has 1,250 distinct linked profiles with fresh captures and supported identities, and 388 blank Scholar fields.
Recorded 11 publication-attribution concerns, including four checked against publication records, plus 24 DBLP identity-review candidates.
The complete 1,250-row fresh-only metrics export is in `tmp/scholar-full-sweep-2026-09-16/fresh-accepted-google_scholar_profiles.csv`; the full canonical metrics import remains pending.
See the [sweep report](acm_scholar_audit_2026-09-16.md) and [all-Fellows row audit](acm_scholar_audit_2026-09-16.csv) for findings, methods, coverage gaps and limitations.
No historical fallback was retained for any newly rejected association.
Preserved earlier manual decisions and verified all other canonical CSVs and the visualization unchanged.
Visualization regeneration remains deferred at the user’s instruction.

## 2026-09-16 20:49 EDT - Remove Unverified Historical Scholar Records

The user clarified that this ACM Fellows refresh must not retain historical Scholar records as a fallback when no fresh profile can be verified.
This supersedes the historical-record preservation policy in the preceding review entries.
Removed the historical Guang R. Gao and John McCarthy records from `data/google_scholar_profiles.csv` because their profiles returned HTTP 404 and no fresh replacement was verified.
Replaced the obsolete Andrew B. Kahng and Dinesh Manocha records with complete data from their verified replacement-profile captures, without copying historical metrics into the replacements.

| Fellow | Action | Profile |
| --- | --- | --- |
| Guang Gao | Removed; no verified fresh replacement | `https://scholar.google.com/citations?user=KYj0CvEAAAAJ` |
| John McCarthy | Removed; no verified fresh replacement | `https://scholar.google.com/citations?user=SuVID2wAAAAJ` |
| Andrew B. Kahng | Replaced with fresh capture dated 2026-09-17 UTC | [Scholar](https://scholar.google.com/citations?user=zQ9GU2EAAAAJ) |
| Dinesh Manocha | Replaced with fresh capture dated 2026-09-17 UTC | [Scholar](https://scholar.google.com/citations?user=Nqawxa0AAAAJ) |

The Scholar CSV now contains 873 rows.
All 871 unaffected records and their order are unchanged; profiles outside this fresh crawl were not classified as failed solely because they were not crawled.
No failed HTTP 404 profile from this fresh crawl remains in the active Scholar CSV.
The remaining full fresh-metrics import is still pending.
At the user’s explicit instruction, did not update `docs/scholar_citations.html`; its bytes and all other CSVs were verified unchanged.
Visualization regeneration is deferred until the end of the data work.

## 2026-09-16 20:44 EDT - Resolve 45 Broken ACM Fellow Scholar Links

Following the fresh-crawl review and the user’s decision to leave Laurie Hendren blank, searched the web for replacements for all 45 remaining HTTP 404 Scholar associations.
Replaced 23 links after live HTTP 200 checks and identity review, and cleared 22 cells where no usable replacement could be verified.
A cleared cell records an unresolved search outcome, not proof that the researcher has no Scholar profile.

| Fellow | Outcome | Evidence |
| --- | --- | --- |
| Yan Solihin | [Replacement profile](https://scholar.google.com/citations?user=sUQFclgAAAAJ) | [Source](https://adscientificindex.com/scientist/mnassar-alyami/6156736/): Coauthor link; live profile matches UCF, computer architecture/security, cache partitioning and Bonsai Merkle Tree papers. |
| Michal Feldman | [Replacement profile](https://scholar.google.com/citations?user=VpLQu7oAAAAJ) | [Source](https://www.mfeldman.sites.tau.ac.il/): Official homepage links this ID; live Tel Aviv profile and algorithmic game theory publications match. |
| Dana Ron | [Replacement profile](https://scholar.google.com/citations?user=f5vfsVkAAAAJ) | [Source](https://adscientificindex.com/scientist/moti-medina/437488/): Coauthor link; live Tel Aviv profile matches property testing and learning publications. |
| David Sankoff | [Replacement profile](https://scholar.google.com/citations?user=-4VIi-UAAAAJ) | [Source](https://adscientificindex.com/scientist/david-sankoff/641574/): Live Ottawa profile matches sequence comparison, genomics and applied probability. |
| Kilian Weinberger | [Replacement profile](https://scholar.google.com/citations?user=8RVWMycAAAAJ) | [Source](https://www.cs.cornell.edu/~kilian/): Official homepage links this ID; live Cornell profile matches machine learning, DenseNet and metric learning. |
| Vineet Bafna | [Replacement profile](https://scholar.google.com/citations?user=zr2I_WMAAAAJ) | [Source](https://scholar.google.com/citations?user=rfS5yTMAAAAJ): Linked from the newly verified Pavel Pevzner profile; live UCSD profile matches bioinformatics and cancer genomics. |
| Alfons Kemper | [Replacement profile](https://scholar.google.com/citations?user=B8TzQFQAAAAJ) | [Source](https://adscientificindex.com/scientist/viktor-leis/1757880/): Coauthor link; live TUM profile matches HyPer and database systems publications. |
| David M Mount | Blank | [Source](https://www.cs.umd.edu/~mount/): Official UMD pages still link the old 404 ID; no verified replacement found. |
| Hong Mei | Blank | [Source](https://faculty.pku.edu.cn/meih/en/index.htm): Peking University page and general web search yielded no verified replacement; Research.com still links the old 404 ID. |
| Yuguang Fang | [Replacement profile](https://scholar.google.com/citations?user=cs45mqMAAAAJ) | [Source](https://www.cs.cityu.edu.hk/~yugufang/): Official homepage links this ID; live CityU profile matches wireless networks and IoT. |
| Glenn Ricart | Blank | [Source](https://en.wikipedia.org/wiki/Glenn_Ricart): General web and bibliography searches found no verified replacement; a Scholar publication-search link is not an author profile. |
| Paola Inverardi | Blank | [Source](https://sisma2016.gov.it/wp-content/uploads/2021/05/CV-Inverardi.pdf): The alternate CV spelling x8XIRFgAAAAJ also returned HTTP 404; other leads did not establish a usable replacement. |
| Ranjit Jhala | [Replacement profile](https://scholar.google.com/citations?user=lh6orZ0AAAAJ) | [Source](https://adscientificindex.com/scientist/ravi-chugh/1850740/): Coauthor link; live UC San Diego profile matches lazy abstraction, BLAST and software verification publications. |
| Rosalind Wright Picard | [Replacement profile](https://scholar.google.com/citations?user=hH3DA2YAAAAJ) | [Source](https://adscientificindex.com/scientist/rosalind-picard/5275111/): Live MIT Media Lab profile matches affective computing and physiological sensing publications. |
| Tajana Rosing | [Replacement profile](https://scholar.google.com/citations?user=DY_XcO4AAAAJ) | [Source](https://adscientificindex.com/scientist/raid-ayoub/1875230/): Coauthor link; live UCSD profile matches computer architecture, embedded systems and energy efficiency. |
| Wei Wang | [Replacement profile](https://scholar.google.com/citations?user=08CVzE8AAAAJ) | [Source](https://scholar.google.com/citations?user=Q1mcglAAAAAJ): Haixun Wang coauthor link; live profile explicitly identifies UCLA's Leonard Kleinrock Professor and matches data mining. Rejected the ByteDance namesake 46Dd4v4AAAAJ. |
| Salvatore J Stolfo | [Replacement profile](https://scholar.google.com/citations?user=iLXSMP8AAAAJ) | [Source](https://www.newx.sg/scholar/iLXSMP8AAAAJ): Web source and Angelos Keromytis coauthor link; live Columbia profile matches intrusion detection and security publications. |
| Mario Gerla | Blank | [Source](https://dblp.org/pid/g/MarioGerla): General web and DBLP searches returned the old 404 Mario Gerla ID or unrelated namesakes; no verified replacement found. |
| Vishal Misra | [Replacement profile](https://scholar.google.com/citations?user=IlCfRosAAAAJ) | [Source](https://scholar.google.com/citations?user=mncyWbcAAAAJ): Angelos Keromytis coauthor link; live networking profile matches TCP/AQM, RED and SOS publications. |
| Daniel Jackson | Blank | [Source](https://www.csail.mit.edu/person/daniel-jackson): MIT identity confirmed; sources still link old PXY96lkAAAAJ. The earlier XYMFjxcAAAAJ candidate belongs to a Newcastle/Northumbria namesake. Another directory lead could not be retrieved; no live replacement verified. |
| Cynthia Dwork | Blank | [Source](https://research.com/u/cynthia-dwork): Alternative pxeyQ_QAAAAJ also returned HTTP 404; other directory source still links old y2H5xmkAAAAJ. |
| Nir N Shavit | Blank | [Source](https://shavitlab.csail.mit.edu/publications.html): Official lab publications page still links old f1NaDVgAAAAJ; no verified replacement found. |
| Yuanyuan Zhou | [Replacement profile](https://scholar.google.com/citations?user=jJ_9TvEAAAAJ) | [Source](https://scholar.google.com/citations?user=JHwivywAAAAJ): Pei Cao coauthor link; live UCSD computer science profile matches systems reliability. Rejected the HKUST materials-science namesake found by web search. |
| Andrew B. Kahng | [Replacement profile](https://scholar.google.com/citations?user=zQ9GU2EAAAAJ) | [Source](https://jacobsschool.ucsd.edu/people/profile/andrew-b-kahng): Official UCSD faculty page links this ID; live profile matches VLSI, EDA and physical design. |
| Dean Tullsen | [Replacement profile](https://scholar.google.com/citations?user=h8wSTmMAAAAJ) | [Source](https://adscientificindex.com/scientist/parthasarathy-ranganathan/4378560/): Coauthor link; live UCSD profile matches simultaneous multithreading, McPAT and computer architecture. |
| Pavel Pevzner | [Replacement profile](https://scholar.google.com/citations?user=rfS5yTMAAAAJ) | [Source](https://scholar.google.com/citations?user=ri4rEPMAAAAJ): Ron Shamir coauthor link; live UCSD profile matches SPAdes, genome assembly and bioinformatics. |
| Chandramohan A Thekkath | Blank | [Source](https://research.com/u/chandramohan-a-thekkath): General web search and research directory still point to old B_uwswQAAAAJ; no verified replacement found. |
| Dinesh Manocha | [Replacement profile](https://scholar.google.com/citations?user=Nqawxa0AAAAJ) | [Source](https://www.cs.umd.edu/people/dmanocha): Official UMD CS page links this ID; live profile matches robotics, collision detection and graphics. |
| Gaetano Borriello | Blank | [Source](https://research.com/u/gaetano-borriello): General web, Wikipedia and research directory still point to old wUS-iRsAAAAJ; no verified replacement found. |
| Jeffrey A Dean | Blank | [Source](https://www.adscientificindex.com/scientist/jeff-dean/4375582): General web, Wikidata and research directory still point to old NMS69lQAAAAJ; no verified replacement found. |
| Shang-Hua Teng | [Replacement profile](https://scholar.google.com/citations?user=JknkZcQAAAAJ) | [Source](https://scholar.google.com/citations?user=APiItS4AAAAJ): Rob Schreiber coauthor link; live USC profile matches smoothed analysis, spectral sparsification and algorithms. |
| Jitendra Malik | [Replacement profile](https://scholar.google.com/citations?user=aOklxsQAAAAJ) | [Source](https://www.adscientificindex.com/scientist/jitendra-malik/1734828): Live Berkeley EECS profile matches computer vision, normalized cuts and visual recognition publications. |
| Lawrence C Paulson | Blank | [Source](https://research.com/u/lawrence-paulson): General web, Wikipedia and research directory still point to old Sv1hcjEAAAAJ; no verified replacement found. |
| Perry Cook | Blank | [Source](https://www.cs.princeton.edu/~prc/): Princeton homepage has no replacement profile link; research directory still points to old ajVR5gEAAAAJ. |
| Guang Gao | Blank | [Source](https://research.com/u/guang-r-gao): Research directory identifies the Delaware computer scientist but still points to old KYj0CvEAAAAJ; unrelated Guang/Guangwei Gao results rejected. |
| Victor Vianu | Blank | [Source](https://research.com/u/victor-vianu): General web, Wikipedia and research directory still point to old CK_GLC8AAAAJ; no verified replacement found. |
| Michael D Schroeder | Blank | [Source](https://adscientificindex.com/scientist/michael-d-schroeder/4387442/): Correct-person directory still links old mPzCK6EAAAAJ; German bioinformatics and other namesakes rejected. |
| Ralf Steinmetz | Blank | [Source](https://research.com/u/ralf-steinmetz): Research directory and author bibliography still link old S8m0ZkkAAAAJ; additional coauthor directory leads could not be retrieved, so no replacement verified. |
| Takeo Kanade | [Replacement profile](https://scholar.google.com/citations?user=askFPfcAAAAJ) | [Source](https://adscientificindex.com/scientist/laszlo-a-jeni/895439/): Coauthor link; live CMU profile matches Lucas-Kanade image registration, face detection and computer vision. |
| Lori Clarke | Blank | [Source](https://adscientificindex.com/scientist/lori-clarke/1289549/): Both research directories still link old oFiuaXEAAAAJ; no verified replacement found. |
| Vaughan Ronald Pratt | Blank | [Source](https://en.wikipedia.org/wiki/Vaughan_Pratt): General web and biography sources still point to old Zc7l_LcAAAAJ; no verified replacement found. |
| Anthony I Wasserman | Blank | [Source](https://www.csauthors.net/anthony-i-wasserman/): Correct-person bibliography still links old 08Dlm8cAAAAJ; general web search yielded no verified replacement. |
| Grady Booch | Blank | [Source](https://www.csauthors.net/grady-booch/): Correct-person bibliography still links old Y0iLlFoAAAAJ; general web search yielded no verified replacement. |
| John McCarthy | Blank | [Source](https://www-formal.stanford.edu/jmc/biography.html): Stanford identity confirmed; general web and bibliography searches did not establish a live replacement for old SuVID2wAAAAJ. |
| Peter J Denning | [Replacement profile](https://scholar.google.com/citations?user=-W3wvGkAAAAJ) | [Source](https://scholar.google.com/citations?user=23RPQBQAAAAJ): Walter Tichy coauthor link; live Naval Postgraduate School profile matches the working-set model and operating systems. |

Rejected the ByteDance Wei Wang namesake, the HKUST materials-science Yuanyuan Zhou namesake, and unavailable alternative IDs for Paola Inverardi and Cynthia Dwork.
The earlier wrong-person Daniel Jackson candidate remains rejected.
Preserved all earlier manual decisions, including Laurie Hendren’s blank field and the accepted Peter Müller and James H. Morris profiles.
No citation metrics were imported or re-dated; the existing Scholar metrics CSV and original crawl caches remain unchanged.
Historical metrics for Andrew B. Kahng, Dinesh Manocha, Guang Gao, and John McCarthy remain stored under their original profile IDs and historical crawl dates.
Updated only the 45 affected embedded visualization records and derived counts, preserving unrelated local changes.
Validated exactly 45 Scholar-cell changes, stable row order, LF line endings, unique nonblank URLs, and unchanged other CSVs.
The Fellows CSV retains 1,638 rows, with 1,255 nonblank Scholar URLs and 383 blanks.
Detailed decisions, source captures, candidate HTML, backups and validation results are retained under `tmp/scholar-45-resolution/`.

## 2026-09-16 20:28 EDT - User Resolution of Hendren and Morris Scholar Profiles

The user directed that Laurie Hendren’s Scholar field remain blank and confirmed James H. Morris’s corrected profile.
Cleared Laurie J Hendren’s existing broken `uouHKIkAAAAJ` link in `data/acm_fellows.csv`; did not adopt the sparse `e557wtEAAAAJ` candidate.
Retained James H Morris’s [confirmed Scholar profile](https://scholar.google.com/citations?user=9Y2cn3EAAAAJ).
The user also confirmed Peter Müller’s [ETH Zurich profile](https://scholar.google.com/citations?user=ttxZRHEAAAAJ) earlier in this review; retained that correction.
These decisions supersede the preceding pending profile-choice recommendations.
No citation metrics were imported or changed.
Updated Laurie Hendren’s embedded visualization record, preserving all other local changes.
Validated exactly one CSV cell change, with all 1,638 Fellow rows retained; 1,277 Scholar links remain and 361 fields are blank.

## 2026-09-16 20:14 EDT - Correct Seven Wrong-Person Scholar Links

At the user’s request, performed general web searches for the seven wrong-person associations identified in the fresh-crawl review.
Replaced three URLs after confirming the researcher’s identity and cleared the other four Scholar cells because no correct profile could be verified.
Clearing means unresolved in this search, not proof that no profile exists.

| Fellow | Outcome | Evidence |
| --- | --- | --- |
| Peter Müller | Replaced with [Scholar](https://scholar.google.com/citations?user=ttxZRHEAAAAJ) | [Source](https://research.com/u/peter-muller): Profile fetched successfully: ETH Zurich; program verification, formal methods; Viper and JML publications. Also linked as a coauthor in David Basin’s fresh capture. |
| Zi Helen Huang | Replaced with [Scholar](https://scholar.google.com/citations?user=iAWMsgEAAAAJ) | [Source](https://about.uq.edu.au/experts/1230): Official UQ page links this exact ID; fetched profile identifies Zi (Helen) Huang, University of Queensland, with multimedia/search/database publications. |
| Nisheeth Vishnoi | Cleared | [Source](https://cs.yale.edu/homes/vishnoi/Home.html): General web searches, Yale faculty/personal pages, DBLP, and an ApplyKite lead did not establish a correct Scholar profile. |
| John Chi-Shing Lui | Cleared | [Source](https://www.cse.cuhk.edu.hk/~cslui/): General web searches and CUHK pages did not establish a correct Scholar profile; a Scholar publication-search link is not an author profile. |
| Jack Davidson | Cleared | [Source](https://www.cs.virginia.edu/~jwd/): General web searches for Jack/Jack W. Davidson and Virginia faculty evidence did not establish a correct Scholar profile. |
| Vicki Hanson | Cleared | [Source](https://vickihanson.org/research/): General web searches, personal research pages, and RIT evidence did not establish a correct Scholar profile. |
| James H Morris | Replaced with [Scholar](https://scholar.google.com/citations?user=9Y2cn3EAAAAJ) | [Source](https://www.wikidata.org/wiki/Q6135248): Web search identifies this ID; the captured profile matches CMU computer science and foundational string-matching/Andrew publications. Identity confirmed against https://www.cs.cmu.edu/~jhm/. Mixed-publication/aggregate-metrics caveat from the previous review remains. |

The James Morris correction establishes the profile association only; its previously observed unrelated medical publication remains a caveat for a future metrics import.
No Scholar citation rows or historical crawl artifacts were changed.
Updated only the seven affected embedded records in `docs/scholar_citations.html` using the visualization generator’s data builder, preserving unrelated pre-existing visualization changes.
Validated exactly seven `google_scholar_profile` cell changes, stable row order, LF line endings, and unchanged other CSVs.
The Fellows CSV retains 1,638 rows, with 1,278 distinct nonblank Scholar links and 360 blanks.
Search-source captures, verified Scholar HTML, backups, and the per-row change record are retained under `tmp/scholar-seven-corrections/`.

## 2026-09-16 20:08 EDT - Fresh Scholar Crawl Exception Review

Reviewed the September 16 Scholar crawl of all 1,282 nonblank URLs from the 1,638-row ACM Fellows dataset.
The crawl ran from 14:20 to 18:45 EDT with 5–7 seconds between profiles and 120–150 seconds between 25-profile batches, retaining five successful pilot captures.
It produced 1,236 successful pages and 46 HTTP 404 responses, with 24 automated name mismatches and no blocking.

Reviewed all 70 exception rows against captured profile names, affiliations, sample publications, ACM citations, historical data, and selected primary identity sources.
Accepted 17 mismatches as accents, transliterations, familiar names, or punctuation/name-part differences.
Rejected seven associations: Peter Müller → Peter Mueller (Texas statistics), Zi Helen Huang → TZE-TA HUANG (oral surgery), Nisheeth Vishnoi → Gerry Che, John Chi-Shing Lui → John C. Neill, Jack Davidson → Jack Davison (NIH), Vicki Hanson → Vicki L. Hansen (planetary science), and James H Morris → Michael H Morris (entrepreneurship).
These findings supersede earlier positive link evidence for those exact URLs; no canonical edits were applied in this review.

All 46 error bodies explicitly report the requested URL as not found.
Preserve the older exported metrics for Andrew B. Kahng, Dinesh Manocha, Guang Gao, and John McCarthy instead of replacing them with blanks or assigning a fresh crawl date.
The other 1,212 successful name matches were not independently identity-audited.
Excluding the seven wrong-person links leaves 1,229 successful captures eligible for a subsequent metrics review/update.

Checked four alternative URLs from local DBLP captures.
The alternative for Tajana Rosing also returned 404; the Daniel Jackson alternative belongs to a different researcher at Northumbria.
The [Laurie Hendren candidate](https://scholar.google.com/citations?user=e557wtEAAAAJ) has publications matching [McGill records](https://www.sable.mcgill.ca/mclab/publications/) but unknown affiliation and sparse coverage.
The [James Morris candidate](https://scholar.google.com/citations?user=9Y2cn3EAAAAJ) matches the [CMU computer scientist](https://www.cs.cmu.edu/~jhm/) but includes an unrelated prostate-cancer publication, so its aggregate metrics require further review.
Neither candidate was applied.

The original cache, input snapshot, report, log, and raw export remain under `../bigcows-crawler/.cache/acm-fellows-scholar-2026-09-16/`.
The local [row-by-row review](../tmp/scholar-crawl-review-2026-09-16/review.md), structured `review.json`, and four candidate captures are under `tmp/scholar-crawl-review-2026-09-16/`.
All canonical CSVs and original crawl artifacts remain unchanged.

## 2026-09-15 18:22 EDT - Consistent Award CSV Sort Order

Clarified the shared [award CSV sort order](../README_FOR_AGENTS.md#award-csv-sort-order): numeric award year descending, then the full stored name ascending using Python's `str.lower()` for case-insensitive comparison.
The comparison preserves punctuation and accents and does not extract surnames or use locale-specific collation.
This matches the name comparison already used by the citation visualization generator.
The earlier documentation specified ascending names without defining capitalization and explicitly covered only the Fellows CSV.

Applied the shared rule to both award CSVs.
Moved Gene Tsudik and Michael D Dahlin into name order within the 2014 and 2010 Fellows classes, respectively; intervening rows shifted accordingly.
The Turing Award CSV already satisfied the rule and required no moves.
The three capitalization-dependent inversions reported in the [18:12 EDT review](#2026-09-15-1812-edt---documentation-and-award-csv-consistency-review) do not require moves under the clarified case-insensitive rule.

Validated both complete row sequences against the shared sort key and compared row contents before and after sorting.
All cell values, row counts, CSV quoting, and Unix LF line endings were preserved, including the preceding user-approved Scholar changes.
No visualization regeneration was performed.

## 2026-09-15 18:21 EDT - User Resolution of Shared-Recipient Scholar Links

Applied the user's manual checks to `data/acm_fellows.csv` and `data/turing_award_winners.csv`.
The user rejected A J Milner's Scholar association; cleared the Turing URL with ID `1bezk50AAAAJ` and kept the already blank Fellows Scholar cell blank.
The user reported that C. Antony R. Hoare's `v-YdOywAAAAJ` URL returns HTTP 404; cleared it from the Fellows CSV and kept the already blank Turing Scholar cell blank.
These removals affect only Scholar links; both people's award-recipient rows and all other fields were retained.

The user reported that both Michael O. Rabin URLs lead to [_UUtVF4AAAAJ](https://scholar.google.com/citations?user=_UUtVF4AAAAJ).
Changed the Fellows URL from `EFZyUcEAAAAJ` to that selected URL; the Turing CSV already used it.
This records the user's selected equivalent URL rather than a wrong-person correction.

All three cross-dataset differences from the [18:12 EDT review](#2026-09-15-1812-edt---documentation-and-award-csv-consistency-review) are resolved, and all 63 matched recipients now have identical Scholar values across the two CSVs.
At completion, the Fellows CSV contained 1,638 rows, 1,282 distinct nonempty Scholar links, and 356 blank Scholar cells.
The Turing CSV contained 81 rows, 43 distinct nonempty Scholar links, and 38 blank Scholar cells.
The earlier 355-name Fellows unresolved table remains the historical search result; Hoare is the additional blank entry following this availability check.
The five Fellows ordering inversions recorded in the preceding review were unchanged in this batch; they were addressed by the [18:22 EDT sorting entry](#2026-09-15-1822-edt---consistent-award-csv-sort-order).
Validated that exactly three Scholar cells changed, with all other cells, row order, and Unix LF line endings preserved.
These decisions rely on the user's checks; no searches, crawls, cache updates, profile exports, or visualization regeneration were performed.

## 2026-09-15 18:12 EDT - Documentation and Award CSV Consistency Review

Compared the documented decisions with [ACM Fellows](../data/acm_fellows.csv) and [Turing Award winners](../data/turing_award_winners.csv) using only local files.
This checks agreement between the notes and CSVs; it does not independently verify profile identities, availability, or redirects.
The CSVs were not changed.

| Dataset | Rows | Scholar Links | Blank Scholar Cells | ACM Profile Links | Blank ACM Profile Cells |
| --- | --- | --- | --- | --- | --- |
| ACM Fellows | 1,638 | 1,283 | 355 | 1,627 | 11 |
| Turing Award Winners | 81 | 44 | 37 | 81 | 0 |

These counts agreed with the preceding dataset-specific entries; the [18:21 EDT resolutions](#2026-09-15-1821-edt---user-resolution-of-shared-recipient-scholar-links) subsequently changed the Scholar totals.
At this review, each dataset had unique names and unique nonempty Scholar URLs, with Unix LF line endings.
The award-year ranges were 1994–2025 for Fellows and 1966–2025 for Turing winners.

All 459 historical Fellows Scholar additions mapped to rows in the CSV at this review after applying the three documented name corrections.
Of those links, 456 matched the CSV; the three differences were the documented replacements for Jian Ma, David Lo, and Ming Li.
At this review, the 355-name unresolved table exactly matched the blank Fellows Scholar cells, and the 11-name unavailable ACM profile table exactly matched the blank Fellows ACM profile cells.
None of the 29 rejected Scholar IDs had been restored to the Fellow from whom it was removed.
The seven Turing additions, the later Hennessy and Goldwasser selections, and the blank Simon and Bachman cells all matched the CSV.
The documented name corrections, H. T. Kung's position immediately before Haibo Chen, and the deliberate citation and location differences recorded for the ACM captures were preserved.

Matched 63 Turing rows to Fellows by a unique identical DBLP URL or an exact CSV name.
The other 18 rows were not paired by these criteria; in particular, Alan Newell and Allen Newell remain separate people.
Three matched rows had different Scholar values at the end of this review.
All three were subsequently resolved in the [18:21 EDT entry](#2026-09-15-1821-edt---user-resolution-of-shared-recipient-scholar-links); the table below preserves the values reviewed:

| Person | ACM Fellows Scholar Profile | Turing Scholar Profile | Review Status |
| --- | --- | --- | --- |
| A J Milner | Blank | [1bezk50AAAAJ](https://scholar.google.com/citations?user=1bezk50AAAAJ) | The Turing link was retained without search corroboration; the Fellows search left its cell blank. |
| C. Antony R. Hoare | [v-YdOywAAAAJ](https://scholar.google.com/citations?user=v-YdOywAAAAJ) | Blank | The Fellows enrichment established this link using its recorded evidence; the later Turing search-only review did not establish a matching ID. |
| Michael O. Rabin | [EFZyUcEAAAAJ](https://scholar.google.com/citations?user=EFZyUcEAAAAJ) | [_UUtVF4AAAAJ](https://scholar.google.com/citations?user=_UUtVF4AAAAJ) | The Fellows enrichment selected one ID; the Turing review retained the other without search corroboration; redirect equivalence is unverified. |

This comparison identified differences between separately reviewed datasets without establishing new wrong-person links.
No cross-dataset link propagation or ID selection was performed.

At this review, both CSVs were ordered by descending award year, and the Turing CSV was also ordered by name within each year.
A literal, case-sensitive name comparison found five adjacent ordering inversions in the Fellows CSV:

| Fellows Year | Preceded at Review | Followed at Review |
| --- | --- | --- |
| 2014 | Paul Syverson | Gene Tsudik |
| 2010 | Michael I. Jordan | Michael D Dahlin |
| 2009 | Ricardo A Baeza-Yates | RJ Miller |
| 1996 | Takao Nishizeki | TRN Rao |
| 1994 | Gerald L Engel | GERALD SUSSMAN |

The last three depended on capitalization under this comparison; the first two were also out of order under a case-insensitive comparison.
The earlier H. T. Kung ordering fix was local to that correction and did not establish that every class was sorted.
This review recorded the ordering issues without changing names or row order.
The [18:22 EDT entry](#2026-09-15-1822-edt---consistent-award-csv-sort-order) subsequently documents the clarified rule and completed re-sort.

## 2026-09-15 17:47 EDT - User Resolution of Turing Award Scholar Candidates

Applied the user's selections in `data/turing_award_winners.csv`.
Updated John L Hennessy's Scholar URL from `WqUMGMsAAAAJ` to [tp07xT0AAAAJ](https://scholar.google.com/citations?user=tp07xT0AAAAJ).
Added the approved [Shafi Goldwasser profile](https://scholar.google.com/citations?user=KA8dgpMAAAAJ) to her previously blank cell.
Kept Herbert A Simon's Scholar cell blank as requested; the historical candidate `9d7rMrkAAAAJ` was never added to the CSV and is no longer pending review.

These decisions resolve all three specific candidate cases from the preceding review without establishing whether Hennessy's old and new URLs redirect to the same profile.
The 14 existing links without corroborating search evidence were unchanged in this batch.
The user subsequently rejected Milner's link and confirmed Rabin's selected URL in the [18:21 EDT resolutions](#2026-09-15-1821-edt---user-resolution-of-shared-recipient-scholar-links).
At completion, the Turing Award dataset contained 81 winners, 44 distinct nonempty Scholar links, and 37 blank Scholar cells.
Only Hennessy's and Goldwasser's Scholar cells changed in this follow-up; all other cells and row order were preserved.
No searches, crawls, profile exports, cache updates, or visualization regeneration were performed.

## 2026-09-15 17:23 EDT - Turing Award Scholar Search Review

Reviewed all 81 rows of `data/turing_award_winners.csv`, checking the 37 existing Scholar links and searching for profiles for all 44 previously blank entries.
Used 202 general web-search queries in 51 serial calls, with at most four queries per call and at least ten seconds between search calls.
Follow-up searches used name variants, affiliations, exact Scholar IDs, and institutional sources where available.
No direct profile requests, crawls, browser automation, or cached profile evidence were used.
Search evidence associates a person with an ID; it does not verify current profile availability, redirect equivalence, account ownership, or the accuracy of every listed publication.

Added seven previously missing links:

| Winner | Added Scholar Profile | Indexed Evidence |
| --- | --- | --- |
| Charles H. Bennett | [mkjGmJEAAAAJ](https://scholar.google.com/citations?user=mkjGmJEAAAAJ) | [Source](https://www.wikidata.org/wiki/Q92931) |
| Gilles Brassard | [Rh7_srgAAAAJ](https://scholar.google.com/citations?user=Rh7_srgAAAAJ) | [Source](https://www-labs.iro.umontreal.ca/~brassard/CV/Brassard-CV-May2024.pdf) |
| Andrew Barto | [CMIgrCgAAAAJ](https://scholar.google.com/citations?user=CMIgrCgAAAAJ) | [Source](https://www.wikidata.org/wiki/Q4756294) |
| Richard Sutton | [6m4wv6gAAAAJ](https://scholar.google.com/citations?user=6m4wv6gAAAAJ) | [Source](https://www.wikidata.org/wiki/Q7328833) |
| Raj Reddy | [mYu2uuIAAAAJ](https://scholar.google.com/citations?user=mYu2uuIAAAAJ) | [Source](https://www.wikidata.org/wiki/Q92820) |
| Stephen A Cook | [VGxPtzIAAAAJ](https://scholar.google.com/citations?user=VGxPtzIAAAAJ) | [Source](https://www.wikidata.org/wiki/Q62870) |
| Dana S Scott | [oaja5KYAAAAJ](https://scholar.google.com/citations?user=oaja5KYAAAAJ) | [Source](https://www.wikidata.org/wiki/Q49823) |

Brassard's institutional CV explicitly supplies his Scholar ID.
The other additions rely on indexed secondary identity records, including explicit Scholar IDs on the matching Wikidata entities.
Sutton's Wikidata record marks `hNTyptAAAAAJ` incorrect and identifies `6m4wv6gAAAAJ` as its replacement; the selected ID also appears in [Gabor Melli's Sutton entry](https://www.gabormelli.com/RKB/Richard_S._Sutton).
These additions are supported identity matches, not live availability checks.

Cleared Charles W Bachman's stored `SqR9pOYAAAAJ` link.
The URL is explicitly listed by [Charles Bachmann at RIT](https://www.linkedin.com/in/charles-bachmann-77020a125), whose [institutional directory entry](https://www.rit.edu/dirs/directory/cmbpci-charles-bachmann) identifies an imaging scientist rather than the Turing Award database pioneer.
No supported replacement was found.

Of the 37 original links, 21 had indexed evidence associating the exact ID with the winner, 14 remained uncorroborated, one had an unresolved alternative ID, and one was removed as a wrong-person match.
Retained the 14 uncorroborated links: Robert Melancton Metcalfe, Judea Pearl, E. Allen Emerson, Frederick Brooks, Jim Gray, Butler W Lampson, A J Milner, John E Hopcroft, Richard Karp, Kenneth Lane Thompson, Kenneth E. Iverson, Michael O. Rabin, J. H. Wilkinson, Marvin Minsky.
Lack of search evidence alone is not grounds to clear them.

Three specific cases were held for user review at the end of this batch.
All three were subsequently resolved in the [17:47 EDT entry](#2026-09-15-1747-edt---user-resolution-of-turing-award-scholar-candidates).
The table preserves the candidates and reasons for holding them at that time:

| Winner | Stored Profile | Candidate | Reason for Holding |
| --- | --- | --- | --- |
| John L Hennessy | [WqUMGMsAAAAJ](https://scholar.google.com/citations?user=WqUMGMsAAAAJ) | [tp07xT0AAAAJ](https://scholar.google.com/citations?user=tp07xT0AAAAJ) | [CitationMap](https://citationmap.com/profile/tp07xT0AAAAJ) and an [indexed architecture overview](https://www.zhihu.com/en/article/674906758) associate the alternative with Stanford's John Hennessy; search did not corroborate the stored ID or establish whether the URLs redirect to the same profile. |
| Shafi Goldwasser | Blank | [KA8dgpMAAAAJ](https://scholar.google.com/citations?user=KA8dgpMAAAAJ) | [CitationMap](https://citationmap.com/profile/KA8dgpMAAAAJ) associates this ID with Berkeley's Shafi Goldwasser, but no independent explicit-ID confirmation was found. |
| Herbert A Simon | Blank | [9d7rMrkAAAAJ](https://scholar.google.com/citations?user=9d7rMrkAAAAJ) | [Wikidata](https://www.wikidata.org/wiki/Q181529) supports the historical identity, but an [indexed biography mirror](https://everything.explained.today/Herbert_A._Simon/) labels the link dead; current availability remains unresolved. |

The remaining 35 previously blank entries had no sufficiently supported candidate after follow-up searches.
Together with the two held blank candidates and Bachman's cleared cell, 38 entries were blank at completion.
At completion, the Turing Award dataset contained 81 winners and 43 distinct nonempty Scholar links, up from 37.
Only eight Scholar cells changed; all names, other cell values, and row order were preserved.
Validated row count, schema, the exact cell-change set, URL format and uniqueness, and Unix LF line endings.
No crawler code, profile exports, caches, or visualizations were changed.
Local scratch files `tmp/turing-scholar-audit-2026-09-15.json`, `tmp/turing-scholar-search-complete-2026-09-15.json`, and `tmp/turing-scholar-search-final-batches-2026-09-15.json` retain per-winner outcomes and the search log; these are not committed artifacts.

## 2026-09-15 17:05 EDT - Restore Name Ordering after H. T. Kung Correction

Moved H. T. Kung immediately ahead of Haibo Chen in the 2023 class to restore the name ordering affected by the earlier formatting correction.
This follow-up to [PR #53 review](https://github.com/lintool/acm-bigcows/pull/53#discussion_r4020136622) changes only the two rows' relative positions; all CSV cell values are preserved.
Earlier entries' row-order preservation statements describe those batches before this follow-up.
No crawls, cache updates, profile exports, or visualization regeneration were performed.

## 2026-09-15 16:37 EDT - Final User Resolution of Scholar Link Conflicts

The user resolved the five remaining conflicting-ID cases through browser checks.
For Dan Roth, Yossi Matias, Ming Li, and Giovanni De Micheli, the user reported that both candidate URLs reach the same profile.
Retained the user-selected URLs for [Dan Roth](https://scholar.google.com/citations?user=E-bpPWgAAAAJ), [Yossi Matias](https://scholar.google.com/citations?user=IwSe1-MAAAAJ), [Mark D. Hill](https://scholar.google.com/citations?user=7lVfIWYAAAAJ), and [Giovanni De Micheli](https://scholar.google.com/citations?user=7SUnVDsAAAAJ).
Updated Ming Li's URL from `oGgPXFEAAAAJ` to the user-selected [j1xcTB4AAAAJ](https://scholar.google.com/citations?user=j1xcTB4AAAAJ); this records the selected equivalent URL rather than a wrong-person correction.

The identity, conflicting-ID, and availability cases presented for user review during the web-search audit were resolved by this point.
The [earlier cache-only review](#2026-09-15---outstanding-review-candidates) separately records identity suspicions and publication-list concerns; this entry does not record a resolution for those cases.
The web-search audit also left 626 links without corroborating search evidence; unsuccessful searches did not establish that profiles were absent for the 355 blank entries.
Only Ming Li's Scholar cell changed in this batch; at completion, the dataset contained 1,638 Fellows, 1,283 distinct nonempty Scholar links, and 355 blank Scholar cells.
No new crawls or automated profile fetches were performed, and no exports, caches, or visualizations were regenerated.

## 2026-09-15 16:34 EDT - User-Confirmed Scholar Profiles and Resolved Link Conflicts

The user checked the candidate Scholar profiles and confirmed [Jian Ma](https://scholar.google.com/citations?user=nDw9v78AAAAJ) and [David Lo](https://scholar.google.com/citations?user=Ra4bt-oAAAAJ).
Added these two URLs to the previously cleared cells in `data/acm_fellows.csv`, resolving the pending replacements described below.
At completion, the ACM Fellows dataset contained 1,283 nonempty Scholar links and 355 blank Scholar cells across 1,638 Fellows.

Retained the stored [C.-C. Jay Kuo profile](https://scholar.google.com/citations?user=81d60okAAAAJ), which the user confirmed resolves correctly; the corresponding CSV row is named `Chung C. J Kuo`.
Retained [XiaoFeng Wang's stored URL](https://scholar.google.com/citations?user=pONu-5EAAAAJ); the user confirmed that the alternative ending in lowercase `j` redirects to the same profile.
Retained the user-selected [David Z. Pan profile](https://scholar.google.com/citations?user=3aLlroEAAAAJ) and [Tandy Warnow profile](https://scholar.google.com/citations?user=BYZtDXEAAAAJ), which already matched the CSV.
Also recorded the user's earlier confirmation that the stored [Madhav Marathe](https://scholar.google.com/citations?user=diIore8AAAAJ) and [Michael Littman](https://scholar.google.com/citations?user=iRMZ2hoAAAAJ) links are correct and should be retained.
These resolutions rely on the user's checks; no new crawls or automated profile fetches were performed.

Five conflicting-ID cases remained unresolved at the end of this batch: Dan Roth, Yossi Matias, Ming Li, Mark D. Hill, and Giovanni De Micheli.
Their stored links were unchanged in this batch; the user's subsequent decisions are recorded in the [16:37 EDT entry](#2026-09-15-1637-edt---final-user-resolution-of-scholar-link-conflicts).
Only the two approved Scholar cells changed in this batch; all other CSV cells and row order were preserved, and no exports, caches, or visualizations were regenerated.

## 2026-09-15 16:27 EDT - Name Corrections and Wrong-Person Scholar Link Removal

Applied five approved cell corrections in `data/acm_fellows.csv` from the web-search-only review.
Corrected `Ht Kung` to `H. T. Kung`, `Andrew K. Mccallum` to `Andrew K. McCallum`, and `Dianne Prost OLeary` to `Dianne Prost O'Leary`.
Supporting name evidence is available in the [H. T. Kung biography](https://handwiki.org/wiki/Biography%3AH._T._Kung), [UMass McCallum page](https://cssi.cs.umass.edu/people/andrew-mccallum), and [O'Leary's Maryland homepage](https://www.cs.umd.edu/~oleary/).

Cleared Jian Ma's Scholar URL with ID `kDZcBhkAAAAJ`, which belongs to plant scientist Jian Feng Ma, as identified in the [JSPS grant document](https://www.jsps.go.jp/file/storage/kaken_12_g_4805/r_8_en_26k21758.pdf).
The ACM Fellow is the [CMU computational biologist Jian Ma](https://www.cmu.edu/computational-cancer/faculty/ma_jian.html).
Candidate replacement [nDw9v78AAAAJ](https://scholar.google.com/citations?user=nDw9v78AAAAJ) is supported by his [indexed biography](https://en.wikipedia.org/wiki/Jian_Ma_%28computational_biologist%29), but was left unassigned pending primary-source confirmation at that time.

Cleared David Lo's Scholar URL with ID `IFg0H1wAAAAJ`, associated with the [UC Riverside medical researcher David D. Lo](https://www.linkedin.com/in/david-d-lo-b7443273).
The ACM Fellow is the [SMU computer scientist David Lo](https://news.smu.edu.sg/sites/news.smu.edu.sg/files/smu/news_room/SMU%20Media%20Release_SMU%20Faculty%20David%20Lo%20achieves%20ACM%20Fellowship%2005Feb2024.pdf).
Candidate replacement [Ra4bt-oAAAAJ](https://scholar.google.com/citations?user=Ra4bt-oAAAAJ) is supported by a [matching secondary listing](https://www.newx.sg/scholar/Ra4bt-oAAAAJ), but was left unassigned pending primary-source confirmation at that time.

The user subsequently approved both replacements in the [16:34 EDT entry](#2026-09-15-1634-edt---user-confirmed-scholar-profiles-and-resolved-link-conflicts).

At completion, the ACM Fellows dataset contained 1,281 nonempty Scholar links and 357 blank Scholar cells across 1,638 Fellows.
All other CSV cells and row order were preserved, including the unresolved Madhav Marathe and Michael Littman links.
No new crawls were performed, and no profile exports, caches, or visualizations were regenerated.

## 2026-09-15 13:49 EDT - Google Scholar Links: Review of All Remaining Missing Entries

This review searched all 522 entries whose Scholar field was blank at the start, including unresolved entries from previous batches.
Each name received a general web search, followed by focused searches or source-link checks where a promising match or identity conflict warranted them.
General web search and existing local records established 167 matching profiles, which were added to the CSV.
At completion, the ACM Fellows dataset contained 1,283 nonempty Scholar links and 355 blank Scholar cells across 1,638 Fellows.
Only the 167 previously blank Scholar URL cells changed; names, row order, and all other CSV fields were preserved.
No computer-use tools or project crawlers were used, and no caches, Scholar profile exports, or visualizations were regenerated.
The source column below distinguishes explicit web links from existing local IDs corroborated by web identity evidence.
Existing CSRankings records are from `../bigcows-crawler/.cache/csrankings/csrankings-*.csv`, and cached profile and coauthor evidence is from `../bigcows-crawler/.cache/google-scholar-profile-cache.json`.
These checks establish identity and link correspondence; they are not fresh audits of publication lists or citation metrics.
An explicit source link established the destination URL even when Scholar returned an access error; that error was not treated as evidence that the profile did not exist.
Every added ID is distinct from all previously assigned IDs and from the wrong-person IDs removed in the earlier audit.

### 2026-09-15 13:49 EDT - Identity Decisions

Explicit web links resolved conflicting local IDs for Yan Solihin, Trent Jaeger, Dennis Shasha, Pavel Pevzner, John Hennessy, and Peter J Denning.
For Raj Reddy, the existing coauthor ID matches the CMU computing researcher, while the other local candidate belongs to an agriculture researcher.
Peter Chen in the 2010 class is Peter M. Chen at Michigan; Peter P Chen is a separate Fellow and remains unresolved.
Waterloo's faculty page explicitly confirms Ming Li's selected ID.
The Stanford page confirms the Oyekunle/Kunle Olukotun name variant.
The Scholar page reached from Michael D Schroeder's source matches his Microsoft systems identity but also contains some apparently unrelated papers, including clinical epilepsy and neural-ranking work; the identity match does not certify the accuracy of every publication.
Namesakes were excluded where affiliations or research areas differed, including Umesh/Vijay Vazirani, Alan/Allen Newell, Gopal Krishna Gupta/Gopal Gupta, Philip M Lewis, John B Goodenough, Adele Goldberg, and Peter Elias.

### 2026-09-15 13:49 EDT - Added Profiles

| ACM Fellow | Added Scholar Profile | Source and Identity Evidence |
| --- | --- | --- |
| Natarajan Shankar | [Scholar](https://scholar.google.com/citations?user=qVzY4XYAAAAJ) | [Source](https://research.com/u/natarajan-shankar): Explicit Scholar link identifies the SRI formal-methods researcher. |
| Yan Solihin | [Scholar](https://scholar.google.com/citations?user=tndlIesAAAAJ) | [Source](https://expertnet.org/index.cfm?fuseaction=experts.details&id=130969): Florida ExpertNet explicitly prints this ID for Yan Solihin; Research.com links the same ID, resolving the different CSRankings candidate. |
| Guoliang Li | [Scholar](https://scholar.google.com/citations?user=Pi89P8kAAAAJ) | [Source](https://www.newx.sg/scholar/Pi89P8kAAAAJ): Exact ID identifies the Tsinghua database researcher. |
| Trent Jaeger | [Scholar](https://scholar.google.com/citations?user=LpwdzeEAAAAJ) | [Source](https://www.cs.ucr.edu/~trentj/research.html): Personal UCR page directly links this ID, agreeing with cached coauthor evidence and resolving the conflicting CSRankings ID. |
| C. Antony R. Hoare | [Scholar](https://scholar.google.com/citations?user=v-YdOywAAAAJ) | **Later removed:** The user reported HTTP 404 in the [18:21 EDT resolutions](#2026-09-15-1821-edt---user-resolution-of-shared-recipient-scholar-links). Initial evidence: [Source](https://research.com/u/tony-hoare): Explicit Scholar link identifies C. A. R. Hoare and his program-verification work. |
| Joseph Bryan Lyles | [Scholar](https://scholar.google.com/citations?user=U12mxPQAAAAJ) | [Source](https://dblp.org/pid/03/4762.html): J. Bryan Lyles networking bibliography matches the exact name and profile ID in existing cached coauthor records. |
| Dennis E. Shasha | [Scholar](https://scholar.google.com/citations?user=UH3qseUAAAAJ) | [Source](https://adscientificindex.com/scientist/dennis-shasha/834425/): The matching research biography explicitly links this Scholar profile. |
| Douglas Lea | [Scholar](https://scholar.google.com/citations?user=7yk1kw4AAAAJ) | [Source](https://gee.cs.oswego.edu/dl/): Personal SUNY Oswego homepage identifies Doug Lea and Java concurrency work, matching the cached coauthor ID. |
| Henry A Kautz | [Scholar](https://scholar.google.com/citations?user=WxQyOYQAAAAJ) | [Source](https://en.wikipedia.org/wiki/Henry_Kautz): Web result explicitly gives the Scholar ID for the AI researcher; existing CSRankings and coauthor records agree. |
| Mark S Ackerman | [Scholar](https://scholar.google.com/citations?user=qBTbnEQAAAAJ) | [Source](https://dblp.org/pid/a/MSAckerman.html): Michigan HCI bibliography matches the existing cached Mark Ackerman coauthor ID. |
| Nir N Shavit | [Scholar](https://scholar.google.com/citations?user=f1NaDVgAAAAJ) | [Source](https://shavitlab.csail.mit.edu/contact.html): MIT lab page directly links this Scholar ID for Nir Shavit. |
| Panganamala Kumar | [Scholar](https://scholar.google.com/citations?user=qGUpTVwAAAAJ) | [Source](https://research.com/u/p-r-kumar): Explicit Scholar link identifies P. R. Kumar at Texas A&M and his control and networking research. |
| Peter Haas | [Scholar](https://scholar.google.com/citations?user=PeCI8KcAAAAJ) | [Source](https://people.cs.umass.edu/~phaas/): Personal UMass homepage identifies Peter J. Haas and his IBM and information-management background, agreeing with existing local records. |
| Sampath Kumar Kannan | [Scholar](https://scholar.google.com/citations?user=WhvtccoAAAAJ) | [Source](https://www.cis.upenn.edu/~kannan/): Personal Penn homepage confirms Sampath Kannan's identity, agreeing with existing CSRankings and coauthor records. |
| Satish Rao | [Scholar](https://scholar.google.com/citations?user=x_cgL6gAAAAJ) | [Source](https://people.eecs.berkeley.edu/~satishr/): Personal Berkeley algorithms homepage corroborates the Satish Rao entry in existing CSRankings. |
| Timoleon Sellis | [Scholar](https://scholar.google.com/citations?user=G1Iux80AAAAJ) | [Source](https://advancedstudies.cyu.fr/medias/fichier/sellis-cv_1657972647832-pdf?ID_FICHE=2228&INLINE=FALSE): CV explicitly gives the Scholar ID and connects Timoleon Sellis with Timos Sellis; cached coauthor evidence agrees. |
| Val Tannen | [Scholar](https://scholar.google.com/citations?user=3Jus1k0AAAAJ) | [Source](https://www.alphaxiv.org/@val-tannen): Database and programming-language research record matches the cached Penn Val Tannen coauthor ID. |
| Yuanyuan Zhou | [Scholar](https://scholar.google.com/citations?user=rWl0U0oAAAAJ) | [Source](https://cseweb.ucsd.edu/~yyzhou/): Personal UCSD systems homepage corroborates the Yuanyuan Zhou entry in existing CSRankings. |
| David Paul Grove | [Scholar](https://scholar.google.com/citations?user=iU8ijrYAAAAJ) | [Source](https://research.ibm.com/people/david-grove): IBM researcher page directly links this Scholar ID. |
| Larry S Davis | [Scholar](https://scholar.google.com/citations?user=lc0ARagAAAAJ) | [Source](https://en.wikipedia.org/wiki/Larry_S._Davis): Maryland computer-vision identity matches the cached Larry Davis coauthor ID. |
| Leslie G Valiant | [Scholar](https://scholar.google.com/citations?user=H509xdsAAAAJ) | [Source](https://dblp.org/pid/v/LeslieGValiant.html): Existing local records identify Leslie G. Valiant at Harvard University; the web result corroborates the matching computing research identity. |
| Raj Reddy | [Scholar](https://scholar.google.com/citations?user=mYu2uuIAAAAJ) | [Source](https://dblp1.uni-trier.de/pid/r/RajReddy.html): Existing local records identify Raj Reddy at University Professor of Computer Science and Robotics, Carnegie Mellon University; the web result corroborates the matching computing research identity. |
| Rajeev Ramnarain Rastogi | [Scholar](https://scholar.google.com/citations?user=3ggE9SkAAAAJ) | [Source](https://adscientificindex.com/scientist/rajeev-rastogi/4968100/): Existing local records identify Rajeev Rastogi at Amazon; the web result corroborates the matching computing research identity. |
| Robert Schreiber | [Scholar](https://scholar.google.com/citations?user=APiItS4AAAAJ) | [Source](https://adscientificindex.com/scientist/doe-hyun-yoon/4379616/): Web coauthor listing identifies Rob Schreiber at Cerebras, agreeing with cached coauthor evidence and excluding the immunologist. |
| Simson L Garfinkel | [Scholar](https://scholar.google.com/citations?user=87fGQ0AAAAAJ) | [Source](https://simson.net/page/Main_Page): Existing local records identify Simson Garfinkel at BasisTech, LLC; the web result corroborates the matching computing research identity. |
| Dean Tullsen | [Scholar](https://scholar.google.com/citations?user=BEEuinQAAAAJ) | [Source](https://research.com/u/dean-tullsen): Existing local records identify Dean M. Tullsen at Univ. of California - San Diego; the web result corroborates the matching computing research identity. |
| Diane L Souvaine | [Scholar](https://scholar.google.com/citations?user=QTRDjTUAAAAJ) | [Source](https://www.cs.tufts.edu/~dls/): Existing local records identify Diane L. Souvaine at Tufts University; the web result corroborates the matching computing research identity. |
| Howard J Karloff | [Scholar](https://scholar.google.com/citations?user=i5PazXwAAAAJ) | [Source](https://research.google/pubs/randomized-algorithms-and-pseudorandom-numbers/): Existing local records identify Howard Karloff at Goldman Sachs; the web result corroborates the matching computing research identity. |
| Ming C Lin | [Scholar](https://scholar.google.com/citations?user=ugFNit4AAAAJ) | [Source](https://www.cs.umd.edu/people/lin): Existing local records identify Ming C. Lin at Univ. of Maryland - College Park; the web result corroborates the matching computing research identity. |
| Peter B. Key | [Scholar](https://scholar.google.com/citations?user=muWfggEAAAAJ) | [Source](https://dblp.org/pid/22/3458): Existing local records identify Peter Key at Consultant researcher; the web result corroborates the matching computing research identity. |
| Ronald M Baecker | [Scholar](https://scholar.google.com/citations?user=-X6Rj5EAAAAJ) | [Source](https://dblp.org/pid/b/RonaldBaecker.html): Existing local records identify Ron Baecker, Ronald Baecker at Professor of Computer Science, University of Toronto; the web result corroborates the matching computing research identity. |
| Shubu Mukherjee | [Scholar](https://scholar.google.com/citations?user=tRaNOv4AAAAJ) | [Source](https://www.bohrium.com/scholar/Y561851t/Shubu_Mukherjee): Existing local records identify Shubu Mukherjee at Vice President, Architecture, SiFive, Inc.; the web result corroborates the matching computing research identity. |
| Susan Landau | [Scholar](https://scholar.google.com/citations?user=6emSUYoAAAAJ) | [Source](https://fletcher.tufts.edu/academics/faculty/susan-landau): Existing local records identify Susan Landau 0001 at Tufts University; the web result corroborates the matching computing research identity. |
| Zehra Ozsoyoglu | [Scholar](https://scholar.google.com/citations?user=QRrrUU0AAAAJ) | [Source](https://www.researchgate.net/profile/Zehra-Ozsoyoglu): Existing local records identify Z. Meral Özsoyoglu at Case Western Reserve University; the web result corroborates the matching computing research identity. |
| Daniel A Spielman | [Scholar](https://scholar.google.com/citations?user=L82mYv8AAAAJ) | [Source](https://dblp.org/pid/s/DanielASpielman.html): Existing local records identify Daniel A. Spielman at Yale University; the web result corroborates the matching computing research identity. |
| David M Ungar | [Scholar](https://scholar.google.com/citations?user=wmKyC-EAAAAJ) | [Source](https://dblp.org/pid/84/5937.html): Existing local records identify David Ungar at Apple; the web result corroborates the matching computing research identity. |
| Douglas C Burger | [Scholar](https://scholar.google.com/citations?user=5JtQbw0AAAAJ) | [Source](https://www.microsoft.com/en-us/research/people/dburger/): Microsoft's Doug Burger biography matches the cached coauthor name, affiliation and ID. |
| Kathleen S Fisher | [Scholar](https://scholar.google.com/citations?user=8mi-oYYAAAAJ) | [Source](https://engineering.tufts.edu/cs/people/faculty/kathleen-fisher): Existing local records identify Kathleen Fisher at Adjunct Professor of Computer Science, Tufts University; the web result corroborates the matching computing research identity. |
| Michael D Dahlin | [Scholar](https://scholar.google.com/citations?user=hdXvVdgAAAAJ) | [Source](https://dblp.org/pid/d/MDahlin): Existing local records identify M Dahlin at Professor of Computer Science University of Texas; the web result corroborates the matching computing research identity. |
| Pavel Pevzner | [Scholar](https://scholar.google.com/citations?user=0fq5QeIAAAAJ) | [Source](https://research.com/u/pavel-pevzner): Explicit Scholar link corroborates the CSRankings ID for the UCSD computational-biology researcher over a different cached coauthor candidate. |
| Peter Chen | [Scholar](https://scholar.google.com/citations?user=dVZNQqUAAAAJ) | [Source](https://web.eecs.umich.edu/~pmchen/): Existing local records identify Peter M. Chen at University of Michigan; the focused web result corroborates this identity. |
| Philip N Klein | [Scholar](https://scholar.google.com/citations?user=gVUD47sAAAAJ) | [Source](https://dblp.org/pid/k/PhilipNKlein.html): Existing local records identify Philip N. Klein at Brown University; the web result corroborates the matching computing research identity. |
| Richard F Lyon | [Scholar](https://scholar.google.com/citations?user=sJJamz4AAAAJ) | [Source](https://research.com/u/richard-f-lyon): Explicit Scholar link identifies Richard F. Lyon and his hearing and recognition research. |
| Wendy Hall | [Scholar](https://scholar.google.com/citations?user=9NaDv3oAAAAJ) | [Source](https://www.southampton.ac.uk/people/5wyswr/professor-dame-wendy-hall): Existing local records identify Wendy Hall 0001 at University of Southampton; the web result corroborates the matching computing research identity. |
| Arie E Kaufman | [Scholar](https://scholar.google.com/citations?user=fDdcWBEAAAAJ) | [Source](https://www.newx.sg/scholar/fDdcWBEAAAAJ): Existing local records identify Arie E. Kaufman at Stony Brook University; the web result corroborates the matching computing research identity. |
| Bruce R. Donald | [Scholar](https://scholar.google.com/citations?user=TkayRqQAAAAJ) | [Source](https://users.cs.duke.edu/~brd/papers/): Existing local records identify Bruce Randall Donald at Duke University; the web result corroborates the matching computing research identity. |
| Chandrajit L. Bajaj | [Scholar](https://scholar.google.com/citations?user=gyL3CZ0AAAAJ) | [Source](https://www.cs.utexas.edu/~bajaj/): Existing local records identify Chandrajit Bajaj at University of Texas at Austin; the web result corroborates the matching computing research identity. |
| Chandramohan A Thekkath | [Scholar](https://scholar.google.com/citations?user=B_uwswQAAAAJ) | [Source](https://research.com/u/chandramohan-a-thekkath): Explicit Scholar link identifies Chandramohan Thekkath and systems publications. |
| Erich L Kaltofen | [Scholar](https://scholar.google.com/citations?user=irht4jgAAAAJ) | [Source](https://kaltofen.math.ncsu.edu/): The matching researcher page explicitly links this Scholar profile. |
| Gaetano Borriello | [Scholar](https://scholar.google.com/citations?user=wUS-iRsAAAAJ) | [Source](https://research.com/u/gaetano-borriello): Explicit Scholar link identifies the Washington ubiquitous-computing researcher. |
| John Chi-Shing Lui | [Scholar](https://scholar.google.com/citations?user=7LVjQ7MAAAAJ) | [Source](https://www.cs.cuhk.hk/~cslui/): Existing local records identify John C. S. Lui at Chinese University of Hong Kong; the web result corroborates the matching computing research identity. |
| John T Riedl | [Scholar](https://scholar.google.com/citations?user=iFWaKtMAAAAJ) | [Source](https://en.wikipedia.org/wiki/John_T._Riedl): Existing local records identify John Riedl at Professor of Computer Science, University of Minnesota; the web result corroborates the matching computing research identity. |
| Jose A Blakeley | [Scholar](https://scholar.google.com/citations?user=VV3ByXUAAAAJ) | [Source](https://dblp.org/pid/79/2594): Existing local records identify Jose Blakeley at Microsoft Corporation; the web result corroborates the matching computing research identity. |
| Laurie J Hendren | [Scholar](https://scholar.google.com/citations?user=uouHKIkAAAAJ) | [Source](https://en.wikipedia.org/wiki/Laurie_Hendren): The reference explicitly gives the Scholar ID for Laurie J. Hendren, the McGill compiler researcher. |
| Paulo Esteves-Verissimo | [Scholar](https://scholar.google.com/citations?user=aMHx8aUAAAAJ) | [Source](https://cemse.kaust.edu.sa/profiles/paulo-esteves-verissimo): Existing local records identify Paulo Esteves Veríssimo at KAUST; the web result corroborates the matching computing research identity. |
| Rajiv Gupta | [Scholar](https://scholar.google.com/citations?user=6P4bGWAAAAAJ) | [Source](https://www.cs.ucr.edu/~gupta/): Existing local records identify Rajiv Gupta 0001 at Univ. of California - Riverside; the web result corroborates the matching computing research identity. |
| Ricardo A Baeza-Yates | [Scholar](https://scholar.google.com/citations?user=v9xULZwAAAAJ) | [Source](https://adscientificindex.com/scientist/ricardo-baeza-yates/1502146/): Existing local records identify Ricardo Baeza-Yates at KTH - Univ. Pompeu Fabra - Univ. de Chile; Sweden, Spain & Chile; the web result corroborates the matching computing research identity. |
| RJ Miller | [Scholar](https://scholar.google.com/citations?user=NjeM1LsAAAAJ) | [Source](https://www.cs.toronto.edu/~miller/publications.html): Renee J. Miller's database research identity matches the RJ Miller Fellow and the existing CSRankings ID. |
| Rudrapatna K Shyamasundar | [Scholar](https://scholar.google.com/citations?user=gNhIpRwAAAAJ) | [Source](https://dblp.uni-trier.de/pid/s/RKShyamasundar.html): DBLP's matching computing bibliography explicitly links this Scholar profile. |
| Shang-Hua Teng | [Scholar](https://scholar.google.com/citations?user=tn29sAQAAAAJ) | [Source](https://www.wikidata.org/wiki/Q92663): The Shang-Hua Teng record explicitly lists this Scholar author ID. |
| Thomas D Erickson | [Scholar](https://scholar.google.com/citations?user=e5yN9ewAAAAJ) | [Source](https://research.com/u/thomas-erickson): Existing local records identify Thomas Erickson at retired@Minneapolis; the web result corroborates the matching computing research identity. |
| Thomas L Dean | [Scholar](https://scholar.google.com/citations?user=zJd3D4YAAAAJ) | [Source](https://en.wikipedia.org/wiki/Thomas_Dean_%28computer_scientist%29): Existing local records identify Thomas Dean at Brown University; the web result corroborates the matching computing research identity. |
| Douglas B Terry | [Scholar](https://scholar.google.com/citations?user=4ZYEiVEAAAAJ) | [Source](https://research.com/u/douglas-terry): The matching research biography explicitly links this Scholar profile. |
| Jack Davidson | [Scholar](https://scholar.google.com/citations?user=n7YuWIAAAAAJ) | [Source](https://dblp.org/pid/d/JWDavidson): Existing local records identify Jack W. Davidson at University of Virginia; the web result corroborates the matching computing research identity. |
| Jitendra Malik | [Scholar](https://scholar.google.com/citations?user=oY9R5YQAAAAJ) | [Source](https://vcresearch.berkeley.edu/faculty/jitendra-malik): Existing local records identify Jitendra Malik at Univ. of California - Berkeley; the web result corroborates the matching computing research identity. |
| Judith S Olson | [Scholar](https://scholar.google.com/citations?user=xfwOz_kAAAAJ) | [Source](https://dblp.org/pid/04/1690.html): Existing local records identify Judith S. Olson at Univ. of California - Irvine; the web result corroborates the matching computing research identity. |
| Lawrence C Paulson | [Scholar](https://scholar.google.com/citations?user=Sv1hcjEAAAAJ) | [Source](https://www.cl.cam.ac.uk/~lp15/): Personal Cambridge page directly links this Scholar ID. |
| Michel X Goemans | [Scholar](https://scholar.google.com/citations?user=nf_EnbAAAAAJ) | [Source](https://www.sciencedirect.com/author/7003828844/michel-x-goemans): Existing local records identify Michel Goemans at RSA Professor of Mathematics, MIT; the web result corroborates the matching computing research identity. |
| Perry Cook | [Scholar](https://scholar.google.com/citations?user=ajVR5gEAAAAJ) | [Source](https://research.com/u/perry-r-cook): Explicit Scholar link identifies the Princeton computer-music researcher. |
| Stephen A Cook | [Scholar](https://scholar.google.com/citations?user=VGxPtzIAAAAJ) | [Source](https://dblp.org/pid/c/StephenACook.html): Existing local records identify Stephen Cook at Department of Computer Science, University of Toronto; the web result corroborates the matching computing research identity. |
| William A.S. Buxton | [Scholar](https://scholar.google.com/citations?user=yrWgTM8AAAAJ) | [Source](https://en.wikipedia.org/wiki/Bill_Buxton): Existing local records identify Bill Buxton at Microsoft Research; the web result corroborates the matching computing research identity. |
| Eric A. Brewer | [Scholar](https://scholar.google.com/citations?user=BbzYzsgAAAAJ) | [Source](https://research.google/people/ericbrewer/): Existing local records identify Eric Brewer at Google and UC Berkeley; the web result corroborates the matching computing research identity. |
| Larry Constantine | [Scholar](https://scholar.google.com/citations?user=sDomS30AAAAJ) | [Source](https://dblp.org/pid/81/6587): The matching researcher page explicitly links this Scholar profile. |
| Rodney Downey | [Scholar](https://scholar.google.com/citations?user=9xo0qlMAAAAJ) | [Source](https://research.com/u/rod-downey): The matching research biography explicitly links this Scholar profile. |
| Tao Jiang | [Scholar](https://scholar.google.com/citations?user=XUhsCZwAAAAJ) | [Source](https://www.cs.ucr.edu/~jiang/): Existing local records identify Tao Jiang 0001 at Univ. of California - Riverside; the web result corroborates the matching computing research identity. |
| Alon Yitzchak Halevy | [Scholar](https://scholar.google.com/citations?user=F_MI0pcAAAAJ) | [Source](https://www.gabormelli.com/RKB/Alon_Y._Halevy): Existing local records identify Alon Halevy at Google; the web result corroborates the matching computing research identity. |
| Arvind | [Scholar](https://scholar.google.com/citations?user=_BqpjCgAAAAJ) | [Source](https://dblp.org/pid/a/Arvind.html): DBLP's matching computing bibliography explicitly links this Scholar profile. |
| Dianne Prost OLeary | [Scholar](https://scholar.google.com/citations?user=5mXaSbgAAAAJ) | [Source](https://en.wikipedia.org/wiki/Dianne_P._O%27Leary): Existing local records identify Dianne P O'Leary at Professor of Computer Science, University of Maryland; the web result corroborates the matching computing research identity. The CSV name was later corrected to `Dianne Prost O'Leary`; see the [name corrections](#2026-09-15-1627-edt---name-corrections-and-wrong-person-scholar-link-removal). |
| Heung-Yeung Shum | [Scholar](https://scholar.google.com/citations?user=9akH-n8AAAAJ) | [Source](https://www.newx.sg/scholar/9akH-n8AAAAJ): Existing local records identify Heung-Yeung Shum at Microsoft; the web result corroborates the matching computing research identity. |
| J Strother Moore | [Scholar](https://scholar.google.com/citations?user=91fyr68AAAAJ) | [Source](https://dblp.org/pid/m/JStrotherMoore.html): The matching researcher page explicitly links this Scholar profile. |
| John E. Laird | [Scholar](https://scholar.google.com/citations?user=ea6cjVUAAAAJ) | [Source](https://dblp.org/pid/l/JohnELaird.html): Existing local records identify John Laird at Emeritus Professor of Computer Science and Engineering, University of Michigan; the web result corroborates the matching computing research identity. |
| Laura M Haas | [Scholar](https://scholar.google.com/citations?user=e9qUUSgAAAAJ) | [Source](https://dblp.org/pid/h/LauraMHaas): Existing local records identify Laura M. Haas at Univ. of Massachusetts Amherst; the web result corroborates the matching computing research identity. |
| Michael Scott | [Scholar](https://scholar.google.com/citations?user=PzaBy-UAAAAJ) | [Source](https://ftp.cs.rochester.edu/people/faculty/scott_michael/index.html): Existing local records identify Michael L. Scott at University of Rochester; the focused web result corroborates this identity. |
| Ming Li | [Scholar](https://scholar.google.com/citations?user=oGgPXFEAAAAJ) | [Source](https://uwaterloo.ca/computer-science/contacts/ming-li): Waterloo's faculty page explicitly links this Scholar ID, agreeing with the existing CSRankings record. Later superseded by the [user-selected equivalent URL](#2026-09-15-1637-edt---final-user-resolution-of-scholar-link-conflicts). |
| Nick McKeown | [Scholar](https://scholar.google.com/citations?user=SqMUez0AAAAJ) | [Source](https://yuba.stanford.edu/~nickm/students.html): Existing local records identify Nick McKeown at Stanford University; the web result corroborates the matching computing research identity. |
| Oyekunle Olukotun | [Scholar](https://scholar.google.com/citations?user=IzXDyR8AAAAJ) | [Source](https://www.cs.stanford.edu/people/oyekunle-olukotun): Stanford confirms the Oyekunle/Kunle name variant and multicore research; the indexed biography agrees with existing CSRankings and cached coauthor records on the Scholar ID. |
| Phillip B Gibbons | [Scholar](https://scholar.google.com/citations?user=F9kqUXkAAAAJ) | [Source](https://www.cs.cmu.edu/~gibbons/): Existing local records identify Phillip B. Gibbons at Carnegie Mellon University; the web result corroborates the matching computing research identity. |
| Susan T Dumais | [Scholar](https://scholar.google.com/citations?user=x8dED5cAAAAJ) | [Source](https://research.com/u/susan-dumais): Existing local records identify Susan Dumais at Technical Fellow, Microsoft Research; the web result corroborates the matching computing research identity. |
| Thomas A Henzinger | [Scholar](https://scholar.google.com/citations?user=jpgplxUAAAAJ) | [Source](https://pub.ista.ac.at/~tah/): Existing local records identify Thomas A. Henzinger at IST Austria; the web result corroborates the matching computing research identity. |
| Victor Vianu | [Scholar](https://scholar.google.com/citations?user=CK_GLC8AAAAJ) | [Source](https://dblp.dagstuhl.de/pid/v/VictorVianu.html): Existing local records identify Victor Vianu at Univ. of California - San Diego; the web result corroborates the matching computing research identity. |
| William D Gropp | [Scholar](https://scholar.google.com/citations?user=vB96fX8AAAAJ) | [Source](https://adscientificindex.com/scientist/william-gropp/1615534/): Existing local records identify William D. Gropp at Univ. of Illinois at Urbana-Champaign; the web result corroborates the matching computing research identity. |
| David M Nicol | [Scholar](https://scholar.google.com/citations?user=HIJ4KNgAAAAJ) | [Source](https://dblp.org/pid/n/DavidMNicol): Existing local records identify David Nicol at William and Mary, Dartmouth, University of Illinois; the web result corroborates the matching computing research identity. |
| Hui Zhang | [Scholar](https://scholar.google.com/citations?user=UMll0FcAAAAJ) | [Source](https://www.cs.cmu.edu/~hzhang/): Existing local records identify Hui Zhang at Carnegie Mellon University, Conviva; the focused web result corroborates this identity. |
| Keith D Cooper | [Scholar](https://scholar.google.com/citations?user=ubiUvvgAAAAJ) | [Source](https://www.wikidata.org/wiki/Q28112942): Existing local records identify Keith D. Cooper at Rice University; the web result corroborates the matching computing research identity. |
| Michael J Franklin | [Scholar](https://scholar.google.com/citations?user=p0sQC6sAAAAJ) | [Source](https://cfn.uchicago.edu/people/michael-franklin/): Existing local records identify Michael J. Franklin at University of Chicago; the web result corroborates the matching computing research identity. |
| Andrew A Chien | [Scholar](https://scholar.google.com/citations?user=zkqz0_0AAAAJ) | [Source](https://computerscience.uchicago.edu/people/andrew-a-chien/): Existing local records identify Andrew A. Chien at University of Chicago; the web result corroborates the matching computing research identity. |
| Michael D Schroeder | [Scholar](https://scholar.google.com/citations?user=mPzCK6EAAAAJ) | [Source](https://adscientificindex.com/scientist/michael-d-schroeder/4387442/): The matching research biography explicitly links this Scholar profile. |
| Vicki Hanson | [Scholar](https://scholar.google.com/citations?user=my5lwzIAAAAJ) | [Source](https://dblp.org/pid/38/3540.html): Existing local records identify Vicki L. Hanson at Rochester Inst. of Technology; the web result corroborates the matching computing research identity. |
| Brent T Hailpern | [Scholar](https://scholar.google.com/citations?user=0uJuWigAAAAJ) | [Source](https://en.wikipedia.org/wiki/Brent_Hailpern): Existing local records identify Brent Hailpern at Part-Time Instructor, Northeastern University; the web result corroborates the matching computing research identity. |
| Daniel A Reed | [Scholar](https://scholar.google.com/citations?user=YCw2r14AAAAJ) | [Source](https://www.sciencedirect.com/author/57203104388/daniel-a-reed): Existing local records identify Daniel A. Reed at University of Utah; the web result corroborates the matching computing research identity. |
| Eugene Myers | [Scholar](https://scholar.google.com/citations?user=jlas1aMAAAAJ) | [Source](https://dblp.org/pid/m/EugeneWMyers): Existing local records identify Eugene W. Myers [CBG] at Max Planck Society; the web result corroborates the matching computing research identity. |
| Mark A Horowitz | [Scholar](https://scholar.google.com/citations?user=e7V7-gEAAAAJ) | [Source](https://en.wikipedia.org/wiki/Mark_Alan_Horowitz): Existing local records identify Mark A. Horowitz at Stanford University; the web result corroborates the matching computing research identity. |
| Ramesh C Jain | [Scholar](https://scholar.google.com/citations?user=wOYUPpwAAAAJ) | [Source](https://research.com/u/ramesh-jain): The matching research biography explicitly links this Scholar profile. |
| Scott J Shenker | [Scholar](https://scholar.google.com/citations?user=hcSDlh4AAAAJ) | [Source](https://en.wikipedia.org/wiki/Scott_Shenker): Existing local records identify Scott Shenker at UC Berkeley and ICSI; the web result corroborates the matching computing research identity. |
| David H Salesin | [Scholar](https://scholar.google.com/citations?user=8E442bkAAAAJ) | [Source](https://research.google/people/107255/): Existing local records identify David Salesin at Google; the web result corroborates the matching computing research identity. |
| George Varghese | [Scholar](https://scholar.google.com/citations?user=SEnY0XQAAAAJ) | [Source](https://web.cs.ucla.edu/~varghese/bio.html): Existing local records identify George Varghese at Univ. of California - Los Angeles; the focused web result corroborates this identity. |
| Jeffrey F Naughton | [Scholar](https://scholar.google.com/citations?user=H-VmFU4AAAAJ) | [Source](https://dblp.org/pid/n/JeffreyFNaughton.html): Existing local records identify Jeffrey Naughton at Celonis; the web result corroborates the matching computing research identity. |
| Thomas G Dietterich | [Scholar](https://scholar.google.com/citations?user=09kJn28AAAAJ) | [Source](https://dblp.org/pid/d/TGDietterich.html): Existing local records identify Thomas Dietterich at Distinguished Professor (Emeritus), Computer Science, Oregon State University; the web result corroborates the matching computing research identity. |
| Barton P Miller | [Scholar](https://scholar.google.com/citations?user=dywFuRMAAAAJ) | [Source](https://adscientificindex.com/scientist/barton-miller/1878651/): Existing local records identify Barton P. Miller at University of Wisconsin - Madison; the web result corroborates the matching computing research identity. |
| David Bernard Shmoys | [Scholar](https://scholar.google.com/citations?user=rD8a4hQAAAAJ) | [Source](https://en.wikipedia.org/wiki/David_Shmoys): Existing local records identify David B. Shmoys at Cornell University; the web result corroborates the matching computing research identity. |
| David D Clark | [Scholar](https://scholar.google.com/citations?user=9s9o-JcAAAAJ) | [Source](https://www.wikidata.org/wiki/Q133639237): Existing local records identify David Clark at Senior Research Scientist, Computer Science and AI Lab, MIT; the web result corroborates the matching computing research identity. |
| Giovanni De Micheli | [Scholar](https://scholar.google.com/citations?user=7SUnVDsAAAAJ) | [Source](https://en.wikipedia.org/wiki/Giovanni_De_Micheli): Existing local records identify Giovanni De Micheli at EPFL; the web result corroborates the matching computing research identity. |
| Jeffrey C Mogul | [Scholar](https://scholar.google.com/citations?user=1pAVdtwAAAAJ) | [Source](https://research.google/people/jeffreymogul/): Existing local records identify Jeff Mogul at Google; the web result corroborates the matching computing research identity. |
| Krithivasan Ramamritham | [Scholar](https://scholar.google.com/citations?user=LFLG5pcAAAAJ) | [Source](https://iitb.irins.org/profile/42854): Existing local records identify Krithi Ramamritham at IIT Bombay; the web result corroborates the matching computing research identity. |
| Marilyn Claire Wolf | [Scholar](https://scholar.google.com/citations?user=dA88kLYAAAAJ) | [Source](https://dblp.org/pid/376/6566.html): The matching researcher page explicitly links this Scholar profile. |
| Ralf Steinmetz | [Scholar](https://scholar.google.com/citations?user=S8m0ZkkAAAAJ) | [Source](https://research.com/u/ralf-steinmetz): The matching research biography explicitly links this Scholar profile. |
| Ravinderpal S Sandhu | [Scholar](https://scholar.google.com/citations?user=wic7YpkAAAAJ) | [Source](https://www.rankless.org/authors/ravinderpal-singh-sandhu): Existing local records identify Ravi S. Sandhu at University of Texas at San Antonio; the web result corroborates the matching computing research identity. |
| Robert A Kowalski | [Scholar](https://scholar.google.com/citations?user=pvkQAj0AAAAJ) | [Source](https://www.doc.ic.ac.uk/~rak/CV.pdf): Imperial-hosted CV explicitly gives this Scholar profile for Robert Anthony Kowalski. |
| Susan B Davidson | [Scholar](https://scholar.google.com/citations?user=LW4lnZYAAAAJ) | [Source](https://dblp.org/pid/d/SBDavidson): Existing local records identify Susan B. Davidson at University of Pennsylvania; the web result corroborates the matching computing research identity. |
| Douglas E Comer | [Scholar](https://scholar.google.com/citations?user=b2f-PjYAAAAJ) | [Source](https://dblp.org/pid/c/DouglasComer.html): Existing local records identify Douglas Comer at Purdue University; the web result corroborates the matching computing research identity. |
| Henry F Korth | [Scholar](https://scholar.google.com/citations?user=4VLZdawAAAAJ) | [Source](https://dblp.org/pid/k/HenryFKorth.html): Existing local records identify Hank Korth at Lehigh University; the web result corroborates the matching computing research identity. |
| James H Morris | [Scholar](https://scholar.google.com/citations?user=Y9cRdbIAAAAJ) | [Source](https://dblp.org/pid/94/280): Existing local records identify James H. Morris at Carnegie Mellon University; the web result corroborates the matching computing research identity. |
| Randal E Bryant | [Scholar](https://scholar.google.com/citations?user=AFgYa68AAAAJ) | [Source](https://dblp.org/pid/b/REBryant): Existing local records identify Randal Bryant at Carnegie Mellon University; the web result corroborates the matching computing research identity. |
| Shahid H Bokhari | [Scholar](https://scholar.google.com/citations?user=6BV79KYAAAAJ) | [Source](https://en.wikipedia.org/wiki/Shahid_Hussain_Bokhari): Existing local records identify Shahid Bokhari at Independent Researcher, Cupertino, CA; the web result corroborates the matching computing research identity. |
| Wesley Kent Fuchs | [Scholar](https://scholar.google.com/citations?user=3AZbXzEAAAAJ) | [Source](https://en.wikipedia.org/wiki/Kent_Fuchs): Existing local records identify W. Kent Fuchs at President, University of Florida; the web result corroborates the matching computing research identity. |
| Willy E Zwaenepoel | [Scholar](https://scholar.google.com/citations?user=KfI_FL4AAAAJ) | [Source](https://www.sciencedirect.com/author/55955749000/willy-zwaenepoel): Existing local records identify Willy Zwaenepoel at University of Sydney; the web result corroborates the matching computing research identity. |
| James D Foley | [Scholar](https://scholar.google.com/citations?user=GmcChLIAAAAJ) | [Source](https://dblp.org/pid/f/JamesDFoley): Existing local records identify James Foley at Professor of Computer Science, Georgia Institute of Technology; the web result corroborates the matching computing research identity. |
| Larry M Masinter | [Scholar](https://scholar.google.com/citations?user=vwDzhiAAAAAJ) | [Source](https://dblp.org/pid/78/3899): Existing local records identify Larry Masinter at Interlisp.org; the web result corroborates the matching computing research identity. |
| Richard J Fateman | [Scholar](https://scholar.google.com/citations?user=MKANuc0AAAAJ) | [Source](https://en.wikipedia.org/wiki/Richard_Fateman): Existing local records identify Richard Fateman at Emeritus Professor of Computer Science, University of California at Berkeley; the web result corroborates the matching computing research identity. |
| Ronald L. Graham | [Scholar](https://scholar.google.com/citations?user=qrPaF3QAAAAJ) | [Source](https://dblp.org/pid/g/RLGraham.html): Existing local records identify Ronald Graham at Professor of Mathematics and Computer Science, UC San Diego; the web result corroborates the matching computing research identity. |
| Takeo Kanade | [Scholar](https://scholar.google.com/citations?user=LQ87h3sAAAAJ) | [Source](https://dblp.org/pid/k/TakeoKanade): Existing local records identify Takeo Kanade at Carnegie Mellon University; the web result corroborates the matching computing research identity. |
| David Maier | [Scholar](https://scholar.google.com/citations?user=80pKMyMAAAAJ) | [Source](https://dblp.org/pid/m/DavidMaier.html): Existing local records identify David Maier 0001 at Portland State University; the web result corroborates the matching computing research identity. |
| Howard Siegel | [Scholar](https://scholar.google.com/citations?user=C1wrYy4AAAAJ) | [Source](https://dblp.org/pid/s/HowardJaySiegel.html): Existing local records identify H.J. Siegel at the matching research profile; the web result corroborates the matching computing research identity. |
| Leon J Osterweil | [Scholar](https://scholar.google.com/citations?user=yvTXYDMAAAAJ) | [Source](https://dblp.uni-trier.de/pid/o/LJOsterweil.html): Existing local records identify Leon Osterweil at University of Massachusetts Amherst; the web result corroborates the matching computing research identity. |
| Lori Clarke | [Scholar](https://scholar.google.com/citations?user=oFiuaXEAAAAJ) | [Source](https://research.com/u/lori-clarke): The matching researcher page explicitly links this Scholar profile. |
| Richard J Cole | [Scholar](https://scholar.google.com/citations?user=p2ttvlEAAAAJ) | [Source](https://adscientificindex.com/scientist/richard-cole/834392/): Existing local records identify Richard Cole at Professor of Computer Science, Courant Institute, New York University; the web result corroborates the matching computing research identity. |
| Robert Staley Cartwright | [Scholar](https://scholar.google.com/citations?user=TtJeqqoAAAAJ) | [Source](https://dblp1.uni-trier.de/pid/c/RCartwright.html): Existing local records identify Robert Cartwright at Rice University; the web result corroborates the matching computing research identity. |
| Daniel A. Menasce | [Scholar](https://scholar.google.com/citations?user=ONloO5IAAAAJ) | [Source](https://dblp.org/pid/m/DAMenasce): DBLP's matching computing bibliography explicitly links this Scholar profile. |
| John H Reif | [Scholar](https://scholar.google.com/citations?user=Er-gEaoAAAAJ) | [Source](https://users.cs.duke.edu/~reif/): Existing local records identify John H. Reif at Duke University; the web result corroborates the matching computing research identity. |
| John L Hennessy | [Scholar](https://scholar.google.com/citations?user=tp07xT0AAAAJ) | [Source](https://citationmap.com/profile/tp07xT0AAAAJ): Existing local records identify John L. Hennessy at Stanford University; the focused web result corroborates this identity and explicitly identifies this Scholar ID, resolving the conflicting local candidate. |
| Vaughan Ronald Pratt | [Scholar](https://scholar.google.com/citations?user=Zc7l_LcAAAAJ) | [Source](https://dblp.org/pid/p/VRPratt.html): The matching researcher page explicitly links this Scholar profile. |
| Victor Basili | [Scholar](https://scholar.google.com/citations?user=B3C4aY8AAAAJ) | [Source](https://www.umiacs.umd.edu/our-experts/faculty/victor-basili): Existing local records identify V Basili at Professor Emeritus University of Maryland; the web result corroborates the matching computing research identity. |
| Abraham Silberschatz | [Scholar](https://scholar.google.com/citations?user=-YvgZDEAAAAJ) | [Source](https://s3-us-west-1.amazonaws.com/ptab-filings%2FIPR2020-01041%2F37): Existing local records identify Abraham Silberschatz at Yale University; the web result corroborates the matching computing research identity. |
| Alfred V Aho | [Scholar](https://scholar.google.com/citations?user=gb2r2ssAAAAJ) | [Source](https://dblp.org/pid/a/AVAho.html): Existing local records identify Alfred Aho at Lawrence Gussman Professor of Computer Science, Columbia University; the web result corroborates the matching computing research identity. |
| Andrew S Tanenbaum | [Scholar](https://scholar.google.com/citations?user=TvjaNqkAAAAJ) | [Source](https://www.cs.vu.nl/~ast/home/cv.pdf): Existing local records identify Andrew S. Tanenbaum at VU Amsterdam; the web result corroborates the matching computing research identity. |
| Anthony I Wasserman | [Scholar](https://scholar.google.com/citations?user=08Dlm8cAAAAJ) | [Source](https://dblp.org/pid/91/2540): The matching researcher page explicitly links this Scholar profile. |
| John A Stankovic | [Scholar](https://scholar.google.com/citations?user=4VJre9IAAAAJ) | [Source](https://research.com/u/john-stankovic): Existing local records identify Jack A. Stankovic at University of Virginia; the web result corroborates the matching computing research identity. |
| Randy H. Katz | [Scholar](https://scholar.google.com/citations?user=PkfChMgAAAAJ) | [Source](https://people.eecs.berkeley.edu/~randy/publications.html): Existing local records identify Randy Katz at University of California, Berkeley; the web result corroborates the matching computing research identity. |
| Sartaj K Sahni | [Scholar](https://scholar.google.com/citations?user=gMQWxE0AAAAJ) | [Source](https://dblp.org/pid/s/SartajSahni.html): Existing local records identify Sartaj K. Sahni at University of Florida; the web result corroborates the matching computing research identity. |
| Edward Lazowska | [Scholar](https://scholar.google.com/citations?user=NhY4TT4AAAAJ) | [Source](https://dblp.org/pid/l/EDLazowska): Existing local records identify Ed Lazowska at Bill & Melinda Gates Chair in Computer Science & Engineering, University of Washington; the web result corroborates the matching computing research identity. |
| Edwin Catmull | [Scholar](https://scholar.google.com/citations?user=qb5SK0QAAAAJ) | [Source](https://dblp.org/pid/c/EdwinECatmull): Existing local records identify Edwin Catmull at Pixar, Disney, retired; the web result corroborates the matching computing research identity. |
| Fred B Schneider | [Scholar](https://scholar.google.com/citations?user=sxjynOsAAAAJ) | [Source](https://dblp.uni-trier.de/pid/s/FredBSchneider.html): Existing local records identify Fred B. Schneider at Cornell University; the web result corroborates the matching computing research identity. |
| Grady Booch | [Scholar](https://scholar.google.com/citations?user=Y0iLlFoAAAAJ) | [Source](https://www.wikidata.org/wiki/Q92803): The matching research biography explicitly links this Scholar profile. |
| Jeffrey D Ullman | [Scholar](https://scholar.google.com/citations?user=wUJ2bXgAAAAJ) | [Source](https://dblp.org/pid/u/JeffreyDUllman.html): Existing local records identify Jeffrey Ullman at Professor of Computer Science, Stanford University; the web result corroborates the matching computing research identity. |
| Nancy Leveson | [Scholar](https://scholar.google.com/citations?user=78y4sEcAAAAJ) | [Source](https://dblp.org/pid/l/NGLeveson.html): The matching researcher page explicitly links this Scholar profile. |
| Roy F Rada | [Scholar](https://scholar.google.com/citations?user=Hvk1n1YAAAAJ) | [Source](https://encyclopedia.pub/entry/38060): Biography of UMBC information-systems researcher Roy F Rada explicitly links this Scholar ID. |
| Butler W Lampson | [Scholar](https://scholar.google.com/citations?user=9eyvm28AAAAJ) | [Source](https://dblp.org/pid/l/ButlerWLampson.html): Existing local records identify Butler Lampson at Technical Fellow, Microsoft Research; the web result corroborates the matching computing research identity. |
| C Gordon Bell | [Scholar](https://scholar.google.com/citations?user=_gzpApwAAAAJ) | [Source](https://dblp.org/pid/b/GBell): Existing local records identify C G Bell at Microsoft (ret.); the web result corroborates the matching computing research identity. |
| Dana S Scott | [Scholar](https://scholar.google.com/citations?user=oaja5KYAAAAJ) | [Source](https://adscientificindex.com/scientist/dana-scott/898012/): The matching researcher page explicitly links this Scholar profile. |
| David Joseph Gries | [Scholar](https://scholar.google.com/citations?user=Ormag-QAAAAJ) | [Source](https://dblp.org/pid/g/DavidGries): Existing local records identify David Gries at Professor Emeritus (as of 2012), Computer Science, Cornell University; the web result corroborates the matching computing research identity. |
| Ed Coffman | [Scholar](https://scholar.google.com/citations?user=Fj5sn6QAAAAJ) | [Source](https://en.wikipedia.org/wiki/Edward_G._Coffman_Jr.): Existing local records identify E. G. Coffman, Jr. at Retired; the web result corroborates the matching computing research identity. |
| John E Hopcroft | [Scholar](https://scholar.google.com/citations?user=4Z6vo5QAAAAJ) | [Source](https://dblp.org/pid/h/JohnEHopcroft.html): Existing local records identify John Hopcroft at Cornell University; the web result corroborates the matching computing research identity. |
| Joseph Traub | [Scholar](https://scholar.google.com/citations?user=b31g8hsAAAAJ) | [Source](https://dblp.org/pid/t/JFTraub.html): Existing local records identify J. F. Traub at Edwin Howard Armstrong Professor of Computer Science, Columbia University; the web result corroborates the matching computing research identity. |
| Paul R McJones | [Scholar](https://scholar.google.com/citations?user=cca4DoCsQjAJ) | [Source](https://www.researchgate.net/profile/Paul-Mcjones): Existing local records identify Paul McJones at Retired; the web result corroborates the matching computing research identity. |
| Peter J Denning | [Scholar](https://scholar.google.com/citations?user=bfs3-ZoAAAAJ) | [Source](https://dblp.org/pid/d/PJDenning.html): The matching researcher page explicitly links this Scholar profile. |
| Robert E Tarjan | [Scholar](https://scholar.google.com/citations?user=lazJixIAAAAJ) | [Source](https://collaborate.princeton.edu/en/persons/robert-endre-tarjan/): Existing local records identify Robert E. Tarjan at Princeton University; the web result corroborates the matching computing research identity. |
| Ronald M Kaplan | [Scholar](https://scholar.google.com/citations?user=HaahwTYAAAAJ) | [Source](https://www.researchgate.net/profile/Ronald-Kaplan): Existing local records identify Ronald Kaplan at Stanford University; the web result corroborates the matching computing research identity. |

### 2026-09-15 13:49 EDT - Unresolved Entries

The following 355 entries were blank at the end of this review.
Hoare's later removal raised the blank count to 356; see the [18:21 EDT resolutions](#2026-09-15-1821-edt---user-resolution-of-shared-recipient-scholar-links).
Unless a more specific reason is recorded below, the searches did not establish a sufficiently supported exact Scholar profile ID for the Fellow.
Bibliographies, article-search links, and similar-name profiles were insufficient on their own.
This does not establish that no Scholar profile exists.

| ACM Fellow | Outcome |
| --- | --- |
| Athina Markopoulou | No sufficiently supported matching profile ID established. |
| Eric Allman | No sufficiently supported matching profile ID established. |
| Nandita Dukkipati | No sufficiently supported matching profile ID established. |
| Anwar Walid | No sufficiently supported matching profile ID established. |
| Azad M Madni | No sufficiently supported matching profile ID established. |
| Russell Housley | No sufficiently supported matching profile ID established. |
| Stephen David Crocker | No sufficiently supported matching profile ID established. |
| Ian Goldberg | No sufficiently supported matching profile ID established. |
| Manik Varma | No sufficiently supported matching profile ID established. |
| Tim Berners-Lee | No sufficiently supported matching profile ID established. |
| Leonard M. Adleman | No sufficiently supported matching profile ID established. |
| Thomas Lengauer | No sufficiently supported matching profile ID established. |
| Manuel Blum | The available local candidates could not be independently established as the computer scientist. |
| Martin Hellman | No sufficiently supported matching profile ID established. |
| Whitfield Diffie | No sufficiently supported matching profile ID established. |
| Andreas Reuter | No sufficiently supported matching profile ID established. |
| Elena Ferrari | No sufficiently supported matching profile ID established. |
| Mona Singh | The previously rejected consultant profile was not reused; no sufficiently supported replacement was established. |
| Peter W Shor | No sufficiently supported matching profile ID established. |
| Avi Wigderson | No sufficiently supported matching profile ID established. |
| Charles Lee Isbell Jr | No sufficiently supported matching profile ID established. |
| Gurudatta Parulkar | No sufficiently supported matching profile ID established. |
| Tom Leighton | No sufficiently supported matching profile ID established. |
| Toniann Pitassi | No sufficiently supported matching profile ID established. |
| Clifford A Lynch | No sufficiently supported matching profile ID established. |
| Michael Sipser | No sufficiently supported matching profile ID established. |
| Silvio Micali | No sufficiently supported matching profile ID established. |
| Steven Michael Hand | No sufficiently supported matching profile ID established. |
| K. Rustan M. Leino | No sufficiently supported matching profile ID established. |
| Radia Perlman | No sufficiently supported matching profile ID established. |
| Ravi Kannan | No sufficiently supported matching profile ID established. |
| Ricardo Bianchini | No sufficiently supported matching profile ID established. |
| Kevin Fall | No sufficiently supported matching profile ID established. |
| Michael Franz | No sufficiently supported matching profile ID established. |
| Ramanathan Guha | No sufficiently supported matching profile ID established. |
| Charles W Bachman | No sufficiently supported matching profile ID established. |
| Faith Ellen | No sufficiently supported matching profile ID established. |
| Chip Elliott | No sufficiently supported matching profile ID established. |
| David J Kasik | No sufficiently supported matching profile ID established. |
| James Gosling | No sufficiently supported matching profile ID established. |
| S E Robertson | Stephen Robertson identity was found, but no sufficiently supported exact Scholar ID was established. |
| Alistair Sinclair | No sufficiently supported matching profile ID established. |
| John Hershberger | No sufficiently supported matching profile ID established. |
| Jonathan Grudin | No sufficiently supported matching profile ID established. |
| Masaru Kitsuregawa | No sufficiently supported matching profile ID established. |
| Steven Scott | The explicit ID in the search results belongs to Craig R. Scott, not the Cray computer architect. |
| Amit Singhal | No sufficiently supported matching profile ID established. |
| Carl Ebeling | No sufficiently supported matching profile ID established. |
| David K Gifford | No sufficiently supported matching profile ID established. |
| Frank Kenneth Zadeck | No sufficiently supported matching profile ID established. |
| John Sanguinetti | No sufficiently supported matching profile ID established. |
| Peter Magnusson | No sufficiently supported matching profile ID established. |
| Carla S. Ellis | No sufficiently supported matching profile ID established. |
| David A Abramson | No sufficiently supported matching profile ID established. |
| Donald Kossmann | No sufficiently supported matching profile ID established. |
| Luiz Andre Barroso | No sufficiently supported matching profile ID established. |
| Robert B Schnabel | No sufficiently supported matching profile ID established. |
| Ron Cytron | No sufficiently supported matching profile ID established. |
| Stephen Trimberger | No sufficiently supported matching profile ID established. |
| Farnam Jahanian | No sufficiently supported matching profile ID established. |
| Gerhard Fischer | No sufficiently supported matching profile ID established. |
| Nell B. Dale | No sufficiently supported matching profile ID established. |
| Patricia G. Selinger | No sufficiently supported matching profile ID established. |
| Terry Winograd | No sufficiently supported matching profile ID established. |
| Vijay P Bhatkar | No sufficiently supported matching profile ID established. |
| Alan Kay | No sufficiently supported matching profile ID established. |
| Charles H House | No sufficiently supported matching profile ID established. |
| Joel Moses | No sufficiently supported matching profile ID established. |
| Mendel Rosenblum | No sufficiently supported matching profile ID established. |
| Paul G Lowney | No sufficiently supported matching profile ID established. |
| Umeshwar Dayal | No sufficiently supported matching profile ID established. |
| Watts S. Humphrey | No sufficiently supported matching profile ID established. |
| Amir Pnueli | No sufficiently supported matching profile ID established. |
| Aristides Requicha | No sufficiently supported matching profile ID established. |
| Catriel Beeri | No sufficiently supported matching profile ID established. |
| Donald E Thomas | No sufficiently supported matching profile ID established. |
| Edward A Feigenbaum | No sufficiently supported matching profile ID established. |
| Eric S Roberts | No sufficiently supported matching profile ID established. |
| John C Klensin | No sufficiently supported matching profile ID established. |
| Rajeev Motwani | No sufficiently supported matching profile ID established. |
| Randy Pausch | No sufficiently supported matching profile ID established. |
| Utpal Banerjee | No sufficiently supported matching profile ID established. |
| Alan Newell | The Dundee accessibility researcher was distinguished from Allen Newell and other namesakes; no exact matching ID was established. |
| Albert G Greenberg | No sufficiently supported matching profile ID established. |
| Alfred Z Spector | No sufficiently supported matching profile ID established. |
| Anthony C Hearn | No sufficiently supported matching profile ID established. |
| Bryant W York | No sufficiently supported matching profile ID established. |
| Dan R Olsen | No sufficiently supported matching profile ID established. |
| Peter Norvig | No sufficiently supported matching profile ID established. |
| Usama M Fayyad | No sufficiently supported matching profile ID established. |
| Michel Dubois | No sufficiently supported matching profile ID established. |
| Rodney A Brooks | No sufficiently supported matching profile ID established. |
| Stephen Bourne | No sufficiently supported matching profile ID established. |
| Umesh Vazirani | The IIT Delhi listing supplies Vijay Vazirani’s ID despite naming Umesh; this conflicting candidate was excluded. |
| David S Wise | No sufficiently supported matching profile ID established. |
| George E. Collins | No sufficiently supported matching profile ID established. |
| Janis A Bubenko | No sufficiently supported matching profile ID established. |
| Paul Mockapetris | No sufficiently supported matching profile ID established. |
| Peter Lee | No sufficiently supported matching profile ID established. |
| Richard Schantz | No sufficiently supported matching profile ID established. |
| Stamatis Vassiliadis | No sufficiently supported matching profile ID established. |
| Barbara J Grosz | No sufficiently supported matching profile ID established. |
| C J Van Rijsbergen | No sufficiently supported matching profile ID established. |
| Gurindar S Sohi | No sufficiently supported matching profile ID established. |
| Mary Harrold | No sufficiently supported matching profile ID established. |
| Richard DeMillo | Two conflicting local IDs remain unresolved after web identity checks. |
| Ambuj Goyal | No sufficiently supported matching profile ID established. |
| Bantwal R Rau | No sufficiently supported matching profile ID established. |
| David B Lomet | No sufficiently supported matching profile ID established. |
| Harold N Gabow | No sufficiently supported matching profile ID established. |
| Sidney Karin | No sufficiently supported matching profile ID established. |
| Vishwani D Agrawal | No sufficiently supported matching profile ID established. |
| Alan H Borning | No sufficiently supported matching profile ID established. |
| Alan Smith | No sufficiently supported matching profile ID established. |
| Cherri M Pancake | No sufficiently supported matching profile ID established. |
| David J. Farber | No sufficiently supported matching profile ID established. |
| Domenico Ferrari | No sufficiently supported matching profile ID established. |
| Donn B Parker | No sufficiently supported matching profile ID established. |
| George Robertson | No sufficiently supported matching profile ID established. |
| Ira Pohl | No sufficiently supported matching profile ID established. |
| Joel S Birnbaum | No sufficiently supported matching profile ID established. |
| John C Reynolds | No sufficiently supported matching profile ID established. |
| Joseph F Jaja | No sufficiently supported matching profile ID established. |
| Ravishankar Iyer | No sufficiently supported matching profile ID established. |
| Richard B Kieburtz | No sufficiently supported matching profile ID established. |
| Richard D Schlichting | No sufficiently supported matching profile ID established. |
| Robert Aiken | No sufficiently supported matching profile ID established. |
| Robert E Kahn | No sufficiently supported matching profile ID established. |
| Sally J Floyd | No sufficiently supported matching profile ID established. |
| Yuri Breitbart | No sufficiently supported matching profile ID established. |
| Alan W Biermann | No sufficiently supported matching profile ID established. |
| Albert R Meyer | No sufficiently supported matching profile ID established. |
| Donald J Haderle | No sufficiently supported matching profile ID established. |
| Donald W Loveland | No sufficiently supported matching profile ID established. |
| Karen Duncan | No sufficiently supported matching profile ID established. |
| Laxminarayan Bhuyan | No sufficiently supported matching profile ID established. |
| Leonard Kleinrock | No sufficiently supported matching profile ID established. |
| Raymond A Lorie | The surfaced Agora ID belongs to Raymond A. Yeh, not Raymond A. Lorie. |
| Akinori Yonezawa | No sufficiently supported matching profile ID established. |
| C. Dianne Martin | No sufficiently supported matching profile ID established. |
| Charles M Geschke | No sufficiently supported matching profile ID established. |
| Chung Jen Tan | No sufficiently supported matching profile ID established. |
| David L Mills | No sufficiently supported matching profile ID established. |
| David L Waltz | No sufficiently supported matching profile ID established. |
| John D Gannon | No sufficiently supported matching profile ID established. |
| John Warnock | No sufficiently supported matching profile ID established. |
| Joseph S DeBlasi | No sufficiently supported matching profile ID established. |
| Koji Torii | No sufficiently supported matching profile ID established. |
| Marc Auslander | No sufficiently supported matching profile ID established. |
| Philip M Lewis | The surfaced Scholar-linked profile belongs to a Monash medical researcher, not the Stony Brook computer scientist. |
| Rob Cook | No sufficiently supported matching profile ID established. |
| Robert L Glass | No sufficiently supported matching profile ID established. |
| Robert T Braden | No sufficiently supported matching profile ID established. |
| Toshihide Ibaraki | No sufficiently supported matching profile ID established. |
| Abraham Kandel | No sufficiently supported matching profile ID established. |
| Albert J Turner | No sufficiently supported matching profile ID established. |
| Aravind K Joshi | No sufficiently supported matching profile ID established. |
| Barbara Gershon Ryder | No sufficiently supported matching profile ID established. |
| Carlo H Sequin | No sufficiently supported matching profile ID established. |
| Clarence A Ellis | No sufficiently supported matching profile ID established. |
| David S Notkin | No sufficiently supported matching profile ID established. |
| Dharma P Agrawal | No sufficiently supported matching profile ID established. |
| Emmerich Welzl | No sufficiently supported matching profile ID established. |
| Gopal Krishna Gupta | The surfaced UT Dallas Gopal Gupta profile was not established as ACM Fellow Gopal Krishna Gupta. |
| Hal Berghel | No sufficiently supported matching profile ID established. |
| James C Browne | No sufficiently supported matching profile ID established. |
| James Jay Horning | No sufficiently supported matching profile ID established. |
| Neil Jones | The local Neil Jones ID has no affiliation and was not independently matched to Neil D. Jones of Copenhagen. |
| Peter P Chen | No sufficiently supported matching profile ID established. |
| Richard Gabriel | No sufficiently supported matching profile ID established. |
| Simon S Lam | No sufficiently supported matching profile ID established. |
| Stephen T Kent | No sufficiently supported matching profile ID established. |
| Susan H. Nycum | No sufficiently supported matching profile ID established. |
| Venkat Rangan | No sufficiently supported matching profile ID established. |
| Alan C Shaw | No sufficiently supported matching profile ID established. |
| H W Lawson | No sufficiently supported matching profile ID established. |
| Herbert Freeman | No sufficiently supported matching profile ID established. |
| Irene Greif | No sufficiently supported matching profile ID established. |
| J D Couger | No sufficiently supported matching profile ID established. |
| Jean-Loup E Baer | No sufficiently supported matching profile ID established. |
| Kenneth C Sevcik | No sufficiently supported matching profile ID established. |
| Kenneth Steiglitz | No sufficiently supported matching profile ID established. |
| Paolo Zanella | No sufficiently supported matching profile ID established. |
| Paul Schneck | No sufficiently supported matching profile ID established. |
| Peter Widmayer | No sufficiently supported matching profile ID established. |
| Raymond Miller | No sufficiently supported matching profile ID established. |
| Raymond Reiter | No sufficiently supported matching profile ID established. |
| Richard A. Kemmerer | No sufficiently supported matching profile ID established. |
| Richard Lipton | No sufficiently supported matching profile ID established. |
| Robert Wilensky | No sufficiently supported matching profile ID established. |
| Roger R Bate | No sufficiently supported matching profile ID established. |
| Zvi Kedem | No sufficiently supported matching profile ID established. |
| Anita Borg | No sufficiently supported matching profile ID established. |
| Anita K Jones | No sufficiently supported matching profile ID established. |
| Arnold Rosenberg | No sufficiently supported matching profile ID established. |
| B. Chandrasekaran | No sufficiently supported matching profile ID established. |
| Barbara Liskov | No sufficiently supported matching profile ID established. |
| Bryan Preas | No sufficiently supported matching profile ID established. |
| Fred W Weingarten | No sufficiently supported matching profile ID established. |
| George Dodd | No sufficiently supported matching profile ID established. |
| Jeanne Ferrante | No sufficiently supported matching profile ID established. |
| Jeffrey Jaffe | No sufficiently supported matching profile ID established. |
| John E Savage | No sufficiently supported matching profile ID established. |
| John Rice | No sufficiently supported matching profile ID established. |
| Jose L. Encarnacao | No sufficiently supported matching profile ID established. |
| Kurt B Akeley | No sufficiently supported matching profile ID established. |
| Larry Stockmeyer | No sufficiently supported matching profile ID established. |
| Lawrence H Landweber | No sufficiently supported matching profile ID established. |
| Maria Klawe | No sufficiently supported matching profile ID established. |
| Marshall C Yovits | No sufficiently supported matching profile ID established. |
| Mary K Vernon | No sufficiently supported matching profile ID established. |
| Michael A Harrison | No sufficiently supported matching profile ID established. |
| Michael E Lesk | No sufficiently supported matching profile ID established. |
| Michael J Fischer | Two conflicting local IDs remain unresolved; the exact linked destination could not be retrieved from the bibliography. |
| Richard E Nance | No sufficiently supported matching profile ID established. |
| Robert M Graham | No sufficiently supported matching profile ID established. |
| TRN Rao | No sufficiently supported matching profile ID established. |
| William Richards Adrion | No sufficiently supported matching profile ID established. |
| Alan H Barr | No sufficiently supported matching profile ID established. |
| Andrew C Yao | No sufficiently supported matching profile ID established. |
| Anthony Oettinger | No sufficiently supported matching profile ID established. |
| Bertram Herzog | No sufficiently supported matching profile ID established. |
| Chak-Kuen Wong | No sufficiently supported matching profile ID established. |
| David H Brandin | No sufficiently supported matching profile ID established. |
| Donald Greenberg | No sufficiently supported matching profile ID established. |
| Dorothy E Denning | No sufficiently supported matching profile ID established. |
| Erwin Engeler | No sufficiently supported matching profile ID established. |
| Franco P Preparata | No sufficiently supported matching profile ID established. |
| Harold J Highland | No sufficiently supported matching profile ID established. |
| Herbert R J Grosch | No sufficiently supported matching profile ID established. |
| J Nievergelt | No sufficiently supported matching profile ID established. |
| J Turner Whitted | No sufficiently supported matching profile ID established. |
| John B Goodenough | The local ID belongs to the UT Austin battery scientist, not the ACM Fellow in software engineering. |
| John R. White | No sufficiently supported matching profile ID established. |
| Kenneth W Kennedy | No sufficiently supported matching profile ID established. |
| Larry Druffel | No sufficiently supported matching profile ID established. |
| Larry Snyder | No sufficiently supported matching profile ID established. |
| Lawrence Bernstein | No sufficiently supported matching profile ID established. |
| Loren C Carpenter | No sufficiently supported matching profile ID established. |
| Myron Ginsberg | No sufficiently supported matching profile ID established. |
| Norihisa Suzuki | No sufficiently supported matching profile ID established. |
| Oscar Ibarra | No sufficiently supported matching profile ID established. |
| Paul W Abrahams | No sufficiently supported matching profile ID established. |
| Paul Young | No sufficiently supported matching profile ID established. |
| Peter Wegner | No sufficiently supported matching profile ID established. |
| R L Ashenhurst | No sufficiently supported matching profile ID established. |
| Robert Constable | No sufficiently supported matching profile ID established. |
| Sambasiva Kosaraju | No sufficiently supported matching profile ID established. |
| Stuart Feldman | No sufficiently supported matching profile ID established. |
| Won Kim | No sufficiently supported matching profile ID established. |
| A J Milner | No sufficiently supported matching profile ID established. |
| Aaron Finerman | No sufficiently supported matching profile ID established. |
| Adele Goldberg | The Princeton psychologist’s ID was excluded; no matching Smalltalk researcher profile was established. |
| Allen Tucker | No sufficiently supported matching profile ID established. |
| Andries van Dam | No sufficiently supported matching profile ID established. |
| Anthony Ralston | No sufficiently supported matching profile ID established. |
| Azriel Rosenfeld | No sufficiently supported matching profile ID established. |
| Barbara B Simons | No sufficiently supported matching profile ID established. |
| Ben Wegbreit | No sufficiently supported matching profile ID established. |
| Bernard A Galler | No sufficiently supported matching profile ID established. |
| Bob O Evans | No sufficiently supported matching profile ID established. |
| Bruce Lindsay | No sufficiently supported matching profile ID established. |
| Burton Smith | No sufficiently supported matching profile ID established. |
| C.L. Liu | No sufficiently supported matching profile ID established. |
| Calvin C. Gotlieb | No sufficiently supported matching profile ID established. |
| Carl Hammer | No sufficiently supported matching profile ID established. |
| Charles L. Bradshaw | No sufficiently supported matching profile ID established. |
| Charles P. Thacker | No sufficiently supported matching profile ID established. |
| Charles W. Gear | No sufficiently supported matching profile ID established. |
| Cordell Green | No sufficiently supported matching profile ID established. |
| Daniel D McCracken | No sufficiently supported matching profile ID established. |
| Daniel S. Bricklin | No sufficiently supported matching profile ID established. |
| David J. Kuck | No sufficiently supported matching profile ID established. |
| David John Wheeler | No sufficiently supported matching profile ID established. |
| David R. Boggs | No sufficiently supported matching profile ID established. |
| Donald Chamberlin | No sufficiently supported matching profile ID established. |
| Donald R Slutz | No sufficiently supported matching profile ID established. |
| Douglas K Brotz | No sufficiently supported matching profile ID established. |
| Edgar F. Codd | No sufficiently supported matching profile ID established. |
| Edsger W. Dijkstra | No sufficiently supported matching profile ID established. |
| Edward A Taft | No sufficiently supported matching profile ID established. |
| Edward McCluskey | No sufficiently supported matching profile ID established. |
| Eric A Weiss | No sufficiently supported matching profile ID established. |
| Fernando Corbato | No sufficiently supported matching profile ID established. |
| Frances Allen | No sufficiently supported matching profile ID established. |
| Frank Friedman | No sufficiently supported matching profile ID established. |
| Franz L. Alt | No sufficiently supported matching profile ID established. |
| Fred H Harris | No sufficiently supported matching profile ID established. |
| Gerald L Engel | No sufficiently supported matching profile ID established. |
| GERALD SUSSMAN | No sufficiently supported matching profile ID established. |
| Harry D. Huskey | No sufficiently supported matching profile ID established. |
| Harvey G. Cragon | No sufficiently supported matching profile ID established. |
| Herbert A. Simon | No sufficiently supported matching profile ID established. |
| Herbert Maisel | No sufficiently supported matching profile ID established. |
| Irv Traiger | No sufficiently supported matching profile ID established. |
| Ivan Sutherland | No sufficiently supported matching profile ID established. |
| J Presper Eckert | No sufficiently supported matching profile ID established. |
| J.N. Hume | No sufficiently supported matching profile ID established. |
| Jack Dennis | No sufficiently supported matching profile ID established. |
| Jack Minker | No sufficiently supported matching profile ID established. |
| James M. Adams | No sufficiently supported matching profile ID established. |
| Jean E Sammet | No sufficiently supported matching profile ID established. |
| Jeff Rulifson | No sufficiently supported matching profile ID established. |
| John A.N. Lee | No sufficiently supported matching profile ID established. |
| John H Esbin | No sufficiently supported matching profile ID established. |
| Joshua Lederberg | No sufficiently supported matching profile ID established. |
| Joyce Currie Little | No sufficiently supported matching profile ID established. |
| Juris Hartmanis | No sufficiently supported matching profile ID established. |
| Kenneth E Batcher | No sufficiently supported matching profile ID established. |
| L. Peter Deutsch | No sufficiently supported matching profile ID established. |
| Lorraine Borman | No sufficiently supported matching profile ID established. |
| M. Stuart Lynn | No sufficiently supported matching profile ID established. |
| Martha Sloan | No sufficiently supported matching profile ID established. |
| Maurice V. Wilkes | No sufficiently supported matching profile ID established. |
| Meir Lehman | No sufficiently supported matching profile ID established. |
| Michael J Flynn | No sufficiently supported matching profile ID established. |
| Michael Stonebraker | No sufficiently supported matching profile ID established. |
| Michael W Blasgen | No sufficiently supported matching profile ID established. |
| Monroe Newborn | No sufficiently supported matching profile ID established. |
| Niklaus E. Wirth | No sufficiently supported matching profile ID established. |
| Patrick Suppes | No sufficiently supported matching profile ID established. |
| Peter Elias | The Lagos geographer’s ID was excluded; no matching MIT information-theory researcher profile was established. |
| Peter G Neumann | No sufficiently supported matching profile ID established. |
| Ray Kurzweil | No sufficiently supported matching profile ID established. |
| Richard E Stearns | No sufficiently supported matching profile ID established. |
| Richard G Canning | No sufficiently supported matching profile ID established. |
| Richard H. Austing | No sufficiently supported matching profile ID established. |
| Richard R. Burton | No sufficiently supported matching profile ID established. |
| Richard W. Hamming | No sufficiently supported matching profile ID established. |
| Robert M Frankston | No sufficiently supported matching profile ID established. |
| Robert W Taylor | No sufficiently supported matching profile ID established. |
| Robert W. Floyd | No sufficiently supported matching profile ID established. |
| Roger M Needham | No sufficiently supported matching profile ID established. |
| Seymour J. Wolfson | No sufficiently supported matching profile ID established. |
| Shmuel Winograd | No sufficiently supported matching profile ID established. |
| Stephen Dunwell | No sufficiently supported matching profile ID established. |
| Stephen S Lavenberg | No sufficiently supported matching profile ID established. |
| Stuart Wecker | No sufficiently supported matching profile ID established. |
| Susan L Graham | No sufficiently supported matching profile ID established. |
| Thomas A D'Auria | No sufficiently supported matching profile ID established. |
| Thomas B. Steel, Jr. | No sufficiently supported matching profile ID established. |
| Thomas DeFanti | No sufficiently supported matching profile ID established. |
| Thomas E. Kurtz | No sufficiently supported matching profile ID established. |
| Tom Hull | No sufficiently supported matching profile ID established. |
| Tse-Yun Feng | No sufficiently supported matching profile ID established. |
| Vinton Cerf | No sufficiently supported matching profile ID established. |
| Walter Carlson | No sufficiently supported matching profile ID established. |
| William A Wulf | No sufficiently supported matching profile ID established. |
| William B Poucher | No sufficiently supported matching profile ID established. |
| William Daniel Hillis | No sufficiently supported matching profile ID established. |
| William F. Atchison | No sufficiently supported matching profile ID established. |
| William Kahan | No sufficiently supported matching profile ID established. |
| William Strecker | No sufficiently supported matching profile ID established. |
| Willis H Ware | No sufficiently supported matching profile ID established. |
| Zohar Manna | No sufficiently supported matching profile ID established. |

## 2026-09-15 10:31 EDT - Google Scholar Links: Eighth Web Search Batch

This bounded batch checked the next 100 missing entries in CSV order, skipping the 21 unresolved entries from earlier batches.
The batch contained 16 from 2020, 18 from 2019, 19 from 2018, 12 from 2017, 12 from 2016, 11 from 2015, 9 from 2014, 3 from 2013.
General web search, corroborated where needed by existing CSRankings and cached Scholar records, established 73 clear matches.
The links below were added, bringing the dataset to 1,116 nonempty Scholar links and 522 blank Scholar cells across 1,638 Fellows.
Only the 73 previously blank Scholar URL cells changed; names and other CSV fields were preserved.
No computer-use tools or project crawlers were used, and no caches, Scholar profile exports, or visualizations were regenerated.
These checks establish identity and link correspondence; they are not fresh audits of Scholar publication lists or metrics.
Existing CSRankings records are from `../bigcows-crawler/.cache/csrankings/csrankings-*.csv`, and cached profile and coauthor evidence is from `../bigcows-crawler/.cache/google-scholar-profile-cache.json`.
Where Scholar access returned an error, an explicit profile link from the cited source established the URL; an access error was not treated as evidence that the profile did not exist.
Three additions replace links removed during the earlier wrong-person audit: Kun Zhou, Xiangyang Li, and Valerie Taylor.
The earlier removal records remain below to prevent those incorrect IDs from being reintroduced.
Jason Nieh's personal homepage resolved the conflicting local IDs, and explicit web links corroborated the cached coauthor IDs for Geoffrey Voelker and Daniel Jackson over their different CSRankings candidates.
Salvatore Stolfo's personal homepage explicitly prints the selected ID, while another search result supplies a different one.
John Hughes's conference profile explicitly connects his selected ID with Chalmers, functional programming, and software testing.

| ACM Fellow | Added Scholar Profile | Source and Identity Evidence |
| --- | --- | --- |
| Kenneth Lane Thompson | [Scholar](https://scholar.google.com/citations?user=FsHMg9AAAAAJ) | [Source](https://adscientificindex.com/scientist/ken-thompson/4378746/): Existing cached profile identifies Ken Thompson at Google and contains UNIX work with Dennis Ritchie, matching the web result and the Fellow's operating-systems citation. |
| Kun Zhou | [Scholar](https://scholar.google.com/citations?user=N-iYby0AAAAJ) | [Source](https://www.newx.sg/scholar/N-iYby0AAAAJ): Exact ID identifies the Zhejiang computer-graphics researcher and agrees with existing CSRankings and coauthor records. |
| Laurie Ann Williams | [Scholar](https://scholar.google.com/citations?user=Cln2viUAAAAJ) | [Source](https://dblp.org/pid/w/LaurieAWilliams.html): The NCSU software-engineering identity agrees with the Laurie Williams aliases and exact ID in existing CSRankings and coauthor records. |
| Matthew A Turk | [Scholar](https://scholar.google.com/citations?user=KltleWgAAAAJ) | [Source](https://sites.cs.ucsb.edu/~mturk/): The UCSB computer-vision researcher and former TTIC president matches the Matthew A. Turk entry in existing CSRankings. |
| Michael J Zyda | [Scholar](https://scholar.google.com/citations?user=qPWq9YwAAAAJ) | [Source](https://research.com/u/michael-zyda): Explicit Scholar link identifies the USC games and virtual-environments researcher. |
| Michael O. Rabin | [Scholar](https://scholar.google.com/citations?user=EFZyUcEAAAAJ) | [Source](https://research.google/programs-and-events/visiting-researcher-program/michael-o-rabin/): The theoretical computer scientist matches the Harvard Michael O. Rabin aliases and profile ID in existing CSRankings. Later standardized to the user's selected equivalent URL in the [18:21 EDT resolutions](#2026-09-15-1821-edt---user-resolution-of-shared-recipient-scholar-links). |
| Peter Stone | [Scholar](https://scholar.google.com/citations?user=qnwjcfAAAAAJ) | [Source](https://www.cs.utexas.edu/people/faculty-researchers/peter-stone): UT Austin AI and robotics identity matches existing CSRankings and coauthor records. |
| Sanjit Arunkumar Seshia | [Scholar](https://scholar.google.com/citations?user=SlZavnIAAAAJ) | [Source](https://vcresearch.berkeley.edu/faculty/sanjit-seshia): Berkeley formal-methods identity matches existing CSRankings and coauthor records. |
| Susanne E Hambrusch | [Scholar](https://scholar.google.com/citations?user=5k0KS3UAAAAJ) | [Source](https://dblp.org/pid/h/SusanneSHambrusch): Bibliography identifies the Purdue computing researcher, matching the cached coauthor name, affiliation and ID. |
| Wang Yi | [Scholar](https://scholar.google.com/citations?user=_ynjrUUAAAAJ) | [Source](https://www.newx.sg/scholar/_ynjrUUAAAAJ): Exact ID identifies the Uppsala real-time and embedded-systems researcher and agrees with existing local records. |
| Wei Wang | [Scholar](https://scholar.google.com/citations?user=UedS9LQAAAAJ) | [Source](https://web.cs.ucla.edu/~weiwang/): Personal UCLA homepage directly links this ID for the data-mining researcher. |
| Wil Van Der Aalst | [Scholar](https://scholar.google.com/citations?user=aSZYyxIAAAAJ) | [Source](https://www.vdaalst.rwth-aachen.de/): RWTH process-mining identity matches the Wil van der Aalst ID in existing CSRankings. |
| Yao-Wen Chang | [Scholar](https://scholar.google.com/citations?user=qKJ_7jAAAAAJ) | [Source](https://cc.ee.ntu.edu.tw/~ywchang/): Personal NTU electrical-engineering homepage directly links this ID under Google Citations. |
| Bradley G Calder | [Scholar](https://scholar.google.com/citations?user=ToaGb5YAAAAJ) | [Source](https://www.alphaxiv.org/@brad-calder): Explicit Scholar link identifies Brad Calder and the Google Cloud and UCSD systems research record. |
| Carlo A Zaniolo | [Scholar](https://scholar.google.com/citations?user=f8FjAtMAAAAJ) | [Source](https://research.com/u/carlo-zaniolo): Explicit Scholar link identifies the UCLA database researcher. |
| Elizabeth Frances Churchill | [Scholar](https://scholar.google.com/citations?user=wZB07xAAAAAJ) | [Source](https://mbzuai.ac.ae/academics/faculty-directory/elizabeth-churchill): MBZUAI HCI identity agrees with existing CSRankings and the cached Google coauthor record. |
| Emery David Berger | [Scholar](https://scholar.google.com/citations?user=RaHaArkAAAAJ) | [Source](https://people.cs.umass.edu/~emery/vita.pdf): UMass software-systems research record agrees with the cached Emery D. Berger coauthor ID. |
| Jason Nieh | [Scholar](https://scholar.google.com/citations?user=e84VgEYAAAAJ) | [Source](https://www.cs.columbia.edu/~nieh/): Personal Columbia homepage directly links this ID, resolving the conflict with the different ID in existing CSRankings. |
| Kanianthra Mani Chandy | [Scholar](https://scholar.google.com/citations?user=_e1E9DQAAAAJ) | [Source](https://research.com/u/k-mani-chandy): Explicit Scholar link identifies K Mani Chandy at Caltech and distributed-systems publications. |
| Maria L Gini | [Scholar](https://scholar.google.com/citations?user=2ewb-10AAAAJ) | [Source](https://cse.umn.edu/cs/maria-gini): Minnesota robotics and AI identity matches existing CSRankings. |
| Matthew B Dwyer | [Scholar](https://scholar.google.com/citations?user=-ZRKCcEAAAAJ) | [Source](https://engineering.virginia.edu/faculty/matthew-b-dwyer): Virginia software-verification identity matches existing CSRankings and coauthor records. |
| Moustafa A Youssef | [Scholar](https://scholar.google.com/citations?user=r6DUyxsAAAAJ) | [Source](https://www.aucegypt.edu/fac/moustafa-youssef): AUC faculty page directly links this ID and identifies the wireless-systems ACM Fellow. |
| Nisheeth Vishnoi | [Scholar](https://scholar.google.com/citations?user=7b5tlJkAAAAJ) | [Source](https://www.cs.yale.edu/homes/vishnoi/Home.html): Yale algorithms researcher matches the Nisheeth K. Vishnoi entry in existing CSRankings. |
| Ramesh Kumar Sitaraman | [Scholar](https://scholar.google.com/citations?user=Hj4o7GYAAAAJ) | [Source](https://www.cics.umass.edu/about/directory/ramesh-sitaraman): UMass networks and distributed-systems identity matches existing CSRankings. |
| Salvatore J Stolfo | [Scholar](https://scholar.google.com/citations?user=DknsgF8AAAAJ) | [Source](https://www.cs.columbia.edu/~sal/index.html): Personal Columbia page explicitly prints this Scholar URL, resolving a different ID returned by another search result. |
| Timothy Chan | [Scholar](https://scholar.google.com/citations?user=CiesWGcAAAAJ) | [Source](https://tmc.web.engr.illinois.edu/pub.html): Illinois algorithms and computational-geometry publications match the Timothy M. Chan entry in existing CSRankings. |
| Xiangyang Li | [Scholar](https://scholar.google.com/citations?user=JURtNb0AAAAJ) | [Source](https://en.ustc.edu.cn/info/1007/1189.htm): USTC's ACM Fellow announcement identifies IoT and mobile-systems work, matching existing CSRankings and coauthor records. |
| Amy S Bruckman | [Scholar](https://scholar.google.com/citations?user=IdWa_JkAAAAJ) | [Source](https://www.cc.gatech.edu/fac/Amy.Bruckman/): Georgia Tech HCI identity matches existing CSRankings and coauthor records; the web results also expose the same exact Scholar ID. |
| Andre M Dehon | [Scholar](https://scholar.google.com/citations?user=nintPk8AAAAJ) | [Source](https://dblp.org/pid/d/ADeHon.html): Computer-architecture bibliography identifies Andre DeHon, matching Penn entries in existing CSRankings and coauthor records. |
| Bangalore S Manjunath | [Scholar](https://scholar.google.com/citations?user=wRYM4qgAAAAJ) | [Source](https://www.computer.org/profiles/b-s-manjunath): IEEE's UCSB image-analysis biography matches the B. S. Manjunath entry in existing CSRankings. |
| Bruce M Maggs | [Scholar](https://scholar.google.com/citations?user=Gwrwxa0AAAAJ) | [Source](https://dblp.org/pid/m/BruceMMaggs.html): Algorithms and networking bibliography matches the Duke Bruce M. Maggs entries in existing local records. |
| Ellen M Voorhees | [Scholar](https://scholar.google.com/citations?user=Bfs9j20AAAAJ) | [Source](https://www.alphaxiv.org/@ellen-voorhees): Information-retrieval research record matches the cached NIST Ellen Voorhees coauthor ID. |
| Frank Mueller | [Scholar](https://scholar.google.com/citations?user=1hEE9ZsAAAAJ) | [Source](https://rqs.umd.edu/people/frank-mueller): NCSU professor identity matches existing CSRankings and coauthor records. |
| John Hughes | [Scholar](https://scholar.google.com/citations?user=adD4xmAAAAAJ) | [Source](https://conf.researchr.org/profile/johnhughes): Exact Scholar URL identifies Chalmers and functional programming and software testing, distinguishing the Fellow from other John Hughes profiles. |
| Mario Gerla | [Scholar](https://scholar.google.com/citations?user=mO3xwbwAAAAJ) | [Source](https://www.wikidata.org/wiki/Q26251480): The Mario Gerla record explicitly lists this Scholar author ID and links the UCLA networking researcher. |
| Mohammad T. Hajiaghayi | [Scholar](https://scholar.google.com/citations?user=SQ1eGN4AAAAJ) | [Source](https://www.cs.umd.edu/user/7851): Maryland algorithms identity matches existing CSRankings and coauthor records. |
| Peter L Bartlett | [Scholar](https://scholar.google.com/citations?user=yQNhFGUAAAAJ) | [Source](https://vcresearch.berkeley.edu/faculty/peter-bartlett): Berkeley machine-learning identity matches the cached Peter Bartlett coauthor ID. |
| Premkumar T Devanbu | [Scholar](https://scholar.google.com/citations?user=tQ5vbOAAAAAJ) | [Source](https://morganlab.ucdavis.edu/people/prem-devanbu): UC Davis Prem Devanbu identity matches the cached coauthor ID and the Fellow's expanded name. |
| Tian He | [Scholar](https://scholar.google.com/citations?user=hc1m_BQAAAAJ) | [Source](https://www.newx.sg/scholar/hc1m_BQAAAAJ): Exact ID identifies the Minnesota computer-science ACM Fellow and agrees with existing local records. |
| Vishal Misra | [Scholar](https://scholar.google.com/citations?user=9hPnkXsAAAAJ) | [Source](https://datascience.columbia.edu/people/vishal-misra/): Columbia computer-networking identity matches existing CSRankings. |
| Wendi Beth Heinzelman | [Scholar](https://scholar.google.com/citations?user=myYVVuYAAAAJ) | [Source](https://hajim.rochester.edu/ece/people/faculty/heinzelman_wendi/index.html): Rochester wireless-networking identity matches existing CSRankings and coauthor records. |
| Andrew K. Mccallum | [Scholar](https://scholar.google.com/citations?user=yILa1y0AAAAJ) | [Source](https://citationmap.com/profile/yILa1y0AAAAJ): Exact ID identifies the UMass computer-science professor and agrees with existing CSRankings and coauthor records. The CSV name was later corrected to `Andrew K. McCallum`; see the [name corrections](#2026-09-15-1627-edt---name-corrections-and-wrong-person-scholar-link-removal). |
| Angelos Dennis Keromytis | [Scholar](https://scholar.google.com/citations?user=mncyWbcAAAAJ) | [Source](https://dblp.org/pid/k/AngelosDKeromytis): Security research bibliography matches the Georgia Tech identity and exact ID in existing local records. |
| Carla Gomes | [Scholar](https://scholar.google.com/citations?user=3hdbdBoAAAAJ) | [Source](https://dblp.org/pid/g/CarlaPGomes.html): Cornell AI researcher matches the Carla P. Gomes entry in existing CSRankings. |
| Edward Alan Fox | [Scholar](https://scholar.google.com/citations?user=KcbSBrUAAAAJ) | [Source](https://fox.cs.vt.edu/): Personal Virginia Tech homepage directly links this ID for Edward Fox. |
| Gail C Murphy | [Scholar](https://scholar.google.com/citations?user=EGA1deoAAAAJ) | [Source](https://www.cs.ubc.ca/people/gail-murphy): UBC software-engineering identity matches existing CSRankings and coauthor records. |
| Geoffrey Voelker | [Scholar](https://scholar.google.com/citations?user=45CJ-rgAAAAJ) | [Source](https://www.alphaxiv.org/@geoffrey-m-voelker): Explicit Scholar link and UCSD homepage identify this ID, agreeing with cached coauthor evidence and resolving the different CSRankings ID. |
| Richard M Fujimoto | [Scholar](https://scholar.google.com/citations?user=q1bkP7AAAAAJ) | [Source](https://www.cc.gatech.edu/people/richard-fujimoto-0): Georgia Tech distributed-simulation identity matches the cached Richard M. Fujimoto coauthor ID. |
| Shafi Goldwasser | [Scholar](https://scholar.google.com/citations?user=KA8dgpMAAAAJ) | [Source](https://citationmap.com/profile/KA8dgpMAAAAJ): Exact ID identifies the Berkeley computer-science professor and agrees with cached coauthor evidence. |
| Anthony Hey | [Scholar](https://scholar.google.com/citations?user=eyOUs-kAAAAJ) | [Source](https://www.turing.ac.uk/people/external-researchers/tony-hey): Tony Hey's scientific-computing identity matches the cached STFC coauthor ID and the Fellow's Anthony Hey name. |
| Daniel Jackson | [Scholar](https://scholar.google.com/citations?user=PXY96lkAAAAJ) | [Source](https://scholar.google.com/citations?user=PXY96lkAAAAJ): Web-indexed profile identifies MIT and Alloy/software-modeling publications, agreeing with cached coauthor evidence and resolving the different CSRankings ID. |
| Holly E Rushmeier | [Scholar](https://scholar.google.com/citations?user=saY3qN5NWbcC) | [Source](https://dblp.dagstuhl.de/pid/13/6571.html): Yale graphics researcher and Holly E. Rushmeier bibliography match existing CSRankings. |
| Michael Saks | [Scholar](https://scholar.google.com/citations?user=mu2I688AAAAJ) | [Source](https://dblp.org/pid/s/MichaelESaks.html): The theoretical-computer-science bibliography matches Rutgers Michael Saks in existing CSRankings and coauthor records. |
| Robert J.K. Jacob | [Scholar](https://scholar.google.com/citations?user=FWjqglcAAAAJ) | [Source](https://hcilab.cs.tufts.edu/publications.html): Tufts HCI publications identify R. J. K. Jacob, matching the cached Rob Jacob coauthor ID. |
| Shwetak N Patel | [Scholar](https://scholar.google.com/citations?user=z4S5rC0AAAAJ) | [Source](https://adscientificindex.com/scientist/shwetak-patel/1684524/): Washington HCI and ubiquitous-computing identity matches existing CSRankings and coauthor records. |
| Valerie Taylor | [Scholar](https://scholar.google.com/citations?user=UUWrt60AAAAJ) | [Source](https://compete.org/valerie-taylor/): Argonne high-performance-computing biography confirms the former Texas A&M appointment, matching the existing CSRankings ID. |
| Cynthia Dwork | [Scholar](https://scholar.google.com/citations?user=y2H5xmkAAAAJ) | [Source](https://dwork.seas.harvard.edu/): Harvard theoretical-computer-science identity matches existing CSRankings. |
| David M. Blei | [Scholar](https://scholar.google.com/citations?user=8OYE6iEAAAAJ) | [Source](https://www.cs.columbia.edu/~blei/static/blei_cv.pdf): Columbia computer-science and statistics identity matches existing CSRankings and coauthor records. |
| Dragomir R Radev | [Scholar](https://scholar.google.com/citations?user=vIqWvgwAAAAJ) | [Source](https://cs.yale.edu/homes/radev/index.html): Yale NLP identity matches the cached Dragomir Radev coauthor ID. |
| Mary P. Czerwinski | [Scholar](https://scholar.google.com/citations?user=LHkrpqEAAAAJ) | [Source](https://czerwinski.live/publications/): Mary P. Czerwinski's HCI publication record matches the cached Microsoft coauthor ID. |
| Michael George Luby | [Scholar](https://scholar.google.com/citations?user=OCzTJZ8AAAAJ) | [Source](https://dblp.org/pid/l/MichaelLuby.html): Coding and algorithms bibliography matches Michael Luby in the cached BitRipple/ICSI coauthor record. |
| Michael Rung-Tsong Lyu | [Scholar](https://scholar.google.com/citations?user=uQnBgK0AAAAJ) | [Source](https://www.cse.cuhk.edu.hk/people/faculty/michael-rung-tsong-lyu/): CUHK faculty page supplies the expanded name and software-engineering identity, matching existing local records. |
| Shmuel Sagiv | [Scholar](https://scholar.google.com/citations?user=j4UuW80AAAAJ) | [Source](https://dblp.org/pid/s/SSagiv.html): Tel Aviv program-analysis identity matches existing CSRankings. |
| Ueli M Maurer | [Scholar](https://scholar.google.com/citations?user=TSsq3GMAAAAJ) | [Source](https://crypto.ethz.ch/~maurer/index.html): ETH cryptography identity matches existing CSRankings. |
| Alberto Luigi Sangiovanni Vincentelli | [Scholar](https://scholar.google.com/citations?user=AhgjQ2QAAAAJ) | [Source](https://vcresearch.berkeley.edu/faculty/alberto-sangiovanni-vincentelli): Berkeley electronic-design-automation identity matches existing CSRankings and coauthor records. |
| Nikil D. Dutt | [Scholar](https://scholar.google.com/citations?user=CpBXPVoAAAAJ) | [Source](https://www.newx.sg/scholar/CpBXPVoAAAAJ): Exact ID identifies the UC Irvine embedded-systems and computer-architecture professor and agrees with existing local records. |
| S. Sudarshan | [Scholar](https://scholar.google.com/citations?user=KtP9-zYAAAAJ) | [Source](https://www.cse.iitb.ac.in/~sudarsha/): IIT Bombay database-systems identity matches existing CSRankings and coauthor records. |
| Samson Abramsky | [Scholar](https://scholar.google.com/citations?user=L2vmD3MAAAAJ) | [Source](https://dblp.org/pid/a/SamsonAbramsky.html): Theoretical-computer-science bibliography matches the Samson Abramsky ID in existing CSRankings. |
| Stephen J Whittaker | [Scholar](https://scholar.google.com/citations?user=TkVUIVsAAAAJ) | [Source](https://campusdirectory.ucsc.edu/cd_detail?uid=swhittak): UCSC directory explicitly connects Stephen J Whittaker with Steve Whittaker, matching existing CSRankings. |
| Timothy Alden Davis | [Scholar](https://scholar.google.com/citations?user=gNMqz_4AAAAJ) | [Source](https://engineering.tamu.edu/cse/profiles/davis-tim.html): Texas A&M scientific-computing identity matches the Timothy A. Davis entry in existing CSRankings. |
| Valerie King | [Scholar](https://scholar.google.com/citations?user=2-iEYMUAAAAJ) | [Source](https://adscientificindex.com/scientist/valerie-king/646997/): Victoria computer-science identity matches existing CSRankings and coauthor records, distinguishing other Valerie King researchers. |
| Carlos J P De Lucena | [Scholar](https://scholar.google.com/citations?user=BCW5XGIAAAAJ) | [Source](https://www.inf.puc-rio.br/en/teacher/carlos-jose-pereira-de-lucena/?isModal=1): PUC-Rio faculty page explicitly prints the Scholar URL and connects the Carlos Lucena name variants. |
| Charu Chandra Aggarwal | [Scholar](https://scholar.google.com/citations?user=x_wsduUAAAAJ) | [Source](https://charuaggarwal.net/): IBM data-mining biography matches the cached Charu Aggarwal coauthor ID. |

Twenty-seven entries were left blank in this batch:

| ACM Fellow | Source and Reason |
| --- | --- |
| Manuel Blum | [Source](https://www.cs.cmu.edu/~mblum/): Searches distinguish the CMU complexity theorist from a Freiburg namesake, but did not independently establish the local CSRankings candidate's exact profile identity. |
| Martin Hellman | [Source](https://profiles.stanford.edu/martin-hellman): Identified the Stanford cryptography researcher, but did not establish an exact Scholar profile URL. |
| Whitfield Diffie | [Source](https://cisac.fsi.stanford.edu/people/whitfield_diffie): Identified the cryptography researcher, but did not establish an exact Scholar profile URL. |
| Andreas Reuter | [Source](https://dblp.org/pid/r/AReuter.html): Identified the database researcher; prominent search results concern unrelated namesakes and no exact matching Scholar URL was established. |
| Elena Ferrari | [Source](https://dawsec.dicom.uninsubria.it/elena.ferrari/publications): Search snippets mention a Scholar link, but the accessible publications page no longer exposes it; no exact ID was established. |
| Mona Singh | [Source](https://www.cs.princeton.edu/~mona/research.html): Identified the Princeton computational-biology researcher, but no replacement ID was established; the previously rejected consultant profile remains excluded. |
| Peter W Shor | [Source](https://math.mit.edu/~shor/): Identified the MIT quantum-computing researcher, but did not establish an exact Scholar profile URL. |
| Avi Wigderson | [Source](https://www.ias.edu/scholars/wigderson): Identified the theoretical computer scientist, but did not establish an exact Scholar profile URL. |
| Charles Lee Isbell Jr | [Source](https://faculty.cc.gatech.edu/~isbell/): Identified the computing researcher, but existing CSRankings lists NOSCHOLARPAGE and searches did not establish a matching exact URL. |
| Gurudatta Parulkar | [Source](https://dblp.org/pid/50/4579.html): Searched the Guru Parulkar alias and identified the networking researcher, but did not establish an exact Scholar profile URL. |
| Tom Leighton | [Source](https://en.wikipedia.org/wiki/F._Thomson_Leighton): Searched Tom Leighton and F. Thomson Leighton, but did not establish an exact Scholar profile URL. |
| Toniann Pitassi | [Source](https://datascience.columbia.edu/people/toniann-pitassi/): Identified the Columbia complexity researcher, but existing CSRankings lists NOSCHOLARPAGE and searches did not establish a matching exact URL. |
| Clifford A Lynch | [Source](https://people.ischool.berkeley.edu/~clifford/): Identified the CNI and Berkeley researcher, but did not establish an exact Scholar profile URL. |
| Michael Sipser | [Source](https://math.mit.edu/~sipser/): Identified the MIT complexity researcher, but did not establish an exact Scholar profile URL. |
| Silvio Micali | [Source](https://ilpstex.mit.edu/en/content/faculty-profiles/silvio-micali): Identified the MIT cryptography researcher, but existing CSRankings lists NOSCHOLARPAGE and searches did not establish a matching exact URL. |
| Steven Michael Hand | [Source](https://www.research.google/people/105153/): Identified the systems researcher; publication-search links and unrelated IDs did not establish a personal Scholar profile URL. |
| Joseph Bryan Lyles | [Source](https://dblp.org/pid/03/4762.html): DBLP search results mention a Scholar profile for J. Bryan Lyles, but the accessible results did not expose its exact URL. |
| K. Rustan M. Leino | [Source](https://dblp.org/pid/l/KRMLeino): Identified the program-verification researcher, but did not establish an exact Scholar profile URL. |
| Radia Perlman | [Source](https://dblp.org/pid/87/2370.html): Identified the networking researcher, but did not establish an exact Scholar profile URL. |
| Ravi Kannan | [Source](https://simons.berkeley.edu/people/ravi-kannan): Identified the theoretical computer scientist, but no replacement ID was established; the previously rejected fluid-dynamics profile remains excluded. |
| Ricardo Bianchini | [Source](https://www.microsoft.com/en-us/research/people/ricardob/): Identified the Microsoft systems researcher, but did not establish an exact Scholar profile URL. |
| Kevin Fall | [Source](https://dblp.org/pid/38/3635.html): Identified the networking researcher, but no replacement ID was established; the previously rejected counseling profile remains excluded. |
| Michael Franz | [Source](https://www.faculty.uci.edu/profile/?facultyId=4680): Identified the UC Irvine systems researcher, but existing CSRankings lists NOSCHOLARPAGE and searches did not establish a matching exact URL. |
| Ramanathan Guha | [Source](https://dblp.org/pid/g/RamanathanVGuha.html): Searched Ramanathan Guha and R. V. Guha, but did not establish an exact matching Scholar profile URL. |
| Charles W Bachman | [Source](https://computerhistory.org/profile/charles-w-bachman/): Identified the database pioneer, but did not establish an exact Scholar profile URL; results for Charles Bachmann concern a different person. |
| Faith Ellen | [Source](https://www.cs.utoronto.ca/~faith/): Identified the Toronto distributed-computing researcher, but existing CSRankings lists NOSCHOLARPAGE and searches did not establish a matching exact URL. |
| Chip Elliott | [Source](https://dblp.org/pid/78/115.html): Identified the BBN networking researcher, but did not establish an exact Scholar profile URL. |

These unresolved results do not establish that no Scholar profile exists.

## 2026-09-15 10:21 EDT - Google Scholar Links: Seventh Web Search Batch

This bounded batch checked the next fifty missing entries in CSV order, skipping the seventeen unresolved entries from earlier batches.
The batch contained thirteen Fellows from 2023, nine from 2022, nineteen from 2021, and nine from 2020.
General web search, corroborated where needed by existing CSRankings and cached Scholar coauthor records, established forty-six clear matches.
The links below were added, bringing the dataset to 1,043 nonempty Scholar links and 595 blank Scholar cells across 1,638 Fellows.
Only the forty-six previously blank Scholar URL cells changed; names and other CSV fields were preserved.
No computer-use tools or project crawlers were used, and no caches, Scholar profile exports, or visualizations were regenerated.
These checks establish identity and link correspondence; they are not fresh audits of Scholar publication lists or metrics.
Existing CSRankings records are from `../bigcows-crawler/.cache/csrankings/csrankings-*.csv`, and cached coauthor evidence is from `../bigcows-crawler/.cache/google-scholar-profile-cache.json`.
Where Scholar access returned an error, an explicit profile link from the cited source established the URL; an access error was not treated as evidence that the profile did not exist.
Six additions replace links removed during the earlier wrong-person audit: Chung C. J Kuo, Hai Li, Meenakshi Balakrishnan, Antonio Gonzalez, Brian Levine, and David Brooks.
The earlier removal records remain below to prevent those incorrect IDs from being reintroduced.
Antonio Gonzalez's personal UPC homepage resolved the conflicting local candidate IDs; the same conflict could not be resolved for Trent Jaeger.
Chandra Narayanaswami's IBM biography supplied a valid profile ID through its inline Scholar link, while its separate footer Scholar link incorrectly used his name as the user parameter.

| ACM Fellow | Added Scholar Profile | Source and Identity Evidence |
| --- | --- | --- |
| Vaughn Timothy Betz | [Scholar](https://scholar.google.com/citations?user=bMdDigQAAAAJ) | [Source](https://www.researchgate.net/profile/Vaughn-Betz): Toronto FPGA researcher Vaughn Betz; exact ID from existing Toronto coauthor records. |
| Vineet Bafna | [Scholar](https://scholar.google.com/citations?user=NzQu5SwAAAAJ) | [Source](https://dblp.org/pid/b/VineetBafna): UCSD computational biology researcher; DBLP ORCID agrees with existing CSRankings, which supplies this ID. |
| Wei-Ying Ma | [Scholar](https://scholar.google.com/citations?user=SToCbu8AAAAJ) | [Source](https://scholars.cityu.edu.hk/en/persons/weiyma/): CityUHK profile explicitly gives this Scholar ID for Wei-Ying Ma; existing CSRankings agrees. |
| Wenjing Lou | [Scholar](https://scholar.google.com/citations?user=hM8uAwoAAAAJ) | [Source](https://cs.vt.edu/people/faculty/wenjing-lou.html): Virginia Tech cybersecurity and wireless networking researcher; ID from matching existing CSRankings. |
| Wenliang Du | [Scholar](https://scholar.google.com/citations?user=1aMkcasAAAAJ) | [Source](https://dblp.org/pid/d/WenliangDu): SEED security education researcher; existing coauthor records explicitly identify Wenliang Du at Syracuse with this ID. |
| XiaoFeng Wang | [Scholar](https://scholar.google.com/citations?user=pONu-5EAAAAJ) | [Source](https://wangxiaofeng7.github.io/): Personal biography identifies the NTU cybersecurity professor, formerly Indiana, and his 2023 ACM Fellowship; existing NTU CSRankings supplies this ID. |
| Xin Luna Dong | [Scholar](https://scholar.google.com/citations?user=uGsKvHoAAAAJ) | [Source](https://www.lunadong.com/): Meta knowledge graphs researcher, formerly Amazon and Google; exact ID from existing Xin Luna Dong coauthor records. |
| Xing Xie | [Scholar](https://scholar.google.com/citations?user=5EQfAFIAAAAJ) | [Source](https://www.microsoft.com/en-us/research/people/xingx/representative-publications/): Microsoft Research researcher; existing Xing Xie coauthor records explicitly identify Microsoft and ACM Fellowship, excluding the environmental engineering namesake. |
| Yann LeCun | [Scholar](https://scholar.google.com/citations?user=WLN3QrAAAAAJ) | [Source](https://yann.lecun.org/): NYU/Meta machine learning researcher; exact ID from existing Yann LeCun coauthor records. |
| Yingying Chen | [Scholar](https://scholar.google.com/citations?user=jCZaWOEAAAAJ) | [Source](https://research.com/u/yingying-chen): Directory links this exact profile for the Rutgers researcher; indexed Scholar coauthors and Rutgers homepage corroborate wireless networking and security. |
| Yoshua Bengio | [Scholar](https://scholar.google.com/citations?user=kukA0LcAAAAJ) | [Source](https://diro.umontreal.ca/en/repertoire-departement/professeurs/professeur/in/in13599/sg/Yoshua%20Bengio/): Montreal machine learning researcher; existing CSRankings and coauthor records agree on this ID. |
| Zhu Han | [Scholar](https://scholar.google.com/citations?user=ty7wIXoAAAAJ) | [Source](https://www.ie.uh.edu/faculty/han-zhu): University of Houston electrical engineering professor; exact ID from existing CSRankings Zhu Han 0001. |
| Alfons Kemper | [Scholar](https://scholar.google.com/citations?user=5n3YivwAAAAJ) | [Source](https://dblp.org/pid/k/AlfonsKemper.html): TU Munich database researcher; exact ID from existing Alfons Kemper CSRankings entry. |
| Chung C. J Kuo | [Scholar](https://scholar.google.com/citations?user=81d60okAAAAJ) | [Source](https://viterbi.usc.edu/directory/faculty/Kuo/Chung-Chieh): USC visual computing researcher C.-C. Jay Kuo; existing CSRankings aliases agree on this ID, excluding the removed materials-research profile. |
| David Atienza Alonso | [Scholar](https://scholar.google.com/citations?user=H1JXhMIAAAAJ) | [Source](https://people.epfl.ch/david.atienza?lang=en): EPFL biography for David Atienza Alonso explicitly gives this Scholar URL. |
| David M Mount | [Scholar](https://scholar.google.com/citations?user=v6PsQKIAAAAJ) | [Source](https://www.cs.umd.edu/people/mount): Maryland computational geometry researcher; exact ID from existing David M. Mount CSRankings entry. |
| Hong Mei | [Scholar](https://scholar.google.com/citations?user=b-ZYIwoAAAAJ) | [Source](https://group.pku.edu.cn/meih/zh_CN/index/43448/list/index.htm): Peking University computer scientist Hong Mei; exact ID from existing CSRankings Hong Mei 0001. |
| Kevin Fu | [Scholar](https://scholar.google.com/citations?user=pZQuSyUAAAAJ) | [Source](https://www.khoury.northeastern.edu/people/kevin-fu/): Northeastern medical-device and analog cybersecurity researcher; exact ID from matching existing CSRankings. |
| Luis H Ceze | [Scholar](https://scholar.google.com/citations?user=KzESVKwAAAAJ) | [Source](https://ready.cs.washington.edu/~luisceze//): Washington computer architecture researcher Luis Ceze; existing CSRankings and coauthor records agree on this ID. |
| Manuel V Hermenegildo | [Scholar](https://scholar.google.com/citations?user=VXQGJD0AAAAJ) | [Source](https://cliplab.org/~herme/engcur/engcur.html): Logic programming researcher at IMDEA and UPM; existing CSRankings and coauthor records agree on this ID. |
| Yuguang Fang | [Scholar](https://scholar.google.com/citations?user=dJgRKmwAAAAJ) | [Source](https://www.cs.cityu.edu.hk/~yugufang/): CityUHK networking researcher; existing CSRankings supplies this ID with the same homepage. |
| Amos Fiat | [Scholar](https://scholar.google.com/citations?user=0MzVIUsAAAAJ) | [Source](https://dblp.org/pid/06/894.html): DBLP links this exact Scholar profile and the Tel Aviv homepage for Amos Fiat. |
| Dale A Miller | [Scholar](https://scholar.google.com/citations?user=d9WopvMAAAAJ) | [Source](https://www.inria.fr/fr/vers-lemergence-dun-internet-de-la-preuve): Inria formal logic researcher Dale Miller; exact ID from existing Inria-Saclay/LIX coauthor records. |
| Feifei Li | [Scholar](https://scholar.google.com/citations?user=qPDhlWkAAAAJ) | [Source](https://users.cs.utah.edu/~lifeifei/research.html): Utah database researcher's publication page directly links this exact Scholar URL, excluding Stanford Fei-Fei Li and chemistry namesakes. |
| Glenn Ricart | [Scholar](https://scholar.google.com/citations?user=xqach48AAAAJ) | [Source](https://router-admin.net/articles/internet-history): Internet history article explicitly links this Scholar URL for Glenn Ricart; Utah faculty listing and ResearchGate corroborate the computing researcher. |
| Hai Li | [Scholar](https://scholar.google.com/citations?user=E6Tpfq8AAAAJ) | [Source](https://ece.duke.edu/people/hai-helen-li/): Duke Hai (Helen) Li; existing CSRankings and Duke coauthor records agree on this ID, excluding the removed materials-research profile. |
| Jacob Otto Wobbrock | [Scholar](https://scholar.google.com/citations?user=TmZ3howAAAAJ) | [Source](https://faculty.washington.edu/wobbrock/bio.html): Washington HCI researcher Jacob O. Wobbrock; existing CSRankings and coauthor records agree on this ID. |
| Lin Zhong | [Scholar](https://scholar.google.com/citations?user=hJPN-G8AAAAJ) | [Source](https://openreview.net/profile?id=~Lin_Zhong1): Yale computer systems researcher with confirmed Yale and Rice email domains; existing CSRankings and coauthor records agree on this ID. |
| Linda Jean Camp | [Scholar](https://scholar.google.com/citations?user=wJPGa2IAAAAJ) | [Source](https://ljcamp.github.io/): UNC Charlotte security researcher L. Jean Camp; existing CSRankings aliases Linda Jean Camp and L. Jean Camp agree on this ID. |
| Mark Braverman | [Scholar](https://scholar.google.com/citations?user=5elBSHQAAAAJ) | [Source](https://www.ias.edu/scholars/mark-braverman): Theoretical computer science researcher; Princeton CSRankings and coauthor records agree on this ID. |
| Meenakshi Balakrishnan | [Scholar](https://scholar.google.com/citations?user=e_749FUAAAAJ) | [Source](https://iitd.irins.org/profile/659669): IIT Delhi profile explicitly gives this Scholar ID for M. Balakrishnan; the IIT Delhi CV identifies his full name as Meenakshi Balakrishnan, excluding the removed clinical namesake. |
| Mubarak Ali Shah | [Scholar](https://scholar.google.com/citations?user=p8gsO3gAAAAJ) | [Source](https://www.crcv.ucf.edu/person/mubarak-shah/): UCF computer vision researcher Mubarak Shah; exact ID from matching existing CSRankings. |
| Paola Inverardi | [Scholar](https://scholar.google.com/citations?user=x8XlRFgAAAAJ) | [Source](https://research.com/u/paola-inverardi): Software engineering researcher associated with L'Aquila; existing GSSI CSRankings record supplies this ID and her L'Aquila homepage. |
| Ranjit Jhala | [Scholar](https://scholar.google.com/citations?user=H3wb878AAAAJ) | [Source](https://ranjitjhala.github.io/research.html): UCSD programming languages and software verification researcher; exact ID from existing CSRankings with the same homepage. |
| Rosalind Wright Picard | [Scholar](https://scholar.google.com/citations?user=1-hcASEAAAAJ) | [Source](https://dblp.org/pid/p/RWPicard.html): DBLP explicitly links this Scholar profile and the MIT homepage for Rosalind W. Picard. |
| Tajana Rosing | [Scholar](https://scholar.google.com/citations?user=CeieiIgAAAAJ) | [Source](https://profiles.ucsd.edu/tajana.rosing): UCSD computer science professor Tajana Rosing; existing CSRankings name variants agree on this ID. |
| Tao Xie | [Scholar](https://scholar.google.com/citations?user=DhhH9J4AAAAJ) | [Source](https://taoxie.cs.illinois.edu/publications.htm): Software engineering researcher; exact ID from existing Peking CSRankings Tao Xie 0001, excluding the political science namesake. |
| Tie-Yan Liu | [Scholar](https://scholar.google.com/citations?user=Nh832fgAAAAJ) | [Source](https://adscientificindex.com/scientist/tie-yan-liu/4383522/): Machine learning researcher associated with Microsoft Research; existing Tie-Yan Liu coauthor records supply this exact ID. |
| Antonio Gonzalez | [Scholar](https://scholar.google.com/citations?user=DRP_OcMAAAAJ) | [Source](https://people.ac.upc.edu/antonio/): UPC computer architecture homepage directly links this ID, resolving disagreement with existing CSRankings WegaFkUAAAAJ and agreeing with cached UPC coauthor evidence. |
| Bonnie J Dorr | [Scholar](https://scholar.google.com/citations?user=jSjEWosAAAAJ) | [Source](https://www.umiacs.umd.edu/our-experts/faculty/bonnie-dorr): Maryland computational linguistics professor emerita; existing CSRankings and UF/IHMC/UMD coauthor records agree on this ID. |
| Brian Levine | [Scholar](https://scholar.google.com/citations?user=oHbIF48AAAAJ) | [Source](https://research.com/u/brian-neil-levine): UMass Amherst computer scientist Brian Neil Levine; existing CSRankings and coauthor records agree on this ID, excluding the removed Toronto neuropsychologist. |
| Cathy H Wu | [Scholar](https://scholar.google.com/citations?user=eiRdbhsAAAAJ) | [Source](https://bioinformatics.udel.edu/people/cathy-wu-phd/): Delaware bioinformatics researcher Cathy H. Wu; exact ID from matching existing CSRankings. |
| Chandra Narayanaswami | [Scholar](https://scholar.google.com/citations?user=jZUeVbcAAAAJ) | [Source](https://research.ibm.com/people/chandra-narayanaswami): IBM biography's inline Google Scholar link gives this exact ID; the separate footer link incorrectly uses a name instead of a profile ID and was not used. |
| David Brooks | [Scholar](https://scholar.google.com/citations?user=vXHA_XYAAAAJ) | [Source](https://davidbrooks.seas.harvard.edu/): Harvard computer architecture professor; existing David Brooks 0001 CSRankings and Harvard coauthor records agree, excluding the old CSRankings alias carrying the removed PET/neuroimaging ID. |
| Graham R. Cormode | [Scholar](https://scholar.google.com/citations?user=gpLVKmEAAAAJ) | [Source](https://dblp.org/pid/c/GrahamCormode): Algorithms and data analysis researcher; DBLP ORCID matches existing Warwick CSRankings, and Meta/Warwick coauthor records agree on this ID. |
| James Allan | [Scholar](https://scholar.google.com/citations?user=-bLGeg0AAAAJ) | [Source](https://www.cics.umass.edu/about/directory/james-allan): UMass Amherst information retrieval researcher; existing CSRankings and coauthor records agree on this ID. |

Four entries were left blank in this batch:

| ACM Fellow | Reason |
| --- | --- |
| Trent Jaeger | Existing CSRankings supplies `JS8aznIAAAAJ`, while existing coauthor records identify the UCR security researcher with `LpwdzeEAAAAJ`; searches and the [UCR research page](https://www.cs.ucr.edu/~trentj/research.html) did not resolve the conflicting exact URLs, so neither was selected. |
| Leonard M. Adleman | Searches identified the USC cryptography and molecular computing researcher, but did not establish an exact Scholar profile URL; existing CSRankings lists `NOSCHOLARPAGE`, and results for Leonard Adelman at George Mason concern a different person. |
| Thomas Lengauer | Searches identified the [Max Planck computational biology researcher](https://www.mpi-inf.mpg.de/departments/research-group-computational-biology/people/thomas-lengauer), but did not establish an exact Scholar profile URL; existing CSRankings lists `NOSCHOLARPAGE`. |
| C. Antony R. Hoare | Searches under Tony Hoare and C. Antony R. Hoare identified the [Microsoft researcher](https://www.microsoft.com/en-us/research/people/thoare/publications/), but did not establish an exact Scholar profile URL. |

These unresolved results do not establish that no Scholar profile exists.

## 2026-09-15 - Google Scholar Links: Sixth Web Search Batch

On 2026-09-15, a bounded batch checked the next fifty missing entries in CSV order, skipping the fourteen unresolved entries from earlier batches.
All fifty Fellows in this batch were from the 2023 class.
General web search, corroborated where needed by existing CSRankings and cached Scholar coauthor records, established forty-seven clear matches.
The links below were added, bringing the dataset to 997 nonempty Scholar links and 641 blank Scholar cells across 1,638 Fellows.
Only the forty-seven previously blank Scholar URL cells changed in this batch; names and other CSV fields were preserved.
No computer-use tools or project crawlers were used, and no caches, Scholar profile exports, or visualizations were regenerated.
These checks establish identity and link correspondence; they are not fresh audits of Scholar publication lists or metrics.
Existing CSRankings records are from `../bigcows-crawler/.cache/csrankings/csrankings-*.csv`, and cached coauthor evidence is from `../bigcows-crawler/.cache/google-scholar-profile-cache.json`.
Where Scholar access returned an error, an explicit profile link from the cited source established the URL; access failure was not treated as proof that the profile was missing.

| ACM Fellow | Added Scholar Profile | Source and Identity Evidence |
| --- | --- | --- |
| Anja Feldmann | [Scholar](https://scholar.google.com/citations?user=mSK3340AAAAJ) | [Source](https://plamadiso.weizenbaum-institut.de/anja-feldmann/): MPI/Saarland researcher; source gives the exact Scholar URL, also present in existing coauthor records. |
| Benjamin Raphael | [Scholar](https://scholar.google.com/citations?user=GhvZjJUAAAAJ) | [Source](https://www.cs.princeton.edu/people/profile/braphael): Princeton computational biology researcher, listed as Ben Raphael; existing CSRankings Benjamin J. Raphael and cached Ben Raphael coauthor records agree on this ID. |
| Björn W. Schuller | [Scholar](https://scholar.google.com/citations?user=TxKNCSoAAAAJ) | [Source](https://www.schuller.it/bws/?page_id=179): Personal page gives the exact Scholar URL; Imperial affiliation agrees with existing CSRankings. |
| Chandra Chekuri | [Scholar](https://scholar.google.com/citations?user=7j3itaMAAAAJ) | [Source](https://chekuri.cs.illinois.edu/): Illinois algorithms researcher; exact ID from existing CSRankings. |
| Christopher Ian Kruegel | [Scholar](https://scholar.google.com/citations?user=f0NoTC0AAAAJ) | [Source](https://www.sba-research.org/team/christopher-kruegel/): UCSB security researcher Christopher Kruegel; existing coauthor records identify the same UCSB/Cisco researcher and exact ID. |
| Corina S Pasareanu | [Scholar](https://scholar.google.com/citations?user=pwIuivQAAAAJ) | [Source](https://www.cylab.cmu.edu/directory/bios/pasareanu-corina.html): CMU/NASA Ames formal verification researcher; exact ID from existing Corina Pasareanu coauthor records. |
| Dana Ron | [Scholar](https://scholar.google.com/citations?user=cbnnDB4AAAAJ) | [Source](https://dblp.org/pid/85/4800.html): DBLP links this profile; indexed Scholar page confirms Tel Aviv University and property-testing publications. |
| David Lo | [Scholar](https://scholar.google.com/citations?user=IFg0H1wAAAAJ) | **Superseded:** See the [later wrong-person correction](#2026-09-15-1627-edt---name-corrections-and-wrong-person-scholar-link-removal). Initial rationale: [Source](https://news.smu.edu.sg/sites/news.smu.edu.sg/files/smu/news_room/SMU%20Media%20Release_SMU%20Faculty%20David%20Lo%20achieves%20ACM%20Fellowship%2005Feb2024.pdf): SMU software engineering researcher and ACM Fellow; exact ID from the matching existing CSRankings entry, excluding the Stanford namesake. |
| David Sankoff | [Scholar](https://scholar.google.com/citations?user=C-BvZ4oAAAAJ) | [Source](https://dblp.org/pid/66/977.html): DBLP links this exact profile and the University of Ottawa homepage for the mathematical genomics researcher. |
| Deborah McGuinness | [Scholar](https://scholar.google.com/citations?user=PLJ0L4QAAAAJ) | [Source](https://faculty.rpi.edu/deborah-mcguinness): RPI knowledge representation researcher; exact ID from existing Deborah L. McGuinness coauthor records, corroborated by Wikidata Q5248328. |
| Elaine Shi | [Scholar](https://scholar.google.com/citations?user=rejzeocAAAAJ) | [Source](https://elaineshi.com/): CMU cryptography researcher and ACM Fellow; existing CSRankings matches her name, homepage and exact ID. |
| Emmett Witchel | [Scholar](https://scholar.google.com/citations?user=k4oSgRkAAAAJ) | [Source](https://www.cs.utexas.edu/~witchel/): UT Austin systems researcher; exact ID from existing CSRankings. |
| Fedor Fomin | [Scholar](https://scholar.google.com/citations?user=96ZXvOsAAAAJ) | [Source](https://www4.uib.no/finn-ansatte/fedor.fomin): Bergen algorithms researcher; existing CSRankings lists Fedor V. Fomin with this ID, excluding the metallurgy namesake. |
| Geoffrey E Hinton | [Scholar](https://scholar.google.com/citations?user=JicYPdAAAAAJ) | [Source](https://www.cs.toronto.edu/~hinton/): Toronto machine learning researcher; exact ID from existing Geoffrey Hinton coauthor records. |
| George Fitzmaurice | [Scholar](https://scholar.google.com/citations?user=u0JtLz0AAAAJ) | [Source](https://research.com/u/george-fitzmaurice): Directory links this exact Scholar URL; identity corroborated by the Autodesk Research page for its HCI researcher. |
| Gerard Medioni | [Scholar](https://scholar.google.com/citations?user=b0k2tTgAAAAJ) | [Source](https://viterbi.usc.edu/directory/faculty/Medioni/Gerard): USC computer vision professor emeritus Gerard Guy Medioni; exact ID from existing USC coauthor records. |
| Haibo Chen | [Scholar](https://scholar.google.com/citations?user=qd9xSkYAAAAJ) | [Source](https://www.newx.sg/scholar/qd9xSkYAAAAJ): Indexed profile identifies the SJTU operating systems researcher; exact ID agrees with existing CSRankings Haibo Chen 0001. |
| Ht Kung | [Scholar](https://scholar.google.com/citations?user=iLQqwosAAAAJ) | [Source](https://research.com/u/ht-kung): Harvard researcher H. T. Kung; exact ID from matching existing CSRankings. The CSV name was later corrected to `H. T. Kung`; see the [name corrections](#2026-09-15-1627-edt---name-corrections-and-wrong-person-scholar-link-removal). |
| Jeffrey S Foster | [Scholar](https://scholar.google.com/citations?user=QWPwfsgAAAAJ) | [Source](https://engineering.tufts.edu/cs/people/faculty/jeffrey-foster): Tufts programming languages and software security researcher; exact ID from existing CSRankings Jeffrey S. Foster, excluding the biologist namesake. |
| Jianfeng Gao | [Scholar](https://scholar.google.com/citations?user=CQ1cqKkAAAAJ) | [Source](https://www.alphaxiv.org/@jianfeng-gao): Directory links this exact profile; indexed Scholar identifies Microsoft Research, Redmond, consistent with his Microsoft biography. |
| Keith Noah Snavely | [Scholar](https://scholar.google.com/citations?user=Db4BCX8AAAAJ) | [Source](https://www.cs.cornell.edu/~snavely/): Cornell computer vision researcher Noah Snavely; existing CSRankings and Cornell/Google coauthor records agree on this ID. |
| Kenneth Richard Koedinger | [Scholar](https://scholar.google.com/citations?user=_8DDVkAAAAAJ) | [Source](https://www.cmu.edu/datalab/about-datalab/koedinger.html): CMU HCI and learning researcher Kenneth R. Koedinger; existing CSRankings and coauthor aliases agree on this ID. |
| Kenneth Ward Church | [Scholar](https://scholar.google.com/citations?user=E6aqGvYAAAAJ) | [Source](https://kwchurch.github.io/): Personal homepage for the NLP researcher links this exact Scholar URL and describes his Bell Labs, Microsoft, Baidu and Northeastern career. |
| Kilian Weinberger | [Scholar](https://scholar.google.com/citations?user=jsxk8vsAAAAJ) | [Source](https://www.cs.cornell.edu/~kilian/): Cornell machine learning researcher; exact ID from existing CSRankings Kilian Q. Weinberger. |
| Kwan-Liu Ma | [Scholar](https://scholar.google.com/citations?user=LgL2HpkAAAAJ) | [Source](https://www.cs.ucdavis.edu/~ma/research.html): UC Davis visualization researcher; exact ID from existing CSRankings. |
| Maria-Florina Balcan | [Scholar](https://scholar.google.com/citations?user=LWlN_BUAAAAJ) | [Source](https://www.wikidata.org/wiki/Q95280352): Wikidata gives this exact ID; matching CMU entry in existing CSRankings agrees. |
| Massoud Pedram | [Scholar](https://scholar.google.com/citations?user=FHiQmOoAAAAJ) | [Source](https://openreview.net/profile?id=~Massoud_Pedram1): USC hardware researcher; exact ID from existing USC coauthor records. |
| Michael Backes | [Scholar](https://scholar.google.com/citations?user=ZVS3KOEAAAAJ) | [Source](https://www.sciencedirect.com/author/6603696569/michael-backes): CISPA security researcher; exact ID from existing CSRankings Michael Backes 0001, excluding the astrophysics namesake. |
| Mikhail Belkin | [Scholar](https://scholar.google.com/citations?user=Iwd9DdkAAAAJ) | [Source](https://www.wikidata.org/wiki/Q102170016): Wikidata gives this exact ID and the ACM Fellowship in machine learning; matching UCSD CSRankings record agrees. |
| Morley Mao | [Scholar](https://scholar.google.com/citations?user=Ba_Ci9UAAAAJ) | [Source](https://ccat.umtri.umich.edu/profile/mao/): Michigan network security researcher; existing Z. Morley Mao coauthor records supply the exact ID. |
| Natasha Noy | [Scholar](https://scholar.google.com/citations?user=FE08ALAAAAAJ) | [Source](https://www.wikidata.org/wiki/Q52174287): Wikidata gives this exact ID for Natalya/Natasha Noy; Google Research biography corroborates the ontology researcher. |
| Nicole Immorlica | [Scholar](https://scholar.google.com/citations?user=_1hCq3UAAAAJ) | [Source](https://dblp.org/pid/43/3631.html): Economics and computation researcher; DBLP ORCID 0000-0003-4180-4657 matches the existing Yale CSRankings record supplying this ID. |
| Nikhil Bansal | [Scholar](https://scholar.google.com/citations?user=3Lmd6AMAAAAJ) | [Source](https://research.com/u/nikhil-bansal): Algorithms researcher with scheduling and discrepancy publications; exact ID from existing Michigan CSRankings Nikhil Bansal 0001. |
| Phoebe Sengers | [Scholar](https://scholar.google.com/citations?user=6c5cf1wAAAAJ) | [Source](https://www.cs.cornell.edu/people/phoebe-sengers): Cornell HCI researcher; university page identifies the 2023 ACM Fellowship and existing CSRankings supplies this ID. |
| Pradeep Dubey | [Scholar](https://scholar.google.com/citations?user=-ad5RSQAAAAJ) | [Source](https://research.com/u/pradeep-dubey): Directory links this exact profile and Intel homepage; Intel and Purdue biographies establish the parallel computing researcher, excluding the Stony Brook economist. |
| Ram D Sriram | [Scholar](https://scholar.google.com/citations?user=W4t8B20AAAAJ) | [Source](https://research.com/u/ram-d-sriram): Directory links this exact profile for the NIST researcher; NIST biography corroborates software systems and collaborative engineering work. |
| Ramon Caceres | [Scholar](https://scholar.google.com/citations?user=rWMibvIAAAAJ) | [Source](https://www.kiskeya.net/ramon/work/pubs.html): Personal publication page for Ramón Cáceres directly links this exact Scholar URL and lists his mobile systems and networking work. |
| Roger B. Dannenberg | [Scholar](https://scholar.google.com/citations?user=whacJzwAAAAJ) | [Source](https://research.com/u/roger-b-dannenberg): Directory links this exact Scholar profile; indexed profile and CMU homepage identify the computer music researcher. |
| Rolf Drechsler | [Scholar](https://scholar.google.com/citations?user=9v_MAAIAAAAJ) | [Source](https://www.rolfdrechsler.de/publications.php): Bremen formal verification and circuit design researcher; exact ID from existing CSRankings. |
| Seffi Naor | [Scholar](https://scholar.google.com/citations?user=xGbDr7YAAAAJ) | [Source](https://naor.cswp.cs.technion.ac.il/): Technion algorithms researcher; exact ID from matching existing CSRankings. |
| Shai Ben-David | [Scholar](https://scholar.google.com/citations?user=kezPqwoAAAAJ) | [Source](https://uwaterloo.ca/computer-science/contacts/shai-ben-david): Waterloo machine learning theory researcher; exact ID from existing CSRankings. |
| Sharad Mehrotra | [Scholar](https://scholar.google.com/citations?user=MTZaRW4AAAAJ) | [Source](https://ics.uci.edu/~sharad/pubs.html): UC Irvine database researcher; exact ID from existing CSRankings. |
| Shrikanth Narayanan | [Scholar](https://scholar.google.com/citations?user=8EDHmYkAAAAJ) | [Source](https://viterbi.usc.edu/directory/cv/narayanan_shrikanth_cv.pdf): USC CV gives this exact Scholar URL; existing CSRankings agrees. |
| Stefan Saroiu | [Scholar](https://scholar.google.com/citations?user=7Z0Z6VsAAAAJ) | [Source](https://www.microsoft.com/en-us/research/people/ssaroiu/): Microsoft systems and security researcher; exact ID from existing Microsoft coauthor records. |
| Steffen Staab | [Scholar](https://scholar.google.com/citations?user=QvpcUn8AAAAJ) | [Source](https://www.ki.uni-stuttgart.de/institute/team/Staab-00003/): Stuttgart AI researcher; exact ID from existing CSRankings. |
| Sumit Gulwani | [Scholar](https://scholar.google.com/citations?user=fZinJ_AAAAAJ) | [Source](https://www.microsoft.com/en-us/research/people/sumitg/publications/): Microsoft program synthesis researcher; exact ID from existing Microsoft coauthor records. |
| Tim Roughgarden | [Scholar](https://scholar.google.com/citations?user=0lcJYs8AAAAJ) | [Source](https://www.wikidata.org/wiki/Q7804199): Wikidata gives this exact ID; existing Columbia CSRankings record agrees. |

Three entries were left blank in this batch:

| ACM Fellow | Reason |
| --- | --- |
| Ian Goldberg | Searches identified the [Waterloo privacy and cryptography researcher](https://cs.uwaterloo.ca/~iang/), but did not establish an exact Scholar profile URL; existing CSRankings also lists `NOSCHOLARPAGE`. |
| Manik Varma | Searches identified the [Microsoft Research researcher](https://www.microsoft.com/en-us/research/people/manik/) and directories advertising Scholar links, but did not resolve an exact profile URL during this batch. |
| Tim Berners-Lee | Searches identified the [MIT researcher and Web inventor](https://www.csail.mit.edu/person/tim-berners-lee), but did not establish an exact Scholar profile URL. |

These unresolved results do not establish that no Scholar profile exists.

## 2026-09-15 - Google Scholar Links: Fifth Web Search Batch

On 2026-09-15, a bounded batch checked the next fifty missing entries in CSV order, skipping the eleven unresolved entries from earlier batches.
The batch contained forty-five Fellows from the 2024 class and five from 2023.
General web search, corroborated where needed by existing CSRankings and cached Scholar coauthor records, established forty-seven clear matches.
The links below were added, bringing the dataset to 950 nonempty Scholar links and 688 blank Scholar cells across 1,638 Fellows.
Only the forty-seven previously blank Scholar URL cells changed in this batch; names and other CSV fields were preserved.
No computer-use tools or project crawlers were used, and no caches, Scholar profile exports, or visualizations were regenerated.
The checks establish identity and link correspondence; they are not fresh audits of Scholar publication lists or metrics.
Existing CSRankings records are from `../bigcows-crawler/.cache/csrankings/csrankings-*.csv`, and cached coauthor evidence is from `../bigcows-crawler/.cache/google-scholar-profile-cache.json`.
Wei Chen was matched through his Microsoft Research page, which explicitly identifies his 2024 ACM Fellowship and Scholar URL; namesakes at Zhejiang and Peking in CSRankings were not used.

| ACM Fellow | Added Scholar Profile | Source and Identity Evidence |
| --- | --- | --- |
| Clark Barrett | [Scholar](https://scholar.google.com/citations?user=BtwmZfQAAAAJ) | [Source](https://research.com/u/clark-barrett): SMT solving and formal verification researcher at Stanford. Exact ID from existing CSRankings: Clark Barrett, Stanford University. |
| Cliff Lampe | [Scholar](https://scholar.google.com/citations?user=aT8oqcoAAAAJ) | [Source](https://research.com/u/cliff-lampe): University of Michigan researcher in online communities and social computing. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=SftrEEMAAAAJ) labeled Cliff Lampe, Professor, School of Information University of Michigan. |
| Dana Randall | [Scholar](https://scholar.google.com/citations?user=6wCEmNYAAAAJ) | [Source](https://www.santafe.edu/people/profile/dana-randall): Georgia Tech professor researching randomized algorithms. Exact ID from existing CSRankings: Dana Randall, Georgia Institute of Technology. |
| Derek Dreyer | [Scholar](https://scholar.google.com/citations?user=1_c89uMAAAAJ) | [Source](https://people.mpi-sws.org/~dreyer/research.html): MPI-SWS programming languages researcher, including RustBelt. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=sCPRIK0AAAAJ) labeled Derek Dreyer, Max Planck Institute for Software Systems (MPI-SWS), Saarland Informatics Campus. |
| Dhabaleswar K Panda | [Scholar](https://scholar.google.com/citations?user=7FXtL98AAAAJ) | [Source](https://dblp.org/pid/p/DhabaleswarKPanda.html): Ohio State researcher; ORCID 0000-0002-0356-1781 matches the cached CSRankings entry. Exact ID from existing CSRankings: Dhabaleswar K. Panda, Ohio State University. |
| Diane Joyce Cook | [Scholar](https://scholar.google.com/citations?user=VpfWvTUAAAAJ) | [Source](https://news.wsu.edu/news/2025/01/22/cook-named-association-for-computing-machinery-fellow/): WSU confirms Diane Cook's ACM Fellowship. Exact ID from existing CSRankings: Diane Joyce Cook, Washington State University. |
| Edward J Delp | [Scholar](https://scholar.google.com/citations?user=qxs5pc4AAAAJ) | [Source](https://engineering.purdue.edu/~ace/): Edward J. Delp at Purdue, researching image and video processing. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=d1KEK84AAAAJ) labeled Edward Delp, Purdue University. |
| Falko Dressler | [Scholar](https://scholar.google.com/citations?user=sK8213AAAAAJ) | [Source](https://www.wikidata.org/wiki/Q23560779): Explicit Scholar ID and TU Berlin affiliation agree with existing CSRankings. Exact ID from existing CSRankings: Falko Dressler, TU Berlin. |
| Fatma Ozcan | [Scholar](https://scholar.google.com/citations?user=JzoifEMAAAAJ) | [Source](https://www.research.google/people/107649/): Fatma Özcan at Google, formerly IBM Almaden, researching database systems. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=D5K6DDcAAAAJ) labeled Fatma Ozcan, Google. |
| Feng Zhao | [Scholar](https://scholar.google.com/citations?user=4C46Y8EAAAAJ) | [Source](https://air.tsinghua.edu.cn/en/info/1046/1190.htm): Feng Zhao's Tsinghua biography confirms earlier Microsoft Research work in sensing and systems. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=5JlEyTAAAAAJ) labeled Feng Zhao, Microsoft Research. |
| Fred Chong | [Scholar](https://scholar.google.com/citations?user=U6OVPVMAAAAJ) | [Source](https://www.cfn.uchicago.edu/people/frederic-chong/): Chicago quantum computing researcher, also known as Frederic T. Chong. Exact ID from existing CSRankings: Fred Chong, University of Chicago. |
| Guoliang Xing | [Scholar](https://scholar.google.com/citations?user=kI5JKs8AAAAJ) | [Source](https://research.cuhk.edu.hk/en/persons/guoliang-xing/): CUHK networked and embedded systems researcher. Exact ID from existing CSRankings: Guoliang Xing, Chinese University of Hong Kong. |
| Haixun Wang | [Scholar](https://scholar.google.com/citations?user=Q1mcglAAAAAJ) | [Source](https://haixun.github.io/): Instacart researcher; personal homepage directly links this exact Scholar URL. |
| Irwin King | [Scholar](https://scholar.google.com/citations?user=MXvC7tkAAAAJ) | [Source](https://www.cse.cuhk.edu.hk/irwin.king/): CUHK professor researching machine intelligence. Exact ID from existing CSRankings: Irwin King, Chinese University of Hong Kong. |
| Jeffrey Michael Heer | [Scholar](https://scholar.google.com/citations?user=vlgs4G4AAAAJ) | [Source](https://homes.cs.washington.edu/~jheer//bio/): UW biography gives the full name Jeffrey Michael Heer and visualization research. Exact ID from existing CSRankings: Jeffrey Michael Heer, University of Washington. |
| Jingren Zhou | [Scholar](https://scholar.google.com/citations?user=64zxhRUAAAAJ) | [Source](https://www.cs.columbia.edu/~jrzhou/): Jingren Zhou's homepage confirms Alibaba and earlier Microsoft database systems work. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=V0lHiEoAAAAJ) labeled Jingren Zhou, Alibaba Group, Microsoft. |
| Justin Zobel | [Scholar](https://scholar.google.com/citations?user=uEHvqE8AAAAJ) | [Source](https://about.unimelb.edu.au/leadership/senior-leadership/deputy-vice-chancellor-research/professor-justin-zobel): University of Melbourne computer scientist and research leader. Exact ID from existing CSRankings: Justin Zobel, University of Melbourne. |
| Lei Chen | [Scholar](https://scholar.google.com/citations?user=gtglwgYAAAAJ) | [Source](https://orcid.org/0000-0002-8257-5806): ORCID explicitly lists the Scholar ID and HKUST identity. Exact ID from existing CSRankings: Lei Chen 0002, HKUST. |
| Luca de Alfaro | [Scholar](https://scholar.google.com/citations?user=gkACFVcAAAAJ) | [Source](https://luca.dealfaro.com/docs/curr.pdf): Luca de Alfaro's CV identifies work in system verification, interface automata, and game theory. Exact ID from existing CSRankings: Luca de Alfaro, Univ. of California - Santa Cruz. |
| Maarten de Rijke | [Scholar](https://scholar.google.com/citations?user=AVDkgFIAAAAJ) | [Source](https://www.uva.nl/over-de-uva/organisatie/hoogleraren/universiteitshoogleraren/maarten-de-rijke.html): Amsterdam professor of AI and information retrieval. Exact ID from existing CSRankings: Maarten de Rijke, University of Amsterdam. |
| Marc Alexa | [Scholar](https://scholar.google.com/citations?user=KNwXLLsAAAAJ) | [Source](https://cg.tu-berlin.de/people/marc-alexa): TU Berlin computer graphics professor. Exact ID from existing CSRankings: Marc Alexa, TU Berlin. |
| Marcelo Arenas | [Scholar](https://scholar.google.com/citations?user=YHR0wkkAAAAJ) | [Source](https://www.marceloarenas.cl/): Catholic University of Chile professor and ACM Fellow researching data management. Exact ID from existing CSRankings: Marcelo Arenas, UC Chile. |
| Marsha Chechik | [Scholar](https://scholar.google.com/citations?user=CYfxRVIAAAAJ) | [Source](https://www.cs.utoronto.ca/~chechik/): Toronto professor researching software engineering and automated verification. Exact ID from existing CSRankings: Marsha Chechik, University of Toronto. |
| Michael Bailey | [Scholar](https://scholar.google.com/citations?user=sMnocAYAAAAJ) | [Source](https://faculty.cc.gatech.edu/~mbailey/): Michael Donald Bailey at Georgia Tech's School of Cybersecurity and Privacy. Exact ID from existing CSRankings: Michael Donald Bailey, Georgia Institute of Technology. |
| Michal Feldman | [Scholar](https://scholar.google.com/citations?user=IKjIhTwAAAAJ) | [Source](https://www.cs.tau.ac.il/~mfeldman/cv-michal.pdf): Tel Aviv professor of computation and economics. Exact ID from existing CSRankings: Michal Feldman, Tel Aviv University. |
| Mira Mezini | [Scholar](https://scholar.google.com/citations?user=ESQUnJEAAAAJ) | [Source](https://www.ae-info.org/ae/Member/Mezini_Mira): TU Darmstadt professor; ORCID 0000-0001-6563-7537 matches CSRankings. Exact ID from existing CSRankings: Mira Mezini, TU Darmstadt. |
| Mohan Kankanhalli | [Scholar](https://scholar.google.com/citations?user=6Lx_eowAAAAJ) | [Source](https://www.comp.nus.edu.sg/~mohan/): NUS AI and multimedia researcher. Exact ID from existing CSRankings: Mohan Kankanhalli, National University of Singapore. |
| Naren Ramakrishnan | [Scholar](https://scholar.google.com/citations?user=fMJwG7MAAAAJ) | [Source](https://website.cs.vt.edu/people/faculty/naren-ramakrishnan.html): Virginia Tech professor researching data science and applied machine learning. Exact ID from existing CSRankings: Naren Ramakrishnan, Virginia Tech. |
| Nate Foster | [Scholar](https://scholar.google.com/citations?user=AH5j40kAAAAJ) | [Source](https://www.cs.cornell.edu/people/nate-foster): Cornell page identifies Nate Foster; existing CSRankings lists his EPFL appointment. Exact ID from existing CSRankings: Nate Foster, EPFL. |
| Niklas Elmqvist | [Scholar](https://scholar.google.com/citations?user=LoQXe24AAAAJ) | [Source](https://www.cs.umd.edu/people/elm): University of Maryland page explicitly lists this Scholar ID for Niklas Elmqvist. Exact ID from existing CSRankings: Niklas Elmqvist, Aarhus University. |
| Peter W O'Hearn | [Scholar](https://scholar.google.com/citations?user=NonivoUAAAAJ) | [Source](https://www.wikidata.org/wiki/Q7176171): Explicit Scholar ID for Peter William O'Hearn, UCL programming languages and verification researcher. |
| Qi Tian | [Scholar](https://scholar.google.com/citations?user=61b6eYkAAAAJ) | [Source](https://www.qitian1987.com/): Huawei AI researcher; personal homepage directly links this exact Scholar URL. |
| Rasmus Pagh | [Scholar](https://scholar.google.com/citations?user=VO4oS8UAAAAJ) | [Source](https://researchprofiles.ku.dk/en/persons/rasmus-pagh/): Copenhagen algorithms researcher; ORCID 0000-0002-1516-9306 matches CSRankings. Exact ID from existing CSRankings: Rasmus Pagh, University of Copenhagen. |
| Satish Chandra | [Scholar](https://scholar.google.com/citations?user=4p8fJSgAAAAJ) | [Source](https://sites.google.com/site/schandraacmorg/): Meta researcher in software engineering and program analysis. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=PMZ1bA4AAAAJ) labeled Satish Chandra, Meta Platforms, Inc.. |
| Scott Hudson | [Scholar](https://scholar.google.com/citations?user=6YU6_QoAAAAJ) | [Source](https://www.cs.cmu.edu/~hudson/): CMU human-computer interaction researcher Scott E. Hudson. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=Hyhp_zUAAAAJ) labeled Scott E. Hudson, Professor of Human-Computer Interaction, Carnegie Mellon University. |
| Stefano Leonardi | [Scholar](https://scholar.google.com/citations?user=p5LCHHEAAAAJ) | [Source](https://phd.uniroma1.it/web/STEFANO-LEONARDI_nC1552_EN.aspx): Sapienza professor researching algorithms, economics and computation. Exact ID from existing CSRankings: Stefano Leonardi 0001, Sapienza University of Rome. |
| Sudip Misra | [Scholar](https://scholar.google.com/citations?user=h33l-A8AAAAJ) | [Source](https://vidwan.inflibnet.ac.in/profile/60468): IIT Kharagpur faculty record explicitly gives this Scholar ID. Exact ID from existing CSRankings: Sudip Misra, IIT Kharagpur. |
| Sudipto Guha | [Scholar](https://scholar.google.com/citations?user=zHCTHbYAAAAJ) | [Source](https://www.umiacs.umd.edu/news-events/news/khuller-wins-esa-test-time-award): Sudipto Guha of UPenn is identified as Samir Khuller's coauthor on approximation algorithms; Khuller's existing cached Scholar page links this exact Guha ID. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=6vXTtDQAAAAJ) labeled Sudipto Guha. |
| Susanne Bodker | [Scholar](https://scholar.google.com/citations?user=tO-dGhkAAAAJ) | [Source](https://www.au.dk/en/show/person/bodker%40cs.au.dk): Aarhus professor Susanne Bødker; ORCID 0000-0002-3571-1617 matches CSRankings. Exact ID from existing CSRankings: Susanne Bødker, Aarhus University. |
| Thad Starner | [Scholar](https://scholar.google.com/citations?user=qr8Vo9IAAAAJ) | [Source](https://faculty.cc.gatech.edu/~thad/): Georgia Tech contextual and wearable computing researcher. Exact ID from existing CSRankings: Thad Starner, Georgia Institute of Technology. |
| Tim J. Menzies | [Scholar](https://scholar.google.com/citations?user=7htTUTgmLtUC) | [Source](https://research.com/u/tim-menzies): North Carolina State software engineering researcher Tim Menzies. Exact ID from existing CSRankings: Tim Menzies, North Carolina State University. |
| Wei Chen | [Scholar](https://scholar.google.com/citations?user=hlEPkxAAAAAJ) | [Source](https://www.microsoft.com/en-us/research/people/weic/news-and-awards/): Microsoft page confirms the 2024 ACM Fellowship and directly links this exact Scholar URL; Zhejiang and Peking CSRankings namesakes were rejected. |
| Aditya Akella | [Scholar](https://scholar.google.com/citations?user=d_rxnzAAAAAJ) | [Source](https://www.cs.utexas.edu/people/faculty-researchers/aditya-akella): UT Austin networking researcher, previously UW-Madison. Exact ID from existing CSRankings: Aditya Akella, University of Texas at Austin. |
| Albrecht Schmidt | [Scholar](https://scholar.google.com/citations?user=qM5jR7YAAAAJ) | [Source](https://www.um.informatik.uni-muenchen.de/personen/professoren/schmidt/index.html): LMU professor researching human-computer interaction and ubiquitous computing. Exact ID from existing CSRankings: Albrecht Schmidt 0001, LMU Munich. |
| Alexander Szalay | [Scholar](https://scholar.google.com/citations?user=rUiWchkAAAAJ) | [Source](https://research.com/u/a-s-szalay): Johns Hopkins astrophysicist and data-intensive science researcher Alexander S. Szalay. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=Dn4kkYUAAAAJ) labeled A. S. Szalay, Blooomberg Distinguished Professor, Johns Hopkins University. |
| Anand Raghunathan | [Scholar](https://scholar.google.com/citations?user=OP7F8jEAAAAJ) | [Source](https://engineering.purdue.edu/~araghu/main.html): Purdue Integrated Systems Laboratory researcher in VLSI and computer engineering. Exact ID from an existing [cached coauthor record](https://scholar.google.com/citations?user=R-z1R84AAAAJ) labeled Anand Raghunathan, Silicon Valley Chair Professor of Electrical and Computer Engineering, Purdue University. |
| Andreas Krause | [Scholar](https://scholar.google.com/citations?user=eDHv58AAAAAJ) | [Source](https://las.inf.ethz.ch/wp-content/uploads/2021/01/krause-cv-2p.pdf): ETH machine learning researcher Andreas Krause. Exact ID from existing CSRankings: Andreas Krause 0001, ETH Zurich. |

Three entries were left blank in this batch:

| ACM Fellow | Reason |
| --- | --- |
| Guoliang Li | Existing CSRankings gives `s9n7-fQAAAAJ` for the Tsinghua database researcher, while an [indexed profile directory](https://www.newx.sg/scholar/Pi89P8kAAAAJ) gives `Pi89P8kAAAAJ` with the same name and affiliation; the [Tsinghua homepage](https://dbgroup.cs.tsinghua.edu.cn/ligl/) established identity but did not resolve the conflicting Scholar URLs, so neither candidate was selected. |
| Russell Housley | Searches for Russell and Russ Housley identified the [Vigil Security and IETF researcher](https://datatracker.ietf.org/person/Russ%20Housley), but did not establish an exact Scholar profile URL. |
| Stephen David Crocker | Searches under Stephen David Crocker, Stephen Crocker, and Steve Crocker did not establish an exact Scholar profile URL for the Internet pioneer. |

These unresolved results do not establish that no Scholar profile exists.

## 2026-09-15 - Google Scholar Links: Fourth Web Search Batch

On 2026-09-15, a bounded batch checked the next fifty missing entries in CSV order, skipping the six unresolved entries from earlier batches.
The batch contained forty-one Fellows from the 2025 class and nine from 2024.
General web search, corroborated where needed by existing CSRankings and cached Scholar coauthor records, established forty-five clear matches.
The links below were added, bringing the dataset to 903 nonempty Scholar links and 735 blank Scholar cells across 1,638 Fellows.
Only the forty-five previously blank Scholar URL cells changed in this batch; names and other CSV fields were preserved.
No computer-use tools or project crawlers were used, and no caches, Scholar profile exports, or visualizations were regenerated.
The checks establish identity and link correspondence; they are not fresh audits of Scholar publication lists or metrics.
Existing CSRankings records are from `../bigcows-crawler/.cache/csrankings/csrankings-*.csv`, and cached coauthor evidence is from `../bigcows-crawler/.cache/google-scholar-profile-cache.json`.
Some CSRankings entries marked `NOSCHOLARPAGE` had independently supported links; the cached CSRankings files were not modified.

| ACM Fellow | Added Scholar Profile | Source and Identity Evidence |
| --- | --- | --- |
| Ke Yi | [Scholar](https://scholar.google.com/citations?user=dWcZPFEAAAAJ) | [Source](https://seng.hkust.edu.hk/about/people/faculty/ke-yi): HKUST faculty page supplies the exact Scholar ID. |
| Ken-Ichi Kawarabayashi | [Scholar](https://scholar.google.com/citations?user=DWERCmsAAAAJ) | [Source](https://www.newx.sg/scholar/DWERCmsAAAAJ): NII/Tokyo graph theorist; exact ID agrees with an existing cached coauthor record. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=UPBuOPIAAAAJ). |
| Kian-Lee Tan | [Scholar](https://scholar.google.com/citations?user=JQ-sxKYAAAAJ) | [Source](https://research.com/u/kian-lee-tan): NUS database researcher; exact ID from an existing cached coauthor record naming NUS. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=9560QjYAAAAJ). |
| Kwang-Ting Cheng | [Scholar](https://scholar.google.com/citations?user=-SgpaF8AAAAJ) | [Source](https://ece.hkust.edu.hk/timcheng): HKUST faculty page links this exact Scholar URL for Tim Kwang-Ting Cheng, electronic design automation researcher. |
| Li Xiong | [Scholar](https://scholar.google.com/citations?user=jJ8BLgsAAAAJ) | [Source](https://cs.emory.edu/~lxiong/): Emory privacy researcher; exact ID agrees with the existing CSRankings record. |
| Luca P Carloni | [Scholar](https://scholar.google.com/citations?user=sEAoh3MAAAAJ) | [Source](https://www.alphaxiv.org/%40luca-carloni): Columbia researcher in systems on chip; exact ID from the existing CSRankings record for Luca P. Carloni. |
| Lujo Bauer | [Scholar](https://scholar.google.com/citations?user=5cJzDZEAAAAJ) | [Source](https://engineering.cmu.edu/directory/bios/bauer-lujo.html): CMU security researcher; exact ID agrees with the existing CSRankings record. |
| Madanlal Musuvathi | [Scholar](https://scholar.google.com/citations?user=6ENuGyoAAAAJ) | [Source](https://www.microsoft.com/en-us/research/people/madanm/): Microsoft Research page uses Madan Musuvathi; cached coauthor record gives Madanlal Musuvathi, Microsoft Research, and this ID. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=d2f0VUQAAAAJ). |
| Marco Dorigo | [Scholar](https://scholar.google.com/citations?user=PwYT6EMAAAAJ) | [Source](https://iridia.ulb.ac.be/~mdorigo/HomePageDorigo/): ULB swarm intelligence researcher; exact ID agrees with the existing CSRankings record. |
| Michael L Gleicher | [Scholar](https://scholar.google.com/citations?user=kDkH9UkAAAAJ) | [Source](https://pages.cs.wisc.edu/~pubs/faculty-info/gleicher.html): Wisconsin faculty page identifies Michael L. Gleicher; exact ID from CSRankings under Michael Gleicher at Wisconsin. |
| Mohamed F Mokbel | [Scholar](https://scholar.google.com/citations?user=GHz1ZVIAAAAJ) | [Source](https://cse.umn.edu/dsi/mohamed-f-mokbel): Minnesota data systems researcher; exact ID agrees with the existing CSRankings record. |
| Nenad Medvidovic | [Scholar](https://scholar.google.com/citations?user=kqW_-2gAAAAJ) | [Source](https://softarch.usc.edu/~neno/): USC software architecture researcher; exact ID agrees with the existing CSRankings record. |
| Noam Nisan | [Scholar](https://scholar.google.com/citations?user=zXQZPnMAAAAJ) | [Source](https://cris.huji.ac.il/en/persons/noam-nisan/): Hebrew University computer scientist; exact ID agrees with the existing CSRankings record. |
| Oded Regev | [Scholar](https://scholar.google.com/citations?user=3-gk0ioAAAAJ) | [Source](https://cims.nyu.edu/people/profiles/REGEV_Oded.html): NYU Courant computer scientist; exact ID from CSRankings for Oded Regev 0001 at NYU. |
| Odest Chadwicke Jenkins | [Scholar](https://scholar.google.com/citations?user=dp5LnVAAAAAJ) | [Source](https://en.wikipedia.org/wiki/Odest_Chadwicke_Jenkins): Michigan robotics researcher; exact ID agrees with the existing CSRankings record. |
| Paolo Ferragina | [Scholar](https://scholar.google.com/citations?user=3EILU3MAAAAJ) | [Source](https://pages.di.unipi.it/ferragina/index.html): Pisa algorithms and data structures researcher; exact ID agrees with the existing CSRankings record. |
| Pei Cao | [Scholar](https://scholar.google.com/citations?user=JHwivywAAAAJ) | [Source](https://crypto.stanford.edu/~cao/): Stanford distributed systems and networking researcher; cached coauthor record names Google and Stanford and supplies this exact ID. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=7b858c0AAAAJ). |
| Peter Müller | [Scholar](https://scholar.google.com/citations?user=iJ0qZckAAAAJ) | [Source](https://www.pm.inf.ethz.ch/people/personal/pmueller-pers.html): ETH program verification researcher; exact ID from CSRankings for Peter Müller 0001 at ETH. |
| Rajkumar Buyya | [Scholar](https://scholar.google.com/citations?user=7xN6JqYAAAAJ) | [Source](https://clouds.cis.unimelb.edu.au/~rbuyya/welcome/biography.html): Melbourne cloud computing researcher; exact ID agrees with the existing CSRankings record. |
| Ratul Mahajan | [Scholar](https://scholar.google.com/citations?user=Sh1yq5QAAAAJ) | [Source](https://ratul.org/): University of Washington networking researcher; exact ID agrees with the existing CSRankings record. |
| Rebecca N. Wright | [Scholar](https://scholar.google.com/citations?user=L-xeJPoAAAAJ) | [Source](https://barnard.edu/profiles/rebecca-wright): Barnard computer scientist; cached coauthor record names Barnard and supplies this exact ID. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=IAeKTGsAAAAJ). |
| Sheelagh Carpendale | [Scholar](https://scholar.google.com/citations?user=43LLX2kAAAAJ) | [Source](https://ilab.ucalgary.ca/people/sheelagh-carpendale/): Visualization researcher with Calgary and SFU affiliations; exact ID agrees with the existing SFU CSRankings record. |
| Stephanie Weirich | [Scholar](https://scholar.google.com/citations?user=-vC_l2kAAAAJ) | [Source](https://www.wikidata.org/wiki/Q57268372): Explicit Scholar ID agrees with existing cached coauthor records naming UPenn. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=2kkddh0AAAAJ). |
| Steve Hodges | [Scholar](https://scholar.google.com/citations?user=7-H0ry4AAAAJ) | [Source](https://research.lancaster-university.uk/en/persons/steve-hodges/): Lancaster researcher associated with micro:bit and SenseCam; cached coauthor record names Lancaster and supplies this exact ID. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=d2f0VUQAAAAJ). |
| Sven Apel | [Scholar](https://scholar.google.com/citations?user=_4ssMloAAAAJ) | [Source](https://www.se.cs.uni-saarland.de/apel/): Saarland software engineering researcher; exact ID agrees with the existing CSRankings record. |
| Swarat Chaudhuri | [Scholar](https://scholar.google.com/citations?user=9j6RBYQAAAAJ) | [Source](https://www.cs.utexas.edu/people/faculty-researchers/swarat-chaudhuri): UT Austin researcher in formal methods and AI; exact ID agrees with the existing CSRankings record. |
| Sylvia Ratnasamy | [Scholar](https://scholar.google.com/citations?user=sAdDcvQAAAAJ) | [Source](https://vcresearch.berkeley.edu/faculty/sylvia-ratnasamy): Berkeley networking researcher; exact ID agrees with the existing CSRankings record. |
| Tadayoshi Kohno | [Scholar](https://scholar.google.com/citations?user=s_YDrrgAAAAJ) | [Source](https://ischool.uw.edu/people/faculty/profile/kohno): Security researcher; exact ID from the existing University of Washington CSRankings record, with ORCID 0000-0002-4899-226X. |
| Tao Mei | [Scholar](https://scholar.google.com/citations?user=7Yq4wf4AAAAJ) | [Source](https://taomei.me/): HiDream.ai founder; cached coauthor records identify the same affiliation and exact ID. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=CcbnBvgAAAAJ). |
| Themis Palpanas | [Scholar](https://scholar.google.com/citations?user=qUBdmWgAAAAJ) | [Source](https://dblp.org/pid/p/ThemisPalpanas.html): DBLP author page links this exact Scholar URL, names Paris Descartes and ORCID 0000-0002-8031-0265; personal homepage corroborates data series research at Paris Cité. |
| Theodore Rappaport | [Scholar](https://scholar.google.com/citations?user=aLOSzWwAAAAJ) | [Source](https://wireless.engineering.nyu.edu/tedrappaport-publications/): NYU Wireless researcher; exact ID from CSRankings under Theodore S. Rappaport at NYU. |
| Tommaso Melodia | [Scholar](https://scholar.google.com/citations?user=WzLpSRkAAAAJ) | [Source](https://www.newx.sg/scholar/WzLpSRkAAAAJ): Northeastern networking researcher; explicit ID agrees with the existing cached coauthor record. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=rAGwv14AAAAJ). |
| Wolfgang Heidrich | [Scholar](https://scholar.google.com/citations?user=IQSbom0AAAAJ) | [Source](https://www.kaust.edu.sa/en/study/faculty/wolfgang-heidrich): KAUST computational imaging researcher; exact ID agrees with the existing CSRankings record. |
| Wolfgang Lehner | [Scholar](https://scholar.google.com/citations?user=YYzvyMQAAAAJ) | [Source](https://en.wikipedia.org/wiki/Wolfgang_Lehner): Dresden database researcher; exact ID agrees with the existing CSRankings record. |
| Xiaohua Jia | [Scholar](https://scholar.google.com/citations?user=L5iEhq0AAAAJ) | [Source](https://scholars.cityu.edu.hk/en/persons/csjia/): CityU faculty page supplies this exact Scholar ID, also present in the existing CSRankings record. |
| Yu Zheng | [Scholar](https://scholar.google.com/citations?user=juUcdgYAAAAJ) | [Source](https://hei77.github.io/yuzheng-student/): JD.com urban computing researcher; cached coauthor records name JD.com and Southwest Jiaotong and supply this exact ID. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=FyUQvCoAAAAJ). |
| Yun Raymond Fu | [Scholar](https://scholar.google.com/citations?user=h-JEcQ8AAAAJ) | [Source](https://www.khoury.northeastern.edu/people/raymond-yun-fu/): Northeastern faculty page identifies Raymond (Yun) Fu; exact ID from CSRankings under Yun Fu 0001 at Northeastern. |
| Zi Helen Huang | [Scholar](https://scholar.google.com/citations?user=PnBlwhgAAAAJ) | [Source](https://staff.itee.uq.edu.au/huang/): Queensland multimedia researcher identified as Zi (Helen) Huang; exact ID agrees with the existing CSRankings record. |
| Abhik Roychoudhury | [Scholar](https://scholar.google.com/citations?user=UxFWSJIAAAAJ) | [Source](https://abhikrc.com/): NUS software researcher; exact ID agrees with the existing CSRankings record. |
| Arindam Banerjee | [Scholar](https://scholar.google.com/citations?user=RY7cuPAAAAAJ) | [Source](https://arindam.cs.illinois.edu/): Illinois machine learning researcher; exact ID from CSRankings under Arindam Banerjee 0001 at Illinois. |
| Ashish Goel | [Scholar](https://scholar.google.com/citations?user=B_rKfusAAAAJ) | [Source](https://research.com/u/ashish-goel): Stanford algorithms researcher; exact ID agrees with the existing Stanford CSRankings record. |
| Bashar A Nuseibeh | [Scholar](https://scholar.google.com/citations?user=aUQ8O9gAAAAJ) | [Source](https://www.wikidata.org/wiki/Q102403083): Explicit Scholar ID agrees with CSRankings under Bashar Ahmad Nuseibeh and with an existing cached coauthor record. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=Y8BLBGcAAAAJ). |
| Benjamin G Zorn | [Scholar](https://scholar.google.com/citations?user=mpar-iAAAAAJ) | [Source](https://www.microsoft.com/en-us/research/people/zorn/news-and-awards/): Microsoft Research page uses Ben Zorn; cached coauthor record names Benjamin Zorn at Microsoft Research Redmond and supplies this ID. Existing coauthor evidence: [cached source profile](https://scholar.google.com/citations?user=Rt1a5-6vh4UC). |
| Brian Curless | [Scholar](https://scholar.google.com/citations?user=tlh8i7gAAAAJ) | [Source](https://research.com/u/brian-curless): University of Washington 3D reconstruction researcher; exact ID agrees with the existing CSRankings record. |
| Carla Fabiana Chiasserini | [Scholar](https://scholar.google.com/citations?user=np0OO24AAAAJ) | [Source](https://www.5gitaly.eu/2019/team-member/chiasserini-carla-2/): Conference speaker biography names Politecnico di Torino, networking research, and explicitly supplies this exact Scholar URL. |

Five entries were left blank in this batch:

| ACM Fellow | Reason |
| --- | --- |
| Nandita Dukkipati | Searches and the [Google Research page](https://research.google/people/author39115/) established the researcher but did not establish an exact Scholar profile URL. |
| Natarajan Shankar | Searches and the [SRI homepage](https://www.csl.sri.com/users/shankar/) established the formal methods researcher but did not establish an exact Scholar profile URL. |
| Yan Solihin | Existing CSRankings gives `sUQFclgAAAAJ`, while [Florida ExpertNet](https://expertnet.org/index.cfm?fuseaction=experts.details&id=130969) lists `tndlIesAAAAJ` inside a malformed URL; the Scholar link on the [ARPERS homepage](https://sites.google.com/view/arpers) could not be resolved through the web tool, so neither candidate was selected. |
| Anwar Walid | Searches did not establish an exact Scholar profile URL; the Scholar link appearing in results for the [Michigan Tech staff page](https://www-cf.mtu.edu/icc/about/staff/) belongs to another staff entry. |
| Azad M Madni | Searches found the systems engineering researcher, including a [CORE Academy biography](https://coreacad.org/Member.aspx?ProId=155), but did not establish an exact Scholar profile URL. |

These unresolved results do not establish that no Scholar profile exists.

## 2026-09-15 - Google Scholar Links: Third Web Search Batch

On 2026-09-15, a bounded batch checked the next twenty missing entries in CSV order, skipping the five unresolved entries from the previous batches.
All twenty were from the 2025 class.
General web search, together with existing CSRankings and cached Scholar coauthor records, established nineteen clear matches.
The nineteen links below were added, bringing the dataset to 858 nonempty Scholar links and 780 blank Scholar cells across 1,638 Fellows.
No computer-use tools or crawlers were used; caches, the Scholar profile export, and the visualization were left unchanged.
These are identity and link reconciliations, not fresh audits of the profiles' publication lists or metrics.

| ACM Fellow | Added Scholar Profile | Source and Identity Evidence |
| --- | --- | --- |
| Cynthia Rudin | [Scholar](https://scholar.google.com/citations?user=mezKJyoAAAAJ) | [Source](https://www.newx.sg/scholar/mezKJyoAAAAJ): Exact ID and Duke machine learning identity in web result; existing CSRankings agrees. |
| Dejan S Milojicic | [Scholar](https://scholar.google.com/citations?user=4VqLAT8AAAAJ) | [Source](https://research.com/u/dejan-milojicic): Web source identifies the HP distributed systems researcher; exact ID appears in existing Scholar coauthor links from profiles ohjQPx8AAAAJ and wR_tv-kAAAAJ, labeled Hewlett Packard Labs. |
| Deming Chen | [Scholar](https://scholar.google.com/citations?user=A_A_LrsAAAAJ) | [Source](https://www.newx.sg/scholar/A_A_LrsAAAAJ): Exact ID and Illinois FPGA/high-level synthesis identity in web result; existing CSRankings agrees. |
| Denys Poshyvanyk | [Scholar](https://scholar.google.com/citations?user=gyLFs0IAAAAJ) | [Source](https://www.cs.wm.edu/~dposhyvanyk/index.html): William & Mary software analytics researcher; exact ID from existing CSRankings, with a Scholar profile also listed by Research.com. |
| Eytan Adar | [Scholar](https://scholar.google.com/citations?user=4tMapHYAAAAJ) | [Source](https://www.cond.org/): Michigan personal page lists Scholar; exact ID from existing CSRankings for the same homepage and affiliation. |
| Franck Cappello | [Scholar](https://scholar.google.com/citations?user=z5u02kIAAAAJ) | [Source](https://franckcappello.github.io/): Personal CV identifies Argonne HPC, fault tolerance, and compression research and lists Scholar; exact ID appears in existing Scholar coauthor links from HaI6LesAAAAJ and UcWOl8YAAAAJ, labeled Argonne. |
| Gail-Joon Ahn | [Scholar](https://scholar.google.com/citations?user=_dzO69sAAAAJ) | [Source](https://search.asu.edu/profile/1258895): ASU directory explicitly gives this Scholar URL; security research and existing CSRankings agree. |
| George Candea | [Scholar](https://scholar.google.com/citations?user=Yd-SGH8AAAAJ) | [Source](https://people.epfl.ch/george.candea?lang=en): EPFL directory confirms the Dependable Systems Lab researcher; exact ID from existing CSRankings with the same lab homepage. |
| George Drettakis | [Scholar](https://scholar.google.com/citations?user=LGo5J4IAAAAJ) | [Source](https://www.wikidata.org/wiki/Q102306354): Exact ID in Wikidata agrees with existing coauthor link in NJ9c4ygAAAAJ, labeled Inria/GRAPHDECO; DBLP and Research.com corroborate graphics publications. |
| Gookwon Edward Suh | [Scholar](https://scholar.google.com/citations?user=neO3vFYAAAAJ) | [Source](https://research.nvidia.com/person/edward-suh): NVIDIA web result explicitly exposes this Scholar ID for Edward Suh; existing coauthor links in ovlpa_IAAAAJ and y80AokkAAAAJ identify NVIDIA/Cornell, and Cornell records connect the full name Gookwon Edward Suh. |
| Hai Jin | [Scholar](https://scholar.google.com/citations?user=o02W0aEAAAAJ) | [Source](https://research.com/u/hai-jin): Web source identifies the Huazhong computing researcher through affiliation and cloud/MapReduce publications; exact ID from existing CSRankings Hai Jin 0001 at HUST. |
| Hanghang Tong | [Scholar](https://scholar.google.com/citations?user=RaINcuUAAAAJ) | [Source](https://grainger.illinois.edu/about/directory/faculty/htong): Illinois directory confirms graph mining research and lists Scholar; exact ID from existing CSRankings. |
| Hui Xiong | [Scholar](https://scholar.google.com/citations?user=cVDF1tkAAAAJ) | [Source](https://ailab.hkust-gz.edu.cn/): Personal institutional page confirms AI, data mining, mobile computing, and Rutgers/HKUST history and lists Scholar; exact ID from existing CSRankings Hui Xiong 0001. |
| Javier Esparza | [Scholar](https://scholar.google.com/citations?user=c9qgPSYAAAAJ) | [Source](https://en.wikipedia.org/wiki/Javier_Esparza_%28computer_scientist%29): Computing biography identifies the TU Munich researcher and lists Scholar; exact ID from existing CSRankings. |
| Jian Ma | [Scholar](https://scholar.google.com/citations?user=kDZcBhkAAAAJ) | **Superseded:** See the [later wrong-person correction](#2026-09-15-1627-edt---name-corrections-and-wrong-person-scholar-link-removal). Initial rationale: [Source](https://www.cmu.edu/computational-cancer/faculty/ma_jian.html): CMU directory confirms computational genomics identity and lists Scholar; exact ID from existing CSRankings Jian Ma 0004 at CMU. |
| Jiaya Jia | [Scholar](https://scholar.google.com/citations?user=XPAkzTEAAAAJ) | [Source](https://facultyprofiles.hkust.edu.hk/profiles.php?profile=jiaya-jia-jia): HKUST faculty directory explicitly lists this Scholar ID, matching existing CSRankings and computer vision research. |
| Jun Zhu | [Scholar](https://scholar.google.com/citations?user=axsP38wAAAAJ) | [Source](https://ml.cs.tsinghua.edu.cn/~jun/index.shtml): Search-indexed personal page identifies Tsinghua probabilistic machine learning researcher; exact ID from existing CSRankings Jun Zhu 0001 with the same homepage. |
| Junfeng Yang | [Scholar](https://scholar.google.com/citations?user=JJ9AvbAAAAAJ) | [Source](https://www.cs.columbia.edu/~junfeng/): Columbia personal page confirms software systems identity and lists Scholar; exact ID from existing CSRankings with the same homepage. |
| Kate Starbird | [Scholar](https://scholar.google.com/citations?user=C6KSF5gAAAAJ) | [Source](https://www.wikidata.org/wiki/Q3813333): Exact Scholar ID in Wikidata; UW HCDE directory independently confirms crisis informatics identity and lists a Scholar profile. |

Eric Allman's cell was left blank because general web searches and his personal homepage did not establish a confident Scholar profile URL in this batch.
This does not establish that no profile exists.

## 2026-09-15 - Google Scholar Links: Second Web Search Batch

On 2026-09-15, the next bounded batch checked the first ten missing Scholar entries in CSV order, all from the 2025 class.
General web search and existing local records established nine clear matches, which were added below.
For Adam Wierman, Aggelos Kiayias, and Cristina Conati, browser inspection also exposed the destination URLs of links on their personal pages.
The remaining work used general tool calls and web search.
At completion, the ACM Fellows dataset contained 839 nonempty Scholar links and 799 blank Scholar cells across 1,638 Fellows.
No crawlers were run, caches refreshed, or Scholar metrics retrieved; the visualization was left unchanged for later regeneration.

| ACM Fellow | Added Scholar Profile | Source and Identity Evidence |
| --- | --- | --- |
| Adam Wierman | [Scholar](https://scholar.google.com/citations?user=4OvOdSgAAAAJ) | [Source](https://adamwierman.com/research/): Personal research page links directly to Scholar; Caltech sustainable computing researcher. |
| Aggelos Kiayias | [Scholar](https://scholar.google.com/citations?user=P_L_vZAAAAAJ) | [Source](https://kiayias.com/Aggelos_Kiayias/Home_of_Aggelos_Kiayias.html): Personal page links directly to Scholar; Edinburgh cryptography researcher. |
| Alessandro Orso | [Scholar](https://scholar.google.com/citations?user=wCfYkMkAAAAJ) | [Source](https://dblp.org/pid/35/805.html): DBLP lists a Scholar profile and software testing publications; exact ID corroborated by existing CSRankings records and the web-indexed CSRankings mirror. |
| Alistair M Moffat | [Scholar](https://scholar.google.com/citations?user=r3xSME0AAAAJ) | [Source](https://research.com/u/alistair-moffat): Web result identifies the Melbourne information retrieval researcher and lists a Scholar link; exact ID comes from existing CSRankings records for Alistair Moffat. |
| Angela Bonifati | [Scholar](https://scholar.google.com/citations?user=0RdtBlUAAAAJ) | [Source](https://intendproject.eu/project/advisory-board): Project advisory board explicitly lists this Scholar URL for Angela Bonifati at Lyon 1 University; her personal page confirms database research. |
| Antonio Torralba | [Scholar](https://scholar.google.com/citations?user=8cxDHS4AAAAJ) | [Source](https://www.wikidata.org/wiki/Q56676344): Exact Scholar ID is attributed to the MIT lab page; existing CSRankings records agree and identify the MIT computer vision researcher. |
| Ariel Procaccia | [Scholar](https://scholar.google.com/citations?user=8ZpV-lkAAAAJ) | [Source](https://www.wikidata.org/wiki/Q20675644): Exact Scholar ID for Ariel D. Procaccia agrees with existing Harvard CSRankings records and the personal website. |
| Baoquan Chen | [Scholar](https://scholar.google.com/citations?user=iHWtrEAAAAAJ) | [Source](https://baoquanchen.info/): Personal page identifies the Peking University graphics researcher and ACM Fellow; exact ID comes from existing CSRankings records with matching affiliation and ORCID. |
| Cristina Conati | [Scholar](https://scholar.google.com/citations?user=Ytp9oFQAAAAJ) | [Source](https://www.cs.ubc.ca/~conati/publications.php): UBC personal publications page links directly to this Scholar profile. |

Athina Markopoulou's cell was left blank because this batch did not confidently resolve the exact Scholar URL; this does not imply that she has no profile.

## 2026-09-15 - Google Scholar Links: First Web Search Batch

On 2026-09-15, general web search identified six strong profile matches in a random sample of ten Fellows with blank Scholar cells (sample seed `13599039689330591045`).
The six links below were added, bringing the dataset to 830 nonempty Scholar links and 808 blank Scholar cells across 1,638 Fellows.
Matching used the linked web sources and corroborating existing local records; no crawlers were run or caches refreshed.
The new profile contents were not retrieved or audited, and citation metrics were unavailable for these six profiles in the export used for this batch.
The citation visualization was regenerated using the existing data.

| ACM Fellow | Added Scholar Profile | Supporting Source |
| --- | --- | --- |
| Prashant J Shenoy | [Scholar](https://scholar.google.com/citations?user=TciP6mcAAAAJ) | [UMass personal page](https://people.cs.umass.edu/~shenoy/) |
| Donald F Towsley | [Scholar](https://scholar.google.com/citations?user=KIFPVWoAAAAJ) | [University of Arizona CQN](https://cqn-erc.arizona.edu/person/don-towsley) |
| Jessica K Hodgins | [Scholar](https://scholar.google.com/citations?user=vswo4rQAAAAJ) | [Wikipedia biography](https://de.wikipedia.org/wiki/Jessica_Hodgins) |
| Jeffrey A Dean | [Scholar](https://scholar.google.com/citations?user=NMS69lQAAAAJ) | [Google Research](https://research.google.com/people/jeff) |
| Joseph M Hellerstein | [Scholar](https://scholar.google.com/citations?user=uFJi3IUAAAAJ) | [Berkeley Institute for Data Science](https://bids.berkeley.edu/people/joseph-hellerstein) |
| Claudio T. Silva | [Scholar](https://scholar.google.com/citations?user=YIwiAAsAAAAJ) | [Personal CV](https://ctsilva.github.io/cv/) |

No confident profile match was found for the other four sampled Fellows: Jack Dennis, Maurice V. Wilkes, Ambuj Goyal, and John B Goodenough.
Their Scholar cells were left blank in this batch; unsuccessful searches do not establish that profiles do not exist.

## 2026-09-15 - Google Scholar Profile Reconciliation

On 2026-09-15, a cache-only review of the 853 linked ACM Fellow Scholar profiles identified 29 high-confidence wrong-person links.
All reviewed Scholar pages were captured on 2026-04-30; the review also used the retained ACM captures from 2026-09-13 and local CSRankings records.
No fresh crawling was performed.
The 29 incorrect `google_scholar_profile` cells were cleared, preserving every Fellow row and all award fields.
After clearing these links, the dataset had 824 nonempty Scholar links and 814 blank Scholar cells across 1,638 Fellows.
No replacement URLs were inserted because the alternate IDs found locally did not have captured Scholar pages available for verification.
The shared Scholar cache and profile export were retained; clearing the join prevents these profiles from contributing to the affected Fellows, while preserving captures and profiles that may be used elsewhere.
The ACM Fellow citation visualization was regenerated from the corrected joins.

Canonical name changes were limited to capitalization: `MITCHELL WAND` became `Mitchell Wand`, and `Xuelong LI` became `Xuelong Li`.
Names differing by accents, initials, nicknames, or ordering were preserved.
In particular, Alan Newell remains Alan Newell; his former Scholar link pointed to Allen Newell, a different person.

### 2026-09-15 - Removed Scholar Links

The former URLs and identity conflicts are retained below so subsequent exports or enrichment do not reassign the rejected IDs to the same Fellows.
Each exclusion applies to the named ACM Fellow; a URL may still be valid for a different person.
Later enrichment batches supplied reviewed replacements for some of these Fellows, while preserving this record of the rejected links.

| ACM Fellow | Former Scholar Profile | Cached Identity Conflict |
| --- | --- | --- |
| Chung C. J Kuo | [Chung Feng Jeffrey Kuo](https://scholar.google.com/citations?user=7zNrjLsAAAAJ) | Materials researcher Chung Feng Jeffrey Kuo; ACM recognizes visual computing. |
| Hai Li | [Hai LI](https://scholar.google.com/citations?user=u7xU-J4AAAAJ) | Nanjing Tech materials researcher; ACM recognizes neuromorphic computing and deep-learning acceleration. |
| Meenakshi Balakrishnan | [Meenakshi P. Balakrishnan](https://scholar.google.com/citations?user=G8StE6wAAAAJ) | Clinical project manager publishing on emergency medicine and cardiac biology; ACM recognizes embedded systems and assistive technology. |
| Antonio Gonzalez | [Antonio González](https://scholar.google.com/citations?user=d5EXd78AAAAJ) | UC San Diego microbiome/QIIME researcher; ACM recognizes computer architecture in Spain. |
| Brian Levine | [Brian Levine](https://scholar.google.com/citations?user=Q5nMrwkAAAAJ) | Toronto/Baycrest neuropsychologist; ACM recognizes network forensics, security, and privacy. |
| David Brooks | [David J Brooks](https://scholar.google.com/citations?user=TaiBcxgAAAAJ) | Newcastle PET/neuroimaging researcher David J Brooks; ACM recognizes power-efficient computer architecture. |
| Kun Zhou | [Kun Zhou](https://scholar.google.com/citations?user=Xk9oMnIAAAAJ) | Nanyang materials/mechanics researcher; ACM recognizes computer graphics. |
| Mona Singh | [Mona Singh](https://scholar.google.com/citations?user=JpAehzgAAAAJ) | Consultant publishing touchscreen and task-reminder patents; ACM recognizes computational protein biology. |
| Xiangyang Li | [Xiangyang Li](https://scholar.google.com/citations?user=wZKoSgsAAAAJ) | Agricultural-university bacterial-genomics profile, also containing unrelated papers; ACM recognizes IoT and mobile systems. |
| Ravi Kannan | [Ravishekar (Ravi) Kannan](https://scholar.google.com/citations?user=jSk1DpYAAAAJ) | Ravishekar Kannan at CFD Research, publishing fluid solvers and aerosol deposition; ACM recognizes theoretical computer science. |
| Valerie Taylor | [valerie taylor](https://scholar.google.com/citations?user=4YCIGjAAAAAJ) | Calgary psychiatry/obesity researcher; the local CSRankings record identifies the computing Fellow at Texas A&M. |
| Kevin Fall | [Kevin Fall](https://scholar.google.com/citations?user=g848MeMAAAAJ) | Texas State counseling professor; ACM recognizes delay-tolerant networking. |
| Robert Schreiber | [Robert Schreiber](https://scholar.google.com/citations?user=kd-l1MoAAAAJ) | Washington University cancer immunologist; ACM recognizes matrix computations and parallel scientific computing. |
| Ming C Lin | [Ming Chang Lin](https://scholar.google.com/citations?user=HfDqADkAAAAJ) | Chemist Ming Chang Lin; ACM recognizes geometric modeling and computer graphics. |
| Peter Magnusson | [S. Peter Magnusson](https://scholar.google.com/citations?user=DYwLYXQAAAAJ) | Copenhagen muscle/tendon researcher S. Peter Magnusson; ACM recognizes full-system simulation. |
| Alan Newell | [Allen Newell](https://scholar.google.com/citations?user=5WfqzjkAAAAJ) | Allen Newell at Carnegie Mellon, publishing AI/cognition work; the ACM Fellow is Alan Newell, recognized for systems for people with disabilities. Do not change Alan to Allen. |
| Ming Li | [Ming Li](https://scholar.google.com/citations?user=c_d8tzoAAAAJ) | Northwest A&F ecology profile with a heterogeneous publication list; ACM recognizes computational complexity. |
| Hui Zhang | [Hui Zhang](https://scholar.google.com/citations?user=iXtCV_QAAAAJ) | TUST iris/biometrics researcher; ACM recognizes network architecture, protocols, and algorithms. |
| Michel Dubois | [Michel J.F. Dubois](https://scholar.google.com/citations?user=DreIyPUAAAAJ) | UniLaSalle agriculture/biotechnology researcher Michel J.F. Dubois; ACM recognizes multiprocessor memory systems. |
| Neil Jones | [R. Neil Jones](https://scholar.google.com/citations?user=GgHEYEIAAAAJ) | Genetics profile R. Neil Jones, also containing heterogeneous biomedical papers; ACM recognizes compilation and partial evaluation. |
| Alan C Shaw | [Allan Clarke Shaw](https://scholar.google.com/citations?user=StrbFQ4AAAAJ) | Sheffield neuroscience student Allan Clarke Shaw; ACM recognizes operating systems, real-time systems, and software modeling. |
| John E Savage | [JE Savage](https://scholar.google.com/citations?user=ASYT5QEAAAAJ) | Vrije Universiteit Amsterdam genetic-association researcher JE Savage; ACM recognizes theoretical computer science, information theory, and VLSI. |
| John B Goodenough | [John B. Goodenough](https://scholar.google.com/citations?user=U8jmzF0AAAAJ) | Texas battery/solid-state chemist John B. Goodenough; ACM recognizes the software-engineering researcher. |
| Adele Goldberg | [Adele E Goldberg](https://scholar.google.com/citations?user=aK42DkQAAAAJ) | Princeton linguist/psychologist Adele E Goldberg; ACM recognizes Smalltalk and object-oriented programming. |
| Bob O Evans | [BOB EVANS OCHIENG](https://scholar.google.com/citations?user=BlOnsXMAAAAJ) | Supply-chain lecturer Bob Evans Ochieng, not the canonical Bob O Evans. Cached DBLP names Bob O. Evans; the ACM profile cell is blank. |
| Bruce Lindsay | [Bruce George Lindsay](https://scholar.google.com/citations?user=YT1C7RIAAAAJ) | Penn State statistician Bruce George Lindsay; ACM recognizes the System R database researcher. |
| Burton Smith | [Benjamin E Smith](https://scholar.google.com/citations?user=b6KgeNEAAAAJ) | Physiotherapist Benjamin E Smith; ACM recognizes scalable shared-memory multiprocessors. |
| C.L. Liu | [Chong Liu 刘崇](https://scholar.google.com/citations?user=T_DdQlAAAAAJ) | Mechanics researcher Chong Liu; ACM recognizes computer-science educator C.L. Liu. The local CSRankings join names Chun-Lei Liu and is not a safe replacement source. |
| Peter Elias | [Peter Elias](https://scholar.google.com/citations?user=8BJBG7YAAAAJ) | University of Lagos geographer; the canonical Fellow citation is for information theory, compression, and error correction. The ACM profile cell is blank. |

### 2026-09-15 - Outstanding Review Candidates

This subsection records unresolved identity suspicions and publication-list concerns from the cache-only review.
The later web-search resolution entries do not document decisions for these cases.

Roy Levin, Prithviraj Banerjee, and Robin Williams were flagged as suspected wrong-person links; the cached evidence was insufficient for a confident correction, so their links were retained.
Manish Gupta, John C. Mitchell, Guang Gao, Ahmed Sameh, and David S Johnson were flagged for likely mixed or misattributed publication lists; their citation metrics were retained pending further review.
Gautam Das, Mikhail Atallah, and Kai Li had lower-confidence publication outliers that might instead reflect valid collaborations.
The local CSRankings joins for Hui Zhang and C.L. Liu identify other people and must not be used to fill replacement Scholar URLs automatically.
The name matcher used in this review accepted 28 of the 29 removed links; matching names or successful fetch status alone does not establish identity.

## 2026-09-13 - Turing Award Reconciliation and Profile Crawl

At the time of reconciliation, `data/turing_award_winners.csv` enumerated 81 recipients across award years 1966–2025, all with verified ACM recipient URLs.
[PR #47](https://github.com/lintool/acm-bigcows/pull/47) reconciled the recipients and award years with ACM and [Wikipedia revision 1373210156](https://en.wikipedia.org/w/index.php?title=Turing_Award&oldid=1373210156), corrected citation text, and completed profile-link coverage.
Official-source and Wikipedia citation discrepancies are recorded in [issue #46](https://github.com/lintool/acm-bigcows/issues/46).

The fresh Safari crawl completed at `2026-09-13T23:48:11Z`: all 81 profiles were fetched successfully in 81 attempts, with 81 distinct HTML captures.
It used the shared crawler's Turing mode, including modern ACM award profiles and legacy `amturing.acm.org` recipient pages.
All identities and award years were checked against the captured HTML.

Retained local artifacts under `../bigcows-crawler/.cache/` are:

- `acm-turing-profile-cache-2026-09-13.json`: captured HTML and parsed fields.
- `acm-turing-profile-input-2026-09-13.csv`: original input snapshot.
- `acm-turing-profile-report-2026-09-13.json` and `acm-turing-profile-state-2026-09-13.json`: original completion records.
- `acm-turing-profile-manifest-2026-09-13.json`: input checksum, award, date, and artifact paths.
- `acm-turing-profile-log-2026-09-13.txt`: console log.

These artifacts are Git-ignored and are not shipped with either repository.
They share the cache directory and date with the Fellows crawl but use a separate prefix.
The crawl snapshot predates the Kahan punctuation correction in [PR #48](https://github.com/lintool/acm-bigcows/pull/48); use read-only comparison for the current CSV and the original snapshot when resuming the retained crawl.

The original completion report flagged seven profiles.
After the Kahan correction, comparison with the post-PR #48 CSV found six citation differences, ten exact name differences, and one location difference, with no name-compatibility or year mismatches.
Preserve the reviewed differences:

- Bennett and Brassard: retain the 2025 citation supported by ACM's [announcement](https://www.acm.org/media-center/2026/march/turing-award-2025).
  Their recipient pages use a different official version; see issue #46.
- Barto, Sutton, and Wigderson: retain terminal periods missing from ACM's text.
- Alan Kay: retain the citation without the surrounding quotation marks on ACM.
- Charles H. Bennett: retain `USA` rather than the page's `United States`.
- Keep existing name forms where differences are initials, middle names, or punctuation.

These counts describe the September 13 captures and the post-#48 CSV, not a live inventory.
A fresh capture is evidence for review, not an instruction to overwrite better canonical data.

## 2026-09-13 - ACM Fellows Profile Crawl Review

The Safari/AppleScript recrawl completed at `2026-09-13T19:53:05Z`, as documented in [PR #43](https://github.com/lintool/acm-bigcows/pull/43).
At crawl completion, all 1,627 supplied ACM profile URLs had cached HTML and status `ok`, with no remaining fetch failures or duplicate HTML captures.
The crawler itself did not edit the CSV.

Local artifacts are under `../bigcows-crawler/.cache/`, with the crawl start date as a suffix:

- `acm-fellow-profile-cache-2026-09-13.json`: fresh profile HTML and parsed fields.
- `acm-fellow-profile-input-2026-09-13.csv`: the CSV snapshot used for the crawl.
- `acm-fellow-profile-report-2026-09-13.json` and `acm-fellow-profile-state-2026-09-13.json`: results at crawl completion, before the later name corrections.
- `acm-fellow-profile-log-2026-09-13.txt`: the original console log.
- `acm-fellow-profile-manifest-2026-09-13.json`: registration of the retained crawl, including the original input checksum and artifact paths.

These files are Git-ignored and available only in the local checkout.
The five original artifacts were renamed without changing their contents, and a manifest was added using the original input snapshot.
Paths embedded in historical logs may refer to the former directory layout.
The April ACM profile cache, its report and directory scan, and obsolete browser experiments were removed.
The April Scholar captures used in the [cache-only Scholar review](#2026-09-15---google-scholar-profile-reconciliation) were retained separately.
Select `--crawl-date 2026-09-13` to use the retained crawl; there is no undated default.
Use `compare_acm_fellow_profiles.py` for comparisons with the current CSV so the original completion records are retained.
See [README_FOR_AGENTS.md](../README_FOR_AGENTS.md) for invocation and comparison guidance.

The subsequent consistency review reparsed all cached pages and corrected Sheila McIlraith, Giovanni De Micheli, and Satoshi Matsuoka in [PR #44](https://github.com/lintool/acm-bigcows/pull/44).
All years and locations matched.
After those corrections, 58 names still differed from the parser output because of valid variants or cleaner CSV names.
These were reviewed and retained; the report's permissive name check does not enumerate all textual differences.

Preserve these deliberate differences from ACM:

- Nikolaj Bjørner: ACM displays the reversed name `Bjorner Nikolaj`.
- Frank Wm Tompa: the captured page omits the citation; retain the CSV citation.
- Richard R. Burton: ACM's citation ends with `analysi`; retain `analysis`.
- Keep clean names instead of duplicated name parts, honorifics, or incorrect capitalization and spacing from ACM, including Giovanni De Micheli and Satoshi Matsuoka.

## 2026-09-13 - ACM Fellows Reconciliation

As reviewed on 2026-09-13, `data/acm_fellows.csv` was a best-effort enumeration of 1,638 Fellows across classes 1994–2025, with 1,627 nonempty ACM profile URLs and 11 blank ACM profile cells.

[PR #42](https://github.com/lintool/acm-bigcows/pull/42) reconciled the dataset with [Wikipedia revision 1374489782](https://en.wikipedia.org/w/index.php?title=List_of_fellows_of_the_Association_for_Computing_Machinery&oldid=1374489782).
After reviewing name variants and discrepancies, no confirmed missing Fellows or incorrect fellowship years remained.
Wikipedia errors and an unsupported entry are recorded in [issue #41](https://github.com/lintool/acm-bigcows/issues/41).

## 2026-09-13 - Unavailable Individual ACM Profiles

On 2026-09-13, the `acm_fellow_profile` cells for 11 HTTP 404 URLs were cleared in `data/acm_fellows.csv`, and those URLs were removed from the shared cache.
All 11 Fellow rows and their other fields were preserved.
The cleanup initially used cached responses from April 28–29, 2026; later browser checks also found those individual pages unavailable.
No verified replacements were found.

The affected people and their former profile URLs are recorded here for provenance:

| Name | Former ACM Profile URL | Recorded HTTP Status |
| --- | --- | --- |
| John D Gannon | [Former ACM Profile](https://awards.acm.org/award-recipients/gannon_1259480) | 404 |
| J D Couger | [Former ACM Profile](https://awards.acm.org/award-recipients/couger_1081272) | 404 |
| Raymond Reiter | [Former ACM Profile](https://awards.acm.org/award-recipients/reiter_1131614) | 404 |
| Larry Stockmeyer | [Former ACM Profile](https://awards.acm.org/award-recipients/stockmeyer_1438050) | 404 |
| Chris S Wallace | [Former ACM Profile](https://awards.acm.org/award-recipients/wallace_1058015) | 404 |
| Harold J Highland | [Former ACM Profile](https://awards.acm.org/award-recipients/highland_1042530) | 404 |
| Bob O Evans | [Former ACM Profile](https://awards.acm.org/award-recipients/evans_1002203) | 404 |
| David John Wheeler | [Former ACM Profile](https://awards.acm.org/award-recipients/wheeler_1002054) | 404 |
| J Presper Eckert | [Former ACM Profile](https://awards.acm.org/award-recipients/eckert_4037602) | 404 |
| Peter Elias | [Former ACM Profile](https://awards.acm.org/award-recipients/elias_1192715) | 404 |
| Roger M Needham | [Former ACM Profile](https://awards.acm.org/award-recipients/needham_1674183) | 404 |

No replacement ACM profile URLs had been confirmed at the end of this review.
Keep their `acm_fellow_profile` cells blank until a valid replacement is verified; retain the ACM Fellow rows.

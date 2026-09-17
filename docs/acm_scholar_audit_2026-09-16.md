# ACM Fellows Scholar Sweep — September 16, 2026

**Import update (2026-09-16 21:21 EDT):** All 1,250 accepted fresh profiles have now been imported and the visualization data refreshed.
The findings and row-level export statuses below describe the earlier audit snapshot; see [Data Notes](data_notes.md) for the completed import.

Completed 2026-09-16 20:58 EDT.

Audited all 1,638 ACM Fellow rows and all 1,255 Scholar links present at the start of this sweep.
Every starting link had a successful fresh capture from the September 16 crawl or its follow-up checks; a successful fetch alone did not establish the correct identity.
Found seven additional wrong-person or mixed-person associations, verified two replacements with new HTTP 200 captures, and cleared five links where no verified live replacement was found.
The resulting dataset has **1,250 distinct linked profiles with fresh captures and supported identities**, plus **388 blank Scholar fields**.
A blank field is a coverage gap, not proof that a public profile does not exist.
No historical record was used as a substitute for a rejected profile.
The visualization was not changed.

## Identity Corrections

| Fellow | Outcome | Evidence |
| --- | --- | --- |
| Carla Gomes | Cleared; no verified replacement | Cornell computational sustainability Fellow; linked profile is a University of Lisbon social-science namesake. [Source](https://www.cs.cornell.edu/gomes/bio.php) |
| Satish Rao | [Fresh replacement](https://scholar.google.com/citations?user=62Uqu6wAAAAJ) | Replaced UES materials-science namesake with Satish B Rao; graph partitioning, metric embeddings and multicommodity flow papers match Berkeley research and coauthors. [Source](https://people.eecs.berkeley.edu/~satishr/) |
| Manish Gupta | [Fresh replacement](https://scholar.google.com/citations?user=fHISoWoAAAAJ) | Replaced an unverified mixed-author profile with Google DeepMind profile; Blue Gene, Java escape analysis and compiler publications match the Fellow and official biography. [Source](https://research.google/people/106704/) |
| Roy Levin | Cleared; no verified replacement | Linked route-search researcher completed a Technion PhD in 2014; Fellow is the older CMU/DEC/Microsoft systems researcher. DBLP also points to the namesake. [Source](https://www.cs.technion.ac.il/news/view-new.php?nwid=688) |
| Prithviraj Banerjee | Cleared; no verified replacement | Linked Apple computer-vision researcher is a USC 2008–2014 graduate; Fellow worked on parallel computing and VLSI CAD at Illinois/Northwestern. DBLP also points to the namesake. [Source](https://users.eecs.northwestern.edu/~dcz338/publications/TLVLSI-accelchip.pdf) |
| Robin Williams | Cleared; no verified replacement | Linked Edinburgh social-science researcher is distinct from the IBM research leader and ACM Fellow described by UC Merced. [Source](https://engineering.ucmerced.edu/content/robin-williams) |
| Ahmed Sameh | Cleared; no verified replacement | Profile is verified at Prince Sultan University and combines that namesake with Purdue numerical analyst Ahmed H. Sameh and unrelated authors. A coauthor link and research.com repeat this wrong association. [Source](https://www.cs.purdue.edu/people/faculty/sameh/) |

Satish Rao’s replacement was discovered in the fresh coauthor lists of Monika Henzinger, Ingemar J. Cox and Philip Klein and checked against Berkeley’s research/publication list.
Manish Gupta’s replacement was discovered in Hubertus Franke’s fresh coauthor list and checked against Google’s biography and Blue Gene/compiler publications.
Both replacement captures used the agreed 5–7 second request pacing and stopped-on-block policy.
Roy Levin’s [CMU doctoral record](https://csd.cmu.edu/academics/doctoral/degrees-conferred/roy-levin) distinguishes the Fellow from the Technion route-search researcher.
The Apple namesake’s [self-published education and publication record](https://www.linkedin.com/in/prithvirajb) further distinguishes Prithviraj Banerjee.

## Publication Attribution Issues

Correct identity does not mean that Scholar’s publication list or aggregate citation totals are clean.
These 11 profiles retain the correct identity, but their captured publication lists contain confirmed or suspected attribution problems.
Four conflicts were checked against publication records; seven remain review candidates.
No citation totals were manually adjusted, and no papers were removed from Scholar.

| Fellow | Finding | Evidence |
| --- | --- | --- |
| Arindam Banerjee | Confirmed conflict: DALYs / healthy-life-expectancy paper names Amitava Banerjee, not Arindam Banerjee. | [Captured profile](https://scholar.google.com/citations?user=RY7cuPAAAAAJ); [Publication](https://stacks.cdc.gov/view/cdc/202311/cdc_202311_DS1.pdf) |
| Gautam Das | Confirmed conflict: Top-ranked next-generation sequencing paper identifies Gautam Das at miBiome Therapeutics, Mumbai; the Fellow is the UT Arlington database researcher. | [Captured profile](https://scholar.google.com/citations?user=oleB9xIAAAAJ); [Publication](https://pmc.ncbi.nlm.nih.gov/articles/PMC10376292/); [miBiome identity](https://www.mibiome.com/about/) |
| Scott J Aaronson | Confirmed conflict: Psilocybin depression paper names Scott T. Aaronson, not the quantum-computing Fellow. | [Captured profile](https://scholar.google.com/citations?user=EYv2BNQAAAAJ); [Publication](https://doi.org/10.1056/NEJMOA2206443) |
| David Patterson | Confirmed conflict: Clio and the Economics of QWERTY is by Paul A. David. | [Captured profile](https://scholar.google.com/citations?user=Wj4ZBFIAAAAJ); [Publication](https://joeornstein.github.io/pols-4641/readings/David%20-%201985%20-%20Clio%20and%20the%20Economics%20of%20QWERTY.pdf) |
| Martin Wong | Needs publication review: Automated process planning book is credited to T. C. Chang and R. A. Wysk in this profile. | [Captured profile](https://scholar.google.com/citations?user=WPhoQiUAAAAJ) |
| John C. Mitchell | Needs publication review: TRNSYS solar-energy software leads this computer-security profile; displayed author is J. W. Mitchell. | [Captured profile](https://scholar.google.com/citations?user=1_kJPIEAAAAJ) |
| Krithivasan Ramamritham | Needs publication review: Dragon2000 standard-cell placement paper is credited to X. Yang and M. Sarrafzadeh. | [Captured profile](https://scholar.google.com/citations?user=LFLG5pcAAAAJ) |
| Kai Li | Needs publication review: Image super-resolution / residual channel attention paper may be a computer-vision namesake; distinguish from Princeton systems work. | [Captured profile](https://scholar.google.com/citations?user=9MSpWOUAAAAJ) |
| David S Johnson | Needs publication review: Genome sequencing, psychology reproducibility and IPv6 papers appear alongside the Fellow’s algorithms work. | [Captured profile](https://scholar.google.com/citations?user=LyEq7qEAAAAJ) |
| Ramesh C Jain | Needs publication review: Diabetes burden and membrane-transporter papers appear alongside multimedia work; attribution needs checking. | [Captured profile](https://scholar.google.com/citations?user=wOYUPpwAAAAJ) |
| James H Morris | Needs publication review: Known prostate-cancer xenograft paper among authentic KMP/Andrew publications; user-approved identity remains unchanged. | [Captured profile](https://scholar.google.com/citations?user=9Y2cn3EAAAAJ) |

## Coverage and Export Issues

- **388 Fellows have blank Scholar fields:** 383 were already blank and five were cleared in this sweep.
- **Canonical metrics import remains pending:** 827 currently linked profiles still have historical metrics, 419 have no canonical metrics row, and 4 have fresh canonical rows.
- The complete fresh-only, identity-reviewed export contains 1,250 profiles at `tmp/scholar-full-sweep-2026-09-16/fresh-accepted-google_scholar_profiles.csv`.
- The canonical metrics CSV now has 870 rows: removed the five existing rows tied to newly rejected associations and added the two verified replacements; unaffected rows retain their original dates.
- **39 existing metrics records are not linked by the current ACM roster** and were not attempted in the fresh ACM crawl; their freshness and scope still require reconciliation before the full import.
- **24 DBLP identity-review candidates** are recorded in the row audit; these include cached-name conflicts and six particularly clear namesake associations encountered during this Scholar review.
- DBLP matches cannot establish identity by themselves: Roy Levin and Prithviraj Banerjee had matching Scholar/DBLP papers for the wrong people.
- Rudrapatna K. Shyamasundar’s profile shows only three publications, so it is a poor basis for career citation coverage even though its TIFR email, IIT Bombay affiliation and research interests support the identity.
- Missing email verification and sparse affiliation metadata are recorded per row, not treated as automatic evidence of a wrong person.

## Method and Limits

Checked the entire roster for capture availability, HTTP status, timestamps, nonempty HTML, parsed metrics, duplicate URLs and duplicate capture bodies.
The initial identity screen found 842 name-compatible profiles with at least two exact normalized publication-title matches to cached DBLP records, 26 recently resolved profiles, and 387 profiles requiring detailed review.
Reviewed affiliation/research metadata across the 842 corroborated profiles and examined names, affiliations, research topics and leading publications for all 387 exceptions against ACM award citations and supporting records.
Reused the 26 identity resolutions completed earlier in this same review session.
Seven new corrections override those initial classifications, including three initially publication-corroborated profiles.
Follow-up web research used university, employer and publication sources; discovery aggregators and coauthor links were not treated as independent proof of identity.
The audit uses the first captured Scholar page, normally 20 publications, and does not claim a complete paper-by-paper authorship audit.
Profiles are supported by the available evidence, not guaranteed error-free.
The 383 initially blank fields were inventoried with the existing September 15/16 search outcomes; this sweep did not repeat a new web search for each blank record.
Cached DBLP records are older corroborating evidence, not fresh DBLP crawls.
Original raw captures remain as audit evidence; they are not active historical fallbacks.

## Files and Validation

The [full row audit](acm_scholar_audit_2026-09-16.csv) contains one record per Fellow, including status, freshness, identity basis, source capture hash, export status and issues.
Detailed initial evidence, final rows, new full-HTML captures, correction decisions and the fresh-only export are under `tmp/scholar-full-sweep-2026-09-16/`.
Validated 1,638 rows, exactly seven changed Scholar cells, unchanged other Fellow fields and ordering, LF line endings, 1,250 unique accepted URLs and complete successful fresh captures.
Preserved the user’s Peter Müller, James H. Morris and Laurie Hendren decisions.
Verified all other canonical CSVs and `docs/scholar_citations.html` byte-for-byte unchanged from the start of the sweep.
No staging, commit, push or visualization regeneration was performed.

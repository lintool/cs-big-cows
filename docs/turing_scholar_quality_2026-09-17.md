# Turing Award Scholar Profile Quality — September 17, 2026

Completed 2026-09-17 21:32 EDT.

This report and its row audit assess Scholar profiles using the evidence available at that time.
Recipient names retain their review-time forms from before the directory reconciliation; use the canonical roster for current names.
DBLP is assessed separately in the later [DBLP review](dblp_profile_quality_2026-09-17.md); its removals do not change these Scholar judgments.
The [maintenance policy](../README_FOR_AGENTS.md#publication-profile-quality) defines the shared criteria; the sections below preserve this assessment's scope and decisions.

**81 recipients assessed: 40 Y; 41 N.**
Every N is a missing stored Scholar link, following the user's explicit policy.
No linked profile showed substantial contamination comparable to the four user-rejected Fellows profiles in the reviewed sample.
All 30 Scholar URLs shared with ACM Fellows retain the same Y rating; none of the four user-rejected Fellows is in this Turing roster.

## Policy and Evidence

The ACM Turing recipient profile is the identity and research reference.
Y permits isolated questionable or misattributed papers when the overall sample is reasonable and adjacent to the recipient's work.
N is reserved for substantial contamination or a wrong-person association, as well as missing links by user instruction.
Substantial mixing can warrant N despite a numerical majority of relevant papers; explicit user decisions take precedence.

Individually reviewed all 800 captured publication entries: 20 per linked profile, including the 10 profiles not shared with the Fellows roster.
The exact successful Scholar captures are from September 17 UTC, corresponding to the September 16 Toronto crawl; retained ACM captures are dated September 13 UTC.
Current URLs and capture hashes match the earlier identity audit; all 30 shared captures also match the Fellows quality evidence.
This is a first-page sample assessment, not a new crawl or a guarantee about the full bibliography or aggregate citation totals.
No new missing-profile search was performed in this quality review; the [prior search outcomes](turing_scholar_search_2026-09-16.csv) remain available.
Only the quality field was added to the Turing roster; URLs, original fields, metrics, Fellows ratings and visualization data were preserved.

The [row audit](turing_scholar_quality_2026-09-17.csv) records all 81 recipients, individual rationales, sources, sample sizes, capture timestamps and hashes.
Its `review_requested` flag is separate from the quality rating: two `Y` profiles have optional review questions, while all 41 missing-link `N` rows have no active quality-review request.
`reviewed_at` records assessment time; `scholar_fetched_at` and `acm_fetched_at` record evidence capture times.

## Optional Attribution Review — Both Remain Y

These two narrow authorship questions remain open, but neither makes the overall profile poor under the requested standard.

| Recipient | Rating | References | Question |
| --- | --- | --- | --- |
| Frederick Brooks | Y | [ACM](https://awards.acm.org/award-recipients/brooks_1002187) · [Scholar](https://scholar.google.com/citations?user=_h65cfgAAAAJ) | The architecture textbook lists Patterson, Hennessy and Goldberg; a contributor or merged-record explanation remains unresolved, but the surrounding sample is coherent. |
| Raj Reddy | Y | [ACM](https://awards.acm.org/award-recipients/reddy_9634208) · [Scholar](https://scholar.google.com/citations?user=mYu2uuIAAAAJ) | HARPY is credited to B. Lowerre; check the thesis/project or merged-record attribution if exact publication ownership matters. |

## Isolated Concerns Retained — All Remain Y

These findings are recorded for transparency and do not require a lower profile-quality rating.

| Recipient | References | Finding | Source |
| --- | --- | --- | --- |
| David Patterson | [ACM](https://awards.acm.org/award-recipients/patterson_2316693) · [Scholar](https://scholar.google.com/citations?user=Wj4ZBFIAAAAJ) | Clio and the Economics of QWERTY is credited to Paul A. David; the rest of the sample is dominated by the recipient's architecture and systems work. | [Publication](https://joeornstein.github.io/pols-4641/readings/David%20-%201985%20-%20Clio%20and%20the%20Economics%20of%20QWERTY.pdf) |
| Kenneth Lane Thompson | [ACM](https://awards.acm.org/award-recipients/thompson_4588371) · [Scholar](https://scholar.google.com/citations?user=FsHMg9AAAAAJ) | The Durkheim book is by the Open University sociologist Kenneth Thompson, distinct from the UNIX recipient; one outlier does not warrant N. | [Publication](https://www.routledge.com/Emile-Durkheim/Thompson/p/book/9780415285315) |
| Stephen A Cook | [ACM](https://awards.acm.org/award-recipients/cook_N991950) · [Scholar](https://scholar.google.com/citations?user=VGxPtzIAAAAJ) | The phage-lysozyme paper lists S. P. Cook, not complexity theorist Stephen A. Cook; the other 19 entries are coherent. | [Publication](https://pdbj.org/mine/summary/1L03) |
| Dana S Scott | [ACM](https://awards.acm.org/award-recipients/scott_1193622) · [Scholar](https://scholar.google.com/citations?user=oaja5KYAAAAJ) | The rheumatoid-arthritis study credits a D. Scott in a UK clinical research context; this appears to be a namesake entry among 19 logic and semantics papers. | [Publication](https://pubmed.ncbi.nlm.nih.gov/12096230/) |

## Contributor and Coverage Context

Robert Metcalfe's sample is dominated by Ethernet, packet networking and related computing work.
Some short-credit flags concern essays in a volume associated with him: [Springer lists Metcalfe for Beyond Calculation and lists its component chapters](https://link.springer.com/book/10.1007/978-1-4612-0685-9), and [Denning identifies Metcalfe as a co-editor of the volume containing How We Will Learn](https://denninginstitute.com/pjd/PUBS/internet30.pdf).
Those contributor relationships are compatible with Y and should not be confused with substantial namesake contamination.
Edwin Catmull's first page is dominated by editions or translations of his creativity book; its coverage is narrow but its identity and content remain reasonable.
Jim Gray's astronomy data publications and other recipients' interdisciplinary computational work are not rejected merely for having a different subject label.

## Retained Evidence

Input snapshots, all 800 titles and credits, selected ACM and Scholar captures, source checks, individual decisions and validation are retained under `../bigcows-crawler/.cache/turing-scholar-quality-2026-09-17-213022/`, relative to the repository root.
The two extra direct source opens recorded in `web-verification-3.json` failed; the report relies on the successful primary-source search results and retained profile evidence, not those failed opens.

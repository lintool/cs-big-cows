# Broader CSRankings Alignment Review

Completed September 18, 2026, using the refreshed 26 alphabetical CSRankings faculty files and retained Scholar/DBLP identity evidence, with selected institutional web checks.
The [first-stage row audit](csrankings_broader_alignment_2026-09-18.csv) records all 1,057 award rows that were unlinked at the start, including candidates, decisions, institutional context, ACM citations and evidence URLs.
The subsequent [local profile-table audit](csrankings_profile_evidence_2026-09-18.csv) checks both rosters against the retained CSRankings table's Scholar IDs and DBLP URLs, adding five historical links.
The canonical award CSVs contain the accepted links and their UTC alignment dates; this report is a historical snapshot.

| Roster | New Links | Total Linked | Still Blank |
| --- | ---: | ---: | ---: |
| ACM Fellows | 183 | 829 | 809 |
| Turing Award winners | 1 | 17 | 64 |

## Evidence and Matching

Candidate generation used alternate names from currently accepted, `Y`-rated Scholar/DBLP profiles, the upstream DBLP alias file, relaxed middle-name matching, common nicknames and similar first-name spellings with matching surnames.
These rules produced candidates for 220 rows; 837 rows had no candidate under this sweep.
Candidate generation was deliberately broader than acceptance and did not establish identity on its own.

Accepted 143 rows after inspecting a shared nonempty Scholar ID together with compatible names and institutional context.
For multiple source spellings, the exact retained DBLP or Scholar spelling was preferred, preserving source disambiguation numbers and campus tags.
Ellen Zegura uses `Ellen W. Zegura`; both candidate spellings share the same Scholar ID, institution and homepage.
Accepted another 31 rows using the exact reviewed DBLP name and corroborating current or historical institution, and five using institutional/research evidence described below.
No link was accepted from a fuzzy name, institution or research area alone.

Retained all existing links and dates, and dated new links `2026-09-18`.
The other award fields, publication-profile URLs and quality ratings were not changed.
This review reused prior profile evidence; it did not recrawl or revalidate every publication profile.

## Selected Institutional Checks

| Award Name | CSRankings Name | Corroboration |
| --- | --- | --- |
| Wang, Wei | Wei Wang 0010 | [UCLA faculty page](https://samueli.ucla.edu/people/wei-wang/) identifies the 2020 ACM Fellow, data-mining research and the UCLA homepage recorded by CSRankings. |
| Littman, Michael | Michael L. Littman | [Brown faculty page](https://cs.brown.edu/people/faculty/mlittman/) supplies the middle initial and reinforcement-learning/AI research, consistent with the award citation on sequential decision-making. |
| Warnow, Tandy | Tandy J. Warnow | [The source homepage](https://tandy.cs.illinois.edu/) identifies the Illinois professor, 2015 ACM Fellowship, phylogenetics and historical linguistics. |
| Morris, Robert | Robert Tappan Morris | [MIT's Fellowship announcement](https://news.mit.edu/2015/five-csail-researchers-named-acm-fellows-0108) corroborates the MIT faculty identity and networking/distributed-systems research. |
| Agrawal, Dharma P | Dharma Agrawal | [Cincinnati's laboratory history](https://eecs.ceas.uc.edu/~cdmc/aboutUs.html) identifies Dharma P. Agrawal and his distributed/wireless-computing work; retained DBLP evidence supplies the same institution and full name. |
| Sutton, Richard | Richard S. Sutton | Retained DBLP and Scholar evidence agrees on the name and Alberta affiliation; the [Alberta directory](https://apps.ualberta.ca/directory/person/rsutton) corroborates reinforcement-learning research. |

Institution changes were considered explicitly.
For example, [Zygmunt Haas's UT Dallas page](https://personal.utdallas.edu/~haas/) records his Cornell history, and [HKBU's Martin Wong appointment](https://www.hkbu.edu.hk/en/whats-new/press-release/2023/0117-hkbu-appoints-professor-martin-wong-ding-fat-as-provost.html) records his earlier UIUC role and electronic-design-automation research.
[Kilian Weinberger's Cornell page](https://www.cs.cornell.edu/~kilian/) reconciles the older Washington University affiliation in the retained DBLP evidence.

## Conflicts and Unresolved Candidates

Two identifier-based candidates were rejected after checking the surrounding identity evidence:

- `Chris S Wallace`: CSRankings associates the roster's Scholar ID with `Christopher Stewart` at Ohio State.
  The stored Scholar identity and [Monash publication record](https://users.monash.edu.au/~dld/CSWallacePublications/) describe Christopher Stewart Wallace of Monash (1933–2004), a different person.
- `Zhang, HongJiang`: CSRankings associates the roster's Scholar ID with `Hong Jiang 0001` at UT Arlington.
  The stored Scholar/DBLP identity and ACM multimedia citation describe HongJiang Zhang, so the mismatching name and institution prevent acceptance.

Wei Wang also has conflicting retained evidence: the current stored DBLP link's review describes `Wei Wang 0011` at HKUST, while the award and UCLA evidence support `Wei Wang 0010` at UCLA.
The CSRankings link uses the corroborated UCLA identity; the original DBLP URL and quality field remain unchanged pending a separate profile review.
These cases demonstrate why shared identifiers and previous quality ratings were not treated as conclusive evidence by themselves.

The remaining 39 rows with candidates were left unresolved because the available evidence did not support an association.
Together with the two rejected identifier matches and 837 rows without candidates, 878 award rows remained blank at the end of the first stage.
The historical-profile follow-up below reduced that to 873; these blanks are not proof of absence from CSRankings.

## Local Profile Table Follow-Up

At the user's request, checked `data/csrankings_profiles.csv` as an additional source of Scholar-ID and DBLP-URL evidence.
Across both rosters, 656 rows had at least one identifier association: 647 agreed with the existing name link, two supported an existing spelling variant, five supported new historical links, and two had misleading old associations.
The spelling variants were Tamal Krishna Dey versus Tamal K. Dey, and Nikil Dutt versus Nikil D. Dutt; their source Scholar IDs and institutions agree, so the current keys were preserved.

The five historical links are listed below.
All have an exact normalized DBLP URL agreement with the retained local table and corroborating institutional identity; the first four also share the same Scholar ID.
Donald Greenberg's retained row has `NOSCHOLARPAGE`, which was not treated as an identifier.
These five records are absent from both the refreshed alphabetical source files and the refreshed combined CSV when checked by name, homepage and usable Scholar ID.
Their links deliberately refer to retained historical records, not a claim of current upstream inclusion.
The local table's `crawl_date` is the old alignment build date, not a fresh capture date; the new roster alignment date is September 18, 2026.

| Award Name | Retained CSRankings Key | Institutional Evidence |
| --- | --- | --- |
| Olson, Judith S | Judith S. Olson | [UC Irvine profile](https://ics.uci.edu/?people=judy-olson), human-computer interaction and remote collaboration. |
| Gottlob, Georg | Georg Gottlob | [Oxford profile](https://www.cs.ox.ac.uk/people/georg.gottlob/), database theory and artificial intelligence. |
| Cardelli, Luca | Luca Cardelli | [Oxford profile](https://www.cs.ox.ac.uk/people/luca.cardelli/), programming languages and verification. |
| Lee, Ruby B | Ruby B. Lee | [Princeton profile](https://www.princeton.edu/~rblee/), processor and multimedia architecture. |
| Greenberg, Donald | Donald Greenberg | [Cornell profile](https://www.cs.cornell.edu/people/donald-greenberg), computer graphics. |

Rejected the legacy table's mapping of MIT networking researcher David D. Clark to `David Clark 0001` at University College London, and its mapping of C. L. Liu to `Chun-Lei Liu` at Berkeley.
The old builder generated these DBLP associations from names; they cannot independently validate the same name match.
No stored DBLP or Scholar URL was changed, and no additional Turing link resulted from this follow-up.

## Validation and Retained Evidence

Checked all original fields and row positions, preservation of existing links and dates, exact source-key membership, one-to-one assignments within each roster and agreement for all 63 shared recipients.
Retained input snapshots, hashes, candidate-generation and decision scripts, complete candidate details, authoring outputs and validation results under `../bigcows-crawler/.cache/csrankings-broader-alignment-2026-09-18/`, relative to the repository root.
The local profile-table follow-up additionally retains its input rosters, the source profile table, identifier associations and validation under `../bigcows-crawler/.cache/csrankings-profile-evidence-2026-09-18/`.
The CSRankings and Scholar profile tables and both visualization datasets are unchanged.
Downstream migration to the explicit name keys and visualization regeneration remain deferred.

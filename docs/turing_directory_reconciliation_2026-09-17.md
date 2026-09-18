# Turing Award Directory Reconciliation

Completed 2026-09-17 23:34 EDT.

**The ACM awards directory is the source of truth unless concrete evidence establishes that it is obviously wrong.**
This review follows the [repository policy](../AGENTS.md#acm-source-of-truth) and the user’s request to copy surname-first names literally.

## Result

Checked all 60 annual directory pages in descending order from 2025 through the first award year, 1966.
The directory contains 81 recipients, all matched one-to-one to the 81 CSV rows using the ACM recipient ID, including case-insensitive alphanumeric IDs and legacy `.cfm` URLs.
There are no missing or extra recipients and no award-year differences.
All 81 names now use the directory’s literal surname-first display text, decoding HTML entities and normalizing rendered whitespace.
9 names differ beyond the reversal of given-name-first order; those differences are recorded below.
No obvious directory name error was identified that warranted an evidence-backed spelling exception.
The individual profile heading is not substituted for the directory name.
Re-sorted the CSV by numeric year descending and full stored name using `str.lower()`.

## Annual Coverage

| Award Year | Directory Recipients | CSV Recipients |
| --- | ---: | ---: |
| [2025](https://awards.acm.org/fellows/award-recipients?year=2025&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [2024](https://awards.acm.org/fellows/award-recipients?year=2024&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [2023](https://awards.acm.org/fellows/award-recipients?year=2023&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2022](https://awards.acm.org/fellows/award-recipients?year=2022&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2021](https://awards.acm.org/fellows/award-recipients?year=2021&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2020](https://awards.acm.org/fellows/award-recipients?year=2020&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [2019](https://awards.acm.org/fellows/award-recipients?year=2019&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [2018](https://awards.acm.org/fellows/award-recipients?year=2018&award=140&region=&submit=Submit&isSpecialCategory=) | 3 | 3 |
| [2017](https://awards.acm.org/fellows/award-recipients?year=2017&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [2016](https://awards.acm.org/fellows/award-recipients?year=2016&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2015](https://awards.acm.org/fellows/award-recipients?year=2015&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [2014](https://awards.acm.org/fellows/award-recipients?year=2014&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2013](https://awards.acm.org/fellows/award-recipients?year=2013&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2012](https://awards.acm.org/fellows/award-recipients?year=2012&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [2011](https://awards.acm.org/fellows/award-recipients?year=2011&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2010](https://awards.acm.org/fellows/award-recipients?year=2010&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2009](https://awards.acm.org/fellows/award-recipients?year=2009&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2008](https://awards.acm.org/fellows/award-recipients?year=2008&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2007](https://awards.acm.org/fellows/award-recipients?year=2007&award=140&region=&submit=Submit&isSpecialCategory=) | 3 | 3 |
| [2006](https://awards.acm.org/fellows/award-recipients?year=2006&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2005](https://awards.acm.org/fellows/award-recipients?year=2005&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2004](https://awards.acm.org/fellows/award-recipients?year=2004&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [2003](https://awards.acm.org/fellows/award-recipients?year=2003&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [2002](https://awards.acm.org/fellows/award-recipients?year=2002&award=140&region=&submit=Submit&isSpecialCategory=) | 3 | 3 |
| [2001](https://awards.acm.org/fellows/award-recipients?year=2001&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [2000](https://awards.acm.org/fellows/award-recipients?year=2000&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1999](https://awards.acm.org/fellows/award-recipients?year=1999&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1998](https://awards.acm.org/fellows/award-recipients?year=1998&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1997](https://awards.acm.org/fellows/award-recipients?year=1997&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1996](https://awards.acm.org/fellows/award-recipients?year=1996&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1995](https://awards.acm.org/fellows/award-recipients?year=1995&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1994](https://awards.acm.org/fellows/award-recipients?year=1994&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [1993](https://awards.acm.org/fellows/award-recipients?year=1993&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [1992](https://awards.acm.org/fellows/award-recipients?year=1992&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1991](https://awards.acm.org/fellows/award-recipients?year=1991&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1990](https://awards.acm.org/fellows/award-recipients?year=1990&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1989](https://awards.acm.org/fellows/award-recipients?year=1989&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1988](https://awards.acm.org/fellows/award-recipients?year=1988&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1987](https://awards.acm.org/fellows/award-recipients?year=1987&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1986](https://awards.acm.org/fellows/award-recipients?year=1986&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [1985](https://awards.acm.org/fellows/award-recipients?year=1985&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1984](https://awards.acm.org/fellows/award-recipients?year=1984&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1983](https://awards.acm.org/fellows/award-recipients?year=1983&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [1982](https://awards.acm.org/fellows/award-recipients?year=1982&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1981](https://awards.acm.org/fellows/award-recipients?year=1981&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1980](https://awards.acm.org/fellows/award-recipients?year=1980&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1979](https://awards.acm.org/fellows/award-recipients?year=1979&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1978](https://awards.acm.org/fellows/award-recipients?year=1978&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1977](https://awards.acm.org/fellows/award-recipients?year=1977&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1976](https://awards.acm.org/fellows/award-recipients?year=1976&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [1975](https://awards.acm.org/fellows/award-recipients?year=1975&award=140&region=&submit=Submit&isSpecialCategory=) | 2 | 2 |
| [1974](https://awards.acm.org/fellows/award-recipients?year=1974&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1973](https://awards.acm.org/fellows/award-recipients?year=1973&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1972](https://awards.acm.org/fellows/award-recipients?year=1972&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1971](https://awards.acm.org/fellows/award-recipients?year=1971&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1970](https://awards.acm.org/fellows/award-recipients?year=1970&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1969](https://awards.acm.org/fellows/award-recipients?year=1969&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1968](https://awards.acm.org/fellows/award-recipients?year=1968&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1967](https://awards.acm.org/fellows/award-recipients?year=1967&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| [1966](https://awards.acm.org/fellows/award-recipients?year=1966&award=140&region=&submit=Submit&isSpecialCategory=) | 1 | 1 |
| **Total** | **81** | **81** |

## Name Differences Beyond Order

| Year | Previous CSV Name | Directory Name |
| --- | --- | --- |
| 2025 | Charles H. Bennett | Bennett, Charles Henry |
| 2013 | Leslie Lamport | Lamport, Leslie Barry |
| 2009 | Charles P. Thacker | Thacker, Charles P |
| 1990 | Fernando Corbato | Corbato, Fernando J |
| 1984 | Niklaus E. Wirth | Wirth, Niklaus E |
| 1981 | Edgar F. Codd | Codd, Edgar F |
| 1975 | Herbert A. Simon | Simon, Herbert A |
| 1972 | Edsger W. Dijkstra | Dijkstra, Edsger W |
| 1968 | Richard W. Hamming | Hamming, Richard W |

## Recipient URL Review

The directory lists three modern recipient URLs where the CSV previously used ACM’s legacy Turing site.
The candidate pages were captured separately after the annual directory crawl; profile dates advance only for accepted successful captures.

| Recipient | Directory URL | Decision |
| --- | --- | --- |
| Bennett, Charles Henry | [Directory Target](https://awards.acm.org/award-recipients/bennett_1202470) | Accepted: page identifies Charles Henry Bennett and the 2025 Turing Award; replaced the legacy URL and set the accepted profile crawl date to 2026-09-18. |
| Brassard, Gilles | [Directory Target](https://awards.acm.org/award-recipients/brassard_UJ34503) | Accepted: page identifies Gilles Brassard and the 2025 Turing Award; replaced the legacy URL and set the accepted profile crawl date to 2026-09-18. |
| Nygaard, Kristen | [Directory Target](https://awards.acm.org/award-recipients/nygaard_5916220) | Accepted: page identifies Kristen Nygaard and the 2001 Turing Award; replaced the legacy URL and set the accepted profile crawl date to 2026-09-18. |

## Preserved Data and Validation

Preserved every location, award citation, DBLP and Scholar URL, publication-profile quality rating and publication-profile crawl date.
The earlier [Turing profile reconciliation](data_notes.md#2026-09-13---turing-award-reconciliation-and-profile-crawl) remains the provenance for deliberate citation and location differences; this review supersedes its name policy.
The Fellows CSV, Scholar metrics, CSRankings data and both generated visualization datasets are byte-for-byte unchanged from the start of this Turing review.
Validated all recipient IDs, annual counts, award years, reviewed names, URL decisions, preserved cells, uniqueness, CSV ordering and LF line endings.
The canonical Scholar join was checked in memory: names and accepted ACM URLs are the only changes in its recipient output; its metrics and coverage remain unchanged.
Visualization regeneration and snapshot-synchronization checks are deferred at the user’s request.

## Retained Evidence

Run directory: `../bigcows-crawler/.cache/turing-directory-reconciliation-2026-09-17/` (relative to the repository root).

- `turing-before.csv` and `protected-hashes.json`: input snapshot and protected-file hashes.
- `1966.html`–`2025.html` and accompanying JSON: all 60 annual pages, source URLs, UTC capture timestamps and HTML SHA-256 hashes.
- `manifest.json`, `directory.json` and `comparison.json`: crawl scope, extracted directory records and complete row mapping.
- `profile-*.json` and `review-decisions.json`: changed-link captures, decisions and reasons.
- `changes.json`, `validation.json` and `final-validation.json`: changed cells, input/output hashes and validation results.
- `reconcile.py`, `compare.py`, `check_links.py`, `apply_reviewed.py`, `validate.py` and `document.py`: reproducible extraction, review, import and validation steps.

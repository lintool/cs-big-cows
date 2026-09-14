# Data Notes

## ACM Fellows reconciliation

As reviewed on 2026-09-13, `data/acm_fellows.csv` is a best-effort enumeration of
1,638 Fellows across classes 1994–2025, with 1,627 nonempty ACM profile URLs and
11 blank profile cells.

[PR #42](https://github.com/lintool/cs-big-cows/pull/42) reconciled the dataset with
[Wikipedia revision 1374489782](https://en.wikipedia.org/w/index.php?title=List_of_fellows_of_the_Association_for_Computing_Machinery&oldid=1374489782).
After reviewing name variants and discrepancies, no confirmed missing Fellows or
incorrect fellowship years remained. Wikipedia errors and an unsupported entry
are recorded in [issue #41](https://github.com/lintool/cs-big-cows/issues/41).

## Latest reviewed ACM Fellows profile crawl

The Safari/AppleScript recrawl completed at `2026-09-13T19:53:05Z`, as documented
in [PR #43](https://github.com/lintool/cs-big-cows/pull/43). All 1,627 supplied URLs
have cached HTML and status `ok`, with no remaining fetch failures or duplicate
HTML captures. The crawler itself did not edit the CSV.

Local artifacts are under `../bigcows-crawler/.cache/`, with the crawl start date
as a suffix:

- `acm-fellow-profile-cache-2026-09-13.json`: fresh profile HTML and parsed fields.
- `acm-fellow-profile-input-2026-09-13.csv`: the CSV snapshot used for the crawl.
- `acm-fellow-profile-report-2026-09-13.json` and `acm-fellow-profile-state-2026-09-13.json`: results at crawl completion, before the later name corrections.
- `acm-fellow-profile-log-2026-09-13.txt`: the original console log.
- `acm-fellow-profile-manifest-2026-09-13.json`: registration of the retained crawl, including the original input checksum and artifact paths.

These files are Git-ignored and available only in the local checkout. The five
original artifacts were renamed without changing their contents, and a manifest
was added using the original input snapshot. Paths embedded in historical logs may
refer to the former directory layout. The April profile cache, its report and
directory scan, and obsolete browser experiments have been removed. Select
`--crawl-date 2026-09-13` to use the retained crawl; there is no undated default.
Use `compare_acm_fellow_profiles.py` for comparisons with the current CSV so the
original completion records are retained. See [README_FOR_AGENTS.md](README_FOR_AGENTS.md)
for invocation and comparison guidance.

The subsequent consistency review reparsed all cached pages and corrected
Sheila McIlraith, Giovanni De Micheli, and Satoshi Matsuoka in
[PR #44](https://github.com/lintool/cs-big-cows/pull/44). All years and locations
matched. After those corrections, 58 names still differed from the parser output
because of valid variants or cleaner CSV names. These were reviewed and retained;
the report's permissive name check does not enumerate all textual differences.

Preserve these deliberate differences from ACM:

- Nikolaj Bjørner: ACM displays the reversed name `Bjorner Nikolaj`.
- Frank Wm Tompa: the captured page omits the citation; retain the CSV citation.
- Richard R. Burton: ACM's citation ends with `analysi`; retain `analysis`.
- Keep clean names instead of duplicated name parts, honorifics, or incorrect
  capitalization and spacing from ACM, including Giovanni De Micheli and Satoshi Matsuoka.

## Unavailable individual ACM profiles

On 2026-09-13, the `acm_fellow_profile` cells for 11 HTTP 404 URLs were cleared
in `data/acm_fellows.csv`, and those URLs were removed from the shared cache.
All 11 Fellow rows and their other fields were preserved. The cleanup initially
used cached responses from April 28–29, 2026; later browser checks also found
those individual pages unavailable. No verified replacements were found.

The affected people and their former profile URLs are recorded here for provenance:

| Name | ACM Fellow profile URL | Status |
| --- | --- | --- |
| John D Gannon | https://awards.acm.org/award-recipients/gannon_1259480 | 404 |
| J D Couger | https://awards.acm.org/award-recipients/couger_1081272 | 404 |
| Raymond Reiter | https://awards.acm.org/award-recipients/reiter_1131614 | 404 |
| Larry Stockmeyer | https://awards.acm.org/award-recipients/stockmeyer_1438050 | 404 |
| Chris S Wallace | https://awards.acm.org/award-recipients/wallace_1058015 | 404 |
| Harold J Highland | https://awards.acm.org/award-recipients/highland_1042530 | 404 |
| Bob O Evans | https://awards.acm.org/award-recipients/evans_1002203 | 404 |
| David John Wheeler | https://awards.acm.org/award-recipients/wheeler_1002054 | 404 |
| J Presper Eckert | https://awards.acm.org/award-recipients/eckert_4037602 | 404 |
| Peter Elias | https://awards.acm.org/award-recipients/elias_1192715 | 404 |
| Roger M Needham | https://awards.acm.org/award-recipients/needham_1674183 | 404 |

No replacement URLs have been confirmed for these entries. Keep their profile
cells blank until a valid replacement is verified; retain the ACM Fellow rows.

## Turing Award reconciliation and profile crawl

The dataset enumerates 81 recipients across award years 1966–2025, all with
verified ACM recipient URLs. [PR #47](https://github.com/lintool/cs-big-cows/pull/47)
reconciled the recipients and award years with ACM and
[Wikipedia revision 1373210156](https://en.wikipedia.org/w/index.php?title=Turing_Award&oldid=1373210156),
corrected citation text, and completed profile-link coverage. Official-source
and Wikipedia citation discrepancies are recorded in
[issue #46](https://github.com/lintool/cs-big-cows/issues/46).

The fresh Safari crawl completed at `2026-09-13T23:48:11Z`: all 81 profiles
were fetched successfully in 81 attempts, with 81 distinct HTML captures. It
used the shared crawler's Turing mode, including modern ACM award profiles and
legacy `amturing.acm.org` recipient pages. All identities and award years were
checked against the captured HTML.

Retained local artifacts under `../bigcows-crawler/.cache/` are:

- `acm-turing-profile-cache-2026-09-13.json`: captured HTML and parsed fields.
- `acm-turing-profile-input-2026-09-13.csv`: original input snapshot.
- `acm-turing-profile-report-2026-09-13.json` and `acm-turing-profile-state-2026-09-13.json`: original completion records.
- `acm-turing-profile-manifest-2026-09-13.json`: input checksum, award, date, and artifact paths.
- `acm-turing-profile-log-2026-09-13.txt`: console log.

These artifacts are Git-ignored and are not shipped with either repository.
They share the cache directory and date with the Fellows crawl but use a separate
prefix. The crawl snapshot predates the Kahan punctuation correction in
[PR #48](https://github.com/lintool/cs-big-cows/pull/48); use read-only comparison
for the current CSV and the original snapshot when resuming the retained crawl.

The original completion report flagged seven profiles. After the Kahan correction,
comparison with the current CSV has six citation differences, ten exact name
differences, and one location difference, with no name-compatibility or year
mismatches. Preserve the reviewed differences:

- Bennett and Brassard: retain the 2025 citation supported by ACM's
  [announcement](https://www.acm.org/media-center/2026/march/turing-award-2025).
  Their recipient pages use a different official version; see issue #46.
- Barto, Sutton, and Wigderson: retain terminal periods missing from ACM's text.
- Alan Kay: retain the citation without the surrounding quotation marks on ACM.
- Charles H. Bennett: retain `USA` rather than the page's `United States`.
- Keep existing name forms where differences are initials, middle names, or punctuation.

These counts describe the September 13 captures and the post-#48 CSV, not a
live inventory. A fresh capture is evidence for review, not an instruction to
overwrite better canonical data.

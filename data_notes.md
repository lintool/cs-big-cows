# Data Notes

## ACM Fellow profile crawl oddities

On 2026-09-13, the `acm_fellow_profile` cells for 11 HTTP 404 URLs were cleared
in `data/acm_fellows.csv`, and those URLs were removed from the shared cache.
All 11 Fellow rows and their other fields were preserved. The cleanup initially
used cached responses from April 28–29, 2026; later browser checks also found
those individual pages unavailable. No verified replacements were found.

After reconciliation and duplicate consolidation, the dataset contains 1,638
Fellows: 1,627 nonempty ACM profile URLs and 11 blank profile cells. The fresh
recrawl completed at `2026-09-13T19:53:05Z`: all 1,627 URLs have complete cached
HTML and status `ok`, with no remaining fetch failures or duplicate HTML captures.
The CSV was not changed by the recrawl. The previous shared cache was preserved;
the fresh cache/report live in `../bigcows-crawler/.cache/acm-recrawl-2026-09-13/`
and are not committed.

Three field differences remain for review; preserve the existing CSV values:

- Nikolaj Bjørner: ACM displays `Bjorner Nikolaj`.
- Frank Wm Tompa: the current profile has no parsed citation.
- Richard R. Burton: ACM's citation ends with `analysi`, missing the final `s`.

An initial stale-page capture for Antonio Gonzalez contained the preceding Andrew
Tomkins page. It was preserved separately and refetched correctly after switching
to the reusable crawler's stronger page-clearing check. It is not a CSV error.

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

## ACM crawling notes

The recommended approach as of 2026-09-13 is **regular Safari through AppleScript**
on macOS. Direct HTTP, Playwright-controlled Chrome (including incognito), and
Safari WebDriver encountered repeated blocking in the fresh recrawl. Native
Safari AppleScript navigation/source access sustained the completed recrawl; the
reusable crawler handled its final 1,022 fetches.

From `cs-big-cows`, use the reusable shared crawler:

```sh
python3 ../bigcows-crawler/scripts/cache_acm_fellow_profiles_safari.py --data data/acm_fellows.csv
```

For a fresh, resumable crawl that preserves the previous cache, choose a new
cache directory and repeat the same command to resume:

```sh
python3 ../bigcows-crawler/scripts/cache_acm_fellow_profiles_safari.py --data data/acm_fellows.csv --cache ../bigcows-crawler/.cache/acm-refresh/cache.json --report ../bigcows-crawler/.cache/acm-refresh/report.json
```

The defaults are 5–7 seconds between profiles and 60–90 seconds every 25 fetch
attempts, plus bounded backoff on errors. Approve macOS permission for the
launching application to control Safari and leave the dedicated crawl window
open. This approach does not require Playwright, remote debugging, Safari's
remote automation setting, or JavaScript from Apple Events.

The cache stores full loaded HTML, timestamps, and parsed metadata. Safari does
not expose HTTP response codes: `status_code` is `null`, and error pages are
recognized from HTML. Browser caching still applies. Successful cached HTML is
reused; transient failures retry automatically. Use `--retry-status http_error`
for cached error pages, and `--refresh` only to intentionally replace existing
entries. CSV changes require separate review. See the
[shared crawler reference](../bigcows-crawler/README_FOR_AGENTS.md) for details.

The earlier Chrome/CDP technique remains historical evidence for the April 2026
crawl. Its ACM Playwright script has been removed from the shared crawler; use
the Safari/AppleScript command above for current and future ACM profile crawls.

# Data Notes

## ACM Fellow profile crawl oddities

As of the 2026-04-29 ACM Fellow profile crawl, `data/acm_fellows.csv` contains
1,640 ACM Fellow profile URLs. The local cache/report live under `.cache/` and
are intentionally not committed.

Current cached profile status counts:

```text
Status       Count  Meaning
----------  -----  ---------------------------------------------
ok           1629  Profile page fetched and parsed successfully.
blocked         0  No blocked/interstitial pages remain.
http_error     11  ACM returned real 404 pages.
missing         0  No missing ACM profile URLs.
```

Total profiles: 1,640. Cached profiles: 1,640. Review candidates: 215. The
current report was generated at `2026-04-29T01:45:49Z`.

The following people appear in `data/acm_fellows.csv`, but their individual ACM
profile URLs currently return ACM 404 pages with page name
`404 - Your Page Could Not Be Found`:

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

No replacement URLs have been confirmed for these entries. Treat the ACM
directory/profile URL as the current CSV value unless ACM fixes or replaces the
individual profile page.

## ACM crawling notes

Direct `urllib` requests and fresh Playwright browser profiles can be blocked by
ACM/Cloudflare. The working approach is to use the Playwright crawler against a
user-launched Chrome instance with remote debugging enabled:

```sh
open -na "Google Chrome" --args --remote-debugging-port=9222 --user-data-dir="$PWD/.cache/chrome-acm-cdp"
python scripts/cache_acm_fellow_profiles_playwright.py --cdp-url http://127.0.0.1:9222 --retry-status blocked
```

The crawler is idempotent and cache-backed. Use `--retry-status blocked` to
refresh blocked cache entries, and use `--refresh` only when intentionally
recrawling already-successful pages.

The successful retry used randomized pacing, for example:

```sh
python scripts/cache_acm_fellow_profiles_playwright.py --cdp-url http://127.0.0.1:9222 --retry-status blocked --delay 4 --delay-jitter 2 --batch-size 25 --batch-size-jitter 5 --batch-pause 90 --batch-pause-jitter 30
```

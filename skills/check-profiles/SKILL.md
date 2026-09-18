---
name: check-profiles
description: Verify ACM Fellows and Turing Award winners' linked Google Scholar, DBLP and CSRankings identities, publication coverage and profile quality in acm-bigcows. Use for individual checks or complete roster reviews.
---

# Check Profiles

Use in the `acm-bigcows` repository.
Unless the user specifies a subset, review every row in `data/acm_fellows.csv` and `data/turing_award_winners.csv`, including missing links and existing `N` ratings.
Evaluate Google Scholar, DBLP and CSRankings separately for each recipient, then reconcile the evidence across services.
Attempt to establish a CSRankings name link for every recipient whose `csrankings_name` is blank, alongside the Scholar and DBLP checks.
Creating or editing this skill does not initiate a profile review.

## Ground Truth and Scope

Read the repository's `AGENTS.md`, [publication quality criteria](../../README_FOR_AGENTS.md#publication-profile-quality), [CSRankings name-link guidance](../../README_FOR_AGENTS.md#csrankings-name-links), and the latest relevant [Data Notes](../../docs/data_notes.md), including cited reviews and explicit user decisions.
Read the [current review status](../../docs/profile_review_status.md) before resuming; update that index when inspection progress or open cases change, and distinguish inspected notes from applied CSV changes and completed audits.
The ACM directory name, recipient profile and award citation establish the recipient's identity and recognized work.
Preserve ACM names, award years, citations and profile links unless strong, cited evidence establishes an actual error; a different spelling on Scholar, DBLP or CSRankings alone is insufficient.
Preserve existing documented ACM corrections and historical recipients omitted from the current directory.
When an ACM profile is unavailable, use retained ACM evidence and corroborating institutional or recipient sources, and state the limitation.
Do not silently make another publication profile the ground truth.

Invoking this skill authorizes correcting obvious errors in the reviewed profile URLs, quality flags and CSRankings name links, with their dependent dates and profile-table associations, unless the user requests a read-only review or dry run.
Apply a correction when concrete, converging evidence supports a clear decision; record the previous value, new value and evidence.
For a proven wrong-person link, use an independently verified replacement if available; otherwise clear the incorrect association and its dependent date rather than inventing a replacement.
An unavailable, invalid or potentially withdrawn profile is a separate case: follow the flag-for-review policy below instead of automatically clearing, replacing or restoring it.
Rate a clearly contaminated or inadequately covered publication profile `N` even when the person matches; retain the URL unless a clearly supported better profile is found under the search workflow below.
Correct ACM data only under the stronger ground-truth exception above, with strong cited evidence of an actual error.
For borderline identity, coverage or contamination findings, preserve the existing values and flag the case for user review with the competing evidence, proposed action and specific decision needed.
Keep a separate review queue; do not invent a third quality value or use `N` solely to signal uncertainty.
Do not ask again for permission already given in the current task.
Preserve unrelated fields, row order and manually accepted decisions.
Do not regenerate visualizations unless the user requests it.

## Evidence Collection

Snapshot the input rosters and profile tables and create a per-recipient review queue before editing.
Keep both award rows for shared recipients in the audit; reuse evidence for the same person/profile, then check that conclusions and any applied changes agree across rosters.
Use recipient IDs, award years and stored URLs to connect older evidence to current names; do not rely on historical spelling or row numbers alone.

Start with existing crawls, publication lists, review evidence and cached CSRankings source files.
Inventory their capture dates, completeness and gaps, then ask whether the user wants to update the evidence before starting any crawl or source refresh, unless that update is already authorized.
Explain that refreshing can be time-consuming and offer to use existing evidence, refresh selected gaps or refresh the full requested scope; provide an approximate effort estimate only when supported by crawl size and pacing information.
Continue useful inspection of existing evidence while awaiting the answer, but do not start the proposed refresh without approval.
If the user keeps the existing evidence, perform the review against those captures and label conclusions with the evidence dates; do not imply a live availability check or advance capture dates merely for re-reviewing them.
Existing captures can support identity and quality judgments as of their capture dates, but cannot prove that a profile remains available or unchanged today.
Assess the captured content rather than simply inheriting existing quality ratings; flag cases whose evidence is missing, incomplete or insufficient for a supported decision.
For an approved refresh, use a new run or explicit refresh that actually fetches upstream content; reparsing a cached success or changing its date is not a fresh crawl.
For future approved Scholar refreshes, collect a larger most-cited publication page and a recent-publications page before judging overall profile quality.
Record both ordering modes, actual retrieved counts and pagination limits; expand further when gaps or suspicious clusters require it.
An existing 20-entry most-cited capture can support identity and sampled-quality findings, but leave broader coverage and recent-work assessment explicitly unresolved when those portions are absent.
This collection policy does not authorize a refresh when the user has chosen existing evidence.
When resuming an approved crawl, reuse its successful captures and fetch unfinished profiles within the approved scope; record each capture's actual timestamp.
Follow the [crawler and reviewed import workflows](../../README_FOR_AGENTS.md#crawlers) before bulk fetching; store captures, hashes, timestamps, input snapshots and run state under `../bigcows-crawler/.cache/`.
Record whether evidence is newly fetched or retained and when it was captured.
Search for corroboration on the recipient's or institution's website, CV, publication list, award announcement or publisher pages as needed.
Search-result snippets can identify leads but do not establish complete publication coverage.

For each recipient, build an identity assessment using the ACM name and citation together with name variants, research areas, country, current and historical institutional affiliations, career chronology, coauthors and representative publications.
Compare the ACM award-time country and institution with the locations and affiliations in Scholar, DBLP, CSRankings, institutional biographies and publication metadata, recording the dates or periods each describes.
Account for moves between countries or institutions, joint and visiting appointments, renamed institutions and stale profile metadata before declaring a mismatch.
When the name, research and publication evidence otherwise converge, a location or affiliation difference alone is not an actionable issue or a reason to ask the user for a decision.
Consider relocation as a possible explanation without claiming a move occurred unless supported; escalate only when the combined evidence leaves a material identity conflict.
Use country and institution as corroborating or conflicting evidence, not as standalone proof of identity; shared institutions do not resolve namesakes, and different current countries do not by themselves disprove a match.
Keep affiliation country distinct from citizenship or nationality, and leave unknown locations unknown rather than inferring them from a person's name.
Treat name normalization, shared Scholar IDs, DBLP aliases and CSRankings identifiers as candidate evidence, not proof.
Inspect contradictory evidence explicitly: identical names and adjacent research areas can still describe different people, and institutional moves can explain different affiliations.
Do not let a copied or previously inferred cross-service association corroborate itself.

## Invalid, Unavailable or Withdrawn Profiles

Flag any previously linked profile that the inspected evidence shows as missing, invalid, private, redirected to an unrelated destination or explicitly withdrawn upstream, stating when that condition was observed.
Do not claim a new disappearance based solely on an old capture or the absence of a local cache file.
Record the original URL or CSRankings key, fetch time, response status, final URL, visible message and any evidence distinguishing a removal from an access failure.
Separate a confirmed removal or withdrawal from a suspected removal and from temporary failures such as timeouts, rate limits, CAPTCHA or login barriers.
A failed request, an empty crawler result or a missing CSRankings row alone does not prove that the author withdrew the profile.
Use the crawler's bounded retries and inspect the returned page before classifying the outcome; do not repeatedly retry or bypass a privacy or withdrawal decision.

Preserve stored values pending the user's review and report the availability finding with its evidence date; a previous `Y` must not be presented as proof of current availability.
Do not advance a successful-capture date on failure, infer a quality change solely from disappearance, or automatically replace or recreate a potentially withdrawn profile from cached, archived or mirrored copies.
Respect an explicit upstream withdrawal and flag the local link and dependent data for the user's disposition; historical evidence is provenance, not authorization to republish or restore withdrawn content.
For CSRankings, distinguish an already documented historical absence from a newly disappeared entry, and flag the latter without automatically dropping or relinking it.
Continue independent checks of the recipient's other services; one service's removal does not invalidate another service's profile or ACM award record.

## Google Scholar and DBLP

For each linked profile, record three separate findings: whether it represents the recipient, whether its publication coverage is substantial, and whether unrelated publications materially contaminate it.
An identity match alone does not establish a good-quality profile.

The user has chosen sampling across highly cited or otherwise central works, recent publications and older work across the recipient's career as the default inspection method.
Do not require inspection of every publication by default; record the sampled scope and expand it when concerns arise.
Check publication titles, authors/coauthors, venues, dates and topics against the ACM-recognized contributions and independent publication evidence.
Examine suspicious clusters beyond the initial sample; broaden inspection when names, topics, chronology or affiliations conflict.
A few matching papers do not establish that the rest of a profile belongs to the recipient.

Both Scholar and DBLP should contain substantial numbers of publications and represent a meaningful part of the recipient's established body of work.
Record the observed publication count or a clearly labeled lower bound, the years covered and how much of the list was inspected.
Distinguish a complete sparse bibliography from a short first page, pagination, an incomplete crawl, a filtered view or an access challenge.
Citation totals and h-index are not publication counts and do not establish identity or completeness.
The user has chosen contextual judgment rather than a numerical minimum: assess substantial coverage relative to the recipient's career and known bibliography, recording actual publication counts or clearly labeled lower bounds.
Do not use a fixed publication-count threshold as an automatic acceptance or rejection rule.
A genuinely sparse profile is evidence of a poor match or inadequate coverage even if some entries fit; a justified exception needs positive identity and coverage evidence recorded in the audit.

Apply the [quality criteria](../../README_FOR_AGENTS.md#publication-profile-quality) independently to each service:

| Finding | Quality Decision |
| --- | --- |
| Supported identity, substantial coverage, and mostly relevant or adjacent publications without substantial contamination | `Y`, allowing isolated attribution errors. |
| Wrong person | `N`, with the conflicting identity evidence. |
| Correct person but substantial unrelated publications, mixed identities or a large unrelated cluster | `N`, even when many papers or a majority are relevant. |
| Obviously incomplete or genuinely sparse coverage without a supported exception | `N`, with actual counts and the coverage concern; do not automatically call it a wrong-person match. |
| Missing stored link | `N`; record that service as missing rather than claiming no public profile exists. |
| Previously linked profile now invalid, unavailable or potentially withdrawn | Flag its availability status for user review; preserve stored values pending disposition and do not treat old evidence as fresh verification. |
| Fetch blocked or available evidence insufficient to assess identity, coverage or contamination | Mark the review unresolved and preserve the previous rating; do not call it verified or infer `N` from access failure alone. |

Substantial contamination is a judgment about the amount, persistence and significance of unrelated work, not a fixed percentage rule.
Consider legitimate interdisciplinary work, career changes and collaborations before calling publications unrelated.
Isolated questionable or misattributed publications are acceptable when the identity, coverage and overall bibliography otherwise support `Y`.
Do not downgrade, seek a replacement or open a user-review item solely for such isolated entries; a brief informational audit note is sufficient.
Expand inspection when an isolated concern may indicate a larger cluster, and flag or reject substantial contamination under the criteria above.
Preserve explicit user ratings unless the user authorizes reconsideration; report new conflicting evidence instead of silently reversing them.
Quality `N` does not itself authorize deleting a stored URL.

## Search for Missing or Better Profiles

Whenever a Scholar or DBLP profile is low quality, perform a general web search for a better profile on that service, including cases that already had an `N` rating before the run.
Whenever a stored Scholar or DBLP link or CSRankings name link is missing, perform a general web search for good matches; also search for the correct CSRankings entry when the existing association is a wrong-person match.
Do not limit discovery to the local tables, existing identifiers or a service's internal search.
Use name variants together with the service name, current and historical institutions, country, research area or distinctive publication titles to distinguish candidates.
Follow links from the recipient's own homepage, institutional biography or CV when available, and inspect the actual candidate profiles rather than accepting search-result snippets.

Apply the same holistic identity, publication-coverage and contamination checks to each plausible replacement, starting with any existing captures for that exact candidate.
General web searches and inspection of public candidate pages remain part of discovery; they do not imply authorization for a bulk crawl or source refresh.
If verifying candidates requires additional crawling or source downloads, include those in the user's refresh choice or ask for a targeted update, grouping candidates rather than asking once per profile.
A same-name result, larger publication count or higher citation count alone does not make a candidate better.
For Scholar and DBLP, accept a replacement only when both identity and quality are clearly supported; do not substitute one poor profile for another merely because it is less poor.
For CSRankings, verify the exact source key and affiliation history against the selected cached or newly refreshed source files and independent identity evidence, recording source dates.

In a normal invocation, add clearly supported missing links and replace low-quality links with clearly supported good alternatives, updating quality flags, dependent dates and CSRankings table associations consistently.
Preserve the old URL, its quality finding and the evidence for replacement in the audit.
An explicit user decision about the old profile remains part of its history; it does not certify or determine the quality of a different candidate URL.
If multiple plausible profiles remain, available candidate evidence is insufficient, or the improvement is borderline, flag the alternatives for user review without changing the association.
When no good match is found, retain a correctly identified low-quality profile with `N`, or leave a missing link blank, and record the search outcome without claiming that no profile exists.

The withdrawal safeguards still apply: search may clarify a disappeared profile or reveal an author-published successor, but do not automatically restore or replace a potentially withdrawn profile or use archived copies as a substitute.
Flag any such successor candidate for the user's review alongside the disappearance evidence.
Record search queries, search dates, candidate URLs or exact name keys, reasons for acceptance or rejection, and any unresolved alternatives.

## CSRankings

For every recipient, either verify the existing `csrankings_name` or attempt to find a supported exact source name; do not stop at checking populated links.
Search the selected cached faculty sources, documented historical profile records and available alias/name-change evidence for candidates, and perform the general web search required for missing links.
Use name variants, country, current and historical affiliations, research areas, publications, Scholar IDs and independently verified DBLP identities together to evaluate candidates.
A missing or poor-quality Scholar or DBLP profile does not preclude a CSRankings link supported by other evidence.
Add a clearly supported match using the source's exact `name`, including punctuation, disambiguation numbers and campus tags, and set `csrankings_name_alignment_date` to the UTC date the association is accepted.
Keep the ACM name unchanged; store the CSRankings identity only in its dedicated field.
For ambiguous candidates, leave the name link blank and flag the alternatives for review; when no supported match is found, leave it blank and record the searches performed.
If a candidate needs source files or captures not already available, follow the evidence-refresh approval policy rather than automatically downloading them.

Resolve every populated `csrankings_name` exactly once against `data/csrankings_profiles.csv`; investigate absent or duplicate keys.
Compare the row's original name, institutional affiliation and its country, homepage, `scholarid` and any `dblp_profile` with the recipient's independently supported identity and affiliation history.
Use the selected cached faculty sources or an approved refresh to check inclusion as of the source date, and retained historical records to establish historical provenance.
Do not describe inclusion in an older source snapshot as confirmed current inclusion.
Respect source disambiguation numbers and campus tags: stripping them for candidate generation must not erase evidence of a namesake.
Ignore blank identifiers and `NOSCHOLARPAGE` as matching evidence.
The current table's DBLP field reproduces CSRankings' name-generated link; follow the [generation and acquisition rules](../../README_FOR_AGENTS.md#csrankings-dblp-link-generation).
Earlier audits used roster-derived DBLP links and cannot independently corroborate those same roster associations.
For current links, inspect retained captures or an approved refresh, recording the original generated URL, final URL, evidence time and author identity.
Compare the resolved author with the award-roster profile; `/pers/hd/` and `/pid/` spelling differences alone are not evidence of different people.
Generation is not a successful capture and does not update profile-crawl or name-alignment dates.
An upstream Scholar identifier can also be wrong; investigate conflicts rather than deciding by identifier alone.
Preserve the original CSRankings source fields, including demonstrably incorrect upstream identifiers; ignore established source errors as matching evidence and do not try to repair them.
Once independent evidence supports the recipient’s name association, treat an obvious upstream error as non-actionable; record a brief audit note when useful without opening a user-review item or repeatedly asking whether to fix it.
Do not modify upstream sources or submit upstream correction requests as part of this skill.
Use the independently reviewed award-roster profile for the accepted association; do not overwrite source fields or add override columns without a separate user request.

Classify the link as supported, wrong person, unresolved or missing in the audit; do not invent a CSRankings quality column.
Documented historical profiles absent from the latest sources remain eligible when identity and provenance are supported.
When applying obvious link corrections, preserve exact accepted keys and synchronize the table to the union of populated keys across both rosters using the name-link guidance.
Include newly accepted links in that synchronization, copying the original CSRankings source fields and retaining provenance for historical exceptions.
Check that each key belongs to only one recipient within a roster and that shared Fellows/Turing recipients use the same accepted key.
Do not run the legacy name-inference builder to regenerate the canonical table.
Always derive the lookup table's DBLP URL from the original CSRankings name; never copy a reviewed award URL or redirect destination into it, or clear it because upstream is wrong.
Keep independently reviewed DBLP links and quality decisions in the award rosters; preserve CSRankings-generated links and flag material conflicts in the audit.

## Update CSV Dates

Apply date changes together with the corresponding accepted data changes, using UTC `YYYY-MM-DD` values.
Keep capture dates, name-alignment decision dates and table-synchronization dates distinct.
The CSRankings lookup table has no date column; record synchronization time in Data Notes and retain source-download timestamps in the evidence audit.

| CSV Field | Required Update |
| --- | --- |
| `acm_fellow_profile_crawl_date`, `google_scholar_profile_crawl_date`, `dblp_profile_crawl_date` in both award rosters | Use the actual `fetched_at` UTC date of the accepted successful capture for the stored URL. An accepted new capture updates the date even if the URL is unchanged. |
| Capture date when a profile URL is added or replaced | Clear any old URL's date and use the accepted capture date for the new URL, including when the evidence is an existing crawl. Leave blank if no accepted successful capture exists; never substitute today's review date. |
| Capture date when a profile URL is cleared | Clear the paired date in the same edit, and set the applicable Scholar or DBLP quality flag to `N`. |
| Capture date during a quality-only review, failed fetch or pending withdrawal decision | Preserve the previous accepted date unless a different successful capture is actually accepted. Record the review or failed-attempt timestamp in the audit instead. |
| `csrankings_name_alignment_date` in both award rosters | Set to the UTC decision date when adding, changing or explicitly revalidating a supported name link, even if using existing evidence. Clear it when removing the name link; preserve it for unresolved cases, unrelated edits or source refresh alone. |
| `crawl_date` in `data/google_scholar_profiles.csv` | If importing a Scholar record, derive its date from the same accepted capture as its stored profile data and metrics. Do not restamp old metrics to the date of a newer identity check. |

Keep dates consistent across shared award recipients using the same accepted profile capture or name-alignment decision.
Preserve capture timestamps and source dates in the evidence audit so every changed CSV date has a traceable basis.
Validate that cleared URLs and name links have blank paired dates, populated dates parse correctly, and no date was advanced simply because the skill ran.
After changing profile links, capture dates or Scholar imports, rebuild the [capture/import queue](../../README_FOR_AGENTS.md#capture-and-import-backlog); queue generation reads local data only and does not authorize a refresh.

## Record and Validate the Review

Produce a dated row audit covering every requested recipient and all three services.
Record the roster, ACM recipient identity and year, reviewed URL or name key, evidence mode (existing captures or approved refresh), fetch outcome where applicable and availability status as of the evidence date, prior and proposed quality, identity finding, country and institutional evidence with relevant time periods, publication count and inspection scope, coverage finding, contamination finding, concrete rationale, evidence URLs/capture dates, unresolved questions and action taken.
For CSRankings, publication-count and quality fields are not applicable; record the identity and source-provenance findings instead.
Record representative relevant and conflicting publications where they determine the decision.
Write the review summary and a completion-time entry in Data Notes according to repository conventions; preserve older audits as historical evidence.

Validate changes against the input snapshots: only authorized fields changed, original award rows/order remain intact, shared-recipient decisions agree, and every populated CSRankings key resolves exactly once with no unreferenced table rows.
Apply the CSV date updates above and the repository's [profile capture-date rules](../../README_FOR_AGENTS.md#profile-crawl-dates), checking old and new dates in the field-level audit.
Verify every CSRankings DBLP link matches upstream-compatible generation, including links with known upstream errors, and that generated visualizations remain unchanged.
Run the source-field manifest checks; after an authorized source update, rebuild that manifest only from the independently retained inputs described in the name-link guidance, never merely to bless a local mismatch.

Report per-roster and per-service totals for reviewed, supported, poor-quality, missing and unresolved cases, distinguishing award rows from unique people and identity problems from coverage or contamination.
Separate applied obvious corrections from borderline cases awaiting the user's decision, and present the latter with enough evidence for individual review.
Report invalid, disappeared and potentially withdrawn profiles separately from missing stored links and ordinary quality problems.
Complete a full sweep only when every requested row has a recorded outcome; blocked or uncertain profiles remain explicitly unresolved.
For a long review, retain resumable progress and identify what remains rather than presenting a sample as a completed sweep.

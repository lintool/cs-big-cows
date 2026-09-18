"""Read-only checks for reviewed profile associations across canonical tables."""
from datetime import date
from urllib.parse import urlsplit
try:
    from csrankings_dblp import csrankings_dblp_url
except ModuleNotFoundError:
    from scripts.csrankings_dblp import csrankings_dblp_url


def normalize_dblp_url(value):
    return (value or "").strip().replace("http://", "https://", 1).split("?", 1)[0].split("#", 1)[0].rstrip("/").removesuffix(".html")


def acm_recipient_id(url):
    if not url:
        return ""
    # Directory/profile slugs use an alphanumeric recipient ID after the last
    # underscore; legacy URLs can end in .cfm and vary in case.
    slug = urlsplit(url).path.rstrip("/").lower().removesuffix(".cfm")
    return slug.rsplit("/", 1)[-1].rsplit("_", 1)[-1]


def validate_alignment_dates(rows):
    for row in rows:
        key = row.get("csrankings_name", "")
        value = row.get("csrankings_name_alignment_date", "")
        if bool(key) != bool(value):
            raise ValueError(f"CSRankings name/date presence mismatch: {row['name']}")
        if value:
            try:
                valid = date.fromisoformat(value).isoformat() == value
            except ValueError:
                valid = False
            if not valid:
                raise ValueError(f"Invalid CSRankings alignment date: {row['name']}: {value}")


def validate_shared_recipients(rosters):
    """Compare independently identified shared people, not just shared URLs.

Only ACM recipient IDs establish cross-award identity here. Missing ACM IDs
are deliberately not inferred from names or publication-profile links.
"""
    seen = {}
    fields = ["dblp_profile", "dblp_profile_crawl_date", "dblp_profile_quality",
              "google_scholar_profile", "google_scholar_profile_crawl_date", "google_scholar_profile_quality",
              "csrankings_name", "csrankings_name_alignment_date"]
    compared = 0
    for roster, rows in rosters.items():
        for row in rows:
            identity = acm_recipient_id(row.get("acm_fellow_profile", ""))
            if not identity:
                continue
            if identity in seen:
                previous_roster, previous = seen[identity]
                if previous_roster == roster:
                    raise ValueError(f"Duplicate ACM recipient ID in {roster}: {identity}")
                compared += 1
                for field in fields:
                    left, right = previous[field], row[field]
                    if field == "dblp_profile":
                        left, right = normalize_dblp_url(left), normalize_dblp_url(right)
                    if left != right:
                        raise ValueError(f"Shared recipient {identity} ({row['name']}) differs in {field}: {previous_roster} / {roster}")
            else:
                seen[identity] = (roster, row)
    return compared


def validate_derived_dblp_links(rosters, profiles):
    """Require upstream-generated links and exact key coverage, not roster URLs."""
    by_name = {}
    for profile in profiles:
        if profile["name"] in by_name:
            raise ValueError(f"Duplicate CSRankings key: {profile['name']}")
        by_name[profile["name"]] = profile
        expected = csrankings_dblp_url(profile["name"])
        if profile["dblp_profile"] != expected:
            raise ValueError(f"CSRankings-generated DBLP mismatch for {profile['name']}: expected {expected!r}")
    referenced = set()
    owners = {}
    for roster, rows in rosters.items():
        roster_keys = set()
        for row in rows:
            key = row.get("csrankings_name", "")
            if not key:
                continue
            if key in roster_keys:
                raise ValueError(f"Repeated CSRankings key in {roster}: {key}")
            roster_keys.add(key)
            identity = acm_recipient_id(row.get("acm_fellow_profile", ""))
            if key in owners:
                previous_roster, previous_identity = owners[key]
                if not identity or not previous_identity or identity != previous_identity:
                    raise ValueError(f"Conflicting or unverified CSRankings key ownership for {key}: {previous_roster} / {roster}")
            else:
                owners[key] = (roster, identity)
            referenced.add(key)
            if key not in by_name:
                raise ValueError(f"Missing CSRankings key: {key}")
    if referenced != set(by_name):
        raise ValueError(f"Unreferenced CSRankings keys: {sorted(set(by_name) - referenced)}")

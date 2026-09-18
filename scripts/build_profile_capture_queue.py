#!/usr/bin/env python3
"""List accepted profile URLs needing capture/import without fetching anything."""
import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path

try:  # Support direct CLI execution and importing from the repository root.
    from profile_validation import normalize_dblp_url
except ModuleNotFoundError:
    from scripts.profile_validation import normalize_dblp_url

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def build_queue(rosters, metrics):
    metrics_urls = {row["profile"] for row in metrics}
    tasks = {}
    for roster, rows in rosters.items():
        for row in rows:
            for service, field in [("acm", "acm_fellow_profile"), ("dblp", "dblp_profile"), ("scholar", "google_scholar_profile")]:
                url = row[field]
                if not url:
                    continue
                reasons = []
                if not row[field + "_crawl_date"]:
                    reasons.append("no_accepted_capture")
                if service == "scholar" and url not in metrics_urls:
                    reasons.append("missing_metrics_import")
                if not reasons:
                    continue
                grouped_url = normalize_dblp_url(url) if service == "dblp" else url
                task = tasks.setdefault((service, grouped_url), {"service": service, "url": grouped_url,
                    "status": "awaiting_refresh_approval", "reasons": [], "recipients": []})
                task["reasons"] = sorted(set(task["reasons"]) | set(reasons))
                task["recipients"].append({"roster": roster, "name": row["name"], "award_year": row["year"],
                                           "acm_profile": row["acm_fellow_profile"], "stored_url": url})
    return sorted(tasks.values(), key=lambda task: (task["service"], task["url"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rosters = {name: read_csv(ROOT / "data" / name) for name in ["acm_fellows.csv", "turing_award_winners.csv"]}
    tasks = build_queue(rosters, read_csv(ROOT / "data/google_scholar_profiles.csv"))
    if args.output.resolve() in {path.resolve() for path in (ROOT / "data").glob("*.csv")}:
        parser.error("Queue output cannot overwrite canonical inputs")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"schema_version": 2, "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Accepted stored links only; excludes missing links and unadopted discovery candidates",
        "tasks": tasks}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(tasks)} capture/import tasks; no requests made")


if __name__ == "__main__":
    main()

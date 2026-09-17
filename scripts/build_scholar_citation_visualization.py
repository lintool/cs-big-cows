#!/usr/bin/env python
"""Generate a JavaScript citation dataset for ACM Fellows or Turing Award winners."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ACM = APP_ROOT / "data" / "acm_fellows.csv"
DEFAULT_TURING = APP_ROOT / "data" / "turing_award_winners.csv"
DEFAULT_SCHOLAR = APP_ROOT / "data" / "google_scholar_profiles.csv"
DEFAULT_OUTPUT = APP_ROOT / "docs" / "scholar_data.js"
DEFAULT_TURING_OUTPUT = APP_ROOT / "docs" / "turing_scholar_data.js"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--award", choices=("fellows", "turing"), default="fellows", help="Award roster to visualize (default: fellows).")
    parser.add_argument("--roster", "--acm", dest="roster", type=Path, help="Override the selected award's input CSV (--acm is a legacy alias).")
    parser.add_argument("--scholar", type=Path, default=DEFAULT_SCHOLAR, help="Path to data/google_scholar_profiles.csv.")
    parser.add_argument("--output", type=Path, help="Override the award-specific JavaScript output path (does not regenerate HTML).")
    args = parser.parse_args()
    args.roster = args.roster or (DEFAULT_TURING if args.award == "turing" else DEFAULT_ACM)
    args.output = args.output or (DEFAULT_TURING_OUTPUT if args.award == "turing" else DEFAULT_OUTPUT)
    return args


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def int_or_none(value: str) -> int | None:
    value = (value or "").strip()
    return int(value) if value else None


def build_data(acm_rows: list[dict[str, str]], scholar_rows: list[dict[str, str]], award: str = "fellows") -> dict[str, Any]:
    scholar_by_profile = {row["profile"]: row for row in scholar_rows if row.get("profile")}
    rows: list[dict[str, Any]] = []
    years: set[int] = set()

    for acm in acm_rows:
        profile = acm.get("google_scholar_profile", "").strip()
        scholar = scholar_by_profile.get(profile) if profile else None
        citation_by_year: dict[str, int] = {}
        if scholar and scholar.get("citation_by_year"):
            citation_by_year = {str(year): int(count) for year, count in json.loads(scholar["citation_by_year"]).items()}
            years.update(int(year) for year in citation_by_year)

        rows.append(
            {
                "name": acm.get("name", ""),
                "year": int_or_none(acm.get("year", "")),
                "location": acm.get("location", ""),
                "acmProfile": acm.get("acm_fellow_profile", ""),
                "scholarProfile": profile,
                "hasScholar": bool(scholar and citation_by_year),
                "crawlDate": (scholar.get("crawl_date") or None) if scholar else None,
                "citations": int_or_none(scholar.get("citations", "") if scholar else ""),
                "hIndex": int_or_none(scholar.get("h_index", "") if scholar else ""),
                "firstCitationYear": int_or_none(scholar.get("first_citation_year", "") if scholar else ""),
                "citationByYear": citation_by_year,
            }
        )

    rows.sort(key=lambda row: (-(row["year"] or 0), row["name"].lower()))
    if not years:
        raise ValueError("No citation-by-year data found")

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "metadata": {
            "award": award,
            "totalRows": len(rows),
            "joinedRows": sum(1 for row in rows if row["hasScholar"]),
            "missingRows": sum(1 for row in rows if not row["hasScholar"]),
            "yearMin": min(years),
            "yearMax": max(years),
        },
        "rows": rows,
    }


def render_data_script(data: dict[str, Any]) -> str:
    # JSON serialization keeps CSV strings as data, including quotes and newlines.
    payload = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)
    payload = payload.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return (
        "// Generated citation dataset; do not edit by hand.\n"
        "// Rebuild with scripts/build_scholar_citation_visualization.py.\n"
        f"window.SCHOLAR_DATA = {payload};\n"
    )


def main() -> int:
    args = parse_args()
    data = build_data(read_csv(args.roster), read_csv(args.scholar), args.award)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_data_script(data), encoding="utf-8")
    print(
        f"Wrote {args.output} rows={data['metadata']['totalRows']} "
        f"joined={data['metadata']['joinedRows']} missing={data['metadata']['missingRows']} "
        f"years={data['metadata']['yearMin']}-{data['metadata']['yearMax']}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

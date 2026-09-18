#!/usr/bin/env python
"""Build a legacy name-inferred CSRankings report in the shared cache.

Each distinct roster DBLP URL is included when its roster name matches exactly
one CSRankings row. This does not verify the DBLP page's identity or enforce a
one-to-one mapping across all URLs. Unmatched and ambiguous names are omitted
from the CSV and summarized in the report. The canonical explicit-key profile
table is protected and cannot be used as an output or report destination.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import string
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE_DIR = APP_ROOT.parent / "bigcows-crawler" / ".cache" / "csrankings"
DEFAULT_FELLOWS = APP_ROOT / "data" / "acm_fellows.csv"
DEFAULT_TURING = APP_ROOT / "data" / "turing_award_winners.csv"
CANONICAL_OUTPUT = APP_ROOT / "data" / "csrankings_profiles.csv"
DEFAULT_OUTPUT = DEFAULT_CACHE_DIR.parent / "csrankings-legacy-profiles.csv"
DEFAULT_REPORT = DEFAULT_CACHE_DIR.parent / "csrankings-profiles-report.json"
CSRANKINGS_COLUMNS = ["name", "affiliation", "homepage", "scholarid", "orcid"]
OUTPUT_COLUMNS = CSRANKINGS_COLUMNS + ["dblp_profile"]
HONORIFICS = {
    "dr",
    "doctor",
    "prof",
    "professor",
    "mr",
    "mrs",
    "ms",
    "sir",
    "dame",
}
SUFFIXES = {
    "jr",
    "sr",
    "ii",
    "iii",
    "iv",
    "phd",
    "dphil",
}
PARTICLES = {"al", "bin", "da", "de", "del", "den", "der", "di", "du", "la", "le", "van", "von"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR, help="Directory containing cached csrankings-*.csv files.")
    parser.add_argument("--fellows", type=Path, default=DEFAULT_FELLOWS, help="ACM Fellows roster containing name and dblp_profile.")
    parser.add_argument("--turing", type=Path, default=DEFAULT_TURING, help="Turing Award roster containing name and dblp_profile.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Legacy output CSV path; canonical profile table is protected.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="JSON report path.")
    args = parser.parse_args()
    for field in ("output", "report"):
        if getattr(args, field).resolve() == CANONICAL_OUTPUT.resolve():
            parser.error(f"--{field} cannot overwrite the canonical CSRankings table; "
                         "synchronize accepted csrankings_name keys instead (see README_FOR_AGENTS.md).")
    return args


def atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(value, encoding="utf-8", newline="\n")
    tmp.replace(path)


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def name_tokens(value: str) -> list[str]:
    # Strip the complete trailing credential before punctuation splits Ph.D.
    # into tokens; a standalone D is a person's initial, not a suffix.
    value = re.sub(r"(?:,\s*|\s+)(?:ph\.?\s*d\.?|dphil)\s*$", "", value, flags=re.IGNORECASE)
    if "," in value:
        surname, given = value.split(",", 1)
        # Keep ordinary trailing suffixes in place (e.g. "John Smith, Jr.").
        if not re.fullmatch(r"(?:jr\.?|sr\.?|ii|iii|iv|ph\.?d\.?|dphil)", given.strip(), re.IGNORECASE):
            value = f"{given} {surname}"
    text = strip_accents(value).lower()
    text = re.sub(r"[^\w\s-]", " ", text)
    text = text.replace("-", " ")
    tokens: list[str] = []
    for raw in re.split(r"\s+", text):
        token = raw.strip("._-")
        if not token or token in HONORIFICS or token in SUFFIXES or re.fullmatch(r"\d{4}", token):
            continue
        tokens.append(token)
    return tokens


def normalized_name(value: str) -> str:
    return " ".join(name_tokens(value))


def useful_last(tokens: list[str]) -> str:
    useful = [token for token in tokens if len(token) > 1 and token not in PARTICLES]
    return useful[-1] if useful else (tokens[-1] if tokens else "")


def compatible_token(left: str, right: str) -> bool:
    return left == right or (len(left) == 1 and right.startswith(left)) or (len(right) == 1 and left.startswith(right))


def compatible_name(left: str, right: str) -> bool:
    left_tokens = name_tokens(left)
    right_tokens = name_tokens(right)
    if not left_tokens or not right_tokens:
        return False

    if normalized_name(left) == normalized_name(right):
        return True

    if useful_last(left_tokens) != useful_last(right_tokens):
        return False

    if not compatible_token(left_tokens[0], right_tokens[0]):
        return False

    left_middle = [token for token in left_tokens[1:-1] if token not in PARTICLES]
    right_middle = [token for token in right_tokens[1:-1] if token not in PARTICLES]
    if bool(left_middle) != bool(right_middle):
        return False

    left_full_middle = [token for token in left_middle if len(token) > 1]
    right_full_middle = [token for token in right_middle if len(token) > 1]
    if not all(any(compatible_token(token, candidate) for candidate in right_middle) for token in left_full_middle):
        return False
    if not all(any(compatible_token(token, candidate) for candidate in left_middle) for token in right_full_middle):
        return False

    left_unmatched_initials = [
        token for token in left_middle if len(token) == 1 and not any(compatible_token(token, candidate) for candidate in right_full_middle)
    ]
    right_unmatched_initials = [
        token for token in right_middle if len(token) == 1 and not any(compatible_token(token, candidate) for candidate in left_full_middle)
    ]
    if left_unmatched_initials and right_unmatched_initials:
        return all(any(compatible_token(token, candidate) for candidate in right_unmatched_initials) for token in left_unmatched_initials) and all(
            any(compatible_token(token, candidate) for candidate in left_unmatched_initials) for token in right_unmatched_initials
        )
    return True


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def read_csrankings_rows(cache_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for letter in string.ascii_lowercase:
        path = cache_dir / f"csrankings-{letter}.csv"
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != CSRANKINGS_COLUMNS:
                raise ValueError(f"{path} has unexpected header {reader.fieldnames!r}")
            rows.extend(dict(row) for row in reader)
    return rows


def build_csrankings_index(rows: list[dict[str, str]]) -> tuple[dict[str, list[dict[str, str]]], dict[str, list[dict[str, str]]]]:
    exact: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_last: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        name = (row.get("name") or "").strip()
        tokens = name_tokens(name)
        if not name or not tokens:
            continue
        exact[normalized_name(name)].append(row)
        by_last[useful_last(tokens)].append(row)
    return exact, by_last


def unique_dblp_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Deduplicate roster links by canonical URL, keeping the first roster's name."""
    valid_rows = []
    seen_profiles: set[str] = set()
    for row in rows:
        name = (row.get("name") or "").strip()
        profile = (row.get("dblp_profile") or "").strip()
        profile = profile.replace("http://", "https://", 1).split("?", 1)[0].split("#", 1)[0].rstrip("/").removesuffix(".html")
        if not name or not profile or profile in seen_profiles:
            continue
        seen_profiles.add(profile)
        item = {"name": name, "profile": profile}
        valid_rows.append(item)
    return valid_rows


def csrankings_candidates_for_name(
    name: str,
    exact: dict[str, list[dict[str, str]]],
    by_last: dict[str, list[dict[str, str]]],
) -> list[dict[str, str]]:
    normalized = normalized_name(name)
    exact_candidates = exact.get(normalized, [])
    if exact_candidates:
        return exact_candidates
    last = useful_last(name_tokens(name))
    return [row for row in by_last.get(last, []) if compatible_name(name, row.get("name", ""))]


def write_output(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


def main() -> int:
    args = parse_args()
    cs_rows = read_csrankings_rows(args.cache_dir)
    cs_exact, cs_by_last = build_csrankings_index(cs_rows)
    dblp_rows = unique_dblp_rows(read_csv(args.fellows) + read_csv(args.turing))

    output_rows: list[dict[str, str]] = []
    unmatched: list[dict[str, Any]] = []
    ambiguous: list[dict[str, Any]] = []
    seen_output_keys: set[tuple[str, str, str, str, str, str]] = set()

    for dblp_row in dblp_rows:
        name = dblp_row["name"]
        candidates = csrankings_candidates_for_name(name, cs_exact, cs_by_last)
        if len(candidates) == 1:
            row = candidates[0]
            key = (
                row.get("name", ""),
                row.get("affiliation", ""),
                row.get("homepage", ""),
                row.get("scholarid", ""),
                dblp_row["profile"],
            )
            if key in seen_output_keys:
                continue
            seen_output_keys.add(key)
            output_row = {column: row.get(column, "") for column in CSRANKINGS_COLUMNS}
            output_row["dblp_profile"] = dblp_row["profile"]
            output_rows.append(output_row)
        elif candidates:
            ambiguous.append(
                {
                    "name": dblp_row["name"],
                    "dblp_profile": dblp_row["profile"],
                    "candidate_count": len(candidates),
                    "candidates": [
                        {column: candidate.get(column, "") for column in CSRANKINGS_COLUMNS}
                        for candidate in candidates[:10]
                    ],
                }
            )
        else:
            unmatched.append({"name": dblp_row["name"], "dblp_profile": dblp_row["profile"]})

    write_output(args.output, output_rows)
    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cache_dir": str(args.cache_dir),
        "fellows": str(args.fellows),
        "turing": str(args.turing),
        "output": str(args.output),
        "csrankings_rows": len(cs_rows),
        "dblp_profiles_rows": len(dblp_rows),
        "included_rows": len(output_rows),
        "unmatched_dblp_profiles": len(unmatched),
        "ambiguous_dblp_profiles": len(ambiguous),
        "unmatched_sample": unmatched[:50],
        "ambiguous": ambiguous[:100],
    }
    atomic_write_json(args.report, report)
    print(
        f"Done. dblp_profiles={len(dblp_rows)} csrankings_rows={len(cs_rows)} included={len(output_rows)} "
        f"unmatched={len(unmatched)} ambiguous={len(ambiguous)} output={args.output} report={args.report}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

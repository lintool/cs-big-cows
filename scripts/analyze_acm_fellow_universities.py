#!/usr/bin/env python3
"""Count ACM Fellow university affiliations from Scholar and CSRankings data."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ACM_FELLOWS = APP_ROOT / "data" / "acm_fellows.csv"
DEFAULT_GOOGLE_SCHOLAR = APP_ROOT / "data" / "google_scholar_profiles.csv"
DEFAULT_CSRANKINGS = APP_ROOT / "data" / "csrankings_profiles.csv"


ALIAS_PATTERNS = [
    (r"\bMIT\b|Massachusetts Inst\.? of Technology|Massachusetts Institute of Technology", "Massachusetts Institute of Technology"),
    (r"\bCMU\b|Carnegie Mellon(?: U\b| University)?", "Carnegie Mellon University"),
    (r"\bUBC\b|University of British Columbia", "University of British Columbia"),
    (r"\bStanford\b|Stanford University", "Stanford University"),
    (r"\bCornell\b|Cornell University", "Cornell University"),
    (r"\bPrinceton\b|Princeton University", "Princeton University"),
    (r"\bHarvard\b|Harvard University", "Harvard University"),
    (r"Columbia University", "Columbia University"),
    (r"\bGeorgia Tech\b|Georgia Institute of Technology", "Georgia Institute of Technology"),
    (r"\bCaltech\b|California Inst\.? of Technology|California Institute of Technology", "California Institute of Technology"),
    (r"\bUIUC\b|Univ\.? of Illinois at Urbana[- ]Champaign|University of Illinois(?: at)? Urbana[- ]Champaign", "University of Illinois Urbana-Champaign"),
    (r"UC Berkeley|U\.?C\.? Berkeley|Univ\.? of California\s*-\s*Berkeley|University of California,? Berkeley", "University of California, Berkeley"),
    (r"\bUCLA\b|Univ\.? of California\s*-\s*Los Angeles|University of California,? Los Angeles", "University of California, Los Angeles"),
    (r"\bUCSD\b|Univ\.? of California\s*-\s*San Diego|University of California,? San Diego", "University of California, San Diego"),
    (r"\bUCSB\b|Univ\.? of California\s*-\s*Santa Barbara|University of California,? Santa Barbara", "University of California, Santa Barbara"),
    (r"\bUCI\b|Univ\.? of California\s*-\s*Irvine|University of California,? Irvine", "University of California, Irvine"),
    (r"Univ\.? of California\s*-\s*Santa Cruz|University of California,? Santa Cruz", "University of California, Santa Cruz"),
    (r"Univ\.? of California\s*-\s*Davis|University of California,? Davis", "University of California, Davis"),
    (r"Univ\.? of California\s*-\s*Riverside|University of California,? Riverside", "University of California, Riverside"),
    (r"\bUW[- ]Madison\b|\bUniv\.? of Wisconsin[- ]Madison\b|University of Wisconsin[- ]Madison", "University of Wisconsin-Madison"),
    (r"\bUW\b(?![- ]Madison)|University of Washington", "University of Washington"),
    (r"\bNYU\b|New York University", "New York University"),
    (r"\bUSC\b|University of Southern California", "University of Southern California"),
    (r"\bEPFL\b|Ecole Polytechnique Federale de Lausanne|École Polytechnique Fédérale de Lausanne", "EPFL"),
    (r"\bETH(?: Zurich| Zürich)?\b|ETH Zurich|ETH Zürich", "ETH Zurich"),
    (r"\bOxford\b|University of Oxford", "University of Oxford"),
    (r"\bCambridge\b|University of Cambridge", "University of Cambridge"),
    (r"\bPurdue\b|Purdue University", "Purdue University"),
    (r"\bUniv\.? of Maryland\s*-\s*College Park|University of Maryland(?:,? College Park)?", "University of Maryland"),
    (r"\bUniv\.? of Pennsylvania\b|\bUPenn\b|University of Pennsylvania", "University of Pennsylvania"),
    (r"\bUniv\.? of Michigan\b|University of Michigan", "University of Michigan"),
    (r"\bUniv\.? of Toronto\b|University of Toronto", "University of Toronto"),
    (r"\bUniv\.? of Waterloo\b|University of Waterloo", "University of Waterloo"),
    (r"University of Wisconsin\s*-\s*Madison|University of Wisconsin, Madison|Univ\.? of Wisconsin\b", "University of Wisconsin-Madison"),
    (r"University of Illinois,? Urbana[- ]Champaign", "University of Illinois Urbana-Champaign"),
    (r"University of Illinois,? Chicago", "University of Illinois at Chicago"),
    (r"\bUniv\.? of Texas at Austin\b|University of Texas at Austin|\bUT Austin\b", "University of Texas at Austin"),
    (r"\bTsinghua\b|Tsinghua University", "Tsinghua University"),
    (r"\bPeking University\b", "Peking University"),
    (r"\bNational University of Singapore\b|\bNUS\b", "National University of Singapore"),
    (r"Chinese University of Hong Kong", "Chinese University of Hong Kong"),
    (r"\bKAIST\b|Korea Advanced Institute of Science and Technology", "KAIST"),
    (r"\bTechnion\b|Technion - Israel Institute of Technology|Israel Institute of Technology", "Technion"),
]

NON_UNIVERSITY_PATTERNS = [
    r"\bGoogle\b",
    r"\bMicrosoft\b",
    r"\bIBM\b",
    r"\bMeta\b",
    r"\bFacebook\b",
    r"\bAmazon\b",
    r"\bApple\b",
    r"\bNVIDIA\b",
    r"\bAdobe\b",
    r"\bResearch\b",
]

GENERIC_ORG_PATTERNS = [
    r"\b([A-Z][A-Za-z.&'\-]+(?: [A-Z][A-Za-z.&'\-]+){0,5} University)\b",
    r"\b(University of [A-Z][A-Za-z.&'\-]+(?: [A-Z][A-Za-z.&'\-]+){0,5}(?: at [A-Z][A-Za-z.&'\-]+(?: [A-Z][A-Za-z.&'\-]+){0,3})?)\b",
    r"\b([A-Z][A-Za-z.&'\-]+(?: [A-Z][A-Za-z.&'\-]+){0,5} Institute of Technology)\b",
    r"\b([A-Z][A-Za-z.&'\-]+ Polytechnic University)\b",
    r"\b(University College London)\b",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--acm-fellows", type=Path, default=DEFAULT_ACM_FELLOWS, help="Path to data/acm_fellows.csv.")
    parser.add_argument("--google-scholar", type=Path, default=DEFAULT_GOOGLE_SCHOLAR, help="Path to data/google_scholar_profiles.csv.")
    parser.add_argument("--csrankings", type=Path, default=DEFAULT_CSRANKINGS, help="Path to data/csrankings_profiles.csv.")
    parser.add_argument("--min-count", type=int, default=1, help="Minimum count to print.")
    parser.add_argument("--examples", type=int, default=0, help="Number of fellow examples to print per university.")
    parser.add_argument("--show-warnings", action="store_true", help="Print normalization warnings to stderr.")
    parser.add_argument("--warnings-limit", type=int, default=50, help="Maximum normalization warnings to print.")
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    return "".join(char for char in normalized if not unicodedata.combining(char))


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def clean_candidate(value: str) -> str:
    candidate = normalize_space(value.strip(" ,.;()"))
    candidate = re.sub(r"^(?:the|The) ", "", candidate)
    candidate = re.sub(r"^(?:Professor|Prof\.?|Distinguished|Emeritus|Associate|Assistant|Adjunct|Chair|Director|Dept\.?|Department|School|College|Faculty)\s+(?:of\s+)?", "", candidate)
    candidate = candidate.replace("Univ. of", "University of")
    candidate = candidate.replace("Univ of", "University of")
    candidate = candidate.replace("Inst. of", "Institute of")
    return normalize_space(candidate)


def is_non_university(value: str) -> bool:
    return any(re.search(pattern, value, re.IGNORECASE) for pattern in NON_UNIVERSITY_PATTERNS)


def normalize_university(value: str) -> str:
    candidate = clean_candidate(value)
    for pattern, replacement in ALIAS_PATTERNS:
        if re.search(pattern, candidate, re.IGNORECASE):
            return replacement
    return candidate


def valid_university(value: str) -> bool:
    if not value or is_non_university(value):
        return False
    if value in {
        "University",
        "National University",
        "State University",
        "Technical University",
        "University of Technology",
        "University of California",
        "University of Illinois",
        "University of Wisconsin",
        "Chinese University",
    }:
        return False
    if re.search(r"\b(Professor|Chair|Director|Department|School|Faculty|Research|Laboratory|Lab)\b", value, re.IGNORECASE):
        return False
    return bool(re.search(r"\b(University|College|Institute of Technology|EPFL|ETH Zurich|KAIST|Technion)\b", value))


def add_warning(warnings: list[dict[str, str]] | None, context: str, affiliation: str, message: str) -> None:
    if warnings is None:
        return
    warnings.append({"context": context, "affiliation": affiliation, "message": message})


def extract_universities(affiliation: str, warnings: list[dict[str, str]] | None = None, context: str = "") -> set[str]:
    affiliation = normalize_space(strip_accents(affiliation))
    if not affiliation or affiliation == "Unknown affiliation":
        return set()

    found: set[str] = set()
    for pattern, replacement in ALIAS_PATTERNS:
        if re.search(pattern, affiliation, re.IGNORECASE):
            found.add(replacement)

    chunks = re.split(r"[,;]|\s+&\s+|\s*/\s+", affiliation)
    for chunk in chunks:
        chunk = clean_candidate(chunk)
        if not chunk or is_non_university(chunk):
            continue
        for pattern in GENERIC_ORG_PATTERNS:
            for match in re.finditer(pattern, chunk):
                university = normalize_university(match.group(1))
                if university == "Columbia University" and re.search(r"British Columbia", chunk, re.IGNORECASE):
                    add_warning(
                        warnings,
                        context,
                        affiliation,
                        "suppressed Columbia University because the source string refers to University of British Columbia",
                    )
                    continue
                if university in {"University of California", "University of Illinois", "University of Wisconsin", "Chinese University"}:
                    add_warning(
                        warnings,
                        context,
                        affiliation,
                        f"suppressed generic parent institution capture: {university}",
                    )
                if valid_university(university):
                    found.add(university)

    return found


def build_indexes(google_rows: list[dict[str, str]], csrankings_rows: list[dict[str, str]]) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    google_by_profile = {row.get("profile", ""): row for row in google_rows if row.get("profile")}
    csrankings_by_dblp = {row.get("dblp_profile", ""): row for row in csrankings_rows if row.get("dblp_profile")}
    return google_by_profile, csrankings_by_dblp


def main() -> int:
    args = parse_args()
    fellows = read_csv(args.acm_fellows)
    google_by_profile, csrankings_by_dblp = build_indexes(read_csv(args.google_scholar), read_csv(args.csrankings))

    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    warnings: list[dict[str, str]] = []
    fellows_with_university = 0

    for fellow in fellows:
        universities: set[str] = set()
        google = google_by_profile.get(fellow.get("google_scholar_profile", ""))
        if google:
            universities.update(
                extract_universities(
                    google.get("affiliation", ""),
                    warnings if args.show_warnings else None,
                    f"{fellow.get('name', '')} / google_scholar",
                )
            )

        csrankings = csrankings_by_dblp.get(fellow.get("dblp_profile", ""))
        if csrankings:
            universities.update(
                extract_universities(
                    csrankings.get("affiliation", ""),
                    warnings if args.show_warnings else None,
                    f"{fellow.get('name', '')} / csrankings",
                )
            )

        if universities:
            fellows_with_university += 1
        for university in universities:
            counts[university] += 1
            if len(examples[university]) < args.examples:
                examples[university].append(fellow.get("name", ""))

    print(f"fellows={len(fellows)} fellows_with_university={fellows_with_university} universities={len(counts)}")
    print(f"{'count':>5}  university")
    print(f"{'-----':>5}  {'-' * 10}")
    for university, count in counts.most_common():
        if count < args.min_count:
            continue
        suffix = ""
        if args.examples > 0 and examples[university]:
            suffix = "  " + "; ".join(examples[university])
        print(f"{count:5d}  {university}{suffix}")

    if args.show_warnings and warnings:
        print("", file=sys.stderr)
        print("normalization_warnings", file=sys.stderr)
        print("----------------------", file=sys.stderr)
        seen: set[tuple[str, str, str]] = set()
        printed = 0
        for warning in warnings:
            key = (warning["context"], warning["message"], warning["affiliation"])
            if key in seen:
                continue
            seen.add(key)
            if printed >= args.warnings_limit:
                remaining = max(0, len(warnings) - printed)
                print(f"... {remaining} additional warnings omitted; increase --warnings-limit to show more", file=sys.stderr)
                break
            print(f"{warning['context']}: {warning['message']} :: {warning['affiliation']}", file=sys.stderr)
            printed += 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

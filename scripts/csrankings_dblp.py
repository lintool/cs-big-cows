#!/usr/bin/env python3
"""Generate CSRankings' own DBLP links, independently of award-roster URLs.

Compatibility target: emeryberger/CSrankings b2e76bcec658a429c26011530767528839d524df,
src/data-loader.ts, src/config.ts and src/utils.ts (translateNameToDBLP).
The bundled he 1.2.0 named-reference map is in data/; see its adjacent license.
No network requests, redirect resolution or identity corrections are performed.
"""
import argparse
import csv
import json
from pathlib import Path
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
ENTITIES = json.loads((Path(__file__).parent / "data/he-1.2.0-encode.json").read_text())
NAMED = re.compile("|".join(re.escape(s) for s in sorted(ENTITIES, key=len, reverse=True)))
# he leaves HTML's legacy control-code overrides alone, as upstream does.
NUMERIC = re.compile(r"[\x01-\x09\x0b\x0c\x0e-\x1f\x7f\x81\x8d\x8f\x90\x9d\xa0-\U0010ffff]")
JS_SPACE = r"[\t\n\v\f\r \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]"


def csrankings_dblp_url(source_name):
    """Return the URL CSRankings generates; preserve the caller's exact key."""
    name = re.sub(f"^{JS_SPACE}+|{JS_SPACE}+$", "", source_name)
    note = re.search(r"(.*)" + JS_SPACE + r"+\[(.*)\]", name)
    if note:
        name = re.sub(f"^{JS_SPACE}+|{JS_SPACE}+$", "", note[1])
    if not name:
        raise ValueError("Empty CSRankings name")
    name = name.replace(" Jr.", "_Jr.").replace(" II", "_II").replace(" III", "_III")
    name = re.sub(r"['.\-]", "=", name)
    name = name.replace("&gt;\u20d2", "&nvgt;").replace("&lt;\u20d2", "&nvlt;")
    name = NAMED.sub(lambda m: "&" + ENTITIES[m[0]] + ";", name)
    name = NUMERIC.sub(lambda m: f"&#x{ord(m[0]):X};", name)
    name = name.replace("&", "=").replace(";", "=")
    parts = name.split(" ")
    last = parts[-1]
    # Match JS parseInt (including its hex form), rather than stripping every
    # four-digit suffix; the upstream function only treats positive values so.
    parsed = re.match(r"^([+-]?)(?:0[xX]([0-9a-fA-F]+)|([0-9]+))", last)
    number = 0
    if parsed:
        number = int(parsed[2], 16) if parsed[2] else int(parsed[3])
        if parsed[1] == "-":
            number = -number
    if number > 0:
        suffix = parts.pop()
        if not parts:
            raise ValueError(f"CSRankings name has only a disambiguator: {source_name}")
        last = parts[-1] + "_" + suffix
    parts.pop()
    given = re.sub(JS_SPACE, "_", " ".join(parts)).replace("-", "=")
    given = quote(given, safe="~!*'()-._")  # JavaScript encodeURIComponent
    return f"https://dblp.org/pers/hd/{last[0].lower()}/{last}:{given}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", type=Path, default=ROOT / "data/csrankings_profiles.csv")
    parser.add_argument("--write", action="store_true", help="Replace only dblp_profile; default is a read-only check.")
    args = parser.parse_args()
    with args.profiles.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        fields, rows = reader.fieldnames, list(reader)
    if not fields or "name" not in fields or "dblp_profile" not in fields:
        parser.error("Input must contain name and dblp_profile columns")
    if len({row["name"] for row in rows}) != len(rows):
        parser.error("Duplicate CSRankings name keys")
    changes = 0
    for row in rows:
        expected = csrankings_dblp_url(row["name"])
        changes += row["dblp_profile"] != expected
        row["dblp_profile"] = expected
    if args.write:
        with args.profiles.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    print(f"{len(rows)} CSRankings rows; {changes} DBLP links {'updated' if args.write else 'differ'}")
    return 0 if args.write or not changes else 1


if __name__ == "__main__":
    raise SystemExit(main())

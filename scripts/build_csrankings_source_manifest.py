#!/usr/bin/env python3
"""Verify original CSRankings fields against retained inputs and write a manifest.

Reads existing local files only. Never fetches sources or edits the profile table.
The manifest must be updated deliberately after an authorized source change.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import string

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FIELDS = ["name", "affiliation", "homepage", "scholarid", "orcid"]


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def source_digest(row):
    values = [row.get(field, "") for field in SOURCE_FIELDS]
    return hashlib.sha256(json.dumps(values, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def build_manifest(profiles, cache_dir, historical_source=None):
    if historical_source and historical_source.resolve() == profiles.resolve():
        raise ValueError("Historical evidence must be an independent retained snapshot, not the current table")
    sources, candidates = {}, {}
    for letter in string.ascii_lowercase:
        path = cache_dir / f"csrankings-{letter}.csv"
        sources[path.name] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for row in read_csv(path):
            candidates.setdefault(row["name"], []).append((path.name, row))
    historical = {}
    if historical_source:
        for row in read_csv(historical_source):
            name = row["name"]
            if name in historical and source_digest(historical[name]) != source_digest(row):
                raise ValueError(f"Conflicting historical source rows: {name}")
            historical[name] = row
        sources["historical"] = {"snapshot": historical_source.name,
                                 "sha256": hashlib.sha256(historical_source.read_bytes()).hexdigest()}
    result = {}
    for row in read_csv(profiles):
        name = row["name"]
        if name in result:
            raise ValueError(f"Duplicate profile key: {name}")
        if len({source_digest(candidate) for _, candidate in candidates.get(name, [])}) > 1:
            raise ValueError(f"Conflicting upstream source rows: {name}")
        digest = source_digest(row)
        matching = [source for source, candidate in candidates.get(name, []) if source_digest(candidate) == digest]
        if matching:
            source = matching[0]
        elif name not in candidates and name in historical and source_digest(historical[name]) == digest:
            source = "historical"
        else:
            raise ValueError(f"Original source fields do not match the supplied evidence: {name}")
        result[name] = {"source": source, "sha256": digest}
    return {"schema_version": 1, "fields": SOURCE_FIELDS, "sources": sources, "profiles": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", type=Path, default=ROOT / "data/csrankings_profiles.csv")
    parser.add_argument("--cache-dir", type=Path, default=ROOT.parent / "bigcows-crawler/.cache/csrankings")
    parser.add_argument("--historical-source", type=Path, help="Independent retained table for documented historical keys")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = build_manifest(args.profiles, args.cache_dir, args.historical_source)
    protected = [args.profiles, *args.cache_dir.glob("csrankings-?.csv")]
    if args.historical_source:
        protected.append(args.historical_source)
    if args.output.resolve() in {path.resolve() for path in protected}:
        parser.error("Manifest output cannot overwrite input evidence")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Verified {len(manifest['profiles'])} source rows; manifest written to {args.output}")


if __name__ == "__main__":
    main()

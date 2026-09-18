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


def read_csv(path, fields=None, exact=False):
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        header = reader.fieldnames
        if not header or len(header) != len(set(header)):
            raise ValueError(f"Invalid CSV header: {path}")
        if fields and (header != fields if exact else not set(fields).issubset(header)):
            raise ValueError(f"Invalid source schema in {path}: expected {'exactly ' if exact else 'at least '}{fields}, got {header}")
        rows = list(reader)
        for number, row in enumerate(rows, 2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"Malformed CSV row in {path}:{number}")
        return rows


def source_digest(row):
    if any(field not in row or not isinstance(row[field], str) for field in SOURCE_FIELDS):
        raise ValueError("Source row must contain all five original fields as strings")
    values = [row[field] for field in SOURCE_FIELDS]
    return hashlib.sha256(json.dumps(values, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def build_manifest(profiles, cache_dir, historical_source=None, legacy_source=None, legacy_names=()):
    if historical_source and historical_source.resolve() == profiles.resolve():
        raise ValueError("Historical evidence must be an independent retained snapshot, not the current table")
    if bool(legacy_source) != bool(legacy_names):
        raise ValueError("Legacy evidence requires both a source and explicitly reviewed names")
    if legacy_source and legacy_source.resolve() == profiles.resolve():
        raise ValueError("Legacy evidence must be an independent upstream snapshot")
    sources, candidates = {}, {}
    for letter in string.ascii_lowercase:
        path = cache_dir / f"csrankings-{letter}.csv"
        sources[path.name] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for row in read_csv(path, SOURCE_FIELDS, exact=True):
            candidates.setdefault(row["name"], []).append((path.name, row))
    historical = {}
    if historical_source:
        for row in read_csv(historical_source, SOURCE_FIELDS):
            name = row["name"]
            if name in historical and source_digest(historical[name]) != source_digest(row):
                raise ValueError(f"Conflicting historical source rows: {name}")
            historical[name] = row
        sources["historical"] = {"snapshot": historical_source.name,
                                 "sha256": hashlib.sha256(historical_source.read_bytes()).hexdigest()}
    legacy = {}
    if legacy_source:
        selected = set(legacy_names)
        for row in read_csv(legacy_source, SOURCE_FIELDS[:-1], exact=True):
            if row['name'] not in selected:
                continue
            # The historical schema did not contain ORCID. A blank is an
            # explicit representation of absence, never an inferred ID.
            row = dict(row, orcid="")
            if row['name'] in legacy and source_digest(legacy[row['name']]) != source_digest(row):
                raise ValueError(f"Conflicting legacy source rows: {row['name']}")
            legacy[row['name']] = row
        missing = selected - set(legacy)
        if missing:
            raise ValueError(f"Reviewed names missing from legacy source: {sorted(missing)}")
        sources['legacy'] = {'snapshot': legacy_source.name,
                             'sha256': hashlib.sha256(legacy_source.read_bytes()).hexdigest(),
                             'fields': SOURCE_FIELDS[:-1],
                             'absent_fields': {'orcid': ''},
                             'reviewed_names': sorted(selected)}
    result = {}
    for row in read_csv(profiles, SOURCE_FIELDS):
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
        elif name not in candidates and name not in historical and name in legacy and source_digest(legacy[name]) == digest:
            source = "legacy"
        else:
            raise ValueError(f"Original source fields do not match the supplied evidence: {name}")
        result[name] = {"source": source, "sha256": digest}
    return {"schema_version": 1, "fields": SOURCE_FIELDS, "sources": sources, "profiles": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", type=Path, default=ROOT / "data/csrankings_profiles.csv")
    parser.add_argument("--cache-dir", type=Path, default=ROOT.parent / "bigcows-crawler/.cache/csrankings")
    parser.add_argument("--historical-source", type=Path, help="Independent retained table for documented historical keys")
    parser.add_argument("--legacy-source", type=Path, help="Independent upstream snapshot with the original four-column schema")
    parser.add_argument("--legacy-name", action="append", default=[], help="Explicitly reviewed name to accept from --legacy-source; repeat for each name")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = build_manifest(args.profiles, args.cache_dir, args.historical_source, args.legacy_source, args.legacy_name)
    protected = [args.profiles, *args.cache_dir.glob("csrankings-?.csv")]
    if args.historical_source:
        protected.append(args.historical_source)
    if args.legacy_source:
        protected.append(args.legacy_source)
    if args.output.resolve() in {path.resolve() for path in protected}:
        parser.error("Manifest output cannot overwrite input evidence")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Verified {len(manifest['profiles'])} source rows; manifest written to {args.output}")


if __name__ == "__main__":
    main()

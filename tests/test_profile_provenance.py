"""Guard source-field preservation and the explicit capture/import backlog."""
import csv
import importlib.util
import json
from pathlib import Path
import string
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


provenance = load("build_csrankings_source_manifest")
queue_builder = load("build_profile_capture_queue")


class ProfileProvenanceTests(unittest.TestCase):
    def test_canonical_source_fields_match_verified_manifest(self):
        manifest = json.loads((ROOT / "docs/csrankings_source_fields.json").read_text())
        self.assertEqual(manifest["fields"], provenance.SOURCE_FIELDS)
        rows = provenance.read_csv(ROOT / "data/csrankings_profiles.csv")
        self.assertEqual(set(manifest["profiles"]), {row["name"] for row in rows})
        for row in rows:
            with self.subTest(name=row["name"]):
                expected = manifest["profiles"][row["name"]]
                self.assertIn(expected["source"], manifest["sources"])
                self.assertEqual(provenance.source_digest(row), expected["sha256"])

    def test_manifest_generation_rejects_repaired_upstream_fields(self):
        def write(path, rows):
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=provenance.SOURCE_FIELDS)
                writer.writeheader()
                writer.writerows(rows)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = dict(name="Alice", affiliation="A", homepage="https://example.org", scholarid="upstream-id", orcid="")
            historical = dict(original, name="Historical Person", affiliation="Old institution")
            for letter in string.ascii_lowercase:
                write(root / f"csrankings-{letter}.csv", [original] if letter == "a" else [])
            profiles, retained = root / "profiles.csv", root / "retained.csv"
            write(profiles, [original, historical])
            write(retained, [historical])
            manifest = provenance.build_manifest(profiles, root, retained)
            self.assertEqual(manifest["profiles"]["Historical Person"]["source"], "historical")
            write(profiles, [dict(original, scholarid="locally-corrected-id"), historical])
            with self.assertRaisesRegex(ValueError, "source fields do not match.*Alice"):
                provenance.build_manifest(profiles, root, retained)
            write(profiles, [original, historical])
            write(root / "csrankings-a.csv", [original, dict(original, affiliation="Conflicting university")])
            with self.assertRaisesRegex(ValueError, "Conflicting upstream source rows: Alice"):
                provenance.build_manifest(profiles, root, retained)
            write(root / "csrankings-a.csv", [original, original])
            self.assertEqual(len(provenance.build_manifest(profiles, root, retained)["profiles"]), 2)
            write(retained, [historical, dict(historical, scholarid="conflicting-id")])
            with self.assertRaisesRegex(ValueError, "Conflicting historical source rows"):
                provenance.build_manifest(profiles, root, retained)

    def test_queue_groups_dblp_url_variants_and_preserves_each_stored_url(self):
        def recipient(url):
            return {"name": "Same Person", "year": "2025", "acm_fellow_profile": "", "acm_fellow_profile_crawl_date": "",
                    "dblp_profile": url, "dblp_profile_crawl_date": "", "google_scholar_profile": "", "google_scholar_profile_crawl_date": ""}
        variants = ["https://dblp.org/pid/57/2381-1", "http://dblp.org/pid/57/2381-1.html?view=by-type#ref"]
        tasks = queue_builder.build_queue({"fellows": [recipient(variants[0])], "turing": [recipient(variants[1])]}, [])
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["url"], variants[0])
        self.assertEqual([row["stored_url"] for row in tasks[0]["recipients"]], variants)
        distinct = queue_builder.build_queue({"fellows": [recipient(variants[0]), recipient("https://dblp.org/pid/57/2381-2")]}, [])
        self.assertEqual(len(distinct), 2)

    def test_manifest_rejects_malformed_shards_even_when_values_would_be_blank(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            header = ",".join(provenance.SOURCE_FIELDS) + "\n"
            for letter in string.ascii_lowercase:
                (root / f"csrankings-{letter}.csv").write_text(header)
            canonical = root / "profiles.csv"
            canonical.write_text(header + "Alice,,,,\n")
            shard = root / "csrankings-a.csv"
            shard.write_text(header + "Alice,,,,\n")
            self.assertEqual(len(provenance.build_manifest(canonical, root)["profiles"]), 1)
            invalid = [
                "name,affiliation,homepage,scholarid\nAlice,,,\n",  # missing blank ORCID
                "name,affiliation,homepage,scholarid,renamed\nAlice,,,,\n",
                "name,affiliation,homepage,scholarid,orcid,orcid\nAlice,,,,,\n",
                "name,homepage,affiliation,scholarid,orcid\nAlice,,,,\n",
                header + "Alice,,,\n",  # truncated row
                header + "Alice,,,,,extra\n",
                "name,affiliation,homepage,scholarid\n",  # empty malformed shard
            ]
            for contents in invalid:
                with self.subTest(contents=contents):
                    shard.write_text(contents)
                    with self.assertRaises(ValueError):
                        provenance.build_manifest(canonical, root)

    def test_manifest_requires_original_fields_in_historical_and_canonical_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            header = ",".join(provenance.SOURCE_FIELDS) + "\n"
            for letter in string.ascii_lowercase:
                (root / f"csrankings-{letter}.csv").write_text(header)
            canonical, historical = root / "profiles.csv", root / "historical.csv"
            valid = header.rstrip("\n") + ",dblp_profile\nAlice,,,,,old-link\n"
            invalid = "name,affiliation,homepage,scholarid\nAlice,,,\n"
            for bad_path in [canonical, historical]:
                canonical.write_text(valid)
                historical.write_text(valid)
                bad_path.write_text(invalid)
                with self.subTest(path=bad_path), self.assertRaisesRegex(ValueError, "Invalid source schema"):
                    provenance.build_manifest(canonical, root, historical)
            canonical.write_text(valid)
            historical.write_text(valid)
            self.assertEqual(provenance.build_manifest(canonical, root, historical)["profiles"]["Alice"]["source"], "historical")

    def test_digest_distinguishes_missing_fields_from_explicit_blanks(self):
        valid = dict(name="Alice", affiliation="", homepage="", scholarid="", orcid="")
        self.assertTrue(provenance.source_digest(valid))
        for field in provenance.SOURCE_FIELDS:
            missing = dict(valid)
            del missing[field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                provenance.source_digest(missing)

    def test_explicit_legacy_schema_preserves_fields_and_marks_absent_orcid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            header = ','.join(provenance.SOURCE_FIELDS) + '\n'
            for letter in string.ascii_lowercase:
                (root / f'csrankings-{letter}.csv').write_text(header)
            canonical, legacy = root / 'profiles.csv', root / 'old.csv'
            original = 'Alice,Old University,http://example.org,NOSCHOLARPAGE'
            canonical.write_text(header + original + ',\n')
            legacy.write_text(','.join(provenance.SOURCE_FIELDS[:-1]) + '\n' + original + '\n')
            manifest = provenance.build_manifest(canonical, root, legacy_source=legacy, legacy_names=['Alice'])
            self.assertEqual(manifest['profiles']['Alice']['source'], 'legacy')
            self.assertEqual(manifest['sources']['legacy']['absent_fields'], {'orcid': ''})
            for values in [original.replace('NOSCHOLARPAGE', 'repaired-id') + ',', original + ',invented-orcid']:
                canonical.write_text(header + values + '\n')
                with self.assertRaisesRegex(ValueError, 'source fields do not match'):
                    provenance.build_manifest(canonical, root, legacy_source=legacy, legacy_names=['Alice'])
            canonical.write_text(header + original + ',\n')
            with self.assertRaisesRegex(ValueError, 'both a source'):
                provenance.build_manifest(canonical, root, legacy_source=legacy)
            with self.assertRaisesRegex(ValueError, 'missing from legacy source'):
                provenance.build_manifest(canonical, root, legacy_source=legacy, legacy_names=['Absent'])
            # Legacy evidence cannot override the current source or silently
            # accept a truncated/malformed modern shard.
            (root / 'csrankings-a.csv').write_text(header + original.replace('Old University', 'New University') + ',\n')
            with self.assertRaisesRegex(ValueError, 'source fields do not match'):
                provenance.build_manifest(canonical, root, legacy_source=legacy, legacy_names=['Alice'])
            (root / 'csrankings-a.csv').write_text(header)
            for malformed in [header + original + ',\n', 'name,affiliation,homepage,scholarid\nAlice,,,\nAlice,X,,\n', 'name,affiliation,homepage,scholarid\nAlice,,\n']:
                legacy.write_text(malformed)
                with self.assertRaises(ValueError):
                    provenance.build_manifest(canonical, root, legacy_source=legacy, legacy_names=['Alice'])

    def test_capture_queue_matches_current_rosters_and_metrics(self):
        rosters = {name: provenance.read_csv(ROOT / "data" / name)
                   for name in ["acm_fellows.csv", "turing_award_winners.csv"]}
        metrics = provenance.read_csv(ROOT / "data/google_scholar_profiles.csv")
        saved = json.loads((ROOT / "docs/profile_capture_queue.json").read_text())
        self.assertEqual(saved["schema_version"], 2)
        self.assertEqual(saved["tasks"], queue_builder.build_queue(rosters, metrics))

    def test_queue_deduplicates_shared_links_and_distinguishes_import_gaps(self):
        def recipient(name, url, captured=""):
            return {"name": name, "year": "2025", "acm_fellow_profile": "", "acm_fellow_profile_crawl_date": "",
                    "dblp_profile": "", "dblp_profile_crawl_date": "", "google_scholar_profile": url,
                    "google_scholar_profile_crawl_date": captured}
        rows = [recipient("Shared", "profile-a"), recipient("Missing", ""),
                recipient("Captured", "profile-b", "2026-09-16"), recipient("Imported", "profile-c", "2026-09-16")]
        tasks = queue_builder.build_queue({"fellows": rows, "turing": [rows[0]]}, [{"profile": "profile-c"}])
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["reasons"], ["missing_metrics_import", "no_accepted_capture"])
        self.assertEqual(len(tasks[0]["recipients"]), 2)
        self.assertEqual(tasks[1]["reasons"], ["missing_metrics_import"])
        self.assertEqual(tasks[0]["status"], "awaiting_refresh_approval")


if __name__ == "__main__":
    unittest.main()

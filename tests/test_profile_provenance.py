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

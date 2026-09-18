"""Check award-roster inputs, shared DBLP identities and crawl-date semantics."""
import csv
import contextlib
import io
from datetime import date
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("csrankings_builder", ROOT / "scripts/build_csrankings_profiles.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class RosterAlignmentTests(unittest.TestCase):
    def test_canonical_ordering(self):
        for filename in ["acm_fellows.csv", "turing_award_winners.csv"]:
            rows = builder.read_csv(ROOT / "data" / filename)
            self.assertEqual(rows, sorted(rows, key=lambda row: (-int(row["year"]), row["name"].lower())), filename)
        profiles = builder.read_csv(builder.CANONICAL_OUTPUT)
        self.assertEqual(profiles, sorted(profiles, key=lambda row: (row["name"].lower(), row["name"])))

    def test_initials_are_not_degree_suffixes(self):
        self.assertFalse(builder.compatible_name("Smith, John D.", "John Smith"))
        self.assertTrue(builder.compatible_name("Smith, D.", "David Smith"))
        self.assertFalse(builder.compatible_name("Smith, D.", "Alice Smith"))
        for name in ["John D. Smith, Ph.D.", "Smith, John D., Ph.D.", "Dr. John D. Smith PhD"]:
            with self.subTest(name=name):
                exact, by_last = builder.build_csrankings_index([{"name": "John D Smith"}, {"name": "John Smith"}])
                self.assertEqual(builder.csrankings_candidates_for_name(name, exact, by_last), [{"name": "John D Smith"}])

    def test_directory_name_order_preserves_identity_matching(self):
        for directory, given_first in [
            ("Orso, Alessandro", "Alessandro Orso"),
            ("De Micheli, Giovanni", "Giovanni De Micheli"),
            ("Smith, John A.", "John A Smith"),
            ("John Smith, Jr.", "John Smith"),
        ]:
            with self.subTest(directory=directory):
                exact, by_last = builder.build_csrankings_index([{"name": given_first}])
                self.assertEqual(builder.csrankings_candidates_for_name(directory, exact, by_last), [{"name": given_first}])
        self.assertFalse(builder.compatible_name("Smith, Alice", "Bob Smith"))

    def test_defaults_use_both_rosters_and_shared_cache(self):
        with patch.object(sys, "argv", ["builder"]):
            args = builder.parse_args()
        self.assertEqual(args.fellows, ROOT / "data/acm_fellows.csv")
        self.assertEqual(args.turing, ROOT / "data/turing_award_winners.csv")
        self.assertEqual(args.report.parent, ROOT.parent / "bigcows-crawler/.cache")
        self.assertEqual(args.output, ROOT.parent / "bigcows-crawler/.cache/csrankings-legacy-profiles.csv")

    def test_cli_rejects_canonical_output_before_reading_or_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            canonical = Path(directory) / "canonical.csv"
            canonical.write_text("preserved table\n")
            alias = Path(directory) / "alias.csv"
            alias.symlink_to(canonical)
            for option in ("--output", "--report"):
                for target in (canonical, alias):
                    with self.subTest(option=option, target=target):
                        with patch.object(builder, "CANONICAL_OUTPUT", canonical), patch.object(
                            sys, "argv", ["builder", option, str(target)]
                        ), patch.object(builder, "read_csrankings_rows") as read, contextlib.redirect_stderr(io.StringIO()):
                            with self.assertRaises(SystemExit) as error:
                                builder.main()
                            self.assertEqual(error.exception.code, 2)
                            read.assert_not_called()
                        self.assertEqual(canonical.read_text(), "preserved table\n")

    def test_canonical_profile_keys_and_reviewed_identity_exclusions(self):
        rosters = builder.read_csv(ROOT / "data/acm_fellows.csv") + builder.read_csv(ROOT / "data/turing_award_winners.csv")
        profiles = builder.read_csv(builder.CANONICAL_OUTPUT)
        self.assertEqual(list(profiles[0]), builder.OUTPUT_COLUMNS)
        self.assertNotIn("crawl_date", profiles[0])
        expected = {r["csrankings_name"] for r in rosters if r["csrankings_name"]}
        actual = [r["name"] for r in profiles]
        self.assertEqual(set(actual), expected)
        self.assertEqual(len(actual), len(set(actual)))
        rejected_names = {"Hui Zhang 0005", "B. Chandrasekaran 0002"}
        self.assertFalse(expected & rejected_names)
        review = builder.read_csv(ROOT / "docs/dblp_profile_quality_2026-09-17.csv")
        rejected_urls = {r["dblp_profile"] for r in review if r["category"] == "identity_mismatch" and r["dblp_profile"]}
        for row in profiles:
            self.assertNotIn(row["dblp_profile"], rejected_urls, row["name"])

    def test_url_deduplication_preserves_distinct_people_with_same_name(self):
        rows = builder.unique_dblp_rows([
            {"name": "Alice First", "dblp_profile": "https://dblp.org/pid/1/2"},
            {"name": "A. First", "dblp_profile": "http://dblp.org/pid/1/2.html?view=by-type#ref"},
            {"name": "Alice First", "dblp_profile": "https://dblp.org/pid/1/3"},
            {"name": "Missing", "dblp_profile": ""},
        ])
        self.assertEqual(rows, [
            {"name": "Alice First", "profile": "https://dblp.org/pid/1/2"},
            {"name": "Alice First", "profile": "https://dblp.org/pid/1/3"},
        ])

    def test_cli_includes_turing_only_people_without_legacy_crawl_date(self):
        def write(path, fields, rows):
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)

        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            fellows, turing = tmp / "fellows.csv", tmp / "turing.csv"
            fields = ["name", "dblp_profile", "dblp_profile_crawl_date"]
            alice = {"name": "Alice Example", "dblp_profile": "https://dblp.org/pid/1/1", "dblp_profile_crawl_date": "2026-09-17"}
            bob = {"name": "Bob Example", "dblp_profile": "https://dblp.org/pid/1/2", "dblp_profile_crawl_date": "2026-09-18"}
            write(fellows, fields, [alice, {"name": "No Profile", "dblp_profile": "", "dblp_profile_crawl_date": ""}])
            write(turing, fields, [alice, bob,
                {"name": "Unmatched Person", "dblp_profile": "https://dblp.org/pid/1/3", "dblp_profile_crawl_date": ""},
                {"name": "Ambiguous Person", "dblp_profile": "https://dblp.org/pid/1/4", "dblp_profile_crawl_date": ""},
            ])
            write(tmp / "csrankings-a.csv", builder.CSRANKINGS_COLUMNS, [
                {"name": "Alice Example", "affiliation": "A"},
                {"name": "Bob Example", "affiliation": "B"},
                {"name": "Ambiguous Person", "affiliation": "C"},
                {"name": "Ambiguous Person", "affiliation": "D"},
            ])
            output, report = tmp / "output.csv", tmp / "report.json"
            with patch.object(sys, "argv", ["builder", "--fellows", str(fellows), "--turing", str(turing),
                    "--cache-dir", str(tmp), "--output", str(output), "--report", str(report)]):
                self.assertEqual(builder.main(), 0)
            result = builder.read_csv(output)
            self.assertEqual([r["name"] for r in result], ["Alice Example", "Bob Example"])
            self.assertEqual(list(result[0]), builder.OUTPUT_COLUMNS)
            self.assertNotIn("crawl_date", result[0])
            counts = json.loads(report.read_text())
            self.assertNotIn("crawl_date", counts)
            self.assertIn("generated_at", counts)
            self.assertEqual((counts["dblp_profiles_rows"], counts["included_rows"], counts["unmatched_dblp_profiles"], counts["ambiguous_dblp_profiles"]), (4, 2, 1, 1))
            self.assertEqual((counts["fellows"], counts["turing"]), (str(fellows), str(turing)))

    def test_canonical_roster_dates_are_valid_and_shared_profiles_agree(self):
        dates = {}
        qualities = {}
        for filename in ["acm_fellows.csv", "turing_award_winners.csv"]:
            for row in builder.read_csv(ROOT / "data" / filename):
                for field in ["acm_fellow_profile", "dblp_profile", "google_scholar_profile"]:
                    date_field = field + "_crawl_date"
                    fields = list(row)
                    self.assertEqual(fields[fields.index(field) + 1], date_field)
                    captured = row[date_field]
                    if field in ["dblp_profile", "google_scholar_profile"]:
                        quality_field = field + "_quality"
                        self.assertEqual(fields[fields.index(date_field) + 1], quality_field)
                        self.assertIn(row[quality_field], {"Y", "N"})
                        if not row[field]:
                            self.assertEqual(row[quality_field], "N")
                    if not row[field]:
                        self.assertEqual(captured, "", (row["name"], field))
                        continue
                    # A reviewed URL can lack an accepted crawler capture.
                    if captured:
                        self.assertEqual(date.fromisoformat(captured).isoformat(), captured)
                    profile = builder.unique_dblp_rows([row])[0]["profile"] if field == "dblp_profile" else row[field]
                    key = (field, profile)
                    self.assertEqual(dates.setdefault(key, captured), captured, key)
                    if field in ["dblp_profile", "google_scholar_profile"]:
                        quality = row[field + "_quality"]
                        self.assertEqual(qualities.setdefault(key, quality), quality, key)


if __name__ == "__main__":
    unittest.main()

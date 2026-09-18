"""Check award selection and the published snapshots against canonical inputs."""

import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder", ROOT / "scripts/build_scholar_citation_visualization.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class CitationDataTests(unittest.TestCase):
    def test_rebuild_hint_selects_the_generated_award(self):
        for award in ("fellows", "turing"):
            with self.subTest(award=award):
                script = builder.render_data_script({"metadata": {"award": award}, "rows": []})
                self.assertIn(f"python scripts/build_scholar_citation_visualization.py --award {award}", script)

    def test_award_specific_defaults(self):
        for award, roster, output in (
            ("fellows", builder.DEFAULT_ACM, builder.DEFAULT_OUTPUT),
            ("turing", builder.DEFAULT_TURING, builder.DEFAULT_TURING_OUTPUT),
        ):
            with self.subTest(award=award), patch.object(sys, "argv", ["builder", "--award", award]):
                args = builder.parse_args()
                self.assertEqual((args.roster, args.output), (roster, output))

    def test_legacy_and_custom_paths(self):
        for flag in ("--acm", "--roster"):
            with self.subTest(flag=flag), patch.object(sys, "argv", ["builder", flag, "custom.csv", "--output", "custom.js"]):
                args = builder.parse_args()
                self.assertEqual((args.award, args.roster, args.output), ("fellows", Path("custom.csv"), Path("custom.js")))

    def test_canonical_joins_and_current_metrics(self):
        metrics = builder.read_csv(builder.DEFAULT_SCHOLAR)
        by_profile = {r["profile"]: r for r in metrics}
        for award, roster, output in (
            ("fellows", builder.DEFAULT_ACM, builder.DEFAULT_OUTPUT),
            ("turing", builder.DEFAULT_TURING, builder.DEFAULT_TURING_OUTPUT),
        ):
            with self.subTest(award=award):
                source = builder.read_csv(roster)
                for recipient in source:
                    metric = by_profile.get(recipient["google_scholar_profile"])
                    if metric:
                        self.assertEqual(recipient["google_scholar_profile_crawl_date"], metric["crawl_date"], recipient["name"])
                expected = builder.build_data(source, metrics, award)
                self.assertEqual(len(expected["rows"]), len(source))
                self.assertEqual({r["name"] for r in expected["rows"]}, {r["name"] for r in source})
                self.assertEqual(expected["metadata"]["award"], award)
                self.assertEqual(expected["metadata"]["totalRows"], len(source))
                histories = sum(bool(r["citationByYear"]) for r in expected["rows"])
                self.assertEqual(expected["metadata"]["joinedRows"], histories)
                self.assertEqual(expected["metadata"]["missingRows"], len(source) - histories)
                for row in expected["rows"]:
                    if row["scholarProfile"] not in by_profile:
                        recipient = next(r for r in source if r["name"] == row["name"])
                        self.assertFalse(recipient["google_scholar_profile_crawl_date"])
                        self.assertFalse(row["hasScholar"])
                        self.assertIsNone(row["citations"])
                        self.assertIsNone(row["crawlDate"])
                        self.assertEqual(row["citationByYear"], {})
                    else:
                        metric = by_profile[row["scholarProfile"]]
                        self.assertEqual(row["citations"], int(metric["citations"]))
                        self.assertEqual(row["crawlDate"], metric["crawl_date"])
                        self.assertEqual(row["citationByYear"], json.loads(metric["citation_by_year"]))
                        self.assertEqual(row["hasScholar"], bool(row["citationByYear"]))


class SnapshotTests(unittest.TestCase):
    def test_snapshots_match_each_roster_and_current_metrics(self):
        metrics = builder.read_csv(builder.DEFAULT_SCHOLAR)
        for award, roster, output in (
            ("fellows", builder.DEFAULT_ACM, builder.DEFAULT_OUTPUT),
            ("turing", builder.DEFAULT_TURING, builder.DEFAULT_TURING_OUTPUT),
        ):
            with self.subTest(award=award):
                saved = json.loads(output.read_text().split("window.SCHOLAR_DATA = ", 1)[1].rstrip(";\n"))
                expected = builder.build_data(builder.read_csv(roster), metrics, award)
                self.assertEqual(saved["metadata"], expected["metadata"])
                self.assertEqual(saved["rows"], expected["rows"])


if __name__ == "__main__":
    unittest.main()

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

    def test_snapshots_match_each_roster_and_current_metrics(self):
        metrics = builder.read_csv(builder.DEFAULT_SCHOLAR)
        by_profile = {r["profile"]: r for r in metrics}
        for award, roster, output in (
            ("fellows", builder.DEFAULT_ACM, builder.DEFAULT_OUTPUT),
            ("turing", builder.DEFAULT_TURING, builder.DEFAULT_TURING_OUTPUT),
        ):
            with self.subTest(award=award):
                source = builder.read_csv(roster)
                saved = json.loads(output.read_text().split("window.SCHOLAR_DATA = ", 1)[1].rstrip(";\n"))
                expected = builder.build_data(source, metrics, award)
                self.assertEqual(saved["metadata"], expected["metadata"])
                self.assertEqual(saved["rows"], expected["rows"])
                self.assertEqual({r["name"] for r in saved["rows"]}, {r["name"] for r in source})
                for row in saved["rows"]:
                    if not row["scholarProfile"]:
                        self.assertFalse(row["hasScholar"])
                        self.assertIsNone(row["citations"])
                        self.assertIsNone(row["crawlDate"])
                        self.assertEqual(row["citationByYear"], {})
                    else:
                        metric = by_profile[row["scholarProfile"]]
                        self.assertEqual(row["citations"], int(metric["citations"]))
                        self.assertEqual(row["crawlDate"], metric["crawl_date"])


if __name__ == "__main__":
    unittest.main()

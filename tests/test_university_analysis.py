"""Exercise explicit CSRankings joins without using publication-profile IDs."""
import contextlib
import importlib.util
import io
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("university_analysis", ROOT / "scripts/analyze_acm_fellow_universities.py")
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


class UniversityAnalysisTests(unittest.TestCase):
    def run_analysis(self, fellows, scholar, csrankings):
        args = SimpleNamespace(acm_fellows="fellows", google_scholar="scholar", csrankings="csrankings",
                               min_count=1, examples=10, show_warnings=False)
        inputs = {"fellows": fellows, "scholar": scholar, "csrankings": csrankings}
        output = io.StringIO()
        with patch.object(analysis, "parse_args", return_value=args), patch.object(
            analysis, "read_csv", side_effect=inputs.__getitem__
        ), contextlib.redirect_stdout(output):
            self.assertEqual(analysis.main(), 0)
        return output.getvalue()

    def test_explicit_keys_override_dblp_and_do_not_infer_missing_links(self):
        output = self.run_analysis(
            [
                {"name": "Alice", "csrankings_name": "Alice 0001", "dblp_profile": "wrong-url", "google_scholar_profile": "scholar-a"},
                {"name": "Bob", "csrankings_name": "", "dblp_profile": "shared-url"},
                {"name": "Carol", "csrankings_name": "Carol", "dblp_profile": ""},
                {"name": "Dan", "csrankings_name": "Unresolved", "dblp_profile": "shared-url"},
            ],
            [{"profile": "scholar-a", "affiliation": "Princeton University"}],
            [
                {"name": "Alice 0001", "dblp_profile": "shared-url", "affiliation": "Princeton University"},
                {"name": "Carol", "dblp_profile": "shared-url", "affiliation": "Massachusetts Institute of Technology"},
            ],
        )
        self.assertIn("fellows=4 fellows_with_university=2 universities=2", output)
        self.assertIn("    1  Princeton University  Alice", output)
        self.assertIn("    1  Massachusetts Institute of Technology  Carol", output)
        self.assertNotIn("Bob", output)
        self.assertNotIn("Dan", output)

    def test_kai_li_affiliation_is_available_without_a_table_dblp_link(self):
        fellows = analysis.read_csv(ROOT / "data/acm_fellows.csv")
        csrankings = analysis.read_csv(ROOT / "data/csrankings_profiles.csv")
        kai = next(row for row in fellows if row["csrankings_name"] == "Kai Li 0001")
        output = self.run_analysis([kai], [], csrankings)
        self.assertIn("    1  Princeton University  Li, Kai", output)

    def test_duplicate_source_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate CSRankings name key: Alice"):
            analysis.build_indexes([], [{"name": "Alice"}, {"name": "Alice"}])

    def test_historical_uc_affiliations_retain_the_campus(self):
        for campus in ['Berkeley', 'Los Angeles', 'San Diego', 'Santa Barbara', 'Irvine', 'Santa Cruz', 'Davis', 'Riverside']:
            for prefix in ['University', 'Univ.', 'Univ']:
                with self.subTest(campus=campus, prefix=prefix):
                    self.assertEqual(analysis.extract_universities(f'{prefix} of California - {campus}'),
                                     {f'University of California, {campus}'})
        self.assertEqual(analysis.extract_universities('University of California'), set())

    def test_historical_csrankings_affiliation_counts_without_scholar(self):
        output = self.run_analysis(
            [{'name': 'Bhuyan, Laxmi Narayan', 'csrankings_name': 'Laxmi N. Bhuyan', 'google_scholar_profile': ''}],
            [],
            [{'name': 'Laxmi N. Bhuyan', 'affiliation': 'University of California - Riverside'}],
        )
        self.assertIn('fellows=1 fellows_with_university=1 universities=1', output)
        self.assertIn('    1  University of California, Riverside  Bhuyan, Laxmi Narayan', output)

    def test_equal_counts_have_deterministic_alphabetical_order(self):
        fellows = [{'name': 'Z', 'csrankings_name': 'Z'}, {'name': 'A', 'csrankings_name': 'A'}]
        sources = [{'name': 'Z', 'affiliation': 'Princeton University'},
                   {'name': 'A', 'affiliation': 'Cornell University'}]
        output = self.run_analysis(fellows, [], sources)
        self.assertEqual(output, self.run_analysis(list(reversed(fellows)), [], sources))
        self.assertLess(output.index('Cornell University'), output.index('Princeton University'))


if __name__ == "__main__":
    unittest.main()

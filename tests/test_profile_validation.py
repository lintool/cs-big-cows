"""Cross-table association checks, including negative regression cases."""
import csv
from pathlib import Path
import unittest

from scripts.profile_validation import (
    validate_alignment_dates, validate_shared_recipients, validate_derived_dblp_links,
)

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def recipient(**changes):
    row = dict(name="Person, Alice", acm_fellow_profile="https://awards.acm.org/award-recipients/person_a123",
               dblp_profile="https://dblp.org/pid/1/2", dblp_profile_crawl_date="2026-09-17", dblp_profile_quality="Y",
               google_scholar_profile="https://scholar.google.com/citations?user=abc", google_scholar_profile_crawl_date="2026-09-16",
               google_scholar_profile_quality="Y", csrankings_name="Alice Person", csrankings_name_alignment_date="2026-09-18")
    row.update(changes)
    return row


class ProfileValidationTests(unittest.TestCase):
    def test_canonical_cross_table_associations(self):
        rosters = {name: read(ROOT / "data" / name) for name in ["acm_fellows.csv", "turing_award_winners.csv"]}
        for rows in rosters.values():
            validate_alignment_dates(rows)
        self.assertGreater(validate_shared_recipients(rosters), 0)
        rejected = [row["dblp_profile"] for row in read(ROOT / "docs/dblp_profile_quality_2026-09-17.csv")
                    if row["category"] == "identity_mismatch"]
        validate_derived_dblp_links(rosters, read(ROOT / "data/csrankings_profiles.csv"), rejected)

    def test_shared_person_profiles_cannot_diverge(self):
        fellow = recipient()
        winner = recipient(name="Alice P. Person", acm_fellow_profile="http://awards.acm.org/award-recipients/PERSON_A123.cfm",
                           dblp_profile="http://dblp.org/pid/1/2.html?view=by-type#ref")
        self.assertEqual(validate_shared_recipients({"fellows": [fellow], "turing": [winner]}), 1)
        for field, value in [("dblp_profile", "https://dblp.org/pid/9/9"), ("google_scholar_profile", ""),
                             ("dblp_profile_quality", "N"), ("csrankings_name", "Different Person"),
                             ("csrankings_name_alignment_date", "2026-09-17")]:
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                changed = dict(winner, **{field: value})
                validate_shared_recipients({"fellows": [fellow], "turing": [changed]})

    def test_namesakes_with_distinct_acm_ids_are_not_merged(self):
        self.assertEqual(validate_shared_recipients({"fellows": [recipient()], "turing": [
            recipient(acm_fellow_profile="https://awards.acm.org/award-recipients/person_b456", dblp_profile="different")]}), 0)
        self.assertEqual(validate_shared_recipients({"fellows": [recipient(acm_fellow_profile="")], "turing": [recipient()]}), 0)

    def test_alignment_dates_require_valid_iso_dates_and_a_link(self):
        validate_alignment_dates([recipient(), recipient(csrankings_name="", csrankings_name_alignment_date="")])
        for name, value in [("Alice Person", "not-a-date"), ("Alice Person", "2026-02-30"),
                            ("Alice Person", "20260918"), ("Alice Person", ""), ("", "2026-09-18")]:
            with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                validate_alignment_dates([recipient(csrankings_name=name, csrankings_name_alignment_date=value)])

    def test_derived_dblp_requires_agreement_except_documented_exclusions(self):
        roster = recipient()
        table = {"name": "Alice Person", "dblp_profile": "http://dblp.org/pid/1/2.html#ref"}
        validate_derived_dblp_links({"fellows": [roster]}, [table], [])
        for wrong in ["https://dblp.org/pid/9/9", ""]:
            with self.subTest(wrong=wrong), self.assertRaisesRegex(ValueError, "Derived DBLP mismatch"):
                validate_derived_dblp_links({"fellows": [roster]}, [dict(table, dblp_profile=wrong)], [])
        rejected = ["http://dblp.org/pid/1/2.html"]
        validate_derived_dblp_links({"fellows": [roster]}, [dict(table, dblp_profile="")], rejected)
        with self.assertRaisesRegex(ValueError, "Derived DBLP mismatch"):
            validate_derived_dblp_links({"fellows": [roster]}, [table], rejected)

    def test_csrankings_key_cannot_be_reused_within_one_roster(self):
        table = [{"name": "Alice Person", "dblp_profile": "https://dblp.org/pid/1/2"}]
        with self.assertRaisesRegex(ValueError, "Repeated CSRankings key"):
            validate_derived_dblp_links({"fellows": [recipient(), recipient(name="Someone Else")]}, table, [])


if __name__ == "__main__":
    unittest.main()

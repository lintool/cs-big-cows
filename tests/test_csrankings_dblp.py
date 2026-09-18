"""Compatibility examples captured from upstream CSRankings' JavaScript."""
import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.csrankings_dblp import csrankings_dblp_url

ROOT = Path(__file__).resolve().parents[1]


class CSRankingsDBLPTests(unittest.TestCase):
    def test_upstream_url_examples(self):
        # Evaluated with src/utils.ts + bundled he 1.2.0 from upstream commit
        # b2e76bcec658a429c26011530767528839d524df, not inferred from award URLs.
        examples = {
            "Emery D. Berger": "b/Berger:Emery_D%3D",
            "Kai Li 0001": "l/Li_0001:Kai",
            "Bernhard Schölkopf [IS]": "s/Sch=ouml=lkopf:Bernhard",
            "  Anja Feldmann [INF]  ": "f/Feldmann:Anja",
            "John Smith Jr.": "s/Smith_Jr=:John",
            "John Smith III": "s/Smith_III:John",
            "Renée O'Connor": "o/O=Connor:Ren%3Deacute%3De",
            "Jean-Luc Évrard": "=/=Eacute=vrard:Jean%3DLuc",
            "Václav Černý": "=/=Ccaron=ern=yacute=:V%3Daacute%3Dclav",
            "Arvind": "a/Arvind:",
            "Alice Person 0000": "0/0000:Alice_Person",
            "Alice Person 0001": "p/Person_0001:Alice",
            "Alice Person 0002": "p/Person_0002:Alice",
            "李 明": "=/=#x660E=:%3D%23x674E%3D",
        }
        for name, suffix in examples.items():
            with self.subTest(name=name):
                self.assertEqual(csrankings_dblp_url(name), "https://dblp.org/pers/hd/" + suffix)

    def test_cli_checks_without_writing_then_changes_only_derived_field(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profiles.csv"
            original = ('name,affiliation,homepage,scholarid,orcid,dblp_profile\n'
                        'Kai Li 0001,Princeton,https://example.org,upstream-error,,https://dblp.org/pid/65/8684\n')
            path.write_text(original)
            command = [sys.executable, str(ROOT / "scripts/csrankings_dblp.py"), "--profiles", str(path)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
            self.assertEqual(path.read_text(), original)
            self.assertEqual(subprocess.run(command + ["--write"], capture_output=True).returncode, 0)
            with path.open(newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(rows, [dict(name="Kai Li 0001", affiliation="Princeton", homepage="https://example.org",
                                       scholarid="upstream-error", orcid="", dblp_profile="https://dblp.org/pers/hd/l/Li_0001:Kai")])
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            once = path.read_bytes()
            subprocess.run(command + ["--write"], capture_output=True, check=True)
            self.assertEqual(path.read_bytes(), once)

    def test_cli_rejects_duplicate_keys_without_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profiles.csv"
            original = "name,dblp_profile\nAlice Person,\nAlice Person,\n"
            path.write_text(original)
            result = subprocess.run([sys.executable, str(ROOT / "scripts/csrankings_dblp.py"),
                                     "--profiles", str(path), "--write"], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(path.read_text(), original)


if __name__ == "__main__":
    unittest.main()

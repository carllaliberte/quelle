#!/usr/bin/env python3
"""Physics locks for QUELLE v0. Tests, not a theorem. Not a QUANTUM seal."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import quelle  # noqa: E402


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _refus(fn, *args, **kwargs) -> str:
    with unittest.TestCase().assertRaises(SystemExit) as ctx:
        fn(*args, **kwargs)
    return str(ctx.exception)


def _cli(args, cwd=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "quelle.py"), *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
    )


class DefaultTirerIsOs(unittest.TestCase):
    def test_tirer_default_source_is_os(self):
        rec = quelle.tirer()
        self.assertEqual(rec["carte"]["source"], "os")
        self.assertEqual(rec["carte"]["format"], "quelle.v0")
        self.assertEqual(rec["carte"]["n_octets"], 32)

    def test_tirer_explicit_os_is_os(self):
        rec = quelle.tirer(16, "os")
        self.assertEqual(rec["carte"]["source"], "os")
        self.assertEqual(rec["carte"]["n_octets"], 16)
        self.assertEqual(len(rec["octets_hex"]), 32)

    def test_cli_tirer_default_is_os(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "carte.quelle.json"
            proc = _cli(["tirer", "--octets", "16", "--vers", str(dest)], cwd=tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertEqual(out["source"], "os")
            written = json.loads(dest.read_text(encoding="utf-8"))
            self.assertEqual(written["source"], "os")


class OsCardIsNotQuantiqueAndNotAPhoton(unittest.TestCase):
    def test_os_card_does_not_mint_quantique(self):
        carte = quelle.tirer()["carte"]
        self.assertEqual(carte["source"], "os")
        self.assertNotIn("quantique", carte)
        self.assertNotIn("mode", carte)
        self.assertNotEqual(carte.get("source"), "quantique")

    def test_os_note_denies_photon(self):
        carte = quelle.tirer()["carte"]
        note = carte["note"].lower()
        self.assertIn("pas un photon", note)
        self.assertNotIn("photon invent", note)

    def test_os_card_is_not_written_as_a_photon_source(self):
        carte = quelle.tirer()["carte"]
        self.assertEqual(carte["source"], "os")
        self.assertIsNone(carte["appareil"])
        dumped = _dump(carte).lower()
        self.assertNotIn('"source": "photon"', dumped)
        self.assertNotIn('"source": "qrng"', dumped)
        self.assertNotIn('"source": "qkd"', dumped)

    def test_example_os_card_is_classique_not_quantique(self):
        carte = json.loads((ROOT / "examples" / "os-32.quelle.json").read_text(encoding="utf-8"))
        self.assertEqual(carte["source"], "os")
        self.assertNotIn("quantique", carte)
        self.assertNotIn("mode", carte)


class CannotWriteQrngWithoutHardware(unittest.TestCase):
    def test_tirer_qrng_refuses_without_hardware(self):
        msg = _refus(quelle.tirer, 32, "qrng")
        self.assertIn("qrng", msg)
        self.assertIn("refus", msg.lower())

    def test_tirer_qkd_refuses_without_hardware(self):
        msg = _refus(quelle.tirer, 32, "qkd")
        self.assertIn("qkd", msg)
        self.assertIn("refus", msg.lower())

    def test_cli_tirer_qrng_refuses(self):
        proc = _cli(["tirer", "--source", "qrng"])
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("qrng", (proc.stderr + proc.stdout).lower())

    def test_cli_tirer_qkd_refuses(self):
        proc = _cli(["tirer", "--source", "qkd"])
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("qkd", (proc.stderr + proc.stdout).lower())

    def test_lire_qrng_without_appareil_and_without_simule_is_a_lie(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "lie.quelle.json"
            p.write_text(
                json.dumps(
                    {
                        "format": "quelle.v0",
                        "id": "QL-lie",
                        "source": "qrng",
                        "simule": False,
                        "appareil": None,
                        "n_octets": 8,
                        "sha256": "0" * 64,
                        "tire_at": "2026-09-03T00:00:00Z",
                    }
                ),
                encoding="utf-8",
            )
            msg = _refus(quelle.lire, str(p))
            self.assertIn("mensong", msg.lower())

    def test_webcam_ibm_ionq_are_not_hardware_paths_in_code(self):
        src = (ROOT / "quelle.py").read_text(encoding="utf-8")
        lowered = src.lower()
        self.assertNotIn("webcam", lowered)
        self.assertNotIn("ibm", lowered)
        self.assertNotIn("ionq", lowered)
        self.assertNotIn("bb84", lowered)
        self.assertIn('source != "os"', src)


class HonestOsIsNotSimule(unittest.TestCase):
    def test_tirer_os_does_not_stamp_simule_true(self):
        carte = quelle.tirer()["carte"]
        self.assertIs(carte["simule"], False)

    def test_cli_tirer_os_does_not_stamp_simule_true(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "os.quelle.json"
            proc = _cli(["tirer", "--source", "os", "--vers", str(dest)], cwd=tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertIs(out["simule"], False)
            written = json.loads(dest.read_text(encoding="utf-8"))
            self.assertIs(written["simule"], False)

    def test_example_os_card_is_not_a_simulation(self):
        carte = json.loads((ROOT / "examples" / "os-32.quelle.json").read_text(encoding="utf-8"))
        self.assertEqual(carte["source"], "os")
        self.assertIs(carte["simule"], False)

    def test_presented_software_protocol_may_claim_simule(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bb84-soft.quelle.json"
            p.write_text(
                json.dumps(
                    {
                        "format": "quelle.v0",
                        "id": "QL-soft",
                        "source": "qkd",
                        "simule": True,
                        "appareil": None,
                        "n_octets": 8,
                        "sha256": "a" * 64,
                        "tire_at": "2026-09-03T00:00:00Z",
                        "note": "BB84 logiciel présenté — simule true",
                    }
                ),
                encoding="utf-8",
            )
            carte = quelle.lire(str(p))
            self.assertIs(carte["simule"], True)
            self.assertEqual(carte["source"], "qkd")


class NoQuantumSealInJson(unittest.TestCase):
    def test_tirer_json_is_not_a_quantum_seal(self):
        dumped = _dump(quelle.tirer()["carte"])
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("quantum seal", dumped.lower())
        self.assertNotIn("Quantum Mode ON", dumped)

    def test_cli_tirer_json_is_not_a_quantum_seal(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "carte.quelle.json"
            proc = _cli(["tirer", "--vers", str(dest)], cwd=tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertNotIn("QUANTUM", proc.stdout)
            written = dest.read_text(encoding="utf-8")
            self.assertNotIn("QUANTUM", written)

    def test_cli_lire_json_is_not_a_quantum_seal(self):
        example = ROOT / "examples" / "os-32.quelle.json"
        proc = _cli(["lire", str(example)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["source"], "os")
        self.assertNotIn("QUANTUM", proc.stdout)
        self.assertNotIn("Imagine", proc.stdout)

    def test_example_json_is_not_a_quantum_seal(self):
        text = (ROOT / "examples" / "os-32.quelle.json").read_text(encoding="utf-8")
        self.assertNotIn("QUANTUM", text)
        self.assertNotIn("Imagine", text)


class ReadmeDoorCopy(unittest.TestCase):
    def test_readme_has_no_imagine_word(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Imagine", text)
        self.assertNotIn("imagine", text)

    def test_readme_does_not_claim_formal_verification(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("formally verified", text)
        self.assertNotIn("formally-verified", text)
        self.assertNotIn("formellement vérifié", text)

    def test_readme_names_three_sources_and_the_public_command(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("`os`", text)
        self.assertIn("`qrng`", text)
        self.assertIn("`qkd`", text)
        self.assertIn("python3 quelle.py tirer", text)
        self.assertIn("python3 quelle.py lire", text)

    def test_readme_says_os_is_classique_not_quantique(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("classique", text)
        self.assertIn("does not mint `quantique`", text)

    def test_copy_on_this_rail_has_no_imagine_word(self):
        for rel in ("README.md", "INTERDIT.md", "JUGE.md", "quelle.py"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("Imagine", text, msg=rel)

    def test_interdit_keeps_the_physics(self):
        text = (ROOT / "INTERDIT.md").read_text(encoding="utf-8")
        self.assertIn("qrng", text)
        self.assertIn("webcam", text)
        self.assertIn("os", text)


class SourcesAreOnlyTheThree(unittest.TestCase):
    def test_unknown_source_is_refused(self):
        msg = _refus(quelle.tirer, 32, "webcam")
        self.assertIn("os | qrng | qkd", msg)

    def test_sources_constant_is_the_three(self):
        self.assertEqual(quelle.SOURCES, ("os", "qrng", "qkd"))


if __name__ == "__main__":
    unittest.main()

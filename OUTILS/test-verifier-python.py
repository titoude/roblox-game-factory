#!/usr/bin/env python3
"""Contrôles de la compilation des sources Python suivies."""
import importlib.util
import io
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

spec = importlib.util.spec_from_file_location("verifier_python", Path(__file__).with_name("verifier-python.py"))
verifier_python = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier_python)


class SyntaxePython(unittest.TestCase):
    def test_compile_sources_suivies_sans_ecrire_dans_le_depot(self):
        with tempfile.TemporaryDirectory() as dossier:
            racine = Path(dossier)
            subprocess.run(["git", "init", "-q"], cwd=racine, check=True)
            suivi = racine / "source suivie.py"
            suivi.write_text("valeur = 1\n", encoding="utf-8")
            subprocess.run(["git", "add", "--", suivi.name], cwd=racine, check=True)
            (racine / "non-suivi.py").write_text("valeur =\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()) as sortie:
                self.assertEqual(verifier_python.verifier(racine), 0)
            self.assertIn("1 fichier(s), 0 erreur(s)", sortie.getvalue())

            suivi.write_text("valeur =\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()) as sortie:
                self.assertEqual(verifier_python.verifier(racine), 1)
            self.assertIn(suivi.name, sortie.getvalue())
            self.assertIn("1 fichier(s), 1 erreur(s)", sortie.getvalue())
            self.assertFalse(list(racine.glob("**/*.pyc")))


if __name__ == "__main__":
    unittest.main()

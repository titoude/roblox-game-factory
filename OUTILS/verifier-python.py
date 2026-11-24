#!/usr/bin/env python3
"""Compile les sources Python suivies, sans écrire de bytecode dans le dépôt."""
import os
import py_compile
import subprocess
import tempfile
from pathlib import Path


def verifier(racine):
    try:
        fichiers = subprocess.check_output(["git", "ls-files", "-z", "--", "*.py"], cwd=racine)
    except (OSError, subprocess.CalledProcessError) as erreur:
        print(f"ECHEC : liste des sources Python : {erreur}")
        return 1
    echecs = 0
    sources = [os.fsdecode(nom) for nom in fichiers.split(b"\0") if nom]
    with tempfile.TemporaryDirectory(prefix="usine-python-") as dossier:
        for source in sources:
            try:
                py_compile.compile(str(racine / source), cfile=str(Path(dossier) / "controle.pyc"), doraise=True)
            except (OSError, py_compile.PyCompileError) as erreur:
                print(f"ECHEC : {erreur}")
                echecs += 1
    print(f"syntaxe Python : {len(sources)} fichier(s), {echecs} erreur(s)")
    return int(echecs > 0)


if __name__ == "__main__":
    raise SystemExit(verifier(Path(__file__).resolve().parent.parent))

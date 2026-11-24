#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôles de luau-verif.ps1 sous Windows PowerShell 5.1, sans modifier le jeu."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

OUTILS = Path(__file__).resolve().parent


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    echecs = []

    def verifier(nom, condition, detail=""):
        print(f"{'PASSE' if condition else 'ECHEC'} : {nom}" +
              (f" : {detail}" if not condition else ""))
        if not condition:
            echecs.append(nom)

    powershell = shutil.which("powershell.exe")
    if not powershell:
        verifier("Windows PowerShell 5.1 disponible", False)
        return 1
    version = subprocess.run([powershell, "-NoProfile", "-NonInteractive", "-Command",
                              "$PSVersionTable.PSVersion.ToString()"], capture_output=True, timeout=20)
    verifier("Windows PowerShell 5.1", version.returncode == 0 and version.stdout.startswith(b"5.1."))
    verifier("script ASCII pur", all(b < 128 for b in (OUTILS / "luau-verif.ps1").read_bytes()))
    with tempfile.TemporaryDirectory(prefix="test-luau-verif-") as dossier:
        racine = Path(dossier)

        def lancer(script, source, environnement=None):
            resultat = subprocess.run([powershell, "-NoProfile", "-NonInteractive", "-ExecutionPolicy",
                                       "Bypass", "-File", str(script), str(source)],
                                      capture_output=True, timeout=30, env=environnement)
            return resultat.returncode, (resultat.stdout + resultat.stderr).decode("utf-8", errors="replace")

        script = OUTILS / "luau-verif.ps1"
        cas = [
            ("globales Roblox filtrées", "ServerScriptService.Correct.lua",
             "local a = game:GetService('Players')\nlocal b = workspace\nlocal c = Instance.new('Part')\nlocal d = Enum.Material.Plastic\ntask.wait()\n", 0, None),
            ("faute de syntaxe", "ServerStorage.Syntaxe.lua", "local x = )", 1, "SYNTAXE"),
            ("globale inconnue", "ServerStorage.Globale.lua", "return workspcae", 1, "GLOBALE"),
            ("fichier vide", "ServerStorage.Vide.lua", "", 1, "VIDE"),
            ("nom sans service", "Incorrect.lua", "return 1", 1, "NOM"),
        ]
        for i, (nom, fichier, contenu, code, diagnostic) in enumerate(cas):
            source = racine / str(i)
            source.mkdir()
            (source / fichier).write_text(contenu, encoding="utf-8")
            retour, sortie = lancer(script, source)
            verifier(f"{nom} : code {code}", retour == code and
                     (diagnostic in sortie if diagnostic else "0 defaut(s)" in sortie), sortie.strip())
        # Le cas correct produit réellement des diagnostics natifs avant filtrage.
        analyse = subprocess.run([str(OUTILS / "bin" / "luau-analyze.exe"),
                                 str(racine / "0" / cas[0][1])], capture_output=True, timeout=20)
        verifier("diagnostics Roblox réellement présents sur stderr", b"Unknown global 'game'" in analyse.stderr)
        retour, sortie = lancer(script, racine / "absent")
        verifier("dossier introuvable : code 5", retour == 5 and "INTROUVABLE" in sortie, sortie.strip())
        vide = racine / "vide"
        vide.mkdir()
        retour, sortie = lancer(script, vide)
        verifier("dossier sans script : code 0", retour == 0 and "aucun script" in sortie, sortie.strip())
        # Isoler la recherche des binaires sans toucher aux exécutables en place.
        copie = racine / "outils" / "luau-verif.ps1"
        copie.parent.mkdir()
        shutil.copyfile(script, copie)
        environnement = dict(os.environ)
        environnement["PATH"] = str(Path(os.environ["SystemRoot"]) / "System32")
        retour, sortie = lancer(copie, racine / "0", environnement)
        verifier("binaires absents : code 2", retour == 2 and "controle partiel" in sortie, sortie.strip())
        retour, sortie = lancer(copie, racine / "3", environnement)
        verifier("défaut prioritaire sur contrôle partiel : code 1", retour == 1 and "VIDE" in sortie, sortie.strip())
        (copie.parent / "bin").mkdir()
        shutil.copyfile(OUTILS / "bin" / "luau-compile.exe", copie.parent / "bin" / "luau-compile.exe")
        retour, sortie = lancer(copie, racine / "0", environnement)
        verifier("analyseur seul absent : code 2", retour == 2 and "controle partiel" in sortie, sortie.strip())
        # Un analyseur qui plante (runtime VC++ trop ancien : 0xC0000005) ne vaut pas un contrôle vert.
        faux = racine / "faux-analyseur"
        faux.mkdir()
        (faux / "luau-analyze.cmd").write_text("@exit /b -1073741819\r\n", encoding="ascii", newline="")
        environnement["PATH"] = str(faux) + os.pathsep + environnement["PATH"]
        retour, sortie = lancer(copie, racine / "0", environnement)
        verifier("analyseur qui plante : code 1", retour == 1 and "ANALYSE" in sortie, sortie.strip())
    return int(bool(echecs))


if __name__ == "__main__":
    raise SystemExit(main())

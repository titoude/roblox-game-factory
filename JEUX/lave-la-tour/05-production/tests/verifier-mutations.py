"""Mutations ciblées sur copies temporaires ; aucun fichier source modifié."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

RACINE = Path(__file__).resolve().parents[4]
PRODUCTION = Path(__file__).resolve().parent.parent
MUTATIONS = [
    ("M6", "Amorce.server", '    if type(genre) ~= "string" or type(id) ~= "string" or #id > 32 then return false end', '', "revue-m6"),
    ("M19", "DonneesService", 'if E.operation(p, operation) then E.hors_ligne(p, math.max(0, maintenant - p.depart)) end', 'E.operation(p, operation); E.hors_ligne(p, math.max(0, maintenant - p.depart))', "revue-m19-m21-d5"),
    ("M21", "DonneesService", 'if not D.valide(p) then warn("[Donnees] profil invalide, ecriture refusee : " .. j.UserId); return false end', '', "revue-m19-m21-d5"),
    ("M22-marque", "Amorce.server", '            Donnees.marquer(joueur)', '', "revue-m22"),
    ("D5", "EtatJoueur", 'return nil, "profil_invalide"', 'return Etat.nouveau()', "revue-m19-m21-d5"),
    ("S1-S2-ecriture-action", "Amorce.server", '            Donnees.marquer(joueur)', '            Donnees.sauver(joueur)', "sauvegarde-budget"),
    ("D8-mousse", "SocialService", 'gain*(C.MOUSSE_MULTIPLICATEUR-1)', 'gain*0.25', "config-comportement"),
    ("D8-validation", "EtatJoueur", 'math.min(p.quotas.mousse_s, C.MOUSSE_QUOTA_S)', 'math.min(p.quotas.mousse_s, 600)', "config-comportement"),
    ("P14-gain-double", "EconomieService", 'return multiplicateur(p, "action") * (', 'return 2 * multiplicateur(p, "action") * (', "rejeu-simulateur"),
    ("P14-revenu", "EconomieService", 'return r * multiplicateur(p, "tout")', 'return 1.5 * r * multiplicateur(p, "tout")', "rejeu-simulateur"),
    ("P14-validation-remote", "VitresService", 'maintenant - a.debut < C.VITRE_DUREE_MIN_S', 'false', "vitres"),
]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    with tempfile.TemporaryDirectory(prefix="llt-mutations-") as temporaire:
        src = Path(temporaire) / "src"
        shutil.copytree(PRODUCTION / "src", src)
        for nom, module, avant, apres, filtre in MUTATIONS:
            fichier = src / ("ServerScriptService.Jeu." + module + ".lua")
            texte = fichier.read_text(encoding="utf-8")
            assert texte.count(avant) == 1, nom + " : cible absente ou ambigue"
            fichier.write_text(texte.replace(avant, apres), encoding="utf-8")
            resultat = subprocess.run([sys.executable, str(RACINE / "OUTILS/banc-luau.py"), str(src),
                                      "--tests", str(PRODUCTION / "tests"), "--filtre", filtre],
                                     capture_output=True, encoding="utf-8", timeout=30)
            fichier.write_text(texte, encoding="utf-8")
            detectee = resultat.returncode == 1 and "ECHEC :" in resultat.stdout and "test suspendu" not in resultat.stdout
            print(f"{nom} : {'DETECTEE' if detectee else 'ECHEC'} ({filtre})")
            if not detectee:
                print(resultat.stdout + resultat.stderr)
                echecs += 1
    return int(echecs > 0)


if __name__ == "__main__":
    raise SystemExit(main())

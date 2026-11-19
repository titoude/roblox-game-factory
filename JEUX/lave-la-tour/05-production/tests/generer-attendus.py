"""Génère les données indépendantes ; bibliothèque standard, aucune modification des outils."""
import json
import os
from pathlib import Path
import subprocess
import sys
from decimal import Decimal, ROUND_CEILING

sys.dont_write_bytecode = True
RACINE = Path(__file__).resolve().parents[4]
ECONOMIE = RACINE / "JEUX/lave-la-tour/03-economie/economie.json"
SIMULATEUR = RACINE / "OUTILS/sim-economie.py"


def luau(valeur):
    if isinstance(valeur, bool):
        return str(valeur).lower()
    if valeur is None:
        return "nil"
    if isinstance(valeur, str):
        return json.dumps(valeur, ensure_ascii=False)
    if isinstance(valeur, (int, float)):
        return repr(valeur)
    if isinstance(valeur, (list, tuple)):
        return "{" + ",\n".join(luau(v) for v in valeur) + "}"
    return "{" + ",\n".join("[" + luau(k) + "] = " + luau(v) for k, v in valeur.items()) + "}"


def main():
    economie = json.loads(ECONOMIE.read_text(encoding="utf-8-sig"))
    execution = subprocess.run([sys.executable, str(SIMULATEUR), str(ECONOMIE), "--json"], capture_output=True, encoding="utf-8", check=True)
    resume, _ = json.JSONDecoder().raw_decode(execution.stdout)
    # Le JSON ne donne pas les soldes : rejeu des flux du simulateur, sans importer Sim.
    profils = {}
    generateurs = {g["id"]: g for g in economie["generateurs"]}
    ameliorations = {a["id"]: a for a in economie["ameliorations"]}
    for nom in ("actif", "lent"):
        resultat = resume["profils"][nom]
        achats = resultat["chronologie_achats"]
        assert len(achats) == resultat["achats"] == 105
        actifs = dict.fromkeys(generateurs, 0)
        mult = dict.fromkeys(generateurs, 1)
        mult_action = mult_tout = 1
        chantiers = []
        solde = economie["depart"]["cash"]
        cadence = economie["action"]["par_minute"] / 60 * economie["profils"][nom]["actions_facteur"]
        prochain = 0
        avant = solde
        for t in range(resultat["fin_s"] + 1):
            for fin, ident in chantiers[:]:
                if fin <= t:
                    actifs[ident] += 1
                    chantiers.remove((fin, ident))
            if prochain < len(achats) and achats[prochain]["temps_s"] == t:
                achat = achats[prochain]
                achat["solde_avant_1s"] = avant
                solde -= achat["cout"]
                achat["solde_apres"] = solde
                ident = achat["id"]
                if ident in generateurs:
                    chantier = generateurs[ident]["chantier_s"]
                    if chantier:
                        chantiers.append((t + chantier, ident))
                    else:
                        actifs[ident] += 1
                else:
                    a = ameliorations[ident]
                    if a["cible"] == "action":
                        mult_action *= a["multiplicateur"]
                    elif a["cible"] == "tout":
                        mult_tout *= a["multiplicateur"]
                    else:
                        mult[a["cible"]] *= a["multiplicateur"]
                prochain += 1
            avant = solde
            revenu = sum(actifs[i] * g["revenu_s"] * mult[i] * mult_tout for i, g in generateurs.items())
            gain = mult_action * (economie["action"]["gain"] * mult_tout + economie["action"]["part_revenu_s"] * revenu)
            solde += revenu + cadence * gain
        profils[nom] = {"achats": achats, "jalons": resultat["jalons_s"], "fin_s": resultat["fin_s"], "cadence": cadence}
    prix = {g["id"]: [int((Decimal(str(g["cout"])) * Decimal(str(g["croissance_cout"])) ** n).to_integral_value(rounding=ROUND_CEILING)) for n in range(g["max"])] for g in economie["generateurs"]}
    texte = "-- Généré par tests/generer-attendus.py ; ne pas éditer.\nreturn " + luau({"economie": economie, "prix": prix, "profils": profils}) + "\n"
    destination = Path(__file__).resolve().parent.parent / "src/ServerStorage.Tests.Attendus.lua"
    temporaire = destination.with_suffix(".tmp")
    temporaire.write_text(texte, encoding="utf-8")
    assert temporaire.read_text(encoding="utf-8") == texte
    os.replace(temporaire, destination)
    print("Attendus : 100 prix exacts, 105 achats par profil, jalons et fins ; module ServerStorage.Tests.Attendus")


if __name__ == "__main__":
    main()

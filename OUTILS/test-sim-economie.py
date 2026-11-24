#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test-sim-economie.py - contrôles du simulateur d'économie. Bibliothèque standard, aucun réseau.

Usage : python OUTILS/test-sim-economie.py        (code de sortie 0 si tout passe, 1 sinon)

Ces cas viennent des défauts trouvés au cycle 1 par les vérificateurs d'économie :
remboursement jugé sur le seul premier exemplaire, revenu marginal oubliant l'action indexée,
verdict PASSE quand la fin n'est pas atteinte sur une durée trop courte.
"""
import hashlib
import subprocess
import copy
import json
import math
import runpy
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
m = runpy.run_path(str(RACINE / "OUTILS" / "sim-economie.py"))
Sim, analyser, valider, SEUILS = m["Sim"], m["analyser"], m["valider"], dict(m["SEUILS_DEFAUT"])

ECO = {
    "jeu": "test", "depart": {"cash": 0},
    "action": {"gain": 1, "par_minute": 30, "part_revenu_s": 0.2},
    "generateurs": [
        {"id": "g1", "cout": 10, "revenu_s": 0.25, "croissance_cout": 1.2, "max": 10, "chantier_s": 0, "debloque": ""},
        {"id": "g2", "cout": 90, "revenu_s": 2, "croissance_cout": 1.2, "max": 10, "chantier_s": 5, "debloque": "g1>=3"},
    ],
    "ameliorations": [
        {"id": "a1", "cout": 40, "cible": "action", "multiplicateur": 2, "debloque": "g1>=2"},
        {"id": "a2", "cout": 300, "cible": "g2", "multiplicateur": 2, "debloque": "g2>=1"},
        {"id": "a3", "cout": 900, "cible": "tout", "multiplicateur": 1.5, "debloque": "g2>=3"},
    ],
    "fin_contenu": "g2>=10",
}

echecs = []


def verifier(nom, condition, detail=""):
    print(("ok     " if condition else "ECHEC  ") + nom + (f" : {detail}" if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


def proche(a, b):
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


# 1. Le revenu marginal annoncé d'un candidat égale la hausse réelle du revenu total, action indexée comprise.
for profil in ({"actions_facteur": 1.0}, {"actions_facteur": 0.5}):
    sim = Sim(copy.deepcopy(ECO), profil)
    sim.actifs.update({"g1": 4, "g2": 2})
    sim.poss.update({"g1": 4, "g2": 2})
    for c in sim.candidats():
        essai = copy.deepcopy(sim)
        avant = essai.revenu()
        if c[0] == "gen":
            essai.actifs[c[1]] += 1
        else:
            u = essai.ups[c[1]]
            if u["cible"] == "action":
                essai.mult_action *= u["multiplicateur"]
            elif u["cible"] == "tout":
                essai.mult_tout *= u["multiplicateur"]
            else:
                essai.mult[u["cible"]] *= u["multiplicateur"]
        gain = essai.revenu() - avant
        verifier(f"marginal de {c[1]} (facteur {profil['actions_facteur']})", proche(gain, c[4]), f"{gain} contre {c[4]}")

# 2. Le remboursement est jugé sur chaque exemplaire : une croissance de 1,2 sur dix exemplaires à 291 s échoue.
long = {"jeu": "t", "depart": {"cash": 0}, "action": {"gain": 1000, "par_minute": 60},
        "generateurs": [{"id": "g", "cout": 2910, "revenu_s": 10, "croissance_cout": 1.2, "max": 10, "chantier_s": 0, "debloque": ""}],
        "fin_contenu": "g>=10"}
valider(long)
a = analyser(Sim(long, {}).lancer(14400), SEUILS, 14400)
ligne = [x for x in a["lignes"] if x["mesure"] == "Remboursement de chaque exemplaire"][0]
verifier("dixième exemplaire hors borne détecté", ligne["verdict"] == "ÉCHEC" and len(a["hors_bornes"]) == 9,
         f"{ligne['verdict']}, {len(a['hors_bornes'])} hors bornes")
dernier = a["hors_bornes"][-1]
verifier("remboursement du dixième = 291 × 1,2^9", proche(dernier[4], 291 * 1.2 ** 9), str(dernier[4]))

# 3. Prix entiers : arrondi à l'entier supérieur de coût × croissance^(rang - 1).
entier = copy.deepcopy(ECO)
entier["prix_entiers"] = True
sim = Sim(entier, {})
sim.poss["g1"] = 2
verifier("prix entier du troisième g1 = 15", sim.cout_gen("g1") == 15, str(sim.cout_gen("g1")))
sim.poss["g1"] = 0
verifier("prix entier du premier g1 = 10", sim.cout_gen("g1") == 10, str(sim.cout_gen("g1")))

exact = {"jeu": "t", "prix_entiers": True, "action": {"gain": 1, "par_minute": 30},
         "generateurs": [{"id": "g", "cout": 5600000, "revenu_s": 34500, "croissance_cout": 1.10, "max": 10}]}
sim = Sim(exact, {})
sim.poss["g"] = 3
verifier("prix entier exact : 5 600 000 × 1,1^3 = 7 453 600", sim.cout_gen("g") == 7453600, str(sim.cout_gen("g")))

# 4. Fin non atteinte sur une durée plus courte que le minimum demandé : échec, pas alerte.
a = analyser(Sim(copy.deepcopy(ECO), {}).lancer(60), SEUILS, 60)
ligne = [x for x in a["lignes"] if x["mesure"] == "Durée de contenu actif"][0]
verifier("durée simulée trop courte = ÉCHEC", ligne["verdict"] == "ÉCHEC", ligne["verdict"])

# 5. L'attente finale (dernier chantier) compte dans les écarts.
a = analyser(Sim(copy.deepcopy(ECO), {}).lancer(14400), SEUILS, 14400)
verifier("fin atteinte sur l'économie de test", a["fin"] is not None)
verifier("attente finale comptée", a["ecarts"][-1][0] == a["achats"][-1][0] and a["ecarts"][-1][1] == a["fin"] - a["achats"][-1][0])

# 6. L'exemple fourni avec l'usine tient ses propres seuils (sinon tout nouveau jeu part d'un modèle faux).
exemple = json.loads((RACINE / "OUTILS" / "GABARITS" / "economie.exemple.json").read_text(encoding="utf-8-sig"))
valider(exemple)
seuils = dict(SEUILS)
seuils.update({k: v for k, v in json.loads((RACINE / "CONNAISSANCES" / "seuils.json").read_text(encoding="utf-8-sig"))["economie"].items() if k in SEUILS})
a = analyser(Sim(exemple, exemple["profils"]["actif"]).lancer(14400), seuils, 14400)
mauvais = [x["mesure"] for x in a["lignes"] if x["verdict"] == "ÉCHEC"]
verifier("exemple du gabarit sans échec", not mauvais, ", ".join(mauvais))

# 7. Contrat public JSON et stabilité de la sortie Markdown du gabarit.
commande = [sys.executable, "OUTILS/sim-economie.py", "OUTILS/GABARITS/economie.exemple.json"]
execution = subprocess.run(commande + ["--json"], cwd=RACINE, capture_output=True, timeout=30)
donnees = json.JSONDecoder().raw_decode(execution.stdout.decode("utf-8"))[0]
verifier("sortie JSON du gabarit : code 0", execution.returncode == 0)
for nom, profil in donnees["profils"].items():
    achats = profil["chronologie_achats"]
    verifier(f"{nom} : nombre d'achats JSON", len(achats) == profil["achats"])
    verifier(f"{nom} : instants strictement croissants", all(a["temps_s"] < b["temps_s"] for a, b in zip(achats, achats[1:])))
    verifier(f"{nom} : dernier achat avant la fin", profil["fin_s"] is not None and achats[-1]["temps_s"] <= profil["fin_s"])
    simulation = Sim(exemple, exemple["profils"][nom]).lancer(14400)
    rangs = {(t, ident): rang for t, ident, rang, *_ in simulation.transactions}
    verifier(f"{nom} : instants, identifiants, exemplaires, coûts et écarts exacts",
             achats == [{"temps_s": t, "id": ident, "exemplaire": rangs.get((t, ident)), "cout": cout,
                         "ecart_s": t - (simulation.achats[i-1][0] if i else 0)}
                        for i, (t, ident, _, cout) in enumerate(simulation.achats)])
    verifier(f"{nom} : jalons horodatés exacts", profil["jalons_s"] == simulation.jalons)
markdown = subprocess.run(commande, cwd=RACINE, capture_output=True, timeout=30)
# Empreinte des octets stdout avec fins de ligne LF (chemin d'entrée fixe).
verifier("Markdown du gabarit inchangé après normalisation des fins de ligne", markdown.returncode == 0 and
         hashlib.sha256(markdown.stdout.replace(b"\r\n", b"\n")).hexdigest() ==
         "8e2178cd211e1582b51f4b9e80c475e484330efa8711dcf41343cb076854da2e")

print(f"{len(echecs)} échec(s)")
sys.exit(1 if echecs else 0)

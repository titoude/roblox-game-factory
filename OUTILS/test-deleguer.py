#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôles de OUTILS\\deleguer.py et de CONNAISSANCES\\routage.json.

  python OUTILS\\test-deleguer.py          contrôles sans lancer de modèle (lancés par verifier-usine.ps1)
  python OUTILS\\test-deleguer.py --reel   en plus : un aller-retour réel par CLI et un repli à l'exécution
                                           (consomme un peu de quota Codex et Claude Haiku)
Code de sortie : 0 si tout passe, 1 sinon.
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
spec = importlib.util.spec_from_file_location("deleguer", os.path.join(ICI, "deleguer.py"))
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
echecs = 0


def controle(nom, condition, detail=""):
    global echecs
    print("%s : %s%s" % ("PASSE" if condition else "ECHEC", nom, (" (" + detail + ")") if detail and not condition else ""))
    if not condition:
        echecs += 1


def appel(args):
    r = subprocess.run([sys.executable, os.path.join(ICI, "deleguer.py")] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=RACINE)
    return r.returncode, r.stdout + r.stderr


routage = d.lire_routage()
roles = routage["roles"]

# 1. Forme du routage
controle("chaque rôle a au moins un candidat", all(r.get("candidats") for r in roles.values()))
fournisseurs = set(routage["fournisseurs"])
controle("chaque candidat nomme un fournisseur connu",
         all(c["fournisseur"] in fournisseurs for r in roles.values() for c in r["candidats"]))
controle("chaque effort est permis par son fournisseur",
         all(c["effort"] in routage["fournisseurs"][c["fournisseur"]]["efforts"] for r in roles.values() for c in r["candidats"]))
etapes = {"00.orchestrateur", "01.veilleur", "02.concepteur", "03.calcul", "03.adversaire", "03.contre-verification",
          "04.relecteur-fun", "05.codeur", "05.producteur-studio", "05.relecteur-code", "06.testeur", "06.analyste",
          "06.qualification", "07.revue-diff", "08.redacteur-kit", "09.analyste-bilan", "11.juge-retours",
          "12.veilleur-promo", "12.scenariste-video"}
controle("tous les rôles de la chaîne sont routés", etapes <= set(roles), ", ".join(sorted(etapes - set(roles))))
petits = set(routage["classes"]["petit"])
controle("aucun petit modèle en premier choix d'un rôle de la chaîne (consigne du 16/11/2026)",
         all(roles[e]["candidats"][0]["modele"] not in petits for e in etapes))
controle("un petit modèle en repli est toujours marqué « degrade »",
         all(c.get("degrade") for e in etapes for c in roles[e]["candidats"] if c["modele"] in petits))
controle("la revue du fun et le concept n'ont pas le même premier modèle (A2)",
         roles["04.relecteur-fun"]["candidats"][0]["modele"] != roles["02.concepteur"]["candidats"][0]["modele"])
controle("le relecteur de code n'a pas le même premier modèle que le codeur (A2)",
         roles["05.relecteur-code"]["candidats"][0]["modele"] != roles["05.codeur"]["candidats"][0]["modele"]
         or bool(roles["05.relecteur-code"].get("interdit_si_auteur")))
controle("plafond G2 écrit et ≤ 2 par défaut", int(routage["plafond_claude_forts_simultanes"]) <= 2)

# 2. Choix et replis (sans lancer)
c, rang, _ = d.choisir(routage, "01.veilleur", pour_lancer=False)
controle("veille : premier choix gpt-6.1-sol", c["modele"] == "gpt-6.1-sol" and rang == 0)
c, rang, ec = d.choisir(routage, "01.veilleur", indisponibles=("codex",), pour_lancer=False)
controle("veille sans Codex : repli Claude, rang 1", c["fournisseur"] == "claude" and rang == 1 and len(ec) == 1)
c, rang, ec = d.choisir(routage, "03.calcul", indisponibles=("codex", "claude"), pour_lancer=False)
controle("économie sans aucun fournisseur : aucun candidat", c is None)
c, rang, ec = d.choisir(routage, "04.relecteur-fun", auteur="claude:claude-opus-5-5", pour_lancer=False)
controle("revue du fun : l'auteur est écarté (A2)", c["modele"] != "claude-opus-5-5")
t3 = d.charge_t3(routage, "03.calcul", roles["03.calcul"]["candidats"][0], "Économie : calcul", "prompt")
controle("charge utile T3 : fournisseur, modèle, option d'effort",
         t3["target"] == {"providerInstanceId": "codex", "model": "gpt-6.1-sol", "options": {"reasoningEffort": "xhigh"}}
         and t3["mode"] == "async" and t3["task"] == "prompt")
t3 = d.charge_t3(routage, "02.concepteur", roles["02.concepteur"]["candidats"][0], "", "p")
controle("charge utile T3 Claude : option « effort »", t3["target"]["options"] == {"effort": "high"}
         and t3["target"]["providerInstanceId"] == "claudeAgent")
controle("dernière ligne RESULTAT reconnue", d.dernier_resultat("bla\nRESULTAT: echec | f.md | raison\n")[0] == "echec")
controle("absence de RESULTAT reconnue", d.dernier_resultat("bla bla")[0] is None)

# 3. Ligne de commande
code, sortie = appel(["--role", "inconnu.role", "--simuler"])
controle("rôle inconnu : code 2", code == 2, sortie[:200])
code, sortie = appel(["--role", "03.calcul", "--simuler", "--indisponible", "codex,claude"])
controle("aucun candidat : code 5", code == 5, sortie[:200])
code, sortie = appel(["--role", "01.veilleur", "--format", "t3"])
controle("format t3 : code 3 et JSON lisible", code == 3 and json.loads(sortie[sortie.index("{"):])["target"]["model"] == "gpt-6.1-sol", sortie[:200])
with tempfile.TemporaryDirectory() as tmp:
    f = os.path.join(tmp, "p.md")
    with io.open(f, "w", encoding="utf-8") as h:
        h.write("voici la clef : x-api-key: " + "A" * 40)
    code, sortie = appel(["--role", "test.ping-codex", "--prompt-fichier", f])
    controle("prompt contenant un secret probable : refusé, code 7", code == 7, sortie[:200])

# 4. Réel (facultatif)
if "--reel" in sys.argv:
    with tempfile.TemporaryDirectory() as tmp:
        f = os.path.join(tmp, "ping.md")
        with io.open(f, "w", encoding="utf-8") as h:
            h.write("Tu es un agent de test. Ne lis aucun fichier, ne modifie rien, ne lance aucune commande. "
                    "Réponds par une seule ligne : RESULTAT: ok | aucun | ping")
        code, sortie = appel(["--role", "test.ping-codex", "--prompt-fichier", f, "--titre", "test réel codex"])
        controle("réel : codex exec rend RESULTAT: ok", code == 0, sortie[-300:])
        code, sortie = appel(["--role", "test.ping-claude", "--prompt-fichier", f, "--titre", "test réel claude"])
        controle("réel : claude -p rend RESULTAT: ok", code == 0, sortie[-300:])
        # Repli à l'exécution : premier candidat avec un modèle qui n'existe pas.
        faux = json.loads(json.dumps(routage))
        faux["roles"]["test.repli"]["candidats"][0]["modele"] = "modele-qui-n-existe-pas"
        fr = os.path.join(tmp, "routage.json")
        with io.open(fr, "w", encoding="utf-8") as h:
            json.dump(faux, h, ensure_ascii=False)
        code, sortie = appel(["--role", "test.repli", "--prompt-fichier", f, "--routage", fr, "--titre", "test réel repli"])
        controle("réel : modèle refusé par la CLI, repli sur le candidat suivant, RESULTAT: ok",
                 code == 0 and "REPLI:" in sortie and "ECHEC-CLI:" in sortie, sortie[-600:])

print("%d échec(s)" % echecs)
sys.exit(1 if echecs else 0)

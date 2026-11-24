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
import time
from contextlib import redirect_stdout
from unittest.mock import patch

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
spec = importlib.util.spec_from_file_location("deleguer", os.path.join(ICI, "deleguer.py"))
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
spec = importlib.util.spec_from_file_location("usine", os.path.join(RACINE, "usine.py"))
usine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usine)

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
sur_accord = set(routage["sur_accord"]["modeles"])
controle("Opus 5.5 et Astra 6.2 sont sur accord du propriétaire (consigne du 24/11/2026)",
         {"claude-opus-5-5", "gpt-6.2-astra"} <= sur_accord)
verifs = {k for k, r in roles.items() if r.get("verification") and k in etapes}
controle("les rôles de vérification sont marqués", {"03.calcul", "03.adversaire", "03.contre-verification", "04.relecteur-fun",
                                                   "05.relecteur-code", "06.qualification", "07.revue-diff"} <= verifs)
controle("vérification : Opus 5.5 ou Astra 6.2 d'abord, puis Codex gpt-6.1-sol en repli marqué « degrade »",
         all(roles[k]["candidats"][0]["modele"] in sur_accord and roles[k]["candidats"][-1]["modele"] == "gpt-6.1-sol"
             and roles[k]["candidats"][-1].get("degrade") for k in verifs))
production = etapes - verifs
controle("production : SWE 2.1 en premier choix (agent principal)",
         all(roles[k]["candidats"][0]["modele"] == "swe-2.1" for k in production))
controle("production : Codex gpt-6.1-sol en premier repli (sauf Studio, qui exige Claude et le MCP de Studio)",
         all(roles[k]["candidats"][1]["modele"] == "gpt-6.1-sol" for k in production - {"05.producteur-studio"}))
champs = {"modele": "m", "effort": "e", "racine": "r", "dernier": "d"}
controle("arguments de la CLI SWE 2.1 : gabarit lisible, prompt hors arguments (G9)",
         all("{prompt}" not in x for x in routage["fournisseurs"]["devin"]["cli_args"])
         and [x.format(**champs) for x in routage["fournisseurs"]["devin"]["cli_args"]] is not None)

# 2. Choix et replis (sans lancer)
c, rang, _ = d.choisir(routage, "01.veilleur", pour_lancer=False)
controle("veille : premier choix SWE 2.1", c["modele"] == "swe-2.1" and rang == 0)
c, rang, _ = d.choisir(routage, "01.veilleur", indisponibles=("devin",), pour_lancer=False)
controle("veille sans SWE 2.1 : repli Codex gpt-6.1-sol, rang 1", c["modele"] == "gpt-6.1-sol" and rang == 1)
c, rang, _ = d.choisir(routage, "01.veilleur", pour_lancer=False, pour_t3=True)
controle("veille depuis T3 Code : SWE 2.1 non joignable, Codex", c["modele"] == "gpt-6.1-sol" and rang == 1)
c, rang, ec = d.choisir(routage, "01.veilleur", indisponibles=("devin", "codex"), pour_lancer=False)
controle("veille sans SWE ni Codex : repli Claude, rang 2", c["fournisseur"] == "claude" and rang == 2 and len(ec) == 2)
c, rang, ec = d.choisir(routage, "03.calcul", indisponibles=("codex", "claude"), pour_lancer=False)
controle("économie sans aucun fournisseur : aucun candidat", c is None)
c, rang, ec = d.choisir(routage, "04.relecteur-fun", auteur="claude:claude-opus-5-5", pour_lancer=False)
controle("revue du fun : l'auteur est écarté (A2)", c["modele"] != "claude-opus-5-5")
t3 = d.charge_t3(routage, "03.calcul", roles["03.calcul"]["candidats"][-1], "Économie : calcul", "prompt")
controle("charge utile T3 : fournisseur, modèle, option d'effort",
         t3["target"] == {"providerInstanceId": "codex", "model": "gpt-6.1-sol", "options": {"reasoningEffort": "xhigh"}}
         and t3["mode"] == "async" and t3["task"] == "prompt")
t3 = d.charge_t3(routage, "02.concepteur", roles["02.concepteur"]["candidats"][2], "", "p")
controle("charge utile T3 Claude : option « effort »", t3["target"]["options"] == {"effort": "high"}
         and t3["target"]["providerInstanceId"] == "claudeAgent")
controle("dernière ligne RESULTAT reconnue", d.dernier_resultat("bla\nRESULTAT: echec | f.md | raison\n")[0] == "echec")
controle("absence de RESULTAT reconnue", d.dernier_resultat("bla bla")[0] is None)

for codex_repond in (True, False):
    tentatives = []

    def lancer_cycle(routage, role, candidat, *args):
        tentatives.append(candidat["modele"])
        if candidat["fournisseur"] == "codex" and codex_repond:
            return {"final": "ETAT_CYCLE: termine | essai", "duree_s": 0,
                    "verdict": "ok", "code_cli": 0, "sans_message": False}
        return {"final": "", "duree_s": 0, "verdict": None, "code_cli": 1, "sans_message": True}

    with tempfile.TemporaryDirectory() as tmp, patch.object(usine, "RACINE", tmp), \
            patch.object(usine, "charger_deleguer", return_value=d), \
            patch.object(usine, "empreinte_etat", return_value=""), \
            patch.object(d, "cli_presente", return_value=True), patch.object(d, "lancer", side_effect=lancer_cycle), \
            redirect_stdout(io.StringIO()):
        code = usine.cmd_cycle("cycle de test", 5, False)
    controle("cycle : SWE 2.1 puis Codex" if codex_repond else "cycle : arrêt sans rejouer les candidats épuisés",
             code == (0 if codex_repond else 1) and tentatives == ["swe-2.1", "gpt-6.1-sol"],
             " -> ".join(tentatives))

# 2 bis. Quota sur accord du propriétaire (Q1) : aucun modèle n'est lancé, tout est simulé.
def principal(args, lancements=None, retours=None, env=None):
    """Lance deleguer.main en isolant JOURNAUX ; rend (code, sortie, modèles lancés, messages envoyés)."""
    lances, messages = [], []
    retours = list(retours or [])

    def faux_lancer(routage, role, candidat, *a):
        lances.append(candidat["modele"])
        if retours:
            return retours.pop(0)
        return {"code_cli": 0, "verdict": "ok", "ligne": "RESULTAT: ok", "duree_s": 0, "final": "RESULTAT: ok | x | y",
                "journal": os.path.join(d.RACINE, "x.log"), "expire": False, "fige": False, "sans_message": False}
    with patch.object(d, "cli_presente", return_value="/bin/cli"), patch.object(d, "lancer", side_effect=faux_lancer), \
            patch.object(d, "prevenir", side_effect=lambda *a: messages.append(a) or 0), \
            patch.dict(os.environ, env or {}), redirect_stdout(io.StringIO()) as sortie:
        code = d.main(args)
    return code, sortie.getvalue(), lances, messages


with tempfile.TemporaryDirectory() as tmp, patch.object(d, "RACINE", tmp), \
        patch.object(d, "JOURNAL", os.path.join(tmp, "JOURNAUX", "delegations.csv")), \
        patch.object(d, "DOS_AGENTS", os.path.join(tmp, "JOURNAUX", "agents")):
    os.environ.pop("USINE_ROLE", None)
    prompt = os.path.join(tmp, "p.md")
    with io.open(prompt, "w", encoding="utf-8") as h:
        h.write("relis le diff")
    c, rang, ec = d.choisir(routage, "07.revue-diff", pour_lancer=False)
    controle("sans accord : Astra 6.2 et Opus 5.5 écartés, repli Codex gpt-6.1-sol",
             c["modele"] == "gpt-6.1-sol" and rang == 2 and d.modeles_sans_accord(ec) == ["gpt-6.2-astra", "claude-opus-5-5"])

    code, sortie, lances, messages = principal(["--role", "07.revue-diff", "--prompt-fichier", prompt])
    controle("sans accord : seul Codex est lancé, jamais Opus ni Astra", code == 0 and lances == ["gpt-6.1-sol"], sortie)
    controle("sans accord : une demande par modèle part au propriétaire",
             sorted(m[2] for m in messages) == ["quota-claude-opus-5-5", "quota-gpt-6.2-astra"]
             and all("--accorder" in m[1] for m in messages), repr(messages))
    controle("sans accord : la demande est écrite dans JOURNAUX",
             set(d.lire_json_local(os.path.join(tmp, "JOURNAUX", "demandes-quota.json"))) == {"claude-opus-5-5", "gpt-6.2-astra"})
    code, sortie, lances, messages = principal(["--role", "03.calcul", "--prompt-fichier", prompt])
    controle("demande déjà ouverte : pas de second message", messages == [] and lances == ["gpt-6.1-sol"], repr(messages))
    code, sortie, lances, messages = principal(["--role", "05.relecteur-code", "--simuler"])
    controle("simulation : aucune demande envoyée, aucun lancement", code == 3 and not messages and not lances
             and "ACCORD-REQUIS: gpt-6.2-astra" in sortie, sortie)
    code, sortie, lances, messages = principal(["--role", "06.qualification", "--prompt-fichier", prompt,
                                                "--indisponible", "gpt-6.1-sol"])
    controle("sans accord et sans Codex : pause, code 10", code == 10 and not lances, sortie)

    code, sortie, _, _ = principal(["--accorder", "gpt-6.2-astra", "--nombre", "1"], env={"USINE_ROLE": "05.codeur"})
    controle("un agent de l'usine ne peut pas s'accorder de quota : code 7", code == 7 and not d.accords_valides(routage), sortie)
    code, sortie, _, _ = principal(["--accorder", "gpt-6.1-sol"])
    controle("accorder un modèle qui n'est pas sur accord : code 2", code == 2, sortie)
    code, sortie, _, _ = principal(["--accorder", "gpt-6.2-astra", "--nombre", "2", "--heures", "1"])
    controle("accord du propriétaire : écrit, demande close", code == 0 and d.accords_valides(routage)["gpt-6.2-astra"]["restant"] == 2
             and "gpt-6.2-astra" not in d.lire_json_local(os.path.join(tmp, "JOURNAUX", "demandes-quota.json")), sortie)
    c, rang, _ = d.choisir(routage, "07.revue-diff", pour_lancer=False)
    controle("avec accord : Astra 6.2 choisi", c["modele"] == "gpt-6.2-astra" and rang == 0)
    c, _, _ = d.choisir(routage, "07.revue-diff", pour_lancer=False, horloge=lambda: time.time() + 2 * 3600)
    controle("accord expiré : repli Codex", c["modele"] == "gpt-6.1-sol")
    controle("Opus toujours sans accord", d.choisir(routage, "06.qualification", pour_lancer=False)[0]["modele"] == "gpt-6.2-astra")

    with patch.object(d.subprocess, "Popen", side_effect=AssertionError("aucun lancement attendu")):
        r = d.lancer(routage, "06.qualification", roles["06.qualification"]["candidats"][0], 0, "p", "", "", 1)
    controle("dernier verrou : lancer() refuse Opus sans accord, sans rien lancer", r["code_cli"] == 10 and r.get("sans_accord"))
    controle("chaque lancement consomme l'accord", d.consommer_accord(routage, "gpt-6.2-astra")
             and d.accords_valides(routage)["gpt-6.2-astra"]["restant"] == 1)

    refus = {"code_cli": 10, "verdict": None, "ligne": "", "duree_s": 0, "final": "", "journal": os.path.join(tmp, "x"),
             "expire": False, "fige": False, "sans_message": True, "sans_accord": True}
    code, sortie, lances, _ = principal(["--role", "03.adversaire", "--prompt-fichier", prompt], retours=[refus])
    controle("accord épuisé entre le choix et le lancement : repli Codex, Opus jamais lancé",
             code == 0 and lances == ["gpt-6.2-astra", "gpt-6.1-sol"] and "SANS-ACCORD:" in sortie, sortie)

    code, sortie, _, _ = principal(["--role", "03.calcul", "--format", "t3", "--prompt-fichier", prompt])
    charge = json.loads(sortie[sortie.index("{"):])
    controle("T3 avec accord : charge utile Astra 6.2, accord consommé",
             code == 3 and charge["target"]["model"] == "gpt-6.2-astra" and "gpt-6.2-astra" not in d.accords_valides(routage), sortie)
    code, sortie, _, messages = principal(["--role", "03.calcul", "--format", "t3", "--prompt-fichier", prompt])
    controle("T3 accord épuisé : charge utile Codex et nouvelle demande",
             json.loads(sortie[sortie.index("{"):])["target"]["model"] == "gpt-6.1-sol"
             and [m[2] for m in messages] == ["quota-gpt-6.2-astra"], sortie)

    with patch.object(d.shutil, "which", return_value="devin"):
        cmd = d.commande_cli(routage, roles["05.codeur"]["candidats"][0], "dernier.txt")
    controle("commande SWE 2.1 : modèle et effort, prompt par l'entrée standard",
             cmd == ["devin", "-p", "--model", "swe-2.1", "--effort", "high", "--output-format", "text"], " ".join(cmd))

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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôles du tableau de bord, en arborescence temporaire : aucun modèle, aucun réseau extérieur."""
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import threading
import urllib.error
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("tableau", os.path.join(ICI, "tableau-de-bord.py"))
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)

echecs = 0


def controle(nom, condition, detail=""):
    global echecs
    if condition:
        print("ok     " + nom)
    else:
        echecs += 1
        print("ECHEC  " + nom + ((" : " + str(detail)[:300]) if detail else ""))


def ecrire(racine, chemin, texte):
    f = os.path.join(racine, *chemin.split("/"))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    with io.open(f, "w", encoding="utf-8") as h:
        h.write(texte)
    return f


with tempfile.TemporaryDirectory() as tmp:
    r = os.path.join(tmp, "usine")
    shutil.copytree(os.path.join(t.RACINE, "CONNAISSANCES"), os.path.join(r, "CONNAISSANCES"))
    shutil.copy(os.path.join(t.RACINE, "ALERTES.md"), r)
    ecrire(r, "JEUX/essai/ETAT.json", "\ufeff" + json.dumps({
        "slug": "essai", "nom": "Essai", "etape": "04-fun", "statut": "bloque", "blocage": "attend Opus",
        "portes": {"P0": {"resultat": "derogation", "note": "n0"}, "P1": {"resultat": "passe"},
                   "P2": {"resultat": "echec", "iterations": 1, "preuve": "JEUX\\essai\\03-economie\\R.md"}},
        "historique": [{"date": "2026-11-20 10:00", "evenement": "porte P1 : passe"}], "mode_degrade": ["x"]}))
    ecrire(r, "JEUX/essai/JOURNAL.md", "| Date | Etape | Agent | Duree | Resultat | Fichier |\n|---|---|---|---|---|---|\n| 2026-11-20 | 03-economie | codex | 3 min | echec | R.md |\n")
    ecrire(r, "JEUX/essai/03-economie/R.md", "rapport")
    ecrire(r, "JEUX/casse/ETAT.json", "{pas du json")
    ecrire(r, "JOURNAUX/cycles.log",
           "2026-11-20T10:00:00Z | tour 1/8 | claude claude-opus-5-5 | 600 s | continuer | essai, 03\n"
           "2026-11-20T10:10:00Z | tour 2/8 | claude claude-opus-5-5 | 300 s | bloque | essai, 04, attend Opus\n"
           "ligne illisible\n"
           "2026-11-21T09:00:00Z | tour 1/2 | codex gpt-6.1-sol | 60 s | termine | fini\n")
    ecrire(r, "JOURNAUX/battement.log", "2026-11-21T08:00:00+00:00 | DECISION: lancer | fais un jeu | essai en cours\n"
                                        "2026-11-21T08:00:01+00:00 | notification important | code 0\n")
    ecrire(r, "JOURNAUX/delegations.csv", "debut_utc;jeu;role;fournisseur;modele;effort;rang;duree_s;code;resultat;titre\n"
                                         "2026-11-20T10:01:00Z;essai;03.calcul;codex;gpt-6.1-sol;xhigh;0;180;1;echec;calcul\n")
    fiche_morte = ecrire(r, "JOURNAUX/agents/mort.json", json.dumps({"id": "mort", "pid": 99999999, "role": "03.calcul", "claude_fort": False}))
    ecrire(r, "JOURNAUX/agents/vif.json", json.dumps({"id": "vif", "pid": os.getpid(), "role": "04.relecteur-fun",
                                                      "modele": "claude-opus-5-5", "claude_fort": True}))
    ecrire(r, "JOURNAUX/agents/vif.log", "sortie de l'agent\nsk-" + "ant-" + "A" * 30 + "\n")
    ecrire(r, "VERROUS/studio.lock", json.dumps({"ressource": "studio", "agent": "a", "depuis": "2026-11-20T10:00:00Z", "expire": "2000-01-01T00:00:00Z"}))
    ecrire(r, "secret.md", "hors des dossiers lisibles")
    ecrire(r, "JOURNAUX/storageState-roblox.json", '{"cookies": []}')
    ecrire(r, "JOURNAUX/session-chrome.json", '{"jeton": "x"}')

    e = t.instantane(r)
    jeu = {j["slug"]: j for j in e["jeux"]}
    controle("deux jeux lus, dont un ETAT.json illisible signalé sans planter", set(jeu) == {"essai", "casse"} and "illisible" in jeu["casse"])
    es = jeu["essai"]
    statuts = {x["id"]: x["statut"] for x in es["etapes"]}
    controle("chaîne : étapes faites, courante bloquée, à venir", statuts["03-economie"] == "faite" and statuts["04-fun"] == "bloquee" and statuts["05-production"] == "a_venir", statuts)
    portes = {p["porte"]: p for p in es["portes"]}
    controle("12 portes P0–P11, résultats et itérations d'ETAT.json", len(portes) == 12 and portes["P2"]["resultat"] == "echec" and portes["P2"]["iterations"] == 1 and portes["P5"]["resultat"] == "non_jugee")
    controle("preuve en chemin portable", portes["P2"]["preuve"] == "JEUX/essai/03-economie/R.md")
    controle("journal du jeu et livrables lus", len(es["journal"]) == 1 and "JEUX/essai/03-economie/R.md" in es["fichiers"])
    c = e["cycles"]["cycles"]
    controle("cycles.log regroupé en 2 cycles, le plus récent en tête", len(c) == 2 and c[0]["etat"] == "termine" and len(c[1]["tours"]) == 2 and c[1]["duree_s"] == 900, c)
    controle("battement : décision et événement", e["battement"]["decisions"][0]["decision"] == "lancer" and len(e["battement"]["evenements"]) == 1)
    a = e["agents"]
    controle("agents : vivant et mort distingués, Claude forts comptés", a["vivants"] == 1 and a["claude_forts_vivants"] == 1 and len(a["en_cours"]) == 2)
    controle("la fiche d'un agent mort n'est pas supprimée (lecture seule)", os.path.exists(fiche_morte))
    controle("délégations et rôles du routage lus", len(a["delegations"]) == 1 and any(x["role"] == "00.orchestrateur" for x in a["roles"]))
    controle("alertes de ALERTES.md lues avec leur statut", len(e["alertes"]) >= 1 and e["alertes_ouvertes"] == sum(1 for x in e["alertes"] if x["ouverte"]))
    controle("verrou expiré signalé", e["verrous"][0]["expire_deja"] is True)
    controle("journaux listés", any(j["fichier"] == "JOURNAUX/cycles.log" for j in e["journaux"]) and any(j["fichier"] == "JEUX/essai/JOURNAL.md" for j in e["journaux"]))
    controle("STOP absent", e["stop"] is False)
    ecrire(r, "STOP", "")
    controle("STOP présent vu", t.instantane(r)["stop"] is True)

    s = t.serveur(r, 0)
    port = s.server_address[1]
    threading.Thread(target=s.serve_forever, daemon=True).start()

    def get(chemin, hote=None, methode="GET"):
        q = urllib.request.Request("http://127.0.0.1:%d%s" % (port, chemin), method=methode)
        if hote:
            q.add_header("Host", hote)
        try:
            with urllib.request.urlopen(q, timeout=10) as rep:
                return rep.status, rep.read().decode("utf-8")
        except urllib.error.HTTPError as x:
            return x.code, x.read().decode("utf-8")

    code, corps = get("/")
    controle("page servie", code == 200 and "Usine Roblox" in corps)
    code, corps = get("/api/etat")
    controle("/api/etat en JSON", code == 200 and json.loads(corps)["jeux"])
    code, corps = get("/api/fichier?chemin=JOURNAUX/agents/vif.log")
    controle("fichier lu, secret masqué", code == 200 and "[masqué]" in corps and "AAAAAAAAAAAAAAAAAAAAAAAA" not in corps, corps)
    for mauvais in ("../" * 6 + "etc/passwd", "secret.md", "JEUX/../secret.md", "STOP", "VERROUS/studio.lock", "%2e%2e/%2e%2e/x.md",
                    "JOURNAUX/storageState-roblox.json", "JOURNAUX/session-chrome.json"):
        code, _ = get("/api/fichier?chemin=" + mauvais)
        controle("refusé : " + mauvais, code == 404)
    code, _ = get("/api/etat", hote="evil.example:%d" % port)
    controle("hôte étranger refusé (rebond DNS)", code == 403)
    code, _ = get("/api/etat", methode="POST")
    controle("écriture refusée (POST)", code == 405)
    s.shutdown()
    s.server_close()

    avant = sorted(os.path.relpath(os.path.join(d, f), r) for d, _, fs in os.walk(r) for f in fs)
    t.instantane(r)
    apres = sorted(os.path.relpath(os.path.join(d, f), r) for d, _, fs in os.walk(r) for f in fs)
    controle("aucun fichier créé ni supprimé par la lecture", avant == apres)

controle("deleguer.py chargé sans écrire de bytecode", sys.dont_write_bytecode is True)
controle("l'état de cette usine se lit sans erreur", t.instantane(t.RACINE)["jeux"] is not None)
print("%d échec(s)" % echecs)
sys.exit(1 if echecs else 0)

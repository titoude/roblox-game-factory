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
import time
import urllib.error
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("tableau", os.path.join(ICI, "tableau-de-bord.py"))
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)

echecs = 0
FAUX_USINE = """import os, sys, time
R = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
print("FAUX", a)
sys.stdout.flush()
if a == ["stop"]:
    open(os.path.join(R, "STOP"), "a").close()
elif a == ["reprendre"] and os.path.exists(os.path.join(R, "STOP")):
    os.remove(os.path.join(R, "STOP"))
elif a and "dormir" in a[0]:
    time.sleep(30)
sys.exit(3 if "--simuler" in a else 0)
"""


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
    s.shutdown()
    s.server_close()

    # Lecture seule : aucun pilotage, aucun jeton dans la page.
    s = t.serveur(r, 0, pilotage=False)
    port = s.server_address[1]
    threading.Thread(target=s.serve_forever, daemon=True).start()
    code, corps = get("/")
    controle("lecture seule : page sans jeton", code == 200 and "{{JETON}}" not in corps and 'name="jeton" content=""' in corps)
    controle("lecture seule : pas de pilotage dans l'état", json.loads(get("/api/etat")[1])["pilotage"] is None)
    code, _ = get("/api/action", methode="POST")
    controle("lecture seule : POST refusé", code == 405)
    s.shutdown()
    s.server_close()

    # Pilotage, avec un faux usine.py : aucun modèle n'est lancé.
    ecrire(r, "usine.py", FAUX_USINE)
    ecrire(r, "JOURNAUX/battement-etat.json", '{"evenements": ["e1"]}')
    s = t.serveur(r, 0)
    port = s.server_address[1]
    threading.Thread(target=s.serve_forever, daemon=True).start()
    page = get("/")[1]
    jeton = page.split('name="jeton" content="', 1)[1].split('"', 1)[0]
    controle("pilotage : jeton propre au lancement dans la page", len(jeton) >= 24 and jeton in page)

    def post(chemin, corps, jeton=jeton, origine=None, type_="application/json"):
        q = urllib.request.Request("http://127.0.0.1:%d%s" % (port, chemin), method="POST",
                                   data=json.dumps(corps).encode("utf-8"))
        q.add_header("Content-Type", type_)
        if jeton:
            q.add_header("X-Jeton", jeton)
        if origine:
            q.add_header("Origin", origine)
        try:
            with urllib.request.urlopen(q, timeout=10) as rep:
                return rep.status, json.loads(rep.read().decode("utf-8"))
        except urllib.error.HTTPError as x:
            return x.code, json.loads(x.read().decode("utf-8"))

    def attendre_fin(ident, limite=20):
        for _ in range(limite * 10):
            for x in json.loads(get("/api/etat")[1])["pilotage"]["taches"]:
                if x["id"] == ident and x["code"] is not None:
                    return x
            time.sleep(0.1)
        return None

    def reservation():
        return json.loads(io.open(os.path.join(r, "JOURNAUX", "battement-etat.json"), encoding="utf-8").read())

    controle("pilotage : sans jeton refusé", post("/api/action", {"action": "stop"}, jeton=None)[0] == 403)
    controle("pilotage : faux jeton refusé", post("/api/action", {"action": "stop"}, jeton="x" * 32)[0] == 403)
    controle("pilotage : origine étrangère refusée", post("/api/action", {"action": "stop"}, origine="http://evil.example")[0] == 403)
    controle("pilotage : corps non JSON refusé", post("/api/action", {"action": "stop"}, type_="text/plain")[0] == 415)
    controle("pilotage : action inconnue refusée", post("/api/action", {"action": "rm"})[0] == 400)
    code, d = post("/api/action", {"action": "verifier"})
    controle("pilotage : STOP présent, vérifier refusé (G0)", code == 409 and "STOP" in d["erreur"], d)
    code, d = post("/api/action", {"action": "reprendre"})
    fin = attendre_fin(d.get("id"))
    controle("pilotage : reprendre passe par usine.py et retire STOP",
             code == 202 and fin and fin["code"] == 0 and not os.path.exists(os.path.join(r, "STOP")), (code, d, fin))
    texte = io.open(os.path.join(r, *d["journal"].split("/")), encoding="utf-8").read()
    controle("pilotage : sortie journalisée dans JOURNAUX/tableau/", d["journal"].startswith("JOURNAUX/tableau/") and "FAUX ['reprendre']" in texte, texte)
    controle("pilotage : cycle sans accord du propriétaire refusé", post("/api/action", {"action": "cycle", "demande": "fais un jeu"})[0] == 400)
    controle("pilotage : retours sans accord refusé", post("/api/action", {"action": "retours", "slug": "essai"})[0] == 400)
    for mauvais in ({"action": "cycle", "accord_modeles": True, "demande": "--simuler"},
                    {"action": "cycle", "accord_modeles": True, "demande": "x", "tours": 99},
                    {"action": "cycle", "accord_modeles": "oui", "demande": "x"},
                    {"action": "retours", "accord_modeles": True, "slug": "../essai"}):
        controle("pilotage : demande invalide refusée %s" % json.dumps(mauvais, ensure_ascii=False), post("/api/action", mauvais)[0] == 400)
    code, d = post("/api/action", {"action": "cycle_simuler", "demande": "fais un jeu", "tours": 2})
    fin = attendre_fin(d.get("id"))
    controle("pilotage : cycle simulé lancé avec --simuler", code == 202 and fin and fin["code"] == 3 and "--simuler" in fin["commande"], (d, fin))
    code, d = post("/api/action", {"action": "cycle", "demande": "fais un jeu dormir", "tours": 2, "accord_modeles": True})
    res = reservation()
    controle("pilotage : cycle accordé lancé et réservé comme battement --lancer",
             code == 202 and res.get("lancement", {}).get("id") == d.get("id") and res.get("evenements") == ["e1"], (code, d, res))
    controle("pilotage : un seul cycle à la fois", post("/api/action", {"action": "cycle", "demande": "x", "accord_modeles": True})[0] == 409)
    controle("pilotage : retours refusés pendant un cycle", post("/api/action", {"action": "retours", "slug": "essai", "accord_modeles": True})[0] == 409)
    code2, _ = post("/api/interrompre", {"id": d.get("id")})
    fin = attendre_fin(d.get("id"))
    res = reservation()
    controle("pilotage : interruption, réservation libérée, le reste conservé",
             code2 == 200 and fin and fin["code"] != 0 and "lancement" not in res and res.get("evenements") == ["e1"], (fin, res))
    os.remove(os.path.join(r, "JOURNAUX", "battement-etat.json"))
    code, d = post("/api/action", {"action": "cycle", "demande": "fais un jeu dormir", "tours": 2, "accord_modeles": True})
    res = reservation()
    controle("pilotage : réservation sans état préalable lisible par battement.py",
             code == 202 and res.get("evenements") == [] and res.get("absents") == {} and "lancement" in res, (code, d, res))
    controle("pilotage : battement réel refusé pendant un cycle", post("/api/action", {"action": "battement"})[0] == 409)
    post("/api/interrompre", {"id": d.get("id")})
    attendre_fin(d.get("id"))
    ecrire(r, "JOURNAUX/battement-etat.json", '{"lancement": {"date": "x", "demande": "veille", "tours": 2}}')
    controle("pilotage : cycle refusé si battement --lancer a réservé", post("/api/action", {"action": "cycle", "demande": "x", "accord_modeles": True})[0] == 409)
    controle("pilotage : réservation d'un autre gardée", reservation()["lancement"]["demande"] == "veille")
    code, d = post("/api/action", {"action": "stop"})
    fin = attendre_fin(d.get("id"))
    controle("pilotage : STOP posé par usine.py", code == 202 and fin and os.path.exists(os.path.join(r, "STOP")))
    controle("pilotage : actions tracées dans actions.log",
             io.open(os.path.join(r, "JOURNAUX", "tableau", "actions.log"), encoding="utf-8").read().count("lancée") >= 4)
    controle("pilotage : interrompre un identifiant inconnu", post("/api/interrompre", {"id": "nul"})[0] == 404)
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

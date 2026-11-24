#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tableau-de-bord.py - interface locale de l'usine : consultation et pilotage.

Lit les vrais fichiers de l'usine (JEUX\\*\\ETAT.json, JOURNAUX\\, ALERTES.md, VERROUS\\, routage.json,
seuils.json) et les sert sur http://127.0.0.1:<port>/ : vue d'ensemble, jeux (étapes et portes),
cycles (tours d'orchestrateur et battements), agents (en cours, routage, délégations), journaux,
alertes et verrous. La lecture n'écrit rien. Le pilotage (STOP, reprendre, vérifier, battement, cycle,
retours) ne fait qu'appeler `python usine.py ...`, donc derrière STOP (G0), le plafond G2 et les verrous ;
un cycle (modèles) exige l'accord explicite du propriétaire et réserve sa place dans battement-etat.json.
Le tableau n'écrit lui-même que JOURNAUX/tableau/ et cette réservation. Aucun réseau extérieur.

  python usine.py tableau                       lance le serveur et ouvre le navigateur
  python OUTILS\\tableau-de-bord.py [--port 8765] [--sans-navigateur] [--lecture-seule] [--racine <dossier>]
  python OUTILS\\tableau-de-bord.py --instantane    imprime l'état en JSON et rend la main

Codes de sortie : 0 arrêt normal | 2 usage | 5 port occupé.
"""
import argparse
import csv
import datetime as dt
import glob
import importlib.util
import io
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tableau-de-bord.html")

ETAPES = [
    ("01-veille", "Veille", "01-VEILLE-NAVIGATEUR.md"),
    ("02-concept", "Concept", "02-CONCEPT.md"),
    ("03-economie", "Économie", "03-REVUE-ECONOMIE.md"),
    ("04-fun", "Fun", "04-REVUE-FUN.md"),
    ("05-production", "Production", "05-PRODUCTION-STUDIO.md"),
    ("06-qa", "QA", "06-QA-MULTIJOUEUR.md"),
    ("07-release", "Release", "07-RELEASE.md"),
    ("08-distribution", "Distribution", "08-DISTRIBUTION.md"),
    ("09-bilan", "Bilan", "09-BILAN.md"),
]
# Porte -> (étape où elle se juge, ce qu'elle ouvre, clé de seuils.json). Même table que etat.ps1.
PORTES = [
    ("P0", "01-veille", "Veille → Concept", "veille"),
    ("P1", "02-concept", "Concept → Économie", "concept"),
    ("P2", "03-economie", "Économie → Fun", "economie"),
    ("P3", "04-fun", "Fun → Production", "fun"),
    ("P4", "05-production", "Prototype (dans la production)", "prototype"),
    ("P5", "06-qa", "QA → Release", "qa"),
    ("P6", "07-release", "Release → Distribution", None),
    ("P7", "08-distribution", "Bêta → Pub", "beta"),
    ("P8", "08-distribution", "Pub → Montée", "pub"),
    ("P9", "09-bilan", "Bilan", None),
    ("P10", "08-distribution", "Retours joueurs (boucle)", "retours"),
    ("P11", "08-distribution", "Promotion (boucle)", "promo"),
]
DOSSIERS_LISIBLES = ("JOURNAUX", "JEUX", "CONNAISSANCES", "VEILLE", "PROCEDURES", "skills")
FICHIERS_LISIBLES = ("ALERTES.md", "GARDE-FOUS.md", "README.md", "README.fr.md", "AGENTS.md")
EXTENSIONS_LISIBLES = (".md", ".log", ".txt", ".csv", ".json", ".lua", ".luau")
EXCLUS = re.compile(r"(^|/)(\.git|brut|captures|__pycache__)(/|$)")
# G10 : aucun export de session navigateur (cookies, storageState, .ROBLOSECURITY), même rangé par erreur ici.
SESSIONS = re.compile(r"(?i)(storage.?state|cookie|roblosecurity|^\.env|session[^/]*\.json$)")
TAILLE_MAX = 400 * 1024


def charger_deleguer():
    sys.dont_write_bytecode = True  # lecture seule : pas de __pycache__ dans l'usine
    spec = importlib.util.spec_from_file_location("deleguer_tdb", os.path.join(RACINE, "OUTILS", "deleguer.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_deleguer = None


def deleguer():
    global _deleguer
    if _deleguer is None:
        _deleguer = charger_deleguer()
    return _deleguer


def masquer(texte):
    """Remplace tout ce qui ressemble à un secret (motifs G9 de deleguer.py)."""
    for motif in deleguer().MOTIFS_SECRETS:
        texte = re.sub(motif, "[masqué]", texte, flags=re.IGNORECASE)
    return texte


def lire_texte(chemin):
    with io.open(chemin, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def lire_json(chemin):
    return json.loads(lire_texte(chemin))


def mtime(chemin):
    try:
        return dt.datetime.fromtimestamp(os.path.getmtime(chemin), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except OSError:
        return None


def rel(racine, chemin):
    return os.path.relpath(chemin, racine).replace(os.sep, "/")


def tableau_md(texte, colonnes=None):
    """Lignes d'un tableau Markdown (hors en-tête et séparateur), en listes de cellules."""
    lignes = []
    for ligne in texte.splitlines():
        l = ligne.strip()
        if not l.startswith("|"):
            continue
        cellules = [c.strip() for c in l.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cellules if c):
            continue
        if colonnes and len(cellules) != colonnes:
            continue
        lignes.append(cellules)
    return lignes[1:] if lignes else []


# ---------- Jeux ----------

def chaine(etat):
    courante = etat.get("etape") or ""
    ids = [e[0] for e in ETAPES]
    rang = ids.index(courante) if courante in ids else -1
    portes = etat.get("portes") or {}
    etapes = []
    for i, (ident, nom, proc) in enumerate(ETAPES):
        if rang < 0:
            statut = "inconnue"
        elif i < rang:
            statut = "faite"
        elif i == rang:
            statut = {"bloque": "bloquee", "arrete": "arretee", "termine": "faite"}.get(etat.get("statut"), "en_cours")
        else:
            statut = "a_venir"
        etapes.append({"id": ident, "nom": nom, "procedure": "PROCEDURES/" + proc, "statut": statut,
                       "portes": [p[0] for p in PORTES if p[1] == ident]})
    liste = []
    for nom, etape, but, cle in PORTES:
        p = portes.get(nom) or {}
        liste.append({"porte": nom, "etape": etape, "but": but, "seuils": cle,
                      "resultat": p.get("resultat") or "non_jugee", "date": p.get("date", ""),
                      "preuve": (p.get("preuve") or "").replace("\\", "/"), "note": p.get("note", ""),
                      "iterations": p.get("iterations", 0)})
    return etapes, liste


def jeux(racine):
    resultat = []
    for f in sorted(glob.glob(os.path.join(racine, "JEUX", "*", "ETAT.json"))):
        dossier = os.path.dirname(f)
        slug = os.path.basename(dossier)
        try:
            e = lire_json(f)
        except Exception as x:
            resultat.append({"slug": slug, "illisible": "%s: %s" % (type(x).__name__, x), "fichier": rel(racine, f)})
            continue
        etapes, portes = chaine(e)
        journal = os.path.join(dossier, "JOURNAL.md")
        lignes_journal = tableau_md(lire_texte(journal)) if os.path.isfile(journal) else []
        fichiers = []
        for ident, _, _ in ETAPES:
            d = os.path.join(dossier, ident)
            if os.path.isdir(d):
                fichiers += [rel(racine, x) for x in sorted(glob.glob(os.path.join(d, "*")))
                             if os.path.isfile(x) and x.endswith(EXTENSIONS_LISIBLES)]
        resultat.append({
            "slug": e.get("slug", slug), "nom": e.get("nom", slug), "cree_le": e.get("cree_le", ""),
            "etape": e.get("etape", ""), "statut": e.get("statut", ""), "blocage": e.get("blocage", ""),
            "place": e.get("place", {}), "mode_degrade": e.get("mode_degrade", []),
            "historique": e.get("historique", []), "etapes": etapes, "portes": portes,
            "journal": [dict(zip(["date", "etape", "agent", "duree", "resultat", "fichier"], l)) for l in lignes_journal if len(l) >= 6],
            "fichiers": fichiers, "fichier": rel(racine, f), "maj": mtime(f), "brut": e,
        })
    return resultat


# ---------- Cycles ----------

def cycles(racine):
    """JOURNAUX/cycles.log (usine.py) regroupé en cycles : un cycle commence à chaque « tour 1/N »."""
    chemin = os.path.join(racine, "JOURNAUX", "cycles.log")
    tours = []
    if os.path.isfile(chemin):
        for ligne in lire_texte(chemin).splitlines():
            m = re.match(r"\s*(\S+)\s*\|\s*tour (\d+)/(\d+)\s*\|\s*(.*?)\s*\|\s*(\d+) s\s*\|\s*(\w+)\s*\|\s*(.*)$", ligne)
            if not m:
                continue
            fournisseur, _, modele = m.group(4).partition(" ")
            tours.append({"date": m.group(1), "tour": int(m.group(2)), "tours": int(m.group(3)),
                          "fournisseur": fournisseur, "modele": modele, "duree_s": int(m.group(5)),
                          "etat": m.group(6), "raison": masquer(m.group(7))})
    groupes = []
    for t in tours:
        if t["tour"] == 1 or not groupes:
            groupes.append({"debut": t["date"], "tours": []})
        groupes[-1]["tours"].append(t)
    for g in groupes:
        g["fin"] = g["tours"][-1]["date"]
        g["etat"] = g["tours"][-1]["etat"]
        g["duree_s"] = sum(t["duree_s"] for t in g["tours"])
    return {"fichier": "JOURNAUX/cycles.log", "existe": os.path.isfile(chemin), "cycles": list(reversed(groupes))}


def battements(racine):
    chemin = os.path.join(racine, "JOURNAUX", "battement.log")
    decisions, evenements = [], []
    if os.path.isfile(chemin):
        for ligne in lire_texte(chemin).splitlines():
            date, _, reste = ligne.partition(" | ")
            m = re.match(r"DECISION:\s*(\w+)\s*\|\s*(.*?)\s*\|\s*(.*)$", reste)
            if m:
                decisions.append({"date": date, "decision": m.group(1), "demande": m.group(2), "raison": masquer(m.group(3))})
            elif reste:
                evenements.append({"date": date, "texte": masquer(reste)})
    etat = os.path.join(racine, "JOURNAUX", "battement-etat.json")
    try:
        e = lire_json(etat) if os.path.isfile(etat) else {}
    except Exception:
        e = {}
    return {"fichier": "JOURNAUX/battement.log", "existe": os.path.isfile(chemin),
            "decisions": list(reversed(decisions[-200:])), "evenements": list(reversed(evenements[-200:])),
            "notifications_vues": len(e.get("evenements", []))}


# ---------- Agents ----------

def agents(racine):
    """Fiches JOURNAUX/agents/*.json, lues sans jamais en supprimer (deleguer.py purge les mortes lui-même)."""
    dos = os.path.join(racine, "JOURNAUX", "agents")
    en_cours = []
    for f in sorted(glob.glob(os.path.join(dos, "*.json"))):
        try:
            fiche = lire_json(f)
        except Exception:
            continue
        fiche["vivant"] = bool(deleguer().pid_vivant(fiche.get("pid")))
        log = os.path.join(dos, fiche.get("id", "") + ".log")
        fiche["journal"] = rel(racine, log) if os.path.isfile(log) else ""
        fiche["derniere_ecriture"] = mtime(log) if os.path.isfile(log) else None
        en_cours.append(fiche)
    sorties = []
    for f in sorted(glob.glob(os.path.join(dos, "*.log")), key=os.path.getmtime, reverse=True)[:50]:
        sorties.append({"fichier": rel(racine, f), "maj": mtime(f), "taille": os.path.getsize(f)})
    delegations = []
    chemin = os.path.join(racine, "JOURNAUX", "delegations.csv")
    if os.path.isfile(chemin):
        with io.open(chemin, encoding="utf-8-sig", newline="") as h:
            delegations = [dict(r) for r in csv.DictReader(h, delimiter=";")]
        for d in delegations:
            d["titre"] = masquer(d.get("titre") or "")
    roles = []
    plafond = None
    try:
        routage = lire_json(os.path.join(racine, "CONNAISSANCES", "routage.json"))
        plafond = routage.get("plafond_claude_forts_simultanes")
        forts = set(routage.get("classes", {}).get("claude_fort", []))
        for nom, r in routage.get("roles", {}).items():
            roles.append({"role": nom, "but": r.get("but", ""), "duree_max_min": r.get("duree_max_min"),
                          "candidats": [dict(c, claude_fort=c.get("modele") in forts) for c in r.get("candidats", [])]})
    except Exception as x:
        roles = [{"role": "routage.json illisible", "but": str(x), "candidats": []}]
    vivants = [a for a in en_cours if a["vivant"]]
    return {"en_cours": en_cours, "vivants": len(vivants),
            "claude_forts_vivants": sum(1 for a in vivants if a.get("claude_fort")),
            "plafond_claude_forts": plafond, "sorties": sorties,
            "delegations": list(reversed(delegations[-500:])), "roles": roles}


# ---------- Alertes, verrous, journaux ----------

def alertes(racine):
    chemin = os.path.join(racine, "ALERTES.md")
    if not os.path.isfile(chemin):
        return []
    cles = ["date", "type", "agent", "jeu", "etape", "constat", "statut"]
    return [dict(zip(cles, l), ouverte=l[-1] == "ouverte") for l in tableau_md(lire_texte(chemin), 7)]


def verrous(racine):
    resultat = []
    maintenant = dt.datetime.now(dt.timezone.utc)
    for f in sorted(glob.glob(os.path.join(racine, "VERROUS", "*.lock"))):
        try:
            v = lire_json(f)
            expire = dt.datetime.fromisoformat(str(v.get("expire", "")).replace("Z", "+00:00"))
            if expire.tzinfo is None:
                expire = expire.replace(tzinfo=dt.timezone.utc)
            v["expire_deja"] = expire < maintenant
        except Exception:
            v = {"ressource": os.path.basename(f), "illisible": True}
        resultat.append(v)
    return resultat


def journaux(racine):
    liste = []
    for f in glob.glob(os.path.join(racine, "JOURNAUX", "**", "*"), recursive=True):
        if os.path.isfile(f) and f.endswith(EXTENSIONS_LISIBLES):
            liste.append({"fichier": rel(racine, f), "maj": mtime(f), "taille": os.path.getsize(f), "groupe": "JOURNAUX"})
    for f in glob.glob(os.path.join(racine, "JEUX", "*", "JOURNAL.md")) + glob.glob(os.path.join(racine, "JEUX", "*", "05-production", "JOURNAL-LOTS.md")):
        liste.append({"fichier": rel(racine, f), "maj": mtime(f), "taille": os.path.getsize(f), "groupe": "Jeux"})
    for nom in ("ALERTES.md", "CONNAISSANCES/JOURNAL-DES-JEUX.md", "CONNAISSANCES/CHANTIERS.md"):
        f = os.path.join(racine, nom)
        if os.path.isfile(f):
            liste.append({"fichier": nom, "maj": mtime(f), "taille": os.path.getsize(f), "groupe": "Usine"})
    liste.sort(key=lambda x: x["maj"] or "", reverse=True)
    return liste


def connaissances(racine):
    def lister(motif):
        return [{"fichier": rel(racine, f), "maj": mtime(f)} for f in sorted(glob.glob(os.path.join(racine, motif)))
                if os.path.isfile(f) and not f.endswith("LISEZ-MOI.md")]
    return {"propositions": lister("CONNAISSANCES/PROPOSITIONS/*.md"),
            "propositions_traitees": len(glob.glob(os.path.join(racine, "CONNAISSANCES", "PROPOSITIONS", "traitees", "*.md"))),
            "bilans": lister("CONNAISSANCES/BILANS/*.md"),
            "releves": sorted(os.path.basename(d) for d in glob.glob(os.path.join(racine, "VEILLE", "RELEVES", "*")) if os.path.isdir(d))}


def git_tete(racine):
    try:
        tete = lire_texte(os.path.join(racine, ".git", "HEAD")).strip()
        if tete.startswith("ref: "):
            ref = tete[5:]
            f = os.path.join(racine, ".git", *ref.split("/"))
            sha = lire_texte(f).strip() if os.path.isfile(f) else ""
            if not sha and os.path.isfile(os.path.join(racine, ".git", "packed-refs")):
                for l in lire_texte(os.path.join(racine, ".git", "packed-refs")).splitlines():
                    if l.endswith(" " + ref):
                        sha = l.split()[0]
            return {"branche": ref.rsplit("/", 1)[-1], "commit": sha[:7]}
        return {"branche": "(détachée)", "commit": tete[:7]}
    except Exception:
        return {"branche": "", "commit": ""}


def instantane(racine=RACINE):
    j = jeux(racine)
    a = agents(racine)
    al = alertes(racine)
    try:
        seuils = lire_json(os.path.join(racine, "CONNAISSANCES", "seuils.json"))
    except Exception:
        seuils = {}
    return {
        "genere": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "racine": racine, "stop": os.path.exists(os.path.join(racine, "STOP")), "git": git_tete(racine),
        "jeux": j, "cycles": cycles(racine), "battement": battements(racine), "agents": a,
        "alertes": al, "alertes_ouvertes": sum(1 for x in al if x["ouverte"]), "verrous": verrous(racine),
        "journaux": journaux(racine), "connaissances": connaissances(racine),
        "etapes": [{"id": e[0], "nom": e[1]} for e in ETAPES],
        "seuils": seuils,
    }


def chemin_autorise(racine, demande):
    """Chemin absolu d'un fichier texte lisible, ou None (hors racine, dossier non prévu, extension, taille)."""
    if not demande or "\x00" in demande:
        return None
    demande = demande.replace("\\", "/").lstrip("/")
    if EXCLUS.search(demande) or SESSIONS.search(demande.rsplit("/", 1)[-1]):
        return None
    absolu = os.path.realpath(os.path.join(racine, demande))
    base = os.path.realpath(racine)
    if os.path.commonpath([absolu, base]) != base:
        return None
    relatif = rel(base, absolu)
    if not (relatif in FICHIERS_LISIBLES or relatif.split("/")[0] in DOSSIERS_LISIBLES):
        return None
    if not absolu.endswith(EXTENSIONS_LISIBLES) or not os.path.isfile(absolu):
        return None
    return absolu


def lire_fichier(racine, demande, queue=False):
    absolu = chemin_autorise(racine, demande)
    if absolu is None:
        return None
    taille = os.path.getsize(absolu)
    with io.open(absolu, "rb") as f:
        if taille > TAILLE_MAX:
            if queue:
                f.seek(taille - TAILLE_MAX)
            donnees = f.read(TAILLE_MAX)
        else:
            donnees = f.read()
    texte = donnees.decode("utf-8-sig", errors="replace")
    return {"fichier": rel(os.path.realpath(racine), absolu), "taille": taille, "tronque": taille > TAILLE_MAX,
            "maj": mtime(absolu), "texte": masquer(texte)}



# ---------- Pilotage ----------
# Chaque action passe par usine.py, donc par ses règles : STOP (G0), plafond G2 et verrous appliqués par
# deleguer.py et l'orchestrateur. Le tableau n'écrit lui-même que JOURNAUX/tableau/ (sortie des actions)
# et, pour un cycle, la réservation « lancement » de battement-etat.json (celle de battement.py --lancer).

ACTIONS = {
    # nom : (libellé, arguments usine.py, lance des modèles, autorisée sous STOP)
    "stop": ("Poser STOP (tout geler)", ["stop"], False, True),
    "reprendre": ("Retirer STOP (reprendre)", ["reprendre"], False, True),
    "verifier": ("Auto-contrôle de l'usine", ["verifier"], False, False),
    "battement_simuler": ("Battement simulé (rien n'est écrit)", ["battement", "--simuler"], False, False),
    "battement": ("Battement (mesures, messages, décision ; aucun modèle)", ["battement"], False, False),
    "cycle_simuler": ("Cycle simulé (montre ce qui serait lancé)", None, False, False),
    "cycle": ("Lancer un cycle d'orchestrateur", None, True, False),
    "retours": ("Boucle des retours joueurs d'un jeu", None, True, False),
}
DEMANDE_OK = re.compile(r"^[^\x00-\x1f\"]{1,200}$")
SLUG_OK = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def arreter_arbre(proc):
    """Arrête usine.py et ses enfants (CLI de l'orchestrateur, agents délégués)."""
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, check=False)
        else:
            import signal
            os.killpg(proc.pid, signal.SIGTERM)
    except OSError:
        proc.terminate()


class Pilote:
    def __init__(self, racine):
        self.racine = racine
        self.jeton = secrets.token_urlsafe(24)
        self.taches = []
        self.verrou = threading.Lock()

    def en_cours(self):
        return [t for t in self.taches if t["code"] is None]

    def chemin_reservation(self):
        return os.path.join(self.racine, "JOURNAUX", "battement-etat.json")

    def lire_reservation(self):
        try:
            e = lire_json(self.chemin_reservation())
            return e if isinstance(e, dict) else {}
        except FileNotFoundError:
            return {}

    def cycle_externe(self):
        """Un cycle lancé hors du tableau (battement --lancer) réserve sa place dans battement-etat.json."""
        try:
            return bool(self.lire_reservation().get("lancement"))
        except Exception:
            return True  # illisible : prudence, comme battement.py

    def ecrire_reservation(self, etat):
        chemin = self.chemin_reservation()
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        provisoire = chemin + ".tableau.tmp"
        with io.open(provisoire, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(etat, ensure_ascii=False, indent=2) + "\n")
        os.replace(provisoire, chemin)

    def reserver(self, t, args):
        # Même réservation durable que battement.py --lancer : tant qu'elle existe, le battement ne lance rien.
        e = self.lire_reservation()
        e["lancement"] = {"date": t["debut"], "demande": args[1] if args[0] == "retours" else args[0], "tours": int(args[2]) if len(args) > 2 else 2,
                          "origine": "tableau de bord", "id": t["id"]}
        self.ecrire_reservation(e)

    def liberer(self, t):
        try:
            e = self.lire_reservation()
            if (e.get("lancement") or {}).get("id") == t["id"]:
                del e["lancement"]
                self.ecrire_reservation(e)
        except Exception as x:
            self.tracer(t, "réservation non libérée (%s) : voir battement-etat.json" % type(x).__name__)

    def commande(self, nom, corps):
        libelle, args, modeles, sous_stop = ACTIONS[nom]
        if args is not None:
            return list(args), libelle
        if nom == "retours":
            slug = str(corps.get("slug") or "")
            if not SLUG_OK.match(slug) or not os.path.isfile(os.path.join(self.racine, "JEUX", slug, "ETAT.json")):
                raise ValueError("jeu inconnu")
            return ["retours", slug], "%s : %s" % (libelle, slug)
        demande = str(corps.get("demande") or "fais un jeu").strip()
        if not DEMANDE_OK.match(demande) or demande.startswith("-"):
            raise ValueError("demande refusée")
        try:
            tours = int(corps.get("tours") or 8)
        except (TypeError, ValueError):
            raise ValueError("tours invalide")
        if not 1 <= tours <= 20:
            raise ValueError("tours entre 1 et 20")
        args = [demande, "--tours", str(tours)] + (["--simuler"] if nom == "cycle_simuler" else [])
        return args, "%s : « %s », %d tour(s)" % (libelle, demande, tours)

    def lancer(self, corps):
        nom = corps.get("action")
        if nom not in ACTIONS:
            return 400, {"erreur": "action inconnue"}
        libelle, _, modeles, sous_stop = ACTIONS[nom]
        if os.path.exists(os.path.join(self.racine, "STOP")) and not sous_stop:
            return 409, {"erreur": "STOP présent (G0) : retirer STOP avant d'agir"}
        if modeles and corps.get("accord_modeles") is not True:
            return 400, {"erreur": "accord du propriétaire sur les modèles requis (Opus 5.5 et Astra 6.2 compris)"}
        try:
            args, titre = self.commande(nom, corps)
        except ValueError as x:
            return 400, {"erreur": str(x)}
        with self.verrou:
            occupe = [t for t in self.en_cours() if t["action"] not in ("stop", "reprendre")]
            if nom not in ("stop", "reprendre"):
                if modeles and (any(ACTIONS[t["action"]][2] for t in occupe) or self.cycle_externe()):
                    return 409, {"erreur": "un cycle tourne déjà : une seule usine à la fois"}
                if any(t["action"] == nom for t in occupe):
                    return 409, {"erreur": "cette action tourne déjà"}
            maintenant = dt.datetime.now(dt.timezone.utc)
            ident = "%s-%s-%d" % (maintenant.strftime("%Y%m%dT%H%M%SZ"), nom, len(self.taches) + 1)
            dossier = os.path.join(self.racine, "JOURNAUX", "tableau")
            os.makedirs(dossier, exist_ok=True)
            journal = os.path.join(dossier, ident + ".log")
            commande = [sys.executable, os.path.join(self.racine, "usine.py")] + args
            t = {"id": ident, "action": nom, "titre": titre, "commande": "python usine.py " + " ".join(
                 ('"%s"' % x if " " in x else x) for x in args), "debut": maintenant.strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "fin": None, "code": None, "journal": rel(self.racine, journal), "modeles": modeles, "pid": None}
            sortie = io.open(journal, "w", encoding="utf-8")
            sortie.write("# %s\n# %s\n# lancé depuis le tableau de bord le %s\n\n" % (titre, t["commande"], t["debut"]))
            sortie.flush()
            env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
            if modeles:
                self.reserver(t, args)
            groupe = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt"
                      else {"start_new_session": True})
            try:
                proc = subprocess.Popen(commande, cwd=self.racine, stdout=sortie, stderr=subprocess.STDOUT,
                                        stdin=subprocess.DEVNULL, env=env, **groupe)
            except OSError as x:
                sortie.close()
                if modeles:
                    self.liberer(t)
                return 500, {"erreur": "lancement impossible : %s" % x}
            t["pid"] = proc.pid
            t["_proc"] = proc
            self.taches.append(t)
            threading.Thread(target=self.attendre, args=(t, proc, sortie), daemon=True).start()
            self.tracer(t, "lancée")
        return 202, self.public(t)

    def attendre(self, t, proc, sortie):
        code = proc.wait()
        sortie.write("\n# fin : code %d\n" % code)
        sortie.close()
        if t["modeles"]:
            self.liberer(t)
        t["fin"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        t["code"] = code
        self.tracer(t, "finie, code %d" % code)

    def interrompre(self, ident):
        for t in self.en_cours():
            if t["id"] == ident:
                arreter_arbre(t["_proc"])
                self.tracer(t, "interrompue depuis le tableau")
                return 200, self.public(t)
        return 404, {"erreur": "aucune action en cours avec cet identifiant"}

    def tracer(self, t, quoi):
        with io.open(os.path.join(self.racine, "JOURNAUX", "tableau", "actions.log"), "a", encoding="utf-8") as f:
            f.write("%s | %s | %s | %s\n" % (dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                             t["action"], quoi, t["commande"]))

    @staticmethod
    def public(t):
        return {k: v for k, v in t.items() if not k.startswith("_")}

    def etat(self):
        orchestrateur = []
        try:
            r = lire_json(os.path.join(self.racine, "CONNAISSANCES", "routage.json"))
            role = (r.get("roles") or {}).get("00.orchestrateur") or {}
            orchestrateur = ["%s %s" % (c.get("fournisseur", ""), c.get("modele", "")) for c in role.get("candidats", [])]
        except Exception:
            pass
        return {"actions": [{"id": k, "libelle": v[0], "modeles": v[2], "sous_stop": v[3]} for k, v in ACTIONS.items()],
                "taches": [self.public(t) for t in reversed(self.taches)],
                "cycle_externe": self.cycle_externe(), "orchestrateur": orchestrateur}

# ---------- Serveur ----------

def fabrique(racine, pilote=None):
    class Gestionnaire(BaseHTTPRequestHandler):
        server_version = "UsineTableau/1"

        def log_message(self, *args):
            pass

        def envoyer(self, code, corps, type_="application/json; charset=utf-8"):
            if isinstance(corps, str):
                corps = corps.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", type_)
            self.send_header("Content-Length", str(len(corps)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'")
            self.end_headers()
            self.wfile.write(corps)

        def json(self, code, objet):
            self.envoyer(code, json.dumps(objet, ensure_ascii=False))

        def do_GET(self):
            # Refuse un nom d'hôte étranger : une page web ne peut pas lire l'usine par rebond DNS.
            if not self.hote_local():
                return self.json(403, {"erreur": "hôte refusé"})
            u = urlsplit(self.path)
            q = parse_qs(u.query)
            if u.path in ("/", "/index.html"):
                page = lire_texte(PAGE).replace("{{JETON}}", pilote.jeton if pilote else "")
                return self.envoyer(200, page, "text/html; charset=utf-8")
            if u.path == "/api/etat":
                e = instantane(racine)
                e["pilotage"] = pilote.etat() if pilote else None
                return self.json(200, e)
            if u.path == "/api/fichier":
                r = lire_fichier(racine, (q.get("chemin") or [""])[0], queue=(q.get("queue") or ["0"])[0] == "1")
                return self.json(200, r) if r else self.json(404, {"erreur": "fichier introuvable ou non lisible ici"})
            return self.json(404, {"erreur": "inconnu"})

        def hote_local(self):
            # Refuse un nom d'hôte étranger : une page web ne peut pas lire l'usine par rebond DNS.
            hote = (self.headers.get("Host") or "").rsplit(":", 1)[0].strip("[]")
            return hote in ("127.0.0.1", "localhost", "::1")

        def do_POST(self):
            if pilote is None:
                return self.json(405, {"erreur": "lecture seule"})
            if not self.hote_local():
                return self.json(403, {"erreur": "hôte refusé"})
            # Jeton propre à ce lancement, présent seulement dans la page servie : une autre page web
            # ne peut ni le lire ni envoyer cet en-tête sans requête préalable que le serveur refuse.
            origine = self.headers.get("Origin")
            if origine and urlsplit(origine).hostname not in ("127.0.0.1", "localhost", "::1"):
                return self.json(403, {"erreur": "origine refusée"})
            if not secrets.compare_digest(self.headers.get("X-Jeton") or "", pilote.jeton):
                return self.json(403, {"erreur": "jeton absent ou faux"})
            if (self.headers.get("Content-Type") or "").split(";")[0].strip() != "application/json":
                return self.json(415, {"erreur": "JSON attendu"})
            try:
                taille = int(self.headers.get("Content-Length") or 0)
                corps = json.loads(self.rfile.read(min(taille, 16384)).decode("utf-8") or "{}")
                if not isinstance(corps, dict):
                    raise ValueError
            except (ValueError, UnicodeDecodeError):
                return self.json(400, {"erreur": "JSON illisible"})
            u = urlsplit(self.path)
            if u.path == "/api/action":
                code, r = pilote.lancer(corps)
                return self.json(code, r)
            if u.path == "/api/interrompre":
                code, r = pilote.interrompre(str(corps.get("id") or ""))
                return self.json(code, r)
            return self.json(404, {"erreur": "inconnu"})

        def do_PUT(self):
            self.json(405, {"erreur": "méthode refusée"})

        do_DELETE = do_PATCH = do_PUT

    return Gestionnaire


def serveur(racine=RACINE, port=8765, hote="127.0.0.1", pilotage=True):
    s = ThreadingHTTPServer((hote, port), fabrique(racine, Pilote(racine) if pilotage else None))
    s.daemon_threads = True
    return s


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Tableau de bord local de l'usine (lecture seule).")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--racine", default=RACINE)
    p.add_argument("--sans-navigateur", action="store_true")
    p.add_argument("--instantane", action="store_true", help="imprime l'état en JSON et rend la main")
    p.add_argument("--lecture-seule", action="store_true", help="consultation seule : aucune action possible")
    a = p.parse_args(argv)
    racine = os.path.abspath(a.racine)
    if not os.path.isdir(os.path.join(racine, "JEUX")):
        print("USAGE : %s n'est pas une racine d'usine (dossier JEUX absent)." % racine)
        return 2
    if a.instantane:
        print(json.dumps(instantane(racine), ensure_ascii=False, indent=1))
        return 0
    try:
        s = serveur(racine, a.port, pilotage=not a.lecture_seule)
    except OSError as x:
        print("PORT: %d occupé (%s). Essayer --port %d." % (a.port, x, a.port + 1))
        return 5
    url = "http://127.0.0.1:%d/" % s.server_address[1]
    print("TABLEAU: %s (%s ; Ctrl+C pour arrêter)" % (url, "lecture seule" if a.lecture_seule else "pilotage par usine.py"))
    sys.stdout.flush()
    if not a.sans_navigateur:
        threading.Timer(0.5, webbrowser.open, (url,)).start()
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        s.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""usine.py - point d'entrée de l'usine Roblox, sans T3 Code.

Fait tourner l'orchestrateur et ses agents sur les abonnements Claude Code (CLI `claude`) et
Codex (CLI `codex`) du propriétaire. Le modèle de chaque rôle vient de CONNAISSANCES\\routage.json.

  python usine.py "fais un jeu"        cycle complet : reprend le jeu en cours, sinon veille puis nouveau jeu
  python usine.py "reprends lave-la-tour"   toute demande reconnue par PROCEDURES\\00-ORCHESTRATION.md
  python usine.py etat                 état des jeux, verrous, alertes ouvertes (aucun modèle lancé)
  python usine.py verifier             auto-contrôle de l'usine et tests des outils (aucun modèle lancé)
  python usine.py roles                qui fait quoi, replis, places libres
  python usine.py retours <slug>       boucle des retours joueurs d'un jeu (procédure 11)
  python usine.py battement [--simuler]  un battement sans modèle : mesures, retours, incidents, messages, décision
  python usine.py canaux              par où le propriétaire est prévenu (aucun secret affiché)
  python usine.py stop | reprendre     pose ou retire le fichier STOP (G0)

Options de « fais un jeu » :
  --tours N     nombre maximal de tours d'orchestrateur (défaut 8). Un tour = une session sans
                interface ; l'état vit sur disque (ETAT.json), le tour suivant reprend où l'autre s'arrête.
  --simuler     montre ce qui serait lancé, ne lance rien.

Chaque tour finit par une ligne « ETAT_CYCLE: continuer|bloque|termine | raison ». La boucle
s'arrête sur « bloque » (frontière humaine : voir ALERTES.md), « termine », un fichier STOP, ou
deux tours de suite sans progrès (même étape, même statut).
Codes de sortie : 0 terminé | 1 échec | 2 usage | 3 simulation | 4 bloqué | 6 STOP.
"""
import argparse
import datetime as dt
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile

RACINE = os.path.dirname(os.path.abspath(__file__))
OUTILS = os.path.join(RACINE, "OUTILS")


def charger_deleguer():
    spec = importlib.util.spec_from_file_location("deleguer", os.path.join(OUTILS, "deleguer.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ps(script, *args):
    """Lance un outil PowerShell de l'usine et rend (code, sortie)."""
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join(OUTILS, script)] + list(args),
                       capture_output=True, cwd=RACINE)
    return r.returncode, (r.stdout + r.stderr).decode("cp850", errors="replace")


def py(script, *args):
    r = subprocess.run([sys.executable, os.path.join(OUTILS, script)] + list(args), capture_output=True, cwd=RACINE,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", errors="replace")


def empreinte_etat():
    """Étape et statut de chaque jeu : sert à détecter un tour sans progrès."""
    etat = {}
    jeux = os.path.join(RACINE, "JEUX")
    for slug in sorted(os.listdir(jeux)):
        f = os.path.join(jeux, slug, "ETAT.json")
        if os.path.isfile(f):
            try:
                with io.open(f, encoding="utf-8-sig") as h:
                    e = json.load(h)
                etat[slug] = "%s|%s|%s" % (e.get("etape"), e.get("statut"), json.dumps(e.get("portes", {}), sort_keys=True))
            except Exception:
                etat[slug] = "illisible"
    tete = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=RACINE).stdout.strip()
    return json.dumps(etat, sort_keys=True) + "|" + tete


def cmd_etat():
    for titre, outil, args in (("Jeux", "etat.ps1", ["-Liste"]), ("Verrous", "verrou.ps1", ["liste"])):
        code, sortie = ps(outil, *args)
        print("== %s ==\n%s" % (titre, sortie.strip() or "(rien)"))
    alertes = [l for l in io.open(os.path.join(RACINE, "ALERTES.md"), encoding="utf-8").read().splitlines()
               if l.startswith("|") and l.rstrip().endswith("| ouverte |")]
    print("== Alertes ouvertes : %d ==" % len(alertes))
    for l in alertes:
        print(l)
    print("== STOP : %s ==" % ("présent" if os.path.exists(os.path.join(RACINE, "STOP")) else "absent"))
    return 0


def cmd_verifier():
    code, sortie = ps("verifier-usine.ps1")
    print(sortie.strip())
    return code


PROMPT_ORCHESTRATEUR = """Tu es l'orchestrateur de l'usine Roblox, lancé sans interface par usine.py (tour {tour} sur {tours}). Racine : {racine}.
Lis d'abord GARDE-FOUS.md, AGENTS.md, PROCEDURES\\00-ORCHESTRATION.md et PROCEDURES\\13-ORCHESTRATION-MULTI-FOURNISSEURS.md, puis fais l'ouverture de session de la procédure 00 (§ 1). Réponds et écris en français, concis et factuel.

Mémoire entre tours et après compaction : `python OUTILS\\historique.py sessions` liste les sessions précédentes de ce dossier (tours d'orchestrateur et enfants, Claude et Codex) ; `historique.py demandes|chercher "<mot>"|lire --session <id>` relit leur texte exact. Utilise-le avant de refaire une décision déjà prise ou si ton contexte a été compacté.

Demande du propriétaire : « {demande} »

Tu n'es pas dans T3 Code : tu n'as pas l'outil delegate_task. Pour déléguer, écris le prompt de l'enfant dans JOURNAUX\\prompts\\<nom>.md puis lance
  python OUTILS\\deleguer.py --role <rôle> --prompt-fichier JOURNAUX\\prompts\\<nom>.md --jeu <slug> --titre "<titre>"
Le rôle fixe le modèle, l'effort et les replis (python OUTILS\\deleguer.py --liste). La commande rend la main quand l'enfant a fini, avec sa ligne RESULTAT ; lance en arrière-plan les enfants qui peuvent tourner en même temps (Codex : sans plafond imposé ; Claude Opus, Fable, Sonnet : le plafond G2 est appliqué par l'outil, code 4 = attendre). Une ligne « REPLI: … mode dégradé » s'écrit dans l'ETAT.json du jeu (mode_degrade).

Avance d'autant d'étapes que tu peux dans ce tour, porte après porte, sans rien demander : l'état vit sur disque, un autre tour reprendra. Ne publie et ne dépense que ce que CONNAISSANCES\\PLAFONDS.md autorise. Devant une frontière humaine (G7) : alerte, statut bloqué, et continue ce qui n'en dépend pas. Vérifie les verrous avant Studio ou le bureau ; un verrou tenu par un autre agent se respecte.

Finis par un commit de ton lot, puis par ces deux lignes exactement :
ETAT_CYCLE: <continuer|bloque|termine> | <jeu, étape atteinte, ce qui manque>
RESULTAT: <ok|echec|arret> | <fichier principal produit ou modifié> | <une phrase>
« continuer » = il reste du travail faisable sans humain ; « bloque » = tout ce qui reste attend le propriétaire ou un verrou ; « termine » = la demande est satisfaite.
"""


def cmd_cycle(demande, tours, simuler):
    d = charger_deleguer()
    routage = d.lire_routage()
    if os.path.exists(os.path.join(RACINE, "STOP")):
        print("STOP: fichier STOP présent (G0). `python usine.py reprendre` pour le retirer.")
        return 6
    candidat, rang, ecartes = d.choisir(routage, "00.orchestrateur")
    for e in ecartes:
        print("ECARTE: " + e)
    if candidat is None:
        print("AUCUN: aucun orchestrateur disponible (CLI claude et codex absentes ?).")
        return 1
    if simuler:
        print("SIMULATION: orchestrateur %s %s effort %s, %d tour(s) au plus, demande « %s »" % (
            candidat["fournisseur"], candidat["modele"], candidat["effort"], tours, demande))
        return 3
    os.makedirs(os.path.join(RACINE, "JOURNAUX", "prompts"), exist_ok=True)
    journal = os.path.join(RACINE, "JOURNAUX", "cycles.log")
    sans_progres = 0
    indisponibles = set()
    for tour in range(1, tours + 1):
        if os.path.exists(os.path.join(RACINE, "STOP")):
            print("STOP: fichier STOP présent, arrêt avant le tour %d." % tour)
            return 6
        avant = empreinte_etat()
        prompt = PROMPT_ORCHESTRATEUR.format(tour=tour, tours=tours, racine=RACINE, demande=demande.replace("«", "").replace("»", ""))
        duree_max = int(routage["roles"]["00.orchestrateur"].get("duree_max_min", 180))
        print("--- tour %d/%d : orchestrateur %s %s (effort %s)" % (tour, tours, candidat["fournisseur"], candidat["modele"], candidat["effort"]))
        sys.stdout.flush()
        r = d.lancer(routage, "00.orchestrateur", candidat, rang, prompt, "", "cycle tour %d" % tour, duree_max)
        final = r["final"].strip()
        print(final[-4000:])
        m = None
        for ligne in reversed(final.splitlines()):
            m = re.search(r"ETAT_CYCLE\s*:\s*(continuer|bloque|termine)\b\s*\|?\s*(.*)", ligne, re.IGNORECASE)
            if m:
                break
        etat_cycle = m.group(1).lower() if m else "inconnu"
        raison = m.group(2).strip() if m else "aucune ligne ETAT_CYCLE"
        with io.open(journal, "a", encoding="utf-8") as h:
            h.write("%s | tour %d/%d | %s %s | %d s | %s | %s\n" % (
                dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), tour, tours,
                candidat["fournisseur"], candidat["modele"], r["duree_s"], etat_cycle, raison))
        if etat_cycle == "termine":
            return 0
        if etat_cycle == "bloque":
            # Prévenir le propriétaire là où il est (procédure 14) ; l'anti-répétition est dans prevenir.py.
            subprocess.run([sys.executable, os.path.join(OUTILS, "prevenir.py"), "envoyer", "--niveau", "important",
                            "--sujet", "Orchestrateur bloqué",
                            "--texte", "Un tour est bloqué. Consulter ALERTES.md et python usine.py etat.",
                            "--cle", "cycle-bloque"], check=False, capture_output=True, cwd=RACINE)
            print("BLOQUE: %s (voir ALERTES.md et `python usine.py etat`)." % raison)
            return 4
        if r["verdict"] is None and (r["code_cli"] != 0 or r["sans_message"]):
            # L'orchestrateur lui-même n'a pas démarré : essayer le candidat suivant.
            indisponibles.add("%s:%s" % (candidat["fournisseur"], candidat["modele"]))
            suivant, rang2, _ = d.choisir(routage, "00.orchestrateur", indisponibles=indisponibles)
            if suivant is None:
                print("ECHEC: orchestrateur indisponible, aucun repli.")
                return 1
            print("REPLI: orchestrateur -> %s %s%s" % (suivant["fournisseur"], suivant["modele"],
                                                    " ; " + suivant["degrade"] if suivant.get("degrade") else ""))
            candidat, rang = suivant, rang2
            continue
        sans_progres = sans_progres + 1 if empreinte_etat() == avant else 0
        if sans_progres >= 2:
            print("ARRET: deux tours de suite sans progrès (même état, aucun commit).")
            return 1
    print("TOURS: %d tour(s) faits, cycle non terminé ; relancer la même commande pour continuer." % tours)
    return 1


def cmd_retours(slug):
    code, sortie = py("retours-joueurs.py", "diagnostic", "--jeu", slug)
    print(sortie.strip())
    if code != 0:
        print("La collecte par Open Cloud n'est pas possible aujourd'hui ; voir PROCEDURES\\11-RETOURS-JOUEURS.md § Accès.")
        return 4
    return cmd_cycle("Boucle des retours joueurs de %s (procédure 11) : collecte, tri, jugement, propositions." % slug, 2, False)


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Usine Roblox : point d'entrée.", usage="python usine.py \"fais un jeu\" | etat | verifier | roles | retours <slug> | stop | reprendre")
    p.add_argument("demande", nargs="+")
    p.add_argument("--tours", type=int, default=8)
    p.add_argument("--simuler", action="store_true")
    a = p.parse_args(argv)
    mot = a.demande[0].lower()
    if len(a.demande) == 1 and mot in ("etat", "état"):
        return cmd_etat()
    if len(a.demande) == 1 and mot in ("verifier", "vérifier"):
        return cmd_verifier()
    if len(a.demande) == 1 and mot in ("roles", "rôles"):
        return charger_deleguer().main(["--liste"])
    if len(a.demande) == 1 and mot == "battement":
        # Un battement sans modèle : mesures, retours, incidents, messages au propriétaire, décision.
        code, sortie = py("battement.py", *(["--simuler"] if a.simuler else []))
        print(sortie.strip())
        return code
    if len(a.demande) == 1 and mot == "canaux":
        code, sortie = py("prevenir.py", "canaux")
        print(sortie.strip())
        return code
    if len(a.demande) == 1 and mot == "stop":
        io.open(os.path.join(RACINE, "STOP"), "a").close()
        print("STOP posé : aucun agent n'agit plus (G0).")
        return 0
    if len(a.demande) == 1 and mot == "reprendre":
        f = os.path.join(RACINE, "STOP")
        if os.path.exists(f):
            os.remove(f)
        print("STOP retiré.")
        return 0
    if mot == "retours" and len(a.demande) == 2:
        return cmd_retours(a.demande[1])
    return cmd_cycle(" ".join(a.demande), a.tours, a.simuler)


if __name__ == "__main__":
    sys.exit(main())

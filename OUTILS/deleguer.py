#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deleguer.py - lance un agent enfant de l'usine avec le modèle prévu pour son rôle.

Source unique du choix : CONNAISSANCES\\routage.json (fournisseur, modèle, effort, replis).
Deux modes :
  --format cli (défaut)  lance la CLI du fournisseur (codex exec, claude -p) sur l'abonnement
                         du propriétaire, attend la fin, journalise, rend la ligne RESULTAT.
  --format t3            n'exécute rien : imprime la charge utile JSON à passer à l'outil
                         delegate_task de T3 Code (l'orchestrateur y colle le prompt).

Usage :
  python OUTILS\\deleguer.py --role 03.calcul --prompt-fichier <prompt.md> [--jeu <slug>] [--titre "..."]
  python OUTILS\\deleguer.py --role 04.relecteur-fun --format t3 --prompt-fichier <prompt.md>
  python OUTILS\\deleguer.py --liste                      tableau des rôles et de leur premier choix
  python OUTILS\\deleguer.py --role 01.veilleur --simuler [--indisponible codex]
  python OUTILS\\deleguer.py --accorder claude-opus-5-5 --nombre 2 [--heures 12]   (propriétaire seulement)
  python OUTILS\\deleguer.py --accords                   accords de quota en cours et demandes ouvertes

Règles appliquées :
  G0  fichier STOP : aucun lancement.
  G2  jamais plus de N agents Claude Opus, Fable ou Sonnet en même temps (N = routage.json,
      l'orchestrateur compte pour un). Le compte se fait sur JOURNAUX\\agents\\*.json (PID vivants).
  G9  le prompt passe par l'entrée standard, jamais par un argument ; un prompt qui ressemble
      à un secret est refusé.
  A6  un modèle indisponible n'est pas remplacé en silence : le repli est écrit dans le journal
      et, s'il est marqué « degrade », rappelé sur la sortie (ligne REPLI:).
  A2  --auteur <fournisseur:modele> écarte ce modèle pour les rôles de relecture indépendante.
  Q1  un modèle de routage.json « sur_accord » (Opus 5.5, Astra 6.2 : quota du propriétaire) n'est
      lancé que sur un accord écrit par le propriétaire (--accorder, N lancements, durée bornée) ;
      chaque lancement en consomme un. Sans accord, le rôle passe au candidat suivant (Codex) et
      une demande d'accord part par OUTILS\\prevenir.py (une par modèle, anti-répétition).

Codes de sortie : 0 l'enfant a rendu RESULTAT: ok | 1 l'enfant a rendu echec, arret, ou rien
  2 usage | 3 simulation ou format t3 (rien lancé) | 4 plafond G2 atteint | 5 aucun candidat
  disponible | 6 fichier STOP | 7 prompt refusé (secret probable) | 8 durée dépassée | 9 agent figé (aucune
  écriture pendant silence_max_min, 20 min par défaut, réglable par rôle dans routage.json)
  10 aucun candidat sans accord du propriétaire (Q1) : demande envoyée.
"""
import argparse
import contextlib
import csv
import datetime as dt
import glob
import io
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid

if os.name == "nt":
    import msvcrt
else:
    import fcntl

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTAGE = os.path.join(RACINE, "CONNAISSANCES", "routage.json")
DOS_AGENTS = os.path.join(RACINE, "JOURNAUX", "agents")
JOURNAL = os.path.join(RACINE, "JOURNAUX", "delegations.csv")

# Motifs de secrets (G9), assemblés par morceaux pour ne pas se détecter soi-même.
MOTIFS_SECRETS = [
    r"_\|WARN" + r"ING:-DO-NOT-SHARE",
    r"discord(app)?\.com/api/(v\d+/)?webhooks/\d{6,}/[A-Za-z0-9_-]{20,}",
    r"x-api-key\s*[:=]\s*[\"']?[A-Za-z0-9+/=_-]{24,}",
    r"ROBLOSECURITY\s*[:=]\s*[\"']?[A-Za-z0-9_|:-]{24,}",
    r"sk-(ant|proj)-[A-Za-z0-9_-]{16,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
]


def lire_routage(chemin=ROUTAGE):
    with io.open(chemin, encoding="utf-8") as f:
        return json.load(f)


def maintenant():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pid_vivant(pid):
    if not pid:
        return False
    try:
        if os.name == "nt":
            sortie = subprocess.run(
                ["tasklist", "/FI", "PID eq %d" % int(pid), "/NH", "/FO", "CSV"],
                capture_output=True, text=True, timeout=15,
            ).stdout
            return ('"%d"' % int(pid)) in sortie
        os.kill(int(pid), 0)
        return True
    except Exception:
        return False


def agents_vivants():
    """Fiches JOURNAUX\\agents\\*.json dont le processus existe encore. Purge les fiches mortes."""
    vivants = []
    if not os.path.isdir(DOS_AGENTS):
        return vivants
    for nom in os.listdir(DOS_AGENTS):
        if not nom.endswith(".json"):
            continue
        chemin = os.path.join(DOS_AGENTS, nom)
        try:
            with io.open(chemin, encoding="utf-8") as f:
                fiche = json.load(f)
        except Exception:
            continue
        if pid_vivant(fiche.get("pid")):
            vivants.append(fiche)
        else:
            try:
                os.remove(chemin)
            except OSError:
                pass
    return vivants


def est_claude_fort(routage, modele):
    return modele in routage.get("classes", {}).get("claude_fort", [])


def places_claude_fort(routage):
    """Nombre d'agents Claude forts encore permis maintenant (G2)."""
    plafond = int(routage.get("plafond_claude_forts_simultanes", 2))
    pris = sum(1 for a in agents_vivants() if a.get("claude_fort"))
    if routage.get("orchestrateur_compte_dans_le_plafond", True):
        # L'orchestrateur est un Claude fort sauf s'il s'est déclaré autrement.
        if os.environ.get("USINE_ORCHESTRATEUR_CLASSE", "claude_fort") == "claude_fort":
            deja = any(a.get("role") == "00.orchestrateur" and a.get("claude_fort") for a in agents_vivants())
            if not deja:
                pris += 1
    return plafond - pris


def modeles_sur_accord(routage):
    return set(routage.get("sur_accord", {}).get("modeles", []))


def chemin_sur_accord(routage, cle, defaut):
    return os.path.join(RACINE, *routage.get("sur_accord", {}).get(cle, defaut).replace("\\", "/").split("/"))


def lire_json_local(chemin):
    try:
        with io.open(chemin, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def ecrire_json_local(chemin, donnees):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    tmp = "%s.%s.tmp" % (chemin, uuid.uuid4().hex)
    with io.open(tmp, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)
    os.replace(tmp, chemin)


@contextlib.contextmanager
def verrou(chemin, delai_s=30):
    """Verrou inter-processus du système (libéré même si le processus meurt) autour d'un lire-modifier-écrire."""
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with io.open(chemin + ".lock", "a+b") as f:
        fin = time.time() + delai_s
        while True:
            try:
                if os.name == "nt":
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.time() > fin:
                    raise TimeoutError("verrou occupé : %s.lock" % chemin)
                time.sleep(0.02)
        try:
            yield
        finally:
            if os.name == "nt":
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def accords_valides(routage, horloge=time.time):
    """Accords du propriétaire encore utilisables : {modele: {restant, expire_utc, ...}}."""
    accords = lire_json_local(chemin_sur_accord(routage, "fichier_accords", "JOURNAUX/accords-quota.json"))
    maintenant_s = horloge()
    valides = {}
    for modele, a in accords.items():
        try:
            expire = dt.datetime.strptime(a["expire_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp()
            restant = int(a["restant"])
        except (KeyError, TypeError, ValueError):
            continue
        if restant > 0 and expire > maintenant_s:
            valides[modele] = a
    return valides


def accord_present(routage, modele, horloge=time.time):
    return modele not in modeles_sur_accord(routage) or modele in accords_valides(routage, horloge)


def consommer_accord(routage, modele, horloge=time.time):
    """Retire un lancement de l'accord du modèle. Vrai si le lancement est permis (Q1)."""
    if modele not in modeles_sur_accord(routage):
        return True
    chemin = chemin_sur_accord(routage, "fichier_accords", "JOURNAUX/accords-quota.json")
    with verrou(chemin):
        if modele not in accords_valides(routage, horloge):
            return False
        accords = lire_json_local(chemin)
        accords[modele]["restant"] = int(accords[modele]["restant"]) - 1
        accords[modele]["dernier_usage_utc"] = maintenant()
        ecrire_json_local(chemin, accords)
    return True


def accorder(routage, modele, nombre, heures, horloge=time.time):
    if modele not in modeles_sur_accord(routage):
        raise ValueError("« %s » n'est pas un modèle sur accord (routage.json, sur_accord)." % modele)
    if nombre < 1 or heures <= 0:
        raise ValueError("--nombre doit être ≥ 1 et --heures > 0.")
    chemin = chemin_sur_accord(routage, "fichier_accords", "JOURNAUX/accords-quota.json")
    expire = dt.datetime.fromtimestamp(horloge() + heures * 3600, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # La demande est close avant l'écriture de l'accord : un échec entre les deux rouvre une demande, jamais l'inverse.
    demandes_chemin = chemin_sur_accord(routage, "fichier_demandes", "JOURNAUX/demandes-quota.json")
    with verrou(demandes_chemin):
        demandes = lire_json_local(demandes_chemin)
        if demandes.pop(modele, None) is not None:
            ecrire_json_local(demandes_chemin, demandes)
    with verrou(chemin):
        accords = lire_json_local(chemin)
        accords[modele] = {"restant": int(nombre), "expire_utc": expire, "accorde_utc": maintenant()}
        ecrire_json_local(chemin, accords)
    return accords[modele]


def prevenir(sujet, texte, cle):
    """Message au propriétaire par OUTILS\\prevenir.py (l'anti-répétition est dans prevenir.py)."""
    r = subprocess.run([sys.executable, os.path.join(RACINE, "OUTILS", "prevenir.py"), "envoyer", "--niveau", "important",
                        "--sujet", sujet, "--texte", texte, "--cle", cle], capture_output=True, cwd=RACINE)
    return r.returncode


def demander_accord(routage, role, modele):
    """Note la demande d'accord (JOURNAUX) et prévient le propriétaire, une fois par modèle."""
    chemin = chemin_sur_accord(routage, "fichier_demandes", "JOURNAUX/demandes-quota.json")
    with verrou(chemin):
        demandes = lire_json_local(chemin)
        deja = modele in demandes
        d = demandes.setdefault(modele, {"premiere_demande_utc": maintenant(), "roles": []})
        if role not in d["roles"]:
            d["roles"].append(role)
        d["derniere_demande_utc"] = maintenant()
        ecrire_json_local(chemin, demandes)
    if deja:
        return None
    return prevenir("Accord de quota demandé : %s" % modele,
                    "Le rôle %s voudrait %s (quota du propriétaire). En attendant, il passe au repli Codex. "
                    "Pour accorder : python OUTILS\\deleguer.py --accorder %s --nombre 1 --heures 12" % (role, modele, modele),
                    "quota-" + modele)


def cli_presente(routage, fournisseur):
    nom = routage["fournisseurs"][fournisseur]["cli"]
    return shutil.which(nom)


def choisir(routage, role, indisponibles=(), auteur=None, pour_lancer=True, pour_t3=False, horloge=time.time):
    """Rend (candidat, rang, raisons d'écart). Le premier candidat utilisable gagne."""
    if role not in routage["roles"]:
        raise SystemExit("USAGE : rôle inconnu « %s ». Voir --liste." % role)
    ecartes = []
    for rang, c in enumerate(routage["roles"][role]["candidats"]):
        cle = "%s:%s" % (c["fournisseur"], c["modele"])
        if c["fournisseur"] in indisponibles or cle in indisponibles or c["modele"] in indisponibles:
            ecartes.append("%s : déclaré indisponible" % cle)
            continue
        if auteur and cle == auteur and routage["roles"][role].get("interdit_si_auteur"):
            ecartes.append("%s : auteur de ce qui est relu (A2)" % cle)
            continue
        if pour_t3 and "t3_providerInstanceId" not in routage["fournisseurs"][c["fournisseur"]]:
            ecartes.append("%s : fournisseur non joignable depuis T3 Code" % cle)
            continue
        if not accord_present(routage, c["modele"], horloge):
            ecartes.append("%s : %s" % (cle, ECART_ACCORD))
            continue
        if pour_lancer and not cli_presente(routage, c["fournisseur"]):
            ecartes.append("%s : CLI « %s » absente" % (cle, routage["fournisseurs"][c["fournisseur"]]["cli"]))
            continue
        if pour_lancer and est_claude_fort(routage, c["modele"]) and role != "00.orchestrateur" and places_claude_fort(routage) < 1:
            ecartes.append("%s : plafond G2 atteint" % cle)
            continue
        return c, rang, ecartes
    return None, -1, ecartes


ECART_ACCORD = "quota du propriétaire, aucun accord en cours (Q1)"


def modeles_sans_accord(ecartes):
    return [e.split(" : ")[0].split(":", 1)[1] for e in ecartes if e.endswith(ECART_ACCORD)]


def charge_t3(routage, role, candidat, titre, prompt):
    f = routage["fournisseurs"][candidat["fournisseur"]]
    return {
        "title": titre or role,
        "role": routage["roles"][role].get("t3_role", "general"),
        "mode": "async",
        "target": {
            "providerInstanceId": f["t3_providerInstanceId"],
            "model": candidat["modele"],
            "options": {f["t3_option_effort"]: candidat["effort"]},
        },
        "task": prompt,
    }


def commande_cli(routage, candidat, fichier_dernier_message):
    f = routage["fournisseurs"][candidat["fournisseur"]]
    exe = shutil.which(f["cli"]) or f["cli"]
    if candidat["fournisseur"] == "codex":
        return [exe, "exec", "-m", candidat["modele"],
                "-c", "model_reasoning_effort=%s" % candidat["effort"],
                "-C", RACINE, "--skip-git-repo-check", "--color", "never",
                "-o", fichier_dernier_message, "-"]
    if candidat["fournisseur"] == "claude":
        return [exe, "-p", "--model", candidat["modele"], "--effort", candidat["effort"],
                "--output-format", "text"] + list(f.get("cli_args_sans_interaction", []))
    if f.get("cli_args"):
        valeurs = {"modele": candidat["modele"], "effort": candidat["effort"], "racine": RACINE,
                   "dernier": fichier_dernier_message}
        return [exe] + [x.format(**valeurs) for x in f["cli_args"]]
    raise SystemExit("fournisseur inconnu : %s" % candidat["fournisseur"])


def ecrire_journal(ligne):
    os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)
    nouveau = not os.path.exists(JOURNAL)
    with io.open(JOURNAL, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        if nouveau:
            w.writerow(["debut_utc", "jeu", "role", "fournisseur", "modele", "effort", "rang", "duree_s", "code", "resultat", "titre"])
        w.writerow(ligne)


def dernier_resultat(texte):
    for ligne in reversed((texte or "").strip().splitlines()):
        m = re.search(r"RESULTAT\s*:\s*(ok|echec|arret)\b(.*)", ligne.strip(), re.IGNORECASE)
        if m:
            return m.group(1).lower(), ligne.strip()
    return None, ""


def jeton_claude(nom="usine-roblox:claude:oauth"):
    """Jeton longue durée de la CLI claude, lu dans le Gestionnaire d'identification ; None s'il manque."""
    if os.name != "nt":
        return None
    try:
        import ctypes
        from ctypes import wintypes

        class CREDENTIAL(ctypes.Structure):
            _fields_ = [("Flags", wintypes.DWORD), ("Type", wintypes.DWORD), ("TargetName", wintypes.LPWSTR),
                        ("Comment", wintypes.LPWSTR), ("LastWritten", wintypes.FILETIME),
                        ("CredentialBlobSize", wintypes.DWORD), ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
                        ("Persist", wintypes.DWORD), ("AttributeCount", wintypes.DWORD), ("Attributes", ctypes.c_void_p),
                        ("TargetAlias", wintypes.LPWSTR), ("UserName", wintypes.LPWSTR)]
        api = ctypes.WinDLL("advapi32", use_last_error=True)
        api.CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(CREDENTIAL))]
        api.CredReadW.restype = wintypes.BOOL
        api.CredFree.argtypes = [ctypes.c_void_p]
        p = ctypes.POINTER(CREDENTIAL)()
        if not api.CredReadW(nom, 1, 0, ctypes.byref(p)):
            return None
        try:
            n = p.contents.CredentialBlobSize
            return bytes(p.contents.CredentialBlob[:n]).decode("utf-16-le") or None
        finally:
            api.CredFree(p)
    except Exception:
        return None


def silence_max_min(routage, role):
    """Minutes sans aucune écriture de l'agent avant de le déclarer figé (17/11/2026 : un appel au
    modèle de l'orchestrateur est resté figé plus de 4 h sans que rien ne l'arrête)."""
    r = routage.get("roles", {}).get(role, {})
    return int(r.get("silence_max_min", routage.get("silence_max_min", 20)))


def derniere_activite(fournisseur, depuis):
    """Instant de la dernière écriture dans une transcription de session ouverte après `depuis`."""
    if fournisseur == "claude":
        dossier = os.path.join(os.path.expanduser("~"), ".claude", "projects", re.sub(r"[^A-Za-z0-9]", "-", RACINE))
        motif = os.path.join(dossier, "*.jsonl")
    else:
        motif = os.path.join(os.path.expanduser("~"), ".codex", "sessions", "*", "*", "*", "*.jsonl")
    meilleur = None
    for chemin in glob.glob(motif):
        try:
            m = os.path.getmtime(chemin)
        except OSError:
            continue
        if m >= depuis - 5 and (meilleur is None or m > meilleur):
            meilleur = m
    return meilleur


def tuer(proc):
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
    else:
        proc.kill()


def attendre_agent(proc, prompt, fournisseur, debut, duree_max_min, silence_min, pas=15, horloge=time.time,
                   activite=None):
    """Rend (code, sortie). 8 = durée maximale dépassée ; 9 = agent figé (ni sortie ni transcription
    pendant `silence_min`). La sortie est lue dans un fil pour ne jamais bloquer la surveillance."""
    activite = activite or derniere_activite
    morceaux, vu = [], [horloge()]

    def lire():
        try:
            proc.stdin.write(prompt.encode("utf-8"))
            proc.stdin.close()
        except Exception:
            pass
        for bloc in iter(lambda: proc.stdout.read1(4096) if hasattr(proc.stdout, "read1") else proc.stdout.read(4096), b""):
            morceaux.append(bloc)
            vu[0] = horloge()

    fil = threading.Thread(target=lire, daemon=True)
    fil.start()
    code = None
    while True:
        fil.join(pas)
        if not fil.is_alive() and proc.poll() is not None:
            code = proc.returncode
            break
        maintenant_s = horloge()
        if maintenant_s - debut > duree_max_min * 60:
            code = 8
        else:
            dernier = max(vu[0], activite(fournisseur, debut) or 0)
            if maintenant_s - dernier > silence_min * 60:
                code = 9
        if code is not None:
            tuer(proc)
            fil.join(20)
            break
    return code, b"".join(morceaux)


def lancer(routage, role, candidat, rang, prompt, jeu, titre, duree_max_min):
    if not consommer_accord(routage, candidat["modele"]):
        # Dernier verrou avant de dépenser : l'accord a expiré ou a été épuisé depuis le choix (Q1).
        ecrire_journal([maintenant(), jeu or "", role, candidat["fournisseur"], candidat["modele"], candidat["effort"], rang,
                        0, 10, "sans-accord", titre or ""])
        return {"code_cli": 10, "verdict": None, "ligne": "", "duree_s": 0, "final": "", "journal": JOURNAL,
                "expire": False, "fige": False, "sans_message": True, "sans_accord": True}
    os.makedirs(DOS_AGENTS, exist_ok=True)
    ident = "%s-%s" % (dt.datetime.now().strftime("%Y%m%d-%H%M%S"), uuid.uuid4().hex[:6])
    fiche = os.path.join(DOS_AGENTS, ident + ".json")
    journal_sortie = os.path.join(DOS_AGENTS, ident + ".log")
    dernier = os.path.join(DOS_AGENTS, ident + ".dernier.txt")
    cmd = commande_cli(routage, candidat, dernier)
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["USINE_ROLE"] = role
    if role == "00.orchestrateur":
        env["USINE_ORCHESTRATEUR_CLASSE"] = "claude_fort" if est_claude_fort(routage, candidat["modele"]) else "autre"
    if candidat["fournisseur"] == "claude" and not env.get("CLAUDE_CODE_OAUTH_TOKEN"):
        # Jeton longue durée (`python OUTILS\jeton-claude.py`) : la connexion interactive expire, lui dure un an.
        jeton = jeton_claude()
        if jeton:
            env["CLAUDE_CODE_OAUTH_TOKEN"] = jeton
    debut = time.time()
    debut_utc = maintenant()
    with io.open(journal_sortie, "w", encoding="utf-8") as log:
        log.write("# %s | role %s | %s %s effort %s | rang %d\n" % (debut_utc, role, candidat["fournisseur"], candidat["modele"], candidat["effort"], rang))
        log.flush()
        proc = subprocess.Popen(cmd, cwd=RACINE, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, env=env)
        with io.open(fiche, "w", encoding="utf-8") as f:
            json.dump({"id": ident, "pid": proc.pid, "role": role, "fournisseur": candidat["fournisseur"],
                       "modele": candidat["modele"], "effort": candidat["effort"],
                       "claude_fort": est_claude_fort(routage, candidat["modele"]),
                       "jeu": jeu, "titre": titre, "debut_utc": debut_utc}, f, ensure_ascii=False)
        code, sortie = attendre_agent(proc, prompt, candidat["fournisseur"], debut, duree_max_min,
                                      silence_max_min(routage, role))
        texte = sortie.decode("utf-8", errors="replace")
        if code == 9:
            texte += "\nSILENCE: aucune activité de l'agent pendant %d min (transcription figée) ; agent arrêté.\n" % silence_max_min(routage, role)
        log.write(texte)
    try:
        os.remove(fiche)
    except OSError:
        pass
    final = texte
    # Codex rend parfois le code 0 alors qu'il a refusé le modèle ou le quota : l'absence de
    # dernier message (fichier -o vide) est alors le seul signe d'un échec de la CLI.
    sans_message = not texte.strip()
    if candidat["fournisseur"] == "codex":
        sans_message = not (os.path.exists(dernier) and os.path.getsize(dernier) > 0)
    if os.path.exists(dernier) and os.path.getsize(dernier) > 0:
        with io.open(dernier, encoding="utf-8", errors="replace") as f:
            final = f.read()
    # Codex recopie le prompt dans sa sortie : on ne lit le verdict que dans son dernier message,
    # jamais dans la transcription (le prompt contient souvent un exemple de ligne RESULTAT).
    if candidat["fournisseur"] == "codex" and sans_message:
        verdict, ligne = None, ""
    else:
        verdict, ligne = dernier_resultat(final)
    duree = int(time.time() - debut)
    ecrire_journal([debut_utc, jeu or "", role, candidat["fournisseur"], candidat["modele"], candidat["effort"], rang,
                    duree, code, verdict or "sans-resultat", titre or ""])
    return {"code_cli": code, "verdict": verdict, "ligne": ligne, "duree_s": duree, "final": final,
            "journal": journal_sortie, "expire": code == 8, "fige": code == 9, "sans_message": sans_message}


def afficher_liste(routage):
    print("%-24s %-8s %-20s %-7s %s" % ("rôle", "fourn.", "modèle", "effort", "replis"))
    for role, r in routage["roles"].items():
        c = r["candidats"][0]
        replis = ", ".join("%s/%s" % (x["modele"], x["effort"]) for x in r["candidats"][1:]) or "aucun (pause et alerte)"
        print("%-24s %-8s %-20s %-7s %s" % (role, c["fournisseur"], c["modele"], c["effort"], replis))
    accords = accords_valides(routage)
    print("sur accord du propriétaire (Q1) : %s" % (", ".join(
        "%s (%s)" % (m, "%d lancement(s) jusqu'au %s" % (int(accords[m]["restant"]), accords[m]["expire_utc"]) if m in accords else "aucun accord")
        for m in sorted(modeles_sur_accord(routage))) or "aucun"))
    print("plafond Claude forts simultanés : %d (orchestrateur compris : %s) ; places libres maintenant : %d" % (
        routage.get("plafond_claude_forts_simultanes", 2),
        "oui" if routage.get("orchestrateur_compte_dans_le_plafond", True) else "non",
        places_claude_fort(routage)))


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Délégation d'un rôle de l'usine au modèle prévu.")
    p.add_argument("--role")
    p.add_argument("--prompt-fichier")
    p.add_argument("--jeu", default="")
    p.add_argument("--titre", default="")
    p.add_argument("--format", choices=["cli", "t3"], default="cli")
    p.add_argument("--simuler", action="store_true")
    p.add_argument("--liste", action="store_true")
    p.add_argument("--indisponible", default="", help="fournisseurs ou modèles à écarter, séparés par des virgules")
    p.add_argument("--auteur", default="", help="fournisseur:modele de l'auteur de ce qui est relu (A2)")
    p.add_argument("--routage", default=ROUTAGE)
    p.add_argument("--accorder", default="", help="modèle sur accord à permettre (propriétaire seulement, Q1)")
    p.add_argument("--nombre", type=int, default=1, help="lancements permis par --accorder")
    p.add_argument("--heures", type=float, default=12, help="durée de validité de --accorder")
    p.add_argument("--accords", action="store_true", help="accords en cours et demandes ouvertes")
    a = p.parse_args(argv)

    routage = lire_routage(a.routage)
    if a.accorder:
        if os.environ.get("USINE_ROLE"):
            print("REFUS : un agent de l'usine ne s'accorde pas de quota ; seul le propriétaire lance --accorder (Q1).")
            return 7
        try:
            r = accorder(routage, a.accorder, a.nombre, a.heures)
        except ValueError as e:
            print("USAGE : %s" % e)
            return 2
        print("ACCORD: %s, %d lancement(s) jusqu'au %s" % (a.accorder, r["restant"], r["expire_utc"]))
        return 0
    if a.accords:
        print(json.dumps({"accords": accords_valides(routage),
                          "demandes": lire_json_local(chemin_sur_accord(routage, "fichier_demandes", "JOURNAUX/demandes-quota.json"))},
                         ensure_ascii=False, indent=2))
        return 0
    if a.liste:
        afficher_liste(routage)
        return 0
    if not a.role:
        p.print_usage()
        return 2
    indispo = tuple(x.strip() for x in a.indisponible.split(",") if x.strip())
    if a.role not in routage["roles"]:
        print("USAGE : rôle inconnu « %s ». Voir --liste." % a.role)
        return 2

    prompt = ""
    if a.prompt_fichier:
        with io.open(a.prompt_fichier, encoding="utf-8") as f:
            prompt = f.read()
        for m in MOTIFS_SECRETS:
            if re.search(m, prompt):
                print("REFUS : le prompt ressemble à un secret (G9).")
                return 7
    elif not a.simuler and a.format == "cli":
        print("USAGE : --prompt-fichier obligatoire pour lancer.")
        return 2

    pour_lancer = (a.format == "cli")
    candidat, rang, ecartes = choisir(routage, a.role, indispo, a.auteur or None, pour_lancer=pour_lancer,
                                      pour_t3=(a.format == "t3"))
    for e in ecartes:
        print("ECARTE: " + e)
    for modele in modeles_sans_accord(ecartes):
        if a.simuler:
            print("ACCORD-REQUIS: %s (simulation : aucune demande envoyée)" % modele)
        else:
            demander_accord(routage, a.role, modele)
            print("ACCORD-DEMANDE: %s demandé au propriétaire ; `--accorder %s` pour le permettre." % (modele, modele))
    if candidat is None and modeles_sans_accord(ecartes) and all(
            e.endswith(ECART_ACCORD) or "indisponible" in e for e in ecartes):
        print("ACCORD: aucun candidat sans accord du propriétaire pour %s ; étape en pause (Q1)." % a.role)
        return 10
    if candidat is None:
        if any("plafond G2" in e for e in ecartes):
            print("PLAFOND: aucun candidat sans dépasser le plafond G2 ; attendre la fin d'un agent Claude fort.")
            return 4
        print("AUCUN: aucun candidat disponible pour %s ; étape en pause, alerte à écrire (règle A6)." % a.role)
        return 5
    if rang > 0:
        print("REPLI: %s passe au choix n° %d (%s %s, effort %s)%s" % (
            a.role, rang + 1, candidat["fournisseur"], candidat["modele"], candidat["effort"],
            " ; mode dégradé : " + candidat["degrade"] if candidat.get("degrade") else ""))

    if a.format == "t3":
        if not a.simuler and not consommer_accord(routage, candidat["modele"]):
            print("ACCORD: l'accord pour %s a expiré entre le choix et l'envoi ; relancer (Q1)." % candidat["modele"])
            return 10
        print(json.dumps(charge_t3(routage, a.role, candidat, a.titre, prompt), ensure_ascii=False, indent=2))
        return 3
    if a.simuler:
        print("SIMULATION: %s -> %s %s effort %s ; commande : %s" % (
            a.role, candidat["fournisseur"], candidat["modele"], candidat["effort"],
            " ".join(os.path.basename(x) if i == 0 else x for i, x in enumerate(commande_cli(routage, candidat, "<fichier>")))))
        return 3
    if os.path.exists(os.path.join(RACINE, "STOP")):
        print("STOP: fichier STOP présent, aucun lancement (G0).")
        return 6

    duree_max = int(routage["roles"][a.role].get("duree_max_min", routage.get("duree_max_min_par_defaut", 45)))
    r = lancer(routage, a.role, candidat, rang, prompt, a.jeu, a.titre, duree_max)
    # Repli à l'exécution : la CLI a échoué (code non nul, ou aucun message de l'agent) sans rendre
    # de RESULTAT : quota, modèle refusé, panne. Un agent qui a répondu sans ligne RESULTAT n'est
    # pas rejoué sur un autre modèle : c'est le prompt qu'il faut corriger.
    while r["verdict"] is None and not r["expire"] and (r["code_cli"] != 0 or r["sans_message"]):
        indispo = indispo + ("%s:%s" % (candidat["fournisseur"], candidat["modele"]),)
        suivant, rang2, ecartes = choisir(routage, a.role, indispo, a.auteur or None)
        if r.get("sans_accord"):
            print("SANS-ACCORD: %s %s non lancé, accord expiré ou épuisé (Q1)" % (candidat["fournisseur"], candidat["modele"]))
        else:
            print("ECHEC-CLI: %s %s a rendu le code %d sans message exploitable (voir %s)" % (
                candidat["fournisseur"], candidat["modele"], r["code_cli"], os.path.relpath(r["journal"], RACINE)))
        if suivant is None:
            break
        candidat, rang = suivant, rang2
        print("REPLI: %s passe au choix n° %d (%s %s, effort %s)%s" % (
            a.role, rang + 1, candidat["fournisseur"], candidat["modele"], candidat["effort"],
            " ; mode dégradé : " + candidat["degrade"] if candidat.get("degrade") else ""))
        r = lancer(routage, a.role, candidat, rang, prompt, a.jeu, a.titre, duree_max)

    print(r["final"].strip()[-6000:])
    print("DELEGATION: %s | %s %s effort %s | %d s | journal %s" % (
        a.role, candidat["fournisseur"], candidat["modele"], candidat["effort"], r["duree_s"],
        os.path.relpath(r["journal"], RACINE)))
    if r["expire"]:
        print("DUREE: dépassée (%d min) ; processus arrêté." % duree_max)
        return 8
    if r.get("fige"):
        print("FIGE: aucune activité pendant %d min ; agent arrêté, aucun repli n'a abouti." % silence_max_min(routage, a.role))
        return 9
    return 0 if r["verdict"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())

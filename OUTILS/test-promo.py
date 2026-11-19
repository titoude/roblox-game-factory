#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôles locaux sans réseau, sans vidéo valide et sans ffmpeg.

Usage : python OUTILS/test-promo.py ; une ligne par contrôle, code 0 si tout passe.
Les témoins de sources sont des textes non vides dans un dossier temporaire.
Ils prouvent les contrôles et la génération, jamais un encodage réel.
"""
import contextlib
import copy
import io
import json
import runpy
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

OUTILS = Path(__file__).resolve().parent
m = runpy.run_path(str(OUTILS / "monter-video.py"))
d = runpy.run_path(str(OUTILS / "decision-promo.py"))
echecs = []


def verifier(nom, condition):
    print(("ok     " if condition else "ECHEC  ") + nom)
    if not condition:
        echecs.append(nom)


def refuse(plan, base):
    try:
        m["valider"](plan, base)
    except (ValueError, KeyError, TypeError):
        return True
    return False


with tempfile.TemporaryDirectory(prefix="tests-promo-") as tmp:
    base = Path(tmp)
    plan = json.loads((OUTILS / "GABARITS/video.plan.exemple.json").read_text(encoding="utf-8"))
    for clip in plan["clips"]:
        m["ecrire_sur"](base / clip["source"], "Témoin texte, pas une vidéo.\n")
    verifier("plan valide", m["valider"](plan, base) == [])
    for nom, changer in [
        ("musique sans licence refusée", lambda p: p.update(musique={"source": "sources/depart.mp4", "origine": "originale"})),
        ("musique sans origine refusée", lambda p: p.update(musique={"source": "sources/depart.mp4", "licence": "CC0"})),
        ("accroche trop longue refusée", lambda p: p.update(accroche="un deux trois quatre cinq six sept huit neuf")),
        ("chevauchement refusé", lambda p: p["sous_titres"][1].update(debut_s=7)),
        ("durée trop courte refusée", lambda p: p.update(duree_cible_s=14)),
        ("durée trop longue refusée", lambda p: p.update(duree_cible_s=61)),
        ("CTA sans nom exact refusé", lambda p: p.update(cta="Joue à un autre jeu")),
        ("source absente refusée", lambda p: p["clips"][0].update(source="absent.mp4")),
        ("durées incohérentes refusées", lambda p: p["clips"][0].update(fin_s=11)),
        ("centre invalide refusé", lambda p: p["clips"][0].update(centre_x=1.1)),
        ("nombre non fini refusé", lambda p: p.update(duree_cible_s=float("nan"))),
    ]:
        p = copy.deepcopy(plan)
        changer(p)
        verifier(nom, refuse(p, base))
    p = copy.deepcopy(plan)
    p["duree_cible_s"] = 40
    p["clips"][1]["fin_s"] = 30
    verifier("avertissement 31–60 secondes", bool(m["valider"](p, base)))
    cmds = m["commandes"](plan, base)
    codec = ["-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "2"]
    crop = "crop=trunc(min(iw\\,ih*9/16)/2)*2:trunc(min(ih\\,iw*16/9)/2)*2:max(0\\,min(iw-ow\\,iw*0.5-ow/2)):(ih-oh)/2,scale=1080:1920,setsar=1,fps=30,setpts=PTS-STARTPTS"
    attendu = ["ffmpeg", "-n", "-ss", "2", "-i", str((base / "sources/depart.mp4").resolve()),
               "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "10", "-map", "0:v:0", "-map", "1:a:0",
               "-vf", crop, "-af", "asetpts=PTS-STARTPTS"] + codec + ["clip-0.mp4"]
    verifier("commande exacte découpe / crop / scale / cadence / H264", cmds[0] == attendu)
    verifier("concat exact avant sous-titres", cmds[2] == ["ffmpeg", "-n", "-i", "clip-0.mp4", "-i", "clip-1.mp4", "-filter_complex",
             "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]"] + codec + ["assemble.mp4"])
    verifier("sous-titres exacts après concat", cmds[3] == ["ffmpeg", "-n", "-i", "assemble.mp4", "-vf", "subtitles=texte.srt"] + codec + ["titre.mp4"])
    verifier("normalisation exacte après sous-titres", cmds[4] == ["ffmpeg", "-n", "-i", "titre.mp4", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:v", "copy", "-c:a", "aac", "sans-musique.mp4"])
    p = copy.deepcopy(plan)
    p["musique"] = {"source": "sources/depart.mp4", "origine": "composition originale fictive", "licence": "CC0 fictive"}
    m["valider"](p, base)
    musique = m["commandes"](p, base)
    verifier("version sans musique et mix normalisé distinct", len(musique) == 6 and musique[4][-1] == "sans-musique.mp4" and musique[5][-1] == "avec-musique.mp4" and "loudnorm=I=-16:TP=-1.5:LRA=11" in musique[5][musique[5].index("-filter_complex") + 1])
    verifier("aucune commande n'écrase un fichier", all(c[1] == "-n" and "-y" not in c for c in musique))
    attendu_srt = ("1\n00:00:00,000 --> 00:00:03,000\nPeux-tu atteindre cette île ?\n\n"
                   "2\n00:00:03,000 --> 00:00:07,500\nUn saut pour rejoindre la passerelle\n\n"
                   "3\n00:00:10,000 --> 00:00:16,500\nVoici le résultat du parcours\n\n"
                   "4\n00:00:17,000 --> 00:00:20,000\nJoue à Îlot Démo, lien du profil\n")
    verifier("SRT complet exact avec accroche et CTA", m["srt"](plan) == attendu_srt)
    fichier = base / "demo.plan.json"
    m["ecrire_sur"](fichier, json.dumps(plan, ensure_ascii=False))
    avant = sorted(str(p) for p in base.rglob("*"))
    out = io.StringIO()
    # main conserve son dictionnaire global propre à runpy.
    with patch.dict(m["main"].__globals__, {"trouver": lambda nom: None}), contextlib.redirect_stdout(out):
        code = m["main"](["monter", str(fichier)])
    verifier("ffmpeg absent : code 3, message et aucune écriture", code == 3 and "ffmpeg absent : étape à faire quand il sera posé par le propriétaire" in out.getvalue() and avant == sorted(str(p) for p in base.rglob("*")))
    with contextlib.redirect_stdout(io.StringIO()):
        code = m["main"](["srt", str(fichier)])
    verifier("sous-commande SRT écrit le contenu exact", code == 0 and (m["dossier"](fichier) / "texte.srt").read_text(encoding="utf-8") == attendu_srt)
    try:
        m["ecrire_sur"](fichier, "autre contenu")
        protege = False
    except ValueError:
        protege = True
    verifier("écriture différente existante refusée", protege)

    journal = OUTILS / "GABARITS/JOURNAL-VIDEOS.exemple.csv"
    exemples = d["lire"](journal)
    verifier("exemple : 12 vidéos, 24 relevés, données manquantes", len(exemples) == 24 and len({(r['plateforme'], r['id_video']) for r in exemples}) == 12 and exemples[-1]["nouveaux_joueurs_attribues"] is None)
    maintenant = datetime(2026, 11, 16, tzinfo=timezone.utc)
    seuils = d["SEUILS_DEFAUT"]
    modele = copy.deepcopy(exemples[1])

    def video(i, **valeurs):
        r = copy.deepcopy(modele)
        r.update(id_video=str(i), vues=2000., nouveaux_joueurs_attribues=0., minutes_de_travail=10.,
                 presentations=3000., vues_engagees=900., choix_de_regarder_pct=65., duree_moyenne_vue_pct=80.)
        r.update(valeurs)
        return r

    def analyse(lignes, **kw):
        return d["analyser"](lignes, seuils, maintenant, **kw)

    cas = [
        ("attendre", [video(1, presentations=30.)], {}),
        ("ameliorer_promo", [video(1, choix_de_regarder_pct=40.)], {}),
        ("continuer", [video(1, nouveaux_joueurs_attribues=6.), video(2, nouveaux_joueurs_attribues=7.)], {}),
        ("arreter_promo", [video(i) for i in range(12)], {}),
        ("ameliorer_jeu", [video(i, nouveaux_joueurs_attribues=3.) for i in range(6)], {"p7": "echec"}),
        ("jeu_suivant", [video(1)], {"cohortes": 2}),
        ("jeu_suivant", [video(i) for i in range(12)], {"autre": "absent"}),
    ]
    for attendu, lignes, kw in cas:
        verifier("verdict " + attendu + " " + str(kw), analyse(lignes, **kw)["verdict"] == attendu)
    verifier("case vide n'est jamais zéro", analyse([video(i, nouveaux_joueurs_attribues=None) for i in range(6)])["verdict"] == "attendre")
    verifier("vidéo trop jeune ignorée", not analyse([video(1, publication=maintenant)])["murs"])
    verifier("relevé 24h ignoré", not analyse([video(1, releve="24h")])["murs"])
    verifier("plafond 12 exige vidéos mûres", analyse([video(i, publication=maintenant) for i in range(12)])["verdict"] == "attendre")
    verifier("11 vidéos sous plafond : revoir CTA", analyse([video(i) for i in range(11)])["verdict"] == "ameliorer_promo")
    verifier("plafond 8 heures même sans exposition", analyse([video(1, minutes_de_travail=480., presentations=1.)])["verdict"] == "arreter_promo")
    verifier("travail jamais doublé 24h et 7j", analyse([video(1, minutes_de_travail=240.), video(1, releve="24h", minutes_de_travail=200.)])["minutes"] == 240)
    verifier("plateformes séparées pour confirmation", analyse([video(1, nouveaux_joueurs_attribues=6.), video(2, plateforme="tiktok", nouveaux_joueurs_attribues=6.)])["verdict"] != "continuer")
    verifier("TikTok sans vu/balayé : raccourcir", analyse([video(1, plateforme="tiktok", choix_de_regarder_pct=None, presentations=None, duree_moyenne_vue_pct=50.)])["diagnostics"][("tiktok", "1")] == "raccourcir")
    verifier("visionnage insuffisant : pas de faux échec", analyse([video(1, vues_engagees=299., duree_moyenne_vue_pct=20.)])["diagnostics"][("youtube", "1")] == "preuve_insuffisante")
    verifier("exemple : continuer sans mélanger plateformes", analyse(exemples)["verdict"] == "continuer")
    rapport = d["rapport"](analyse(exemples), "2026-11-16", "attend", seuils)
    verifier("rapport : faits calculs dénominateurs verdict action", all(t in rapport for t in ["Faits", "Calculs", "/ 2000.0 vues", "Verdict", "Action suivante", "Publication bloquée"]))

sys.exit(1 if echecs else 0)

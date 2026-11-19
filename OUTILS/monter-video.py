#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Montage local, bibliothèque standard, sans réseau.

Usage : monter-video.py verifier|commandes|monter|srt <plan>
Chemins sources relatifs au plan. Sorties dans sorties/<nom du plan>/.
commandes prépare seulement le SRT et imprime des commandes PowerShell,
à lancer depuis le dossier indiqué. Aucun média n'est exécuté en simulation.
Codes : 0 succès, 2 entrée invalide, 3 ffmpeg absent, 4 montage invalide.
Les sources sont supposées assez larges ; son=false remplace leur son par
du silence. Avec son=true (défaut), chaque source doit avoir une piste audio.
"""
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
FFMPEG_ABSENT = 3


def ecrire_sur(chemin, texte):
    """Temporaire, relecture, remplacement ; conserve un ancien fichier différent."""
    if not texte:
        raise ValueError("écriture vide refusée")
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    if chemin.exists():
        if chemin.read_text(encoding="utf-8") == texte:
            return
        raise ValueError(f"fichier existant différent : {chemin}")
    fd, nom = tempfile.mkstemp(dir=chemin.parent, suffix=".tmp")
    tmp = Path(nom)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(texte)
        if tmp.read_text(encoding="utf-8") != texte:
            raise ValueError("écriture incomplète")
        os.replace(tmp, chemin)
    finally:
        tmp.unlink(missing_ok=True)


def nombre(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError("nombre fini attendu")
    return v


def texte(v):
    if not isinstance(v, str) or not v.strip() or any(c in v for c in "\r\n\x00"):
        raise ValueError("texte non vide sur une ligne attendu")
    return v


def source(base, nom):
    chemin = (base / texte(nom)).resolve()
    if not chemin.is_file() or chemin.stat().st_size == 0:
        raise ValueError(f"source absente ou vide : {chemin}")
    return chemin


def valider(plan, base):
    texte(plan["jeu"])
    accroche = texte(plan["accroche"])
    if len(accroche.split()) > 8:
        raise ValueError("accroche : 8 mots au plus")
    cta = texte(plan["cta"])
    if not re.search(r"(?<!\w)" + re.escape(plan["jeu"]) + r"(?!\w)", cta):
        raise ValueError("CTA : nom exact du jeu requis")
    cible = nombre(plan["duree_cible_s"])
    if not 15 <= cible <= 60:
        raise ValueError("durée : 15 à 60 s")
    if not isinstance(plan["clips"], list) or not plan["clips"]:
        raise ValueError("clips manquants")
    total = 0
    for clip in plan["clips"]:
        source(base, clip["source"])
        debut, fin = nombre(clip["debut_s"]), nombre(clip["fin_s"])
        if debut < 0 or fin <= debut or not 0 <= nombre(clip["centre_x"]) <= 1:
            raise ValueError("clip : temps ou centre_x invalides")
        if not isinstance(clip.get("son", True), bool):
            raise ValueError("son : booléen attendu")
        total += fin - debut
    if abs(total - cible) > 0.001:
        raise ValueError("somme des clips différente de la durée cible")
    # Accroche 0–3 s et CTA sur les 3 dernières secondes sont aussi incrustés.
    precedent = 3
    if not isinstance(plan["sous_titres"], list):
        raise ValueError("sous_titres : liste attendue")
    for st in plan["sous_titres"]:
        debut, fin = nombre(st["debut_s"]), nombre(st["fin_s"])
        texte(st["texte"])
        if debut < precedent or fin <= debut or fin > total - 3:
            raise ValueError("sous-titres : chevauchement ou hors fenêtre 3 s / CTA final")
        if round(fin * 1000) <= round(debut * 1000):
            raise ValueError("sous-titre trop court")
        precedent = fin
    musique = plan.get("musique")
    if musique is not None:
        texte(musique["origine"])
        texte(musique["licence"])
        source(base, musique["source"])
    return ["durée hors de la plage conseillée 15–30 s"] if total > 30 else []


def horodatage(s):
    ms = round(s * 1000)
    sec, ms = divmod(ms, 1000)
    minute, sec = divmod(sec, 60)
    heure, minute = divmod(minute, 60)
    return f"{heure:02}:{minute:02}:{sec:02},{ms:03}"


def srt(plan):
    lignes = [{"debut_s": 0, "fin_s": 3, "texte": plan["accroche"]}]
    lignes += plan["sous_titres"]
    lignes += [{"debut_s": plan["duree_cible_s"] - 3,
                "fin_s": plan["duree_cible_s"], "texte": plan["cta"]}]
    return "\n".join(f"{i}\n{horodatage(st['debut_s'])} --> {horodatage(st['fin_s'])}\n{st['texte']}\n"
                     for i, st in enumerate(lignes, 1))


def trouver(nom):
    local = RACINE / "OUTILS" / "bin" / (nom + (".exe" if os.name == "nt" else ""))
    return shutil.which(nom) or (str(local) if local.is_file() else None)


def dossier(plan_path):
    return plan_path.parent / "sorties" / plan_path.name.removesuffix(".plan.json")


def commandes(plan, base, executable="ffmpeg"):
    """Arguments exacts, sans shell. Tous les chemins produits sont relatifs au cwd."""
    codec = ["-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "2"]
    resultat = []
    for i, clip in enumerate(plan["clips"]):
        duree = clip["fin_s"] - clip["debut_s"]
        cmd = [executable, "-n", "-ss", str(clip["debut_s"]), "-i", str(source(base, clip["source"]))]
        if not clip.get("son", True):
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        filtre = ("crop=trunc(min(iw\\,ih*9/16)/2)*2:trunc(min(ih\\,iw*16/9)/2)*2:"
                  f"max(0\\,min(iw-ow\\,iw*{clip['centre_x']}-ow/2)):(ih-oh)/2,"
                  "scale=1080:1920,setsar=1,fps=30,setpts=PTS-STARTPTS")
        cmd += ["-t", str(duree), "-map", "0:v:0", "-map", "0:a:0" if clip.get("son", True) else "1:a:0",
                "-vf", filtre, "-af", "asetpts=PTS-STARTPTS"] + codec + [f"clip-{i}.mp4"]
        resultat.append(cmd)
    cmd = [executable, "-n"]
    for i in range(len(plan["clips"])):
        cmd += ["-i", f"clip-{i}.mp4"]
    flux = "".join(f"[{i}:v:0][{i}:a:0]" for i in range(len(plan["clips"])))
    cmd += ["-filter_complex", flux + f"concat=n={len(plan['clips'])}:v=1:a=1[v][a]",
            "-map", "[v]", "-map", "[a]"] + codec + ["assemble.mp4"]
    resultat.append(cmd)
    resultat.append([executable, "-n", "-i", "assemble.mp4", "-vf", "subtitles=texte.srt"] + codec + ["titre.mp4"])
    normal = "loudnorm=I=-16:TP=-1.5:LRA=11"
    resultat.append([executable, "-n", "-i", "titre.mp4", "-af", normal, "-ar", "48000",
                     "-c:v", "copy", "-c:a", "aac", "sans-musique.mp4"])
    if plan.get("musique"):
        resultat.append([executable, "-n", "-i", "titre.mp4", "-stream_loop", "-1", "-i",
                         str(source(base, plan["musique"]["source"])), "-filter_complex",
                         "[0:a][1:a]amix=inputs=2:duration=first," + normal + "[a]",
                         "-map", "0:v:0", "-map", "[a]", "-t", str(plan["duree_cible_s"]),
                         "-c:v", "copy", "-c:a", "aac", "-ar", "48000", "avec-musique.mp4"])
    return resultat


def controler(probe, fichier, duree):
    data = json.loads(subprocess.check_output([probe, "-v", "error", "-show_streams", "-show_format",
                                               "-of", "json", str(fichier)], text=True))
    videos = [s for s in data["streams"] if s["codec_type"] == "video"]
    if (not videos or (videos[0]["width"], videos[0]["height"]) != (1080, 1920)
            or not any(s["codec_type"] == "audio" for s in data["streams"])
            or abs(float(data["format"]["duration"]) - duree) > 0.25):
        raise ValueError("ffprobe : dimensions, durée ou son incorrects")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["verifier", "commandes", "monter", "srt"])
    parser.add_argument("plan", type=Path)
    args = parser.parse_args(argv)
    if (RACINE / "STOP").exists():
        print("STOP présent : arrêt")
        return 2
    # Aucun dossier ni SRT créé si l'exécutable manque, même avec un plan invalide.
    ffmpeg = trouver("ffmpeg")
    if args.action == "monter" and not ffmpeg:
        print("ffmpeg absent : étape à faire quand il sera posé par le propriétaire")
        return FFMPEG_ABSENT
    try:
        path = args.plan.resolve()
        plan = json.loads(path.read_text(encoding="utf-8-sig"))
        for avertissement in valider(plan, path.parent):
            print("AVERTISSEMENT : " + avertissement)
        if args.action == "verifier":
            print("Plan valide")
            return 0
        sortie = dossier(path)
        cmds = commandes(plan, path.parent, ffmpeg or "ffmpeg")
        if args.action in ("srt", "commandes"):
            ecrire_sur(sortie / "texte.srt", srt(plan))
            print(f"SRT : {sortie / 'texte.srt'}")
            if args.action == "commandes":
                quote = lambda s: "'" + s.replace("'", "''") + "'"
                print("Set-Location -LiteralPath " + quote(str(sortie)))
                for cmd in cmds:
                    print("& " + " ".join(quote(s) for s in cmd))
            return 0
        # Travail dans un dossier neuf : aucun fichier existant écrasé.
        if sortie.exists():
            existants = list(sortie.iterdir())
            if (any(p.name != "texte.srt" for p in existants)
                    or ((sortie / "texte.srt").exists()
                        and (sortie / "texte.srt").read_text(encoding="utf-8") != srt(plan))):
                raise ValueError("sorties déjà présentes : choisir un nouvel identifiant de plan")
        sortie.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=sortie.parent, prefix="montage-") as tmp:
            travail = Path(tmp)
            ecrire_sur(travail / "texte.srt", srt(plan))
            for cmd in cmds:
                subprocess.run(cmd, cwd=travail, check=True)
                if (travail / cmd[-1]).stat().st_size == 0:
                    raise ValueError("sortie vidéo vide")
            probe = trouver("ffprobe")
            for nom in ("sans-musique.mp4", "avec-musique.mp4"):
                if (travail / nom).exists() and probe:
                    controler(probe, travail / nom, plan["duree_cible_s"])
            if not probe:
                print("ffprobe absent : dimensions, durée et son non vérifiés")
            # Ne conserve que les exports et le SRT, pas les intermédiaires lourds.
            for nom in ("texte.srt", "sans-musique.mp4", "avec-musique.mp4"):
                if (travail / nom).exists():
                    sortie.mkdir(exist_ok=True)
                    if nom == "texte.srt":
                        ecrire_sur(sortie / nom, srt(plan))
                    else:
                        (travail / nom).rename(sortie / nom)
        print(f"Montage : {sortie}")
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 4 if args.action == "monter" else 2


if __name__ == "__main__":
    sys.exit(main())

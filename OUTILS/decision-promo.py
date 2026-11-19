#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P11 documentaire, sans réseau ni dépendance à mesures-joueurs.py.

Usage : decision-promo.py <JOURNAL-VIDEOS.csv> [--p7 passe|echec|attend]
  [--cohortes-insuffisantes N] [--autre-canal inconnu|autorise|absent]
  [--date AAAA-MM-JJ] [--seuils fichier.json]
Une ligne 7j n'est mûre que sept jours après publication. Les compteurs 7j
sont cumulatifs : jamais additionnés aux 24h. minutes_de_travail est le
temps cumulé par vidéo, compté une fois (maximum des relevés).
P7 est fourni par l'opérateur : il atteste la maturité et les seuils produit.
Les lignes doivent être comparables dans une plateforme ; une attribution
par vidéo exige des liens distincts et des joueurs dédupliqués en amont.
Codes : 0 rapport écrit, 2 entrée invalide. Aucun verdict n'autorise à publier.
"""
import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SEUILS_DEFAUT = {
    "lot_initial": 6, "videos_max": 12, "presentations_min": 1000,
    "vues_engagees_min": 300, "choix_de_regarder_min_pct": 60,
    "duree_moyenne_vue_min_pct": 70, "vues_lot_min": 10000,
    "joueurs_pour_1000_min": 1, "piste_videos_min": 2,
    "piste_joueurs_pour_1000_min": 3, "piste_vues_min": 1000,
    "travail_max_heures": 8, "cohortes_insuffisantes_max": 2,
}
CHAMPS = ("plateforme,id_video,date_publication_utc,duree_s,angle,accroche,cta,lien_partage,releve,"
          "vues,vues_engagees,presentations,choix_de_regarder_pct,duree_moyenne_vue_pct,"
          "partages,abonnes_gagnes,clics,nouveaux_joueurs_attribues,minutes_de_travail").split(",")
NUMERIQUES = ["duree_s"] + CHAMPS[9:]


def lire(chemin):
    with Path(chemin).open(encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != CHAMPS:
            raise ValueError("colonnes attendues : " + ",".join(CHAMPS))
        lignes, cles, constantes = [], set(), {}
        for r in lecteur:
            if None in r or any(v is None for v in r.values()):
                raise ValueError("ligne CSV incomplète")
            r = {k: v.strip() for k, v in r.items()}
            r["plateforme"] = r["plateforme"].lower()
            if r["plateforme"] not in ("youtube", "tiktok") or r["releve"] not in ("24h", "7j"):
                raise ValueError("plateforme youtube|tiktok et relevé 24h|7j requis")
            if any(not r[k] for k in CHAMPS[:7]):
                raise ValueError("identité de vidéo incomplète")
            publication = datetime.fromisoformat(r["date_publication_utc"].replace("Z", "+00:00"))
            if publication.utcoffset() != timedelta(0):
                raise ValueError("date_publication_utc : fuseau UTC requis")
            r["publication"] = publication
            cle = (r["plateforme"], r["id_video"])
            if (*cle, r["releve"]) in cles:
                raise ValueError("relevé en double")
            cles.add((*cle, r["releve"]))
            identite = tuple(r[k] for k in CHAMPS[2:8])
            if cle in constantes and constantes[cle] != identite:
                raise ValueError("identité incohérente entre relevés")
            constantes[cle] = identite
            for k in NUMERIQUES:
                r[k] = float(r[k]) if r[k] else None
                v = r[k]
                if v is not None and (not math.isfinite(v) or (v < 0 and k != "abonnes_gagnes")):
                    raise ValueError(f"nombre invalide : {k}")
                if v is not None and k not in ("duree_s", "choix_de_regarder_pct", "duree_moyenne_vue_pct", "minutes_de_travail") and not v.is_integer():
                    raise ValueError(f"compteur entier requis : {k}")
            if r["duree_s"] is None or r["duree_s"] <= 0:
                raise ValueError("durée positive requise")
            if r["choix_de_regarder_pct"] is not None and r["choix_de_regarder_pct"] > 100:
                raise ValueError("choix de regarder supérieur à 100 %")
            lignes.append(r)
    return lignes


def ratio(r):
    if r["vues"] and r["nouveaux_joueurs_attribues"] is not None and r["lien_partage"]:
        return 1000 * r["nouveaux_joueurs_attribues"] / r["vues"]
    return None


def diagnostic(r, s):
    if r["plateforme"] == "youtube":
        if r["presentations"] is None or r["presentations"] < s["presentations_min"] or r["choix_de_regarder_pct"] is None:
            return "preuve_insuffisante"
        if r["choix_de_regarder_pct"] < s["choix_de_regarder_min_pct"]:
            return "changer_accroche"
        if r["vues_engagees"] is None or r["vues_engagees"] < s["vues_engagees_min"]:
            return "preuve_insuffisante"
    if r["duree_moyenne_vue_pct"] is None:
        return "preuve_insuffisante"
    if 15 <= r["duree_s"] <= 30 and r["duree_moyenne_vue_pct"] < s["duree_moyenne_vue_min_pct"]:
        return "raccourcir"
    taux = ratio(r)
    if taux is not None and r["vues"] >= s["piste_vues_min"] and taux >= s["piste_joueurs_pour_1000_min"]:
        return "piste"
    return "preuve_insuffisante"


def analyser(lignes, s, maintenant, p7="attend", cohortes=0, autre="inconnu"):
    murs = [r for r in lignes if r["releve"] == "7j" and maintenant - r["publication"] >= timedelta(days=7)]
    diagnostics = {(r["plateforme"], r["id_video"]): diagnostic(r, s) for r in murs}
    travail = {}
    for r in lignes:
        cle = (r["plateforme"], r["id_video"])
        if r["minutes_de_travail"] is not None:
            travail[cle] = max(travail.get(cle, 0), r["minutes_de_travail"])
    minutes = sum(travail.values())
    groupes, pistes, arrets, conversions = [], [], [], []
    for plateforme in ("youtube", "tiktok"):
        lot = [r for r in murs if r["plateforme"] == plateforme]
        if not lot:
            continue
        # Un champ absent invalide le ratio du lot entier, sans remplacer par zéro.
        complet = all(r["vues"] is not None and r["nouveaux_joueurs_attribues"] is not None and r["lien_partage"] for r in lot)
        vues = sum(r["vues"] for r in lot) if all(r["vues"] is not None for r in lot) else None
        joueurs = sum(r["nouveaux_joueurs_attribues"] for r in lot) if complet else None
        taux = 1000 * joueurs / vues if complet and vues else None
        groupes.append((plateforme, len(lot), vues, joueurs, taux))
        qualifies = [r for r in lot if ratio(r) is not None and r["vues"] >= s["piste_vues_min"] and ratio(r) >= s["piste_joueurs_pour_1000_min"]]
        if len(qualifies) >= s["piste_videos_min"]:
            gagnant = max(qualifies, key=ratio)
            pistes.append(f"{plateforme} : 3 variantes de l'angle {gagnant['angle']}")
        if taux is not None and vues >= s["vues_lot_min"]:
            if taux >= s["joueurs_pour_1000_min"]:
                conversions.append(plateforme)
            else:
                for r in lot:
                    cle = (plateforme, r["id_video"])
                    if diagnostics[cle] == "preuve_insuffisante":
                        diagnostics[cle] = "revoir_cta"
                if len(lot) >= s["videos_max"] and len(qualifies) < s["piste_videos_min"]:
                    arrets.append(plateforme)

    def resultat(v, raison, action):
        return {"verdict": v, "raison": raison, "action": action, "murs": murs,
                "diagnostics": diagnostics, "groupes": groupes, "minutes": minutes,
                "travail_incomplet": len(travail) < len({(r['plateforme'], r['id_video']) for r in lignes})}

    if cohortes >= s["cohortes_insuffisantes_max"]:
        return resultat("jeu_suivant", "produit insuffisant : cohortes comparables après correction", "Archiver le bilan produit et choisir le prochain jeu.")
    if minutes >= 60 * s["travail_max_heures"]:
        return resultat("jeu_suivant" if autre == "absent" else "arreter_promo",
                        "plafond de travail atteint ; canal non qualifié si exposition insuffisante",
                        "Arrêter ce canal ; consigner les preuves disponibles et les autres canaux autorisés.")
    if conversions and p7 == "echec":
        return resultat("ameliorer_jeu", "bonne conversion ; P7 en échec", "Corriger l'arrivée et la boucle puis mesurer une seconde cohorte comparable.")
    if groupes and all(n >= s["videos_max"] for _, n, _, _, _ in groupes) and len(groupes) == len({r['plateforme'] for r in lignes}):
        return resultat("jeu_suivant" if autre == "absent" else "arreter_promo",
                        "plafond expérimental de vidéos atteint", "Arrêter les variantes ; archiver le bilan sans conclure à un échec du produit.")
    if pistes:
        return resultat("continuer", "piste confirmée sur au moins deux vidéos", "; ".join(pistes) + ". Respecter P7 et les plafonds avant diffusion.")
    actifs = {r["plateforme"] for r in lignes}
    if arrets and set(arrets) == actifs:
        return resultat("jeu_suivant" if autre == "absent" else "arreter_promo",
                        "acquisition insuffisante après le plafond de vidéos mûres", "Arrêter la méthode ; examiner un autre canal autorisé ou archiver le jeu.")
    causes = sorted(set(diagnostics.values()) - {"preuve_insuffisante", "piste"})
    if causes:
        actions = {"changer_accroche": "changer la première scène et sa phrase",
                   "raccourcir": "avancer le résultat et retirer les temps morts",
                   "revoir_cta": "revoir le CTA et le parcours ; si ≥100 clics et <10 joueurs, examiner clic→jeu"}
        return resultat("ameliorer_promo", ", ".join(causes), "; ".join(actions[c] for c in causes) + ". Après 6 vidéos, corriger la cause ; 12 maximum par plateforme.")
    return resultat("attendre", "aucune preuve mûre suffisante pour conclure", "Compléter les relevés et l'attribution ; attendre 7 jours après la dernière publication du lot initial.")


def rapport(resultat, date, p7, seuils):
    r = resultat
    lignes = [f"# Décision promotion — {date}", "", "## Faits déclarés (CSV, non vérifiés sur les plateformes)",
              f"Vidéos mûres à 7j : {len(r['murs'])}. P7 fourni : {p7}.",
              "Publication bloquée : compte du propriétaire et autorisation PLAFONDS.md § 3 requis ; cet outil ne publie rien.",
              "Seuils expérimentaux issus de la veille p2, à calibrer ; aucune norme de plateforme.",
              "24h et vidéos trop jeunes ignorés pour le verdict. Aucune moyenne de pourcentages.",
              "Comparabilité, liens distincts et attribution dédupliquée sont à vérifier humainement.",
              "", "## Calculs et dénominateurs",
              f"Travail : somme des maxima cumulés par vidéo = {r['minutes']:g} min / 60 = {r['minutes']/60:g} h.",
              "Travail incomplet : " + ("oui ; total connu seulement" if r["travail_incomplet"] else "non"),
              "Seuils utilisés : `" + json.dumps(seuils, ensure_ascii=False, sort_keys=True) + "`."]
    for plateforme, n, vues, joueurs, taux in r["groupes"]:
        lignes.append(f"- {plateforme}, {n} vidéos 7j : 1000 × {joueurs} joueurs / {vues} vues = {taux} joueurs/1000 (None = absent ou non défini).")
    for v in r["murs"]:
        cle = (v["plateforme"], v["id_video"])
        lignes.append(f"- {cle[0]}/{cle[1]} : {r['diagnostics'][cle]}. "
                      f"1000 × {v['nouveaux_joueurs_attribues']} / {v['vues']} vues = {ratio(v)} ; "
                      f"choix natif {v['choix_de_regarder_pct']} % ({v['presentations']} présentations) ; "
                      f"durée native {v['duree_moyenne_vue_pct']} % ({v['vues_engagees']} vues engagées).")
    lignes += ["", "## Verdict", r["verdict"], "", "Raison : " + r["raison"], "", "Action suivante : " + r["action"], ""]
    return "\n".join(lignes)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("journal", type=Path)
    parser.add_argument("--p7", choices=["passe", "echec", "attend"], default="attend")
    parser.add_argument("--cohortes-insuffisantes", type=int, default=0)
    parser.add_argument("--autre-canal", choices=["inconnu", "autorise", "absent"], default="inconnu")
    parser.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    parser.add_argument("--seuils", type=Path, default=RACINE / "CONNAISSANCES" / "seuils.json")
    args = parser.parse_args(argv)
    try:
        if (RACINE / "STOP").exists():
            raise ValueError("STOP présent : arrêt")
        if args.cohortes_insuffisantes < 0:
            raise ValueError("nombre de cohortes négatif")
        maintenant = datetime.fromisoformat(args.date).replace(tzinfo=timezone.utc)
        seuils = dict(SEUILS_DEFAUT)
        promo = json.loads(args.seuils.read_text(encoding="utf-8-sig")).get("promo", {})
        for k in seuils:
            if k in promo:
                v = promo[k]
                if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0:
                    raise ValueError(f"seuil promo invalide : {k}")
                seuils[k] = v
        resultat = analyser(lire(args.journal), seuils, maintenant, args.p7, args.cohortes_insuffisantes, args.autre_canal)
        contenu = rapport(resultat, args.date, args.p7, seuils)
        sortie = args.journal.parent / f"DECISION-PROMO-{args.date}.md"
        # Réutilise uniquement la fonction d'écriture locale, sans autre outil d'agent.
        import runpy
        runpy.run_path(str(Path(__file__).with_name("monter-video.py")))["ecrire_sur"](sortie, contenu)
        print(f"P11: {resultat['verdict']} | {resultat['raison']}")
        print(f"Rapport : {sortie}")
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sim-economie.py - simulateur de cadence pour la revue d'économie (PROCEDURES/03-REVUE-ECONOMIE.md).

Usage :
    python OUTILS/sim-economie.py <economie.json> [--sortie RAPPORT.md] [--json] [--seuils seuils.json]

Entrée : un fichier economie.json (modèle : OUTILS/GABARITS/economie.exemple.json).
Sortie : un rapport Markdown (cadence des achats, remboursements, jalons, offres) jugé contre
CONNAISSANCES/seuils.json, section "economie". Le verdict porte sur le profil "actif".

Modèle : pas d'une seconde. Le joueur achète l'objet débloqué qui minimise
(attente pour pouvoir payer + temps de remboursement). C'est une politique de joueur raisonnable,
pas une preuve de plaisir de jeu ni de rétention.

Action : "gain" pièces par action, "par_minute" actions, et en option "part_revenu_s" : chaque action
rapporte en plus ce nombre de secondes du revenu des générateurs en service (le geste reste utile
quand les générateurs dominent). Une amélioration de cible "action" multiplie les deux.

Remboursement (règle E3) : jugé sur CHAQUE exemplaire acheté, au prix payé, avec les multiplicateurs
permanents acquis à l'achat, à partir de la mise en service (le chantier est jugé à part). Le revenu
ajouté compte le revenu direct de l'exemplaire ET le supplément d'action qu'il entraîne quand l'action
est indexée (part_revenu_s) : il dépend donc du profil. Le tableau "Générateurs" ne donne que le
remboursement nominal du premier exemplaire.

Options de l'objet racine : "prix_entiers": true arrondit chaque prix de générateur à l'entier supérieur.
Les écarts entre achats sont rangés dans la fenêtre de leur début.

Non modélisés : revenu hors ligne, récompenses quotidiennes, bonus temporaires, aide entre joueurs,
offres payantes. Le rapport d'économie les chiffre à part, en minutes de revenu.

Code de sortie : 0 aucun échec, 1 au moins un échec, 2 entrée invalide.
Bibliothèque standard uniquement. Aucun accès réseau.
"""
import argparse
import json
import math
import os
import re
import sys
from decimal import ROUND_CEILING, Decimal, getcontext
from pathlib import Path

getcontext().prec = 60

TYPES_OFFRE_OK = {"confort", "temps", "expression", "acces"}
TYPES_OFFRE_INTERDITS = {
    "pouvoir": "vend du pouvoir contre d'autres joueurs (G6, E6)",
    "aleatoire": "objet aléatoire payant (E13)",
}
TYPES_OFFRE_SELON_JEU = {"monnaie", "multiplicateur"}
SEUILS_DEFAUT = {
    "premier_achat_max_s": 60, "ecart_max_0_10min_s": 120, "ecart_max_10_60min_s": 480,
    "ecart_max_apres_60min_s": 900, "payback_min_s": 30, "payback_max_s": 300,
    "chantier_max_s": 180, "contenu_actif_min_min": 90, "retard_lent_min_pct": 5,
}


def duree(s):
    if s is None:
        return "—"
    s = int(round(s))
    h, r = divmod(s, 3600)
    m, sec = divmod(r, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


def nombre(x):
    if x is None:
        return "—"
    if abs(x) >= 1000:
        return f"{x:,.0f}".replace(",", " ")
    return f"{x:.2f}".rstrip("0").rstrip(".").replace(".", ",")


class Entree(Exception):
    pass


def valider(eco):
    if not isinstance(eco, dict):
        raise Entree("le fichier doit contenir un objet JSON")
    gens = eco.get("generateurs")
    if not isinstance(gens, list) or not gens:
        raise Entree("'generateurs' doit être une liste non vide")
    ids = set()
    for g in gens:
        for champ in ("id", "cout", "revenu_s"):
            if champ not in g:
                raise Entree(f"générateur sans '{champ}' : {g}")
        if g["cout"] <= 0 or g["revenu_s"] <= 0:
            raise Entree(f"générateur '{g['id']}' : coût et revenu doivent être positifs")
        if g.get("croissance_cout", 1.0) < 1.0:
            raise Entree(f"générateur '{g['id']}' : croissance_cout inférieure à 1")
        if g["id"] in ids:
            raise Entree(f"identifiant en double : {g['id']}")
        ids.add(g["id"])
    for u in eco.get("ameliorations", []):
        for champ in ("id", "cout", "cible", "multiplicateur"):
            if champ not in u:
                raise Entree(f"amélioration sans '{champ}' : {u}")
        if u["id"] in ids:
            raise Entree(f"identifiant en double : {u['id']}")
        ids.add(u["id"])
        if u["cible"] not in ("action", "tout") and u["cible"] not in {g["id"] for g in gens}:
            raise Entree(f"amélioration '{u['id']}' : cible inconnue '{u['cible']}'")
        if u["multiplicateur"] <= 1 or u["cout"] <= 0:
            raise Entree(f"amélioration '{u['id']}' : multiplicateur > 1 et coût > 0 attendus")
    act = eco.get("action") or {}
    if float(act.get("part_revenu_s", 0)) < 0:
        raise Entree("action : 'part_revenu_s' ne peut pas être négatif")
    depart = float((eco.get("depart") or {}).get("cash", 0))
    if float(act.get("gain", 0)) * float(act.get("par_minute", 0)) <= 0 and depart < min(g["cout"] for g in gens):
        raise Entree("ni action rémunérée ni cash de départ suffisant : le joueur ne peut rien acheter")


class Sim:
    def __init__(self, eco, profil):
        self.eco = eco
        self.t = 0
        self.cash = float((eco.get("depart") or {}).get("cash", 0))
        self.gens = {g["id"]: g for g in eco["generateurs"]}
        self.ups = {u["id"]: u for u in eco.get("ameliorations", [])}
        self.poss = {i: 0 for i in self.gens}      # achetés, chantier compris
        self.actifs = {i: 0 for i in self.gens}    # construits, donc productifs
        self.achetes = set()
        self.mult = {i: 1.0 for i in self.gens}
        self.mult_action = 1.0
        self.mult_tout = 1.0
        self.chantiers = []
        self.jalons = {}
        self.achats = []
        self.delai = float(profil.get("delai_achat_s", 3))
        act = eco.get("action") or {}
        # Actions par seconde du profil, gain fixe par action, et part du revenu des générateurs
        # ajoutée à chaque action ("part_revenu_s" secondes de revenu des générateurs en service).
        self.cadence = float(act.get("par_minute", 0)) / 60.0 * float(profil.get("actions_facteur", 1.0))
        self.gain = float(act.get("gain", 0))
        self.part_revenu = float(act.get("part_revenu_s", 0))
        self.transactions = []   # (t, id, rang de l'exemplaire, coût payé, revenu marginal, chantier)
        self.fin = None
        self.blocage = None

    # --- revenus -------------------------------------------------------
    def revenu_gen(self, gid):
        return self.actifs[gid] * self.gens[gid]["revenu_s"] * self.mult[gid] * self.mult_tout

    def revenu_gens(self):
        return sum(self.revenu_gen(i) for i in self.gens)

    def revenu_action(self):
        par_action = self.gain * self.mult_tout + self.part_revenu * self.revenu_gens()
        return self.cadence * self.mult_action * par_action

    def revenu(self):
        return self.revenu_gens() + self.revenu_action()

    # --- conditions ----------------------------------------------------
    def valeur(self, nom):
        if nom == "t":
            return self.t
        if nom == "cash":
            return self.cash
        if nom == "revenu_s":
            return self.revenu()
        if nom in self.actifs:
            return self.actifs[nom]
        raise Entree(f"condition : nom inconnu '{nom}'")

    def vrai(self, expr):
        if not expr:
            return True
        for terme in re.split(r"\s+et\s+", expr.strip()):
            m = re.match(r"^achete:([\w-]+)$", terme)
            if m:
                if m.group(1) not in self.achetes:
                    return False
                continue
            m = re.match(r"^jalon:([\w-]+)$", terme)
            if m:
                if m.group(1) not in self.jalons:
                    return False
                continue
            m = re.match(r"^([\w-]+)\s*(>=|>|==)\s*([\d.]+)$", terme)
            if not m:
                raise Entree(f"condition illisible : '{terme}'")
            v, op, seuil = self.valeur(m.group(1)), m.group(2), float(m.group(3))
            if not ((op == ">=" and v >= seuil) or (op == ">" and v > seuil) or (op == "==" and v == seuil)):
                return False
        return True

    # --- achats --------------------------------------------------------
    def cout_gen(self, gid):
        g = self.gens[gid]
        if self.eco.get("prix_entiers"):
            # Prix arrondi à l'entier supérieur de coût × croissance^(rang-1), en calcul décimal exact :
            # en flottants, 5 600 000 × 1,1^3 donne 7 453 600,000000001 et l'arrondi ajoute une pièce.
            exact = Decimal(str(g["cout"])) * Decimal(str(g.get("croissance_cout", 1.0))) ** self.poss[gid]
            return int(exact.to_integral_value(rounding=ROUND_CEILING))
        return g["cout"] * (g.get("croissance_cout", 1.0) ** self.poss[gid])

    def effet_action(self):
        # Un revenu de générateur en plus augmente aussi le gain de l'action indexée sur ce revenu.
        return 1.0 + self.cadence * self.mult_action * self.part_revenu

    def candidats(self):
        res = []
        for gid, g in self.gens.items():
            if self.poss[gid] >= g.get("max", 1) or not self.vrai(g.get("debloque", "")):
                continue
            res.append(("gen", gid, g.get("nom", gid), self.cout_gen(gid),
                        g["revenu_s"] * self.mult[gid] * self.mult_tout * self.effet_action()))
        for uid, u in self.ups.items():
            if uid in self.achetes or not self.vrai(u.get("debloque", "")):
                continue
            if u["cible"] == "action":
                base = self.revenu_action()
            elif u["cible"] == "tout":
                base = self.revenu()
            else:
                base = self.revenu_gen(u["cible"]) * self.effet_action()
            delta = (u["multiplicateur"] - 1) * base
            if delta > 0:
                res.append(("amel", uid, u.get("nom", uid), float(u["cout"]), delta))
        return res

    def choisir(self):
        rev = self.revenu()
        meilleur, score_min = None, math.inf
        for c in self.candidats():
            cout, delta = c[3], c[4]
            manque = max(0.0, cout - self.cash)
            attente = 0.0 if manque == 0 else (manque / rev if rev > 0 else math.inf)
            score = attente + cout / delta
            if score < score_min:
                meilleur, score_min = c, score
        return meilleur

    def acheter(self, c):
        genre, ident, nom, cout, marginal = c
        self.cash -= cout
        if genre == "gen":
            self.poss[ident] += 1
            chantier = float(self.gens[ident].get("chantier_s", 0))
            self.transactions.append((self.t, ident, self.poss[ident], cout, marginal, chantier))
            if chantier > 0:
                self.chantiers.append((self.t + chantier, ident))
            else:
                self.actifs[ident] += 1
        else:
            u = self.ups[ident]
            self.achetes.add(ident)
            if u["cible"] == "action":
                self.mult_action *= u["multiplicateur"]
            elif u["cible"] == "tout":
                self.mult_tout *= u["multiplicateur"]
            else:
                self.mult[u["cible"]] *= u["multiplicateur"]
        self.achats.append((self.t, ident, nom, cout))

    def fini(self):
        expr = self.eco.get("fin_contenu")
        if expr:
            return self.vrai(expr)
        return all(n >= 1 for n in self.actifs.values()) and len(self.achetes) == len(self.ups)

    def lancer(self, duree_max):
        dernier = -math.inf
        while self.t <= duree_max:
            pret = [c for c in self.chantiers if c[0] <= self.t]
            for c in pret:
                self.actifs[c[1]] += 1
                self.chantiers.remove(c)
            for j in self.eco.get("jalons", []):
                if j["id"] not in self.jalons and self.vrai(j.get("condition", "")):
                    self.jalons[j["id"]] = self.t
            if self.fini():
                self.fin = self.t
                break
            cible = self.choisir()
            if cible is None and not self.chantiers:
                self.blocage = (self.t, "plus rien à acheter alors que la fin de contenu n'est pas atteinte")
                break
            if cible is not None and self.cash >= cible[3] and self.t - dernier >= self.delai:
                self.acheter(cible)
                dernier = self.t
            elif cible is not None and self.revenu() <= 0 and self.cash < cible[3] and not self.chantiers:
                self.blocage = (self.t, f"revenu nul et {cible[2]} hors de portée ({nombre(cible[3])})")
                break
            self.cash += self.revenu()
            self.t += 1
        return self


def analyser(sim, seuils, duree_max):
    fin = sim.fin if sim.fin is not None else min(sim.t, duree_max)
    temps = [a[0] for a in sim.achats]
    ecarts = []
    precedent = 0
    for t in temps:
        ecarts.append((precedent, t - precedent))
        precedent = t
    # Attente finale : jusqu'à la fin de la durée simulée, ou jusqu'à la mise en service du dernier chantier.
    if fin > precedent:
        ecarts.append((precedent, fin - precedent))

    def maxi(debut, limite):
        vals = [e for e in ecarts if debut <= e[0] < limite]
        return max(vals, key=lambda e: e[1]) if vals else None

    lignes = []

    def juger(nom, valeur, ok, attendu, detail=""):
        lignes.append({"mesure": nom, "valeur": valeur, "verdict": "PASSE" if ok else "ÉCHEC",
                       "attendu": attendu, "detail": detail})

    premier = temps[0] if temps else None
    juger("Premier achat", duree(premier), premier is not None and premier <= seuils["premier_achat_max_s"],
          f"≤ {duree(seuils['premier_achat_max_s'])}",
          f"{sim.achats[0][2]} à {nombre(sim.achats[0][3])}" if sim.achats else "aucun achat")
    for nom, debut, limite, cle in (("Écart maximal, 0 à 10 min", 0, 600, "ecart_max_0_10min_s"),
                                    ("Écart maximal, 10 à 60 min", 600, 3600, "ecart_max_10_60min_s"),
                                    ("Écart maximal, après 60 min", 3600, math.inf, "ecart_max_apres_60min_s")):
        e = maxi(debut, limite)
        if e is None:
            lignes.append({"mesure": nom, "valeur": "—", "verdict": "SANS OBJET", "attendu": f"≤ {duree(seuils[cle])}",
                           "detail": "aucun achat dans cette fenêtre"})
        else:
            juger(nom, duree(e[1]), e[1] <= seuils[cle], f"≤ {duree(seuils[cle])}", f"à partir de {duree(e[0])}")
    # Remboursement de chaque exemplaire acheté (règle E3) : prix réellement payé ÷ revenu ajouté par
    # l'exemplaire avec les multiplicateurs permanents acquis à l'achat. Compté à partir de la mise en
    # service : le chantier est jugé à part.
    hors = []
    pire = None
    for (t, ident, rang, cout, marginal, chantier) in sim.transactions:
        pb = cout / marginal if marginal > 0 else math.inf
        if pire is None or pb > pire[0]:
            pire = (pb, ident, rang, t)
        if pb < seuils["payback_min_s"] or pb > seuils["payback_max_s"]:
            hors.append((t, ident, rang, cout, pb, chantier))
    if sim.transactions:
        detail = f"{len(hors)} exemplaire(s) hors bornes sur {len(sim.transactions)}"
        if hors:
            h = hors[0]
            detail += f" ; premier : {h[1]} n°{h[2]} à {duree(h[0])} ({duree(h[4])})"
        juger("Remboursement de chaque exemplaire", f"max {duree(pire[0])} ({pire[1]} n°{pire[2]})", not hors,
              f"{duree(seuils['payback_min_s'])} à {duree(seuils['payback_max_s'])}", detail)
    if sim.blocage:
        juger("Blocage", duree(sim.blocage[0]), False, "aucun", sim.blocage[1])
    mini = seuils["contenu_actif_min_min"] * 60
    if sim.fin is not None:
        juger("Durée de contenu actif", duree(sim.fin), sim.fin >= mini, f"≥ {duree(mini)}", "fin de contenu atteinte")
    elif not sim.blocage:
        # Fin non atteinte : prouvé seulement si la durée simulée couvre le minimum demandé.
        if duree_max >= mini:
            lignes.append({"mesure": "Durée de contenu actif", "valeur": f"> {duree(duree_max)}", "verdict": "ALERTE",
                           "attendu": f"≥ {duree(mini)}",
                           "detail": "fin de contenu non atteinte dans la durée simulée : cadence non jugée au-delà"})
        else:
            juger("Durée de contenu actif", f"> {duree(duree_max)}", False, f"≥ {duree(mini)}",
                  "durée simulée plus courte que le minimum demandé : rien n'est prouvé (allonger duree_max_s)")
    rangs = {(t, ident): rang for t, ident, rang, *_ in sim.transactions}
    chronologie = []
    precedent = 0
    for t, ident, _, cout in sim.achats:
        # Pour le premier achat, l'écart est mesuré depuis le début de la simulation.
        chronologie.append({"temps_s": t, "id": ident, "exemplaire": rangs.get((t, ident)),
                            "cout": cout, "ecart_s": t - precedent})
        precedent = t
    return {"lignes": lignes, "ecarts": ecarts, "fin": sim.fin, "achats": sim.achats, "jalons": sim.jalons,
            "chronologie_achats": chronologie, "revenu_final": sim.revenu(), "hors_bornes": hors,
            "part_action": (sim.revenu_action() / sim.revenu() if sim.revenu() > 0 else 0.0)}


def juger_generateurs(eco, seuils):
    res = []
    precedent = None
    for g in eco["generateurs"]:
        payback = g["cout"] / g["revenu_s"]
        chantier = float(g.get("chantier_s", 0))
        defauts = []
        if payback < seuils["payback_min_s"]:
            defauts.append(f"remboursement sous {duree(seuils['payback_min_s'])}")
        if payback > seuils["payback_max_s"]:
            defauts.append(f"remboursement au-delà de {duree(seuils['payback_max_s'])}")
        if chantier > seuils["chantier_max_s"]:
            defauts.append(f"chantier au-delà de {duree(seuils['chantier_max_s'])}")
        ratio = ""
        if precedent:
            ratio = f"coût ×{g['cout'] / precedent['cout']:.1f}, revenu ×{g['revenu_s'] / precedent['revenu_s']:.1f}"
        res.append({"id": g["id"], "nom": g.get("nom", g["id"]), "cout": g["cout"], "revenu_s": g["revenu_s"],
                    "payback": payback, "chantier": chantier, "ratio": ratio, "defauts": defauts})
        precedent = g
    return res


def juger_offres(eco):
    res = []
    competitif = bool(eco.get("competitif", False))
    for o in eco.get("offres", []):
        typ = str(o.get("type", "")).lower()
        if typ in TYPES_OFFRE_OK:
            verdict, raison = "PASSE", ""
        elif typ in TYPES_OFFRE_INTERDITS:
            verdict, raison = "ÉCHEC", TYPES_OFFRE_INTERDITS[typ]
        elif typ in TYPES_OFFRE_SELON_JEU:
            if competitif:
                verdict, raison = "ÉCHEC", "jeu compétitif : vendre de la monnaie ou un multiplicateur vend du pouvoir (E6)"
            else:
                verdict, raison = "ALERTE", "à justifier : aucun effet sur un autre joueur, et texte de boutique exact"
        else:
            verdict, raison = "ÉCHEC", f"type inconnu '{typ}' (attendu : confort, temps, expression, acces)"
        if verdict == "PASSE" and not o.get("prix_robux"):
            verdict, raison = "ALERTE", "prix en Robux manquant"
        res.append({"id": o.get("id", "?"), "nom": o.get("nom", o.get("id", "?")), "type": typ,
                    "prix": o.get("prix_robux"), "verdict": verdict, "raison": raison})
    return res


def rapport(eco, seuils, resultats, gens, offres, duree_max, source):
    L = []
    L.append(f"# Simulation économique — {eco.get('jeu', '?')}")
    L.append("")
    L.append(f"Entrée : `{source}`. Seuils : `CONNAISSANCES/seuils.json`, section `economie`. Durée simulée : {duree(duree_max)} au plus.")
    L.append("Ce rapport est un **calcul** : pas d'une seconde, joueur qui achète l'objet au meilleur compromis attente + remboursement. "
             "Il ne mesure ni le plaisir de jeu ni la rétention, et rien n'y est vérifié en jeu.")
    L.append("")
    echec = False
    for nom, r in resultats.items():
        principal = nom == "actif"
        L.append(f"## Profil « {nom} »" + ("" if principal else " (information, hors verdict)"))
        L.append("")
        L.append("| Mesure | Valeur | Attendu | Verdict | Détail |")
        L.append("|---|---|---|---|---|")
        for x in r["lignes"]:
            L.append(f"| {x['mesure']} | {x['valeur']} | {x['attendu']} | {x['verdict']} | {x['detail']} |")
            if principal and x["verdict"] == "ÉCHEC":
                echec = True
        L.append("")
        part = str(round(r["part_action"] * 100, 1)).replace(".", ",")
        L.append(f"Achats : {len(r['achats'])}. Revenu en fin de simulation : {nombre(r['revenu_final'])} par seconde, "
                 f"dont {part} % venant de l'action du joueur.")
        if r["hors_bornes"]:
            L.append("")
            L.append("Exemplaires hors bornes de remboursement (15 premiers) :")
            L.append("")
            L.append("| Temps | Exemplaire | Coût payé | Remboursement | Chantier |")
            L.append("|---|---|---|---|---|")
            for (t, ident, rang, cout, pb, chantier) in r["hors_bornes"][:15]:
                L.append(f"| {duree(t)} | {ident} n°{rang} | {nombre(cout)} | {duree(pb)} | {duree(chantier)} |")
        if r["jalons"]:
            L.append("Jalons : " + ", ".join(f"{k} à {duree(v)}" for k, v in sorted(r["jalons"].items(), key=lambda kv: kv[1])) + ".")
        L.append("")
        if principal:
            L.append("### Chronologie des achats (profil actif)")
            L.append("")
            L.append("| Temps | Écart | Achat | Coût |")
            L.append("|---|---|---|---|")
            precedent = 0
            montres = r["achats"] if len(r["achats"]) <= 60 else r["achats"][:40] + r["achats"][-10:]
            for i, (t, _, nom_a, cout) in enumerate(montres):
                if len(r["achats"]) > 60 and i == 40:
                    L.append(f"| … | … | {len(r['achats']) - 50} achats non listés | … |")
                    precedent = r["achats"][-11][0]
                L.append(f"| {duree(t)} | {duree(t - precedent)} | {nom_a} | {nombre(cout)} |")
                precedent = t
            L.append("")
    L.append("## Générateurs")
    L.append("")
    L.append("| Générateur | Coût | Revenu/s | Remboursement | Chantier | Par rapport au précédent | Défauts |")
    L.append("|---|---|---|---|---|---|---|")
    for g in gens:
        if g["defauts"]:
            echec = True
        L.append(f"| {g['nom']} | {nombre(g['cout'])} | {nombre(g['revenu_s'])} | {duree(g['payback'])} | {duree(g['chantier'])} | "
                 f"{g['ratio'] or '—'} | {'ÉCHEC : ' + ' ; '.join(g['defauts']) if g['defauts'] else 'aucun'} |")
    L.append("")
    L.append("Remboursement nominal = coût du premier exemplaire ÷ revenu par seconde, sans amélioration, attendu entre "
             f"{duree(seuils['payback_min_s'])} et {duree(seuils['payback_max_s'])} ; chantier ≤ {duree(seuils['chantier_max_s'])}. "
             "Le remboursement de chaque exemplaire réellement acheté est jugé dans le tableau du profil.")
    L.append("")
    L.append("## Offres payantes")
    L.append("")
    if offres:
        L.append("| Offre | Type | Prix (Robux) | Verdict | Raison |")
        L.append("|---|---|---|---|---|")
        for o in offres:
            if o["verdict"] == "ÉCHEC":
                echec = True
            L.append(f"| {o['nom']} | {o['type']} | {o['prix'] if o['prix'] else '—'} | {o['verdict']} | {o['raison'] or '—'} |")
    else:
        L.append("Aucune offre déclarée.")
    L.append("")
    L.append(f"Jeu déclaré {'compétitif' if eco.get('competitif') else 'non compétitif'} : "
             "dans un jeu compétitif, monnaie et multiplicateur de revenu payants sont refusés.")
    L.append("")
    L.append("## Verdict de cadence")
    L.append("")
    L.append("**ÉCHEC** : au moins un seuil n'est pas tenu." if echec else
             "**PASSE** : aucun seuil jugé n'est en échec pour le profil actif (une ligne ALERTE ou SANS OBJET n'est pas une preuve).")
    L.append("Les lignes ALERTE demandent une justification écrite dans le rapport d'économie.")
    L.append("")
    return "\n".join(L), echec


def ecrire_sur(chemin, texte):
    tmp = str(chemin) + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(texte)
    with open(tmp, "r", encoding="utf-8") as f:
        if f.read() != texte or not texte:
            os.remove(tmp)
            raise OSError(f"écriture incomplète : {chemin} (disque plein ?)")
    os.replace(tmp, chemin)


def main():
    p = argparse.ArgumentParser(description="Simulateur de cadence économique de l'usine Roblox.")
    p.add_argument("economie")
    p.add_argument("--sortie")
    p.add_argument("--json", action="store_true")
    p.add_argument("--seuils")
    a = p.parse_args()
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8")
        except Exception:
            pass
    try:
        with open(a.economie, "r", encoding="utf-8-sig") as f:
            eco = json.load(f)
        valider(eco)
        chemin_seuils = Path(a.seuils) if a.seuils else Path(__file__).resolve().parent.parent / "CONNAISSANCES" / "seuils.json"
        seuils = dict(SEUILS_DEFAUT)
        if chemin_seuils.exists():
            with open(chemin_seuils, "r", encoding="utf-8-sig") as f:
                seuils.update({k: v for k, v in json.load(f).get("economie", {}).items() if k in SEUILS_DEFAUT})
        duree_max = int(eco.get("duree_max_s", 14400))
        profils = eco.get("profils") or {"actif": {"actions_facteur": 1.0, "delai_achat_s": 3},
                                         "lent": {"actions_facteur": 0.5, "delai_achat_s": 3}}
        if "actif" not in profils:
            raise Entree("le profil 'actif' est obligatoire")
        resultats = {nom: analyser(Sim(eco, pr).lancer(duree_max), seuils, duree_max) for nom, pr in profils.items()}
        # Poids du geste : si le joueur deux fois moins actif finit presque en même temps, l'action ne vaut rien.
        if "lent" in resultats and resultats["actif"]["fin"] and resultats["lent"]["fin"]:
            fa, fl = resultats["actif"]["fin"], resultats["lent"]["fin"]
            retard = (fl - fa) / fa * 100
            mini = float(seuils.get("retard_lent_min_pct", 5))
            resultats["lent"]["lignes"].append({
                "mesure": "Retard du joueur lent sur le joueur actif",
                "valeur": f"{str(round(retard, 1)).replace('.', ',')} %",
                "verdict": "PASSE" if retard >= mini else "ALERTE",
                "attendu": f"≥ {str(mini).replace('.', ',')} %",
                "detail": f"actif {duree(fa)}, lent {duree(fl)}" + ("" if retard >= mini else
                          " ; le geste du joueur ne pèse presque rien dans la progression")})
        gens = juger_generateurs(eco, seuils)
        offres = juger_offres(eco)
        texte, echec = rapport(eco, seuils, resultats, gens, offres, duree_max, a.economie)
    except (Entree, json.JSONDecodeError, OSError, KeyError, TypeError) as e:
        print(f"ENTRÉE INVALIDE : {e}", file=sys.stderr)
        return 2
    if a.sortie:
        ecrire_sur(a.sortie, texte)
        print(f"rapport écrit : {a.sortie}")
    if a.json:
        print(json.dumps({"echec": echec, "profils": {n: {"lignes": r["lignes"], "fin_s": r["fin"], "achats": len(r["achats"]),
                                                                      "chronologie_achats": r["chronologie_achats"], "jalons_s": r["jalons"]}
                                                       for n, r in resultats.items()},
                          "generateurs": gens, "offres": offres}, ensure_ascii=False, indent=2))
    elif not a.sortie:
        print(texte)
    print("VERDICT : " + ("ÉCHEC" if echec else "PASSE"))
    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())

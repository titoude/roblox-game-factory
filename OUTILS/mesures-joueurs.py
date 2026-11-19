#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mesures agrégées UTC, bibliothèque standard, lecture seule Open Cloud v2.
Codes : 0 succès (y compris verdict echec/attend et diagnostic sans identifiant),
2 entrée/configuration invalide, 3 identifiant absent en collecte, 4 HTTP 401/403,
5 plafond de requêtes atteint, 6 panne réseau/API/disque. Aucun etat.ps1 exécuté.
"""
import argparse
import csv
from datetime import date, datetime, timedelta, timezone
import io
import json
import math
from pathlib import Path
import re
import sys
from usine_opencloud import (BASE, PORTEES, Client as ClientCommun, Erreur,
                             ecrire_sur, identifiant, lire_json)

RACINE = Path(__file__).resolve().parent.parent
CHAMPS = ('nouveaux', 'actifs', 'sessions', 'minutes', 's_0_60', 's_61_180',
          's_181_600', 's_601_1800', 's_1801_plus', 'retours_j1', 'retours_j7')
ETAPES = ('arrivee', 'premiere_action', 'premier_achat', 'min_3', 'min_10')


class Client(ClientCommun):
    def lister(self, token='', taille=100, prefixe='j_'):
        return super().lister(token, taille, prefixe)


def dossier(slug):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise Erreur('Slug invalide')
    return RACINE / 'JEUX' / slug


def configuration(args):
    jeu = dossier(args.jeu)
    etat = lire_json(jeu / 'ETAT.json') if (jeu / 'ETAT.json').exists() else {}
    config = lire_json(jeu / 'mesures.json') if (jeu / 'mesures.json').exists() else {}
    univers = args.univers or etat.get('place', {}).get('universeId_prod')
    magasin = args.magasin or config.get('magasin')
    if not univers or not str(univers).isdigit():
        raise Erreur('Univers absent : --univers ou ETAT.json place.universeId_prod requis')
    if not isinstance(magasin, str) or not magasin.strip():
        raise Erreur('Magasin absent : --magasin ou mesures.json requis')
    return univers, magasin


def diagnostic(args):
    univers, magasin = configuration(args)
    nom, secret = identifiant(args.jeu)
    print(f'Identifiant : {nom} : ' + ('présent' if secret else 'absent'))
    print(f'À créer par le propriétaire : {nom} ; univers {univers} ; magasin {magasin}.')
    print('Portées : ' + ', '.join(PORTEES) + ' ; aucune écriture.')
    if not secret:
        for portee in PORTEES:
            print(portee + ' : non testée (identifiant absent)')
        return 0
    client = Client(univers, magasin, secret, args.base_url, maximum=3)
    try:
        page = client.lister(taille=1)
        print(PORTEES[0] + ' : accordée')
        entrees = page.get('dataStoreEntries', [])
        if entrees:
            client.lire(entrees[0]['id'])
            print(PORTEES[1] + ' : accordée')
        else:
            print(PORTEES[1] + ' : non testée (aucune clé disponible)')
    except Erreur as erreur:
        print(str(erreur))
        return erreur.code
    return 0


def jour(texte):
    valeur = date.fromisoformat(texte)
    if valeur.isoformat() != texte:
        raise Erreur('Jour attendu : AAAA-MM-JJ')
    return valeur


def valider(entree):
    cle = entree.get('id', '')
    if not re.fullmatch(r'j_\d{4}-\d{2}-\d{2}', cle):
        raise Erreur('Clé journalière invalide')
    jour(cle[2:])
    valeur = entree.get('value')
    if isinstance(valeur, str):
        valeur = json.loads(valeur)
    if not isinstance(valeur, dict) or not valeur:
        raise Erreur('Compteurs absents')
    resultat = {}
    for nom, n in valeur.items():
        # e_ : étapes d'entonnoir ; refus_, anomalie_ : compteurs d'incident lus par le battement ;
        # avis_ : notes du sondage en jeu (procédure 14).
        autorise = nom in CHAMPS or re.fullmatch(r'(e|refus|anomalie|avis)_[a-z0-9][a-z0-9_]{0,39}', nom)
        technique = re.fullmatch(r'_envoi_[A-Za-z0-9]+', nom)
        if not (autorise or technique) or type(n) is not int or n < 0:
            raise Erreur('Compteur invalide (contenu non affiché)')
        if autorise:
            resultat[nom] = n
    if not resultat:
        raise Erreur('Aucun compteur de mesure')
    return cle[2:], resultat


def lire_csv(chemin):
    if not chemin.exists():
        return {}
    resultat = {}
    with chemin.open(encoding='utf-8-sig', newline='') as f:
        for ligne in csv.DictReader(f):
            date_jour = ligne.pop('jour')
            _, compteurs = valider({'id': 'j_' + date_jour,
                                     'value': {k: int(v) for k, v in ligne.items() if v != ''}})
            if date_jour in resultat:
                raise Erreur('Jour CSV dupliqué')
            resultat[date_jour] = compteurs
    return resultat


def collecter(args):
    chemin = dossier(args.jeu) / '08-distribution/MESURES.csv'
    jours = lire_csv(chemin)
    if args.source.startswith('fichier:'):
        entrees = [json.loads(l) for l in Path(args.source[8:]).read_text(encoding='utf-8-sig').splitlines() if l.strip()]
    elif args.source == 'api':
        univers, magasin = configuration(args)
        nom, secret = identifiant(args.jeu)
        if not secret:
            raise Erreur(f'Identifiant absent : {nom} ; lancer diagnostic.', 3)
        entrees = Client(univers, magasin, secret, args.base_url, args.max_requetes).entrees('j_')
    else:
        raise Erreur('Source attendue : api ou fichier:<chemin.jsonl>')
    nombre = 0
    # Aucun remplacement avant validation complète : une panne préserve le CSV précédent.
    for entree in entrees:
        date_jour, compteurs = valider(entree)
        jours[date_jour] = compteurs
        nombre += 1
    if not jours:
        raise Erreur('Aucune mesure : CSV vide refusé')
    etapes = sorted({'e_' + e for e in ETAPES} | {k for v in jours.values() for k in v if k.startswith('e_')})
    autres = sorted({k for v in jours.values() for k in v if k.startswith(('refus_', 'anomalie_', 'avis_'))})
    colonnes = ['jour', *CHAMPS, *etapes, *autres]
    texte = io.StringIO(newline='')
    sortie = csv.DictWriter(texte, fieldnames=colonnes, lineterminator='\n')
    sortie.writeheader()
    for date_jour, compteurs in sorted(jours.items()):
        sortie.writerow(dict(compteurs, jour=date_jour))
    ecrire_sur(chemin, texte.getvalue())
    print(f'Collecte : {nombre} jours relus ; {len(jours)} jours conservés.')


def wilson(succes, total):
    if not total:
        return None
    z = 1.959963984540054
    p = succes / total
    den = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / den
    marge = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / den
    return (100 * (centre - marge), 100 * (centre + marge))


def calculer(jours, aujourd, seuils):
    dates = sorted(jour(j) for j in jours if jour(j) < aujourd)
    cohortes = []
    incomplet = not dates
    if dates:
        incomplet = any((dates[0] + timedelta(days=i)).isoformat() not in jours
                        for i in range((dates[-1] - dates[0]).days + 1))
    bases = {1: 0, 7: 0}
    retours = {1: 0, 7: 0}
    manque = {1: incomplet, 7: incomplet}
    for debut in dates:
        nouveaux = jours[debut.isoformat()].get('nouveaux')
        ligne = {'jour': debut.isoformat(), 'nouveaux': nouveaux}
        for n in (1, 7):
            retour = debut + timedelta(days=n)
            mur = retour < aujourd
            valeur = jours.get(retour.isoformat(), {}).get('retours_j' + str(n)) if mur else None
            if mur and (nouveaux is None or valeur is None):
                manque[n] = True
            if mur and nouveaux is not None and valeur is not None:
                if valeur > nouveaux:
                    raise Erreur('Retours supérieurs à la cohorte')
                bases[n] += nouveaux
                retours[n] += valeur
            ligne['j' + str(n)] = 100 * valeur / nouveaux if mur and nouveaux and valeur is not None else None
        cohortes.append(ligne)
    def somme(champ):
        valeurs = [jours[d.isoformat()].get(champ) for d in dates]
        return sum(valeurs) if valeurs and all(v is not None for v in valeurs) and not incomplet else None
    def ratio(a, b, facteur=1):
        return facteur * a / b if a is not None and b else None
    sessions, minutes = somme('sessions'), somme('minutes')
    j1 = None if manque[1] else ratio(retours[1], bases[1], 100)
    intervalle = wilson(retours[1], bases[1]) if j1 is not None else None
    moyenne = ratio(minutes, sessions)
    total = somme('nouveaux')
    etapes = sorted({'e_' + e for e in ETAPES} | {k for v in jours.values() for k in v if k.startswith('e_')})
    entonnoir = {k: ratio(somme(k), total, 100) for k in etapes}
    if manque[1] or bases[1] < seuils['cohorte_min'] or j1 is None or moyenne is None:
        verdict, raison = 'attend', 'donnée absente ou cohorte mûre insuffisante'
    elif j1 < seuils['j1_min_pct'] or moyenne < seuils['session_min_min']:
        verdict, raison = 'echec', 'J1 ou durée de session sous le seuil'
    else:
        verdict, raison = 'passe', 'cohorte, J1 et durée de session aux seuils'
    return dict(cohortes=cohortes, cohorte=bases[1], retours_j1=retours[1], j1=j1,
                cohorte_j7=bases[7], j7=None if manque[7] else ratio(retours[7], bases[7], 100),
                intervalle=intervalle, moyenne=moyenne,
                abandon_60=ratio(somme('s_0_60'), sessions, 100),
                abandon_180=ratio(somme('s_61_180'), sessions, 100), entonnoir=entonnoir,
                verdict=verdict, raison=raison, sessions=sessions, minutes=minutes,
                borne_sous_seuil=intervalle[0] < seuils['j1_min_pct'] if intervalle else None)


def afficher(v):
    return 'absent / trop jeune' if v is None else f'{v:.4f}' if isinstance(v, float) else str(v)


def juger(args):
    aujourd = jour(args.aujourdhui) if args.aujourdhui else datetime.now(timezone.utc).date()
    chemin = dossier(args.jeu) / '08-distribution'
    jours = lire_csv(chemin / 'MESURES.csv')
    seuils = lire_json(RACINE / 'CONNAISSANCES/seuils.json')
    r = calculer(jours, aujourd, seuils['beta'])
    nom = f'MESURES-{aujourd.isoformat()}.md'
    texte = f'# Mesures au {aujourd.isoformat()} UTC\n\n## Faits\n\n'
    texte += f'{len(jours)} jours collectés ; seuls les jours UTC terminés sont calculés.\n'
    texte += 'Agrégats par compte ; source, appareil et origine organique non vérifiables avec ce format.\n'
    texte += 'Les étapes sont cumulées par date de réalisation, pas par cohorte : leur ratio peut dépasser 100 %.\n\n'
    texte += '## Calculs\n\nJour | Nouveaux | J1 % | J7 %\n---|---:|---:|---:\n'
    for c in r['cohortes']:
        texte += ' | '.join(afficher(c[k]) for k in ('jour', 'nouveaux', 'j1', 'j7')) + '\n'
    for k in ('cohorte', 'retours_j1', 'j1', 'cohorte_j7', 'j7', 'sessions', 'minutes', 'moyenne', 'abandon_60', 'abandon_180'):
        texte += f'\n- {k} : {afficher(r[k])}'
    texte += '\n\nJ1 pondéré = somme retours J1 / somme nouveaux des cohortes mûres × 100.\n'
    texte += 'J1 mûr si date cohorte + 1 < aujourd’hui ; J7 mûr si date cohorte + 7 < aujourd’hui.\n'
    texte += 'Durée moyenne = minutes / sessions ; abandons = tranche / sessions × 100.\n'
    texte += f"IC Wilson 95 % : {r['intervalle']} ; borne basse sous seuil J1 : {r['borne_sous_seuil']}.\n"
    texte += 'Le verdict compare le taux ponctuel au seuil ; la borne basse est un signal séparé.\n\n'
    texte += 'Entonnoir = étapes / nouveaux de la période × 100 :\n'
    for k, v in r['entonnoir'].items():
        texte += f'- {k} : {afficher(v)} %\n'
    texte += f"\n## Verdict\n\nP7: {r['verdict']} | {r['raison']}\n\n"
    texte += f"Seuils beta : {seuils['beta']}. Référence descriptive GameAnalytics 2026 : {seuils['reference_gameanalytics_2026']}.\n"
    texte += 'Ce calcul interne ne valide ni la release ni une autorisation publicitaire (G15).\n\n'
    texte += 'Commande proposée à l’orchestrateur (jamais exécutée ici) :\n\n```powershell\n'
    if r['verdict'] == 'attend':
        texte += f'OUTILS\\etat.ps1 -Jeu {args.jeu} -Statut bloque -Note "P7 attend : mesures incomplètes ou trop jeunes"\n'
    else:
        texte += f'OUTILS\\etat.ps1 -Jeu {args.jeu} -Porte P7 -Resultat {r["verdict"]} -Preuve "JEUX\\{args.jeu}\\08-distribution\\{nom}"\n'
    texte += '```\n'
    ecrire_sur(chemin / nom, texte)
    print(f"P7: {r['verdict']} | {r['raison']}")
    return r


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commandes = parser.add_subparsers(dest='commande', required=True)
    for nom in ('diagnostic', 'collecter', 'juger'):
        p = commandes.add_parser(nom)
        p.add_argument('--jeu', required=True)
        if nom != 'juger':
            p.add_argument('--univers')
            p.add_argument('--magasin')
            p.add_argument('--base-url', default=BASE, help=argparse.SUPPRESS)
        if nom == 'collecter':
            p.add_argument('--source', default='api')
            p.add_argument('--max-requetes', type=int, default=100)
        if nom == 'juger':
            p.add_argument('--aujourdhui')
    args = parser.parse_args(argv)
    try:
        if (RACINE / 'STOP').exists():
            raise Erreur('STOP présent : arrêt')
        dossier(args.jeu)
        if args.commande == 'collecter' and args.max_requetes < 1:
            raise Erreur('--max-requetes doit être positif')
        resultat = globals()[args.commande](args)
        return resultat if type(resultat) is int else 0
    except Erreur as erreur:
        print(str(erreur), file=sys.stderr)
        return erreur.code
    except (ValueError, KeyError, TypeError, OverflowError):
        print('Format ou configuration invalide (contenu non affiché).', file=sys.stderr)
        return 2
    except OSError:
        print('Erreur système ou disque (détails non affichés).', file=sys.stderr)
        return 6


if __name__ == '__main__':
    sys.exit(main())

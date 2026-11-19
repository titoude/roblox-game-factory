#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interrupteurs Open Cloud v2, bibliothèque standard ; aucune écriture implicite.
Documentation officielle vérifiée le 16/11/2026 : PATCH .../entries/interrupteurs,
corps {"value": table}, allowMissing=true ; universe-datastores.objects:update.
https://create.roblox.com/docs/cloud/guides/data-stores
https://github.com/Roblox/creator-docs/blob/main/content/en-us/reference/cloud/cloud.docs.json
Codes : 0 succès/diagnostic sans clé, 2 entrée/configuration invalide,
3 clé absente, 4 accès refusé, 6 panne réseau/API/disque (écriture possiblement reçue).
Une seule instance opératrice : PATCH ne fournit pas de comparaison atomique ici.
Ne jamais relancer aveuglément après une panne : relire l'entrée et le journal.
"""
import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import json
import math
from http.client import HTTPException
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request

sys.dont_write_bytecode = True
from usine_opencloud import BASE, Client as ClientCommun, Erreur, ecrire_sur, lire_json
from prevenir import refuse, verrou_local

RACINE = Path(__file__).resolve().parent.parent
LECTURE = 'usine-roblox:opencloud:lecture'
ECRITURE = 'usine-roblox:opencloud:interrupteurs'
PORTEE = 'universe-datastores.objects:update'


def lire_secret(nom):
    """Lecture exacte de deux identifiants dédiés ; aucune énumération."""
    if nom not in (LECTURE, ECRITURE):
        raise Erreur('Nom d’identifiant interdit')
    if os.name != 'nt':
        raise Erreur('Le Gestionnaire d’identifiants exige Windows', 3)

    class Credential(ctypes.Structure):
        _fields_ = [('Flags', wintypes.DWORD), ('Type', wintypes.DWORD),
                    ('TargetName', wintypes.LPWSTR), ('Comment', wintypes.LPWSTR),
                    ('LastWritten', wintypes.FILETIME), ('CredentialBlobSize', wintypes.DWORD),
                    ('CredentialBlob', ctypes.POINTER(ctypes.c_ubyte)),
                    ('Persist', wintypes.DWORD), ('AttributeCount', wintypes.DWORD),
                    ('Attributes', ctypes.c_void_p), ('TargetAlias', wintypes.LPWSTR),
                    ('UserName', wintypes.LPWSTR)]

    api = ctypes.WinDLL('Advapi32.dll', use_last_error=True)
    pointeur = ctypes.POINTER(Credential)()
    api.CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                             ctypes.POINTER(ctypes.POINTER(Credential))]
    api.CredReadW.restype = wintypes.BOOL
    api.CredFree.argtypes = [ctypes.c_void_p]
    if not api.CredReadW(nom, 1, 0, ctypes.byref(pointeur)):
        if ctypes.get_last_error() == 1168:
            return None
        raise Erreur('Lecture du Gestionnaire impossible', 6)
    try:
        secret = ctypes.string_at(pointeur.contents.CredentialBlob,
                                  pointeur.contents.CredentialBlobSize).decode('utf-16-le').rstrip('\0')
        if not secret or any(c in secret for c in '\r\n'):
            raise Erreur('Identifiant inutilisable', 3)
        return secret
    finally:
        api.CredFree(pointeur)


def dossier(slug):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise Erreur('Slug invalide')
    return RACINE / 'JEUX' / slug


def valide(v, regle):
    typ = regle.get('type')
    if typ == 'boolean':
        return type(v) is bool
    if typ == 'number':
        return (type(v) in (int, float) and math.isfinite(v)
                and type(regle.get('min')) in (int, float)
                and type(regle.get('max')) in (int, float)
                and regle['min'] <= v <= regle['max'])
    return typ == 'string' and type(v) is str and len(v) <= 200


def configuration(args):
    jeu = dossier(args.jeu)
    if not (jeu / 'reglages.json').exists() or not (jeu / 'ETAT.json').exists():
        raise Erreur('Configuration absente : reglages.json et ETAT.json requis')
    config = lire_json(jeu / 'reglages.json')
    etat = lire_json(jeu / 'ETAT.json')
    univers = args.univers or etat.get('place', {}).get('universeId_prod')
    magasin = args.magasin or config.get('magasin')
    if not univers or not str(univers).isdigit():
        raise Erreur('Univers absent : --univers ou ETAT.json place.universeId_prod requis')
    # Aucun accès à un magasin de profils, même via --magasin.
    if not isinstance(magasin, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*Reglages_v1', magasin):
        raise Erreur('Magasin attendu : <NomCourt>Reglages_v1')
    declarations = config.get('interrupteurs')
    if not isinstance(declarations, dict) or not declarations:
        raise Erreur('Déclarations interrupteurs absentes')
    for nom, regle in declarations.items():
        if (not re.fullmatch(r'[a-z][a-z0-9_]{0,59}', nom) or nom in ('version', 'maj')
                or not isinstance(regle, dict) or not valide(regle.get('defaut'), regle)):
            raise Erreur('Déclaration invalide (nom, type, défaut ou bornes)')
    return jeu, univers, magasin, declarations


class Client(ClientCommun):
    def lire_interrupteurs(self):
        # Ne reprend pas les messages HTTP distants : ils pourraient contenir une clé.
        return self.requete('GET')

    def requete(self, methode, valeur=None):
        url = self.url + '/interrupteurs' + ('?allowMissing=true' if methode == 'PATCH' else '')
        data = None if valeur is None else json.dumps({'value': valeur}, allow_nan=False).encode('utf-8')
        req = Request(url, data=data, method=methode,
                      headers={'x-api-key': self.secret, 'Content-Type': 'application/json'})
        try:
            with self.ouvrir(req, timeout=20) as reponse:
                return json.load(reponse)
        except HTTPError as erreur:
            if erreur.code == 404 and methode == 'GET':
                return {'value': {'version': 0, 'maj': 0}}
            if erreur.code in (401, 403):
                raise Erreur('Accès Open Cloud refusé (HTTP %s)' % erreur.code, 4)
            raise Erreur('API : HTTP %s ; aucune relance automatique' % erreur.code, 6)
        except (URLError, TimeoutError, HTTPException):
            raise Erreur('Réseau indisponible ; relire avant toute relance', 6)

    def poser(self, valeur):
        return self.requete('PATCH', valeur)


def contenu(entree, declarations):
    valeur = entree.get('value')
    if isinstance(valeur, str):
        valeur = json.loads(valeur)
    if not isinstance(valeur, dict):
        raise Erreur('Entrée distante invalide')
    version = valeur.get('version')
    if type(version) is not int or not 0 <= version < 2**53 - 1:
        raise Erreur('Version distante invalide')
    if type(valeur.get('maj')) not in (int, float) or not math.isfinite(valeur['maj']):
        raise Erreur('Horodatage distant invalide')
    # Refuser une entrée incohérente plutôt qu'écraser des réglages inconnus.
    if any(n not in declarations and n not in ('version', 'maj') for n in valeur):
        raise Erreur('Nom distant non déclaré ; aligner les déclarations avant écriture')
    if any(n in valeur and not valide(valeur[n], r) for n, r in declarations.items()):
        raise Erreur('Valeur distante invalide')
    return dict(valeur)


def main(argv=None, lecteur=None):
    try:
        # La lecture, le PATCH et le journal constituent une seule opération locale.
        with verrou_local(RACINE, 'interrupteurs'):
            return commande(argv, lecteur)
    except OSError:
        print('Opération indisponible ou déjà en cours (détails masqués).')
        return 6


def commande(argv=None, lecteur=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sous = parser.add_subparsers(dest='commande', required=True)
    for nom in ('diagnostic', 'lire', 'poser', 'historique'):
        p = sous.add_parser(nom)
        p.add_argument('--jeu', required=True)
        p.add_argument('--univers')
        p.add_argument('--magasin')
        p.add_argument('--base-url', default=BASE, help='Réservé aux tests HTTP locaux')
        if nom == 'poser':
            p.add_argument('--nom', required=True)
            p.add_argument('--valeur', required=True, help='JSON scalaire ; chaîne brute acceptée')
            p.add_argument('--raison', required=True)
            p.add_argument('--confirmer', action='store_true')
    args = parser.parse_args(argv)
    lecteur = lecteur or lire_secret
    secrets = []
    def afficher(texte):
        for secret in secrets:
            for forme in (secret, json.dumps(secret, ensure_ascii=False)[1:-1], json.dumps(secret)[1:-1]):
                texte = texte.replace(forme, '[secret masqué]')
        print(texte)
    def sensible(texte):
        return isinstance(texte, str) and (refuse(texte) or any(s in texte for s in secrets))
    try:
        if (RACINE / 'STOP').exists():
            raise Erreur('STOP présent : arrêt')
        jeu = dossier(args.jeu)
        journal = jeu / '07-release/JOURNAL-INTERRUPTEURS.md'
        if args.commande == 'historique':
            # Masquer aussi les deux clés si elles figurent accidentellement dans un ancien journal.
            secrets.extend(s for s in (lecteur(LECTURE), lecteur(ECRITURE)) if s)
            historique = journal.read_text(encoding='utf-8') if journal.exists() else 'Aucun historique local.'
            if refuse(historique):
                raise Erreur('Historique contenant des données sensibles : affichage refusé')
            afficher(historique)
            return 0
        lecture = lecteur(LECTURE)
        if lecture:
            secrets.append(lecture)
        ecriture = lecteur(ECRITURE)
        if ecriture:
            secrets.append(ecriture)
        if args.commande == 'diagnostic':
            afficher('Clé lecture : ' + ('présente' if lecture else 'absente'))
            afficher('Clé interrupteurs : ' + ('présente' if ecriture else 'absente'))
            afficher('Portées : universe-datastores.objects:read (lecture), ' + PORTEE + ' (écriture).')
            afficher('Aucun appel réseau ; permissions non testées.')
            if not lecture and not ecriture:
                afficher('Aucune clé ; aucune écriture possible.')
            if not (jeu / 'reglages.json').exists():
                afficher('reglages.json absent : intégration du jeu à préparer.')
            return 0
        jeu, univers, magasin, declarations = configuration(args)
        if args.commande == 'poser':
            if args.nom not in declarations:
                raise Erreur('Nom non déclaré dans reglages.json')
            try:
                nouvelle = json.loads(args.valeur)
            except ValueError:
                nouvelle = args.valeur
            if not valide(nouvelle, declarations[args.nom]):
                raise Erreur('Valeur refusée : type, longueur ou bornes')
            if not args.raison.strip() or len(args.raison) > 500:
                raise Erreur('Raison requise, 500 caractères au plus')
            if sensible(nouvelle) or sensible(args.raison):
                raise Erreur('Secret ou identifiant probable : écriture refusée')
        if not lecture:
            raise Erreur('Clé de lecture absente : ' + LECTURE, 3)
        if args.commande == 'poser' and args.confirmer:
            if not ecriture:
                raise Erreur('Clé d’écriture absente : ' + ECRITURE + ' ; rien écrit', 3)
            if ecriture == lecture:
                raise Erreur('Clé d’écriture identique à la clé de lecture : refus', 3)
        client = Client(univers, magasin, lecture, args.base_url)
        valeur = contenu(client.lire_interrupteurs(), declarations)
        if any(sensible(v) for v in valeur.values()):
            raise Erreur('Entrée distante contenant des données sensibles : affichage et écriture refusés')
        if args.commande == 'lire':
            afficher(json.dumps(valeur, ensure_ascii=False, indent=2))
            return 0
        ancienne = valeur.get(args.nom, declarations[args.nom]['defaut'])
        if sensible(ancienne):
            raise Erreur('Défaut contenant des données sensibles : écriture refusée')
        valeur[args.nom] = nouvelle
        valeur['version'] += 1
        valeur['maj'] = int(datetime.now(timezone.utc).timestamp())
        afficher(('écriture confirmée prévue : ' if args.confirmer else 'Simulation, aucune écriture : ')
                 + magasin + '/interrupteurs ' + json.dumps(valeur, ensure_ascii=False))
        if not args.confirmer:
            return 0
        # Préparer une intention durable avant PATCH ; un arrêt entre le réseau et
        # le journal doit rester visible au prochain processus, sous le même mutex.
        intention = journal.with_suffix('.en-cours.json')
        if intention.exists():
            raise Erreur('Écriture précédente incertaine : relire et réconcilier le fichier .en-cours.json avant de le retirer', 6)
        def cellule(v):
            return json.dumps(v, ensure_ascii=False).replace('|', '&#124;').replace('<', '&lt;').replace('>', '&gt;')
        historique = journal.read_text(encoding='utf-8') if journal.exists() else (
            '# Journal des interrupteurs\n\n| Date UTC | Nom | Ancienne | Nouvelle | Raison | Version |\n'
            '|---|---|---|---|---|---|\n')
        ligne = ('| ' + datetime.now(timezone.utc).isoformat() + ' | ' + args.nom + ' | '
                 + cellule(ancienne) + ' | ' + cellule(nouvelle) + ' | ' + cellule(args.raison)
                 + ' | ' + str(valeur['version']) + ' |\n')
        if sensible(historique):
            raise Erreur('Historique contenant des données sensibles : écriture refusée')
        ecrire_sur(intention, json.dumps({'valeur': valeur, 'ligne': ligne}, ensure_ascii=False) + '\n')
        Client(univers, magasin, ecriture, args.base_url).poser(valeur)
        try:
            ecrire_sur(journal, historique + ligne)
            intention.unlink()
        except (OSError, Erreur):
            raise Erreur('écriture distante reçue, journal local non écrit : réconcilier sans relancer', 6)
        afficher('écriture reçue ; journal local écrit ; version ' + str(valeur['version']))
        return 0
    except Erreur as erreur:
        afficher(str(erreur))
        return erreur.code
    except (OSError, ValueError, TypeError, AttributeError, OverflowError):
        afficher('Configuration, réponse ou disque invalide (contenu non affiché).')
        return 6


if __name__ == '__main__':
    raise SystemExit(main())

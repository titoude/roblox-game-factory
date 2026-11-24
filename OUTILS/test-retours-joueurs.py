#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôles isolés : aucun secret ni réseau extérieur. Code 0 si tout passe."""
import contextlib
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import threading
import subprocess
import sys
from types import SimpleNamespace

OUTILS = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('retours', OUTILS / 'retours-joueurs.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
echecs = []
nombre = 0
PORTEE_TEST = m.PORTEES[0]


def verifier(nom, condition):
    global nombre
    nombre += 1
    print(('ok     ' if condition else 'ECHEC  ') + nom)
    if not condition:
        echecs.append(nom)


def refuse(action, code=2):
    try:
        action()
    except m.Erreur as erreur:
        return erreur.code == code
    return False


def commande(*args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return m.main(list(args))


class Serveur(BaseHTTPRequestHandler):
    mode = 'normal'
    appels = []
    def log_message(self, *args):
        pass

    def do_GET(self):
        Serveur.appels.append(self.path)
        statut = 200
        corps = {}
        if self.mode in ('401', '403'):
            statut, corps = int(self.mode), {'message': 'permission denied'}
        elif self.mode == '429' and len(self.appels) == 1:
            statut, corps = 429, {'message': 'slow down'}
        elif '/entries/' in self.path:
            corps = {'value': {'t': 1794820000, 'userId': 99, 'lang': 'en', 'version': 4,
                              'categorie': 'bug', 'texte': 'The bridge is broken'}}
        elif 'pageToken=suivant' in self.path:
            corps = {'dataStoreEntries': [{'id': 'r_2_99'}]}
        else:
            corps = {'dataStoreEntries': [{'id': 'r_1_99'}], 'nextPageToken': 'suivant'}
        self.send_response(statut)
        self.send_header('Content-Type', 'application/json')
        if statut == 429:
            self.send_header('Retry-After', '2')
        self.end_headers()
        self.wfile.write(json.dumps(corps).encode())


with tempfile.TemporaryDirectory(prefix='retours-tests-') as temp:
    m.RACINE = Path(temp)
    source = OUTILS / 'GABARITS' / 'retours.exemple.jsonl'
    verifier('20 exemples fictifs', len(m.lignes(source)) == 20)
    valeur = {'t': 100, 'userId': 1, 'lang': 'fr', 'version': 4, 'categorie': 'bug', 'texte': 'Pont cassé'}
    verifier('objet et chaîne JSON acceptés', m.valider(valeur)[1] is None and m.valider(json.dumps(valeur))[1] is None)
    for champ, contenu in [('t', True), ('userId', -1), ('lang', 3), ('version', '4'),
                           ('categorie', 'admin'), ('texte', 'a' * 501), ('texte', '')]:
        verifier('rejet ' + champ + ' ' + str(contenu)[:15], m.valider(dict(valeur, **{champ: contenu}))[1] is not None)
    verifier('JSON interne invalide rejeté', m.valider('{')[1] is not None)
    verifier('normalisation accents et ponctuation', m.normaliser(' ÉTÉ !!!  Pont… ') == 'ete pont')
    arguments = ['--jeu', 'test', '--source', 'fichier:' + str(source)]
    verifier('collecte fichier', commande('collecter', *arguments) == 0)
    sortie = Path(temp) / 'JEUX/test/10-retours'
    brut = next((sortie / 'brut').glob('*.jsonl'))
    avant = brut.read_bytes()
    verifier('seconde collecte sans duplication', commande('collecter', *arguments) == 0 and brut.read_bytes() == avant)
    verifier('tri complet', commande('trier', '--jeu', 'test') == 0)
    chemin = next(sortie.glob('LOT-*.json'))
    lot = m.lire_json(chemin)
    verifier('invalides avec raisons', len(lot['invalides']) == 4 and all(v['raison'] for v in lot['invalides']))
    verifier('doublons regroupés et joueurs distincts', any(g['nombre_retours'] >= 3 and g['joueurs_distincts'] >= 2 for g in lot['groupes']))
    verifier('quasi-doublons', any(g['nombre_retours'] == 2 and 'blue bridge' in g['extraits'][0] for g in lot['groupes']))
    abus = {a for g in lot['groupes'] for a in g['abus']}
    verifier('quatre signaux abus', len(abus) == 4)
    verifier('lot sans userId ni clé brute', 'userId' not in chemin.read_text(encoding='utf-8') and 'r_179' not in chemin.read_text(encoding='utf-8'))
    verifier('extraits bornés et statut', all(len(g['extraits']) <= 3 and all(len(e) <= 200 for e in g['extraits']) and g['statut'] == 'a_juger' for g in lot['groupes']))
    jugement = {g['id']: {'decision': 'corriger', 'raison': 'À vérifier', 'impact': 4, 'effort': 2} for g in lot['groupes']}
    avis = Path(temp) / 'jugement.json'
    m.ecrire_sur(avis, m.json_texte({}))
    p = SimpleNamespace(jeu='test', lot=chemin, jugement=avis)
    verifier('jugement incomplet refusé', refuse(lambda: m.propositions(p)))
    premier = next(iter(jugement))
    jugement[premier]['decision'] = 'executer'
    m.ecrire_sur(avis, m.json_texte(jugement))
    verifier('décision inconnue refusée', refuse(lambda: m.propositions(p)))
    jugement[premier]['decision'] = 'refuser'
    m.ecrire_sur(avis, m.json_texte(jugement))
    verifier('propositions complètes', commande('propositions', '--jeu', 'test', '--lot', str(chemin), '--jugement', str(avis)) == 0)
    verifier('écriture vide refusée', refuse(lambda: m.ecrire_sur(Path(temp) / 'vide', ''), 6))
    serveur = ThreadingHTTPServer(('127.0.0.1', 0), Serveur)
    fil = threading.Thread(target=serveur.serve_forever, daemon=True)
    fil.start()
    base = f'http://127.0.0.1:{serveur.server_port}'
    pauses = []
    def client(maximum=20):
        return m.Client(1, 'TestRetours_v1', 'factice', base, maximum, pauses.append)
    # Injection en mémoire, sans argument, fichier ni variable d'environnement.
    m.lire_identifiant = lambda nom: 'factice'
    try:
        client_original = m.Client
        m.Client = lambda *a, **kw: client_original(*a, **kw, pause=pauses.append)
        commun = ['--jeu', 'http', '--univers', '1', '--magasin', 'Test', '--base-url', base]
        verifier('collecte HTTP plafond un : liste conservée', commande('collecter', *commun, '--max-requetes', '1') == 5)
        verifier('collecte HTTP plafond un : première lecture', commande('collecter', *commun, '--max-requetes', '1') == 5)
        verifier('collecte HTTP plafond un : seconde page', commande('collecter', *commun, '--max-requetes', '1') == 5)
        verifier('collecte HTTP plafond un : seconde lecture', commande('collecter', *commun, '--max-requetes', '1') == 0)
        http_brut = next((Path(temp) / 'JEUX/http/10-retours/brut').glob('*.jsonl'))
        verifier('deux entrées HTTP sans perte', len(m.lignes(http_brut)) == 2)
        verifier('deuxième collecte HTTP sans doublon', commande('collecter', *commun) == 0 and len(m.lignes(http_brut)) == 2)
        m.Client = client_original
        Serveur.appels = []
        c = client()
        page = c.lister()
        verifier('pagination HTTP', c.lister(page['nextPageToken'])['dataStoreEntries'][0]['id'] == 'r_2_99')
        verifier('lecture HTTP objet', c.lire('r_1_99')['value']['userId'] == 99)
        verifier('filtre et taille HTTP', 'maxPageSize=100' in Serveur.appels[0] and 'filter=id.startsWith' in Serveur.appels[0])
        Serveur.mode, Serveur.appels = '429', []
        pauses.clear()
        c = client()
        c.lister()
        verifier('429 Retry-After et délai', c.requetes == 2 and pauses == [2, 1])
        verifier('plafond requêtes', refuse(lambda: client(0).lister(), 5))
        for statut in ('401', '403'):
            Serveur.mode = statut
            verifier('HTTP ' + statut + ' liste', refuse(lambda: client().lister(), 4))
            verifier('HTTP ' + statut + ' lecture', refuse(lambda: client().lire('r_1_99'), 4))
            capture = io.StringIO()
            with contextlib.redirect_stdout(capture):
                code = m.diagnostic(SimpleNamespace(jeu='test', univers='1', magasin='Test', base_url=base))
            verifier('diagnostic ' + statut + ' portées et secret masqué', code == 4 and PORTEE_TEST in capture.getvalue() and 'factice' not in capture.getvalue())
    finally:
        serveur.shutdown()
        serveur.server_close()
        fil.join()

for script in ('ServerScriptService.Jeu.RetoursService.lua', 'StarterPlayer.StarterPlayerScripts.RetoursClient.client.lua'):
    compilation = subprocess.run([str(OUTILS / 'bin' / ('luau-compile' + ('.exe' if os.name == 'nt' else ''))), '--null',
                                  str(OUTILS / 'GABARITS/luau' / script)], capture_output=True)
    verifier('compilation ' + script, compilation.returncode == 0)

print(f'{nombre - len(echecs)}/{nombre} contrôles passés')
raise SystemExit(1 if echecs else 0)

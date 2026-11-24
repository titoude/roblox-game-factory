#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests autonomes, réseau local uniquement, aucun secret. Code 0 si tous passent."""
import contextlib
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from types import SimpleNamespace
sys.dont_write_bytecode = True
OUTILS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('mesures', OUTILS / 'mesures-joueurs.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
nombre, echecs = 0, []
def verifier(nom, ok):
    global nombre
    nombre += 1
    print(('ok     ' if ok else 'ECHEC  ') + nom)
    if not ok: echecs.append(nom)
def refuse(f, code=2):
    try: f()
    except m.Erreur as e: return e.code == code
    return False
def commande(*args):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return m.main(list(args))
source = OUTILS / 'GABARITS/mesures.exemple.jsonl'
seuils = m.lire_json(OUTILS.parent / 'CONNAISSANCES/seuils.json')['beta']
class Serveur(BaseHTTPRequestHandler):
    mode, appels = 'normal', []
    def log_message(self, *a): pass
    def do_GET(self):
        Serveur.appels.append(self.path)
        statut = 200
        if self.mode in ('401', '403'):
            statut, corps = int(self.mode), {'message': 'factice'}
        elif self.mode == '429' and len(self.appels) == 1:
            statut, corps = 429, {}
        elif '/entries/j_' in self.path:
            corps = json.loads(source.read_text().splitlines()[0])
        elif 'pageToken=deux' in self.path:
            corps = {'dataStoreEntries': [{'id': 'j_2026-11-02'}]}
        else:
            corps = {'dataStoreEntries': [{'id': 'j_2026-11-01'}], 'nextPageToken': 'deux'}
        self.send_response(statut)
        if statut == 429: self.send_header('Retry-After', '2')
        self.end_headers(); self.wfile.write(json.dumps(corps).encode())
with tempfile.TemporaryDirectory(prefix='usine-mesures-') as temp:
    m.RACINE = Path(temp)
    m.ecrire_sur(m.RACINE / 'CONNAISSANCES/seuils.json', (OUTILS.parent / 'CONNAISSANCES/seuils.json').read_text(encoding='utf-8'))
    verifier('collecte fictive 14 jours', commande('collecter', '--jeu', 'test', '--source', 'fichier:' + str(source)) == 0)
    csv = m.RACINE / 'JEUX/test/08-distribution/MESURES.csv'
    jours = m.lire_csv(csv)
    verifier('14 lignes sans doublon', len(jours) == 14)
    r = m.calculer(jours, date(2026,11,15), seuils)
    verifier('cohorte J1 exacte', r['cohorte'] == 1300 and r['retours_j1'] == 260 and r['j1'] == 20)
    verifier('cohorte J7 exacte', r['cohorte_j7'] == 700 and r['j7'] == 5)
    verifier('durée et tranches exactes', r['moyenne'] == 10 and abs(r['abandon_60'] - 100/30) < 1e-10 and abs(r['abandon_180'] - 100/15) < 1e-10)
    verifier('entonnoir exact', r['entonnoir']['e_premiere_action'] == 80)
    verifier('verdict passe', r['verdict'] == 'passe')
    bas, haut = m.wilson(50, 100)
    verifier('Wilson connu 50/100', abs(bas - 40.3831530) < 1e-6 and abs(haut - 59.6168470) < 1e-6)
    verifier('Wilson zéro succès', abs(m.wilson(0,100)[0]) < 1e-10)
    verifier('Wilson sans base absent', m.wilson(0,0) is None)
    verifier('cohorte trop jeune attend', m.calculer(jours, date(2026,11,2), seuils)['verdict'] == 'attend')
    verifier('cohorte insuffisante attend', m.calculer(jours, date(2026,11,3), seuils)['verdict'] == 'attend')
    manquant = {k: dict(v) for k,v in jours.items() if k != '2026-11-05'}
    absent = m.calculer(manquant, date(2026,11,15), seuils)
    verifier('jour manquant absent et attend', absent['verdict'] == 'attend' and absent['j1'] is None and absent['moyenne'] is None)
    manquant = {k: dict(v) for k,v in jours.items()}
    del manquant['2026-11-02']['retours_j1']
    verifier('champ absent attend', m.calculer(manquant, date(2026,11,15), seuils)['j1'] is None)
    faibles = {k: dict(v, retours_j1=0, minutes=100) for k,v in jours.items()}
    verifier('zéro explicite echec', m.calculer(faibles, date(2026,11,15), seuils)['verdict'] == 'echec')
    faibles = {k: dict(v, retours_j1=8) for k,v in jours.items()}
    rr = m.calculer(faibles, date(2026,11,15), seuils)
    verifier('borne basse signal séparé', rr['verdict'] == 'passe' and rr['borne_sous_seuil'])
    verifier('jour courant exclu', m.calculer(jours, date(2026,11,14), seuils)['sessions'] == 13*150)
    verifier('jugement écrit', commande('juger','--jeu','test','--aujourdhui','2026-11-15') == 0)
    rapport = csv.with_name('MESURES-2026-11-15.md').read_text(encoding='utf-8')
    verifier('rapport faits calculs verdict commande', all(t in rapport for t in ('## Faits','## Calculs','P7: passe','etat.ps1','Wilson','GameAnalytics')))
    nouveau = Path(temp) / 'nouveau.jsonl'
    m.ecrire_sur(nouveau, json.dumps({'id':'j_2026-11-14','value':dict(jours['2026-11-14'], nouveaux=120)})+'\n')
    verifier('relecture remplace le jour', commande('collecter','--jeu','test','--source','fichier:'+str(nouveau)) == 0 and m.lire_csv(csv)['2026-11-14']['nouveaux'] == 120 and len(m.lire_csv(csv)) == 14)
    avant = csv.read_bytes()
    m.ecrire_sur(nouveau, '{"id":"j_2026-11-14","value":{"userId":123}}\n')
    verifier('donnée personnelle refusée sans écrasement', commande('collecter','--jeu','test','--source','fichier:'+str(nouveau)) == 2 and csv.read_bytes() == avant)
    verifier('écriture vide refusée', refuse(lambda: m.ecrire_sur(nouveau,''),6))
    verifier('slug traversée refusé', refuse(lambda: m.dossier('../ailleurs')))
    verifier('identifiant interdit sans lecture', refuse(lambda: __import__('usine_opencloud').lire_identifiant('RobloxStudioAuth-test')))
    verifier('base extérieure refusée', refuse(lambda: m.Client(1,'Test','factice','https://example.com')))
    serveur = ThreadingHTTPServer(('127.0.0.1',0),Serveur)
    fil = threading.Thread(target=serveur.serve_forever,daemon=True); fil.start()
    base = f'http://127.0.0.1:{serveur.server_port}'
    pauses = []
    def client(maximum=20): return m.Client(1,'Test','factice',base,maximum,pauses.append)
    try:
        entrees = list(client().entrees('j_'))
        verifier('pagination et lecture HTTP', [e['id'] for e in entrees] == ['j_2026-11-01','j_2026-11-02'])
        verifier('filtre j_ HTTP', 'j_' in Serveur.appels[0] and 'filter=' in Serveur.appels[0])
        Serveur.mode, Serveur.appels = '429', []
        pauses.clear(); c = client(); c.lister()
        verifier('429 avec Retry-After', c.requetes == 2 and pauses == [2,1])
        verifier('plafond respecté', refuse(lambda: client(0).lister(),5))
        for statut in ('401','403'):
            Serveur.mode = statut
            verifier('HTTP '+statut+' sans fuite', refuse(lambda: client().lister(),4))
        Serveur.mode = 'normal'
        m.identifiant = lambda slug: ('identifiant-fictif','factice')
        original = m.Client
        m.Client = lambda *a, **kw: original(*a, **kw, pause=lambda _: None)
        verifier('collecte API locale complète', commande('collecter','--jeu','http','--univers','1','--magasin','Test','--base-url',base) == 0)
        m.identifiant = lambda slug: ('identifiant-fictif',None)
        verifier('diagnostic absent sans réseau', commande('diagnostic','--jeu','test','--univers','1','--magasin','Test') == 0)
        verifier('collecte sans identifiant code 3', commande('collecter','--jeu','test','--univers','1','--magasin','Test') == 3)
    finally:
        serveur.shutdown(); serveur.server_close(); fil.join()
    m.ecrire_sur(m.RACINE/'STOP','arrêt\n')
    verifier('STOP respecté', commande('juger','--jeu','test') == 2)
compilation = subprocess.run([str(OUTILS/'bin'/('luau-compile'+('.exe' if os.name=='nt' else ''))),'--null',str(OUTILS/'GABARITS/luau/ServerScriptService.Jeu.MesuresService.lua')],capture_output=True)
verifier('compilation Luau --null', compilation.returncode == 0)
print(f'{nombre-len(echecs)}/{nombre} contrôles passés')
raise SystemExit(1 if echecs else 0)

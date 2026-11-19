#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests autonomes : HTTP local, identifiants fictifs injectés, aucun accès Roblox."""
import contextlib
import importlib.util
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from http.client import IncompleteRead

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('interrupteurs', Path(__file__).with_name('interrupteurs.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
L, E = 'lecture-factice-ne-pas-afficher', 'ecriture-factice-ne-pas-afficher'
appels, sorties, demandes = [], [], []
valeur = {'boutique_ouverte': True, 'vitesse': 1, 'version': 7, 'maj': 123}
mode = 'normal'
nombre = 0


class Serveur(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def envoyer(self, statut, objet):
        self.send_response(statut)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(objet).encode())

    def do_GET(self):
        appels.append(('GET', self.path, self.headers.get('x-api-key'), None))
        if mode == 'refus':
            return self.envoyer(403, {'message': L + E})
        if mode == 'absent':
            return self.envoyer(404, {})
        if mode == 'redirection':
            self.send_response(302)
            self.send_header('Location', 'https://example.com/interdit')
            self.end_headers()
            return
        self.envoyer(200, {'value': valeur})

    def do_PATCH(self):
        global valeur
        corps = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        appels.append(('PATCH', self.path, self.headers.get('x-api-key'), corps))
        if mode == 'panne-ecriture':
            return self.envoyer(500, {'message': L + E})
        valeur = corps['value']
        self.envoyer(200, {'value': valeur})


def verifier(nom, ok):
    global nombre
    assert ok, 'ECHEC ' + nom
    nombre += 1
    print('ok     ' + nom)


def lecteur(nom):
    demandes.append(nom)
    assert nom in (m.LECTURE, m.ECRITURE)
    return {m.LECTURE: L, m.ECRITURE: E}.get(nom)


with tempfile.TemporaryDirectory() as temp:
    m.RACINE = Path(temp)
    jeu = m.RACINE / 'JEUX/test'
    jeu.mkdir(parents=True)
    m.ecrire_sur(jeu/'ETAT.json', '{"place":{"universeId_prod":"123"}}\n')
    config = {'magasin': 'TestReglages_v1', 'interrupteurs': {
        'boutique_ouverte': {'type': 'boolean', 'defaut': True},
        'vitesse': {'type': 'number', 'defaut': 1, 'min': 0, 'max': 2},
        'message_maintenance': {'type': 'string', 'defaut': ''}}}
    m.ecrire_sur(jeu/'reglages.json', json.dumps(config)+'\n')
    journal = jeu/'07-release/JOURNAL-INTERRUPTEURS.md'
    serveur = ThreadingHTTPServer(('127.0.0.1', 0), Serveur)
    fil = threading.Thread(target=serveur.serve_forever, daemon=True)
    fil.start()
    base = f'http://127.0.0.1:{serveur.server_port}'

    def commande(nom, *args, secret=lecteur):
        flux = io.StringIO()
        with contextlib.redirect_stdout(flux):
            code = m.main([nom, '--jeu', 'test', '--base-url', base, *args], lecteur=secret)
        sorties.append(flux.getvalue())
        assert L not in sorties[-1] and E not in sorties[-1], 'Fuite de clé'
        return code

    def poser(*options, nom='boutique_ouverte', v='false', secret=lecteur):
        return commande('poser', '--nom', nom, '--valeur', v, '--raison', 'Incident | ligne\n suivante',
                        *options, secret=secret)

    def ecritures():
        return sum(a[0] == 'PATCH' for a in appels)

    try:
        verifier('lecture locale', commande('lire') == 0 and '"version": 7' in sorties[-1])
        verifier('simulation sans appel écriture', poser() == 0 and ecritures() == 0 and not journal.exists())
        verifier('écriture confirmée', poser('--confirmer') == 0 and ecritures() == 1)
        verifier('version incrémentée et maj', valeur['version'] == 8 and valeur['maj'] > 123 and valeur['boutique_ouverte'] is False)
        texte = journal.read_text(encoding='utf-8')
        verifier('journal date valeurs raison', all(t in texte for t in ('Date UTC', 'boutique_ouverte', 'true', 'false', 'Incident', '&#124;', '\\n')))
        verifier('journal une ligne de données', len(texte.splitlines()) == 5)
        verifier('GET lecture, PATCH écriture', all(a[2] == (L if a[0] == 'GET' else E) for a in appels))
        verifier('clé et magasin uniques', all(a[1].split('?')[0] == '/cloud/v2/universes/123/data-stores/TestReglages_v1/entries/interrupteurs' for a in appels))
        verifier('corps v2 et création autorisée', appels[-1][1].endswith('?allowMissing=true') and set(appels[-1][3]) == {'value'})
        avant, appelsAvant = journal.read_bytes(), len(appels)
        verifier('nom non déclaré refusé', poser('--confirmer', nom='inconnu') == 2 and len(appels) == appelsAvant)
        verifier('type faux refusé', poser('--confirmer', v='1') == 2)
        verifier('nombre hors bornes refusé', poser('--confirmer', nom='vitesse', v='3') == 2)
        verifier('booléen refusé pour nombre', poser('--confirmer', nom='vitesse', v='true') == 2)
        verifier('chaîne longue refusée', poser('--confirmer', nom='message_maintenance', v='é'*201) == 2)
        sans = lambda nom: L if nom == m.LECTURE else None
        verifier('clé écriture absente claire', poser('--confirmer', secret=sans) == 3 and 'Clé d’écriture absente' in sorties[-1])
        verifier('aucune écriture après refus', ecritures() == 1 and journal.read_bytes() == avant)
        verifier('clé lecture jamais réutilisée', poser('--confirmer', secret=lambda _: L) == 3 and ecritures() == 1)
        verifier('lecture absente', commande('lire', secret=lambda _: None) == 3)
        verifier('diagnostic sans clé sans réseau', commande('diagnostic', secret=lambda _: None) == 0 and 'Aucune clé' in sorties[-1] and len(appels) == appelsAvant)
        verifier('historique local', commande('historique') == 0 and 'boutique_ouverte' in sorties[-1])
        mode = 'refus'
        verifier('erreur HTTP sans secret', commande('lire') == 4)
        mode = 'redirection'
        verifier('redirection non suivie', commande('lire') == 6)
        mode = 'panne-ecriture'
        avantEcritures = ecritures()
        verifier('panne sans relance ni journal', poser('--confirmer') == 6 and ecritures() == avantEcritures + 1 and journal.read_bytes() == avant)
        verifier('écriture incertaine interdit le rejeu', poser('--confirmer') == 6 and ecritures() == avantEcritures + 1)
        # Réconciliation simulée : le serveur local a rejeté le PATCH (mode 500).
        journal.with_suffix('.en-cours.json').unlink()
        mode = 'absent'
        verifier('première entrée version 1', poser('--confirmer') == 0 and valeur['version'] == 1)
        mode = 'normal'
        valeur['inconnu'] = True
        avantEcritures = ecritures()
        verifier('nom distant inconnu refuse écrasement', poser('--confirmer') == 2 and ecritures() == avantEcritures)
        del valeur['inconnu']
        verifier('magasin profils refusé', commande('lire', '--magasin', 'Profils_v1') == 2)
        verifier('base extérieure refusée', commande('lire', '--base-url', 'https://example.com') == 2)
        m.ecrire_sur(m.RACINE/'STOP', 'arrêt\n')
        avantAppels = len(appels)
        verifier('STOP respecté', commande('lire') == 2 and len(appels) == avantAppels)
        verifier('seulement deux noms de secrets autorisés', set(demandes) == {m.LECTURE, m.ECRITURE})
        verifier('aucun secret dans les sorties ni journal', all(L not in s and E not in s for s in sorties) and L not in journal.read_text(encoding='utf-8') and E not in journal.read_text(encoding='utf-8'))
    finally:
        serveur.shutdown()
        serveur.server_close()
        fil.join()
print(f'{nombre}/{nombre} contrôles passés')


class Regressions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.racine = Path(self.tmp.name)
        self.addCleanup(setattr, m, 'RACINE', m.RACINE)
        m.RACINE = self.racine
        self.jeu = self.racine / 'JEUX/test'
        self.journal = self.jeu / '07-release/JOURNAL-INTERRUPTEURS.md'
        self.secret = 'cle-factice' + chr(92) + 'avec"guillemets'
        self.valeur = {'version': 1, 'maj': 123, 'message': ''}
        m.ecrire_sur(self.jeu / 'ETAT.json', '{"place":{"universeId_prod":"123"}}\n')
        m.ecrire_sur(self.jeu / 'reglages.json', json.dumps({
            'magasin': 'TestReglages_v1', 'interrupteurs': {'message': {'type': 'string', 'defaut': ''}}}) + '\n')

    def commande(self, *args):
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            code = m.main(list(args) + ['--jeu', 'test'],
                          lecteur=lambda nom: self.secret if nom == m.ECRITURE else L)
        self.assertNotIn(self.secret, sortie.getvalue())
        return code

    def poser(self, texte='Maintenance', raison='Incident'):
        return self.commande('poser', '--nom', 'message', '--valeur', texte,
                             '--raison', raison, '--confirmer')

    def test_secret_avec_echappements_refuse_avant_ecriture(self):
        with patch.object(m.Client, 'lire_interrupteurs', return_value={'value': self.valeur}), \
                patch.object(m.Client, 'poser') as ecrire:
            self.assertEqual(self.poser(self.secret), 2)
            self.assertEqual(self.poser(raison=self.secret), 2)
            ecrire.assert_not_called()
        self.assertFalse(self.journal.exists())

    def test_identifiant_joueur_refuse_dans_message_et_raison(self):
        with patch.object(m.Client, 'lire_interrupteurs', return_value={'value': self.valeur}), \
                patch.object(m.Client, 'poser') as ecrire:
            self.assertEqual(self.poser('user_id=42'), 2)
            self.assertEqual(self.poser(raison='joueur 42'), 2)
            ecrire.assert_not_called()

    def test_reponse_http_tronquee_est_masquee(self):
        with patch.object(m.ClientCommun, '__init__', return_value=None):
            client = m.Client('123', 'TestReglages_v1', L)
        client.url, client.secret = 'https://apis.roblox.com/test', L
        client.ouvrir = lambda *a, **k: (_ for _ in ()).throw(IncompleteRead(L.encode(), 100))
        with patch.object(m, 'Client', return_value=client):
            self.assertEqual(self.commande('lire'), 6)

    def test_preparation_sur_disque_echoue_sans_patch(self):
        with patch.object(m.Client, 'lire_interrupteurs', return_value={'value': self.valeur}), \
                patch.object(m.Client, 'poser') as ecrire, \
                patch.object(m, 'ecrire_sur', side_effect=OSError('disque plein')):
            self.assertEqual(self.poser(), 6)
            ecrire.assert_not_called()

    def test_patch_incertain_non_rejoue_apres_plantage(self):
        with patch.object(m.Client, 'lire_interrupteurs', return_value={'value': self.valeur}), \
                patch.object(m.Client, 'poser', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.poser()
        with patch.object(m.Client, 'lire_interrupteurs', return_value={'value': self.valeur}), \
                patch.object(m.Client, 'poser') as ecrire:
            self.assertEqual(self.poser(), 6)
            ecrire.assert_not_called()

    @unittest.skipUnless(m.os.name == 'nt', 'Mutex natif Windows')
    def test_deux_operateurs_ne_lisent_pas_la_meme_version(self):
        entre, finir = threading.Event(), threading.Event()
        codes = []
        def ecrire(valeur):
            entre.set()
            if not finir.wait(5):
                raise OSError('Test concurrent trop lent')
            return {'value': valeur}
        def premier():
            codes.append(self.poser())
        with patch.object(m.Client, 'lire_interrupteurs', return_value={'value': self.valeur}) as lire, \
                patch.object(m.Client, 'poser', side_effect=ecrire):
            fil = threading.Thread(target=premier)
            fil.start()
            try:
                self.assertTrue(entre.wait(5))
                self.assertEqual(self.poser('Autre maintenance'), 6)
                self.assertEqual(lire.call_count, 1)
            finally:
                finir.set()
                fil.join(timeout=10)
            self.assertFalse(fil.is_alive())
        self.assertEqual(codes, [0])


raise SystemExit(not unittest.TextTestRunner(stream=sys.stdout).run(unittest.defaultTestLoader.loadTestsFromTestCase(Regressions)).wasSuccessful())

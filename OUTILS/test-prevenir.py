"""Contrôles locaux : aucun identifiant Windows ni accès réseau extérieur."""
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import prevenir as p
from usine_opencloud import ecrire_sur, json_texte


def main():
    controles = 0
    def verifier(condition, nom):
        nonlocal controles
        assert condition, nom
        controles += 1
        print('OK : ' + nom)
    requetes = []
    class Serveur(BaseHTTPRequestHandler):
        def do_POST(self):
            requetes.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
            self.send_response(204)
            self.end_headers()
        def log_message(self, *args):
            pass
    http = ThreadingHTTPServer(('127.0.0.1', 0), Serveur)
    fil = threading.Thread(target=http.serve_forever, daemon=True)
    fil.start()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            racine = Path(tmp)
            sortie = io.StringIO()
            secret = 'FAUX_SECRET_abcdefghijklmnopqrstuvwxyz'
            webhook = 'https://discord.com/api/webhooks/123456789/' + secret
            config = {c: {'actif': False, 'niveau_min': 'info'} for c in p.CANAUX}
            def sauver():
                ecrire_sur(racine / 'CONNAISSANCES/contact.json', json_texte(config))
            def secrets(nom):
                return ('envoi@example.invalid', webhook if nom.endswith('discord-webhook') else secret)
            url = 'http://127.0.0.1:' + str(http.server_port)
            date = datetime(2026, 11, 16, 12, tzinfo=timezone.utc)
            sequence = 0
            def envoyer(niveau='important', **kw):
                nonlocal sequence
                sequence += 1
                kw.setdefault('cle', 'essai-' + str(sequence))
                with redirect_stdout(sortie):
                    return p.envoyer(niveau, kw.pop('sujet', 'Sujet français é'), kw.pop('texte', 'Corps UTF-8 été'),
                                     racine=racine, maintenant=kw.pop('maintenant', date), _secrets=secrets,
                                     _urls={'discord': url, 'ntfy': url}, **kw)
            sauver()
            verifier(envoyer() == 3 and (racine / 'JOURNAUX/messages-proprietaire.md').exists(), 'aucun canal : code 3 et journal')
            config['discord']['actif'] = config['ntfy']['actif'] = True
            sauver()
            verifier(envoyer() == 0, 'deux canaux HTTP locaux acceptés')
            verifier(requetes[-2]['allowed_mentions'] == {'parse': []} and 'Sujet français é' in requetes[-2]['content'], 'Discord : contenu et aucune mention')
            verifier(requetes[-1]['priority'] == 4 and requetes[-1]['topic'] == secret and requetes[-1]['message'] == 'Corps UTF-8 été', 'ntfy : sujet privé, UTF-8 et priorité important')
            for niveau, priorite in [('info', 2), ('urgent', 5)]:
                envoyer(niveau)
                verifier(requetes[-1]['priority'] == priorite, 'priorité ntfy ' + niveau)
            for niveau, heures in [('info', 24), ('important', 12), ('urgent', 1)]:
                ecrire_sur(racine / 'JOURNAUX/prevenir-etat.json', json_texte({'cles': {}, 'jours': {}}))
                cle = 'dedoublon-' + niveau
                verifier(envoyer(niveau, cle=cle) == 0 and envoyer(niveau, cle=cle, maintenant=date + timedelta(seconds=1)) == 3
                         and envoyer(niveau, cle=cle, maintenant=date + timedelta(hours=heures)) == 0,
                         'anti-répétition ' + niveau + ' et expiration')
            ecrire_sur(racine / 'JOURNAUX/prevenir-etat.json', json_texte({'cles': {}, 'jours': {date.date().isoformat(): 20}}))
            verifier(envoyer() == 3 and envoyer('urgent') == 0, 'plafond quotidien et exception urgent')
            ecrire_sur(racine / 'JOURNAUX/prevenir-etat.json', json_texte({'cles': {}, 'jours': {date.date().isoformat(): 19}}))
            avant = len(requetes)
            verifier(envoyer() == 0 and len(requetes) == avant + 1, 'plafond partagé entre les canaux')
            verifier(envoyer(texte='x-api-key=' + 'A' * 30) == 7, 'secret probable refusé')
            verifier(all(envoyer(texte=nom + ' : 123456789') == 7 for nom in ('userId', 'joueur', 'user')), 'identifiants joueurs refusés')
            verifier(envoyer(sujet='a' * 61) == 7 and envoyer(texte='b' * 601) == 7, 'bornes sujet et texte')
            ecrire_sur(racine / 'JOURNAUX/prevenir-etat.json', json_texte({'cles': {}, 'jours': {}}))
            config['discord']['niveau_min'] = 'urgent'
            sauver()
            avant = len(requetes)
            envoyer()
            verifier(len(requetes) == avant + 1, 'filtrage niveau_min')
            config['discord']['niveau_min'] = 'info'
            sauver()
            def panne(nom):
                if nom.endswith('discord-webhook'):
                    raise OSError(secret)
                return secrets(nom)
            with redirect_stdout(sortie):
                code = p.envoyer('urgent', 'Canal en panne', 'Le second doit répondre.', racine=racine,
                                 _secrets=panne, _urls={'ntfy': url})
            verifier(code == 0 and requetes[-1]['priority'] == 5, 'canal en panne, autre servi')
            config['ntfy']['actif'] = False
            sauver()
            with redirect_stdout(sortie):
                code = p.envoyer('urgent', 'Panne totale', 'Essai local.', racine=racine, _secrets=panne)
            verifier(code == 4, 'tous canaux en panne : code 4')
            config['discord']['actif'] = False
            config['courriel'] = {'actif': True, 'niveau_min': 'info', 'destinataire': 'reception@example.invalid'}
            sauver()
            messages = []
            verifier(envoyer(_smtp=lambda m, u, s: messages.append(m)) == 0, 'couche SMTP injectable')
            m = messages[0]
            from email import policy
            from email.parser import BytesParser
            mime = BytesParser(policy=policy.default).parsebytes(m.as_bytes())
            verifier(str(mime['To']) == 'reception@example.invalid' and str(mime['Subject']) == 'Sujet français é'
                     and mime.get_content().strip() == 'Corps UTF-8 été', 'MIME SMTP : destinataire, sujet et corps UTF-8')
            ecrire_sur(racine / 'STOP', 'arrêt\n')
            avant = len(requetes)
            verifier(envoyer('urgent') == 3 and len(requetes) == avant, 'STOP : aucun envoi')
            contenu = '\n'.join(f.read_text(encoding='utf-8') for f in (racine / 'JOURNAUX').glob('*')) + sortie.getvalue()
            verifier(secret not in contenu and webhook not in contenu and 'A' * 30 not in contenu, 'aucun faux secret dans journaux, état ou sortie')
            for url_interdite in ('https://discord.com.evil.invalid/api/webhooks/123/a', 'http://discord.com/api/webhooks/123/a'):
                try:
                    p.url_valide(url_interdite, True)
                    valide = True
                except ValueError:
                    valide = False
                verifier(not valide, 'URL Discord étrangère ou sans TLS refusée')
    finally:
        http.shutdown()
        http.server_close()
        fil.join()
    print(f'{controles} contrôles passés.')
    return 0


class Regressions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.racine = Path(self.tmp.name)
        self.date = datetime(2026, 11, 17, 23, 30, tzinfo=timezone.utc)
        self.secret = 'mot-factice' + chr(92) + 'avec"guillemets'
        self.messages = []
        ecrire_sur(self.racine / 'CONNAISSANCES/contact.json', json_texte({
            'courriel': {'actif': True, 'destinataire': 'test@example.invalid'}}))

    def envoyer(self, **kw):
        with redirect_stdout(io.StringIO()):
            return p.envoyer(kw.pop('niveau', 'important'), 'Incident usine', kw.pop('texte', 'Résumé agrégé.'),
                             racine=self.racine, maintenant=kw.pop('maintenant', self.date),
                             _secrets=lambda _: ('test@example.invalid', self.secret),
                             _smtp=lambda *args: self.messages.append(args), **kw)

    def test_secret_brut_refuse_avant_journal_meme_sans_canal(self):
        self.assertEqual(self.envoyer(texte=self.secret, canal='journal'), 7)
        self.assertFalse((self.racine / 'JOURNAUX/messages-proprietaire.md').exists())

    def test_secret_opencloud_brut_refuse(self):
        secret = 'autre-cle-ouverte-factice'
        with redirect_stdout(io.StringIO()):
            code = p.envoyer('important', 'Incident', secret, racine=self.racine,
                             _secrets=lambda nom: ('test', secret if nom.endswith('opencloud:lecture') else self.secret),
                             _smtp=lambda *a: self.messages.append(a))
        self.assertEqual(code, 7)
        self.assertFalse((self.racine / 'JOURNAUX/messages-proprietaire.md').exists())

    def test_stop_ne_modifie_aucun_fichier(self):
        ecrire_sur(self.racine / 'STOP', 'arrêt\n')
        avant = {f: f.read_bytes() for f in self.racine.rglob('*') if f.is_file()}
        self.assertEqual(self.envoyer(), 3)
        self.assertEqual(avant, {f: f.read_bytes() for f in self.racine.rglob('*') if f.is_file()})

    def test_identifiants_joueurs_courts_et_urls_refuses(self):
        for texte in ('playerId=42', 'user_id: 7', 'joueur 1',
                      'https://www.roblox.com/users/42/profile', 'Compte 123456789'):
            with self.subTest(texte=texte):
                self.assertEqual(self.envoyer(texte=texte), 7)
        self.assertEqual(self.messages, [])

    def test_resume_agrege_autorise(self):
        self.assertEqual(self.envoyer(texte='Joueurs : 3 ; sessions : 100 ; J1 : 12 %.'), 0)

    def test_anti_repetition_sans_cle(self):
        self.assertEqual(self.envoyer(), 0)
        self.assertEqual(self.envoyer(), 3)
        self.assertEqual(len(self.messages), 1)

    def test_changement_de_niveau_ne_raccourcit_pas_le_delai(self):
        self.assertEqual(self.envoyer(niveau='info', cle='incident'), 0)
        self.assertEqual(self.envoyer(niveau='urgent', cle='incident',
                                     maintenant=self.date + timedelta(hours=2)), 3)
        self.assertEqual(len(self.messages), 1)

    def test_plafond_compte_en_utc(self):
        ecrire_sur(self.racine / 'JOURNAUX/prevenir-etat.json', json_texte({
            'cles': {}, 'jours': {'2026-11-17': 20}}))
        self.assertEqual(self.envoyer(maintenant=self.date.astimezone(timezone(timedelta(hours=2)))), 3)
        self.assertEqual(self.messages, [])

    def test_plantage_apres_envoi_ne_permet_pas_le_rejeu(self):
        def envoyer_puis_planter(*args):
            self.messages.append(args)
            raise KeyboardInterrupt()
        with patch.object(p, 'transport', side_effect=envoyer_puis_planter):
            with self.assertRaises(KeyboardInterrupt):
                self.envoyer(cle='incident')
        self.assertEqual(self.envoyer(cle='incident'), 3)
        self.assertEqual(len(self.messages), 1)

    @unittest.skipUnless(os.name == 'nt', 'Mutex natif Windows')
    def test_mutex_interprocessus_et_abandon(self):
        code = ('import sys; sys.path.insert(0, sys.argv[1]); import prevenir; '
                'verrou = prevenir.verrou_local(sys.argv[2], sys.argv[3]); verrou.__enter__(); '
                'print("acquis", flush=True); sys.stdin.read()')
        for nom in ('contact', 'battement', 'interrupteurs'):
            with self.subTest(nom=nom):
                enfant = subprocess.Popen([sys.executable, '-c', code, str(Path(__file__).parent), str(self.racine), nom],
                                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                try:
                    self.assertEqual(enfant.stdout.readline().strip(), 'acquis')
                    with self.assertRaises(OSError):
                        with p.verrou_local(self.racine, nom):
                            self.fail('Deux processus possèdent le mutex')
                finally:
                    enfant.terminate()
                    enfant.communicate(timeout=10)
                with p.verrou_local(self.racine, nom):
                    pass  # Le noyau rend un mutex abandonné, aucun fichier périmé.


if __name__ == '__main__':
    main()
    raise SystemExit(not unittest.TextTestRunner(stream=sys.stdout).run(unittest.defaultTestLoader.loadTestsFromTestCase(Regressions)).wasSuccessful())

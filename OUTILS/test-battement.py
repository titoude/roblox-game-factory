"""Tests du battement en arborescence temporaire, sans modèle ni réseau."""
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import battement as b
from usine_opencloud import ecrire_sur, json_texte


def main():
    nombre = 0
    def verifier(condition, nom):
        nonlocal nombre
        assert condition, nom
        nombre += 1
        print('OK : ' + nom)
    with tempfile.TemporaryDirectory() as tmp:
        racine = Path(tmp)
        date = datetime(2026, 11, 16, 12, tzinfo=timezone.utc)
        jeu = racine / 'JEUX/essai'
        notifications = []
        etat = {'statut': 'en_cours', 'portes': {}, 'place': {}}
        seuils = {'retours': {'joueurs_distincts_pour_ameliorer': 3}}
        def sauver():
            ecrire_sur(jeu / 'ETAT.json', json_texte(etat))
            ecrire_sur(racine / 'CONNAISSANCES/seuils.json', json_texte(seuils))
        def prevenir(*args, **kw):
            notifications.append((args, kw))
            return 0
        def tour(**kw):
            with redirect_stdout(io.StringIO()):
                return b.battement(racine, maintenant=date, _prevenir=prevenir, _commit=date.timestamp(), **kw)
        def unique(prefixe, action=None):
            avant = len([n for n in notifications if n[1]['cle'].startswith(prefixe)])
            if action:
                action()
            tour()
            tour()
            return len([n for n in notifications if n[1]['cle'].startswith(prefixe)]) == avant + 1
        sauver()
        verifier('DECISION: lancer | reprendre essai' in tour(), 'décision lancer : jeu en cours')
        etat['statut'] = 'termine'
        sauver()
        ecrire_sur(racine / 'VEILLE/TENDANCES.md', 'Veille récente\n')
        os.utime(racine / 'VEILLE/TENDANCES.md', (date.timestamp(), date.timestamp()))
        verifier('DECISION: attendre' in tour(), 'décision attendre : rien de prêt')
        os.utime(racine / 'VEILLE/TENDANCES.md', (date.timestamp() - 8 * 86400,) * 2)
        verifier('DECISION: lancer | veille' in tour(), 'veille ancienne : lancer')
        etat['statut'] = 'en_cours'
        sauver()
        ecrire_sur(racine / 'VERROUS/studio.lock', '{"expire":"2020-01-01"}\n')
        verifier('DECISION: lancer' in tour() and 'expiré' in tour(), 'verrou expiré ignoré et signalé')
        ecrire_sur(racine / 'VERROUS/studio.lock', '{"expire":"2027-01-01T00:00:00Z"}\n')
        etat['etape'] = '06-qa'
        sauver()
        avant = len(notifications)
        with redirect_stdout(io.StringIO()):
            b.battement(racine, maintenant=date, _prevenir=prevenir, _commit=date.timestamp() - 49 * 3600)
        verifier(len(notifications) == avant, 'verrou explique absence de progrès')
        (racine / 'VERROUS/studio.lock').unlink()
        etat['etape'] = '02-concept'
        sauver()
        for typ in ('connexion', 'paiement', 'captcha', '2fa', 'permission'):
            ecrire_sur(racine / 'ALERTES.md', f'| 2026-11-16 10:00 | {typ} | test | - | test | constat | ouverte |\n')
            verifier(unique('alerte-'), 'nouvelle alerte une fois : ' + typ)
            verifier(notifications[-1][0][0] == ('important' if typ == 'permission' else 'urgent'), 'niveau alerte ' + typ)
        ecrire_sur(racine / 'ALERTES.md', '# Aucune alerte\n')
        etat['portes']['P7'] = {'resultat': 'passe'}
        sauver()
        verifier(unique('p7-'), 'P7 passe : une seule notification')
        mesures = jeu / '08-distribution/MESURES.csv'
        ecrire_sur(mesures, 'jour,refus_action,sessions\n2026-11-16,21,\n')
        verifier(unique('incident-'), 'incident refus sans historique : une fois')
        # Nouveau compteur avec historique : seuil 5 x médiane = 50.
        historique = ''.join(f'{(date.date()-timedelta(days=i)).isoformat()},10,100\n' for i in range(1, 9))
        ecrire_sur(mesures, 'jour,anomalie_action,sessions\n' + historique + '2026-11-16,51,\n')
        verifier(unique('incident-'), 'incident avec historique : une fois')
        ecrire_sur(mesures, 'jour,refus_historique,sessions\n' + historique + '2026-11-16,50,\n')
        avant = len(notifications)
        tour()
        verifier(len(notifications) == avant, 'seuil strict : égalité sans incident')
        ecrire_sur(mesures, 'jour,refus_historique,sessions\n' + historique + '2026-11-16,51,\n')
        verifier(unique('incident-'), 'incident refus avec historique : une fois')
        ecrire_sur(mesures, 'jour,sessions\n' + ''.join(f'{(date.date()-timedelta(days=i)).isoformat()},100\n' for i in range(2, 9)))
        avant = len(notifications)
        tour()
        verifier(len(notifications) == avant, 'jour absent : pas une chute à zéro')
        ajouter = mesures.read_text() + '2026-11-15,10\n'
        ecrire_sur(mesures, ajouter)
        verifier(unique('chute-'), 'chute des sessions : une fois')
        avant = len(notifications)
        for _ in range(2):
            with redirect_stdout(io.StringIO()):
                b.battement(racine, maintenant=date, _prevenir=prevenir, _commit=date.timestamp() - 49 * 3600)
        verifier(len(notifications) == avant + 1 and notifications[-1][1]['cle'].startswith('sans-progres-'), 'sans progrès : une fois')
        cycles = racine / 'JOURNAUX/cycles.log'
        ecrire_sur(cycles, ''.join(f'2026-11-16T10:00:00Z | tour {i}/7 | test\n' for i in range(1, 8)))
        verifier(unique('quota-'), 'quota dépassé : une fois')
        verifier('DECISION: attendre' in tour(), 'plafond quotidien empêche lancement')
        ecrire_sur(cycles, '# Aucun tour\n')
        seuils['permanence'] = {'heures_actives': '13-18'}
        sauver()
        verifier('hors heures actives' in tour(), 'heures actives')
        verifier(b.actif(23, '22-06') and b.actif(5, '22-06') and not b.actif(12, '22-06'), 'plage traverse minuit')
        seuils['permanence']['heures_actives'] = '00-24'
        etat['statut'] = 'termine'
        sauver()
        ecrire_sur(jeu / '10-retours/LOT-2026-11-16.json', json_texte({'groupes': [{'statut': 'a_juger', 'joueurs_distincts': 3}]}))
        verifier('DECISION: lancer | retours essai' in tour(), 'lot de retours atteint le seuil')
        etat['place']['universeId_prod'] = '123'
        sauver()
        def absent(slug):
            return 'nom-autorise', None
        tour(_identifiant=absent)
        tour(_identifiant=absent)
        verifier((racine / 'JOURNAUX/battement.log').read_text().count('identifiant Open Cloud absent') == 1, 'identifiant absent noté une fois par jour')
        appels = []
        def execution(r, outil, commande, slug):
            appels.append((outil, commande))
            return 4 if commande == 'collecter' and outil == 'mesures-joueurs.py' else 0
        tour(_identifiant=lambda slug: ('nom', 'faux'), _executer=execution)
        verifier(appels == [('mesures-joueurs.py', 'collecter'), ('retours-joueurs.py', 'collecter'), ('retours-joueurs.py', 'trier')], 'échec collecte : jugement ignoré, autre outil servi')
        lancements = []
        ancien_run = b.subprocess.run
        try:
            b.subprocess.run = lambda args, **kw: lancements.append(args)
            ecrire_sur(cycles, ''.join(f'2026-11-16T10:00:00Z | tour {i}/5 | test\n' for i in range(1, 6)))
            tour(lancer=True, _identifiant=absent)
            verifier(len(lancements) == 1 and lancements[0][-2:] == ['--tours', '1'], 'lancement limité au quota restant (appel intercepté)')
            ecrire_sur(cycles, cycles.read_text() + '2026-11-16T11:00:00Z | tour 6/6 | test\n')
            tour(lancer=True, _identifiant=absent)
            verifier(len(lancements) == 1, 'quota atteint : aucun appel orchestrateur')
            tour(lancer=True, simuler=True)
            verifier(len(lancements) == 1, 'simulation avec lancer : aucun appel orchestrateur')
        finally:
            b.subprocess.run = ancien_run
        avant = {p.relative_to(racine): p.read_bytes() for p in racine.rglob('*') if p.is_file()}
        tour(simuler=True)
        apres = {p.relative_to(racine): p.read_bytes() for p in racine.rglob('*') if p.is_file()}
        verifier(avant == apres, 'simulation strictement sans écriture')
        ecrire_sur(racine / 'STOP', 'arrêt\n')
        avant = (racine / 'JOURNAUX/battement.log').read_bytes()
        verifier('STOP présent' in tour() and (racine / 'JOURNAUX/battement.log').read_bytes() == avant, 'STOP : bloqué sans écriture')
    print(f'{nombre} contrôles passés.')
    return 0


class Regressions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.racine = Path(self.tmp.name)
        self.jeu = self.racine / 'JEUX/essai'
        self.date = datetime(2026, 11, 17, 12, tzinfo=timezone.utc)
        self.etat = {'statut': 'en_cours', 'etape': '02-concept', 'portes': {}, 'place': {}}
        self.seuils = {}
        self.sauver()

    def sauver(self):
        ecrire_sur(self.jeu / 'ETAT.json', json_texte(self.etat))
        ecrire_sur(self.racine / 'CONNAISSANCES/seuils.json', json_texte(self.seuils))

    def tour(self, **kw):
        with redirect_stdout(io.StringIO()):
            return b.battement(self.racine, maintenant=self.date, _commit=self.date.timestamp(),
                               _prevenir=kw.pop('_prevenir', lambda *a, **k: 0), **kw)

    def verrou(self, ressource='studio', expire='2026-11-18T00:00:00Z'):
        ecrire_sur(self.racine / 'VERROUS' / (ressource.replace(':', '_') + '.lock'),
                   json_texte({'ressource': ressource, 'expire': expire}))

    def test_verrou_expire_ignore_signale_et_conserve(self):
        self.etat['etape'] = '06-qa'
        self.sauver()
        self.verrou(expire='2026-11-17T13:00:00+02:00')
        ligne = self.tour()
        self.assertIn('DECISION: lancer', ligne)
        self.assertIn('expiré', ligne)
        self.assertTrue((self.racine / 'VERROUS/studio.lock').exists())

    def test_verrou_utile_attendre(self):
        self.etat.update(etape='06-qa', place={'placeId_test': '123', 'placeId_prod': '456'})
        self.sauver()
        for ressource in ('studio', 'bureau', 'place:123'):
            with self.subTest(ressource=ressource):
                self.verrou(ressource)
                self.assertIn('DECISION: attendre', self.tour())
                (self.racine / 'VERROUS' / (ressource.replace(':', '_') + '.lock')).unlink()
        self.verrou('place:456')
        self.assertIn('DECISION: lancer', self.tour())

    def test_verrou_sans_rapport_lancer_code_hors_studio(self):
        self.etat['etape'] = '05-production'
        self.sauver()
        for ressource in ('studio', 'bureau', 'place:123', 'chrome:veille'):
            self.verrou(ressource)
        self.assertIn('DECISION: lancer | reprendre essai', self.tour())

    def test_production_attente_explicite_studio(self):
        self.etat.update(etape='05-production', blocage='Attend : Studio libre, puis prototype en Play.')
        self.sauver()
        self.verrou()
        self.assertIn('DECISION: attendre', self.tour())

    def test_verrou_chrome_necessaire_et_verrou_illisible(self):
        self.etat['etape'] = '08-distribution'
        self.sauver()
        self.verrou('chrome:veille')
        self.assertIn('DECISION: attendre', self.tour())
        (self.racine / 'VERROUS/chrome_veille.lock').unlink()
        self.etat['etape'] = '06-qa'
        self.sauver()
        ecrire_sur(self.racine / 'VERROUS/studio.lock', '{tronque')
        self.assertIn('DECISION: attendre', self.tour())

    def test_un_autre_jeu_disponible_est_selectionne(self):
        self.etat['etape'] = '06-qa'
        self.sauver()
        self.verrou()
        ecrire_sur(self.racine / 'JEUX/autre/ETAT.json', json_texte({
            'statut': 'en_cours', 'etape': '03-economie'}))
        self.assertIn('DECISION: lancer | reprendre autre', self.tour())

    def test_seuils_incident_et_chute_lus(self):
        for seuil, valeur, compteur, courant, base, attendu in (
                ('incident_refus_min', 100, 'refus_action', 51, None, False),
                ('incident_facteur_mediane', 10, 'refus_action', 51, 10, False),
                ('chute_sessions_pct', 10, 'sessions', 20, 100, False),
                ('chute_mediane_min', 200, 'sessions', 5, 100, False),
                ('incident_refus_min', 1, 'refus_action', 2, None, True),
                ('incident_facteur_mediane', 2, 'refus_action', 21, 10, True),
                ('chute_sessions_pct', 50, 'sessions', 40, 100, True),
                ('chute_mediane_min', 1, 'sessions', 1, 10, True)):
            with self.subTest(seuil=seuil, valeur=valeur):
                self.seuils['permanence'] = {seuil: valeur}
                self.sauver()
                debut = 2 if compteur == 'sessions' else 1
                historique = '' if base is None else ''.join(
                    f'{(self.date.date()-timedelta(days=i)).isoformat()},{base}\n' for i in range(debut, 9))
                jour = '2026-11-16' if compteur == 'sessions' else '2026-11-17'
                ecrire_sur(self.jeu / '08-distribution/MESURES.csv',
                           'jour,' + compteur + '\n' + historique + jour + ',' + str(courant) + '\n')
                ecrire_sur(self.racine / 'JOURNAUX/battement-etat.json', json_texte({'evenements': [], 'absents': {}}))
                notifications = []
                self.tour(_prevenir=lambda *a, **k: notifications.append(k) or 0)
                self.assertEqual(bool(notifications), attendu)

    def test_heures_locales_et_quota_utc_autour_de_minuit(self):
        self.date = datetime(2026, 11, 18, 0, 30, tzinfo=timezone(timedelta(hours=2)))
        self.seuils['permanence'] = {'heures_actives': '00-01'}
        self.sauver()
        self.assertIn('DECISION: lancer', self.tour())
        ecrire_sur(self.racine / 'JOURNAUX/cycles.log', ''.join(
            f'2026-11-17T20:00:00Z | tour {i}/6 | test\n' for i in range(1, 7)))
        self.assertIn('plafond quotidien', self.tour())

    def test_notification_filtree_reste_a_livrer(self):
        ecrire_sur(self.racine / 'ALERTES.md', '| date | permission | test | - | test | constat | ouverte |\n')
        self.tour(_prevenir=lambda *a, **k: 3)
        notifications = []
        self.tour(_prevenir=lambda *a, **k: notifications.append(k) or 0)
        self.assertEqual(len(notifications), 1)

    def test_nom_compteur_externe_ne_fuit_pas_dans_les_cles(self):
        ecrire_sur(self.jeu / '08-distribution/MESURES.csv',
                   'jour,refus_userid_123456789\n2026-11-17,21\n')
        notifications = []
        self.tour(_prevenir=lambda *a, **k: notifications.append(k) or 0)
        traces = json_texte([{k: v for k, v in n.items() if k != 'racine'} for n in notifications])
        traces += (self.racine / 'JOURNAUX/battement-etat.json').read_text(encoding='utf-8')
        traces += (self.racine / 'JOURNAUX/battement.log').read_text(encoding='utf-8')
        self.assertNotIn('123456789', traces)

    def test_ancienne_cle_compteur_reconnue_sans_renotifier(self):
        ecrire_sur(self.jeu / '08-distribution/MESURES.csv',
                   'jour,refus_userid_123456789\n2026-11-17,21\n')
        ecrire_sur(self.racine / 'JOURNAUX/battement-etat.json', json_texte({
            'evenements': ['incident-essai-2026-11-17-refus_userid_123456789'], 'absents': {}}))
        notifications = []
        self.tour(_prevenir=lambda *a, **k: notifications.append(k) or 0)
        self.assertEqual(notifications, [])
        self.assertNotIn('123456789', (self.racine / 'JOURNAUX/battement-etat.json').read_text(encoding='utf-8'))

    def test_notification_acceptee_persiste_avant_suite_en_panne(self):
        ecrire_sur(self.racine / 'ALERTES.md', '| date | permission | test | - | test | constat | ouverte |\n')
        self.etat['place']['universeId_prod'] = '123'
        self.sauver()
        notifications = []
        with self.assertRaises(OSError):
            self.tour(_prevenir=lambda *a, **k: notifications.append(k) or 0,
                      _identifiant=lambda _: (_ for _ in ()).throw(OSError('panne')))
        self.tour(_prevenir=lambda *a, **k: notifications.append(k) or 0,
                  _identifiant=lambda _: ('nom', None))
        self.assertEqual(len(notifications), 1)

    def test_lancement_incertain_non_rejoue_apres_plantage(self):
        with patch.object(b.subprocess, 'run', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.tour(lancer=True)
        with patch.object(b.subprocess, 'run') as lancement:
            self.assertIn('DECISION: bloque', self.tour(lancer=True))
            lancement.assert_not_called()


if __name__ == '__main__':
    resultat = unittest.TextTestRunner(stream=sys.stdout).run(unittest.defaultTestLoader.loadTestsFromTestCase(Regressions))
    if resultat.wasSuccessful():
        main()
    raise SystemExit(not resultat.wasSuccessful())

"""Battement sans modèle par défaut ; --simuler ne modifie aucun fichier.
Défauts permanence : tours_max_par_jour=6, tours_par_battement=2,
heures_actives="00-24", sans_progres_heures=48. Dates des mesures et quotas UTC ;
heures actives en heure locale du poste. Aucun verrou existant n'est libéré.
"""
import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
from pathlib import Path
import re
from statistics import median
import subprocess
import sys
from usine_opencloud import ecrire_sur, lire_json, json_texte, identifiant
import prevenir

RACINE = Path(__file__).resolve().parent.parent
DEFAUTS = dict(tours_max_par_jour=6, tours_par_battement=2,
               heures_actives='00-24', sans_progres_heures=48,
               incident_refus_min=20, incident_facteur_mediane=5,
               chute_sessions_pct=30, chute_mediane_min=20)


def lire(chemin, defaut):
    return lire_json(chemin) if chemin.exists() else defaut


def ajouter(chemin, texte):
    ecrire_sur(chemin, (chemin.read_text(encoding='utf-8') if chemin.exists() else '') + texte + '\n')


def alertes(racine):
    chemin = racine / 'ALERTES.md'
    resultat = []
    for ligne in chemin.read_text(encoding='utf-8-sig').splitlines() if chemin.exists() else []:
        cellules = [c.strip() for c in ligne.strip().strip('|').split('|')]
        if len(cellules) == 7 and cellules[-1] == 'ouverte':
            resultat.append(cellules)
    return resultat


def tours_du_jour(racine, jour):
    chemin = racine / 'JOURNAUX/cycles.log'
    return sum(l.startswith(jour) and bool(re.search(r'\| tour \d+/\d+ \|', l))
               for l in chemin.read_text(encoding='utf-8').splitlines()) if chemin.exists() else 0


def actif(heure, plage):
    debut, fin = map(int, plage.split('-'))
    if not 0 <= debut <= 23 or not 0 <= fin <= 24:
        raise ValueError('Plage invalide')
    return debut <= heure < fin if debut < fin else heure >= debut or heure < fin


def compteurs(chemin):
    if not chemin.exists():
        return {}
    with chemin.open(encoding='utf-8-sig', newline='') as f:
        return {r['jour']: {k: int(v) for k, v in r.items() if k != 'jour' and v != ''}
                for r in csv.DictReader(f)}


def executer(racine, outil, commande, slug):
    return subprocess.run([sys.executable, str(racine / 'OUTILS' / outil), commande, '--jeu', slug],
                          cwd=racine, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          timeout=600).returncode


def verrous_actifs(racine, utc):
    actifs, expires, illisibles = set(), 0, 0
    for chemin in (racine / 'VERROUS').glob('*.lock'):
        nom = chemin.stem
        if re.fullmatch(r'place_\d+|chrome_[A-Za-z0-9_-]+', nom):
            nom = nom.replace('_', ':', 1)
        elif nom not in ('studio', 'bureau'):
            continue
        try:
            expiration = datetime.fromisoformat(lire_json(chemin)['expire'].replace('Z', '+00:00'))
            # Les verrous actuels sont en UTC ; les anciens sans offset aussi.
            if expiration.tzinfo is None:
                expiration = expiration.replace(tzinfo=timezone.utc)
            if expiration <= utc:
                expires += 1
                continue
        except FileNotFoundError:
            continue  # Rendu entre l'énumération et la lecture.
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            illisibles += 1  # Une écriture interrompue ne prouve pas la liberté.
        actifs.add(nom)
    return actifs, expires, illisibles


def besoins(etat):
    etape, blocage = etat.get('etape', ''), etat.get('blocage', '')
    ressources = set()
    # La production commence par code, banc et relecture hors Studio (P14).
    # Une attente de Play/Studio inscrite dans l'état indique la suite en place.
    en_studio = etape == '06-qa' or (etape == '05-production' and bool(re.search(
        r'attend.*studio|studio.*(?:libre|verrou|indisponible)|prototype.*play', blocage, re.I)))
    if en_studio:
        ressources.update(('studio', 'bureau'))
    if en_studio or etape == '07-release':
        place = etat.get('place', {})
        cible = place.get('placeId_prod') if etape == '07-release' else (
            place.get('placeId_test') or place.get('placeId_prod'))
        if cible:
            ressources.add('place:' + str(cible))
    if etape in ('01-veille', '07-release', '08-distribution'):
        ressources.update(('bureau', 'chrome:*'))
    return ressources


def depend(etat, verrous):
    requis = besoins(etat)
    return bool(requis & verrous or ('chrome:*' in requis and any(v.startswith('chrome:') for v in verrous)))


@prevenir.serialiser('battement')
def battement(racine=RACINE, simuler=False, maintenant=None, lancer=False, *,
              _prevenir=None, _identifiant=None, _executer=None, _commit=None):
    racine = Path(racine)
    local = maintenant or datetime.now().astimezone()
    if local.tzinfo is None:
        local = local.astimezone()
    utc = local.astimezone(timezone.utc)
    jour = utc.date().isoformat()
    log = racine / 'JOURNAUX/battement.log'
    if (racine / 'STOP').exists():
        ligne = 'DECISION: bloque | - | STOP présent'
        print(ligne)
        # G0 : aucune écriture du battement sous STOP.
        return ligne
    seuils = lire(racine / 'CONNAISSANCES/seuils.json', {})
    permanence = dict(DEFAUTS, **seuils.get('permanence', {}))
    if any(type(permanence[c]) is not int or permanence[c] < 1 for c in
           ('tours_max_par_jour', 'tours_par_battement', 'sans_progres_heures',
            'incident_refus_min', 'incident_facteur_mediane', 'chute_mediane_min', 'chute_sessions_pct')):
        raise ValueError('Seuil invalide')
    if permanence['chute_sessions_pct'] > 100:
        raise ValueError('Pourcentage invalide')
    horaire = actif(local.hour, permanence['heures_actives'])
    chemin_etat = racine / 'JOURNAUX/battement-etat.json'
    etat = lire(chemin_etat, {'evenements': [], 'absents': {}})
    vus = set(etat['evenements'])
    ouverts = alertes(racine)
    verrous, expires, illisibles = verrous_actifs(racine, utc)
    jeux = [(p.parent, lire_json(p)) for p in sorted((racine / 'JEUX').glob('*/ETAT.json'))]
    en_cours = [(p, e) for p, e in jeux if e.get('statut') == 'en_cours']
    quota = tours_du_jour(racine, jour)
    notifier = _prevenir or prevenir.envoyer

    def evenement(cle, niveau, sujet, texte, slug=None):
        if cle in vus:
            return
        if simuler:
            print('SIMULATION : notification ' + niveau + ' : ' + sujet)
            return
        code = notifier(niveau, sujet, texte, cle=cle, jeu=slug, racine=racine)
        # Journal seul/filtrage ne prouve pas la livraison au propriétaire.
        if code == 0:
            vus.add(cle)
            etat['evenements'] = sorted(vus)
            ecrire_sur(chemin_etat, json_texte(etat))
        ajouter(log, f'{utc.isoformat()} | notification {niveau} | code {code}')

    for a in ouverts:
        cle = 'alerte-' + hashlib.sha256('|'.join(a[:5]).encode()).hexdigest()[:24]
        evenement(cle, 'urgent' if a[1] in ('connexion', 'paiement', 'captcha', '2fa') else 'important',
                  'Action du propriétaire requise', 'Une alerte est ouverte. Consulter ALERTES.md sur le poste.')
    lots = []
    collecte_en_panne = False
    for dossier, e in jeux:
        slug = dossier.name
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            continue
        if e.get('place', {}).get('universeId_prod') and not simuler:
            _, secret = (_identifiant or identifiant)(slug)
            if not secret:
                if etat['absents'].get(slug) != jour:
                    ajouter(log, f'{utc.isoformat()} | {slug} | identifiant Open Cloud absent, collecte ignorée')
                    etat['absents'][slug] = jour
            else:
                for outil, suite in [('mesures-joueurs.py', ('collecter', 'juger')),
                                     ('retours-joueurs.py', ('collecter', 'trier'))]:
                    for commande in suite:
                        try:
                            code = (_executer or executer)(racine, outil, commande, slug)
                        except (OSError, subprocess.TimeoutExpired):
                            code = 6
                        ajouter(log, f'{utc.isoformat()} | {slug} | {outil} {commande} | code {code}')
                        if code != 0:
                            collecte_en_panne = True
                            break
        p7 = e.get('portes', {}).get('P7', {})
        rapports = sorted((dossier / '08-distribution').glob('MESURES-*.md'))
        passe = p7.get('resultat') == 'passe'
        if rapports and not p7:
            passe |= bool(re.search(r'^P7: passe\b', rapports[-1].read_text(encoding='utf-8'), re.M))
        if passe:
            evenement('p7-' + slug, 'important', 'Un jeu marche',
                      'La porte P7 vient de passer. Vérifier les preuves de distribution.', slug)
        mesures = compteurs(dossier / '08-distribution/MESURES.csv')
        for nom, valeur in mesures.get(jour, {}).items():
            if nom.startswith(('refus_', 'anomalie_')):
                precedent = [mesures.get((utc.date() - timedelta(days=i)).isoformat(), {}).get(nom)
                             for i in range(1, 8)]
                precedent = [v for v in precedent if v is not None]
                seuil = max(permanence['incident_refus_min'], permanence['incident_facteur_mediane'] * median(precedent)) if precedent else permanence['incident_refus_min']
                if valeur > seuil:
                    # Le nom vient du jeu : il peut contenir un identifiant même
                    # quand le texte de la notification reste agrégé.
                    prefixe = 'incident-' + slug + '-' + jour + '-'
                    cle = prefixe + hashlib.sha256(nom.encode()).hexdigest()
                    ancienne_cle = prefixe + nom
                    if ancienne_cle in vus:
                        vus.remove(ancienne_cle)
                        vus.add(cle)
                    evenement(cle, 'urgent',
                              'Incident probable sur un jeu', 'Un compteur de sécurité dépasse son seuil. Vérifier les mesures.', slug)
        hier = utc.date() - timedelta(days=1)
        sessions = mesures.get(hier.isoformat(), {}).get('sessions')
        precedent = [mesures.get((hier - timedelta(days=i)).isoformat(), {}).get('sessions') for i in range(1, 8)]
        # Sept jours complets sont nécessaires pour annoncer une chute de fréquentation.
        if sessions is not None and all(v is not None for v in precedent):
            base = median(precedent)
            if base >= permanence['chute_mediane_min'] and sessions < permanence['chute_sessions_pct'] / 100 * base:
                evenement('chute-' + slug + '-' + hier.isoformat(), 'urgent',
                          'Chute brutale des sessions', 'Les sessions du jour terminé sont sous le seuil de la médiane précédente.', slug)
        lot = sorted((dossier / '10-retours').glob('LOT-*.json'))
        if lot and any(g.get('statut') == 'a_juger' and g.get('joueurs_distincts', 0) >=
                       seuils.get('retours', {}).get('joueurs_distincts_pour_ameliorer', 3)
                       for g in lire_json(lot[-1]).get('groupes', [])):
            lots.append(slug)
    if en_cours and not ouverts and not any(depend(e, verrous) for _, e in en_cours):
        if _commit is not None:
            dernier = _commit
        else:
            r = subprocess.run(['git', 'log', '-1', '--format=%ct'], cwd=racine,
                               capture_output=True, text=True, timeout=10)
            dernier = float(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
        if dernier is not None and utc.timestamp() - dernier >= permanence['sans_progres_heures'] * 3600:
            evenement('sans-progres-' + str(int(dernier)), 'important', 'Usine sans progrès',
                      'Aucun commit depuis le seuil prévu, sans alerte ni verrou explicatif.')
    if quota > permanence['tours_max_par_jour']:
        evenement('quota-' + jour, 'important', 'Quota quotidien dépassé',
                  'Le nombre de tours journalisés dépasse le plafond de permanence.')
    demande, decision, raison = '-', 'attendre', 'aucun travail prêt'
    candidats = [(p, e) for p, e in jeux if e.get('statut') in ('en_cours', 'bloque')
                 and not any(a[3] in ('-', p.name) for a in ouverts)]
    libres = [(p, e) for p, e in candidats if e.get('statut') == 'en_cours' and not e.get('blocage') and not depend(e, verrous)]
    if etat.get('lancement'):
        decision, raison = 'bloque', 'lancement précédent non réconcilié (voir battement-etat.json)'
    elif not horaire:
        raison = 'hors heures actives'
    elif quota >= permanence['tours_max_par_jour']:
        raison = 'plafond quotidien de tours atteint'
    elif libres:
        decision, demande, raison = 'lancer', 'reprendre ' + libres[0][0].name, 'jeu en cours disponible'
    elif ouverts and any(a[3] == '-' for a in ouverts):
        decision, raison = 'bloque', 'alerte globale ouverte'
    elif lots:
        disponibles = [s for s in lots if not any(a[3] == s for a in ouverts)]
        if disponibles:
            decision, demande, raison = 'lancer', 'retours ' + disponibles[0], 'lot de retours prêt'
    elif any(depend(e, verrous) for _, e in candidats):
        raison = 'ressource nécessaire à la prochaine étape verrouillée'
    elif en_cours or any(e.get('statut') == 'bloque' for _, e in jeux):
        decision, raison = 'bloque', 'jeu bloqué ou alerte ouverte'
    else:
        tendance = racine / 'VEILLE/TENDANCES.md'
        if not tendance.exists() or utc.timestamp() - tendance.stat().st_mtime > 7 * 86400:
            if depend({'etape': '01-veille'}, verrous):
                raison = 'ressource nécessaire à la veille verrouillée'
            else:
                decision, demande, raison = 'lancer', 'veille', 'veille absente ou de plus de 7 jours'
    if expires:
        raison += f' ; {expires} verrou(s) expiré(s) ignoré(s), conservé(s)'
    if illisibles:
        raison += f' ; {illisibles} verrou(s) illisible(s) conservé(s) actif(s)'
    if collecte_en_panne:
        raison += ' ; collecte incomplète (voir journal)'
    ligne = f'DECISION: {decision} | {demande} | {raison}'
    print(ligne)
    if not simuler:
        etat['evenements'] = sorted(vus)
        ecrire_sur(chemin_etat, json_texte(etat))
        ajouter(log, utc.isoformat() + ' | ' + ligne)
    if lancer and not simuler and decision == 'lancer' and not (racine / 'STOP').exists():
        tours = min(permanence['tours_par_battement'], permanence['tours_max_par_jour'] - quota)
        # Réservation durable avant le processus enfant. Si le parent meurt,
        # l'enfant peut vivre encore : aucune reprise automatique ne peut le nier.
        etat['lancement'] = {'date': utc.isoformat(), 'demande': demande, 'tours': tours}
        ecrire_sur(chemin_etat, json_texte(etat))
        subprocess.run([sys.executable, str(racine / 'usine.py'), demande, '--tours', str(tours)], cwd=racine, check=False)
        del etat['lancement']
        ecrire_sur(chemin_etat, json_texte(etat))
    return ligne


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--simuler', action='store_true')
    p.add_argument('--lancer', action='store_true')
    p.add_argument('--maintenant', type=lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M'))
    a = p.parse_args(argv)
    try:
        battement(simuler=a.simuler, maintenant=a.maintenant, lancer=a.lancer)
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
        print('DECISION: bloque | - | lecture ou configuration invalide (détails masqués)')
        return 2


if __name__ == '__main__':
    sys.exit(main())

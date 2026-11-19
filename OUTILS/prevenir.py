"""Notifications privées du propriétaire, bibliothèque standard Windows.
Codes : 0 canal externe accepté ; 3 sans envoi (désactivé, STOP ou filtré) ;
4 tous les canaux externes sélectionnés en échec ; 2 usage/configuration ; 7 refus.
Les injections _secrets, _urls et _smtp sont exclusivement des paramètres Python
pour les tests ; aucune option CLI ne permet de rediriger un secret de production.
"""
import argparse
from contextlib import contextmanager
from functools import wraps
import hashlib
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from email.message import EmailMessage
import importlib.util
import json
import multiprocessing
import os
from pathlib import Path
import re
import smtplib
import ssl
import subprocess
import sys
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, ProxyHandler
from usine_opencloud import ecrire_sur, lire_json, json_texte, SansRedirection

RACINE = Path(__file__).resolve().parent.parent
NIVEAUX = {'info': 0, 'important': 1, 'urgent': 2}
DELAIS = {'info': 86400, 'important': 43200, 'urgent': 3600}
CANAUX = ('windows', 'discord', 'ntfy', 'courriel')
NOMS = {'discord': 'discord-webhook', 'ntfy': 'ntfy-sujet', 'courriel': 'smtp'}
_spec = importlib.util.spec_from_file_location('deleguer_contact', Path(__file__).with_name('deleguer.py'))
_deleguer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_deleguer)


@contextmanager
def verrou_local(racine, nom):
    # Mutex de processus : protège les remplacements atomiques concurrents sous Windows.
    if os.name != 'nt':
        yield
        return
    api = ctypes.WinDLL('kernel32', use_last_error=True)
    api.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
    api.CreateMutexW.restype = wintypes.HANDLE
    api.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    api.ReleaseMutex.argtypes = [wintypes.HANDLE]
    api.CloseHandle.argtypes = [wintypes.HANDLE]
    identite = hashlib.sha256(str(Path(racine).resolve()).lower().encode()).hexdigest()
    handle = api.CreateMutexW(None, False, 'Local\\UsineRoblox-' + nom + '-' + identite)
    acquis = False
    try:
        if not handle:
            raise OSError('Mutex indisponible')
        acquis = api.WaitForSingleObject(handle, 0) in (0, 0x80)
        if not acquis:
            raise OSError('Une exécution est déjà en cours')
        yield
    finally:
        if acquis:
            api.ReleaseMutex(handle)
        if handle:
            api.CloseHandle(handle)


def serialiser(nom):
    def decorer(fonction):
        @wraps(fonction)
        def appel(*args, **kw):
            with verrou_local(kw.get('racine', args[0] if nom == 'battement' and args else RACINE), nom):
                return fonction(*args, **kw)
        return appel
    return decorer


def lire_contact(nom):
    # Noms dédiés uniquement ; les clés Open Cloud servent au refus des fuites.
    permis = {'usine-roblox:contact:' + n for n in NOMS.values()}
    permis.update(('usine-roblox:opencloud:lecture', 'usine-roblox:opencloud:interrupteurs'))
    if (nom not in permis and not re.fullmatch(r'usine-roblox:opencloud:[a-z0-9-]+:lecture', nom)) or os.name != 'nt':
        raise ValueError('Identifiant interdit ou Windows absent')
    class Credential(ctypes.Structure):
        _fields_ = [('Flags', wintypes.DWORD), ('Type', wintypes.DWORD),
                    ('TargetName', wintypes.LPWSTR), ('Comment', wintypes.LPWSTR),
                    ('LastWritten', wintypes.FILETIME), ('CredentialBlobSize', wintypes.DWORD),
                    ('CredentialBlob', ctypes.POINTER(ctypes.c_ubyte)),
                    ('Persist', wintypes.DWORD), ('AttributeCount', wintypes.DWORD),
                    ('Attributes', ctypes.c_void_p), ('TargetAlias', wintypes.LPWSTR),
                    ('UserName', wintypes.LPWSTR)]
    api = ctypes.WinDLL('Advapi32.dll', use_last_error=True)
    ptr = ctypes.POINTER(Credential)()
    api.CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                            ctypes.POINTER(ctypes.POINTER(Credential))]
    api.CredReadW.restype = wintypes.BOOL
    api.CredFree.argtypes = [ctypes.c_void_p]
    if not api.CredReadW(nom, 1, 0, ctypes.byref(ptr)):
        if ctypes.get_last_error() == 1168:
            return None
        raise OSError('Lecture impossible')
    try:
        secret = ctypes.string_at(ptr.contents.CredentialBlob,
                                  ptr.contents.CredentialBlobSize).decode('utf-16-le').rstrip('\0')
        if not secret or any(c in secret for c in '\r\n'):
            raise ValueError('Identifiant invalide')
        return (ptr.contents.UserName or '', secret)
    finally:
        api.CredFree(ptr)


def configuration(racine):
    chemin = racine / 'CONNAISSANCES/contact.json'
    config = lire_json(chemin) if chemin.exists() else {}
    for canal in CANAUX:
        c = config.get(canal, {})
        if type(c.get('actif', False)) is not bool or c.get('niveau_min', 'info') not in NIVEAUX:
            raise ValueError('Configuration invalide')
    return config


def journal(racine, texte):
    chemin = racine / 'JOURNAUX/messages-proprietaire.md'
    avant = chemin.read_text(encoding='utf-8') if chemin.exists() else '# Messages au propriétaire\n'
    ecrire_sur(chemin, avant + texte + '\n')


def refuse(texte):
    return (any(re.search(m, texte, re.I) for m in _deleguer.MOTIFS_SECRETS)
            or re.search(r'\b(?:user[_ -]?id|player[_ -]?id|joueur|user|player|compte)\b\D{0,20}\d+', texte, re.I)
            or re.search(r'roblox\.com/(?:[a-z-]+/)?users/\d+', texte, re.I))


def url_valide(url, discord=False):
    u = urlsplit(url)
    if u.scheme != 'https' or not u.hostname or u.username or u.password or u.fragment:
        raise ValueError('URL refusée')
    if discord and (u.hostname not in ('discord.com', 'discordapp.com') or u.port not in (None, 443)
                    or not re.fullmatch(r'/api/(?:v\d+/)?webhooks/\d+/[\w-]+', u.path)):
        raise ValueError('Webhook refusé')


def transport(canal, config, niveau, sujet, texte, secret, url_test=None, smtp_test=None):
    if canal == 'windows':
        # XML sur stdin : aucun contenu de message en argument, fenêtre cachée.
        ps = '''$ErrorActionPreference='Stop'
[Windows.UI.Notifications.ToastNotificationManager,Windows.UI.Notifications,ContentType=WindowsRuntime] > $null
[Windows.Data.Xml.Dom.XmlDocument,Windows.Data.Xml.Dom.XmlDocument,ContentType=WindowsRuntime] > $null
$d=[Console]::In.ReadToEnd() | ConvertFrom-Json
$x=[Windows.Data.Xml.Dom.XmlDocument]::new()
$x.LoadXml('<toast><visual><binding template="ToastText02"><text id="1">'+[Security.SecurityElement]::Escape($d.sujet)+'</text><text id="2">'+[Security.SecurityElement]::Escape($d.texte)+'</text></binding></visual></toast>')
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Usine Roblox').Show([Windows.UI.Notifications.ToastNotification]::new($x))'''
        subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden', '-Command', ps],
                       input=json.dumps({'sujet': sujet, 'texte': texte}), text=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=9,
                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0), check=True)
        return
    if not secret:
        raise ValueError('Identifiant absent')
    utilisateur, valeur = secret
    if canal == 'courriel':
        message = EmailMessage()
        message['From'], message['To'], message['Subject'] = utilisateur, config['destinataire'], sujet
        message.set_content(texte, charset='utf-8')
        if smtp_test:
            smtp_test(message, utilisateur, valeur)
            return
        contexte = ssl.create_default_context()
        port = int(config.get('port', 587))
        classe = smtplib.SMTP_SSL if port == 465 else smtplib.SMTP
        options = {'context': contexte} if port == 465 else {}
        with classe(config['hote'], port, timeout=9, **options) as smtp:
            if port != 465:
                smtp.starttls(context=contexte)
            smtp.login(utilisateur, valeur)
            smtp.send_message(message)
        return
    if canal == 'discord':
        url = valeur
        url_valide(url, True)
        corps = json.dumps({'content': sujet + '\n' + texte, 'allowed_mentions': {'parse': []}}, ensure_ascii=False).encode('utf-8')
        entetes = {'Content-Type': 'application/json'}
    else:
        serveur = config.get('serveur', 'https://ntfy.sh').rstrip('/')
        url_valide(serveur)
        if not re.fullmatch(r'[A-Za-z0-9_-]{20,}', valeur):
            raise ValueError('Sujet ntfy trop court ou invalide')
        corps = json.dumps({'topic': valeur, 'title': sujet, 'message': texte,
                            'priority': {'info': 2, 'important': 4, 'urgent': 5}[niveau]}, ensure_ascii=False).encode('utf-8')
        url = serveur  # API JSON ntfy : sujet dans le corps, UTF-8 conservé.
        entetes = {'Content-Type': 'application/json'}
    if url_test:
        u = urlsplit(url_test)
        if u.scheme != 'http' or u.hostname not in ('127.0.0.1', 'localhost', '::1'):
            raise ValueError('Injection réservée au serveur local')
        url = url_test
    with build_opener(ProxyHandler({}), SansRedirection()).open(Request(url, corps, entetes), timeout=9) as r:
        if not 200 <= r.status < 300:
            raise OSError('Envoi refusé')


def travail(connexion, arguments):
    try:
        transport(*arguments)
        connexion.send(True)
    except Exception:
        connexion.send(False)
    finally:
        connexion.close()


@serialiser('contact')
def envoyer(niveau, sujet, texte, cle=None, jeu=None, canal=None, *, racine=RACINE,
            maintenant=None, _secrets=None, _urls=None, _smtp=None):
    racine = Path(racine)
    if (_urls is not None or _smtp is not None) and _secrets is None:
        raise ValueError('Injection sans lecteur de test interdite')
    champs = [sujet, texte, cle or '', jeu or '']
    if (niveau not in NIVEAUX or not 0 < len(sujet) <= 60 or not 0 < len(texte) <= 600
            or any(refuse(c) or any(ord(x) < 32 for x in c) for c in champs)
            or (jeu and not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', jeu))
            or (cle and len(cle) > 200) or canal not in (None, 'journal', *CANAUX)):
        print('REFUS : message ou métadonnées invalides, secret ou identifiant probable.')
        return 7
    if (racine / 'STOP').exists():
        print('STOP : aucun envoi ni écriture.')
        return 3
    config = configuration(racine)
    # Vérifier les valeurs brutes avant le journal, y compris en mode journal seul.
    secrets = {}
    for c, nom in NOMS.items():
        try:
            secrets[c] = (_secrets or lire_contact)('usine-roblox:contact:' + nom)
        except Exception:
            secrets[c] = None
    noms_opencloud = ['usine-roblox:opencloud:lecture', 'usine-roblox:opencloud:interrupteurs']
    if jeu:
        noms_opencloud.append('usine-roblox:opencloud:' + jeu + ':lecture')
    for nom in noms_opencloud:
        try:
            secrets[nom] = (_secrets or lire_contact)(nom)
        except Exception:
            secrets[nom] = None
    if any(s and s[1] in champ for s in secrets.values() for champ in champs):
        print('REFUS : contenu contenant un secret connu.')
        return 7
    date = (maintenant or datetime.now(timezone.utc)).astimezone(timezone.utc)
    cle = cle or 'message-' + hashlib.sha256(json.dumps([sujet, texte, jeu], ensure_ascii=False).encode()).hexdigest()
    chemin = racine / 'JOURNAUX/prevenir-etat.json'
    etat = lire_json(chemin) if chemin.exists() else {'cles': {}, 'jours': {}}
    externes = [c for c in CANAUX if config.get(c, {}).get('actif', False)
                and canal in (None, c) and NIVEAUX[niveau] >= NIVEAUX[config[c].get('niveau_min', 'info')]]
    raison = None
    if date.timestamp() < etat.get('echeances', {}).get(cle, etat['cles'].get(cle, 0) + DELAIS[niveau]):
        raison = 'anti-répétition'
    elif etat['jours'].get(date.date().isoformat(), 0) >= 20 and niveau != 'urgent':
        raison = 'plafond quotidien'
    journal(racine, f'\n{date.isoformat()} | {niveau} | {jeu or "usine"} | {sujet} | {texte} | {raison or "reçu"}')
    if raison or not externes:
        print('Journal seul : ' + (raison or 'aucun canal externe configuré pour ce niveau') + '.')
        return 3
    succes = False
    jour = date.date().isoformat()
    tentatives = etat['jours'].get(jour, 0)
    for c in externes:
        if tentatives >= 20 and niveau != 'urgent':
            journal(racine, c + ' : évité, plafond quotidien tous canaux confondus')
            continue
        tentatives += 1
        etat['jours'][jour] = tentatives
        # Réserver avant tout effet externe : une réponse perdue ou un arrêt ne
        # permet pas de rejouer le même envoi. Le délai couvre aussi les échecs.
        etat['cles'][cle] = date.timestamp()
        etat.setdefault('echeances', {})[cle] = date.timestamp() + DELAIS[niveau]
        ecrire_sur(chemin, json_texte(etat))
        try:
            secret = secrets.get(c)
            arguments = (c, config[c], niveau, sujet, texte, secret, (_urls or {}).get(c), _smtp)
            if _secrets is not None or _urls is not None or _smtp is not None:
                transport(*arguments)
                accepte = True
            else:
                parent, enfant = multiprocessing.Pipe(False)
                processus = multiprocessing.get_context('spawn').Process(target=travail, args=(enfant, arguments))
                processus.start()
                enfant.close()
                try:
                    accepte = parent.poll(10) and parent.recv()
                finally:
                    if processus.is_alive():
                        processus.terminate()
                    processus.join()
                    parent.close()
        except Exception:
            accepte = False
        succes |= accepte
        resultat = c + (' : accepté' if accepte else ' : échec (détails masqués)')
        print(resultat)
        journal(racine, resultat)
    # Chaque tentative externe compte, tous canaux confondus.
    etat['jours'][jour] = tentatives
    ecrire_sur(chemin, json_texte(etat))
    return 0 if succes else 4


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='commande', required=True)
    e = sub.add_parser('envoyer')
    e.add_argument('--niveau', choices=NIVEAUX, required=True)
    e.add_argument('--sujet', required=True)
    e.add_argument('--texte', required=True)
    e.add_argument('--cle')
    e.add_argument('--jeu')
    e.add_argument('--canal', choices=('journal', *CANAUX))
    sub.add_parser('canaux')
    sub.add_parser('essai')
    j = sub.add_parser('journal')
    j.add_argument('--n', type=int, default=20)
    a = p.parse_args(argv)
    try:
        if a.commande == 'envoyer':
            return envoyer(a.niveau, a.sujet, a.texte, a.cle, a.jeu, a.canal)
        if a.commande == 'journal':
            if a.n < 1:
                p.error('--n doit être positif')
            chemin = RACINE / 'JOURNAUX/messages-proprietaire.md'
            print('\n'.join(chemin.read_text(encoding='utf-8').splitlines()[-a.n:]) if chemin.exists() else 'Journal absent.')
            return 3
        config = configuration(RACINE)
        if a.commande == 'canaux':
            print('journal : toujours actif')
            for c in CANAUX:
                actif = config.get(c, {}).get('actif', False)
                etat = 'désactivé'
                if actif:
                    try:
                        etat = 'activé, identifiant ' + ('présent' if c == 'windows' or lire_contact('usine-roblox:contact:' + NOMS[c]) else 'absent')
                    except Exception:
                        etat = 'activé, identifiant illisible'
                print(c + ' : ' + etat + ' ; niveau_min=' + config.get(c, {}).get('niveau_min', 'info'))
            return 0
        codes = [envoyer('urgent', 'Essai usine Roblox', 'Message de vérification du canal privé.', canal=c)
                 for c in CANAUX if config.get(c, {}).get('actif', False)]
        if not codes:
            return envoyer('info', 'Essai usine Roblox', 'Aucun canal externe activé.')
        return 0 if 0 in codes else 4 if 4 in codes else 3
    except Exception:
        print('Erreur de configuration ou écriture impossible (détails masqués).')
        return 2


if __name__ == '__main__':
    multiprocessing.freeze_support()
    sys.exit(main())

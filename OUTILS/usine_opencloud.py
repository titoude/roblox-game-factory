"""Client Open Cloud v2 en lecture seule ; aucun secret affiché ou enregistré."""
import ctypes
from ctypes import wintypes
from email.utils import parsedate_to_datetime
import json
import os
from pathlib import Path
import re
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

BASE = 'https://apis.roblox.com'
PORTEES = ('universe-datastores.objects:list', 'universe-datastores.objects:read')

class Erreur(Exception):
    def __init__(self, message, code=2):
        super().__init__(message)
        self.code = code


def lire_json(chemin):
    return json.loads(Path(chemin).read_text(encoding='utf-8-sig'))


def ecrire_sur(chemin, texte):
    if not texte:
        raise Erreur('Écriture vide refusée', 6)
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    nom = None
    try:
        with tempfile.NamedTemporaryFile(dir=chemin.parent, delete=False) as fichier:
            nom = fichier.name
            contenu = texte.encode('utf-8')
            fichier.write(contenu)
            fichier.flush()
            os.fsync(fichier.fileno())
        if Path(nom).read_bytes() != contenu:
            raise Erreur('Relecture différente : écriture annulée', 6)
        os.replace(nom, chemin)
    finally:
        if nom and Path(nom).exists():
            Path(nom).unlink()


def json_texte(objet):
    return json.dumps(objet, ensure_ascii=False, indent=2) + '\n'


def lire_identifiant(nom):
    """Lit uniquement un nom générique autorisé, sans énumérer les identifiants."""
    if not re.fullmatch(r'usine-roblox:opencloud:(?:[a-z0-9-]+:)?lecture', nom):
        raise Erreur('Nom d’identifiant interdit')
    if os.name != 'nt':
        raise Erreur('Le Gestionnaire d’identifiants exige Windows')

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


def identifiant(slug, lecteur=None):
    lecteur = lecteur or lire_identifiant
    for nom in (f'usine-roblox:opencloud:{slug}:lecture', 'usine-roblox:opencloud:lecture'):
        secret = lecteur(nom)
        if secret is not None:
            return nom, secret
    return 'usine-roblox:opencloud:lecture', None


class SansRedirection(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Client:
    def __init__(self, univers, magasin, secret, base=BASE, maximum=100, pause=time.sleep):
        url = urlsplit(base)
        if base != BASE and not (url.scheme == 'http' and url.hostname in ('127.0.0.1', 'localhost', '::1')
                                 and not url.username and not url.password and not url.query and not url.fragment):
            raise Erreur('--base-url réservé à un serveur local HTTP')
        self.url = (base.rstrip('/') + '/cloud/v2/universes/' + quote(str(univers), safe='')
                    + '/data-stores/' + quote(magasin, safe='') + '/entries')
        self.secret, self.maximum, self.pause = secret, maximum, pause
        self.requetes = 0
        self.ouvrir = build_opener(SansRedirection()).open

    def get(self, portee, suffixe='', parametres=None):
        while True:
            if self.requetes >= self.maximum:
                raise Erreur('Plafond de requêtes atteint ; relancer pour reprendre.', 5)
            if self.requetes:
                self.pause(1)
            self.requetes += 1
            url = self.url + suffixe + ('?' + urlencode(parametres) if parametres else '')
            try:
                with self.ouvrir(Request(url, headers={'x-api-key': self.secret}), timeout=20) as reponse:
                    return json.load(reponse)
            except HTTPError as erreur:
                if erreur.code == 429:
                    attente = erreur.headers.get('Retry-After', '2')
                    try:
                        secondes = float(attente)
                    except ValueError:
                        secondes = parsedate_to_datetime(attente).timestamp() - time.time()
                    # Une longue attente rend la main sans retenter prématurément.
                    if secondes > 60:
                        raise Erreur('HTTP 429 : Retry-After > 60 s ; relancer plus tard.', 5)
                    self.pause(max(0, secondes))
                    continue
                if erreur.code in (401, 403):
                    message = erreur.read(16384).decode('utf-8', errors='replace')
                    message = message.replace(self.secret, '[secret masqué]')
                    message = ' '.join(message.split())[:1000]
                    raise Erreur(f'{portee} : manquante (HTTP {erreur.code} : {message})', 4)
                raise Erreur(f'API : HTTP {erreur.code}', 6)
            except (URLError, TimeoutError):
                raise Erreur('Réseau indisponible ou délai dépassé', 6)

    def lister(self, token='', taille=100, prefixe='r_'):
        return self.get(PORTEES[0], parametres={'maxPageSize': taille, 'pageToken': token,
                                              'filter': 'id.startsWith(' + json.dumps(prefixe) + ')' })

    def lire(self, cle):
        return self.get(PORTEES[1], '/' + quote(cle, safe=''))


    def entrees(self, prefixe):
        token = ''
        vus = set()
        while True:
            page = self.lister(token, prefixe=prefixe)
            for entree in page.get('dataStoreEntries', []):
                cle = entree['id']
                if cle.startswith(prefixe):
                    yield dict(self.lire(cle), id=cle)
            token = page.get('nextPageToken', '')
            if not token:
                break
            if token in vus:
                raise Erreur('Pagination répétée', 6)
            vus.add(token)

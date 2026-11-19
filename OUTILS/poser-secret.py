#!/usr/bin/env python3
"""poser-secret.py : range un secret dans le Gestionnaire d'identification Windows sans jamais l'afficher.

  python OUTILS\\poser-secret.py <nom> --depuis-fichier F [--motif REGEX] [--garder]
  python OUTILS\\poser-secret.py <nom> --presse-papiers [--motif REGEX]
  python OUTILS\\poser-secret.py <nom> --verifier            (dit seulement présent/absent et la longueur)
  python OUTILS\\poser-secret.py <nom> --variable NOM_VAR      (copie aussi le secret dans une variable
                                                               d'environnement de l'utilisateur Windows)

--motif extrait le secret d'un texte plus long (les séquences de terminal et les blancs sont retirés
avant la recherche). Le fichier source est effacé sauf --garder. Rien n'est écrit dans git ni dans
les journaux : seuls le nom, la longueur et le résultat sont affichés.
Noms en usage : usine-roblox:opencloud:lecture, usine-roblox:opencloud:interrupteurs,
usine-roblox:claude:oauth (jeton longue durée de `claude setup-token`).
Codes : 0 ok | 1 secret introuvable | 2 usage | 3 hors Windows.
"""
import argparse
import ctypes
import os
import re
import sys

NOMS_PERMIS = re.compile(r"^usine-roblox:[a-z0-9:_-]{3,60}$")


def _api():
    if os.name != "nt":
        print("HORS WINDOWS : Gestionnaire d'identification indisponible.")
        sys.exit(3)
    from ctypes import wintypes

    class CREDENTIAL(ctypes.Structure):
        _fields_ = [("Flags", wintypes.DWORD), ("Type", wintypes.DWORD), ("TargetName", wintypes.LPWSTR),
                    ("Comment", wintypes.LPWSTR), ("LastWritten", wintypes.FILETIME),
                    ("CredentialBlobSize", wintypes.DWORD), ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
                    ("Persist", wintypes.DWORD), ("AttributeCount", wintypes.DWORD), ("Attributes", ctypes.c_void_p),
                    ("TargetAlias", wintypes.LPWSTR), ("UserName", wintypes.LPWSTR)]
    api = ctypes.WinDLL("advapi32", use_last_error=True)
    api.CredWriteW.argtypes = [ctypes.POINTER(CREDENTIAL), wintypes.DWORD]
    api.CredWriteW.restype = wintypes.BOOL
    api.CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(CREDENTIAL))]
    api.CredReadW.restype = wintypes.BOOL
    api.CredFree.argtypes = [ctypes.c_void_p]
    return api, CREDENTIAL


def ecrire(nom, secret):
    api, CREDENTIAL = _api()
    donnees = secret.encode("utf-16-le")
    tampon = (ctypes.c_ubyte * len(donnees)).from_buffer_copy(donnees)
    c = CREDENTIAL()
    c.Type = 1  # CRED_TYPE_GENERIC
    c.TargetName = nom
    c.CredentialBlobSize = len(donnees)
    c.CredentialBlob = ctypes.cast(tampon, ctypes.POINTER(ctypes.c_ubyte))
    c.Persist = 2  # CRED_PERSIST_LOCAL_MACHINE
    c.UserName = "usine"
    if not api.CredWriteW(ctypes.byref(c), 0):
        raise OSError(ctypes.get_last_error(), "CredWriteW")


def lire(nom):
    api, CREDENTIAL = _api()
    p = ctypes.POINTER(CREDENTIAL)()
    if not api.CredReadW(nom, 1, 0, ctypes.byref(p)):
        return None
    try:
        n = p.contents.CredentialBlobSize
        return bytes(p.contents.CredentialBlob[:n]).decode("utf-16-le")
    finally:
        api.CredFree(p)


def variable_utilisateur(nom_var, valeur):
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as k:
        winreg.SetValueEx(k, nom_var, 0, winreg.REG_SZ, valeur)
    try:  # prévenir les fenêtres ouvertes (les nouveaux processus verront la variable)
        ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x1A, 0, "Environment", 2, 5000, None)
    except Exception:
        pass


def nettoyer(texte):
    texte = re.sub(r"\x1b\][^\x07]*\x07", "", texte)
    texte = re.sub(r"\x1b\[[0-9;?<>]*[A-Za-z]", "", texte)
    return re.sub(r"\s+", "", texte)


def presse_papiers():
    import subprocess
    r = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"], capture_output=True, text=True)
    return r.stdout


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("nom")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--depuis-fichier")
    src.add_argument("--presse-papiers", action="store_true")
    src.add_argument("--verifier", action="store_true")
    p.add_argument("--motif")
    p.add_argument("--garder", action="store_true")
    p.add_argument("--variable")
    a = p.parse_args(argv)
    if not NOMS_PERMIS.match(a.nom):
        print("NOM refusé : attendu usine-roblox:<famille>:<usage>.")
        return 2
    if a.verifier:
        s = lire(a.nom)
        print("%s : %s" % (a.nom, "présent (%d caractères)" % len(s) if s else "absent"))
        return 0 if s else 1
    if a.depuis_fichier:
        with open(a.depuis_fichier, "rb") as f:
            octets = f.read()
        # Tee-Object et Out-File de PowerShell 5.1 écrivent en UTF-16 avec BOM.
        if octets[:2] in (b"\xff\xfe", b"\xfe\xff"):
            brut = octets.decode("utf-16", errors="replace")
        else:
            brut = octets.decode("utf-8-sig", errors="replace")
    elif a.presse_papiers:
        brut = presse_papiers()
    else:
        s = lire(a.nom)
        if s and a.variable:
            variable_utilisateur(a.variable, s)
            print("variable %s posée depuis %s." % (a.variable, a.nom))
            return 0
        print("USAGE : --depuis-fichier, --presse-papiers, --verifier ou --variable.")
        return 2
    if a.motif:
        m = re.findall(a.motif, nettoyer(brut))
        secret = m[-1] if m else None
        if isinstance(secret, tuple):
            secret = secret[0]
    else:
        secret = brut.strip()
    if not secret:
        print("SECRET introuvable dans la source.")
        return 1
    ecrire(a.nom, secret)
    relu = lire(a.nom)
    if relu != secret:
        print("ÉCHEC : relecture différente.")
        return 1
    if a.variable:
        variable_utilisateur(a.variable, secret)
    if a.depuis_fichier and not a.garder:
        os.remove(a.depuis_fichier)
    print("%s posé (%d caractères)%s%s." % (a.nom, len(secret), ", variable %s posée" % a.variable if a.variable else "",
                                              ", source effacée" if a.depuis_fichier and not a.garder else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

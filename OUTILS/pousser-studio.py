#!/usr/bin/env python3
"""pousser-studio.py : envoie tout le code d'un jeu dans le Studio ouvert, dans l'ordre, avec garde-fous.

  python OUTILS\\pousser-studio.py <slug> [--place-attendue ID|locale] [--simuler] [--avec-tests]

1. Contrôle d'identité : la place ouverte doit être celle attendue (`locale` = PlaceId 0).
   Pour une place distante, renseigner USINE_ARCHIPEL_PLACE_ID afin d'interdire la place d'Archipel.
2. Verrou : `studio` détenu par l'agent courant (USINE_AGENT), sinon refus (G1).
3. Ordre : ReplicatedStorage, puis modules serveur, puis scripts clients, puis scripts serveur
   (*.server.lua) en dernier, pour qu'aucun script ne démarre avant ses modules.
   ServerStorage.Tests.* seulement avec --avec-tests.
4. Chaque fichier passe par OUTILS\\pousser-script.ps1 (même Luau que l'envoi à la main), puis
   execute_luau en mode Edit ; arrêt au premier échec.
Codes : 0 ok | 1 échec d'envoi | 2 usage | 3 STOP | 4 place inattendue ou verrou absent.
"""
import argparse
import os
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)
import studio_mcp  # noqa: E402


def rang(nom):
    if nom.startswith("ReplicatedStorage."):
        return 0
    if nom.endswith(".server.lua"):
        return 4
    if nom.startswith("ServerScriptService.") or nom.startswith("ServerStorage."):
        return 1 if not nom.startswith("ServerStorage.Tests.") else 3
    if nom.endswith(".client.lua"):
        return 2
    return 1


def fichiers(src, avec_tests):
    noms = [n for n in os.listdir(src) if n.endswith(".lua")]
    if not avec_tests:
        noms = [n for n in noms if not n.startswith("ServerStorage.Tests.")]
    return sorted(noms, key=lambda n: (rang(n), n))


def verrou_tenu(agent):
    r = subprocess.run(["powershell", "-NoProfile", "-File", os.path.join(ICI, "verrou.ps1"), "liste"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    for ligne in r.stdout.splitlines():
        if ligne.startswith("studio |") and ("agent %s " % agent) in ligne and "EXPIRE" not in ligne:
            return True
    return False


def luau_de(fichier):
    with tempfile.TemporaryDirectory() as t:
        sortie = os.path.join(t, "envoi.luau")
        r = subprocess.run(["powershell", "-NoProfile", "-File", os.path.join(ICI, "pousser-script.ps1"), fichier, "-Sortie", sortie],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0 or not os.path.isfile(sortie):
            raise RuntimeError("pousser-script.ps1 : %s" % r.stdout.strip()[-300:])
        with open(sortie, encoding="utf-8-sig") as f:
            return f.read()


def arret_demande():
    if os.path.exists(os.path.join(RACINE, "STOP")):
        print("ARRET : fichier STOP présent (G0).")
        return True
    return False


def main(argv=None):
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("slug")
    p.add_argument("--place-attendue", default="locale")
    p.add_argument("--simuler", action="store_true")
    p.add_argument("--avec-tests", action="store_true")
    a = p.parse_args(argv)
    if arret_demande():
        return 3
    src = os.path.join(RACINE, "JEUX", a.slug, "05-production", "src")
    if not os.path.isdir(src):
        print("INTROUVABLE : %s" % src)
        return 2
    liste = fichiers(src, a.avec_tests)
    if a.simuler:
        for n in liste:
            print("ENVOI prévu : %s" % n)
        return 0
    if a.place_attendue == "locale":
        attendu = 0
    elif a.place_attendue.isascii() and a.place_attendue.isdecimal():
        attendu = int(a.place_attendue)
    else:
        p.error("--place-attendue doit être « locale » ou un identifiant numérique")
    archipel = os.environ.get("USINE_ARCHIPEL_PLACE_ID", "")
    if attendu and not (archipel.isascii() and archipel.isdecimal() and int(archipel) > 0):
        print("REFUS : renseigner USINE_ARCHIPEL_PLACE_ID avant tout envoi vers une place distante.")
        return 4
    agent = os.environ.get("USINE_AGENT") or "defaut"
    if not verrou_tenu(agent):
        print("REFUS : verrou studio non détenu par %s (OUTILS\\verrou.ps1 prendre studio -agent %s)." % (agent, agent))
        return 4
    c = studio_mcp.Client()
    try:
        ident = c.luau('return tostring(game.PlaceId) .. "|" .. tostring(game.GameId) .. "|" .. game.Name')
        champs = ident.strip().split("|", 2)
        if len(champs) != 3 or not (champs[0].isascii() and champs[0].isdecimal()):
            print("REFUS : identité de la place ouverte illisible.")
            return 4
        place = int(champs[0])
        print("place ouverte : %s" % ident.strip())
        if attendu and place == int(archipel):
            print("REFUS : la place ouverte est Archipel (%d)." % place)
            return 4
        if place != attendu:
            print("REFUS : place %d ouverte, %s attendue." % (place, a.place_attendue))
            return 4
        for n in liste:
            if arret_demande():
                return 3
            try:
                code = luau_de(os.path.join(src, n))
                if arret_demande():
                    return 3
                r = c.luau(code)
            except Exception as e:
                print("ECHEC %s : %s" % (n, str(e)[:400]))
                return 1
            print("OK %s : %s" % (n, r.strip()[:160]))
    finally:
        c.fermer()
    print("ENVOI terminé : %d fichier(s)." % len(liste))
    return 0


if __name__ == "__main__":
    sys.exit(main())

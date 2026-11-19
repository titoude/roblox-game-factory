#!/usr/bin/env python3
"""jeton-claude.py : crée le jeton longue durée (un an) de la CLI claude et le range, sans l'afficher.

  python OUTILS\\jeton-claude.py            lance `claude setup-token` dans un pseudo-terminal large,
                                            capture le jeton, le range dans le Gestionnaire d'identification
                                            (usine-roblox:claude:oauth) et dans la variable utilisateur
                                            CLAUDE_CODE_OAUTH_TOKEN, puis vérifie un appel sans interface.
  python OUTILS\\jeton-claude.py --verifier  vérifie seulement que le jeton rangé fonctionne.

Le navigateur s'ouvre sur la page de connexion de Claude : si le compte y est déjà connecté, la
connexion se fait seule ; sinon choisir le compte du propriétaire (frontière G7 : connexion).
OUTILS\\deleguer.py lit ce jeton pour chaque agent Claude quand la variable manque.
Pourquoi un pseudo-terminal : à travers un tube, l'interface de la CLI coupe le jeton en lignes et
remplace les espaces par des déplacements de curseur ; la capture recollait alors du texte au jeton.
Codes : 0 ok | 1 échec | 3 hors Windows ou pywinpty absent.
"""
import importlib.util
import os
import re
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
NOM = "usine-roblox:claude:oauth"


def _secret():
    s = importlib.util.spec_from_file_location("poser_secret", os.path.join(ICI, "poser-secret.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def nettoyer(brut):
    t = re.sub(r"\x1b\][^\x07]*\x07", "", brut)
    t = re.sub(r"\x1b\[\d*C", " ", t)  # déplacement de curseur = espace
    t = re.sub(r"\x1b\[[0-9;?<>]*[A-Za-z]", " ", t)
    return t


def extraire(brut):
    """Le jeton dans la sortie de setup-token, ou None. Le texte collé après lui est exclu."""
    t = nettoyer(brut)
    candidats = re.findall(r"sk-ant-oat01-[A-Za-z0-9_-]+", t)
    if not candidats:
        return None
    c = candidats[-1]
    m = re.match(r"sk-ant-oat01-[A-Za-z0-9_-]*AA", c)  # le plus long préfixe finissant par AA
    return m.group(0) if m else None


def essayer(jeton):
    env = dict(os.environ, CLAUDE_CODE_OAUTH_TOKEN=jeton)
    r = subprocess.run(["claude", "-p", "Réponds exactement : JETON-OK", "--model", "claude-haiku-5-5"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
                       cwd=os.environ.get("TEMP", ICI), timeout=180, shell=(os.name == "nt"))
    return "JETON-OK" in r.stdout


def creer():
    try:
        from winpty import PtyProcess
    except ImportError:
        print("pywinpty absent : pip install pywinpty, ou lancer `claude setup-token` à la main puis "
              "`python OUTILS\\poser-secret.py %s --presse-papiers --motif \"sk-ant-oat01-[A-Za-z0-9_-]+\"`." % NOM)
        return 3
    p = PtyProcess.spawn("claude setup-token", dimensions=(60, 1000))
    brut, fin, jeton = "", time.time() + 300, None
    while time.time() < fin:
        try:
            brut += p.read(4096)
        except EOFError:
            break
        if "won't be able" in nettoyer(brut) or "ne pourrez plus" in nettoyer(brut):
            jeton = extraire(brut)
            break
        time.sleep(0.2)
    try:
        p.terminate(force=True)
    except Exception:
        pass
    if not jeton:
        print("ÉCHEC : aucun jeton capturé (connexion non faite dans les 5 minutes ?).")
        return 1
    if not essayer(jeton):
        print("ÉCHEC : jeton capturé (%d caractères) mais refusé par l'API ; rien n'est rangé." % len(jeton))
        return 1
    s = _secret()
    s.ecrire(NOM, jeton)
    s.variable_utilisateur("CLAUDE_CODE_OAUTH_TOKEN", jeton)
    print("JETON rangé (%d caractères) dans %s et CLAUDE_CODE_OAUTH_TOKEN ; appel d'essai réussi." % (len(jeton), NOM))
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if os.name != "nt":
        print("HORS WINDOWS.")
        return 3
    if "--verifier" in argv:
        j = _secret().lire(NOM)
        if not j:
            print("ABSENT : %s. Lancer python OUTILS\\jeton-claude.py." % NOM)
            return 1
        ok = essayer(j)
        print("JETON %s." % ("valide" if ok else "REFUSÉ (le refaire : python OUTILS\\jeton-claude.py)"))
        return 0 if ok else 1
    return creer()


if __name__ == "__main__":
    sys.exit(main())

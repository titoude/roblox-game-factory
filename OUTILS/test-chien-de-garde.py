"""Chien de garde de deleguer.py : agent figé (17/11/2026, appel figé plus de 4 h), agent bavard, durée maximale."""
import importlib.util
import os
import subprocess
import sys
import time

spec = importlib.util.spec_from_file_location("d", os.path.join(os.path.dirname(os.path.abspath(__file__)), "deleguer.py"))
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
n = 0


def verifier(c, nom):
    global n
    assert c, nom
    n += 1
    print("OK : " + nom)


def proc(code):
    return subprocess.Popen([sys.executable, "-c", code], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


t = time.time()
code, _ = d.attendre_agent(proc("import time; time.sleep(120)"), "x", "claude", time.time(), 10, 0.05, pas=1,
                           activite=lambda f, dd: None)
verifier(code == 9 and time.time() - t < 30, "agent figé (ni sortie ni transcription) : arrêté, code 9")
code, out = d.attendre_agent(proc("import time\nfor i in range(6):\n  print(i, flush=True); time.sleep(1)\nprint('RESULTAT: ok | x | y')"),
                             "x", "claude", time.time(), 10, 0.04, pas=1, activite=lambda f, dd: None)
verifier(code == 0 and b"RESULTAT: ok" in out, "agent qui écrit régulièrement : jamais coupé, sortie complète")
code, _ = d.attendre_agent(proc("import time; time.sleep(6); print('RESULTAT: ok | a | b')"), "x", "claude", time.time(), 10, 0.05,
                           pas=1, activite=lambda f, dd: time.time())
verifier(code == 0, "sortie muette mais transcription active : jamais coupé")
code, _ = d.attendre_agent(proc("import time\nwhile 1:\n  print(1, flush=True); time.sleep(0.5)"), "x", "claude", time.time(), 0.05, 10,
                           pas=1, activite=lambda f, dd: None)
verifier(code == 8, "durée maximale dépassée : code 8")
verifier(d.silence_max_min({"roles": {"r": {"silence_max_min": 7}}}, "r") == 7 and d.silence_max_min({"roles": {}}, "r") == 20,
         "seuil de silence lu par rôle, 20 min par défaut")
print("%d controles OK" % n)

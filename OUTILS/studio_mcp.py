#!/usr/bin/env python3
"""studio_mcp.py : client minimal du serveur MCP de Roblox Studio (stdio, JSON-RPC), pour les outils de l'usine.

  python OUTILS\\studio_mcp.py studios                      Studios ouverts (id, place, mode)
  python OUTILS\\studio_mcp.py appel <outil> '<json>'        appelle un outil MCP (studio_id ajouté si absent)
  python OUTILS\\studio_mcp.py luau <fichier.luau> [Edit|Server|Client]   execute_luau sur un fichier

Le Studio visé est celui de la variable USINE_STUDIO_ID, sinon le seul ouvert ; s'il y en a plusieurs,
l'outil refuse plutôt que de deviner (G1 : un seul écrivain par place, jamais Archipel par erreur).
Codes : 0 ok | 1 erreur d'outil | 2 usage | 4 Studio ambigu ou absent.
"""
import json
import os
import queue
import subprocess
import sys
import threading
import time

BAT = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Roblox", "mcp.bat")


class ErreurStudio(RuntimeError):
    pass


class Client:
    def __init__(self, delai_s=20):
        if not os.path.isfile(BAT):
            raise ErreurStudio("serveur MCP de Studio introuvable : %s" % BAT)
        self.p = subprocess.Popen(["cmd", "/c", BAT], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, bufsize=0)
        self.n = 0
        self.delai_s = delai_s
        self._lignes = queue.Queue()
        self._ferme = False
        self._studio = None
        threading.Thread(target=self._lire, daemon=True).start()
        try:
            self.req("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                    "clientInfo": {"name": "usine-roblox", "version": "1"}})
            self._envoyer({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
        except (ErreurStudio, OSError):
            self.fermer()
            raise

    def _lire(self):
        try:
            for ligne in iter(self.p.stdout.readline, b""):
                self._lignes.put(ligne)
        finally:
            self._lignes.put(b"")

    def _envoyer(self, obj):
        self.p.stdin.write((json.dumps(obj) + "\n").encode("utf-8"))
        self.p.stdin.flush()

    def req(self, methode, params=None, *, delai_s=None):
        if self._ferme:
            raise ErreurStudio("serveur MCP fermé")
        fin = time.monotonic() + (self.delai_s if delai_s is None else min(self.delai_s, delai_s))
        self.n += 1
        rid = self.n
        self._envoyer({"jsonrpc": "2.0", "id": rid, "method": methode, "params": params or {}})
        while True:
            try:
                restant = fin - time.monotonic()
                if restant <= 0:
                    raise queue.Empty
                ligne = self._lignes.get(timeout=restant)
            except queue.Empty:
                self.fermer()
                raise ErreurStudio("délai de réponse MCP dépassé : %s" % methode) from None
            if not ligne:
                self.fermer()
                raise ErreurStudio("serveur MCP fermé")
            try:
                msg = json.loads(ligne.decode("utf-8"))
            except ValueError:
                continue
            if msg.get("id") == rid:
                if "error" in msg:
                    raise ErreurStudio(json.dumps(msg["error"], ensure_ascii=False))
                return msg.get("result")

    def appel(self, outil, args=None, studio=True, *, delai_s=None):
        args = dict(args or {})
        if studio and "studio_id" not in args:
            args["studio_id"] = self.studio()
        r = self.req("tools/call", {"name": outil, "arguments": args}, delai_s=delai_s) or {}
        texte = "\n".join(c.get("text", json.dumps(c, ensure_ascii=False)) for c in r.get("content", []))
        if r.get("isError"):
            raise ErreurStudio(texte)
        return texte

    def studios(self, attente_s=20):
        fin = time.monotonic() + attente_s
        while True:
            try:
                st = json.loads(self.appel("list_roblox_studios", {}, studio=False,
                                           delai_s=fin - time.monotonic())).get("studios", [])
            except ValueError:
                st = []
            restant = fin - time.monotonic()
            if st or restant <= 0:
                return st
            time.sleep(min(2, restant))
            if time.monotonic() >= fin:
                return st

    def studio(self):
        if self._studio:
            return self._studio
        voulu = os.environ.get("USINE_STUDIO_ID")
        st = self.studios()
        if voulu:
            if not any(s.get("id") == voulu for s in st):
                raise ErreurStudio("Studio %s absent (ouverts : %s)" % (voulu, [s.get("name") for s in st]))
            self._studio = voulu
        elif len(st) == 1:
            self._studio = st[0].get("id")
        else:
            raise ErreurStudio("%d Studio(s) ouverts (%s) : fixer USINE_STUDIO_ID" % (len(st), [s.get("name") for s in st]))
        return self._studio

    def luau(self, code, contexte="Edit"):
        return self.appel("execute_luau", {"code": code, "datamodel_type": contexte})

    def fermer(self):
        if self._ferme:
            return
        self._ferme = True
        try:
            self.p.terminate()
        except Exception:
            pass


def main(argv=None):
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    a = sys.argv[1:] if argv is None else argv
    if not a:
        print(__doc__)
        return 2
    c = None
    try:
        c = Client()
        if a[0] == "studios":
            for s in c.studios():
                print("%s | %s | %s | cloud=%s" % (s.get("id"), s.get("name"), s.get("mode"), s.get("persistedToCloud")))
            return 0
        if a[0] == "appel" and len(a) >= 2:
            print(c.appel(a[1], json.loads(a[2]) if len(a) > 2 else {}))
            return 0
        if a[0] == "luau" and len(a) >= 2:
            with open(a[1], encoding="utf-8") as f:
                print(c.luau(f.read(), a[2] if len(a) > 2 else "Edit"))
            return 0
        print(__doc__)
        return 2
    except ErreurStudio as e:
        print("ERREUR : %s" % e)
        return 4 if "Studio" in str(e) else 1
    finally:
        if c is not None:
            c.fermer()


if __name__ == "__main__":
    sys.exit(main())

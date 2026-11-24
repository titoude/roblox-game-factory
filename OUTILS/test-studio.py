#!/usr/bin/env python3
"""Contrôles Studio sans ouvrir ni modifier de place."""
import importlib.util
import io
import json
import os
import queue
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import Event
from types import SimpleNamespace
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("pousser_studio", Path(__file__).with_name("pousser-studio.py"))
pousser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pousser)


class EnvoiStudio(unittest.TestCase):
    def test_g1_exige_le_verrou_de_la_place(self):
        with tempfile.TemporaryDirectory() as dossier, patch.object(pousser, "RACINE", dossier), \
                patch.dict(os.environ, {"USINE_AGENT": "producteur"}), \
                patch.object(pousser.studio_mcp, "Client") as studio, \
                patch.object(pousser, "luau_de", return_value="return true"), redirect_stdout(io.StringIO()):
            racine = Path(dossier)
            src = racine / "JEUX/lave-la-tour/05-production/src"
            src.mkdir(parents=True)
            (src / "ReplicatedStorage.Test.lua").write_text("return true\n", encoding="utf-8")
            verrous = racine / "VERROUS"
            verrous.mkdir()
            maintenant = datetime.now(timezone.utc)

            def ecrire_verrou(nom, ressource, agent, expire):
                (verrous / nom).write_text(json.dumps({
                    "ressource": ressource, "agent": agent, "expire": expire.isoformat(),
                }), encoding="utf-8-sig")

            futur = maintenant + timedelta(minutes=5)
            ecrire_verrou("studio.lock", "studio", "producteur", futur)
            self.assertEqual(pousser.main(["lave-la-tour"]), 4)
            ecrire_verrou("place_0.lock", "place:0", "autre", futur)
            self.assertEqual(pousser.main(["lave-la-tour"]), 4)
            ecrire_verrou("place_0.lock", "place:0", "producteur", maintenant - timedelta(minutes=5))
            self.assertEqual(pousser.main(["lave-la-tour"]), 4)
            studio.assert_not_called()

            (verrous / "studio.lock").unlink()
            ecrire_verrou("place_0.lock", "place:0", "producteur", futur)
            client = studio.return_value
            client.luau.side_effect = ["0|0|Place locale", "script envoyé"]
            self.assertEqual(pousser.main(["lave-la-tour"]), 0)
            self.assertEqual(client.luau.call_count, 2)
            client.fermer.assert_called_once()

    def test_verrou_lit_les_sept_decimales_de_powershell(self):
        with tempfile.TemporaryDirectory() as dossier, patch.object(pousser, "RACINE", dossier):
            verrous = Path(dossier) / "VERROUS"
            verrous.mkdir()
            verrou = verrous / "place_42.lock"
            maintenant = datetime.now(timezone.utc)
            for minutes, attendu in [(5, True), (-5, False)]:
                with self.subTest(minutes=minutes), redirect_stdout(io.StringIO()):
                    date = maintenant + timedelta(minutes=minutes)
                    verrou.write_text(json.dumps({
                        "ressource": "place:42", "agent": "producteur",
                        "expire": date.strftime("%Y-%m-%dT%H:%M:%S.%f7Z"),
                    }), encoding="utf-8-sig")
                    self.assertEqual(pousser.verrou_tenu("producteur", 42), attendu)

    def test_stop_refuse_meme_si_le_verrou_est_detenu(self):
        with tempfile.TemporaryDirectory() as dossier, patch.object(pousser, "RACINE", dossier), \
                patch.object(pousser, "verrou_tenu", return_value=True) as verrou, \
                patch.object(pousser.studio_mcp, "Client") as studio, redirect_stdout(io.StringIO()):
            (Path(dossier) / "STOP").touch()
            self.assertEqual(pousser.main(["lave-la-tour"]), 3)
        verrou.assert_not_called()
        studio.assert_not_called()

    def test_stop_pendant_preparation_interdit_ecriture(self):
        with tempfile.TemporaryDirectory() as dossier, patch.object(pousser, "RACINE", dossier), \
                patch.object(pousser, "verrou_tenu", return_value=True), \
                patch.object(pousser.studio_mcp, "Client") as studio, redirect_stdout(io.StringIO()):
            src = Path(dossier) / "JEUX/lave-la-tour/05-production/src"
            src.mkdir(parents=True)
            (src / "ReplicatedStorage.Test.lua").write_text("return true\n", encoding="utf-8")
            client = studio.return_value
            client.luau.return_value = "0|0|Place locale"

            def preparer(_):
                (Path(dossier) / "STOP").touch()
                return "return true"

            with patch.object(pousser, "luau_de", side_effect=preparer):
                self.assertEqual(pousser.main(["lave-la-tour"]), 3)
            self.assertEqual(client.luau.call_count, 1)
            client.fermer.assert_called_once()

    def test_simulation_n_ouvre_pas_studio(self):
        sortie = io.StringIO()
        with patch.object(pousser.studio_mcp, "Client") as studio, redirect_stdout(sortie):
            self.assertEqual(pousser.main(["lave-la-tour", "--simuler"]), 0)
        studio.assert_not_called()
        self.assertIn("ENVOI prévu : ServerScriptService.Jeu.Amorce.server.lua", sortie.getvalue())

    def test_place_distante_exige_identifiant_archipel(self):
        with patch.dict(os.environ, {"USINE_ARCHIPEL_PLACE_ID": ""}), \
                patch.object(pousser.studio_mcp, "Client") as studio, redirect_stdout(io.StringIO()):
            self.assertEqual(pousser.main(["lave-la-tour", "--place-attendue", "101"]), 4)
        studio.assert_not_called()

    def test_refus_places_interdites_et_inattendues(self):
        for attendu, ouvert in (("101", 101), ("102", 103), ("locale", 101), ("locale", "")):
            with self.subTest(attendu=attendu, ouvert=ouvert), \
                    patch.dict(os.environ, {"USINE_ARCHIPEL_PLACE_ID": "101"}), \
                    patch.object(pousser, "verrou_tenu", return_value=True), \
                    patch.object(pousser.studio_mcp, "Client") as studio, redirect_stdout(io.StringIO()):
                client = studio.return_value
                client.luau.return_value = f"{ouvert}|0|Place de test"
                self.assertEqual(pousser.main(["lave-la-tour", "--place-attendue", attendu]), 4)
                self.assertEqual(client.luau.call_count, 1)
                client.fermer.assert_called_once()


class TransportMCP:
    def __init__(self, *messages):
        self.lignes = queue.Queue()
        for ligne in messages:
            self.lignes.put(ligne)
        self.stdin = io.BytesIO()
        self.stdout = SimpleNamespace(readline=self.lignes.get)
        self.arrets = 0
        self.ferme = Event()

    def terminate(self):
        self.arrets += 1
        self.ferme.set()
        self.lignes.put(b"")


class ClientMCP(unittest.TestCase):
    def client(self, transport, delai_s):
        mcp = pousser.studio_mcp
        with patch.object(mcp, "BAT", __file__), patch.object(mcp.subprocess, "Popen", return_value=transport):
            return mcp.Client(delai_s=delai_s)

    def test_initialisation_bornee_sans_reponse(self):
        transport = TransportMCP()
        with self.assertRaisesRegex(pousser.studio_mcp.ErreurStudio, "délai.*initialize"):
            self.client(transport, 0.05)
        self.assertEqual(transport.arrets, 1)

    def test_ecriture_bornee_meme_si_mcp_ne_lit_pas(self):
        transport = TransportMCP(b'{"id":1,"result":{}}\n')
        client = self.client(transport, 5)

        def ecriture_bloquee(_):
            transport.ferme.wait(3)
            raise BrokenPipeError()

        transport.stdin = SimpleNamespace(write=ecriture_bloquee)
        debut = time.monotonic()
        try:
            with self.assertRaisesRegex(pousser.studio_mcp.ErreurStudio, "délai.*écriture.*tools/call"):
                client.req("tools/call", delai_s=0.05)
            self.assertLess(time.monotonic() - debut, 2)
        finally:
            client.fermer()
        self.assertEqual(transport.arrets, 1)

    def test_liste_studios_respecte_son_delai(self):
        transport = TransportMCP(b'{"id":1,"result":{}}\n')
        client = self.client(transport, 5)
        debut = time.monotonic()
        try:
            with self.assertRaisesRegex(pousser.studio_mcp.ErreurStudio, "délai.*tools/call"):
                client.studios(attente_s=0.05)
            self.assertLess(time.monotonic() - debut, 2)
        finally:
            client.fermer()
        self.assertEqual(transport.arrets, 1)

    def test_reponse_recue_apres_une_notification(self):
        transport = TransportMCP(b'{"id":1,"result":{}}\n', b'{"method":"notifications/progress"}\n',
                                 b'{"id":2,"result":{"ok":true}}\n')
        client = self.client(transport, 1)
        try:
            self.assertEqual(client.req("tools/list"), {"ok": True})
        finally:
            client.fermer()


if __name__ == "__main__":
    unittest.main()

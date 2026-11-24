#!/usr/bin/env python3
"""Contrôles Studio sans ouvrir ni modifier de place."""
import importlib.util
import io
import os
import queue
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("pousser_studio", Path(__file__).with_name("pousser-studio.py"))
pousser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pousser)


class EnvoiStudio(unittest.TestCase):
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

    def terminate(self):
        self.arrets += 1
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

"""Contrôles locaux de historique.py : transcriptions fabriquées, aucun accès réseau."""
from contextlib import redirect_stdout
import io
import json
import os
import sys
import tempfile

import historique as h


def main():
    controles = 0

    def verifier(condition, nom):
        nonlocal controles
        assert condition, nom
        controles += 1
        print('OK : ' + nom)

    jeton = 'sk-' + 'ant-' + 'A1b2C3d4E5f6G7h8I9j0KLMNOP'
    with tempfile.TemporaryDirectory() as rep:
        dossier = os.path.join(rep, 'projet usine')
        os.makedirs(dossier)
        h.CLAUDE_PROJETS = os.path.join(rep, 'claude')
        h.CODEX_SESSIONS = os.path.join(rep, 'codex')
        rc = os.path.join(h.CLAUDE_PROJETS, h.encoder_dossier(dossier))
        os.makedirs(rc)
        claude = os.path.join(rc, 'aaaa1111-2222-3333-4444-555566667777.jsonl')
        lignes = [
            {'type': 'user', 'timestamp': '2026-11-17T10:00:00Z', 'message': {'role': 'user', 'content': 'Fais un jeu de lavage de vitres, pas de dépense.'}},
            {'type': 'assistant', 'timestamp': '2026-11-17T10:00:05Z', 'message': {'role': 'assistant', 'content': [
                {'type': 'text', 'text': 'Je lance la veille.'},
                {'type': 'tool_use', 'name': 'Bash', 'input': {'command': 'git status'}}]}},
            {'type': 'user', 'timestamp': '2026-11-17T10:00:06Z', 'message': {'role': 'user', 'content': [
                {'type': 'tool_result', 'content': 'erreur introuvable XYZ-42'}]}},
            {'type': 'user', 'timestamp': '2026-11-17T10:01:00Z', 'message': {'role': 'user', 'content': '<task-notification>fini</task-notification>'}},
            {'type': 'user', 'timestamp': '2026-11-17T10:01:30Z', 'message': {'role': 'user', 'content': 'Delegated task node:x (veille) [completed]: ok'}},
            {'type': 'user', 'timestamp': '2026-11-17T10:02:00Z', 'message': {'role': 'user', 'content': '<system-reminder>bruit</system-reminder>Voici ma clé ' + jeton + ' ne la recopie pas'}},
            {'type': 'system', 'subtype': 'compact_boundary', 'timestamp': '2026-11-17T11:00:00Z'},
            {'type': 'user', 'timestamp': '2026-11-17T11:00:00Z', 'isCompactSummary': True, 'message': {'role': 'user', 'content': 'Résumé : un jeu est en cours.'}},
            {'type': 'user', 'timestamp': '2026-11-17T11:00:01Z', 'isMeta': True, 'message': {'role': 'user', 'content': '<local-command-caveat>x</local-command-caveat>'}},
            {'type': 'user', 'timestamp': '2026-11-17T11:05:00Z', 'message': {'role': 'user', 'content': 'Publie seulement après la QA à deux clients.'}},
        ]
        with io.open(claude, 'w', encoding='utf-8') as f:
            f.write('pas du json\n')
            for d in lignes:
                f.write(json.dumps(d, ensure_ascii=False) + '\n')
        rx = os.path.join(h.CODEX_SESSIONS, '2026', '11', '17')
        os.makedirs(rx)
        codex = os.path.join(rx, 'rollout-2026-11-17T10-00-00-01a1ea22-8bd2-7723-99c2-48e96159408e.jsonl')
        with io.open(codex, 'w', encoding='utf-8') as f:
            for d in [
                {'type': 'session_meta', 'payload': {'cwd': dossier}},
                {'type': 'response_item', 'timestamp': '2026-11-17T12:00:00Z', 'payload': {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'Relis le banc Luau.'}]}},
                {'type': 'response_item', 'timestamp': '2026-11-17T12:00:02Z', 'payload': {'type': 'function_call', 'name': 'shell', 'arguments': '{"cmd":"python banc"}'}},
                {'type': 'compacted', 'timestamp': '2026-11-17T12:30:00Z', 'payload': {}},
            ]:
                f.write(json.dumps(d) + '\n')
        autre = os.path.join(h.CODEX_SESSIONS, '2026', '11', '17', 'rollout-autre.jsonl')
        with io.open(autre, 'w', encoding='utf-8') as f:
            f.write(json.dumps({'type': 'session_meta', 'payload': {'cwd': os.path.join(rep, 'ailleurs')}}) + '\n')
        os.utime(claude, (2000000000, 2000000000))

        ev = list(h.evenements(claude))
        demandes = [e['texte'] for e in ev if e['demande']]
        verifier(len(demandes) == 3, 'trois demandes réelles du propriétaire (ni résultats, ni notifications, ni résumé, ni méta)')
        verifier(demandes[0].startswith('Fais un jeu') and demandes[2].startswith('Publie seulement'), 'texte exact conservé, ordre gardé')
        verifier('bruit' not in demandes[1], 'rappels système retirés des demandes')
        verifier(sum(1 for e in ev if e['compaction']) == 1, 'frontière de compaction repérée')
        verifier(any(e['role'] == 'résumé' for e in ev), 'résumé de compaction étiqueté, pas pris pour une demande')
        verifier(jeton not in h.couper(demandes[1], 500) and '[MASQUÉ]' in h.couper(demandes[1], 500), 'secret masqué à l\'affichage')
        chemin_long = 'C:/Users/x/' + '/'.join(['dossier%d' % i for i in range(20)])
        verifier(h.masquer(chemin_long) == chemin_long, 'un long chemin n\'est pas pris pour un secret')

        s = h.lister_sessions(dossier)
        verifier([x[1] for x in s] == ['claude', 'codex'], 'sessions Claude et Codex du dossier, la plus récente d\'abord ; autre dossier exclu')
        verifier(h.trouver_session(None, dossier) == claude, 'sans --session : la plus récente')
        verifier(h.trouver_session('01a1ea22-8bd2', dossier) == codex, 'identifiant partiel Codex retrouvé')
        evx = list(h.evenements(codex))
        verifier([e['texte'] for e in evx if e['demande']] == ['Relis le banc Luau.'], 'demande Codex lue')
        verifier(any(e['compaction'] for e in evx), 'compaction Codex repérée')

        sortie = io.StringIO()
        with redirect_stdout(sortie):
            code = h.main(['--dossier', dossier, 'chercher', 'XYZ-4[0-9]', '--session', 'aaaa1111'])
        verifier(code == 0 and 'XYZ-42' in sortie.getvalue(), 'recherche dans les résultats d\'outils')
        with redirect_stdout(io.StringIO()):
            verifier(h.main(['--dossier', dossier, 'chercher', 'introuvable-zzz']) == 1, 'recherche vide : code 1')
            verifier(h.main(['--dossier', dossier, 'chercher', '(']) == 2, 'motif invalide : code 2')

        ancien = sys.stdin
        sys.stdin = io.StringIO(json.dumps({'session_id': 'aaaa1111-2222-3333-4444-555566667777', 'transcript_path': claude, 'source': 'compact'}))
        sortie = io.StringIO()
        try:
            with redirect_stdout(sortie):
                h.main(['crochet-compaction'])
        finally:
            sys.stdin = ancien
        r = json.loads(sortie.getvalue())
        ctx = r['hookSpecificOutput']['additionalContext']
        verifier(r['hookSpecificOutput']['hookEventName'] == 'SessionStart', 'crochet : format SessionStart')
        verifier('Publie seulement après la QA' in ctx and 'historique.py chercher' in ctx, 'crochet : demandes exactes et mode d\'emploi injectés')
        verifier(jeton not in ctx, 'crochet : aucun secret injecté')
        sys.stdin = io.StringIO('pas du json')
        sortie = io.StringIO()
        try:
            with redirect_stdout(sortie):
                code = h.main(['--dossier', os.path.join(rep, 'vide'), 'crochet-compaction'])
        finally:
            sys.stdin = ancien
        verifier(code == 0 and sortie.getvalue() == '', 'crochet : entrée illisible et aucune session = silence, jamais d\'erreur')

    print('%d controles OK' % controles)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""historique.py : un agent relit son propre historique de session (Claude Code ou Codex).

Une compaction résume la conversation et perd des détails : demandes exactes du propriétaire,
chemins, messages d'erreur, décisions. Les transcriptions complètes restent sur disque ; cet outil
les relit sans modèle.

  python OUTILS\\historique.py sessions   [--dossier D] [--n 10]
  python OUTILS\\historique.py demandes   [--session ID|CHEMIN] [--n 30] [--long 600]
  python OUTILS\\historique.py chercher MOTIF [--session ID|CHEMIN] [--n 40] [--contexte 240]
  python OUTILS\\historique.py lire       [--session ID|CHEMIN] [--depuis N] [--nombre 40] [--long 1500]
  python OUTILS\\historique.py compactions [--session ID|CHEMIN]
  python OUTILS\\historique.py crochet-compaction   (crochet SessionStart de Claude Code : JSON sur stdin)

Sans --session : la session la plus récente du dossier courant (celle qui tourne).
--session accepte un identifiant (préfixe suffisant) ou le chemin d'un .jsonl.
Les secrets probables (motifs G9) sont masqués à l'affichage.
Codes : 0 ok | 1 rien trouvé | 2 usage.
"""
import argparse
import glob
import io
import json
import os
import re
import sys

ACCUEIL = os.path.expanduser("~")
CLAUDE_PROJETS = os.path.join(ACCUEIL, ".claude", "projects")
CODEX_SESSIONS = os.path.join(ACCUEIL, ".codex", "sessions")

# Mêmes familles que deleguer.py (G9), plus les jetons longs ; assemblés par morceaux.
MOTIFS_SECRETS = [
    r"_\|WARN" + r"ING:-DO-NOT-SHARE[^\s\"']*",
    r"discord(app)?\.com/api/(v\d+/)?webhooks/\d{6,}/[A-Za-z0-9_-]{20,}",
    r"(?i)x-api-key\s*[:=]\s*[\"']?[A-Za-z0-9+/=_-]{24,}",
    r"ROBLOSECURITY\s*[:=]\s*[\"']?[A-Za-z0-9_|:-]{24,}",
    r"sk-(ant|proj)-[A-Za-z0-9_-]{16,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----",
    r"(?i)\b(bearer|token|secret|password|mot de passe)\s*[:=]\s*[\"']?[A-Za-z0-9+/=_.-]{20,}",
    # Jeton long : 80 caractères et plus, sans « / » (les chemins restent lisibles), avec chiffres et majuscules.
    r"\b(?=[A-Za-z0-9+_-]*\d)(?=[A-Za-z0-9+_-]*[A-Z])[A-Za-z0-9+_-]{80,}={0,2}",
]
RE_SECRETS = [re.compile(m) for m in MOTIFS_SECRETS]
RE_RAPPEL = re.compile(r"<system-reminder>[\s\S]*?</system-reminder>")
RE_BALISES_CMD = re.compile(r"<(local-command-caveat|local-command-stdout|command-name|command-message|command-args)>[\s\S]*?</\1>")


def masquer(texte):
    for r in RE_SECRETS:
        texte = r.sub("[MASQUÉ]", texte)
    return texte


def encoder_dossier(chemin):
    """Nom du dossier de projet de Claude Code : tout caractère non alphanumérique devient « - »."""
    return re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(chemin))


def _meme_dossier(a, b):
    try:
        return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))
    except Exception:
        return False


def _cwd_codex(chemin):
    try:
        with io.open(chemin, encoding="utf-8", errors="replace") as f:
            for _ in range(5):
                ligne = f.readline()
                if not ligne:
                    break
                d = json.loads(ligne)
                if d.get("type") == "session_meta":
                    return (d.get("payload") or {}).get("cwd")
    except Exception:
        return None
    return None


def lister_sessions(dossier, jours_codex=14):
    """[(mtime, fournisseur, id, chemin)] du plus récent au plus ancien."""
    res = []
    rep = os.path.join(CLAUDE_PROJETS, encoder_dossier(dossier))
    for p in glob.glob(os.path.join(rep, "*.jsonl")):
        res.append((os.path.getmtime(p), "claude", os.path.splitext(os.path.basename(p))[0], p))
    if os.path.isdir(CODEX_SESSIONS):
        tous = sorted(glob.glob(os.path.join(CODEX_SESSIONS, "*", "*", "*", "*.jsonl")), key=os.path.getmtime, reverse=True)
        for p in tous[:400]:
            cwd = _cwd_codex(p)
            if cwd and _meme_dossier(cwd, dossier):
                m = re.search(r"([0-9a-f]{8}-[0-9a-f-]{27,})\.jsonl$", p)
                res.append((os.path.getmtime(p), "codex", m.group(1) if m else os.path.basename(p), p))
    res.sort(reverse=True)
    return res


def trouver_session(session, dossier):
    if session and os.path.isfile(session):
        return session
    if session:
        candidats = [p for p in glob.glob(os.path.join(CLAUDE_PROJETS, "*", session + "*.jsonl"))]
        if os.path.isdir(CODEX_SESSIONS):
            candidats += glob.glob(os.path.join(CODEX_SESSIONS, "*", "*", "*", "*" + session + "*.jsonl"))
        candidats.sort(key=os.path.getmtime, reverse=True)
        return candidats[0] if candidats else None
    s = lister_sessions(dossier)
    return s[0][3] if s else None


def _texte_contenu(contenu):
    """Texte lisible d'un champ content (chaîne ou liste de blocs). Rend (texte, est_resultat_outil)."""
    if isinstance(contenu, str):
        return contenu, False
    morceaux, resultat = [], False
    for b in contenu or []:
        if not isinstance(b, dict):
            continue
        t = b.get("type")
        if t in ("text", "input_text", "output_text"):
            morceaux.append(b.get("text", ""))
        elif t == "tool_use":
            morceaux.append("[outil %s] %s" % (b.get("name"), json.dumps(b.get("input"), ensure_ascii=False)))
        elif t == "tool_result":
            resultat = True
            c = b.get("content")
            morceaux.append("[résultat] " + (_texte_contenu(c)[0] if c is not None else ""))
    return "\n".join(m for m in morceaux if m), resultat


def evenements(chemin):
    """Entrées lisibles : dict(n, quand, role, texte, demande, compaction)."""
    n = 0
    with io.open(chemin, encoding="utf-8", errors="replace") as f:
        for ligne in f:
            try:
                d = json.loads(ligne)
            except ValueError:
                continue
            quand = d.get("timestamp", "")
            t = d.get("type")
            if t == "system" and d.get("subtype") == "compact_boundary":
                n += 1
                yield dict(n=n, quand=quand, role="compaction", texte="--- compaction ---", demande=False, compaction=True)
                continue
            if t in ("user", "assistant") and isinstance(d.get("message"), dict):
                texte, resultat = _texte_contenu(d["message"].get("content"))
                resume = bool(d.get("isCompactSummary"))
                propre = RE_BALISES_CMD.sub("", RE_RAPPEL.sub("", texte)).strip()
                notification = propre.startswith(("Delegated task ", "<task-notification>", "[Request interrupted"))
                demande = (t == "user" and not resultat and not d.get("isMeta") and not resume and bool(propre)
                           and not notification)
                if not texte.strip():
                    continue
                n += 1
                role = "résumé" if resume else ("outil" if resultat else ("notification" if t == "user" and notification else ("propriétaire" if t == "user" else "agent")))
                yield dict(n=n, quand=quand, role=role, texte=propre if demande else texte, demande=demande, compaction=False)
                continue
            if t == "response_item":  # Codex
                p = d.get("payload") or {}
                if p.get("type") == "message":
                    texte, _ = _texte_contenu(p.get("content"))
                    propre = RE_RAPPEL.sub("", texte).strip()
                    if not propre:
                        continue
                    role = p.get("role")
                    n += 1
                    demande = role == "user" and not propre.startswith("<") and "AGENTS.md instructions" not in propre[:200]
                    yield dict(n=n, quand=quand, role="propriétaire" if demande else ("agent" if role == "assistant" else role or "?"),
                               texte=propre, demande=demande, compaction=False)
                elif p.get("type") in ("function_call", "custom_tool_call", "local_shell_call"):
                    n += 1
                    yield dict(n=n, quand=quand, role="outil", texte="[outil %s] %s" % (p.get("name"), p.get("arguments") or p.get("input") or p.get("action")),
                               demande=False, compaction=False)
                elif p.get("type") in ("function_call_output", "custom_tool_call_output"):
                    n += 1
                    sortie = p.get("output")
                    yield dict(n=n, quand=quand, role="outil", texte="[résultat] " + (sortie if isinstance(sortie, str) else json.dumps(sortie, ensure_ascii=False)),
                               demande=False, compaction=False)
            elif t == "compacted":  # Codex
                n += 1
                yield dict(n=n, quand=quand, role="compaction", texte="--- compaction ---", demande=False, compaction=True)


def couper(texte, long):
    texte = masquer(texte).replace("\r", "")
    return texte if len(texte) <= long else texte[:long] + " […+%d car.]" % (len(texte) - long)


def ligne(e, long):
    return "#%d %s [%s] %s" % (e["n"], e["quand"][:19].replace("T", " "), e["role"], couper(e["texte"], long))


def cmd_sessions(a):
    s = lister_sessions(a.dossier)[: a.n]
    if not s:
        print("AUCUNE session pour %s" % a.dossier)
        return 1
    import datetime as dt
    for mt, fournisseur, ident, chemin in s:
        premiere = next((e for e in evenements(chemin) if e["demande"]), None)
        print("%s | %-6s | %s | %d ko | %s" % (dt.datetime.fromtimestamp(mt).strftime("%Y-%m-%d %H:%M"), fournisseur, ident,
                                               os.path.getsize(chemin) // 1024, couper(premiere["texte"], 100).replace("\n", " ") if premiere else "-"))
    return 0


def _session(a):
    chemin = trouver_session(a.session, a.dossier)
    if not chemin:
        print("AUCUNE session trouvée (%s)." % (a.session or a.dossier))
        sys.exit(1)
    print("session : %s" % chemin)
    return chemin


def cmd_demandes(a):
    d = [e for e in evenements(_session(a)) if e["demande"]]
    if not d:
        print("AUCUNE demande.")
        return 1
    for e in d[-a.n:]:
        print(ligne(e, a.long))
    return 0


def cmd_chercher(a):
    try:
        r = re.compile(a.motif, re.IGNORECASE)
    except re.error as ex:
        print("MOTIF invalide : %s" % ex)
        return 2
    trouves = 0
    for e in evenements(_session(a)):
        m = r.search(e["texte"])
        if not m:
            continue
        debut = max(0, m.start() - a.contexte)
        extrait = ("…" if debut else "") + e["texte"][debut: m.end() + a.contexte]
        print("#%d %s [%s] %s" % (e["n"], e["quand"][:19].replace("T", " "), e["role"], couper(extrait, 2 * a.contexte + 200).replace("\n", " ⏎ ")))
        trouves += 1
        if trouves >= a.n:
            print("… (limite --n atteinte)")
            break
    return 0 if trouves else 1


def cmd_lire(a):
    for e in evenements(_session(a)):
        if e["n"] < a.depuis:
            continue
        if e["n"] >= a.depuis + a.nombre:
            break
        print(ligne(e, a.long))
    return 0


def cmd_compactions(a):
    chemin = _session(a)
    tous = list(evenements(chemin))
    c = [e for e in tous if e["compaction"]]
    print("%d compaction(s), %d entrées." % (len(c), len(tous)))
    for e in c:
        avant = [x for x in tous if x["demande"] and x["n"] < e["n"]]
        print("#%d %s ; demandes avant : %d (dernière : %s)" % (e["n"], e["quand"][:19], len(avant),
                                                              couper(avant[-1]["texte"], 160).replace("\n", " ") if avant else "-"))
    return 0


def rappel(chemin, n=12, long=500):
    """Texte injecté après une compaction : demandes exactes du propriétaire et mode d'emploi."""
    tous = list(evenements(chemin))
    d = [e for e in tous if e["demande"]]
    lignes = [
        "Contexte compacté : le résumé ci-dessus a pu perdre des détails. La transcription complète reste lisible.",
        "Session : %s" % chemin,
        "Avant de reprendre, vérifie au besoin avec :",
        "  python OUTILS\\historique.py demandes --session \"%s\"" % chemin,
        "  python OUTILS\\historique.py chercher \"<mot>\" --session \"%s\"" % chemin,
        "  python OUTILS\\historique.py lire --depuis <n> --session \"%s\"" % chemin,
        "Demandes du propriétaire, les plus récentes (texte exact, %d sur %d) :" % (min(n, len(d)), len(d)),
    ]
    for e in d[-n:]:
        lignes.append("- " + ligne(e, long).replace("\n", " "))
    return "\n".join(lignes)


def cmd_crochet(a):
    try:
        entree = json.load(sys.stdin)
    except Exception:
        entree = {}
    chemin = entree.get("transcript_path") or trouver_session(entree.get("session_id"), entree.get("cwd") or a.dossier)
    if not chemin or not os.path.isfile(chemin):
        return 0
    sortie = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": rappel(chemin)}}
    sys.stdout.write(json.dumps(sortie, ensure_ascii=False))
    return 0


def main(argv=None):
    for flux in (sys.stdout, sys.stderr):
        try:
            flux.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dossier", default=os.getcwd())
    sp = p.add_subparsers(dest="cmd")
    s = sp.add_parser("sessions"); s.add_argument("--n", type=int, default=10)
    for nom in ("demandes", "chercher", "lire", "compactions"):
        q = sp.add_parser(nom)
        q.add_argument("--session")
        if nom == "chercher":
            q.add_argument("motif")
            q.add_argument("--n", type=int, default=40)
            q.add_argument("--contexte", type=int, default=240)
        if nom == "demandes":
            q.add_argument("--n", type=int, default=30)
            q.add_argument("--long", type=int, default=600)
        if nom == "lire":
            q.add_argument("--depuis", type=int, default=1)
            q.add_argument("--nombre", type=int, default=40)
            q.add_argument("--long", type=int, default=1500)
    sp.add_parser("crochet-compaction")
    a = p.parse_args(argv)
    if not a.cmd:
        p.print_help()
        return 2
    return {"sessions": cmd_sessions, "demandes": cmd_demandes, "chercher": cmd_chercher, "lire": cmd_lire,
            "compactions": cmd_compactions, "crochet-compaction": cmd_crochet}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())

# Roblox Game Factory

A software factory where a chain of AI agents (Claude Code + Codex) takes a Roblox game from market scan to release, through numbered gates with hard thresholds, and rewrites its own rules after every game.

> Docs and code comments are in French (the author is French). A full French README is in [`README.fr.md`](README.fr.md).

```
Market scan → Concept → Economy → Fun → Production → QA → Release → Distribution → Post-mortem → rules updated
                     live game: player feedback → patch batch → QA → release
```

## Honest status (19 Nov 2026)

- **0 games published.** Game #2, *Lave la tour* (wash a skyscraper from a gondola), had its first real Play session in Roblox Studio on 17 Nov 2026: world built, HUD, 60 fps, three wipes → pane confirmed by the server → coins credited.
- The fun gate scored it **5.7 / 6.1 / 6.4** across three independent reviews, below the bar. The factory logged that instead of faking a pass and moved the real question to the playable prototype.

## How it runs

```powershell
python usine.py "fais un jeu"      # "make a game": resume the current game, or scan the market and start a new one
python usine.py etat               # games, locks, open alerts (no model call)
python usine.py verifier           # self-check: structure, secrets, test suites, Luau syntax + tests
python usine.py roles              # which model plays which role, fallbacks, free slots
python usine.py tableau            # local dashboard at http://127.0.0.1:8765/ (--lecture-seule: no controls)
```

- `usine.py` starts the orchestrator through the `claude` CLI. The orchestrator delegates each role through `OUTILS/deleguer.py`, which picks the provider (`codex` or `claude`), model and effort from `CONNAISSANCES/routage.json`, enforces the agent cap and fallbacks, and logs every delegation.
- **A reviewer is never the model that wrote the work.** Never more than 2 large Claude agents at once.

## What's actually in here

| Piece | Where | What it does |
|---|---|---|
| Hard guardrails | `GARDE-FOUS.md` | Rules G0–G17 that override any prompt: no spending, no publishing, no credentials, stop on CAPTCHA/terms/payment |
| Gates and thresholds | `CONNAISSANCES/SEUILS-PORTES.md`, `seuils.json` | P0–P11 with numbers, e.g. live beta must hit D1 ≥ 8 % and sessions ≥ 8 min |
| Procedures | `PROCEDURES/00–14` | One per stage, plus orchestration, owner bootstrap, player feedback, promotion |
| Watchdog | `OUTILS/deleguer.py`, `test-chien-de-garde.py` | Reads agent output in a thread and watches the session transcript on disk; 20 min of silence → kills the process tree, exit code 9, falls back to the next model. Added after a real 4-hour freeze on 17 Nov |
| Luau test bench | `OUTILS/banc-luau.py`, `OUTILS/luau/` | Runs the game's server logic outside Studio against a fake Roblox runtime (`faux-roblox.luau`), one process per suite, deterministic; static analysis + compile on every script |
| Studio push | `OUTILS/pousser-studio.py` | Pushes the game's scripts into Studio over MCP, under a lock, with a check that it is writing into the right place |
| Player feedback loop | `OUTILS/retours-joueurs.py`, `PROCEDURES/11` | Collects in-game feedback through Open Cloud (read-only key), clusters it, judges it, turns it into patch batches |
| Self-improvement | `CONNAISSANCES/BILANS/`, `PROPOSITIONS/` | Every game ends with a post-mortem; agents propose rule changes, the orchestrator merges them |
| Dashboard | `OUTILS/tableau-de-bord.py` | Local web interface over the real files: games with stages and gates P0–P11, ETAT.json history, orchestrator cycles and heartbeat decisions, live agents (G2 count), delegations, routing, logs, alerts, locks, STOP. A Pilotage screen sets/removes STOP and runs verifier, heartbeat, cycle and player-feedback loop by calling `usine.py` (so STOP, G2 and locks apply); a cycle needs an explicit owner consent box, reserves its slot in `battement-etat.json` like `battement --lancer`, and logs to `JOURNAUX/tableau/`. POSTs need a per-launch token and a local Origin. Binds to 127.0.0.1, refuses foreign Host headers, masks secret patterns, stdlib only |
| Games | `JEUX/<slug>/` | One folder per game: state, journal, concept, economy model, reviews, source, tests |

## What the first Play session broke

The bench was green; Studio was not.

1. The test place was never published, so `GetDataStore` threw *"You must publish this place to the web to access DataStore"*, the bootstrap died on line 7, no RemoteEvents were created, and every client waited forever. Fix: a safe store wrapper (in-memory in Studio only, real error in production) and a new test suite.
2. `PlayerModule` was missing from PlayerScripts, so the gondola client hung on `WaitForChild`. Fix: 5 s timeout, then a `ContextActionService` fallback.

Lesson written back into the rules: a green bench doesn't mean the place is publishable.

## Not included

Agent logs, locks, secrets, binaries (`OUTILS/bin/` holds the Luau toolchain: `luau`, `luau-analyze`, `luau-compile`) and private player data are excluded. Secrets live in the Windows Credential Manager, never in files.

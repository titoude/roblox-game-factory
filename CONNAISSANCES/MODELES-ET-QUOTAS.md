# Modèles, efforts et simultanéité

> **Depuis le 16/11/2026, la source unique du choix de modèle est `CONNAISSANCES\routage.json`** (lue par `OUTILS\deleguer.py`, procédure 13). `python OUTILS\deleguer.py --liste` imprime le tableau à jour. Consignes du propriétaire (`PLAFONDS.md` § 4) : veille, calcul, revue adversariale, code, tests et analyses par Codex `gpt-6.1-sol` ; aucun petit modèle (Haiku) en premier choix ; 2 agents Claude Opus, Fable ou Sonnet au plus, **orchestrateur compris**. Le tableau « Qui fait quoi » ci-dessous est celui du cycle 1, gardé pour l'historique : là où il nomme Haiku, lire `gpt-6.1-sol`.

Identifiants relevés dans T3 Code le 15/11/2026 (`orchestrator_capabilities`). À revérifier une fois par fil d'orchestration, avant la première délégation.

| Fournisseur (`providerInstanceId`) | Modèle (`model`) | Option d'effort |
|---|---|---|
| `claudeAgent` | `claude-opus-5-5`, `claude-fable-5-2`, `claude-haiku-5-5`, `claude-sonnet-5-5` | `effort` : low, medium, high, xhigh, max |
| `codex` | `gpt-6.1-sol` | `reasoningEffort` : low, medium, high, xhigh, max, ultra |

## Qui fait quoi

| Étape | Rôle | Modèle | Effort | Nombre | Écrit dans la place ? |
|---|---|---|---|---|---|
| 00 | Orchestrateur | `claude-opus-5-5` | medium | 1 (session principale) | Non, sauf s'il produit lui-même |
| 01 | Veilleur navigateur | `claude-haiku-5-5` | high | 1 à 4 | Non |
| 01 | Lecteur de page sans navigateur | agent natif `web-fetch`, `model: "haiku"` | — | 1 à la fois, appelé par l'orchestrateur | Non |
| 02 | Concepteur | `claude-fable-5-2` (repli autorisé : `claude-opus-5-5` medium) | high | 1 | Non |
| 03 | Vérificateur économie « calcul » | `gpt-6.1-sol` | xhigh | 1 | Non |
| 03 | Vérificateur économie « adversaire » | `gpt-6.1-sol` | xhigh | 1 | Non |
| 04 | Relecteur fun | `claude-opus-5-5` | high | 1 | Non |
| 05 | Producteur Studio | `claude-opus-5-5` | high | 1, jamais 2 | **Oui, seul** |
| 05 | Relecteur de code (par lot sensible) | `gpt-6.1-sol` | high | 0 à 1 | Non (lit un commit) |
| 06 | Testeur en jeu | `claude-haiku-5-5` | high | 2 à 4 | Non (Play uniquement) |
| 06 | Analyste console et contre-vérification | `gpt-6.1-sol` | high | 1 à 2 | Non |
| 06 | Qualification indépendante | `claude-fable-5-2` | high | 1 | Non |
| 07 | Revue du diff avant PROD | `gpt-6.1-sol` | xhigh | 1 | Non |
| 07, 08, 09 | Release, distribution, bilan | Orchestrateur | medium | — | Réglages et publication, sous verrou |

Haiku peut monter à `xhigh` quand la tâche le demande (lecture fine d'une page chargée, scénario de test long).

## Simultanéité

- **Opus, Fable, Sonnet : 2 sous-agents au plus en même temps** (garde-fou G2). La chaîne n'en demande qu'un à la fois ; le seul cas à deux est « producteur + qualification » ou « concepteur + relecteur fun ». Trois ou plus : accord écrit du propriétaire.
- **Haiku et Codex** : pas de plafond imposé. Valeurs d'usage : 4 Haiku, 3 Codex, parce qu'il n'y a qu'un bureau, un Chrome et un Studio.
- **Écriture dans une place** : un seul agent, verrou `place:<placeId>`.
- **Bureau** (souris, clavier) : un seul agent, verrou `bureau`.

## Lancer un sous-agent

Depuis T3 Code, outil `delegate_task` (un enfant ne reçoit que `task` : le prompt doit se suffire) :

```json
{
  "title": "Veille : Roblox Charts",
  "role": "research",
  "mode": "async",
  "target": { "providerInstanceId": "claudeAgent", "model": "claude-haiku-5-5", "options": { "effort": "high" } },
  "task": "<prompt type de PROCEDURES\\01-VEILLE-NAVIGATEUR.md, complété>"
}
```

```json
{
  "title": "Économie : calcul",
  "role": "review",
  "mode": "async",
  "target": { "providerInstanceId": "codex", "model": "gpt-6.1-sol", "options": { "reasoningEffort": "xhigh" } },
  "task": "<prompt type de PROCEDURES\\03-REVUE-ECONOMIE.md, complété>"
}
```

- Sous-agent Claude sans réglage particulier et au premier plan : l'outil natif `Agent` suffit. Avec un effort imposé, en arrière-plan ou pour Codex : `delegate_task`.
- On ne sonde pas une délégation en cours : on suit ce que l'outil indique, et on annule (`task_cancel`) une délégation devenue inutile.
- Depuis Claude Code seul (sans T3 Code), Codex n'est pas joignable : voir « Replis ».

## Constats du cycle 1 (15/11/2026)

- `delegate_task` fonctionne depuis une session Fable 5.2, y compris quand cette session est elle-même une tâche déléguée : trois Haiku et deux `gpt-6.1-sol` lancés en `mode: "async"`, la fin de chacun réveille l'orchestrateur.
- `orchestrator_capabilities` : `claudeAgent` et `codex` actifs, les autres fournisseurs désactivés. `reasoningEffort` de Codex accepte aussi `ultra` ; `effort` de Claude accepte aussi `ultrathink`. Autres modèles Codex listés : `gpt-6-astra`, `gpt-6.1-terra`, `gpt-6-luna` (non utilisés).
- **Un Haiku délégué n'a pas `WebFetch`**, seulement `WebSearch` (chargé par `ToolSearch`). Il ne lit donc aucune page. La lecture passe par l'agent natif `web-fetch` avec `model: "haiku"`, appelé par l'orchestrateur, au premier plan, une page par appel (10 à 70 s l'appel).
- Un Haiku délégué a bien le shell et le système de fichiers : il a lu les procédures et écrit son relevé au bon endroit. Durée d'un veilleur : 3 à 4 minutes.
- Le serveur MCP de Studio, le navigateur intégré et Chrome n'ont pas été essayés depuis un sous-agent (interdits ce cycle).

## Replis

| Situation | Repli | Autorisé par |
|---|---|---|
| Sous-agents Opus, Fable et Sonnet interdits ou déjà au plafond (G2) | L'orchestrateur joue lui-même le concepteur s'il tourne sur Fable 5.2 ou Opus 5.5. Il ne joue le relecteur fun que faute de mieux : la porte P3 s'écrit alors en **dérogation** (règle A8) et se rejoue avec Opus 5.5 avant le lot L0 | Cycle 1, consigne du propriétaire |
| Fable 5.2 indisponible ou quota épuisé pour le concept | `claude-opus-5-5`, effort medium | Le propriétaire (consigne initiale) |
| Codex indisponible (session Claude Code seule, quota) | Étape 03 en **mode dégradé** : `OUTILS\sim-economie.py` lancé par l'orchestrateur + relecture adversaire par Haiku xhigh. La porte P2 n'est validée qu'« à confirmer » ; elle se rejoue avec Codex avant la release. | Règle A6 |
| Opus indisponible pour la production | Pause de l'étape et alerte. Pas de remplacement. | Règle A6 |
| Haiku indisponible | Pause de la veille ou de la QA ; l'orchestrateur peut lire lui-même 10 pages au plus. | Règle A6 |

Tout mode dégradé s'écrit dans l'`ETAT.json` du jeu (`mode_degrade`) et apparaît au bilan.

## Coût et contexte

- Un sous-agent rend 15 lignes au plus et le chemin de son fichier : l'orchestrateur lit le fichier seulement s'il en a besoin.
- On ne relance pas un agent pour un petit correctif de rapport : l'orchestrateur corrige.
- Chaque délégation est notée dans le `JOURNAL.md` du jeu (modèle, effort, durée, résultat) : c'est la base du coût par jeu au bilan.

## Constats du cycle 2 (16/11/2026)

- `orchestrator_capabilities` : `codex` (gpt-6.1-sol, gpt-6-astra, gpt-6.1-terra, gpt-6-luna) et `claudeAgent` (Opus 5.5, Sonnet 5.5, Fable 5.2, Haiku 5.5) actifs ; les autres fournisseurs désactivés.
- 13 délégations par `delegate_task` dans le cycle : 11 `gpt-6.1-sol` (2 veilles et relectures en `high`, 2 contre-vérifications en `xhigh`, 6 développements d'outils et de jeu en `high`), 2 Opus 5.5 `high` (revues du fun), 1 Haiku (veille, annulée sur consigne du propriétaire). Durées : 8 à 35 minutes.
- **Un `gpt-6.1-sol` délégué lit des pages web** (15 pages lues pour la veille promo, avec arrêt propre devant une vérification antirobot), ce qu'un Haiku délégué ne faisait pas au cycle 1 : la veille passe par lui.
- Les CLI `codex exec` et `claude -p` répondent depuis `OUTILS\deleguer.py` (8 à 12 s pour un aller-retour) ; `codex exec` rend le code 0 même quand il refuse un modèle : l'outil se fie à l'absence de dernier message.
- Jusqu'à 4 `gpt-6.1-sol` ont tourné en même temps sur des fichiers distincts, sans collision, à condition de nommer dans chaque prompt les fichiers des autres agents à ne pas toucher.
- Non essayé : le serveur MCP de Studio depuis un enfant (Studio verrouillé tout le cycle).


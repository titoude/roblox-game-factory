# 13 — Orchestration multi-fournisseurs (Claude Code et Codex)

**Qui** : l'orchestrateur. **But** : lancer chaque rôle sur le bon modèle, au bon effort, sur les abonnements du propriétaire (Claude Code et Codex), avec un repli écrit quand un fournisseur manque, que l'usine tourne dans T3 Code ou sans lui.

Source unique du choix : `CONNAISSANCES\routage.json`. Aucun modèle ne s'écrit en dur dans un prompt ou une procédure : on nomme un **rôle**.

## 1. Deux façons de faire tourner l'usine

| | Dans T3 Code | Sans T3 Code (logiciel autonome) |
|---|---|---|
| Lancer | Ouvrir le dossier, écrire « fais un jeu » | `python usine.py "fais un jeu"` (ou `usine "fais un jeu"`) |
| Orchestrateur | Le fil ouvert (Opus 5.5 ou Fable 5.2) | `claude -p` lancé par `usine.py`, un tour à la fois, état sur disque |
| Déléguer | Outil `delegate_task`, charge utile donnée par `python OUTILS\deleguer.py --role <rôle> --format t3 --prompt-fichier <f>` | `python OUTILS\deleguer.py --role <rôle> --prompt-fichier <f> --jeu <slug>` (lance `codex exec` ou `claude -p`, attend, journalise) |
| Fin d'un enfant | La fin de l'enfant réveille le fil | La commande rend la main avec la ligne `RESULTAT:` |
| Plafond G2 | Compté par l'orchestrateur avant chaque lancement | Appliqué par l'outil (`JOURNAUX\agents\`, code de sortie 4) |
| Coût | `JEUX\<slug>\JOURNAL.md` | `JOURNAUX\delegations.csv` (rôle, modèle, effort, durée, résultat), à reporter au journal du jeu |

Les deux modes lisent le même routage, les mêmes procédures et le même état : un cycle commencé dans l'un se reprend dans l'autre.

## 2. Qui fait quoi (premier choix, puis replis dans l'ordre)

`python OUTILS\deleguer.py --liste` imprime le tableau à jour.

**Depuis le 24/11/2026 (consigne du propriétaire)** : SWE 2.1 (fournisseur `devin`) est l'agent principal de chaque rôle de production et de l'orchestration, Codex `gpt-6.1-sol` en premier repli ; les rôles de vérification (`"verification": true` : économie, contre-vérification, revue du fun, relecture de code, qualification, revue du diff) passent par Astra 6.2 (`gpt-6.2-astra`) ou Opus 5.5, **sur accord du propriétaire** (§ 4 bis), avec Codex `gpt-6.1-sol` en repli marqué `degrade`. Le tableau ci-dessous est celui du 16/11/2026 (`PLAFONDS.md` § 4), gardé pour les replis :

| Famille de tâches | Modèle | Pourquoi |
|---|---|---|
| Calcul, revue adversariale, code, veille, tests, analyse de console, jugement des retours | Codex `gpt-6.1-sol` (effort `high`, `xhigh` pour les revues) | Rigueur, volume, hors plafond G2 : c'est le cheval de trait |
| Conception, qualification, rédaction du kit, scénarios vidéo | Claude Fable 5.2, effort `high` | Jugement de produit ; un seul à la fois |
| Orchestration, revue du fun, écriture dans Studio | Claude Opus 5.5 (`medium` pour orchestrer, `high` sinon) | Conduite longue, serveur MCP de Studio |
| Tri mécanique sans enjeu, repli de dernier rang | Claude Haiku 5.5 (`xhigh`) | Jamais en premier choix ; un relevé ou un test fait par Haiku est « à confirmer » |

- **Indépendance (A2)** : un relecteur n'est jamais le modèle auteur. `--auteur <fournisseur:modele>` l'écarte ; concept (Fable) et revue du fun (Opus) sont deux modèles différents, code (Codex) et qualification (Fable) aussi.
- **Effort** : `low` pour un contrôle de chaîne, `high` par défaut, `xhigh` quand une erreur coûte une production (économie, diff de release). Au-delà (`max`, `ultra`) : seulement sur décision écrite au bilan.
- **Simultanéité** : 2 agents Claude Opus, Fable ou Sonnet au plus, **orchestrateur compris** (donc un seul enfant Claude fort à la fois) ; Codex : valeur d'usage 3 à 4 en parallèle ; un seul écrivain par place, un seul agent au bureau.

## 3. Lancer un enfant

1. Écrire le prompt (prompt type de la procédure de l'étape, complété) dans `JOURNAUX\prompts\<jeu>-<étape>-<rôle>.md`. Prompt autonome (A1) : racine, rôle, fichiers à lire, entrées avec leur commit, sortie exacte, interdits, dernière ligne `RESULTAT: <ok|echec|arret> | <fichier> | <phrase>`. Aucun secret (l'outil refuse un prompt qui y ressemble, code 7).
2. T3 Code : `python OUTILS\deleguer.py --role <rôle> --format t3 --prompt-fichier <f> --titre "<titre>"`, puis passer le JSON imprimé à `delegate_task` tel quel. Sans T3 Code : la même commande sans `--format t3`.
3. Noter la délégation dans `JEUX\<slug>\JOURNAL.md` (modèle, effort, durée, résultat).
4. Ne rien modifier de ce que l'enfant lit pendant qu'il tourne (E10).

Codes de sortie de `deleguer.py` : 0 `RESULTAT: ok` ; 1 échec, arrêt ou pas de ligne `RESULTAT` ; 3 simulation ou format T3 ; 4 plafond G2 (attendre) ; 5 aucun candidat (pause et alerte, règle A6) ; 6 `STOP` ; 7 prompt refusé ; 8 durée dépassée (processus arrêté) ; 9 agent figé ; 10 aucun candidat sans accord du propriétaire (demande envoyée, étape en pause).

## 4. Replis

| Situation | Ce que fait l'outil | Ce que fait l'orchestrateur |
|---|---|---|
| CLI absente (`codex` ou `claude` introuvable) | Écarte le candidat, prend le suivant, imprime `REPLI:` | Écrit le mode dégradé dans `ETAT.json` si la ligne le dit |
| La CLI échoue au lancement (modèle refusé, quota épuisé, connexion expirée) : code non nul ou aucun message de l'agent | Imprime `ECHEC-CLI:`, relance le candidat suivant | Idem ; si c'est une connexion expirée : alerte « connexion » (G7), seul le propriétaire se reconnecte |
| Plafond G2 atteint | Code 4, rien n'est lancé | Attend la fin d'un agent Claude fort, ou prend un rôle Codex |
| Plus aucun candidat | Code 5 | Étape en pause, alerte, travail qui n'en dépend pas |
| L'enfant répond sans ligne `RESULTAT` | Code 1, pas de relance sur un autre modèle | Corrige le prompt : ce n'est pas une panne de fournisseur |
| Dans T3 Code, un fournisseur est désactivé | — | `orchestrator_capabilities`, puis `--indisponible <fournisseur>` pour obtenir la charge utile du repli |

## 4 bis. Quota du propriétaire : modèles sur accord (Q1)

Opus 5.5 et Astra 6.2 consomment les abonnements du propriétaire : `routage.json` les liste dans `sur_accord`. L'outil ne les lance (ni ne donne leur charge utile T3) que sur un accord écrit **par le propriétaire** :

- `python OUTILS\deleguer.py --accorder <modèle> --nombre N --heures H` : N lancements permis pendant H heures (`JOURNAUX\accords-quota.json`) ; chaque lancement en consomme un. Refusé si la commande vient d'un agent de l'usine (`USINE_ROLE` posé, code 7).
- Sans accord en cours : le candidat est écarté (`ECARTE: … quota du propriétaire`), le rôle passe au suivant (Codex), et une demande part par `OUTILS\prevenir.py` (une par modèle tant qu'elle est ouverte, `JOURNAUX\demandes-quota.json`). `--simuler` n'envoie rien.
- `python OUTILS\deleguer.py --accords` : accords en cours et demandes ouvertes. Un agent ne s'accorde jamais de quota lui-même.

Un repli marqué `degrade` dans le routage ne valide pas une porte : elle s'écrit `a_confirmer` et se rejoue avec le modèle prévu avant l'étape qui engage de la production (A8) ou avant la release (A6).

## 5. Ce qui est prouvé, ce qui ne l'est pas

Prouvé en exécution réelle le 16/11/2026 (`python OUTILS\test-deleguer.py --reel`, 24 contrôles) : aller-retour `codex exec` (gpt-6.1-sol) et `claude -p` ; repli à l'exécution quand Codex refuse le modèle (Codex rend alors le code 0 : l'outil se fie à l'absence de dernier message) ; refus d'un prompt contenant un secret probable ; charge utile T3 conforme à ce que `delegate_task` a accepté pendant le cycle 2 (enfants gpt-6.1-sol `high` et `xhigh`, Opus 5.5 `high`).

Non prouvé : l'accès d'un enfant lancé par CLI au serveur MCP de Studio ; le comportement réel sur quota épuisé (seul un modèle refusé a été provoqué) ; un cycle complet de plusieurs tours par `usine.py` (un tour d'état a été joué, voir `CONNAISSANCES\BILANS\CYCLE-2.md`).

Limite connue : la connexion de la CLI Claude expire (avertissement lu le 16/11/2026 : fin entre le 21 et le 24/11/2026). Pour des tours sans surveillance, le propriétaire lance une fois `claude setup-token` ; un agent ne se connecte jamais lui-même (G8).

## 6. Changer le routage

Seul l'orchestrateur, au bilan (procédure 09), sur comparaison sur pièces ou échecs répétés. `python OUTILS\test-deleguer.py` doit passer après toute modification (aucun petit modèle en premier choix, relecteur différent de l'auteur, plafond G2 écrit).

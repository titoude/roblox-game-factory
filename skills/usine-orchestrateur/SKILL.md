---
name: usine-orchestrateur
description: Orchestrateur de l'usine à jeux Roblox. À utiliser pour lancer ou reprendre un cycle de l'usine (veille, concept, économie, fun, production Studio, QA, release, distribution, bilan), pour connaître l'état des jeux, juger une porte de décision ou déléguer une étape à des sous-agents. Déclencheurs - « lance l'usine », « cycle », « nouveau jeu », « reprendre <jeu> », « état de l'usine », « bilan <jeu> ».
---

# Orchestrateur de l'usine Roblox

Racine de l'usine : `%USERPROFILE%\Documents\Projets\USINE-ROBLOX` (ou la variable d'environnement `USINE_ROBLOX` si elle est définie). Tous les chemins ci-dessous en partent.

Tu es l'orchestrateur : Claude Opus 5.5, effort moyen (repli : Fable 5.2). Tu pilotes la chaîne, tu juges les portes, tu es le seul à écrire dans `CONNAISSANCES\`, le seul à publier. Tu ne produis pas et ne relis pas le même travail.

## Avant tout

1. Lis `GARDE-FOUS.md`. S'il existe un fichier `STOP` à la racine : arrête-toi et dis-le.
2. Lis `PROCEDURES\00-ORCHESTRATION.md` en entier : c'est ta procédure, elle fait foi sur ce résumé.
3. Lance `powershell -File OUTILS\verifier-usine.ps1`, puis `powershell -File OUTILS\etat.ps1 -Liste`.
4. Lis `ALERTES.md` (alertes ouvertes) et `CONNAISSANCES\PLAFONDS.md` (ce qui est autorisé aujourd'hui).
5. Avant la première délégation : `python OUTILS\deleguer.py --liste`. Le modèle d'un rôle vient de `CONNAISSANCES\routage.json` (procédure 13), jamais d'un prompt.

## Ce que tu fais

| Demande | Action |
|---|---|
| « fais un jeu », « cycle » ou rien de précis | Cycle complet sans question : reprendre le jeu en cours à son étape ; sinon veille, puis nouveau jeu, jusqu'à la publication permise et aux boucles du jeu en ligne |
| « retours <slug> », « promo <slug> » | `PROCEDURES\11-RETOURS-JOUEURS.md`, `PROCEDURES\12-PROMOTION-VIDEO.md` |
| « veille » | `PROCEDURES\01-VEILLE-NAVIGATEUR.md`, puis synthèse dans `VEILLE\TENDANCES.md` |
| « nouveau jeu » | `OUTILS\nouveau-jeu.ps1`, puis `PROCEDURES\02-CONCEPT.md` |
| « reprendre <slug> » | `JEUX\<slug>\ETAT.json`, puis la procédure de son étape |
| « bilan <slug> » | `PROCEDURES\09-BILAN.md` |
| « état » | État des jeux, alertes ouvertes, rien d'autre |

Pour chaque étape : lire sa procédure, préparer les entrées en fichiers, déléguer avec le **prompt type** de la procédure complété, lire la ligne `RESULTAT:`, juger la porte contre `CONNAISSANCES\seuils.json`, enregistrer avec `OUTILS\etat.ps1`, committer.

## Règles qui ne se discutent pas

- Deux agents Opus, Fable ou Sonnet au plus en même temps, toi compris : un seul enfant Claude fort à la fois. Codex `gpt-6.1-sol` fait la veille, le calcul, le code et les tests ; aucun petit modèle en premier choix.
- Un seul agent écrit dans une place : vérifie `OUTILS\verrou.ps1 liste` avant de lancer le producteur.
- Aucune dépense, aucune publication publique, aucune annonce sans ligne dans `PLAFONDS.md`.
- CAPTCHA, conditions d'utilisation, double authentification, connexion, paiement : arrêt, `OUTILS\alerte.ps1`, et tu continues ce qui n'en dépend pas.
- Un seuil ne s'abaisse pas en cours de jeu. Deux retours au concepteur par porte de conception ; le troisième échec abandonne l'idée.
- Un sous-agent reçoit un prompt autonome ; il ne lance pas d'autre sous-agent.
- Aucun secret dans un fichier, un prompt ou une commande.

## Fin de session

Verrous rendus, `ETAT.json` et `JOURNAL.md` à jour, commit fait. Compte rendu en 10 lignes : étape atteinte, portes jugées avec leur preuve, alertes ouvertes, prochaine action. Ce qui n'a pas été vérifié est dit comme tel.

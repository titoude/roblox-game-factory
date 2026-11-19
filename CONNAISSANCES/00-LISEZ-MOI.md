# Mémoire partagée de l'usine

Ce dossier est lu par tous les agents et s'améliore après chaque jeu.

## Qui écrit quoi

| Fichier | Qui écrit | Quand |
|---|---|---|
| `PLAFONDS.md` | Le propriétaire seul | Avant toute dépense ou publication |
| `REGLES.md`, `seuils.json`, `SEUILS-PORTES.md`, `MODELES-ET-QUOTAS.md`, `SOURCES-VEILLE.md`, `JOURNAL-DES-JEUX.md`, `LECONS-ARCHIPEL.md`, `BILANS\` | L'orchestrateur seul | Au bilan (`PROCEDURES\09-BILAN.md`), ou sur ordre du propriétaire |
| `PROPOSITIONS\` | Tout agent | Dès qu'il constate quelque chose qui devrait changer une règle |

Un agent qui n'est pas l'orchestrateur ne modifie jamais une règle : il dépose `PROPOSITIONS\AAAA-MM-JJ-<role>-<sujet>.md` (gabarit `OUTILS\GABARITS\PROPOSITION-LECON.md`).
L'orchestrateur fusionne ou refuse chaque proposition au bilan, écrit sa décision dans le fichier et le déplace dans `PROPOSITIONS\traitees\`.
Un commit qui touche ce dossier hors `PROPOSITIONS\` commence par `[orchestrateur]` ou `[proprietaire]` (contrôlé par `OUTILS\hooks\commit-msg`).

## Quoi lire selon son rôle

| Rôle | À lire |
|---|---|
| Tous | `..\GARDE-FOUS.md`, puis les sections de `REGLES.md` de son domaine |
| Orchestrateur | Tout le dossier, `PROPOSITIONS\` en attente, `..\ALERTES.md` |
| Veille | `SOURCES-VEILLE.md`, `REGLES.md` § Marché, `seuils.json` § veille |
| Concept | `REGLES.md` § Concept, Économie, Fun ; `LECONS-ARCHIPEL.md` ; `..\VEILLE\TENDANCES.md` |
| Revue économie | `REGLES.md` § Économie ; `seuils.json` § economie ; `LECONS-ARCHIPEL.md` § Économie |
| Revue fun | `REGLES.md` § Fun, Concept ; `LECONS-ARCHIPEL.md` § Produit |
| Production | `REGLES.md` § Production, Économie ; `LECONS-ARCHIPEL.md` § Technique |
| QA | `REGLES.md` § QA ; `seuils.json` § qa, prototype |
| Release, distribution | `PLAFONDS.md` ; `REGLES.md` § Lancement ; `seuils.json` § beta, pub |

## Principes

- Une règle porte un identifiant, une origine (étude, leçon, bilan) et un statut : `active`, `à calibrer`, `retirée`. Une règle retirée reste dans le fichier, barrée, avec la raison.
- Les valeurs chiffrées des portes vivent dans `seuils.json` (source unique, lue aussi par les scripts). `SEUILS-PORTES.md` en donne le sens, l'origine et l'historique.
- Les seuils ne changent qu'au bilan, sur données mesurées. Pendant un jeu, une dérogation s'écrit dans l'`ETAT.json` du jeu avec sa raison.
- Tout ce qui est écrit ici doit pouvoir être vérifié : une règle sans origine ou une leçon sans preuve est refusée.

# Jeux

Un dossier par jeu, créé par `OUTILS\nouveau-jeu.ps1 -Slug <slug> -Nom "<nom>"`. La veille, elle, est commune : `..\VEILLE\`.

```
JEUX\<slug>\
  ETAT.json              étape, statut, portes jugées, modes dégradés (OUTILS\etat.ps1)
  JOURNAL.md             une ligne par délégation ou décision
  02-concept\            FICHE-CONCEPT.md
  03-economie\           economie.json, SIMULATION.md, RAPPORT-ECONOMIE*.md
  04-fun\                RAPPORT-FUN.md
  05-production\         PLAN-PRODUCTION.md, src\ (source de vérité du code), JOURNAL-LOTS.md, MONDE.md, captures\ (hors git)
  06-qa\                 RAPPORT-QA-<n>.md, notes-*.md, captures\ (hors git)
  07-release\            CHECKLIST-RELEASE.md, MANIFESTE-IDS.json, REVUE-DIFF-v<n>.md
  08-distribution\       KIT-LANCEMENT.md, JOURNAL-CAMPAGNES.md
  09-bilan\              BILAN.md
```

Règles :

- Un seul jeu en production à la fois.
- Aucun fichier de place (`.rbxl`), aucune vidéo, aucune capture dans git : le disque C: est presque plein.
- `MANIFESTE-IDS.json` ne contient que des identifiants publics, jamais une clé.
- `archipel\` est un cas particulier : le jeu est né avant l'usine, ses sources restent dans `blox-craft`.

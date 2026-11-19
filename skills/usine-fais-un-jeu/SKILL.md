---
name: usine-fais-un-jeu
description: Lance un cycle complet de l'usine à jeux Roblox, sans question au propriétaire - veille, idée, conception, économie, fun, production, QA, publication, retours des joueurs. À utiliser quand le propriétaire dit « fais un jeu », « lance l'usine », « un nouveau jeu » ou « continue le jeu en cours ».
---

# Fais un jeu

Racine de l'usine : `%USERPROFILE%\Documents\Projets\USINE-ROBLOX` (ou la variable d'environnement `USINE_ROBLOX`).

Tu es l'orchestrateur. Deux façons de tourner, même routage, même état sur disque :

- **Dans T3 Code** : suis `PROCEDURES\00-ORCHESTRATION.md` (commande « fais un jeu ») ; délègue avec `delegate_task`, charge utile donnée par `python OUTILS\deleguer.py --role <rôle> --format t3 --prompt-fichier <fichier>`.
- **Sans T3 Code** : `python usine.py "fais un jeu"` lance l'orchestrateur et ses agents sur les CLI `claude` et `codex` (procédure 13).

## Avant tout

1. `GARDE-FOUS.md` ; fichier `STOP` présent : arrêt.
2. `python usine.py verifier`, puis `python usine.py etat`, puis `python usine.py roles`.
3. `CONNAISSANCES\PLAFONDS.md` : ce qui peut être publié ou dépensé aujourd'hui (case vide = interdit).

## Ce que « fais un jeu » veut dire

Reprendre le jeu en cours à son étape ; s'il n'y en a pas, veille (si elle a plus de 7 jours), trois pistes, fiche concept, revue d'économie, revue du fun, plan de production, code et tests hors Studio, production et QA dans Studio, release dans les limites de `PLAFONDS.md`, puis les boucles du jeu en ligne : retours des joueurs (procédure 11), mesures, promotion préparée (procédure 12). Chaque porte se juge contre `CONNAISSANCES\seuils.json` et s'enregistre avec `OUTILS\etat.ps1`. Une idée qui échoue trois fois à une porte de conception est abandonnée et la suivante commence, sans rien demander.

## Ce qui arrête

Une frontière humaine (CAPTCHA, conditions, double authentification, connexion, paiement, permission) : alerte, statut bloqué, et tout ce qui n'en dépend pas continue. Un verrou tenu par un autre agent se respecte. Ce qui n'a pas été vu en jeu se dit « non vérifié ».

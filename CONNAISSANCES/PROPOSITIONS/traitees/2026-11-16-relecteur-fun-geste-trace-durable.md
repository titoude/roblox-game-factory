# Proposition — Le geste principal laisse une trace durable

- Date : 2026-11-16. Agent : relecteur fun, Claude Opus 5.5, effort high. Jeu : `lave-la-tour`. Étape : 04.

## Constat

Pour fermer un défaut d'économie (stock de vitres disputé, N02), la fiche v3 fait resalir chaque vitre 20 s après son lavage et rend la hauteur affichée indépendante des vitres lavées. Le défaut d'économie est fermé, mais le geste ne laisse plus rien : c'est la première cause de la note 4 sur la boucle courte. Aucune règle Fun n'a arrêté ce choix à la conception ni à la revue d'économie.

## Preuve

`JEUX\lave-la-tour\02-concept\FICHE-CONCEPT.md` § 3 ter, M07 ; `JEUX\lave-la-tour\04-fun\RAPPORT-FUN-INDEPENDANT.md`, axe 2. Les gagnants du thème lus (Cut a Rock, Depth Incremental) font du résultat du geste la progression elle-même (lu sur leur titre, non joué).

## Règle ou seuil visé

Nouvelle règle Fun (`REGLES.md`, après F10), et une ligne de contrôle dans `PROCEDURES\03-REVUE-ECONOMIE.md`.

## Changement proposé

F11 : « Le résultat du geste principal reste visible au moins jusqu'à la fin de la session ; aucune correction d'économie ne le remet à zéro en silence. Une remise à zéro passe par un événement montré au joueur. » Revue d'économie : toute correction qui touche au résultat visible du geste est signalée à la revue du fun.

## Portée

Jeux à un geste (incrémental, simulation) ; à juger au bilan pour les autres.

---
Décision de l'orchestrateur (bilan du cycle 2, 2026-11-16) : fusionnée dans F11 (à calibrer) et dans la procédure 03 (signalement à la revue du fun).

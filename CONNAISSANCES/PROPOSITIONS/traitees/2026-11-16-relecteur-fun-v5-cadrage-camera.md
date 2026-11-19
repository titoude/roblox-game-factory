# Proposition — Le cadrage de la caméra se confronte à tout ce que la fiche dit « visible »

- Date : 2026-11-16. Agent : relecteur fun, Claude Opus 5.5, effort high. Jeu : `lave-la-tour`. Étape : 04 (revue de la fiche v5).

## Constat

Pour protéger le geste au doigt, la fiche v5 tient la caméra face à la vitre du joueur (vitre au centre, au moins 40 % de la largeur d'un téléphone). La correction est juste pour le geste. Mais la même fiche promet encore que les robots lavent « sous les yeux du joueur » les trois autres façades, que l'on voit « en face, les tours des autres », et qu'un inconnu rejoint un joueur en touchant une seconde place « visible depuis sa propre nacelle ». Les tours entourent la place et chaque joueur lave la façade qui regarde la place : avec ce cadrage, la place et les autres tours sont dans le dos de la caméra, et les autres façades hors du cadre. Ni le concepteur ni le résumé de tête n'ont relu les promesses de visibilité après avoir fixé la caméra.

## Preuve

`git show bf4e35f:JEUX/lave-la-tour/02-concept/FICHE-CONCEPT.md` : l.89 (caméra tenue), l.83 (« sous les yeux »), l.275 (« en face, les tours des autres »), l.197 (seconde place « visible depuis sa propre nacelle »), l.87 et l.195 (façade face à la place, tours autour de la place). Analyse : `JEUX\lave-la-tour\04-fun\RAPPORT-FUN-V5.md`, § 2.1 et correction A.

## Proposition

Ajouter à la procédure 02 (conception), liste de complétude de la porte P1 : « Dès qu'une fiche fixe la caméra (cadrage, angle, verrou), chaque phrase qui dit qu'une chose est visible (par le joueur, depuis la place, depuis les autres tours) précise d'où on la voit, et l'annexe A dit ce qui est dans le cadre à 0 s, 60 s et 5 min. » Vérifiable à la lecture : chaque occurrence de « visible », « voit », « sous les yeux », « en face » porte un point de vue compatible avec la caméra écrite.

Leçon générale : une correction qui verrouille un élément (caméra, commandes, parcours) se relit contre toute la fiche, pas seulement contre le défaut qu'elle corrige. La v4 avait le même défaut sous une autre forme (le résumé « monter » contredit par le parcours en serpentine, proposition `2026-11-16-relecteur-fun-v4-promesse-monotone.md`).

---
Décision de l'orchestrateur (bilan du cycle 2, 2026-11-16) : fusionnée dans C11 (à calibrer) et dans la liste de complétude de la procédure 02.

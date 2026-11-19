# Proposition — La grandeur qui porte la promesse ne recule jamais

- Date : 2026-11-16. Agent : relecteur fun, Claude Opus 5.5, effort high. Jeu : `lave-la-tour`. Étape : 04.

## Constat

La fiche v4 promet « monter en lavant » et l'écrit en résumé (« Cinq vitres font une rangée : la nacelle monte d'un étage »). Mais son parcours détaillé est une serpentine qui redescend sur deux façades sur quatre. Son annexe A annonce « un étage de plus toutes les 10 secondes » entre 61 et 180 s, alors que, d'après ce même parcours, aucun étage nouveau n'arrive avant 3 min 30 environ. Ni la conception ni la porte P1 (complétude) n'ont confronté le résumé au parcours détaillé.

## Preuve

`git show 4e98dca:JEUX/lave-la-tour/02-concept/FICHE-CONCEPT.md` : l.70 (promesse), l.75 (serpentine : « façade 2 en descendant … façade 4 en descendant »), l.261 (annexe A, 61–180 s). Calcul et conséquences : `JEUX\lave-la-tour\04-fun\RAPPORT-FUN-V4.md`, § « Les corrections demandées à la v3 » et correction 1.

## Règle ou seuil visé

Nouvelle règle Concept (`REGLES.md`, après C9) et une ligne de contrôle dans `PROCEDURES\04-REVUE-FUN.md` § Méthode.

## Changement proposé

C10 : « La grandeur qui porte la promesse (hauteur, profondeur, taille, distance) ne baisse jamais en jeu normal et progresse au moins une fois entre 61 et 180 s. La fiche le montre dans l'annexe A, calculé à partir du parcours détaillé et pas du résumé. »

Revue du fun, méthode : rejouer l'annexe A à partir du parcours détaillé et noter toute phrase de résumé qu'il contredit.

## Portée

Jeux dont la promesse est une grandeur qui croît (incrémental vertical, profondeur, course) ; à juger au bilan pour les autres.

---
Décision de l'orchestrateur (bilan du cycle 2, 2026-11-16) : fusionnée dans C10 (à calibrer) et dans la méthode de la procédure 04.

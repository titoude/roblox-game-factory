# Proposition — Synchroniser le plan avec le prototype corrigé

- Date : 2026-11-16. Agent : contre-vérificateur n°4, gpt-6.1-sol, effort xhigh. Jeu : lave-la-tour. Étape : 03, passe papier.

## Constat

La fiche v5 et `economie.json` sont cohérents et la simulation passe. Le plan provisoire de production décrit encore le prototype v3 : le suivre ferait coder un stock et un parcours différents de ceux contre-vérifiés.

## Preuve

Commit unique `bf4e35fe9bb6c96e0f370b08a615752a6e1462e6`, preuves lues et calculées, aucun test en jeu :

- `JEUX/lave-la-tour/05-production/PLAN-PRODUCTION.md`, L25/42–49/58 : cinq étages,30 vitres, resalissure20 s, mousse30 s, stock invisible chez autrui ; première vitre8 s et achat27 s.
- `JEUX/lave-la-tour/02-concept/FICHE-CONCEPT.md`, L143–155/182–189/267–281 : tour1 de120 étages×5=600 vitres, état propre persistant, pigeons100 après10 s, mousse fenêtre10 s ; première vitre6 s, achat25 s,28 vitres à60 s et88 à180 s.
- Calcul : cinq étages×5=25 vitres, soit **trois de moins** que le parcours annoncé à60 s. La simulation monétaire ignore le stock : son PASSER ne peut pas détecter cette divergence du plan.
- Rapport : `JEUX/lave-la-tour/03-economie/RAPPORT-ECONOMIE-contre-verification-4.md`, N01. Aucun coût ni revenu de robot à modifier.

## Règle ou seuil visé

`PROCEDURES/05-PRODUCTION-STUDIO.md` § Conditions de départ et § Constantes ; `REGLES.md` E10 et A3. Aucun seuil à changer.

## Changement proposé

Ajouter à la préparation de L0 : « Après une nouvelle version de la fiche, aligner le plan de production sur cette version avant de coder : stock et géométrie de la boucle, transitions de resalissure, premières actions et achats, durée et quotas des bonus. Un plan déclaré provisoire conserve ce statut jusqu'à cette mise à jour. Distinguer les résultats monétaires du simulateur des preuves du parcours physique ; ne pas modifier les coûts ou revenus pour corriger un plan périmé. »

## Portée

Jeux de l'usine dont le concept évolue après l'écriture du plan. Proposition documentaire, pas une nouvelle demande d'autorisation ni une obligation de rejouer des contrôles inchangés.

---
Décision de l'orchestrateur (au bilan) : en attente.

---
Décision de l'orchestrateur (bilan du cycle 2, 2026-11-16) : fusionnée dans P13 (active) et dans la procédure 05 (conditions de départ).

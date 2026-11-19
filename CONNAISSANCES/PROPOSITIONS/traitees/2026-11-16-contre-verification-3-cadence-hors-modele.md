# Proposition — Couvrir la cadence des nouvelles boucles hors modèle

- Date : 2026-11-16. Agent : contre-vérificateur économie n°3, gpt-6.1-sol, effort xhigh. Jeu : lave-la-tour. Étape : 03, passe papier.

## Constat

La fiche v4 conserve les constantes des robots et la simulation officielle passe, mais ajoute une Flèche dont le prix utilise un équipement que sa condition d'accès n'impose pas. Le PASSER du simulateur ne couvre donc pas tous les états autorisés de cette nouvelle boucle.

## Preuve

Commit `4e98dca296dd2bbbf78df7a75794808309c8e735`, `JEUX/lave-la-tour/02-concept/FICHE-CONCEPT.md`, lignes 127 et 142–149 : accès r10≥10, R_fin=300757992117, segment maximal 540R_fin.

`JEUX/lave-la-tour/03-economie/RAPPORT-ECONOMIE-contre-verification-3.md`, §2.1 et F01 : simulateur sortie 0 et SIMULATION.md identique ; état légal r1…r9=3, r10=10, aucune amélioration, R=156621278732,75. Le segment maximal se finance en 942,69 s à 30 unités/min, même en 914,96 s au plafond 40 sans mousse, au-delà de 900 s. Aucune défaillance d'implémentation supposée ; preuve papier uniquement.

## Règle ou seuil visé

`PROCEDURES/03-REVUE-ECONOMIE.md` § Conventions et Porte P2 ; `REGLES.md` E10/E12 ; `seuils.json` § economie.ecart_max_apres_60min_s. Aucun changement du seuil proposé.

## Changement proposé

Ajouter à la procédure 03 :

> À chaque ajout de boucle ou changement de stock, de geste ou de coopération, dresser la liste des mécanismes ignorés par le simulateur. Pour chaque nouvel accès, calculer la cadence et les promesses de récompense dans l'état d'équipement minimal qu'autorise cet accès, ainsi que dans l'état de référence. Un résultat PASSER du simulateur ne valide que son périmètre ; conserver les constantes de coût et de revenu ne dispense pas de cette contre-vérification. Séparer les défauts démontrés, les hypothèses de calcul et les scénarios QA.

## Portée

Tous les jeux de l'usine ayant une boucle ou un revenu de référence hors modèle ; contrôle papier en complément de la passe code et de la QA. Aucun outil, seuil ni règle active modifié par cette proposition.

---
Décision de l'orchestrateur (au bilan) : en attente.

---
Décision de l'orchestrateur (bilan du cycle 2, 2026-11-16) : fusionnée dans E16 (active) et dans la procédure 03.

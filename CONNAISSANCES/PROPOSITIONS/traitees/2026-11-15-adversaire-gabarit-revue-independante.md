# Proposition — Gabarit de revue économique indépendante

- Date : 2026-11-15. Agent : adversaire, Codex gpt-6.1-sol xhigh. Jeu : lave-la-tour. Étape : 03, passe 1 papier.

## Constat

Le gabarit commun demande des résultats de simulation et une simulation rejouée alors que l'adversaire indépendant peut recevoir l'interdiction de lire le résultat du calculateur. Ses seules valeurs de verdict pour la cadence sont PASSE et ÉCHEC, et il n'a pas de champ distinct pour une gravité conditionnelle à un test futur.

## Preuve

- OUTILS/GABARITS/RAPPORT-ECONOMIE.md:L13 : cadence limitée à PASSE / ÉCHEC ; L27–L39 : commande et résultats du simulateur ; L52–L56 : simulation rejouée et effet simulé.
- PROCEDURES/03-REVUE-ECONOMIE.md, section Agent « adversaire » : rôle de recherche de failles distinct du rôle « calcul » ; section Rapport : défaut certain seulement sur chemin démontrable, sinon scénario de jeu.
- Mission reçue pour lave-la-tour : « Ne lis pas le rapport de l'autre vérificateur (RAPPORT-ECONOMIE-calcul.md) ni SIMULATION.md. »
- JEUX/lave-la-tour/03-economie/RAPPORT-ECONOMIE-adversaire.md, verdict et sections 2, 3, 6 : distinction appliquée sans consulter l'autre revue.

## Règle ou seuil visé

OUTILS/GABARITS/RAPPORT-ECONOMIE.md ; PROCEDURES/03-REVUE-ECONOMIE.md, section Rapport. Aucun seuil économique à modifier.

## Changement proposé

Ajouter au gabarit cette instruction exacte :

> Pour le rôle adversaire indépendant, la cadence peut être « non évaluée, rôle calcul ». Les tableaux et résultats de simulation sont facultatifs ; les calculs directs doivent rester reproductibles et une proposition non simulée est explicitement marquée comme telle. Ne jamais consulter l'autre rapport ou sa simulation si l'indépendance de la mission l'interdit. Séparer le compteur des P0/P1 certains de la gravité conditionnelle des risques à vérifier en jeu ; l'absence d'une règle dans une fiche ne démontre pas une vulnérabilité d'implémentation. Un défaut démontré du modèle papier reste distinct d'une preuve en jeu au sens de G15.

Ajouter « non évaluée » aux choix de cadence et « effet calculé / non simulé » à l'intitulé des propositions. Aucun changement de règle ou d'outil n'a été effectué par cet agent.

## Portée

Toutes les revues économiques indépendantes de l'usine, en particulier la passe papier. La validation de cadence et la contre-vérification restent requises par leurs procédures existantes.

---
Décision de l'orchestrateur (bilan du cycle 1, 2026-11-15) : **fusionnée**. Gabarit OUTILS\GABARITS\RAPPORT-ECONOMIE.md : cadence « non évaluée » pour l'adversaire, compteur séparé des risques à vérifier en jeu, section « Décisions manquantes dans la fiche », propositions « effet simulé ou calculé ».

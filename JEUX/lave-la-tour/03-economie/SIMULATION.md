# Simulation économique — lave-la-tour

Entrée : `JEUX/lave-la-tour/03-economie/economie.json`. Seuils : `CONNAISSANCES/seuils.json`, section `economie`. Durée simulée : 4:00:00 au plus.
Ce rapport est un **calcul** : pas d'une seconde, joueur qui achète l'objet au meilleur compromis attente + remboursement. Il ne mesure ni le plaisir de jeu ni la rétention, et rien n'y est vérifié en jeu.

## Profil « actif »

| Mesure | Valeur | Attendu | Verdict | Détail |
|---|---|---|---|---|
| Premier achat | 0:20 | ≤ 1:00 | PASSE | Robot ventouse à 10 |
| Écart maximal, 0 à 10 min | 1:01 | ≤ 2:00 | PASSE | à partir de 6:50 |
| Écart maximal, 10 à 60 min | 5:32 | ≤ 8:00 | PASSE | à partir de 59:23 |
| Écart maximal, après 60 min | 6:18 | ≤ 15:00 | PASSE | à partir de 1:15:49 |
| Remboursement de chaque exemplaire | max 3:39 (r4 n°10) | 0:30 à 5:00 | PASSE | 0 exemplaire(s) hors bornes sur 100 |
| Durée de contenu actif | 1:37:09 | ≥ 1:30:00 | PASSE | fin de contenu atteinte |

Achats : 105. Revenu en fin de simulation : 390 985 389 755 par seconde, dont 23,1 % venant de l'action du joueur.
Jalons : contrats à 4:41, tour2 à 15:33, tour3 à 50:52.

### Chronologie des achats (profil actif)

| Temps | Écart | Achat | Coût |
|---|---|---|---|
| 0:20 | 0:20 | Robot ventouse | 10 |
| 0:36 | 0:16 | Robot ventouse | 12 |
| 0:50 | 0:14 | Robot ventouse | 15 |
| 1:04 | 0:14 | Robot ventouse | 18 |
| 1:17 | 0:13 | Robot ventouse | 21 |
| 1:39 | 0:22 | Raclette large | 40 |
| 2:15 | 0:36 | Raclette automatique | 90 |
| 2:37 | 0:22 | Raclette automatique | 108 |
| 2:55 | 0:18 | Raclette automatique | 130 |
| 3:11 | 0:16 | Raclette automatique | 156 |
| 3:14 | 0:03 | Robot ventouse | 25 |
| 3:28 | 0:14 | Raclette automatique | 187 |
| 3:31 | 0:03 | Robot ventouse | 30 |
| 3:45 | 0:14 | Raclette automatique | 224 |
| 4:31 | 0:46 | Bras articulé | 800 |
| 5:05 | 0:34 | Bras articulé | 936 |
| 5:32 | 0:27 | Bras articulé | 1 096 |
| 5:56 | 0:24 | Bras articulé | 1 282 |
| 6:00 | 0:04 | Raclette automatique | 269 |
| 6:03 | 0:03 | Robot ventouse | 36 |
| 6:11 | 0:08 | Savon moussant | 700 |
| 6:29 | 0:18 | Bras articulé | 1 500 |
| 6:32 | 0:03 | Raclette automatique | 323 |
| 6:50 | 0:18 | Bras articulé | 1 754 |
| 7:51 | 1:01 | Nacelle robot | 7 000 |
| 8:36 | 0:45 | Nacelle robot | 7 980 |
| 8:47 | 0:11 | Ventouses renforcées | 2 400 |
| 8:50 | 0:03 | Raclette automatique | 387 |
| 8:53 | 0:03 | Raclette automatique | 465 |
| 9:18 | 0:25 | Nacelle robot | 9 098 |
| 9:45 | 0:27 | Nacelle robot | 10 371 |
| 9:48 | 0:03 | Robot ventouse | 43 |
| 9:51 | 0:03 | Bras articulé | 2 053 |
| 10:13 | 0:22 | Nacelle robot | 11 823 |
| 10:36 | 0:23 | Nacelle robot | 13 478 |
| 10:39 | 0:03 | Bras articulé | 2 401 |
| 10:42 | 0:03 | Robot ventouse | 52 |
| 11:01 | 0:19 | Nacelle robot | 15 365 |
| 11:04 | 0:03 | Bras articulé | 2 810 |
| 11:25 | 0:21 | Nacelle robot | 17 516 |
| … | … | 55 achats non listés | … |
| 1:22:07 | 6:18 | Station de lavage orbitale | 4 500 000 000 000 |
| 1:25:55 | 3:48 | Station de lavage orbitale | 4 792 500 000 000 |
| 1:27:35 | 1:40 | Station de lavage orbitale | 5 104 012 500 000 |
| 1:29:11 | 1:36 | Station de lavage orbitale | 5 435 773 312 500 |
| 1:30:16 | 1:05 | Station de lavage orbitale | 5 789 098 577 813 |
| 1:31:10 | 0:54 | Station de lavage orbitale | 6 165 389 985 371 |
| 1:32:02 | 0:52 | Station de lavage orbitale | 6 566 140 334 420 |
| 1:32:47 | 0:45 | Station de lavage orbitale | 6 992 939 456 157 |
| 1:33:29 | 0:42 | Station de lavage orbitale | 7 447 480 520 807 |
| 1:34:09 | 0:40 | Station de lavage orbitale | 7 931 566 754 660 |

## Profil « lent » (information, hors verdict)

| Mesure | Valeur | Attendu | Verdict | Détail |
|---|---|---|---|---|
| Premier achat | 0:40 | ≤ 1:00 | PASSE | Robot ventouse à 10 |
| Écart maximal, 0 à 10 min | 1:09 | ≤ 2:00 | PASSE | à partir de 8:10 |
| Écart maximal, 10 à 60 min | 6:07 | ≤ 8:00 | PASSE | à partir de 48:40 |
| Écart maximal, après 60 min | 7:01 | ≤ 15:00 | PASSE | à partir de 1:24:05 |
| Remboursement de chaque exemplaire | max 4:07 (r4 n°10) | 0:30 à 5:00 | PASSE | 0 exemplaire(s) hors bornes sur 100 |
| Durée de contenu actif | 1:47:01 | ≥ 1:30:00 | PASSE | fin de contenu atteinte |
| Retard du joueur lent sur le joueur actif | 10,2 % | ≥ 5,0 % | PASSE | actif 1:37:09, lent 1:47:01 |

Achats : 105. Revenu en fin de simulation : 345 871 690 936 par seconde, dont 13,0 % venant de l'action du joueur.
Jalons : contrats à 5:51, tour2 à 17:55, tour3 à 56:47.

## Générateurs

| Générateur | Coût | Revenu/s | Remboursement | Chantier | Par rapport au précédent | Défauts |
|---|---|---|---|---|---|---|
| Robot ventouse | 10 | 0,25 | 0:40 | 0:00 | — | aucun |
| Raclette automatique | 90 | 2 | 0:45 | 0:00 | coût ×9.0, revenu ×8.0 | aucun |
| Bras articulé | 800 | 12 | 1:07 | 0:10 | coût ×8.9, revenu ×6.0 | aucun |
| Nacelle robot | 7 000 | 80 | 1:28 | 0:20 | coût ×8.8, revenu ×6.7 | aucun |
| Drone laveur | 200 000 | 1 650 | 2:01 | 0:40 | coût ×28.6, revenu ×20.6 | aucun |
| Essaim de drones | 5 600 000 | 34 500 | 2:42 | 1:00 | coût ×28.0, revenu ×20.9 | aucun |
| Canon à mousse | 165 000 000 | 790 000 | 3:29 | 1:30 | coût ×29.5, revenu ×22.9 | aucun |
| Dirigeable laveur | 5 000 000 000 | 19 600 000 | 4:15 | 2:00 | coût ×30.3, revenu ×24.8 | aucun |
| Hélico-brosse | 150 000 000 000 | 520 000 000 | 4:48 | 2:30 | coût ×30.0, revenu ×26.5 | aucun |
| Station de lavage orbitale | 4 500 000 000 000 | 15 500 000 000 | 4:50 | 3:00 | coût ×30.0, revenu ×29.8 | aucun |

Remboursement nominal = coût du premier exemplaire ÷ revenu par seconde, sans amélioration, attendu entre 0:30 et 5:00 ; chantier ≤ 3:00. Le remboursement de chaque exemplaire réellement acheté est jugé dans le tableau du profil.

## Offres payantes

| Offre | Type | Prix (Robux) | Verdict | Raison |
|---|---|---|---|---|
| Raclette motorisée | confort | 149 | PASSE | — |
| Chantiers express | temps | 99 | PASSE | — |
| Peintures de nacelle | expression | 49 | PASSE | — |
| Mousse colorée | expression | 29 | PASSE | — |
| Styles de tour | expression | 79 | PASSE | — |

Jeu déclaré non compétitif : dans un jeu compétitif, monnaie et multiplicateur de revenu payants sont refusés.

## Verdict de cadence

**PASSE** : aucun seuil jugé n'est en échec pour le profil actif (une ligne ALERTE ou SANS OBJET n'est pas une preuve).
Les lignes ALERTE demandent une justification écrite dans le rapport d'économie.

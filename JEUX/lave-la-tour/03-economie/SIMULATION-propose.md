# Simulation économique — lave-la-tour

Entrée : `JEUX\lave-la-tour\03-economie\economie-propose.json`. Seuils : `CONNAISSANCES/seuils.json`, section `economie`. Durée simulée : 4:00:00 au plus.
Ce rapport est un **calcul** : pas d'une seconde, joueur qui achète l'objet au meilleur compromis attente + remboursement. Il ne mesure ni le plaisir de jeu ni la rétention, et rien n'y est vérifié en jeu.

## Profil « actif »

| Mesure | Valeur | Attendu | Verdict | Détail |
|---|---|---|---|---|
| Premier achat | 0:20 | ≤ 1:00 | PASSE | Robot ventouse à 10 |
| Écart maximal, 0 à 10 min | 1:28 | ≤ 2:00 | PASSE | à partir de 7:23 |
| Écart maximal, 10 à 60 min | 2:13 | ≤ 8:00 | PASSE | à partir de 48:31 |
| Écart maximal, après 60 min | 11:37 | ≤ 15:00 | PASSE | à partir de 1:00:20 |
| Durée de contenu actif | 1:30:07 | ≥ 1:30:00 | PASSE | fin de contenu atteinte |

Achats : 105. Revenu en fin de simulation : 1 266 389 935 par seconde.
Jalons : tranche2 à 5:01, tour2 à 14:59, tour3 à 41:04.

### Chronologie des achats (profil actif)

| Temps | Écart | Achat | Coût |
|---|---|---|---|
| 0:20 | 0:20 | Robot ventouse | 10 |
| 0:36 | 0:16 | Robot ventouse | 12 |
| 0:51 | 0:15 | Robot ventouse | 14,4 |
| 1:05 | 0:14 | Robot ventouse | 17,28 |
| 1:19 | 0:14 | Robot ventouse | 20,74 |
| 2:10 | 0:51 | Raclette automatique | 90 |
| 2:39 | 0:29 | Raclette automatique | 108 |
| 2:46 | 0:07 | Raclette large | 40 |
| 3:07 | 0:21 | Raclette automatique | 129,6 |
| 3:26 | 0:19 | Raclette automatique | 155,52 |
| 3:29 | 0:03 | Robot ventouse | 24,88 |
| 3:46 | 0:17 | Raclette automatique | 186,62 |
| 3:49 | 0:03 | Robot ventouse | 29,86 |
| 4:51 | 1:02 | Bras articulé | 800 |
| 5:35 | 0:44 | Bras articulé | 960 |
| 5:44 | 0:09 | Raclette automatique | 223,95 |
| 6:14 | 0:30 | Bras articulé | 1 152 |
| 6:21 | 0:07 | Raclette automatique | 268,74 |
| 6:48 | 0:27 | Bras articulé | 1 382 |
| 6:51 | 0:03 | Robot ventouse | 35,83 |
| 6:55 | 0:04 | Raclette automatique | 322,49 |
| 7:20 | 0:25 | Bras articulé | 1 659 |
| 7:23 | 0:03 | Robot ventouse | 43 |
| 8:51 | 1:28 | Nacelle robot | 7 000 |
| 9:54 | 1:03 | Nacelle robot | 8 393 |
| 10:09 | 0:15 | Ventouses renforcées | 2 400 |
| 10:12 | 0:03 | Raclette automatique | 386,98 |
| 10:15 | 0:03 | Raclette automatique | 464,38 |
| 10:52 | 0:37 | Nacelle robot | 10 063 |
| 11:00 | 0:08 | Bras articulé | 1 991 |
| 11:37 | 0:37 | Nacelle robot | 12 066 |
| 11:44 | 0:07 | Bras articulé | 2 389 |
| 11:47 | 0:03 | Robot ventouse | 51,6 |
| 12:19 | 0:32 | Nacelle robot | 14 467 |
| 12:25 | 0:06 | Bras articulé | 2 867 |
| 14:19 | 1:54 | Drone laveur | 60 000 |
| 14:51 | 0:32 | Nacelle robot | 17 346 |
| 15:58 | 1:07 | Drone laveur | 69 480 |
| 17:19 | 1:21 | Double équipe | 110 000 |
| 17:52 | 0:33 | Drone laveur | 80 458 |
| … | … | 55 achats non listés | … |
| 1:11:57 | 11:37 | Station de lavage orbitale | 19 250 000 000 |
| 1:16:39 | 4:42 | Station de lavage orbitale | 20 693 750 000 |
| 1:19:05 | 2:26 | Station de lavage orbitale | 22 245 781 250 |
| 1:20:47 | 1:42 | Station de lavage orbitale | 23 914 214 844 |
| 1:22:15 | 1:28 | Station de lavage orbitale | 25 707 780 957 |
| 1:23:24 | 1:09 | Station de lavage orbitale | 27 635 864 529 |
| 1:24:27 | 1:03 | Station de lavage orbitale | 29 708 554 368 |
| 1:25:25 | 0:58 | Station de lavage orbitale | 31 936 695 946 |
| 1:26:18 | 0:53 | Station de lavage orbitale | 34 331 948 142 |
| 1:27:07 | 0:49 | Station de lavage orbitale | 36 906 844 253 |

## Profil « lent » (information, hors verdict)

| Mesure | Valeur | Attendu | Verdict | Détail |
|---|---|---|---|---|
| Premier achat | 0:40 | ≤ 1:00 | PASSE | Robot ventouse à 10 |
| Écart maximal, 0 à 10 min | 1:28 | ≤ 2:00 | PASSE | à partir de 8:20 |
| Écart maximal, 10 à 60 min | 2:13 | ≤ 8:00 | PASSE | à partir de 49:29 |
| Écart maximal, après 60 min | 11:34 | ≤ 15:00 | PASSE | à partir de 1:01:21 |
| Durée de contenu actif | 1:31:05 | ≥ 1:30:00 | PASSE | fin de contenu atteinte |

Achats : 105. Revenu en fin de simulation : 1 266 389 932 par seconde.
Jalons : tranche2 à 6:04, tour2 à 15:57, tour3 à 42:02.

## Générateurs

| Générateur | Coût | Revenu/s | Remboursement | Chantier | Par rapport au précédent | Défauts |
|---|---|---|---|---|---|---|
| Robot ventouse | 10 | 0,25 | 0:40 | 0:00 | — | aucun |
| Raclette automatique | 90 | 2 | 0:45 | 0:00 | coût ×9.0, revenu ×8.0 | aucun |
| Bras articulé | 800 | 12 | 1:07 | 0:10 | coût ×8.9, revenu ×6.0 | aucun |
| Nacelle robot | 7 000 | 80 | 1:28 | 0:20 | coût ×8.8, revenu ×6.7 | aucun |
| Drone laveur | 60 000 | 500 | 2:00 | 0:40 | coût ×8.6, revenu ×6.2 | aucun |
| Essaim de drones | 520 000 | 3 200 | 2:42 | 1:00 | coût ×8.7, revenu ×6.4 | aucun |
| Canon à mousse | 4 600 000 | 22 000 | 3:29 | 1:30 | coût ×8.8, revenu ×6.9 | aucun |
| Dirigeable laveur | 42 000 000 | 165 000 | 4:15 | 2:00 | coût ×9.1, revenu ×7.5 | aucun |
| Hélico-brosse | 390 000 000 | 1 350 000 | 4:49 | 2:30 | coût ×9.3, revenu ×8.2 | aucun |
| Station de lavage orbitale | 19 250 000 000 | 66 000 000 | 4:52 | 3:00 | coût ×49.4, revenu ×48.9 | aucun |

Remboursement = coût du premier exemplaire ÷ revenu par seconde, attendu entre 0:30 et 5:00 ; chantier ≤ 3:00.

## Offres payantes

| Offre | Type | Prix (Robux) | Verdict | Raison |
|---|---|---|---|---|
| Raclette automatique | confort | 149 | PASSE | — |
| Chantiers express | temps | 99 | PASSE | — |
| Peintures de nacelle | expression | 49 | PASSE | — |
| Mousse colorée | expression | 29 | PASSE | — |
| Styles de tour | expression | 79 | PASSE | — |

Jeu déclaré non compétitif : dans un jeu compétitif, monnaie et multiplicateur de revenu payants sont refusés.

## Verdict de cadence

**PASSE** : tous les seuils sont tenus pour le profil actif.
Les lignes ALERTE demandent une justification écrite dans le rapport d'économie.

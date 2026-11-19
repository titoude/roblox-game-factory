# Relevé de veille — RoStats, Roblox Charts, API documentée — 2026-11-15

- Veilleur : orchestrateur (Claude Fable 5.2), pages lues par un lecteur Claude Haiku 5.5 (agent `web-fetch`, une page par appel). Repli de la règle A6 : les veilleurs Haiku délégués n'avaient pas d'outil de lecture de page (voir `v1`, `v2`, `v4`).
- Mission : A (tour des tendances, tour 1), puis matière de la mission B (voir `b1-theme-un-geste.md`).
- Outil de navigation utilisé : lecture sans navigateur (`WebFetch`). Mode de preuve : « lu par WebFetch ». Rien n'a été vu à l'écran.
- Session : 2026-11-15, de 22:13 à 22:23 UTC environ (l'outil ne rend pas l'heure de chaque page). Pages lues : 9 (plafond 40) — RoStats 7 (plafond 8), Roblox Charts 1, RoWatcher 1. Un appel à l'API documentée `games.roblox.com/v1/games` à 22:22:30 UTC.
- Sources interrompues : Roblox Charts (page lue, classement non rendu : coquille de script, 646 caractères) ; RoWatcher (`/terms` : coquille vide, conditions illisibles → source non retenue, aucune autre page lue). Aucun CAPTCHA, aucune connexion, aucun refus.

## Pages lues

| # | URL | Ce qui a été lu |
|---|---|---|
| 1 | https://www.roblox.com/charts | Rien d'utile : classement chargé par script |
| 2 | https://rowatcher.com/terms | Rien : page vide sans rendu de script |
| 3 | https://rostats.io/charts/2026-10 | Classement d'octobre 2026, moyennes journalières, comparaison à septembre |
| 4 | https://rostats.io/charts/2026-11 | Classement de novembre en cours (14 jours sur 30, données jusqu'au 14/11), comparaison à octobre |
| 5 | https://rostats.io/genres | Joueurs, visites et nombre de jeux par genre (instantané) |
| 6 | https://rostats.io/new | Jeux de moins de 30 à 60 jours : « New & rising », « New & stable », « Breakouts by genre », « Moving up in the top 100 » (10 lignes par tableau en accès libre) |
| 7 | https://rostats.io/trending | Moyenne des 24 dernières heures contre les 24 précédentes (jeux de 500 joueurs et plus) |
| 8 | https://rostats.io/games/10766972131 | Fiche de Throw Food For Animals |
| 9 | https://rostats.io/games/10765288803 | Fiche de Break and Steal an Egg |

Ce que RoStats dit de ses chiffres : « Ranked by average players across the days of the month » ; « Averages are daily averages of sampled player counts » ; durée de session et revenus sont des estimations du site.

## Relevé — classement mensuel (moyenne de joueurs, novembre 2026 en cours contre octobre 2026)

Source : page 4 ; colonne « octobre » confirmée par la page 3. Unité : joueurs simultanés, moyenne journalière du mois. Novembre ne couvre que 14 jours : une moyenne partielle se compare avec prudence à un mois plein.

| Rang nov. | Jeu | Moy. nov. (14 j) | Moy. oct. | Rang oct. | Écart absolu | Écart relatif | Pic nov. |
|---|---|---:|---:|---|---:|---:|---:|
| 1 | Steal An Egg and Collect Rare Pets | 846 562 | 1 341 295 | 1 | −494 733 | −36,9 % | 7 622 107 |
| 2 | Brookhaven RP | 362 102 | 367 750 | 3 | −5 648 | −1,5 % | 676 125 |
| 3 | Blox Fruits | 294 777 | 175 376 | 6 | +119 401 | +68,1 % | 721 599 |
| 4 | Murder Mystery 2 | 288 604 | 404 427 | 2 | −115 823 | −28,6 % | 631 147 |
| 5 | Throw Food For Animals | 202 898 | 12 532 | 106 | +190 366 | +1 519 % | 2 474 602 |
| 6 | Adopt Me! | 170 285 | 226 902 | 4 | −56 617 | −25,0 % | 757 309 |
| 7 | RIVALS | 151 315 | 164 562 | 7 | −13 247 | −8,0 % | 472 496 |
| 8 | 99 Nights in the Forest | 144 272 | 203 864 | 5 | −59 592 | −29,2 % | 1 447 066 |
| 9 | Break and Steal an Egg | 103 526 | 104 490 | 11 | −964 | −0,9 % | 657 113 |
| 10 | Steal a Brainrot | 88 654 | 155 204 | 8 | −66 550 | −42,9 % | 944 391 |
| 11 | Jujutsu Shenanigans | 87 986 | 131 418 | 9 | −43 432 | −33,0 % | 163 823 |
| 12 | Anime Adventures | 85 728 | 13 746 | 93 | +71 982 | +523,7 % | 141 555 |
| 13 | Dandy's World | 84 974 | 114 123 | 10 | −29 149 | −25,5 % | 253 863 |
| 14 | Fisch | 72 828 | 78 590 | 13 | −5 762 | −7,3 % | 380 954 |
| 15 | DONT SPLASH | 72 504 | NP (nouvelle entrée) | — | NP | NP | 167 091 |
| 16 | Fish It! | 63 976 | 73 441 | 14 | −9 465 | −12,9 % | 144 058 |
| 17 | Forsaken | 59 222 | 50 786 | 23 | +8 436 | +16,6 % | 278 097 |
| 18 | The Strongest Battlegrounds | 58 589 | 52 636 | 21 | +5 953 | +11,3 % | 172 266 |
| 19 | Catalog Avatar Creator | 58 055 | 61 171 | 19 | −3 116 | −5,1 % | 93 054 |
| 20 | Dress To Impress | 55 796 | 71 757 | 16 | −15 961 | −22,2 % | 112 713 |
| 21 | Pet Simulator 99! | 49 644 | 52 064 | 22 | −2 420 | −4,6 % | 94 362 |
| 22 | Attack on Titan Revolution | 48 734 | 15 145 | 81 | +33 589 | +221,8 % | 71 746 |
| 23 | Violence District | 48 270 | 52 842 | 20 | −4 572 | −8,7 % | 93 219 |
| 24 | Evade | 44 092 | 48 669 | 25 | −4 577 | −9,4 % | 83 475 |
| 25 | Practical Basketball | 44 049 | 6 345 | 229 | +37 704 | +594,2 % | 119 046 |

Rangs 26 à 50, lignes relevées par mot-clé seulement : 30 Hyper Realistic Ragdoll 36 935 (nouvelle entrée) ; 32 Cameraman Tower Defense 35 728 (+133,9 %) ; 34 Survive Your Ideas 34 649 (nouvelle entrée) ; 38 +1 Speed Keyboard Escape 29 701 (93 249 en octobre, −68,1 %) ; 39 +1 Venom Evolution 29 072 (14 508, +100,4 %) ; 43 Sell Fries! 24 564 (31 349, −21,6 %) ; 47 Ragdoll Physics 23 139 (nouvelle entrée) ; 48 Steal A Pet And Ride It! 23 002 (9 084, +153,2 %) ; 49 BlockSpin 21 921 (19 998, +9,6 %).

Octobre contre septembre (page 3), lignes utiles au thème : Break and Steal an Egg 3 832 → 104 490 (+2 627 %) ; +1 Speed Keyboard Escape 168 437 → 93 249 (−44,6 %) ; Ride A Pet 99 134 → 72 054 (−27,3 %) ; Steal a Brainrot 118 848 → 155 204 (+30,6 %) ; nouvelles entrées d'octobre au-delà du rang 40 : +1 Stone Skipping 27 412 (rang 41), Climb For Animals Eggs 25 466 (rang 43), Tap Simulator REBORN 25 213 (rang 44). Aucune de ces trois n'apparaît dans les 50 premiers de novembre (les mots-clés « +1 », « animals » et « egg » étaient cherchés ; « tap » ne l'était pas : pour Tap Simulator REBORN l'absence est **non vérifiée**).

## Plus fortes montées du mois (page 4, « Biggest gainers », jeux de 1 000 joueurs moyens et plus)

| Jeu | Rang nov. | Moy. nov. | Moy. oct. | Écart relatif |
|---|---|---:|---:|---:|
| Cut a Rock | 70 | 17 261 | 897 | +1 824 % |
| +1 Power Fruit Evolution | 176 | 8 576 | 527 | +1 527 % |
| Throw Food For Animals | 5 | 202 898 | 12 532 | +1 519 % |
| LINE UP! Metro Tycoon | 172 | 8 700 | 603 | +1 343 % |
| Club Legacy: Soccer Manager | 373 | 4 437 | 323 | +1 274 % |
| Climb and Steal an Egg | 285 | 5 647 | 419 | +1 248 % |
| Push the Patient [1-2 PLAYER OBBY] | 168 | 8 839 | 708 | +1 148 % |
| Make a Cartoon! | 128 | 11 472 | 1 145 | +901,9 % |
| Ride An Egg | 187 | 8 190 | 846 | +868,1 % |
| Depth Incremental | 66 | 18 072 | 2 586 | +598,8 % |

## Jeux récents (page 6, semaine close le 14/11 contre la précédente)

| Jeu | Genre | Âge | Moyenne de la semaine | Écart sur la semaine |
|---|---|---|---:|---|
| Throw Food For Animals | Simulation | 59 j | 261 253 | +80,7 % |
| Survive Your Ideas | Survival | 40 j | 55 019 | +179,2 % |
| +1 Venom Evolution | Simulation | 42 j | 27 598 | −9,7 % |
| MALAM SAMA OPAH | Survival | 27 j | 26 876 | +76,5 % |
| Unstable SMP FFA | Action | 26 j | 25 914 | +225,1 % |
| Sweep The Moon | Simulation | 24 j | 24 664 | +489,0 % |
| Bloody Ragdoll Physics | Simulation | 16 j | 23 908 | +1 265 % |
| Sandworm Playground | Simulation | 14 j | 22 314 | nouveau |
| Criminal Simulator | Simulation | 39 j | 21 639 | +10,0 % |
| Depth Incremental | Simulation | 39 j | 18 768 | +8,0 % |
| Ragdoll Soccer | Sports & Racing | 33 j | 18 584 | +2 960 % |
| Ragdoll Research | Simulation | 19 j | 18 495 | +189,5 % |
| Ant Evolution | Survival | 19 j | 16 542 | nouveau |
| Do Not Stop. | Survival | 22 j | 12 511 | nouveau |
| Throw a Seed | Simulation | 9 j | 12 427 | nouveau |
| Build a REAL House | Simulation | 26 j | 12 353 | nouveau |
| Steal A Balut | Simulation | 29 j | 11 305 | +2,2 % |
| Steal Eggs From Tsunami! | Simulation | 43 j | 9 976 | +12,9 % |

« Stop The Tsunami! » (35 j) : 26 621 de moyenne la veille, rang 66 du top 100 de RoStats. « Ragdoll Soccer » existe bien sous ce nom (créateur Ragdoll Athletics), contrairement à ce que conclut `v4-contexte.md`.

## Genres (page 5, instantané, joueurs « right now »)

| Genre | Joueurs | Jeux suivis | Joueurs par jeu (calculé) |
|---|---:|---:|---:|
| Simulation (Idle, Incremental Simulator, Physics Sim, Sandbox, Tycoon, Vehicle Sim) | 5 164 732 | 25 381 | 203 |
| Survival | 1 934 914 | 5 199 | 372 |
| Roleplay & Avatar Sim | 1 635 585 | 2 223 | 736 |
| Action | 1 308 358 | 3 324 | 394 |
| RPG | 691 862 | 875 | 791 |
| Obby & Platformer | 626 748 | 8 445 | 74 |
| Sports & Racing | 626 531 | 1 223 | 512 |
| Shooter | 500 137 | 1 310 | 382 |
| Party & Casual | 420 695 | 3 261 | 129 |
| Strategy | 369 790 | 962 | 384 |

La colonne « joueurs par jeu » est un **calcul** (joueurs ÷ jeux suivis), pas une médiane : la tête du classement en concentre l'essentiel (Steal An Egg, à lui seul, 564 000 à 739 000 joueurs au moment des lectures).

## Fiches de jeux (pages 8 et 9)

| Champ | Throw Food For Animals | Break and Steal an Egg |
|---|---|---|
| universeId / placeId | 10766972131 / 120219252362013 | 10765288803 / 114326934417838 |
| Genre affiché | Simulation · Tycoon | Simulation · Tycoon |
| Créé le | 2026-09-18 | 2026-09-05 |
| Taille de serveur | 5 | 7 |
| Moyenne 24 h / 7 jours | 399 352 / 261 253 | 99 841 / 91 736 |
| Pic | 2 474 602 (« 28 hours ago ») | 1 311 860 (il y a 28 jours) |
| Visites | 264 067 199 | 440 635 605 |
| Votes positifs | 94,2 % | 97,0 % |
| Durée de session (estimation du site) | 20 min | 19 min |
| Mises à jour sur 30 jours | 174 (environ 6 par jour) | 81 |
| Événements titrés | « New Map + Admin Abuse » (31/10, 07/11), « DREAMLAND EVENT » (14/11), « Halloween Update » (25/10) | « UPDATE + Admin Abuse » (18/10), « ADMIN ABUSE » (29/10), « MASSIVE UPDATE » (01/11), « UPDATE + Secret Gate » (08/11) |
| Action d'après la description (non joué) | Lancer de la nourriture le plus loin possible, attirer et collecter des animaux, gagner de l'argent grâce à eux, acheter une meilleure nourriture, s'entraîner pour la « Throw Power », débloquer des zones | Casser des œufs, faire éclore des animaux rares, les voler, échapper aux gardes, les poser dans sa base pour gagner de l'argent, améliorer vitesse et pioche, compléter l'Index |
| Revenus | NP (réservé aux abonnés du site ; de toute façon non public, règle M4) | NP |

## Prix relevés

| Jeu | Offre | Prix (Robux) | Type apparent | URL | Date |
|---|---|---:|---|---|---|
| Throw Food For Animals | Passe « x2 Cash » | 99 | multiplicateur de monnaie | https://rostats.io/games/10766972131 | 2026-11-15 |
| Throw Food For Animals | Passe « x2 Training Power » | 149 | multiplicateur de progression | idem | idem |
| Throw Food For Animals | 50 produits, de 2 à 12 000 ; premiers : « Throw Power Pack 1 » 2, « Super Lucky Throw » 9, « Server Luck 2x » 19, « Money Pack 1 » 24, « 5m of Training » 39 | 2 à 12 000 | monnaie, puissance, chance, temps | idem | idem |
| Break and Steal an Egg | Aucune passe ; 130 produits, de 1 à 6 299 ; premiers : « Pickaxe [Tier 1] » 3, « 2x Speed » 3, « Trail 1 » 3, « 4x Speed » 5, « Skip Speed Upgrade [Tier 1] » 9, « Skip Time [1] » 9 | 1 à 6 299 | puissance, vitesse, temps, apparence | https://rostats.io/games/10765288803 | 2026-11-15 |

## Instantané par l'API documentée (`OUTILS\instantane-univers.ps1`, 22:22:30 UTC)

| Jeu | universeId | CCU instantané | Créé le | Modifié le |
|---|---|---:|---|---|
| Throw Food For Animals | 10766972131 | 233 221 | 2026-09-18 | 2026-11-14 |
| Break and Steal an Egg | 10765288803 | 73 578 | 2026-09-05 | 2026-11-15 |
| Survive Your Ideas | 10769671316 | 56 546 | 2026-10-06 | 2026-11-15 |
| Brookhaven RP | 1686885941 | 372 915 | 2020-04-21 | 2026-11-14 |

Détail : `VEILLE\instantanes.csv`.

## Ce que je n'ai pas pu lire

- Roblox Charts : Top Playing Now, Top Trending, Up-and-Coming. Couverture des 40 rangs visés par la mission A : **0 %** sur la source prévue. Le classement mensuel de RoStats (25 premiers lus sur 25) le remplace pour l'ordre de grandeur, pas pour le classement du jour.
- Moyennes de novembre des jeux sortis du top 50 (+1 Stone Skipping, Climb For Animals Eggs) : seulement « sous 21 921 » (moyenne du rang 49).
- Liste des jeux en baisse : RoStats n'en publie pas sur les pages lues.
- Pages Roblox des jeux (description complète, vignettes, votes) : non tentées, même technique de rendu que les Charts.
- Conditions de RoWatcher : illisibles sans navigateur.

## Remarques

- La page 7 affiche 100 lignes ; le lecteur les a toutes rendues alors que 10 étaient attendues. Seules les lignes utiles sont reprises ici et dans le dossier de thème. La consigne au lecteur doit plafonner le nombre de lignes (corrigé dans la procédure 01).
- Les titres portent des emojis et des étiquettes de mise à jour ; ils sont simplifiés ici. Quelques séparations titre/créateur ont été déduites par le lecteur.
- Budget de recherches de la session : 15 recherches web faites par les trois veilleurs (2 + 3 + 10) pour un plafond de 10 par session. Le plafond n'avait pas été réparti entre veilleurs par l'orchestrateur : erreur d'orchestration, corrigée dans la procédure 01. Aucune recherche supplémentaire n'a été faite ensuite.

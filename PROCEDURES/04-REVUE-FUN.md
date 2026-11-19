# 04 — Revue du fun et de l'adéquation Roblox

**Qui** : Claude Opus 5.5, effort high. Un seul agent, qui n'a ni écrit la fiche ni produit le jeu (règle A2).
**But** : dire si ce jeu sera amusant dans la première minute et s'il ressemble à ce qui fonctionne sur Roblox, avant d'engager la production.

## Deux passes

| Passe | Quand | Pièces |
|---|---|---|
| **1. Papier** | Après la porte P2 | Fiche concept, simulation économique, tendances et dossier de thème |
| **2. Prototype** | À la porte P4, sur le prototype des 60 premières secondes | Le jeu en Play (lecture seule de la place), captures PC et format téléphone, console |

## Grille (chaque axe noté sur 10, avec sa preuve)

| Axe | Question | Ce qui fait une bonne note |
|---|---|---|
| 1. Première minute | Le joueur fait-il l'action promise en 60 s, sans lire ? | Scénario seconde par seconde crédible ; aucun menu avant l'action ; récompense immédiate |
| 2. Boucle courte | Refaire l'action dix fois est-il agréable ? | Retour visuel et sonore, variation, résultat visible qui grossit |
| 3. Progression visible | Voit-on à distance qu'un joueur est plus avancé ? | Chaque palier change une silhouette (F1) ; un objectif suivant toujours affiché (F2) |
| 4. Social | Y a-t-il une raison d'inviter un ami et une scène à raconter ? | Interaction dans le jeu, pas dans un menu ; scène montrable en vignette (F5) |
| 5. Adéquation Roblox | Colle-t-il au public et à la découverte ? | Jouable au pouce, session utile de 5 min, thème porté par la veille, promesse fidèle à la vignette, rien qui provoque un abandon avant 60 s |
| 6. Retour | Pourquoi revenir demain, et dans une semaine ? | Raison visible avant de partir (F6) ; contenu ou objectif à J7, pas seulement un cadeau de connexion |
| 7. Faisabilité | L'usine peut-elle le construire et le tenir à jour ? | Périmètre respecté (C4) ; coût de contenu soutenable ; pas de dépendance à un asset qu'on ne sait pas produire |

Pour l'axe 5, s'appuyer sur ce que Roblox dit de sa page d'accueil : il regarde l'abandon avant 60 s et entre 61 et 180 s, les jours joués, le temps par joueur, le jeu entre amis. Un jeu qui perd ses entrants dans la première minute n'est pas rattrapé par la publicité.

## Méthode

1. Lire les pièces, pas un résumé. Rejouer mentalement la première minute en notant chaque moment où un enfant de 10 ans sur téléphone décroche.
2. Comparer à 3 gagnants **et** 3 faibles du dossier de thème : qu'est-ce qui distingue ce jeu des faibles ?
3. Noter chaque axe avec une preuve : passage de la fiche, ligne de la simulation, capture (passe 2). Sans preuve : « non vérifiable », et la note ne dépasse pas 5.
4. Rendre un verdict : **GO**, **ITÉRER** (avec 3 à 5 corrections classées par impact) ou **REFUS** (avec la raison de fond).
5. Écrire les 5 scénarios de test que la QA devra rejouer pour confirmer ou infirmer ce jugement.

Passe 2 : jouer réellement le prototype en Play via le serveur MCP de Studio, sans écrire dans la place (pas de mode Edit, pas de `save_place`). Chronométrer la première action. Les notes de la passe 1 sont révisées à la lumière de ce qui est **vu**.

## Rapport

`JEUX\<slug>\04-fun\RAPPORT-FUN.md` (gabarit `OUTILS\GABARITS\RAPPORT-FUN.md`) : tableau des notes, verdict, corrections classées, scénarios pour la QA, limites de la revue (ce qui n'a pas pu être jugé).

## Porte P3

**Passe 1 (papier), depuis le bilan du cycle 2 (règle A9).** Le relecteur note toujours les 7 axes et dit pour chacun si la note est fondée sur ce qui est lu, plafonnée faute de preuve possible sur papier, ou abaissée par ce que la fiche écrit. La porte passe si :

- la moyenne des axes **vérifiables sur papier** atteint `fun.moyenne_verifiable_papier_min` (7,0) ;
- aucun axe n'est sous 5,0 ;
- la fiche porte un critère d'arrêt ferme et mesurable pour le prototype ;
- le relecteur a rejoué l'annexe A à partir du parcours détaillé (C10) et confronté le cadrage à tout ce que la fiche dit visible (C11).

Les axes non vérifiables sur papier (en général la boucle courte et le retour) ne sont pas comptés à 5 dans la moyenne : ils se jugent à la **passe 2**, sur le prototype, contre des mesures que le relecteur de la passe 1 écrit d'avance (mesure, seuil). L'axe « retour » ne dépasse 5 qu'en bêta (J1, session).

**Passe 2 (prototype, porte P4)** : moyenne des 7 axes ≥ 7,0, aucun axe sous 5,0, verdict GO, et toutes les mesures de l'arrêt ferme tenues.

ITÉRER : retour au concepteur avec le rapport, 2 retours au plus. REFUS ou troisième échec : idée abandonnée (A5).

Origine : trois revues indépendantes de `lave-la-tour` (5,7 ; 6,1 ; 6,4). Avec deux axes plafonnés à 5, l'ancienne règle exigeait 7,8 sur les cinq autres : aucune fiche ne pouvait passer, et le relecteur l'a écrit lui-même. `lave-la-tour` est resté en dérogation ; la règle vaut à partir du jeu suivant, « à calibrer ».

Un GO de complaisance coûte une production entière. En cas de doute entre GO et ITÉRER : ITÉRER.

## Mode dégradé (aucun relecteur indépendant disponible)

Constat du cycle 1 : quand les sous-agents Opus, Fable et Sonnet sont interdits ou au plafond, il ne reste pour relire que l'orchestrateur, qui a souvent écrit la fiche. Il peut rédiger la revue pour préparer le travail, mais elle ne vaut ni validation ni arrêt (règle A8) : `etat.ps1 -Porte P3 -Resultat a_confirmer`, le jeu reste à l'étape 04, et la revue se rejoue avec Opus 5.5 avant tout lot de production. Le rapport dit en tête que le relecteur est l'auteur.

À la passe papier, les axes 2 (boucle courte) et 6 (retour) ne se prouvent guère : ils restent notés (5 au plus) mais sortent de la moyenne de la passe 1 (voir « Porte P3 », règle A9).

## Prompt type (relecteur fun)

```
Tu es relecteur « fun et adéquation Roblox » de l'usine. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md, PROCEDURES\04-REVUE-FUN.md, CONNAISSANCES\REGLES.md (Fun, Concept) et CONNAISSANCES\LECONS-ARCHIPEL.md (Produit).
Passe : <1 papier | 2 prototype>. Pièces : JEUX\<slug>\02-concept\FICHE-CONCEPT.md, JEUX\<slug>\03-economie\SIMULATION.md, VEILLE\TENDANCES.md, <dossier de thème><, passe 2 : place <placeId> ouverte dans Studio, en Play uniquement>.
Tu n'as pas écrit cette fiche : juge-la sans chercher à la sauver. Note les 7 axes sur 10 avec une preuve chacun, rends GO, ITÉRER ou REFUS, classe les corrections par impact, écris 5 scénarios de test pour la QA.
Passe 2 : tu joues en Play, tu n'écris pas dans la place (ni mode Edit, ni save_place), tu chronomètres la première action.
Aucun sous-agent. Aucune modification de la fiche.
Sortie : JEUX\<slug>\04-fun\RAPPORT-FUN.md d'après OUTILS\GABARITS\RAPPORT-FUN.md.
Dernière ligne : RESULTAT: <ok|echec|arret> | <fichier> | <verdict, moyenne, axe le plus faible>.
```

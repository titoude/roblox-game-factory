# Revue du fun et de l'adéquation Roblox — Lave la tour (`lave-la-tour`), fiche v5

- Passe : 1 (papier), contre-vérification de la version 5. Troisième revue de la porte P3 (v3 : 5,7 ; v4 : 6,1). Entrées figées au commit `bf4e35f`, lues par `git show bf4e35f:<chemin>`.
- Relecteur : Claude Opus 5.5, effort high, le 2026-11-16. Je n'ai écrit ni la fiche (v5 : Fable 5.2), ni le code, ni les revues précédentes. Règle A2 tenue.
- Pièces : `02-concept\FICHE-CONCEPT.md` (v5), `03-economie\SIMULATION.md`, `VEILLE\TENDANCES.md`, `VEILLE\RELEVES\2026-11-15\b1-theme-un-geste.md`, `04-fun\RAPPORT-FUN-V4.md` (lu pour ses demandes ; il ne me lie pas), `GARDE-FOUS.md`, `PROCEDURES\04-REVUE-FUN.md`, `CONNAISSANCES\REGLES.md`, `CONNAISSANCES\LECONS-ARCHIPEL.md`, `CONNAISSANCES\seuils.json` (§ `fun`), `ETAT.json`. Aucune recherche web, aucun jeu joué, ni Studio ni navigateur.
- Hors de mon périmètre : la justesse des chiffres d'économie (contre-vérification en parallèle). Je ne juge que ce qu'ils font au jeu.
- Références : `l.N` = ligne N de la fiche v5 au commit `bf4e35f`. « Calcul » = déduit par moi des lignes citées.

## Verdict

**ITÉRER** — moyenne **6,4/10** (45/70). Axes les plus faibles : **boucle courte (5)** et **retour (5)**, plafonnés faute de preuve possible sur papier. Parmi les axes vérifiables, le plus faible est la **progression visible (6)**, abaissée par ce que la v5 écrit sur la caméra. Moyenne des cinq axes vérifiables : **7,0**.

Porte P3 (`seuils.json` § `fun` : moyenne ≥ 7,0, aucun axe sous 5,0, verdict GO) : **non passée**. Aucun axe sous 5. Pas de REFUS : aucun défaut de fond ; ce qui reste est de la spécification, corrigeable en quelques phrases.

Comptage, tel que les textes l'écrivent : c'est la **troisième** revue de P3 sans GO. La procédure 04 (« REFUS ou troisième échec : idée abandonnée »), `fun.iterations_max = 2` et la règle A5 mènent tous à l'abandon, sauf dérogation écrite (A4). Cette décision revient à l'orchestrateur (section dédiée plus bas).

Progression : 5,7 → 6,1 → 6,4. Les axes vérifiables passent de 6,6 à 7,0. La v5 a fait les corrections demandées pour de vrai, mais la correction 2 (caméra tenue) a ouvert une contradiction neuve avec trois promesses de la fiche (les robots « sous les yeux », les autres tours visibles depuis la nacelle, le chemin social entre inconnus).

## 1. Les cinq corrections demandées à la v4 : réelles, partielles ou affirmées

| Correction (revue v4) | Ce que la v5 écrit dans le corps | Statut | Cohérence interne |
|---|---|---|---|
| 1. Montée monotone | Une seule façade de 5 vitres, 5 vitres = 1 étage, « Aucun angle, aucune descente » (l.87) ; compteur « Étage 7 / 120 » (l.85) ; M07 : rangées finies de bas en haut + masque de 5 bits (l.188) ; annexe A recalculée (l.267–281) ; prévision « 12 étages entre 61 et 180 s » (l.300) | **Réelle** | Calcul : vitre k finie à 4 + 2k s. 5ᵉ vitre à 14 s (2ᵉ étage), 10ᵉ à 24 s, 20ᵉ à 44 s (5ᵉ étage), 25ᵉ à 54 s, 28 vitres à 60 s, 30ᵉ à 64 s (7ᵉ), 60ᵉ à 124 s (13ᵉ), 85ᵉ à 174 s (18ᵉ) : l'annexe A et l'annexe C sont cohérentes avec le parcours. Deux réserves. (a) « Le compteur ne baisse jamais » (l.9, l.85) est faux au déménagement : la nouvelle tour sort « entièrement sale » (l.154), le compteur passe d'environ « Étage 93 / 120 » à « Étage 1 / 280 » (calcul : 466,5 vitres lavées en tour 1, l.147). Le reset est choisi et mis en scène, il est défendable ; l'affirmation, non. (b) « Sans exception » (l.281) suppose que les cinq achats de 61 à 180 s ne coûtent aucun temps de geste ; un toucher sur le bouton d'achat en coûte un peu. La marge reste large (12 étages prévus) |
| 2. Geste protégé de la caméra tactile | Caméra tenue, vitre au centre, ≥ 40 % de la largeur ; un toucher commencé sur la vitre ne fait jamais tourner la vue ; joystick et saut masqués ; boutons hors de la vitre et hors des pouces ; « Descendre » et « Monter » (l.89) ; « la caméra ne bouge pas » (l.271) ; définition d'une passe (l.182) ; arrêt si la caméra tourne (l.324) | **Réelle** pour le geste | **A cassé trois promesses de la même fiche.** Une caméra qui regarde la façade du joueur, vitre à 40 % de l'écran, a la place et les autres tours **dans le dos** (les tours entourent la place et chaque joueur lave « la façade qui regarde la place », l.87, l.195) et ne montre aucune des trois autres façades. Donc : « Les robots lavent sous les yeux du joueur les trois autres façades » (l.83) est impossible ; « en face, les tours des autres » (l.275) aussi ; et « toucher la seconde place éclairée d'une tour voisine, visible depuis sa propre nacelle » (l.197) n'est pas faisable. Voir § 2 |
| 3. Méta allégée | Beffroi, fanions et cloches supprimés (l.12) ; contrat du jour sur la parcelle du joueur, sans visiteur (l.174) ; trophée remplacé par une plaque (l.154) ; annexe B : 4 tours, contrat = façade de la boucle principale (l.288) | **Réelle** | Plus de rendu par joueur sur un objet partagé. Reste une méta à cinq pièces (tours, déménagement, Flèche et record, contrat quotidien, pigeons), mais chacune est écrite et attachée à la parcelle du joueur |
| 4 a. Mousse visible après le quota | « Quota atteint : le +25 % s'arrête, la mousse reste à l'écran » + petit texte (l.187) | **Réelle** | Cohérent avec l.176 et l.198 |
| 4 b. Chemin pour rejoindre | Bouton « Rejoindre <ami> » 5 s après l'arrivée, un toucher, assis à côté (l.197) | **Partielle** | Vrai pour les amis Roblox (test v4 : 2 touchers, 15 s : tenu, calcul ≈ 6 à 8 s). Trous : (a) les deux amis voient chacun « Rejoindre » l'un vers l'autre, rien ne dit qui rejoint qui si les deux touchent ; (b) le bouton tombe à 5 s, en plein « Frotte ! » (l.271), et un nouveau joueur qui le touche saute sa première minute ; (c) le chemin des non-amis passe par une vue que la caméra interdit (ci-dessus) |
| 4 c. « Chez <visiteur> ! » | Proposé aux deux quand la tour devient étincelante avec un visiteur à bord, avant les pigeons (l.155, l.199) | **Réelle** | Cohérent avec le quota de pigeons et avec « on s'aide à tour de rôle ». Calcul : un duo lave 60 vitres par minute et finit la tour 1 vers 10 min ; la proposition arrive au bon moment |
| 5. Ce qu'on voit tient la promesse | Robots qui lavent les trois autres façades jusqu'à la hauteur de la nacelle, « décor, sans stock ni crédit » (l.83, l.188) ; scène de vignette à 5 min, 30ᵉ étage, sans coucher de soleil ni nuages (l.201) | **Réelle** pour la vignette, **partielle** pour les robots | Vignette atteignable : calcul, solo 30ᵉ étage vers 4:54, duo vers 2:30 à 3:00. Robots : plus aucun robot sur du verre sale, c'est tenu. Mais la hauteur lavée par les robots suit la nacelle, pas le nombre de robots : un ou cent robots lavent autant ; rien ne dit l'état des trois façades avant le premier robot (0 à 25 s) ni pendant un contrat ou une visite. Et le joueur ne les voit pas travailler (caméra) |

Le résumé de tête (l.9–13) décrit fidèlement les corrections, à deux exceptions près : « ne baisse jamais » (faux au déménagement) et « sous les yeux » (contredit par la caméra).

## 2. Ce que la v5 a cassé, alourdi ou laissé incohérent

1. **Caméra tenue contre visibilité (le défaut principal de la v5).** Voir le tableau. Conséquences : le joueur ne voit pas ses achats travailler (axe 2 : « résultat visible qui grossit »), ne voit jamais les autres joueurs pendant qu'il lave (axe 3 : « voit-on à distance… »), et un inconnu ne peut pas trouver une seconde place libre (axe 4). Sur un serveur de 6, chacun est assis seul face à son mur. Correction bon marché : cadrer de biais (correction A plus bas).
2. **Joueur assis en permanence.** Apparition assis (l.271), joystick masqué (l.89), contrat et visite par bouton et vol de caméra (l.174, l.197). La place centrale (l.195) n'a plus de rôle pendant le jeu ; « s'approcher d'une nacelle propose Monter » (l.89) ne dit pas comment on approche une nacelle restée au 90ᵉ étage. C'est la forme des jeux de clic, qui existent sur Roblox ; le risque n'est pas l'ennui de l'avatar, c'est la disparition de la rencontre entre inconnus.
3. **Une seule façade et des tours de 120 à 400 étages.** Hauteurs écrites : 600, 1 400 et 2 000 unités (l.228) pour une façade de 5 vitres. Si une vitre est à peu près carrée (la largeur n'est pas écrite), la tour 3 est 80 fois plus haute que large : une aiguille. Lisible de loin comme hauteur, mais à 2 000 unités le rendu, le brouillard et la lecture « qui est plus avancé » sur téléphone sont renvoyés au lot L7 (l.228). Calcul : en solo, un joueur quitte la tour 1 vers l'étage 93/120, la tour 2 vers 212/280, et finit le contenu vers l'étage 278/400 de la tour 3 (l.147–149). Le sommet promis (« monte jusqu'au sommet », l.64) n'est atteint que si le joueur retarde le déménagement ; rien n'invite à le faire.
4. **La Flèche part-elle du sol ?** « Quatrième tour, sans fin … il sort du sommet » (l.160) ne dit pas si la Flèche est posée sur la tour 3 ou repart du sol. Si elle repart du sol, l'objectif à J7 commence par une chute de ~278 étages à 40 (calcul), et il faut ~7 segments, environ 50 minutes, pour retrouver sa hauteur. Hors L0, à trancher avant la production.
5. **Plus de trophée ni de beffroi.** Bon pour C4 et l'axe 7. La plaque (l.154) est un panneau : elle ne vaut rien pour F1, mais la hauteur et la taille de la tour suffisent.
6. **« Chez <visiteur> ! ».** Bien écrit. Il ne dit pas quoi faire si la tour du visiteur est elle aussi étincelante (rare : le visiteur n'a pas avancé).
7. **Lisibilité au téléphone.** Visibles depuis la nacelle, d'après la fiche : pièces, « Étage n / N », objectif, bouton d'achat (l.85, l.89), « Descendre » (l.89), « Contrat du jour » et son compte à rebours (l.174), réservoir (l.172), « Rejoindre <ami> » (l.197), « Déménager » (l.154), texte du quota de mousse (l.187), compte à rebours des pigeons (l.155). Jusqu'à 8 éléments en même temps autour d'une vitre qui prend 40 % de la largeur, plus la barre de Roblox. Archipel s'est cassé exactement ainsi (LECONS Produit 5). Aucun plan d'écran n'est écrit.
8. **Reste d'une version précédente.** « La seconde place de la nacelle s'éclaire si un autre joueur est proche » (l.274) : personne ne marche, « proche » ne veut plus rien dire (texte hérité de la v4, l.254 de la v4).
9. **Périmètre C4.** Tenu, plus nettement qu'en v4 : une boucle, une seconde place, une suite de tours. Le contrat reste un petit système (lieu, cycle, bouton, compte à rebours, trajet de caméra) que l'annexe B range dans la boucle principale ; je l'accepte.
10. **Coût de contenu.** En baisse : 7 sons (de 6 à 9 en v4), ~75 chaînes, beffroi et ses objets retirés (l.224–226). En hausse : des robots animés sur trois façades de six tours, synchronisés avec la nacelle de chacun ; des vols de caméra (rejoindre, contrat) ; une caméra et une saisie tactile sur mesure. Tout cela se fait en pièces simples et en script.
11. **Laissé tel quel depuis la v3 (pour mémoire).** La passe « Raclette motorisée » lave à 30 vitres par minute (l.214), soit exactement le rythme actif : elle fait monter la tour sans geste. C'est du confort non compétitif (l.210), donc pas un défaut G6 ; mais c'est le seul verbe du jeu qu'on vend en automatique. À regarder en passe 2 : un joueur qui l'a achetée a-t-il encore envie de frotter ?

## Notes

Sans preuve, la note ne dépasse pas 5. Mode : vu, lu, non vérifiable. Nature : **(a)** fondée sur ce qui est lu ; **(b)** plafonnée faute de preuve possible sur papier ; **(c)** abaissée par ce que la fiche écrit.

| Axe | Note /10 | Preuve | Mode | Nature |
|---|---|---|---|---|
| 1. Première minute | 8 | Annexe A cohérente avec le parcours (calcul au § 1) : apparition assis face à une vitre lavable, « Frotte ! », premier geste à 4 s, première montée à 14 s, 28 vitres et nacelle au 6ᵉ étage à 60 s (l.271–275), aucun menu, texte le plus long de 4 mots (l.277). La réserve de la v4 (caméra) est levée (l.89, l.271). Moins : le bouton « Rejoindre <ami> » à 5 s en concurrence avec « Frotte ! » pour le joueur invité (l.197) ; les achats ne sont pas comptés dans le rythme ; le premier robot acheté à 25 s « se met à laver la façade de gauche » (l.273), hors du cadre | lu | (a) |
| 2. Boucle courte | 5 | Spécifié : traînée en moins de 150 ms, trois passes, note montante sur 8 crans, rideau d'eau, fanfare tous les 10 étages (l.91), vitres d'aspect différent à place fixe (8ᵉ fiente, 17ᵉ buée, l.93), passe définie (l.182), vitre qui reste propre (l.188). Le plaisir ne se lit pas. La variation est purement visuelle (tache tenace supprimée, l.18), sans adresse demandée, à ~90 touchers par minute pendant tout le contenu (calcul : 30 vitres × 3 passes). Le joueur ne voit pas ses robots travailler (§ 2.1) | lu ; plaisir non vérifiable | (b) |
| 3. Progression visible | 6 | Pour : montée monotone dans une tour (l.87), dix paliers à silhouette propre (l.97–104), anneau propre sur les quatre faces grâce aux robots (l.83), trois tours de tailles différentes, objectif suivant toujours affiché (l.85, F2). Contre : la caméra tenue cache au joueur les autres tours et ses propres robots, pendant presque tout le temps de jeu (l.89 contre l.82, l.83, l.275) ; le compteur retombe à 1 au déménagement (l.154) malgré l.9 ; la Flèche peut repartir du sol (l.160) ; à 2 000 unités, lecture à vérifier au L7 (l.228) | lu | (a), abaissée par (c) |
| 4. Social | 7 | Seconde place utile, nacelle deux fois plus rapide, mousse visible même au quota (l.187, l.196), pourboire plafonné (l.198), chemin d'ami en un toucher (l.197), « Chez <visiteur> ! » contre la boucle de pigeons (l.155, l.199), scène de vignette atteignable vers 5 min (l.201, F5). Les six « contre » de la v4 sont traités. Contre neufs : chemin des non-amis infaisable avec la caméra écrite ; conflit si deux amis touchent « Rejoindre » ensemble ; serveur de 6 sans rencontre possible entre inconnus | lu | (a), avec réserve |
| 5. Adéquation Roblox | 7 | Verbe porté par la veille (Sweep The Moon +489 % sur la semaine, Clean The Ballpit! +172 % sur 24 h, `b1-theme-un-geste.md`), titre au moule du genre (« Wash The Tower », l.22), geste au pouce protégé (l.89), promesse tenue de 61 à 180 s (12 étages, l.281), session utile de 5 min (contrat vers 4:41, SIM), vignette fidèle et atteignable (l.201). Contre : HUD téléphone sans plan pour 8 éléments (§ 2.7) ; Sweep The Moon a l'antériorité du verbe ; le corpus montre que les gagnants changent le geste, et nous gardons le verbe en changeant l'axe | lu | (a) |
| 6. Retour (J1, J7) | 5 | J1 : réservoir « 2 h à 50 % » affiché (l.172), compte à rebours du contrat visible depuis la nacelle (l.174, F6), tour enregistrée vitre par vitre (l.188). J7 : la Flèche seule, que le geste fait pousser, avec record et balise (l.160–167), ouverte au jour 3 ou 4 pour une demi-heure par jour (l.314). La rétention ne se lit pas ; le départ de la Flèche (sol ou toit) n'est pas écrit | lu ; rétention non vérifiable | (b) |
| 7. Faisabilité pour l'usine | 7 | Méta allégée comme demandé (l.12), contenu par répétition d'un module d'étage, objets en pièces simples, sons 7, chaînes ~75, pièces bornées à 1 500 par client (l.224–227), C4 tenu (annexe B). Moins : robots animés sur trois façades de six tours, caméra et saisie tactile sur mesure, rendu à 2 000 unités renvoyé au L7. L'univers TEST n'existe pas encore (`ETAT.json`, blocage) : c'est un frein au calendrier, pas à la conception | lu | (a) |
| **Moyenne** | **6,4** | 45 / 7 = 6,43. Axes vérifiables (1, 3, 4, 5, 7) : 35 / 5 = **7,0** | | |

## Où un joueur de 10 ans sur téléphone décroche

| Moment | Ce qui se passe | Pourquoi il part |
|---|---|---|
| 0–6 s | Assis, caméra fixe, main fantôme, « Frotte ! » | Rien sur papier, si la saisie tactile tient ce que dit l.89 |
| 5 s, joueur venu avec un ami | « Rejoindre <ami> » apparaît pendant « Frotte ! » | Deux appels à la fois ; s'il touche le bouton, il quitte sa tour avant sa première vitre |
| 25–56 s | Il achète trois robots ; ils lavent « la façade de gauche », hors du cadre | « J'ai acheté quoi ? » : le bouton se vide, rien ne bouge à l'écran |
| 2–15 min | ~90 touchers par minute, toujours le même mur, la ville sous lui | Fatigue du pouce possible ; non vérifiable sur papier |
| Seul sur un serveur de 6 | Ne voit aucun autre joueur pendant qu'il lave | Aucune rencontre, aucune envie d'aller voir « la tour qui brille » |
| ~16 min | « Tour 2 prête — Déménager » ; après la scène, « Étage 1 / 280 » | « Je recommence ? » : atténué par la scène et la tour plus haute |

## Comparaison au corpus

Corpus de `b1-theme-un-geste.md`. Aucun jeu n'a été joué.

| Jeu | Gagnant ou faible | Ce qui nous en rapproche | Ce qui nous en distingue |
|---|---|---|---|
| Cut a Rock | Gagnant (+1 824 % sur le mois) | Un geste qui transforme l'objet pour de bon, et la transformation est le progrès | Chez nous, la hauteur porte le progrès et ne recule plus dans une tour |
| Depth Incremental | Gagnant (+598,8 %) | Une distance verticale qui ne fait qu'avancer, comme notre montée désormais | Son « record » ne repart pas de zéro ; nos déménagements, si |
| Sweep The Moon | Gagnant (+489 % sur la semaine) | Même verbe, robots qui nettoient pour de vrai | Façade verticale ; il a l'antériorité |
| Throw Lucky Block For Animals | Faible (1 073 sur 24 h) | — | Nous ne reprenons pas tel quel le geste d'un gagnant |
| Sell Fries! | Faible (−21,6 %) | Tâche de service répétée, tycoon calme | Silhouettes et hauteur ; le risque de corvée reste tant que le geste n'est pas joué |
| +1 Speed Keyboard Escape | Faible (retombé en deux mois) | Geste de mode | Un objectif à J7 (la Flèche) |

## Corrections demandées, par impact

Les corrections A à D sont à écrire **avant le L0** ; E à G avant le premier lot de production (L1). Formes directement applicables :

**A. Cadrer la caméra de biais** (axes 2, 3, 4). Au § 3 « Caméra et commandes » (l.89), remplacer « la vitre en cours est au centre et occupe au moins 40 % de la largeur d'un écran de téléphone, avec ses voisines et la ville en dessous. » par : « La caméra est placée de biais, à environ 35° de la façade et un peu au-dessus de la nacelle : la vitre en cours est au centre et occupe au moins 40 % de la largeur d'un écran de téléphone ; l'arête de la tour, la façade voisine où travaillent les robots et la ville en dessous sont dans le cadre. À chaque achat de robot et à chaque fanfare des 10 étages, la caméra recule 2 secondes pour montrer la tour entière et ce qui vient d'arriver, puis revient ; jamais pendant un glissement. » Puis, au § 3 (l.83), remplacer « sous les yeux du joueur » par « dans le cadre de la caméra (façade voisine) » ; à l'annexe A (l.275), remplacer « en face, les tours des autres » par « sur le côté, la façade voisine et ses robots ». *Test* : capture téléphone à 60 s, au moins un robot visible au travail et la vitre ≥ 40 % de la largeur.

**B. Rejoindre sans conflit ni concurrence avec la première minute** (axes 1, 4). Au § 4 (l.197), remplacer « Quand un ami Roblox du joueur est sur le serveur, un bouton « Rejoindre <ami> » apparaît dans sa nacelle 5 secondes après son arrivée » par « Quand un ami Roblox est déjà sur le serveur, le bouton « Rejoindre <ami> » n'apparaît que chez le joueur arrivé en dernier, après sa première rangée (vers 14 s), et seulement si la seconde place de l'ami est libre ; le serveur prend le premier appui, et le bouton disparaît chez les deux ». Remplacer « Pour les autres joueurs : toucher la seconde place éclairée d'une tour voisine, visible depuis sa propre nacelle, propose « Monter à bord ». » par « Pour les autres joueurs : au pied de chaque tour, une borne s'éclaire quand la seconde place est libre ; après « Descendre », s'en approcher sur la place propose « Monter à bord ». » À l'annexe A (l.274), remplacer « La seconde place de la nacelle s'éclaire si un autre joueur est proche » par « La seconde place de sa nacelle est éclairée : elle est libre ». *Test* : B, ami de A, assis à côté de A en 2 touchers au plus et 20 s au plus après son apparition, après avoir lavé sa première rangée.

**C. Arrêt ferme et mesuré** (décision). Remplacer l'annexe D 2 bis (l.324) par : « 2 bis. Arrêt ferme au prototype (porte P4), condition de la dérogation de P3. L'idée est abandonnée sans nouvelle itération si l'une de ces mesures échoue, au format téléphone : (1) latence contact → traînée de plus de 150 ms sur plus d'une vitre sur 20 ; (2) une rotation de caméra pendant 20 glissés commencés sur la vitre ; (3) moins de 25 vitres lavées à 60 s ou première montée après 20 s, par le relecteur sans aide ; (4) moins de 8 étages nouveaux entre 61 et 180 s, ou une baisse du compteur ; (5) plaisir du geste noté sous 6 par le relecteur de la passe 2, raisons écrites, ou sous 6 par le propriétaire après 3 minutes de jeu. Le seuil n'est pas révisé après la mesure. » (Le texte actuel arrête sur « aucun étage » alors que la fiche en prévoit 12 : un prototype à un seul étage passerait.)

**D. Écrire le périmètre du L0.** Ajouter à l'annexe B, après l.289 : « Prototype L0 (porte P4) : 0 à 180 secondes, tour 1, robots r1 et r2, raclette large, caméra et saisie tactile, une seconde place jouée à 2 clients. Ni contrat, ni Flèche, ni pigeons, ni déménagement, ni offres. »

**E. Compteur et Flèche** (axes 3, 6 ; hors L0). Remplacer « qui ne baisse jamais » (l.85) par « qui ne baisse jamais dans une même tour ; au déménagement, il repart de 1 sur une tour plus haute ». Au § 3 bis (l.160), écrire où naît la Flèche ; option recommandée : « La Flèche se construit sur le toit de la tour 3 : à son ouverture, les robots finissent la tour 3 sous les yeux du joueur (aucune pièce créditée), la nacelle monte au toit, et le premier segment commence au 401ᵉ étage. » Sinon, assumer par écrit le départ du sol.

**F. Plan d'écran téléphone** (axe 5 ; hors L0). Au § 3, lister les éléments visibles depuis la nacelle avec leur place et leur priorité (un seul bouton contextuel à la fois parmi « Déménager », « Contrat du jour », « Rejoindre »), et l'état de l'écran à 0 s, 60 s, 5 min et 20 min.

**G. Robots et hauteur** (axe 3 ; hors L0). Au § 3 ter M07 (l.188), écrire l'état des trois autres façades avant le premier robot, et pendant un contrat ou une visite ; et la largeur d'une façade, pour fixer les proportions des tours.

## Scénarios à rejouer par la QA

1. **Premier contact, téléphone, nouveau compte, sans lire.** Chronométrer le premier geste et la première vitre (prévision : 4 s et 6 s ; seuil 60 s). Vingt vitres glissées comme le montre la main fantôme : 20 validées, 0 rotation de caméra, latence contact → traînée ≤ 150 ms mesurée (journal horodaté sous `RunService:IsStudio()`). Vingt touchers commencés hors de la vitre : la caméra ne tourne pas non plus.
2. **Solo de 0 à 180 s, relevé toutes les 5 s** de l'étage affiché : 0 baisse, au moins 8 étages nouveaux entre 61 et 180 s (prévision 12), aucun trou de plus de 10 s sans événement visible. Capture à 60 s : vitre ≥ 40 % de la largeur, au moins un robot visible au travail, aucun bouton sur la vitre ni sous les pouces (Q4, 48 px).
3. **Deux clients amis.** B apparaît après A : B est assis à côté de A en 2 touchers et 20 s au plus. Les deux touchent « Rejoindre » en même temps : un seul déplacement, aucun état cassé. Mousse visible ; étages par minute du duo contre un joueur seul (attendu × 2). Quota de mousse forcé : mousse encore visible, texte du quota affiché. Tour de A rendue étincelante : « Chez B ! » proposé avant le compte à rebours des pigeons.
4. **Lisibilité, PC 1920 × 1080 et téléphone (Q8).** Six tours posées par action de test à des avancements différents. Depuis la place, puis depuis une nacelle : le testeur classe les joueurs par avancement sans lire, et trouve une seconde place libre d'un inconnu.
5. **Le propre reste propre.** Laver 37 vitres, quitter en pleine rangée, revenir : même vitre, même masque, aucune vitre resalie (Q5). Trois minutes sans vider le stock : 0 vitre lavée redevenue sale.

## Pour la décision de l'orchestrateur

Cette section ne change ni mes notes ni mon verdict.

**Les trois conditions de la revue v4.**

| Condition | Remplie par la v5 ? | Preuve |
|---|---|---|
| (a) La v5 écrit les corrections 1, 2 et 4 a | **Oui.** 1 réelle (l.87, annexe A cohérente) ; 2 réelle pour le geste (l.89), mais elle a créé la contradiction du § 2.1, à fermer par la correction A ; 4 a réelle (l.187) | § 1 |
| (b) Dérogation écrite | Relève de l'orchestrateur (`ETAT.json`, règle A4). La fiche la présuppose déjà (« condition de la dérogation de P3 », l.324) | — |
| (c) Arrêt ferme et écrit d'avance | **Ferme, oui** (« abandonnée sans nouvelle itération », l.324). **Mesurable, en partie** : la rotation de caméra et « aucun étage » se mesurent, la note de plaisir est un jugement écrit. **Trop lâche** : « aucun étage entre 61 et 180 s » laisse passer un prototype à 1 étage pour 12 prévus ; ni latence, ni rythme, ni première montée n'y figurent. Correction C | l.324 |

**Mon avis : engager le prototype L0 sous dérogation, sans parler de GO, après avoir écrit A, B, C et D.** Ce n'est pas un avis pour sauver le jeu ; c'est l'option qui coûte le moins pour savoir.

Pourquoi pas une itération de plus sur papier : elle ne peut pas ouvrir P3. Avec 5 aux axes 2 et 6, il faut 7,8 de moyenne sur les cinq autres ; les corrections A à G les porteraient vers 7,4 (calcul : axe 3 à 7, axe 4 à 8), soit 6,7 au total. Une quatrième fiche coûterait une revue et une contre-vérification d'économie pour un verdict connu d'avance.

Pourquoi pas l'abandon, bien qu'il se défende (A5 et procédure 04 à la lettre ; troisième dérogation sur ce jeu après P0 et P2 ; verbe déjà porté par Sweep The Moon) :
1. Les axes vérifiables atteignent 7,0, et ce qui manque ne relève pas du fond.
2. Ce qui reste inconnu (plaisir du geste, rythme réel, caméra au doigt) est justement ce que mesure un L0 étroit : une façade, une nacelle, deux robots, deux clients.
3. L'usine n'a encore rien joué : un premier prototype calibre aussi la grille (procédure 04, mode dégradé, dernier paragraphe) et la passe 2, qui n'ont jamais servi.
4. Avec l'arrêt C, le pire cas coûte un lot L0 et donne une leçon mesurée. Sans l'arrêt C, je changerais d'avis : un prototype sans seuil ferme est un GO de complaisance différé.

Réserve de calendrier : `ETAT.json` est bloqué sur l'univers TEST du propriétaire ; le L0 n'est peut-être pas lançable tout de suite, quelle que soit la décision.

**Mesures de la passe 2 sur le prototype** (liste de la v4, confirmée et corrigée).

*Axe 2 — boucle courte*, au format téléphone et en PC plein écran, toutes requises pour dépasser 5 :

| Mesure | Seuil | Changement depuis la v4 |
|---|---|---|
| Latence contact → traînée visible | ≤ 150 ms sur 20 vitres sur 20 (F3) | inchangé |
| Glisser et tapoter | 10 sur 10 pour chaque geste ; 0 rotation de caméra, y compris pour les touchers commencés hors de la vitre ; joystick et saut absents en capture | précisé |
| Rythme réel du relecteur, sans aide | ≥ 25 vitres à 60 s (fiche : 28) ; première montée ≤ 20 s (fiche : 14 s) | inchangé |
| Montée de 61 à 180 s | ≥ 8 étages nouveaux (fiche : 12), 0 baisse du compteur | **ajouté** (mesurable depuis la façade unique) |
| Retours distincts dans la minute | ≥ 4 parmi : traînée, éclat et pièce volante, note qui monte, rideau d'eau et montée, vitre d'aspect différent ; la fiente (8ᵉ vitre, ~20 s) et la buée (17ᵉ, ~38 s) vues avant 45 s | précisé (places fixes, l.93) |
| Robots visibles | au moins un robot acheté visible au travail dans le cadre à 60 s | **ajouté** (correction A) |
| Sons | note montante sur 8 crans vérifiée dans le journal ; aucun son répété plus de 3 s sans variation | inchangé |
| Fluidité | ≥ 30 images par seconde au téléphone pendant la traînée (`qa.fps_min_telephone`) | inchangé |
| Résultat durable | 0 vitre lavée redevenue sale en 3 min | inchangé |
| Jugement | plaisir du geste ≥ 7 par le relecteur après 3 min, raisons écrites ; sans test par un humain (propriétaire ou enfant), pas plus de 7 | inchangé |

*Axe 4 — social*, au L0 à 2 clients : chemin d'ami (≤ 2 touchers, ≤ 20 s), appui simultané sans conflit, duo × 2, mousse visible au quota. **Ajouté** : la v5 rend ce chemin mesurable dès le L0.

*Axe 6 — retour* : inchangé. Aucune mesure d'un prototype de 60 s ne justifie 7. Le L0 montre seulement que l'axe ne tombe pas sous 5 (sauvegarde fidèle, scénario 5 ; raison de revenir visible depuis la nacelle). Le 7 se gagne en bêta : J1 ≥ 8 % sur 200 joueurs organiques, session médiane ≥ 8 min (`seuils.json` § `beta`) ; repère proposé, non écrit en seuil : J7 ≥ 1,6 %.

*Retiré du L0* : la lisibilité à 2 000 unités et les six tours (lot L7).

## Limites de cette revue

- Passe papier : rien n'est vu. Le plaisir du geste (axe 2) et la rétention (axe 6) ne se prouvent qu'en Play puis en bêta.
- La contradiction caméra contre visibilité (§ 2.1) est un raisonnement géométrique sur la disposition écrite (tours autour de la place, façade lavée face à la place, vitre à 40 % de l'écran). Une autre disposition, non écrite, pourrait l'éviter : c'est la raison de la correction A.
- Les horaires (étages à 64, 124, 174 s ; étage 93 en fin de tour 1 ; vignette vers 4:54 en solo) sont des **calculs** à partir des lignes citées et de 2 s par vitre.
- Je n'ai pas jugé l'économie. Les corrections E (Flèche sur le toit) et B (bouton après la première rangée) peuvent la toucher à la marge et demandent un regard de la contre-vérification.
- Le corpus n'a pas été joué ; la veille est en dérogation (P0).

Passe 2 seulement — première action chronométrée : sans objet (passe 1). Erreurs console : sans objet.

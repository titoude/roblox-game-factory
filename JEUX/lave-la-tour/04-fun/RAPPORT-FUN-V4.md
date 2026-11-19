# Revue du fun et de l'adéquation Roblox — Lave la tour (`lave-la-tour`), fiche v4

- Passe : 1 (papier). Itération 2 sur 2 de la porte P3. Entrées figées au commit `4e98dca`, lues par `git show 4e98dca:<chemin>`.
- Relecteur : Claude Opus 5.5, effort high, le 2026-11-16. Je n'ai écrit ni la fiche (v4 : Fable 5.2, joué par l'orchestrateur), ni le code, ni la revue précédente. Règle A2 tenue (concepteur Fable, relecteur Opus).
- Pièces : `02-concept\FICHE-CONCEPT.md` (v4), `03-economie\SIMULATION.md`, `VEILLE\TENDANCES.md`, `VEILLE\IDEES-CANDIDATES.md`, `VEILLE\RELEVES\2026-11-15\b1-theme-un-geste.md`, `04-fun\RAPPORT-FUN-INDEPENDANT.md` (revue de la v3, lue pour ses demandes, elle ne me lie pas), `CONNAISSANCES\REGLES.md`, `CONNAISSANCES\LECONS-ARCHIPEL.md`, `PROCEDURES\04-REVUE-FUN.md`, `CONNAISSANCES\seuils.json`. Aucune recherche web, aucun jeu joué, ni Studio ni navigateur.
- Hors de mon périmètre : la justesse des chiffres d'économie (contre-vérification en parallèle). Je ne juge que ce qu'ils font au jeu.
- Références : `FICHE l.N` = ligne N de la fiche au commit `4e98dca` ; `SIM` = `SIMULATION.md` au même commit.

## Verdict

**ITÉRER** — moyenne **6,1/10** (43/70). Axes les plus faibles : **boucle courte (5)** et **retour (5)**, plafonnés faute de preuve possible sur papier. Parmi les axes vérifiables, les plus faibles sont social, adéquation Roblox et faisabilité (6 chacun).

Porte P3 (`seuils.json` § `fun`) : **non passée**. La moyenne de 7,0 n'est pas atteinte et le verdict n'est pas GO ; aucun axe n'est sous 5,0. Pas de REFUS : aucun défaut de fond. Ce qui manque relève de la spécification (parcours de la nacelle, geste au doigt sur téléphone, méta trop chargée) et se corrige sur papier.

Progression depuis la v3 : 5,7 → 6,1. Les deux axes qui étaient sous le plancher (boucle courte, retour : 4) remontent jusqu'au plafond de 5, parce que ce que la v3 écrivait contre eux a disparu.

**Comptage des échecs (à trancher par l'orchestrateur, pas par moi).** C'est le deuxième échec de P3. `seuils.json` (`fun.iterations_max = 2`) et la règle A5 (« deux échecs … abandonnée », à calibrer) mènent à l'abandon. La procédure 04 § Porte P3 n'abandonne qu'au « troisième échec ». Les deux textes se contredisent, comme l'avait déjà noté `JOURNAL.md` pour P2.

## Les corrections demandées à la v3 : réponse réelle, partielle ou seulement affirmée

| Demande (revue v3) | Réponse de la v4 | Statut | Ce que la réponse a cassé ou alourdi |
|---|---|---|---|
| 1. Le propre reste propre, et le joueur monte en lavant | M07 récrit : « Une vitre lavée reste propre » (FICHE l.172) ; 5 vitres = 1 étage (l.70) ; resalissure seulement par les pigeons, le déménagement et le lundi du beffroi, toujours montrés (l.139, l.172) ; première montée à 14 s (l.252) | **Réelle pour « le propre reste propre ». Partielle pour « monter en lavant »** | Le parcours en serpentine (l.75) fait **descendre** la nacelle sur les façades 2 et 4 : une rangée sur deux fait perdre un étage. Après 54 s, aucun étage neuf avant 3 min 30 environ (calcul plus bas), alors que l'annexe A annonce « un étage de plus toutes les 10 secondes » entre 61 et 180 s (l.261). L'annexe est donc contredite par le parcours de la même fiche. Ajouts : tour étincelante, pigeons, scène de déménagement, trophée miniature |
| 2. Un geste qui se sent et qui varie | Glisser ou tapoter (l.166), traînée en moins de 150 ms, note qui monte sur une série, rideau d'eau, fanfare (l.77), une vitre sur dix spéciale (l.79) | **Réelle sur le papier** ; le plaisir reste non vérifiable | La fiche montre un glisser (« Une main fantôme glisse dessus », l.251) mais ne dit pas que ce glisser est capté par le jeu. Sur téléphone, Roblox fait tourner la caméra quand on glisse le doigt sur l'écran. Rien n'est écrit sur la caméra dans la nacelle, ni sur le joystick et le bouton de saut. Sons : de 6 à 9 |
| 3. La seconde place sert à quelque chose | « Monter à bord » en un toucher, on lave ensemble la tour du propriétaire, la nacelle monte deux fois plus vite, mousse à durée unique de 10 s (l.179, l.171) | **Réelle**, avec deux trous | (a) Le chemin n'est pas écrit : le joueur apparaît dans sa propre nacelle (l.251), et rien ne dit comment il en sort ni comment il atteint la tour d'un ami. Le test demandé (« un toucher, moins de 10 s après son apparition ») n'est donc pas atteignable tel quel. (b) Le quota de 300 s de mousse par partenaire et par jour éteint l'effet visible (l.171) : l'« explosion de mousse » de la scène à filmer (l.182) disparaît au bout de 5 minutes avec son meilleur ami. Calcul en plus : un duo lave 60 vitres par minute, finit la tour 1 vers 10 min et la tour 2 environ 15 min avant l'ouverture de la tour 3 (tours ouvertes par les achats, SIM « tour2 à 15:33, tour3 à 50:52 ») ; il passe ensuite ce temps à relaver la bande du haut après chaque vol de pigeons |
| Objectif à J7 (axe 6) | La Flèche, tour sans fin, segment par segment, record du serveur (l.144–150) ; le beffroi, chantier de la semaine sans série de connexion (l.158) | **Réelle** pour la Flèche ; **réelle mais lourde** pour le beffroi | La Flèche garde une valeur au geste : seul le lavage la fait pousser (l.144). Le beffroi fait doublon avec le contrat du jour (deux façades spéciales payées en minutes de revenu). C'est un objet **partagé** dont la saleté est **propre à chaque joueur** (600 vitres chacun, l.158), et la fiche ne dit ni où se placent six nacelles ni ce que chacun voit de la saleté des autres. C'est le risque de rendu par joueur que la revue v3 relevait sur les façades, déplacé sur le beffroi |
| Vitre lavable dès 0 s (tableau de décrochage) | Annexe A récrite : premier geste vers 4 s, première vitre à 6 s (l.251) | **Réelle** | — |

Calcul de la serpentine (d'après FICHE l.75, l.247, l.255, l.261) : la façade 1 monte du 1ᵉʳ au 5ᵉ étage et se finit vers 54 s. La façade 2 redescend au 1ᵉʳ étage vers 1:46, la façade 3 remonte vers 2:37, la façade 4 redescend vers 3:28. L'étage 6 n'arrive qu'au changement de bande, vers **3:30**. Dans la fenêtre de 61 à 180 s que Roblox mesure, la nacelle descend environ 100 s, remonte 50 s, et n'atteint aucun étage nouveau. La fiche ne dit pas ce qu'affiche « Étage n / 30 » pendant une descente.

## Notes

Sans preuve, la note ne dépasse pas 5. Mode : vu, lu, non vérifiable. Nature de la note : **(a)** fondée sur ce qui est lu ; **(b)** plafonnée faute de preuve possible sur papier ; **(c)** abaissée par ce que la fiche écrit.

| Axe | Note /10 | Preuve | Mode | Nature |
|---|---|---|---|---|
| 1. Première minute | 8 | Annexe A (l.251–257) : apparition dans la nacelle face à une vitre lavable, un seul mot (« Frotte ! »), premier geste vers 4 s, première montée à 14 s, robots à 25, 41 et 56 s, 5 étages lavés à 60 s, texte le plus long de 4 mots. Pas de menu. Les achats en jeu suivent ceux de la simulation à 5 ou 6 s près (SIM : 0:20, 0:36, 0:50 ; l.259). Réserve : le glisser montré par la main fantôme n'est pas protégé de la caméra tactile (l.251, rien sur la caméra) | lu | (a), avec réserve |
| 2. Boucle courte | 5 | Tout ce que la revue v3 demandait est écrit : traînée en moins de 150 ms, note qui monte, rideau d'eau à chaque rangée, fanfare à chaque bande, tache tenace et fiente (l.77–79), vitre qui reste propre (l.172). Mais le plaisir d'un geste ne se lit pas. Aucune adresse n'est demandée (la nacelle glisse seule, l.170) : la variation repose sur 2 vitres spéciales et sur les sons | lu ; plaisir non vérifiable | (b) |
| 3. Progression visible | 7 | Dix paliers à silhouette propre (l.83–90, F1), hauteur lavée lisible de la place (l.70), tours de 30, 60 et 100 étages, puis la Flèche avec sa balise et son record (l.150), trophée miniature de la tour finie (l.138), objectif suivant toujours affiché (l.73, F2). Moins un point : la serpentine (l.75) fait baisser la hauteur une rangée sur deux et laisse la tour propre en escalier selon les façades ; vue d'un autre côté que la façade 1, la bande paraît en retard | lu | (a), abaissée par (c) |
| 4. Social | 6 | Seconde place visible et éclairée, montée en un bouton, nacelle deux fois plus rapide, mousse, pourboire (l.179–181) : l'interaction a lieu dans le jeu (F8). Contre : le chemin entre sa nacelle et celle de l'ami n'est pas écrit ; la mousse visible s'éteint au quota de 300 s par partenaire (l.171) ; la tour du visiteur n'avance pas pendant qu'il aide ; une tour propre en duo mène à des vols de pigeons en boucle (calcul ci-dessus). La scène de vignette (l.182 : 90ᵉ étage, coucher du soleil, Flèches au-dessus des nuages) n'est pas atteignable dans les 10 premières minutes (F5), et ni le cycle jour et nuit ni les nuages ne figurent dans les coûts (l.205) | lu | (a), abaissée par (c) |
| 5. Adéquation Roblox | 6 | Verbe porté par la veille (Sweep The Moon 24 664 sur la semaine, +489 % ; Clean The Ballpit! +172 % sur 24 h, `b1-theme-un-geste.md`), titre court du même moule (« Wash The Tower », l.12), se joue au pouce, session utile de 5 min (bras articulé et contrats vers 4:31 à 4:41, SIM), promesse visible dès 14 s. Contre : dans la fenêtre de 61 à 180 s, la promesse « monter » cale (étage 6 vers 3:30) et l'annexe A affirme le contraire (l.261) ; le glisser sur téléphone n'est pas spécifié face à la caméra de Roblox ; la vignette promet « la ville très bas » (l.54), qui n'arrive qu'en tour 2 ou 3 ; Sweep The Moon a l'antériorité du verbe | lu | (a), abaissée par (c) |
| 6. Retour (J1, J7) | 5 | J1 : réservoir « 2 h à 50 % » affiché (l.154), compte à rebours du contrat sur le panneau de la place (l.156), tour enregistrée telle qu'on l'a laissée (l.172). J7 : la Flèche, que le geste fait pousser, avec record d'étages (l.144–150), et le beffroi de la semaine (l.158). Pour un joueur d'une demi-heure par jour, la Flèche commence vers le jour 3 ou 4 (l.291). La rétention elle-même ne se lit pas | lu ; rétention non vérifiable | (b) |
| 7. Faisabilité pour l'usine | 6 | Contenu par répétition d'un module d'étage, pièces bornées (l.208), robots en pièces simples. Mais la v4 alourdit tout : sons de 6 à 9, chaînes de 70 à 90, objectif de pièces de 1 500 à 2 000 (l.207–208) ; objets nouveaux : vol de pigeons, beffroi, segment et balise de la Flèche, trophées, 4 fanions, 2 vitres spéciales, scène de déménagement de 20 s, tour qui sort de terre (l.138, l.205). C4 : l'annexe B (l.265–267) compte 1 + 1 + 1, mais la méta porte à la fois les tours, la Flèche avec son record, un contrat quotidien et un beffroi hebdomadaire, qui a son lieu, son cycle, sa récompense et son état par joueur sur un objet partagé. Archipel a échoué par accumulation de systèmes (LECONS Produit 1), et l'usine n'a encore rien produit dans Studio (`ETAT.json` : « univers TEST du propriétaire » attendu) | lu | (c) |
| **Moyenne** | **6,1** | 43 / 7 = 6,14 | | |

## Où un joueur de 10 ans sur téléphone décroche

| Moment | Ce qui se passe | Pourquoi il part |
|---|---|---|
| 0–6 s | Une main fantôme **glisse** sur la vitre, « Frotte ! » | Il imite la main. Si le jeu ne capte pas ce glisser, la caméra Roblox tourne et la vitre ne se lave pas. La fiche ne le dit pas : c'est le risque le plus grave de la minute, et le moins cher à fermer |
| 6–54 s | 5 vitres = 1 étage, 3 robots, rideau d'eau, note qui monte | Rien sur papier : c'est la meilleure minute écrite par l'usine jusqu'ici |
| 54 s – 1:46 | La nacelle passe l'angle (la vue tourne), puis **redescend** étage par étage sur la façade 2 | « Je descends ? » : la promesse est de monter, et le compteur d'étage baisse ou reste à 5 (la fiche ne dit pas lequel) |
| 1:46 – 3:30 | Elle remonte, redescend ; aucun étage neuf avant 3:30 environ | Des événements continuent (robots 4 et 5, raclette large vers 1:45, raclette automatique vers 2:20), mais la hauteur, ce qui porte la promesse, cale dans la fenêtre que Roblox mesure |
| Toute la partie | Des « robots laveurs » montent et descendent sur des vitres sales qui restent sales (M07 : « Les robots sont un décor animé : ils ne lavent pas les vitres du stock », l.172) | « Ils servent à quoi ? » : petite incohérence pour un enfant, à corriger à bas coût |
| 5 min de duo avec le même ami | La mousse s'éteint (quota) | L'effet le plus montrable disparaît sans explication ; ils continuent à deux, mais sans fête |
| Duo vers 10 min sur la tour 1 | Tour étincelante, puis pigeons en boucle sur la bande du haut jusqu'à l'ouverture de la tour 2 | La resalissure de la v3 revient sous une forme montrée et comique, mais elle revient, et justement pour ceux qui jouent à deux |

## Comparaison au corpus

Corpus de `b1-theme-un-geste.md`. Aucun jeu n'a été joué : ce qu'ils font est lu sur leur titre ou leur fiche.

| Jeu | Gagnant ou faible | Ce qui nous en rapproche | Ce qui nous en distingue |
|---|---|---|---|
| Cut a Rock | Gagnant (+1 824 % sur le mois) | Désormais, un geste qui transforme durablement l'objet (vitre qui reste propre) | Sa transformation est le progrès lui-même ; chez nous la hauteur suit le geste, mais pas de façon monotone (serpentine) |
| Depth Incremental | Gagnant (+598,8 % sur le mois) | Une distance verticale comme progression ; la Flèche sans fin ressemble à sa profondeur | Lui ne fait (d'après son titre) qu'avancer ; nous descendons une rangée sur deux |
| Sweep The Moon | Gagnant (+489 % sur la semaine) | Même verbe, robots qui nettoient | Façade verticale et montée ; mais chez nous les robots ne nettoient pas (M07), et il a l'antériorité |
| Throw Lucky Block For Animals | Faible (1 073 sur 24 h) | — | Nous ne reprenons pas tel quel le geste d'un gagnant |
| Sell Fries! | Faible (−21,6 %) | Tâche de service répétée, tycoon calme | Silhouettes et hauteur visibles ; le risque de « corvée » reste le même tant que le geste n'est pas joué |
| +1 Speed Keyboard Escape | Faible (retombé en deux mois) | Geste de mode | La v4 a un objectif à J7 (la Flèche) que la v3 n'avait pas |

Ce qui nous distingue des faibles : une différence visible (la hauteur), un résultat durable du geste et un objectif après la fin du contenu. Ce qui nous en rapproche encore : un plaisir du geste qu'aucune pièce ne prouve, et une promesse « monter » qui cale entre 61 et 180 s.

## Corrections demandées, par impact

1. **Rendre la montée monotone.** La fiche se contredit : « Cinq vitres font une rangée : la nacelle monte d'un étage » (l.70) contre une serpentine qui descend sur les façades 2 et 4 (l.75) ; et l'annexe A (l.261) ne correspond pas à son propre parcours. Option recommandée : une **hélice d'un étage**. Un étage = 20 vitres (5 par façade), la nacelle passe l'angle à chaque façade et monte d'un étage à chaque tour. Elle ne descend jamais, l'anneau de verre propre se voit de tous les côtés (F1 renforcée), et il y a 20 vitres séparées au lieu de 25 (P12 tenue). Coût : 4 angles par étage au lieu de 3 par bande. Il faut un angle d'environ 0,5 s, sinon le rythme de 30 vitres par minute est à rechiffrer par l'économie. Première montée vers 48 s au lieu de 14 s. Pour garder la montée rapide de la première minute : les 5 premiers étages de la tour 1 ne se lavent que sur la façade 1 (le stock de la tour 1 passe de 600 à 525 pour 467 lavées : à contre-vérifier), puis l'hélice prend le relais. Dans tous les cas : le compteur « Étage n » ne baisse jamais, et l'annexe A se récrit à partir du parcours. *Test* : 0 baisse du compteur en 3 min ; au moins 2 nouveaux étages entre 61 et 180 s.
2. **Protéger le geste de la caméra tactile et cadrer la vitre.** Écrire dans la fiche : dans la nacelle, la caméra est tenue par le jeu (la vitre au centre, au moins 40 % de la largeur d'un écran de téléphone), un toucher qui commence sur la vitre est pris par le jeu et ne fait jamais tourner la caméra, joystick et saut sont masqués, bouton d'achat et objectif restent hors de la vitre et hors des zones des pouces (Q4). Coût faible, impact maximal : c'est le geste du jeu, sur l'appareil visé. *Test* : 30 vitres glissées au format téléphone, 30 validées, 0 rotation de caméra, latence ≤ 150 ms.
3. **Alléger la méta.** Fusionner le contrat du jour et le beffroi (par exemple, le contrat devient la part du jour du beffroi, 10 min de revenu chaque jour et 30 min à la fin de la semaine), ou supprimer le beffroi : la Flèche porte déjà le J7. Si le beffroi reste, l'attacher à la parcelle de chaque joueur plutôt qu'à un objet partagé, ce qui supprime l'état par joueur sur un objet commun et la question des six nacelles. Gain : un cycle, un lieu, un rendu par client et des chaînes en moins (C4, axe 7). *Test* : deux clients lavent leur beffroi en même temps, sans collision, chacun voit son propre état.
4. **Social : plafonner le bonus, pas l'effet ; écrire le chemin.** (a) La mousse reste visible tant que le duo lave ; seul le +25 % s'arrête au quota (E15 tenue, plaisir intact). (b) Écrire comment un joueur quitte sa nacelle et rejoint la seconde place d'un ami, par exemple un bouton « Rejoindre <ami> » dans sa nacelle quand un ami Roblox est sur le serveur, qui l'assoit en un toucher. (c) Quand la tour du propriétaire devient étincelante avec un visiteur à bord, proposer « Chez <visiteur> ! » avant les pigeons, pour que le duo passe à la tour de l'autre. *Test* : B, ami de A, est assis à côté de A en 2 touchers au plus et 15 s au plus après son apparition ; la mousse est encore visible après 5 min de duo.
5. **Que ce qu'on voit tienne la promesse.** Les robots ne travaillent que sur la partie déjà propre (ils la font briller sous la nacelle) ou sur le toit, jamais sur du verre sale qu'ils laissent sale. Récrire la scène de vignette (l.182) avec une scène atteignable avant 10 min (F5) : deux amis dans la nacelle vers le 10ᵉ étage de la tour 1, mousse, ville en bas. Retirer le coucher du soleil et les nuages, ou les chiffrer au § 6. *Test* : capture à 10 min avec deux clients, lisible à 150 px de large (L7).

## Scénarios à rejouer par la QA

1. **Premier contact, téléphone, nouveau compte, sans lire.** Chronométrer le premier geste et la première vitre (prévision : 4 s et 6 s ; seuil 60 s). Glisser 10 vitres comme le montre la main fantôme : 10 validées, caméra immobile, latence contact → traînée ≤ 150 ms mesurée (journal horodaté sous `RunService:IsStudio()` ou décompte d'images).
2. **Solo de 0 à 180 s, relevé toutes les 5 s** de l'étage affiché et de la hauteur de la nacelle. Attendu : 0 baisse, au moins 2 étages nouveaux entre 61 et 180 s, aucun trou de plus de 20 s sans événement visible (prévision de la fiche ; défaut au-delà de 45 s). Comparer à l'annexe A de la version testée.
3. **Deux clients amis.** B rejoint la seconde place de A depuis son apparition : compter touchers et secondes. Mousse déclenchée ; étages par minute du duo contre ceux d'un joueur seul (attendu × 2). Avec une action de test, atteindre le quota de mousse et noter ce qui reste visible. Rendre la tour de A étincelante (action de test) : noter ce qui est proposé au duo avant les pigeons.
4. **Lisibilité depuis la place**, PC 1920 × 1080 et téléphone (Q8). Poser par action de test six tours à des avancements différents (tour 1 étage 5, tour 2 étage 30, tour 3 étage 90, une Flèche de 3 segments). Le testeur classe les joueurs par avancement sans lire ; la bande propre de chaque tour se voit ; aucun robot ne se tient sur du verre sale.
5. **Le propre reste propre.** Laver 37 vitres, quitter en pleine rangée, revenir : la nacelle reprend à la même vitre et aucune vitre n'est resalie (Q5). Jouer 10 min sans vider le stock : 0 vitre lavée redevenue sale. Forcer le stock à 0 : compte à rebours visible, puis les pigeons salissent la bande du haut et rien d'autre.

## Pour la décision de l'orchestrateur

Cette section ne change ni mes notes ni mon verdict.

**Moyenne des seuls axes vérifiables sur le papier** (1, 3, 4, 5, 7) : (8 + 7 + 6 + 6 + 6) / 5 = **6,6**. Avec les deux axes plafonnés à 5, P3 exige 7,8 sur ces cinq axes (procédure 04). J'estime qu'une v5 qui applique les cinq corrections les porterait vers 7,4 (axes 3 et 5 + 1, 4 et 7 + 1), soit 6,7 au total : la passe papier ne peut pas ouvrir P3 pour ce jeu telle qu'elle est écrite. C'est une estimation, pas une mesure.

**Ce que le prototype des 60 premières secondes (P4, passe 2) doit montrer pour qu'un axe plafonné vaille 7 ou plus.**

*Axe 2, boucle courte*, en Play, au format téléphone et en PC plein écran, toutes conditions requises :

| Mesure | Seuil |
|---|---|
| Latence contact → traînée visible | ≤ 150 ms sur 20 vitres sur 20 (F3) |
| Glisser et tapoter | 10 vitres validées sur 10 pour chaque geste ; 0 rotation de caméra pendant les glissés |
| Rythme réel du relecteur, sans aide | ≥ 25 vitres à 60 s (fiche : 28) ; première montée ≤ 20 s |
| Retours distincts observés dans la minute | ≥ 4 parmi : traînée, éclat et pièce volante, note qui monte, rideau d'eau et montée, vitre spéciale ; une vitre spéciale vue avant 45 s (à placer de façon fixe dans la première bande) |
| Sons | Note montante sur 8 crans vérifiée dans le journal (identifiant et hauteur de chaque son) ; aucun son répété plus de 3 s sans variation |
| Fluidité | ≥ 30 images par seconde au format téléphone pendant la traînée (`qa.fps_min_telephone`) |
| Résultat durable | 0 vitre lavée redevenue sale en 3 min |
| Jugement | Plaisir du geste noté ≥ 7 par le relecteur de la passe 2 après 3 min de jeu, raisons écrites. Sans aucun test par un humain (propriétaire ou enfant), je ne donnerais pas plus de 7 |

*Axe 6, retour* : **aucune mesure d'un prototype de 60 s ne justifie 7**. Le prototype peut seulement montrer que l'axe ne doit pas tomber sous 5 : sauvegarde fidèle (scénario 5), raison de revenir visible depuis la nacelle sans ouvrir de menu (réservoir, compte à rebours du contrat), F6. Le 7 se gagne en bêta : J1 ≥ 8 % sur 200 joueurs organiques au moins et session médiane ≥ 8 min (`seuils.json` § `beta`). Je propose d'y ajouter, sans que ce soit un seuil écrit : J7 ≥ 1,6 % (repère GameAnalytics de `seuils.json`) et la part des joueurs revenus à J7 qui avancent la Flèche ou le beffroi.

**Cette fiche mérite-t-elle qu'on engage le prototype L0 ? Mon avis : oui, mais sous conditions, et sans parler de GO.**

Pour :
1. Les deux axes plafonnés pèsent 2 sur 7 et mesurent exactement ce que le L0 mesure (geste, rythme de montée). Une itération de plus sur papier ne peut pas les faire bouger ; elle plafonne vers 6,7.
2. Les défauts qui restent sont de spécification : parcours, caméra, méta. Ils se corrigent en une demi-page, sans toucher aux coûts ni aux revenus des robots, sauf le temps d'angle si l'hélice est retenue.
3. Le L0 peut rester étroit : 0 à 180 s, tour 1, les 5 premiers robots, raclette large, une seconde place. Ni Flèche, ni beffroi, ni pigeons, ni déménagement.
4. Un critère d'arrêt existe déjà (annexe D 2 bis, l.301), et la procédure 04 dit elle-même que la grille n'est pas calibrée tant qu'aucun jeu n'a été joué : un premier prototype est aussi ce qui la calibre.

Contre :
1. Ce serait la troisième dérogation sur le même jeu (P0, P2, puis P3) : l'usine plie ses portes pour son premier jeu, exactement le cas que la procédure appelle « GO de complaisance ».
2. La règle A5, lue à la lettre, demande l'abandon.
3. Le verbe « nettoyer » est déjà occupé par deux gagnants récents (Sweep The Moon, Clean The Ballpit!).
4. `ETAT.json` est bloqué sur l'univers TEST du propriétaire : le L0 n'est peut-être pas lançable de toute façon.

Ma conclusion : engager le L0 seulement si les trois conditions suivantes sont réunies.
- (a) Une v5 écrit d'abord les corrections 1, 2 et 4 a ; c'est peu de travail.
- (b) La dérogation est écrite dans `ETAT.json` (règle A4), avec cette raison : « plafond structurel de la passe papier, axes 2 et 6 ».
- (c) L'arrêt est ferme et écrit d'avance : plaisir du geste sous 6 en passe 2, ou aucun étage nouveau entre 61 et 180 s, et l'idée est abandonnée sans nouvelle itération.

Si l'orchestrateur refuse la dérogation, l'abandon selon A5 se défend. La leçon serait alors que la porte P3 papier ne peut pas laisser passer un jeu à un geste, et c'est au bilan d'en décider.

## Limites de cette revue

- Passe papier : rien n'est vu. Le plaisir du geste (axe 2) et la rétention (axe 6) ne se prouvent qu'en Play puis en bêta.
- Le corpus n'a pas été joué ; la veille est en dérogation (P0 : Charts du jour illisibles, prix et cadence pour 2 jeux sur 20).
- Les horaires de la serpentine (3:30 pour l'étage 6) et des boucles de pigeons en duo sont des **calculs** à partir des lignes citées de la fiche et des jalons de la simulation ; ils supposent 2 s par vitre et un duo qui commence ensemble.
- Je n'ai pas jugé la justesse de l'économie. Les corrections 1 (temps d'angle, stock de la tour 1) et 3 (récompenses fusionnées) la touchent et demandent une contre-vérification avant la production.
- Le beffroi n'est pas jugeable sur son plaisir tant que sa disposition physique n'est pas écrite.

Passe 2 seulement — première action chronométrée : sans objet (passe 1). Erreurs console : sans objet.

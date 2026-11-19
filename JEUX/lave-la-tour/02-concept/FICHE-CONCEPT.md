# Fiche concept — Lave la tour (`lave-la-tour`)

Version 5.1 du 2026-11-16. Auteur : Claude Fable 5.2, effort high (concepteur joué par l'orchestrateur du cycle 2). Statut : version écrite après le deuxième échec de la porte P3 (`04-fun\RAPPORT-FUN-V4.md`, ITÉRER à 6,1) et l'échec papier de la contre-vérification n° 3 (`03-economie\RAPPORT-ECONOMIE-contre-verification-3.md`, 1 défaut P1). Aucune constante de coût ou de revenu des robots ne change depuis la version 2. À contre-vérifier (économie) et à relire (fun) par des agents qui n'ont pas écrit cette version.

**Ce qui change depuis la version 4.**

D'après la revue du fun (corrections 1 à 5 de `RAPPORT-FUN-V4.md`) :

1. **La montée ne recule jamais** (correction 1). Plus de serpentine ni d'angles : le joueur lave **une seule façade**, celle qui regarde la place, large de 5 vitres ; 5 vitres = 1 étage, du premier au dernier. Les tours comptent 120, 280 et 400 étages (600, 1 400 et 2 000 vitres). Le compteur « Étage n » ne baisse jamais dans une même tour.
2. **Les robots travaillent pour de vrai à l'écran** (correction 5) : ils lavent les trois autres façades, jusqu'à la hauteur de la nacelle. Aucun robot ne se tient sur du verre sale qu'il laisse sale.
3. **Le geste est protégé de la caméra tactile** (correction 2) : dans la nacelle, la caméra est tenue par le jeu, un toucher qui commence sur la vitre ne fait jamais tourner la vue, joystick et saut sont masqués (§ 3, « Caméra et commandes »).
4. **La méta est allégée** (correction 3) : le beffroi de la semaine, ses fanions et ses cloches sont supprimés ; la Flèche porte seule l'objectif à J7. Le contrat du jour se lave sur la parcelle du joueur. Le trophée miniature devient une plaque.
5. **Social** (correction 4) : la mousse reste visible tant que le duo lave, seul le +25 % s'arrête au quota ; bouton « Rejoindre <ami> » dans sa nacelle ; quand la tour devient étincelante avec un visiteur à bord, le jeu propose « Chez <visiteur> ! » avant les pigeons. Scène de vignette atteignable en 5 minutes.

D'après la contre-vérification d'économie n° 3 :

6. **F01 (P1)** : la Flèche ne s'ouvre qu'avec **les 100 robots en service et les 5 améliorations** ; la promesse hors ligne est récrite sur cet état.
7. **F02 (P2)** : la tache tenace qui comptait double est supprimée. Les vitres différentes ne sont plus que visuelles : toute vitre vaut une unité, trois passes, le même gain. Les cadences 30, 15 et 40 sont des vitres, sans pondération.
8. **F03 (P2)** : annexe A recalculée sans angle ni tache tenace (28 vitres et 5 étages à 60 s, calcul discret).
9. **Décisions D03 à D10** écrites au § 3 ter (M05, M07, M08, M10) ; D01, D02 et D09 disparaissent avec la tache tenace et le beffroi.
10. **Stock** : la tour 2 passe à 1 400 vitres pour couvrir aussi un joueur au plafond de 40 vitres par minute (calcul de stress du rapport, § 2.3).
11. **Version 5.1** : décisions D11 à D13 de `03-economie/RAPPORT-ECONOMIE-contre-verification-4.md` (M11 à M13 ; ce rapport rend 0 défaut P0 ou P1 et « oui pour L0 et L1 » sur la v5) ; corrections A à G de `04-fun/RAPPORT-FUN-V5.md` (revue indépendante de la v5 : axes vérifiables à 7,0, avis « prototype L0 sous dérogation après A, B, C, D ») : caméra de biais qui montre les robots, bouton « Rejoindre » sans conflit, arrêt ferme et mesuré, périmètre du L0, compteur au déménagement, Flèche sur le toit de la tour 3, plan d'écran, état des autres façades et largeur des tours.
Titre de travail en anglais (texte source, règle C8) : **Wash The Tower**.

**Ce qui avait changé de la version 3 à la version 4**, d'après `04-fun\RAPPORT-FUN-INDEPENDANT.md` : le propre reste propre et le joueur monte en lavant ; geste au doigt avec traînée, note qui monte et vitres différentes ; seconde place de nacelle utile ; la Flèche comme objectif après le contenu ; vitre lavable dès 0 seconde.

**Ce qui avait changé de la version 2 à la version 3**, d'après `03-economie\RAPPORT-ECONOMIE-contre-verification-1.md` (aucune constante de coût ou de revenu ne change) :

1. **Stock de vitres propre à chaque joueur** (N02, M07) : plus aucune vitre disputée entre un propriétaire et ses visiteurs.
2. **Raclette motorisée** (N03) : 30 vitres par minute, dans le plafond commun de 40 ; la règle de monétisation le dit.
3. **Quotas** (N04, M02, M06) : mousse comptée en temps, partenaire désigné à chaque activation, plancher quand le joueur n'a encore aucun robot.
4. **État** (M05, M08, M09) : déplacement de la nacelle, intervalle hors ligne, arrondi des prix et plafond de solde.
5. **Annexes A et C** (D3) recalculées avec le simulateur corrigé (revenu ajouté complet, prix entiers).

**Ce qui avait changé de la version 1 à la version 2**, la version 1 ayant été refusée à la porte P2 par `03-economie\RAPPORT-ECONOMIE-calcul.md` (D1 à D3) et `RAPPORT-ECONOMIE-adversaire.md` (A01 à A03, M01 à M09) :

1. **Le geste garde sa valeur** (A02) : une vitre rapporte une pièce de base **plus une part du revenu des robots** (§ 3 bis). En version 1, le joueur deux fois moins actif finissait 1,1 % plus tard que le joueur actif ; il finit maintenant 10 % plus tard.
2. **Remboursement de chaque exemplaire sous 5 minutes** (A01, D2) : la croissance du coût par exemplaire baisse de 1,2 à 1,06–1,17 à partir du palier 3.
3. **Durée de contenu** (D1) : coûts et revenus des paliers 5 à 10 relevés ; 97 minutes simulées au lieu de 87.
4. **Mousse plafonnée par jour et par partenaire** (A03).
5. **Décisions d'état écrites** (M01 à M09) : nouveau § 3 ter.
6. **Offre renommée** « Raclette motorisée » (elle portait le nom du robot r2) ; règle de monétisation reformulée.
7. **Annexe C** recalculée avec le simulateur au lieu d'estimations de l'auteur (D3).

Sources de marché : `VEILLE\RELEVES\2026-11-15\b1-theme-un-geste.md` et `v5-orchestrateur-rostats.md`. Aucun jeu du corpus n'a été joué ; tout chiffre de marché absent de ces relevés est `NP`.

## 0. Pistes étudiées et choix

**Piste A — L'aimant.** Promesse : lancer un aimant dans un canal et remonter des épaves de plus en plus grosses. Différence visible : la prise sort de l'eau en vrai volume et s'empile sur le quai du joueur. Première minute : lancer, remonter une boîte de conserve, la vendre, acheter une corde. Inviter : une grosse prise se remonte à plusieurs. Revenir : un canal vidé chaque jour. Risque : une quarantaine d'objets à modeler, ce que l'usine fait mal ; le geste « lancer » est déjà celui du gagnant du mois.

**Piste B — La boule de neige.** Promesse : rouler une boule de neige qui grossit et en faire des statues. Différence visible : la boule grossit sous les pieds du joueur. Première minute : rouler, déposer, premier bonhomme. Inviter : rouler à deux une boule géante. Revenir : la neige retombe chaque jour. Risque : jeu de saison ; l'usine n'a ni univers ni droits de publication, la saison serait passée avant la sortie.

**Piste C — Lave la tour.** Promesse : laver les vitres d'un gratte-ciel depuis une nacelle et monter étage après étage. Différence visible : la progression est une hauteur ; la partie propre de la tour brille et se voit de tout le serveur. Première minute : une vitre sale devant soi, trois coups de raclette, des pièces, un premier robot laveur. Inviter : une nacelle à deux places et un bonus de mousse à plusieurs sur la même façade. Revenir : un contrat du jour et des robots qui travaillent pendant l'absence. Risque : laver est une corvée si le retour visuel est faible ; tout repose sur le plaisir du geste.

| Piste | Promesse | Vignette | 60 s | Différence | Périmètre | Social | Coût | Total /30 |
|---|---|---|---|---|---|---|---|---|
| A | Remonter des épaves à l'aimant | 5 | 4 | 4 | 4 | 4 | 2 | 23 |
| B | Rouler une boule de neige géante | 5 | 5 | 2 | 4 | 3 | 4 | 23 |
| C | Laver un gratte-ciel et monter | 4 | 5 | 4 | 5 | 3 | 5 | 26 |

Piste retenue : **C**, parce que son contenu se fabrique par répétition d'un module d'étage (coût le plus bas des trois), que sa progression se lit à distance sans texte (règle F1), et que le geste « nettoyer » monte dans le corpus (Sweep The Moon, +489 % sur la semaine) sans y être porté par un jeu vertical. A est écartée pour son coût d'objets, B pour sa saison.

## 1. Promesse d'action

> Lave les vitres d'un gratte-ciel et monte jusqu'au sommet.

Image fixe : un personnage dans une nacelle, raclette levée, au milieu d'une façade — verre bleu étincelant en dessous (ce qu'il a lavé), vitres brunes au-dessus (ce qui reste), la ville très bas.

## 2. Différence visible

| Jeu du corpus | Ce qu'il fait (d'après sa fiche ou son titre, non joué) | Ce que nous faisons autrement, visible en capture |
|---|---|---|
| Throw Food For Animals | Lancer loin, collecter des animaux qui rapportent à la base | Pas de collection : la progression est la hauteur lavée d'une tour, lisible de l'autre bout du serveur |
| Sweep The Moon | Balayer un sol, des robots nettoient | Même verbe « nettoyer », mais sur une façade verticale, depuis une nacelle qui monte ; les robots grimpent sur la tour |
| Break and Steal an Egg | Voler les animaux des autres, fuir des gardes | Aucun vol : on peut laver la tour d'un autre joueur, et les deux y gagnent |

## 3. Boucle de progression

Action → résultat → monnaie → amélioration → prochain objectif :

1. Le joueur frotte une vitre (trois passes de raclette, au doigt qui glisse ou en tapotant, 2 secondes) : la raclette laisse une traînée de verre propre, la vitre étincelle. **Elle reste propre.**
2. Chaque vitre lavée donne des **pièces** : une base fixe, plus une part du revenu de ses robots.
3. **Cinq vitres font une rangée : la nacelle monte d'un étage.** Toujours vers le haut : la hauteur du joueur est exactement ce qu'il a lavé, et la bande de verre propre se voit de la place et des autres tours.
4. Les pièces achètent une meilleure raclette (gain par vitre) et des **robots laveurs** (revenu par seconde). Les robots lavent dans le cadre de la caméra (façade voisine) les trois autres façades, sous la hauteur de sa nacelle.
5. Trois robots en service d'un palier débloquent le palier suivant ; certains paliers ouvrent une tour plus haute.
6. L'objectif suivant est toujours affiché en bas de l'écran (« Encore 2 robots ventouses → raclette automatique »), avec l'étage atteint (« Étage 7 / 120 »), qui ne baisse jamais dans une même tour ; au déménagement, il repart de 1 sur une tour plus haute.

**Parcours de la nacelle.** Le joueur lave la façade qui regarde la place : une colonne de verre large de 5 vitres, du premier étage au sommet. Une rangée se lave dans n'importe quel ordre ; quand ses 5 vitres sont propres, la nacelle monte d'un étage (0,4 seconde, pendant laquelle le toucher suivant est déjà accepté). Aucun angle, aucune descente. Un joueur seul monte d'un étage toutes les 10 secondes ; à deux dans la nacelle, toutes les 5 secondes.

**Caméra et commandes.** Dans la nacelle, la caméra est tenue par le jeu : elle est placée de biais, à environ 35° de la façade et un peu au-dessus de la nacelle : la vitre en cours est au centre et occupe au moins 40 % de la largeur d'un écran de téléphone ; l'arête de la tour, la façade voisine où travaillent les robots et la ville en dessous sont dans le cadre. À chaque achat de robot et à chaque fanfare des 10 étages, la caméra recule 2 secondes pour montrer la tour entière et ce qui vient d'arriver, puis revient ; jamais pendant un glissement, et le lavage reste possible pendant ce recul. Un toucher qui commence sur la vitre est pris par le jeu : il ne fait jamais tourner la caméra. Le joystick et le bouton de saut de Roblox sont masqués tant que le joueur est assis. Le bouton d'achat et l'objectif sont en bas, hors de la vitre ; aucun bouton sous les pouces au repos (Q4). Un bouton discret « Descendre » rend la marche et la caméra libres sur la place ; revenir au pied de sa tour, ou à la borne d'une autre tour dont la seconde place est libre, propose « Monter ».

**Plan d'écran (téléphone d'abord, mêmes places en PC).** Haut gauche : pièces et revenu par seconde. Haut centre : « Étage n / N ». Haut droit : rien (liste des joueurs de Roblox, F9). Bas centre : l'objectif suivant et, juste au-dessus, le bouton d'achat proposé (un seul). Bas gauche : « Idée / bug » et « Descendre », petits. Bord droit, à mi-hauteur : **un seul bouton contextuel à la fois**, par priorité : « Déménager », puis « Chez <visiteur> ! », puis « Rejoindre <ami> », puis « Contrat du jour ». Les messages (bonus de mousse atteint, pigeons, réservoir au retour) passent en une ligne sous le compteur d'étage, un à la fois (F4). Rien sur la vitre, rien sous les pouces au repos, largeurs fixes (Q9).

| Moment | Ce qui est à l'écran, en plus de la vitre |
|---|---|
| 0 s | « Frotte ! », la main fantôme ; pièces à 0, « Étage 1 / 120 » |
| 60 s | Pièces, « Étage 6 / 120 », objectif « 3 robots → raclette automatique », bouton « Robot 18 » |
| 5 min | Les mêmes, plus le bouton contextuel « Contrat du jour » (ouvert vers 4:41) |
| 20 min | Les mêmes sur la tour 2 ; bouton contextuel selon la priorité ; aucun élément de plus |

**Retours du geste (règle F3).** Premier retour visuel moins de 150 ms après le contact (traînée de raclette qui découvre le verre). Trois passes : la vitre étincelle, une pièce vole vers le compteur, un son court. Sur une série de vitres sans pause de plus de 3 secondes, la note du son monte d'un cran par vitre (huit crans, puis elle repart) : aucun effet sur le gain. Fin de rangée : un rideau d'eau balaie l'étage, la nacelle monte, deux notes. Tous les 10 étages : une fanfare courte et le numéro de l'étage en grand.

**Vitres différentes (visuel seulement).** Une vitre sur dix environ a un autre aspect : fiente (éclabousse, bruit comique), buée (on y dessine en frottant), affiche collée (elle se décolle en trois lambeaux). Elles valent exactement une vitre : trois passes, 1,5 seconde au moins, le même gain, une unité du budget. Leur place est fixe (fonction du numéro de la vitre) : la 8ᵉ vitre de la tour 1 est une fiente, la 17ᵉ une buée. Aucun bonus caché (E5).

Les six premiers paliers (le tableau complet est au § 3 bis) :

| Palier | Coût | Gain | Ce qui change à l'écran (silhouette, pas couleur) | Débloqué par |
|---|---|---|---|---|
| 1 Robot ventouse | 10 | 0,25 pièce/s | Un petit robot à ventouses collé à la façade, qui monte et descend | Dès l'arrivée |
| 2 Raclette automatique | 90 | 2 pièces/s | Un rail horizontal avec une lame qui balaie un étage | 3 robots ventouses |
| 3 Bras articulé | 800 | 12 pièces/s | Un bras de grue fixé au toit ; ouverture du contrat du jour | 3 raclettes automatiques |
| 4 Nacelle robot | 7 000 | 80 pièces/s | Une seconde nacelle, sans pilote, sur la façade voisine | 3 bras articulés |
| 5 Drone laveur | 200 000 | 1 650 pièces/s | Des drones en vol autour de la tour ; la tour 2 (280 étages) est prête | 3 nacelles robots |
| 6 Essaim de drones | 5 600 000 | 34 500 pièces/s | Un nuage de drones qui fait le tour de l'immeuble | 3 drones laveurs |

## 3 bis. Économie complète (entrée de la revue d'économie)

Monnaie unique : pièces. Cash de départ : 0.

**Action.** Gain d'une vitre = **raclette × (1 pièce × multiplicateurs « tous les revenus » + 0,2 seconde du revenu des robots en service)**. « Raclette » vaut 1 au départ, 2 avec la raclette large, 3 avec le savon moussant. Avec les deux améliorations, une vitre rapporte donc 3 pièces de base plus 0,6 seconde du revenu des robots. Rythme d'un joueur actif : 30 vitres par minute, soit 2 secondes par vitre, glissement et montée de la nacelle compris (profil lent : 15). Le serveur refuse plus de 40 vitres par minute et par joueur (§ 3 ter). Toutes les vitres valent une unité : il n'existe aucune vitre qui compte ou paie double.

Dans `economie.json` : `action.gain = 1`, `action.par_minute = 30`, `action.part_revenu_s = 0.2` ; les améliorations de cible `action` multiplient les deux termes.

**Robots laveurs (générateurs).** Dix exemplaires au plus par palier. Prix de l'exemplaire n = coût du premier × croissance^(n − 1), arrondi à l'entier supérieur (`prix_entiers: true` dans `economie.json`). Le chantier est le délai entre l'achat et la mise en service.

| Id | Nom | Coût du premier | Revenu par seconde | Croissance du coût | Chantier (s) | Débloqué par |
|---|---|---:|---:|---:|---:|---|
| r1 | Robot ventouse | 10 | 0,25 | 1,2 | 0 | — |
| r2 | Raclette automatique | 90 | 2 | 1,2 | 0 | r1 ≥ 3 |
| r3 | Bras articulé | 800 | 12 | 1,17 | 10 | r2 ≥ 3 |
| r4 | Nacelle robot | 7 000 | 80 | 1,14 | 20 | r3 ≥ 3 |
| r5 | Drone laveur | 200 000 | 1 650 | 1,13 | 40 | r4 ≥ 3 |
| r6 | Essaim de drones | 5 600 000 | 34 500 | 1,10 | 60 | r5 ≥ 3 |
| r7 | Canon à mousse | 165 000 000 | 790 000 | 1,075 | 90 | r6 ≥ 3 |
| r8 | Dirigeable laveur | 5 000 000 000 | 19 600 000 | 1,06 | 120 | r7 ≥ 3 |
| r9 | Hélico-brosse | 150 000 000 000 | 520 000 000 | 1,065 | 150 | r8 ≥ 3 |
| r10 | Station de lavage orbitale | 4 500 000 000 000 | 15 500 000 000 | 1,065 | 180 | r9 ≥ 3 |

**Améliorations (achat unique).**

| Id | Nom | Coût | Effet | Débloquée par |
|---|---|---:|---|---|
| a1 | Raclette large | 40 | gain de l'action × 2 | r1 ≥ 2 |
| a2 | Savon moussant | 700 | gain de l'action × 1,5 (soit × 3 avec a1) | r2 ≥ 3 |
| a3 | Ventouses renforcées | 2 400 | revenu de r2 × 2 | r3 ≥ 1 |
| a4 | Double équipe | 350 000 | tous les revenus × 1,5 | r5 ≥ 1 |
| a5 | Contrat d'immeuble | 7 000 000 000 | tous les revenus × 1,25 | r8 ≥ 1 |

Les multiplicateurs se composent une seule fois chacun (a4 puis a5 : × 1,875).

**Jalons.** Contrat du jour ouvert : r3 ≥ 1. Tour 2 (280 étages) : r5 ≥ 1. Tour 3 (400 étages) : r8 ≥ 1. Dans `economie.json` : jalons `contrats`, `tour2`, `tour3`. La Flèche : les 100 robots en service et les 5 améliorations (voir plus bas).

**Tours et stock de vitres.** Chaque joueur a une parcelle et une tour à la fois. Stock = vitres encore sales de la façade qu'il lave (étages × 5).

| Tour | Étages | Vitres | Ouverte par | Temps passé dessus (simulation, profil actif) | Vitres lavées à 30 par minute | Réserve | Vitres lavées par un joueur à 40 par minute (jalons recalculés par la contre-vérification n° 3) | Réserve |
|---|---:|---:|---|---|---:|---:|---:|---:|
| 1 | 120 | 600 | arrivée | 0 à 15:33 | 466,5 | 133,5 | 574,7 | 25,3 |
| 2 | 280 | 1 400 | r5 ≥ 1 | 15:33 à 50:52 | 1 059,5 | 340,5 | 1 334,7 | 65,3 |
| 3 | 400 | 2 000 | r8 ≥ 1 | 50:52 à 1:37:09 | 1 388,5 | 611,5 | 1 762 | 238 |
| La Flèche | sans fin | 200 par segment de 40 étages | 100 robots et 5 améliorations | après la fin du contenu | — | — | — | — |

Un joueur seul, même au plafond de 40 vitres par minute, a toujours une vitre sale devant lui jusqu'à la tour suivante. Deux laveurs sur la même tour la finissent avant : c'est prévu (voir « Tour étincelante »).

- **Déménagement.** Quand la tour suivante est prête, un bouton « Tour 2 prête — Déménager » remplace l'objectif. Le joueur choisit le moment. À l'appui : le visiteur éventuel est ramené à sa tour, le lavage s'arrête, le changement de tour s'enregistre d'un seul coup (identifiant unique : un appui répété ne fait rien), puis une scène de 20 secondes montre les robots finir l'ancienne tour (aucune pièce créditée) et la nouvelle, entièrement sale, sortir de terre. Une plaque au pied de la parcelle compte les tours finies. Rien de ce que le joueur possède n'est remis à zéro.
- **Tour étincelante.** Si la façade est entièrement propre avant que la tour suivante soit prête : drapeau au sommet, éclat visible de tout le serveur. Avec un visiteur à bord, le jeu propose aux deux « Chez <visiteur> ! » : un toucher, et le duo passe sur la tour du visiteur. Sinon, si le joueur reste assis dans sa nacelle avec un stock à zéro pendant 10 secondes de suite (compte à rebours « Les pigeons arrivent… » ; quitter la nacelle, partir au contrat, se déconnecter, déménager ou acheter un segment l'annule), un vol de pigeons salit sous ses yeux les 20 étages du haut (100 vitres). C'est la seule façon dont une vitre lavée redevient sale : un événement annoncé et montré. Ces vitres paient comme les autres ; elles ne changent ni l'étage atteint ni le record.
- Le stock ne manque donc jamais plus de 10 secondes, quel que soit le rythme, y compris à 80 vitres par minute (deux laveurs au plafond : 100 vitres durent alors 75 secondes).

**Fin de contenu de la v1.** r10 ≥ 10 (dix stations orbitales en service). C'est la borne que juge le simulateur. Le profil simulé possède alors les 100 robots et les 5 améliorations.

**La Flèche (objectif au-delà du contenu, visible à J7).** Elle se construit **sur le toit de la tour 3** : à son ouverture, les robots finissent la tour 3 dans le cadre de la caméra (aucune pièce créditée), la nacelle monte au toit, et le premier segment commence au 401ᵉ étage. Le joueur ne redescend jamais. Sans fin. **Elle s'ouvre quand les 100 robots sont en service et les 5 améliorations achetées** (l'objectif affiché le dit : « Encore 4 robots → la Flèche »). Elle pousse par **segments de 40 étages** (200 vitres). Le joueur achète un segment en pièces : il sort du sommet, sale ; le joueur le lave ; le segment lavé reste. Il peut acheter le segment suivant dès que le précédent est acheté, mais pas le surlendemain : **deux segments non finis au plus** (celui qu'il lave et un d'avance).

- Revenu de référence final : **R_fin = 300 757 992 117 pièces par seconde**. C'est le revenu R de tout joueur admis sur la Flèche, à 0,19 pièce près (valeur exacte : 300 757 992 117,1875) ; constante écrite dans `Config`.
- Prix du segment n = 60 × min(4 + n, 9) × R_fin, arrondi à l'entier supérieur : 5 minutes de R_fin pour le premier (90 227 397 635 100 pièces), 9 minutes à partir du cinquième (162 409 315 743 180 pièces, sous le plafond de solde de 9 × 10¹⁵).
- Cadence, à revenu constant et en partant d'un solde nul : le profil actif gagne 1,3 × R_fin : un segment se finance en 3 min 51 s (le premier) à 6 min 55 s (à partir du cinquième) et se lave en 6 min 40 s. Profil lent : 4 min 21 s à 7 min 50 s pour financer, 13 min 20 s pour laver. Sans laver du tout : 9 minutes au plus. Aucun écart ne dépasse le seuil de 15 minutes. Financement et lavage se recouvrent : ces durées ne s'additionnent pas.
- **Retour d'absence** : une réserve pleine (2 h à 50 %, soit 60 minutes de R_fin) finance à elle seule les 7 premiers segments (5 + 6 + 7 + 8 + 9 + 9 + 9 = 53 minutes), ou 6 segments au prix de 9 minutes. Ils s'achètent un par un, au rythme du lavage : la raison de revenir est du verre sale à laver, qui fait pousser la tour.
- **Record d'étages** : la hauteur de la Flèche de chaque joueur (400 + 40 × segments achetés et entièrement lavés une première fois) est réelle dans le monde, portée par une balise au sommet, et affichée sur le panneau de la place (classement du serveur, sans gain). Relaver des vitres salies par les pigeons ne l'augmente pas. La Flèche ne débloque ni robot ni multiplicateur.
- Sur la Flèche, les pigeons ne viennent que si tous les segments achetés sont propres et que le joueur reste 10 secondes sans pouvoir ou vouloir acheter le suivant ; ils salissent 20 étages déjà lavés, jamais un étage non acheté.


**Revenu de référence R.** Partout où cette fiche parle de « minutes de revenu », R est le revenu par seconde des **robots en service**, améliorations permanentes comprises, **sans** le gain des vitres, la mousse, les pourboires ni aucune prime. Une minute de revenu vaut 60 × R pièces, R étant lu au moment de l'attribution.

**Hors ligne (règle E12).** Pendant l'absence, les robots qui étaient en service au moment du départ rapportent 50 % de R, pendant 2 heures au plus. Les chantiers en cours continuent ; un robot mis en service pendant l'absence ne compte dans R qu'au retour. Le jeu affiche « Réservoir d'eau : 2 h à 50 % » et le niveau restant. Le stock se crédite une seule fois, au retour.

**Contrat du jour (règles E4, F7).** Sur la parcelle du joueur, à côté de sa tour : une verrière de 40 vitres, une fois par jour UTC, faisable seul, ouverte à partir de r3 ≥ 1 (R vaut alors au moins 12 pièces par seconde). Le joueur y va par un bouton (« Contrat du jour »), sa nacelle s'y déplace ; aucun visiteur n'y monte. Ses vitres rapportent leur gain normal et comptent dans le budget de 40 par minute ; la raclette motorisée y marche. Récompense à la dernière vitre : 10 minutes de revenu (600 × R, R lu à cet instant), une seule fois par joueur et par jour. Compte à rebours du prochain contrat visible depuis la nacelle et sur le panneau de la place.

**Bonus cumulables (règle E5).** Un seul bonus multiplicatif temporaire existe : la mousse (§ 4), +25 % sur le gain de l'action, non cumulable avec elle-même, plafonnée par jour et par partenaire. Plafond total des bonus temporaires : × 1,25.

## 3 ter. Décisions d'état (réponses à M01–M09)

| # | Décision |
|---|---|
| M01 Cadence | Budget de **40 vitres par minute et par joueur** (identifiant de compte), sur une fenêtre glissante de 60 secondes, partagé entre lavage manuel, raclette motorisée, sa tour, la tour d'un autre et le contrat. Une vitre exige trois passes et 1,5 seconde au moins ; toute vitre vaut une unité. Une passe = un tapotement, ou un glissement du doigt sur au moins la moitié de la largeur de la vitre ; les deux comptent pareil. Les 2 secondes par vitre du profil actif comprennent le glissement vers la vitre suivante (0,3 seconde au plus) et la montée d'un étage (0,4 seconde), pendant lesquels le toucher suivant est déjà accepté. Les budgets des joueurs sont indépendants. |
| M02 Revenu de référence | R défini au § 3 bis, sans aucune récompense dans sa propre base. Chaque pourboire consomme son quota en minutes de revenu au taux du moment (pièces ÷ (60 × R)) ; une hausse de R ne recrédite rien. Tant que R est inférieur à 1 pièce par seconde, les quotas de pourboires se calculent avec R = 1 : un débutant peut recevoir jusqu'à 600 pièces de pourboires par jour. La mousse se compte en temps, pas en revenu (M06). |
| M03 Jour | Jour UTC du serveur. Contrat, quotas de pourboires et de bonus de mousse sont enregistrés par compte et par jour, et survivent à un changement de serveur. Un contrat commencé avant minuit et fini après compte pour le jour où il est fini. |
| M04 Machine d'état d'un robot | Achat (débit) → chantier → **en service**. Seuls les robots en service produisent et comptent pour les déblocages et les jalons, par tous les chemins, payants ou non. Une mise en service n'arrive qu'une fois. |
| M05 Offres | Les cinq offres sont des passes durables, non cumulables avec elles-mêmes, relues à chaque connexion. « Chantiers express » s'applique aux chantiers lancés après l'achat. « Raclette motorisée » marche sur sa tour, sur celle d'un autre et sur le contrat, par le même chemin de validation que le lavage manuel, et s'arrête dès que le joueur quitte sa nacelle. Elle lave une vitre toutes les 2 secondes (30 par minute), dans le budget commun ; elle ne marche pas depuis la seconde place d'un autre joueur tant que le visiteur ne possède pas lui-même la passe (la passe suit le compte, pas la nacelle). Avec ou sans elle, la nacelle glisse seule vers la vitre sale suivante de la rangée dès qu'une vitre est finie ; s'il n'en reste aucune, elle attend (tour étincelante, puis pigeons). |
| M06 Mousse | Fenêtre de 10 secondes, **seule durée de la mousse** : elle dure tant que les deux laveurs finissent chacun une vitre à moins de 10 secondes d'écart, chaque vitre finie repoussant l'échéance sans cumuler. Quota en **temps de bonus effectif** : 600 secondes par joueur et par jour, dont 300 au plus avec un même partenaire (l'autre occupant de la nacelle). Seul le temps réellement écoulé est débité, sans double compte. **Quota atteint : le +25 % s'arrête, la mousse reste à l'écran** tant que le duo lave ; un petit texte dit « Bonus de mousse du jour atteint ». Le pourboire du propriétaire se calcule sans mousse. La mousse ne touche ni les robots ni R. |
| M07 Stock et état d'une tour | **Une vitre lavée reste propre.** État enregistré d'une tour : son numéro, le nombre de **rangées finies**, et un **masque de 5 bits** pour la rangée en cours. Les rangées se finissent dans l'ordre, de bas en haut ; dans la rangée en cours, les vitres se lavent dans n'importe quel ordre. Au retour, la tour est comme le joueur l'a laissée, vitre par vitre. Zone salie par les pigeons : même représentation (numéro de cycle, première rangée, rangées finies, masque), une seule zone à la fois, lavée de bas en haut. Chaque vitre n'est créditée qu'une fois par cycle de saleté, à celui qui la finit ; une vitre déjà finie est refusée sans effet. Un nouveau cycle ne naît que de deux événements montrés : les pigeons et le déménagement. **Deux laveurs au plus par tour** : le propriétaire et l'occupant de la seconde place ; ils lavent la même rangée, le serveur attribue à chacun la vitre sale libre suivante, jamais la même. Si le propriétaire quitte le serveur, le visiteur garde ce qu'il a gagné et retourne à sa tour. Les robots lavent à l'écran les trois autres façades : c'est un décor, sans stock ni crédit. Tant qu'aucun robot n'est en service, elles restent sales. Ensuite elles sont propres jusqu'à l'étage de la nacelle moins un retard de (10 − nombre de paliers de robots possédés) étages : avec un seul palier, les robots suivent 9 étages plus bas ; avec les dix, ils suivent la nacelle. Plus de robots se voit donc sur la tour. Pendant un contrat ou une visite, ils finissent de rattraper la dernière hauteur de la nacelle puis attendent. Contrat du jour : 40 vitres propres à chaque joueur, même représentation. |
| M08 Sauvegarde | **Pendant une session, l'état du serveur en mémoire fait foi** : le profil s'enregistre toutes les 60 secondes, à la sortie du joueur et à la fermeture du serveur, jamais à chaque vitre ni à chaque achat en pièces (une écriture par vitre dépasserait les limites de Roblox dès trois joueurs ; revue du commit `8702805`, S1 et S2). Une coupure brutale du serveur peut faire perdre au plus 60 secondes de jeu. Chaque opération rare et irréversible (crédit hors ligne, prime du contrat, déménagement, segment) porte un identifiant : rejouée, elle ne fait rien. Le crédit hors ligne s'enregistre avec sa consommation dans la même écriture que le chargement. Un futur achat en Robux s'enregistrera avant d'être confirmé (E8) ; un reçu rejoué n'accorde rien. Une seule session par compte. Le stock hors ligne couvre l'intervalle entre l'heure de départ enregistrée et l'heure de retour ; le crédit et la remise à zéro de l'heure de départ s'enregistrent ensemble. Si cet enregistrement échoue, rien n'est crédité et le même intervalle se rejoue à la connexion suivante. Aucune action de vente, de rangement ou de remise à zéro n'existe en v1. L'avancement de la tour, du contrat et de la Flèche fait partie de la sauvegarde ; un déménagement et l'achat d'un segment sont des opérations identifiées comme les autres (rejouées, elles ne font rien). Une vitre finie est créditée et inscrite dans le masque dans la même opération. |
| M09 Nombres | Prix arrondis à l'entier supérieur de coût du premier × croissance^(n − 1), jamais à partir du prix précédent déjà arrondi. Soldes en nombres à virgule double précision, plafonnés à 9 × 10¹⁵ pièces (le plus gros prix de la v1 est d'environ 8 × 10¹² ; au revenu final, le plafond s'atteint plus de 6 heures après la fin du contenu). Affichage abrégé (k, M, Md, Bn). Le remboursement d'un robot se compte à partir de sa mise en service ; le chantier se juge à part. |
| M11 « Chez <visiteur> ! » (D11) | Proposé aux deux occupants seulement si la tour du visiteur a encore des vitres sales. Le premier des deux qui appuie emmène le duo ; le serveur revérifie au clic que la destination a du stock et que les deux sont toujours à bord. Le propriétaire de la tour quittée devient le visiteur de l'autre. Aucun quota n'est remis à zéro par un voyage. Si personne n'appuie, ou si la tour du visiteur est propre elle aussi : pigeons après 10 secondes continues dans la nacelle, comme en solo. |
| M12 Segment acheté après un vol de pigeons (D12) | La zone salie par les pigeons reste, avec ses crédits. Ordre de lavage : la zone des pigeons d'abord, puis le segment neuf. La limite « deux segments non finis » compte les segments achetés pas encore lavés une première fois ; la zone des pigeons n'en fait pas partie. |
| M13 Visiteur à bord quand le propriétaire part au contrat (D13) | Le visiteur est ramené à sa tour avant le déplacement ; son lavage s'arrête, les vitres finies restent créditées ; le bonus de mousse s'arrête ; aucun quota n'est restauré. |
| M10 Pourboire au bord du quota | Le dernier pourboire qui dépasserait le quota du jour ou du partenaire est crédité au prorata de ce qui reste, puis plus rien ce jour-là. Jamais de pourboire refusé en entier pour un dépassement partiel, jamais de dépassement. |

## 4. Boucle sociale

- Taille de serveur visée : 6 joueurs (les deux fiches lues du corpus affichent 5 et 7). Chaque joueur a sa tour autour d'une place centrale.
- Pourquoi inviter un ami (dans le jeu, pas dans un menu) : chaque nacelle a une **seconde place**, vide et éclairée, visible de tous. Un ami y lave **les vitres de cette tour, avec le propriétaire** : deux raclettes sur la même rangée, la nacelle monte deux fois plus vite, et la **mousse** jaillit dès que chacun a fini une vitre : +25 % sur le gain de l'action de chacun (M06).
- **Comment on se rejoint.** Quand un ami Roblox est déjà sur le serveur, le bouton « Rejoindre <ami> » n'apparaît que chez le joueur arrivé en dernier, après sa première rangée (vers 14 s), et seulement si la seconde place de l'ami est libre ; le serveur prend le premier appui, et le bouton disparaît chez les deux. Un toucher, et il est assis à côté de lui (la caméra vole d'une tour à l'autre). Pour les autres joueurs : au pied de chaque tour, une borne s'éclaire quand la seconde place est libre ; après « Descendre », s'en approcher sur la place propose « Monter à bord » (la nacelle n'a pas besoin de redescendre : le joueur y est porté). Une place occupée ne propose rien.
- Ce que chacun y gagne : le visiteur touche son propre gain par vitre (indexé sur ses propres robots) et la mousse ; le propriétaire touche un **pourboire** égal à 50 % de son propre gain par vitre pour chaque vitre lavée par le visiteur, sans mousse, voit sa tour monter plus vite et garde tout son budget de lavage. Plafonds (E5) : pourboires reçus limités à 10 minutes de revenu par jour, dont 5 minutes au plus venant d'un même joueur (prorata au bord du quota, M10) ; bonus de mousse limité à 10 minutes par jour, dont 5 avec un même partenaire. Avec la raclette au maximum, un ami qui lave 30 vitres par minute apporte au propriétaire 9 secondes de revenu par minute : le plafond de 5 minutes s'atteint en 33 minutes d'aide environ.
- La tour du visiteur n'avance pas pendant qu'il aide : c'est le prix de l'aide, payé par la mousse et par le tour suivant. Quand la tour du propriétaire devient étincelante, « Chez <visiteur> ! » emmène le duo sur l'autre tour (§ 3 bis) : on s'aide à tour de rôle.
- Le visiteur descend quand il veut (bouton « Retour à ma tour ») et retrouve sa tour comme il l'a laissée. Une tour sans visiteur ne perd rien.
- La scène qu'on raconte ou qu'on filme, atteignable dans les 5 premières minutes à deux : deux amis dans la même nacelle vers le 30ᵉ étage de la tour 1, une explosion de mousse, la bande de verre propre sous eux, les robots sur les côtés, la place et les autres tours en bas.
- Ce qui se passe si le joueur est seul : rien ne manque. Robots, contrat du jour et toute la progression se jouent seul ; aucun objectif ne dépend d'un autre joueur (F7).

## 5. Monétisation

Règle en une phrase, vérifiable dans le code :

> Aucun achat en Robux ne crédite un solde de pièces, ne multiplie le gain d'une action ou le revenu d'un robot, ni ne relève le plafond de 40 vitres par minute commun à tous : on ne vend qu'un lavage automatique à 30 vitres par minute, du temps de chantier et de l'apparence.

Jeu compétitif (un joueur peut-il nuire à un autre ou le dépasser dans un classement qui compte) : **non**. Aucun vol, aucune perte infligée, aucun classement récompensé. Le tableau des étages lavés du serveur est un affichage sans gain.

| Offre | Type (confort, temps, expression, acces) | Prix conseillé (Robux) | Effet exact | Ce qu'elle ne fait pas |
|---|---|---|---|---|
| Raclette motorisée | confort | 149 | Lave à 30 vitres par minute, tant que le joueur est dans sa nacelle, par la même validation que le lavage manuel. Le joueur peut laver à la main en plus, jusqu'au plafond de 40 vitres par minute qui vaut pour tout joueur, payant ou non | Ne dépasse jamais 40 vitres par minute au total ; ne marche ni hors ligne ni hors de la nacelle ; ne change pas le gain par vitre |
| Chantiers express | temps | 99 | Divise par deux la durée des chantiers lancés après l'achat : les robots produisent plus tôt | Ne saute aucun déblocage ; ne change ni les coûts ni le revenu d'un robot en service |
| Peintures de nacelle | expression | 49 | Les douze couleurs et motifs de nacelle, en un seul lot, sans tirage | Aucun effet de jeu |
| Mousse colorée | expression | 29 | Couleur de la mousse et de la traînée de raclette | Ne déclenche ni ne prolonge la mousse ; aucun effet de jeu |
| Styles de tour | expression | 79 | Verre teinté, néons, enseigne au sommet | Aucun étage, jalon ou gain de plus ; ne masque pas la saleté |

Repère de marché (lu, non jugé) : Throw Food For Animals vend une passe « x2 Cash » à 99 Robux, une passe « x2 Training Power » à 149 Robux et 50 produits de 2 à 12 000 Robux ; Break and Steal an Egg vend 130 produits de 1 à 6 299 Robux. Notre règle exclut ces ventes de monnaie et de puissance. Revenu attendu : `NP`.

## 6. Coût de contenu et de modération

- Objets : 10 robots construits en pièces simples, chacun avec une silhouette propre ; 1 module d'étage et 3 tours générées par répétition (120, 280, 400 étages), plus le segment de la Flèche et sa balise ; 1 nacelle à deux places ; 1 verrière de contrat ; 1 place centrale et son panneau ; 5 aspects de saleté, 3 vitres d'aspect différent ; 1 vol de pigeons ; 1 drapeau ; 1 plaque.
- Niveaux : 3 tours, la Flèche générée, 1 verrière de contrat générée.
- Textes : environ 75 chaînes, en anglais puis en français. Sons : 7 (raclette, étincelle à note variable, pièce, achat, mousse, rangée et palier, pigeons).
- Nombre de pièces borné (P12) : par joueur, seules les 5 vitres de la rangée en cours (et les 5 de la suivante) sont des pièces séparées ; chaque façade tient en deux panneaux, un propre et un sale, dont la hauteur suit l'avancement. Robots : trois modèles visibles au plus par palier, détaillés sur sa propre tour, simplifiés sur celles des autres. Objectif : moins de 1 500 pièces affichées par client à 6 joueurs en tour 3, à mesurer au lot L7.
- Largeur : une vitre fait 5 unités de large et 5 de haut ; la colonne de verre lavée fait 25 unités. Le corps des tours fait 35, 55 et 75 unités de côté (verre au centre, ailes pleines), soit des tours 17, 25 et 27 fois plus hautes que larges.
- Hauteur : 5 unités de monde par étage, soit 600, 1 400 et 2 000 unités pour les trois tours ; la Flèche ajoute 200 unités par segment. La ville est réellement très bas : c'est la promesse de la vignette. Le rendu à cette hauteur (distance d'affichage, brouillard) est à vérifier au lot L7.
- Chaque tour se voit d'en bas et de côté : quatre façades habillées, dessous de nacelle et toit modelés (F10).
- Modération : rien de propre au jeu. Aucun texte libre, aucun nom choisi, aucune création de joueur. Le chat est celui de Roblox.
- Rythme de mise à jour soutenable : une par semaine (un style de tour, un robot décoratif, une verrière de contrat, un aspect de vitre). Les deux gagnants lus en publient 81 et 174 par mois : l'écart est un risque, noté en annexe D.

## 7. Données de marché

Source : `VEILLE\RELEVES\2026-11-15\b1-theme-un-geste.md`. Moyennes de joueurs, pas de pics. Fenêtre de chaque ligne : mois (novembre 2026, 14 jours, contre octobre), semaine (close le 14/11) ou 24 h (lue le 15/11). Donnée absente : `NP`.

| # | Gagnants du thème | Moyenne (fenêtre) | Tendance | Source |
|---|---|---|---|---|
| 1 | Throw Food For Animals | 202 898 (mois) | +1 519 % sur le mois | rostats.io/charts/2026-11 |
| 2 | Break and Steal an Egg | 103 526 (mois) | −0,9 % | idem |
| 3 | +1 Venom Evolution | 29 072 (mois) | +100,4 % | idem |
| 4 | Sweep The Moon | 24 664 (semaine) | +489,0 % sur la semaine | rostats.io/new |
| 5 | Steal A Pet And Ride It! | 23 002 (mois) | +153,2 % | rostats.io/charts/2026-11 |
| 6 | Depth Incremental | 18 072 (mois) | +598,8 % | idem |
| 7 | Cut a Rock | 17 261 (mois) | +1 824 % | idem |
| 8 | Throw a Seed | 12 427 (semaine) | nouveau, 9 jours | rostats.io/new |
| 9 | Build a REAL House | 12 353 (semaine) | nouveau, 26 jours | idem |
| 10 | +1 Power Fruit Evolution | 8 576 (mois) | +1 527 % | rostats.io/charts/2026-11 |

| # | Faibles ou retombés | Moyenne (fenêtre) | Tendance | Ce qui semble leur manquer (hypothèse) | Source |
|---|---|---|---|---|---|
| 1 | +1 Speed Keyboard Escape | 29 701 (mois) | −44,6 % puis −68,1 % | Geste de mode, non renouvelé | rostats.io/charts/2026-10 et 2026-11 |
| 2 | Steal a Brainrot | 88 654 (mois) | −42,9 % | Reprises concurrentes du même geste | rostats.io/charts/2026-11 |
| 3 | Steal An Egg | 846 562 (mois) | −26,1 % puis −36,9 % | Reste premier ; recule depuis son pic | idem |
| 4 | Sell Fries! | 24 564 (mois) | −21,6 % | NP | idem |
| 5 | +1 Stone Skipping | sous 21 921 (mois) | −20 % au moins | Entré puis sorti du top 50 en un mois | idem |
| 6 | Throw Lucky Block For Animals | 1 073 (24 h) | NP sur 30 jours | Reprend le geste du gagnant sans le changer | rostats.io/trending |
| 7 | Dungeon Incremental | 826 (24 h) | NP | idem | idem |
| 8 | +1 Jump Monkey Escape | 721 (24 h) | NP | idem | idem |
| 9 | Throw Food For Clowns | 649 (24 h) | NP | idem | idem |
| 10 | +1 Leviathan Evolution | 553 (24 h) | NP | idem | idem |

Ce que ces données ne disent pas : la chance de réussite d'un geste nouveau (les échecs sous 500 joueurs sont invisibles), la rétention, le revenu, le rôle des vidéos et de la publicité.

## Annexe A — Les 60 premières secondes

Calcul discret : premier geste à 4 s, la vitre k finit à 4 + 2k secondes (aucun angle, aucune vitre double ; la montée d'un étage ne retarde pas la vitre suivante). Les robots paient en continu ; une vitre paie 1 pièce plus 0,2 seconde du revenu des robots. À vérifier au prototype (porte P4).

| Seconde | Ce que voit le joueur | Ce qu'il fait | Ce qu'il gagne |
|---|---|---|---|
| 0–6 | Il apparaît assis dans sa nacelle, au pied de sa tour, le nez sur une vitre brune **déjà lavable**. Une main fantôme glisse dessus. Un seul mot : « Frotte ! » | Glisse le doigt ou tapote : premier geste vers 4 s, traînée de verre propre sous le doigt en moins de 150 ms ; la caméra ne bouge pas | Première vitre finie à 6 s : 1 pièce |
| 6–14 | La nacelle glisse seule vers la vitre suivante ; la note du son monte à chaque vitre | Finit la rangée : 5ᵉ vitre à 14 s | 5 pièces ; un rideau d'eau balaie l'étage et **la nacelle monte au 2ᵉ étage** |
| 14–25 | En bas : « Étage 2 / 120 » et le bouton « Robot 10 » qui se remplit. La 8ᵉ vitre est une fiente | Lave la 2ᵉ rangée (10ᵉ vitre à 24 s), achète le robot ventouse à 25 s (solde : 10) | 3ᵉ étage ; la caméra recule 2 s : le premier robot (0,25 pièce/s) se colle à la façade voisine et se met à la laver, dans le cadre |
| 25–45 | « Robot 12 ». La 17ᵉ vitre est couverte de buée. La seconde place de sa nacelle est éclairée : elle est libre | Lave, achète le deuxième robot à 41 s (solde : 12,40) | 5ᵉ étage à 44 s (20 vitres) |
| 45–60 | « Robot 15 », puis « 3 robots → raclette automatique ». Sous lui, la bande de verre propre ; sur le côté, la façade voisine et ses robots | Achète le troisième robot à 56 s (solde : 16,70), continue de monter | 6ᵉ étage à 54 s (25 vitres), **28 vitres à 60 s**, 3 robots ; l'objectif affiché est la raclette automatique |

Aucun menu, aucun texte de plus de 8 mots avant la première action. Texte le plus long de la minute : « 3 robots → raclette automatique » (4 mots).

Le simulateur compte un revenu continu dès 0 seconde et achète dans l'ordre le plus rentable : robots à 20, 36, 50, 64 et 77 secondes, raclette large à 99 secondes. En jeu, le lavage paie par vitre entière et la première vitre finit à 6 secondes : les trois premiers achats tombent à 25, 41 et 56 secondes, soit 5 à 6 secondes après la simulation. L'interface propose l'achat que le simulateur ferait.

**De 61 à 180 secondes** (la fenêtre que Roblox mesure) : **un étage de plus toutes les 10 secondes, sans exception** : la nacelle arrive au 7ᵉ étage à 64 s, au 13ᵉ à 124 s, au 18ᵉ à 174 s, soit 12 étages nouveaux dans la fenêtre. Robots 4 et 5 vers 1:10 et 1:25 ; raclette large (gain × 2) vers 1:45 ; première raclette automatique (nouvelle silhouette sur la façade de droite) vers 2:20 ; fanfare à l'arrivée au 10ᵉ étage (1:34). Aucun trou de plus de 10 secondes sans événement visible.


## Annexe B — Périmètre

- Boucle principale : laver des vitres → pièces → raclette et robots → étages plus hauts.
- Boucle sociale : seconde place de nacelle (laver à deux la tour de l'un, pourboire, mousse).
- Méta-progression : quatre tours successives (120, 280, 400 étages, puis la Flèche sans fin). Le contrat du jour est une façade de plus de la boucle principale, pas un système.
- **Prototype L0 (porte P4)** : 0 à 180 secondes, tour 1, robots r1 et r2, raclette large, caméra et saisie tactile, une seconde place jouée à 2 clients. Ni contrat, ni Flèche, ni pigeons, ni déménagement, ni offres.
- Exclu de la v1, volontairement : classement mondial, renaissance (prestige), animaux de compagnie, échanges entre joueurs, toute forme de combat ou de vol, météo, quêtes multiples, tirages aléatoires, vente de pièces ou de multiplicateurs, série de connexions quotidiennes.

## Annexe C — Prévisions chiffrées

Le bilan les comparera au mesuré. Les lignes « simulation » viennent de `OUTILS\sim-economie.py` sur les constantes du § 3 bis, profil actif ; elles ne comptent ni le hors ligne, ni le contrat, ni la mousse, ni les pourboires : un joueur qui fait son contrat chaque jour finit plus tôt (la contre-vérification n° 3 a calculé 97 min sans prime ; la prime du contrat seule raccourcit de quelques minutes, à mesurer en QA).

| Prévision | Valeur | D'où vient-elle |
|---|---|---|
| Temps jusqu'à la première action | 4 s (première vitre finie à 6 s) | Annexe A : apparition dans la nacelle, vitre lavable dès 0 s |
| Première montée d'un étage | 14 s | Annexe A : 5 vitres |
| Étages lavés à 60 s | 5 étages finis, nacelle au 6ᵉ | Annexe A : 28 vitres |
| Étages nouveaux entre 61 et 180 s | 12 (un toutes les 10 s) | Annexe A |
| Premier achat | 20 s en simulation, 25 s en jeu | 10 pièces à 0,5 pièce/s ; en jeu, la dixième vitre finit à 24 s |
| Plus long intervalle sans événement visible, de 61 à 180 s | 10 s | Annexe A |
| Stock de vitres le plus tendu | tour 1 à 40 vitres par minute : 575 lavées pour 600 | § 3 bis, calcul de la contre-vérification n° 3 |
| Segment de la Flèche (profil actif) | financé en 3 min 51 s à 6 min 55 s, lavé en 6 min 40 s ; 9 min au plus sans laver | § 3 bis, calcul |
| Segments financés par une réserve hors ligne pleine | 7 premiers, ou 6 au prix de 9 minutes | § 3 bis, calcul |
| Écart maximal entre achats, 0 à 10 min | 61 s | Simulation (seuil : 120 s) |
| Écart maximal entre achats, 10 à 60 min | 332 s | Simulation (seuil : 480 s) |
| Écart maximal entre achats, après 60 min | 378 s | Simulation (seuil : 900 s) |
| Remboursement le plus long d'un exemplaire | 219 s (247 s pour le profil lent) | Simulation, 10ᵉ nacelle robot, revenu direct et supplément de lavage compris (seuil : 300 s) ; 285 s en ne comptant que le revenu direct |
| Tour 2, tour 3 | 16 min, 51 min | Simulation (15:33 et 50:52) |
| Durée de contenu actif | 97 min (107 min pour le profil lent) | Simulation (seuil : 90 min) |
| Part du revenu venant du geste, en fin de jeu | 23 % (actif), 13 % (lent) | Simulation |
| J1 attendu | 8 % | Aucune donnée de marché (`NP`) ; valeur du seuil de la porte P7, posée comme objectif |
| Fin de la tour 3 pour un joueur d'une demi-heure par jour | jour 3 ou 4 (`NP` mesuré) | 97 min de contenu actif, réservoir hors ligne en plus ; la Flèche prend la suite |
| Durée de session attendue | 10 min | Seuil P7 à 8 min ; RoStats estime 19 et 20 min pour deux gagnants du thème (estimation du site) |
| Nombre de lots de production | 10 | Lots L0 à L9 de la procédure 05 |

## Annexe D — Critères d'arrêt

Ce qui, observé en bêta, ferait abandonner ce jeu :

1. Plus de 50 % des entrants partent avant 60 secondes, après deux corrections de l'arrivée.
2. Moins de 20 % des joueurs achètent le troisième palier (bras articulé) : le geste ne tient pas dix minutes.
2 bis. **Arrêt ferme au prototype (porte P4), condition de la dérogation de P3.** L'idée est abandonnée sans nouvelle itération si l'une de ces mesures échoue, au format téléphone : (1) latence contact → traînée de plus de 150 ms sur plus d'une vitre sur 20 ; (2) une rotation de caméra pendant 20 glissés commencés sur la vitre ; (3) moins de 25 vitres lavées à 60 s ou première montée après 20 s, par le relecteur sans aide ; (4) moins de 8 étages nouveaux entre 61 et 180 s, ou une baisse du compteur ; (5) plaisir du geste noté sous 6 par le relecteur de la passe 2, raisons écrites, ou sous 6 par le propriétaire après 3 minutes de jeu s'il y joue. Le seuil n'est pas révisé après la mesure.
3. J1 sous 5 % sur 200 joueurs organiques après deux corrections de la boucle.
4. Session médiane sous 4 minutes.
5. La cadence d'une mise à jour par semaine ne suffit pas à tenir une moyenne de joueurs stable sur 30 jours, et l'usine ne sait pas faire plus.

# Rapport d'économie — Lave la tour (`lave-la-tour`)

- Passe : **1 (papier), contre-vérification n° 3**, fiche v4 ; rôle calcul et adversaire indépendant.
- Agent : **gpt-6.1-sol, effort xhigh**, le 2026-11-16 ; ni auteur de la fiche ni des corrections.
- Entrées exclusivement au commit **4e98dca296dd2bbbf78df7a75794808309c8e735**, par `git show` : garde-fous, AGENTS, procédure 03, règles Économie, seuils, mémoire de l'usine et leçons Économie, gabarits, fiche, JSON, simulation, rapport fusionné et contre-vérification 2. `ETAT.json` lu pour distinguer la dérogation historique du présent verdict.
- Références **F:L…** : `JEUX/lave-la-tour/02-concept/FICHE-CONCEPT.md` ; **S:L…** : `OUTILS/sim-economie.py`, au commit ci-dessus. Autres références : fichier et section nommés.
- Preuves : **lus et calculs locaux**, aucun constat en jeu. Aucun Studio, navigateur, réseau, sous-agent, installation ou commit. Sources, JSON, simulation et outils non modifiés par cet audit.

## Verdict

| Point | Résultat |
|---|---|
| Cadence du modèle de référence, profil actif | **PASSE**, sortie 0 ; `SIMULATION.md` reproduit à l'identique |
| Cadence de la v4, ajouts compris | **ÉCHEC papier** : accès à la Flèche ne garantissant pas le revenu utilisé par ses promesses, F01 |
| Défauts P0 certains | **0** |
| Défauts P1 certains | **1**, F01 ; deux symptômes d'une même cause, comptés une seule fois |
| Autres défauts certains | **2 P2**, F02 et F03 |
| Risques à vérifier en jeu, non comptés parmi les défauts certains | **2 P0, 4 P1, 2 P2**, Q01 à Q08 |
| Décisions manquantes avant le code | **10**, D01 à D10 ; hors deux paramètres du moteur déjà signalés |
| Monétisation / E6 | **Conforme sur papier** ; portée de l'auto au beffroi à préciser, D09 |
| Avis pour la porte P2 | **Retour au concept** ; ne pas reconduire le PASSER de la v3 aux ajouts de la v4 |

La dérogation historique d'`ETAT.json` n'est ni modifiée ni remplacée par ce rapport. Aucun correctif proposé n'est appliqué.

## 1. Faits (lus)

### Transcription et couverture

Comparaison indépendante des tableaux de la fiche au JSON, avec assertions :

| Bloc | Résultat |
|---|---|
| Départ, action, prix entiers | 0 pièce ; gain 1 ; cadence 30 ; indexation 0,2 s ; arrondi supérieur : conformes à F:L94–100 |
| Robots | **10/10 lignes conformes** : identifiant, nom, coût, revenu, croissance, chantier, maximum 10 et déblocage, F:L104–113 |
| Améliorations | **5/5 conformes** : coût, cible, multiplicateur, déblocage, F:L119–125 |
| Profils | Actif ×1 et lent ×0,5 ; même délai moteur : conformes |
| Jalons et fin | `contrats` r3≥1, `tour2` r5≥1, `tour3` r8≥1 ; fin r10≥10 : conformes à F:L127/142 ; renommage de `tranche2` sans changement de condition |
| Offres | 5 noms, types et prix conformes au § 5 ; `competitif:false` conforme à la déclaration de la fiche |
| `apres_contenu` | Condition, R_fin littéral, segment 10 étages/200 vitres et prix : conformes à F:L144–150 |
| `stock_vitres` | 20 vitres/étage, 5/rangée, bande de 5 étages, tours 30/60/100, pigeons 100 après 10 s, deux laveurs, budget 40 : conformes |

**Aucune erreur de transcription trouvée.** Une transcription fidèle peut conserver un défaut de conception : F01.

`apres_contenu` et `stock_vitres` sont **ignorés par le simulateur**. Taches, contrat, beffroi, absence, mousse, pourboires, effets des passes, scènes de déménagement et plafond de solde ne sont pas simulés. Leur absence est déclarée, pas une vérification de leur innocuité. `delai_achat_s` et `duree_max_s` restent omis du JSON, absents de la fiche ; valeurs moteur **3 s** pour les deux profils et **14 400 s**.

### Historique des défauts fermés

| Acquis de la v3 / dernière contre-vérification | État au commit audité |
|---|---|
| Durée, remboursements, valeur du geste (D1/D2, A01/A02) | Fermés **dans le modèle de référence** ; constantes conformes, mêmes résultats |
| Mousse sans quotas, puis décompte ambigu (A03, M06/N04) | **Fermés au papier** : 10 s, temps réellement écoulé sans double compte, 600 s/jour et 300 s/partenaire, F:L171 |
| Arrondi flottant (N05), marginal incomplet (N01) | Fermés : Decimal avant plafond ; revenu direct et action ajoutée, S:L193–204/211–222 |
| Stock disputé v2 (N02), M07/M08 | **Couverture changée** : deux laveurs partagent une tour finie ; pigeons et attribution unique écrits. Pas de pénurie permanente démontrée ; nouveaux cas en D05–D08/Q01/Q04 |
| Annexe A auparavant fermée (D3) | **Réouverte P2** par le nouveau parcours : F03 |
| Rejeu, passes et quotas | Risques d'exécution conservés ; aucun futur code du jeu qualifié |

## 2. Calculs (reproductibles)

### 2.1 Relance figée

Script, seuils, JSON, fiche et simulation extraits par `git show 4e98dca:<chemin>` dans une arborescence temporaire **hors dépôt**. Depuis cette copie :

```powershell
python OUTILS\sim-economie.py JEUX\lave-la-tour\03-economie\economie.json --json
```

**Sortie 0, `echec:false`.** Une sortie Markdown sans `--sortie` reproduit `SIMULATION.md` à l'identique après normalisation des fins de ligne et retrait de la ligne terminale `VERDICT`. Aucun `SIMULATION.md` du dépôt réécrit. Calculs intermédiaires JSON dans `%TEMP%\contre-verification-3-lave-la-tour-wb23syij`.

| Profil | Premier achat | Max 0–10 min | Max 10–60 min | Max après 60 min | Fin de contenu | Achats |
|---|---:|---:|---:|---:|---:|---:|
| Actif | 20 s | 61 s | 332 s | 378 s | **5 829 s = 97:09** | 105 |
| Lent | 40 s | 69 s | 367 s | 421 s | **6 421 s = 107:01** | 105 |

100 robots en service et cinq améliorations ; **0/100 remboursements hors bornes** par profil. Jalons actif : **281 / 933 / 3 052 s** ; lent : **351 / 1 075 / 3 407 s**. Retard lent `(6421−5829)/5829 = 10,156 % ≥5 %`. Valeurs de simulation de l'annexe C conformes.

| Contrôle indépendant | Calcul | Moteur |
|---|---|---|
| Premier achat | `10 / (30/60 × 1) = 20 s` | 20 s |
| Écart initial maximal | À t=410, cash 3,3 ; revenu 102,9/s jusqu'à420, puis118,5/s. À470 : `3,3+10×102,9+50×118,5=6957,3<7000` ; à471 : 7075,8≥7000 | 471−410 = **61 s** |
| r4 n°10 | `ceil(7000×1,14^9)=22764` ; ajouté `80×(1+0,5×3×0,2)=104/s` ; remboursement `22764/104=218,8846 s` | 219 s ; lent `22764/92=247,4348 s` |

Chantier maximal **180 s**, jugé séparément.

### 2.2 R_fin et Flèche

Les 100 robots, a3 doublant r2 et a4×a5=1,875 :

```text
R_fin_exact = 10 × (0,25 + 2×2 + 12 + 80 + 1650 + 34500
                    + 790000 + 19600000 + 520000000 + 15500000000) × 1,875
            = 300 757 992 117,1875 pièces/s.
```

Fiche/JSON choisissent la **constante entière 300 757 992 117**. Écart de 0,1875 pièce/s, relatif ≈6,23×10⁻¹³ ; pas de rupture de cadence. Les prix utilisent la constante écrite. Le prix publié du cinquième est juste.

Équipement complet : `G=3×(1,875+0,2R)=5,625+0,6R` ; total actif `1,3R+2,8125`, lent `1,15R+1,40625`.

| Segment n | Minutes R_fin | Prix en pièces | Financement actif depuis 0 | Financement lent depuis 0 | Lavage actif / lent sans tenaces |
|---|---:|---:|---:|---:|---:|
| 1 | 5 | 90 227 397 635 100 | 230,77 s (3:51) | 260,87 s (4:21) | 400 / 800 s |
| 2 | 6 | 108 272 877 162 120 | 276,92 s (4:37) | 313,04 s (5:13) | 400 / 800 s |
| 3 | 7 | 126 318 356 689 140 | 323,08 s (5:23) | 365,22 s (6:05) | 400 / 800 s |
| 4 | 8 | 144 363 836 216 160 | 369,23 s (6:09) | 417,39 s (6:57) | 400 / 800 s |
| ≥5 | 9 | **162 409 315 743 180** | 415,38 s (6:55) | 469,57 s (7:50) | 400 / 800 s |

« 7:50 » lent est le **maximum**, pas le premier financement. Lavages 6:40/13:20 supposant 200 ordinaires : tenaces au §2.4.

**Ne pas additionner systématiquement financement et lavage** : les robots produisent pendant le lavage et le solde se conserve. Équipement complet : même sans action, prix maximal financé en **540 s**, lavage400/800 s ; pas de dépassement900 s démontré. Un segment est utile : 10 étages lavables et un record visible. E3 concerne les générateurs, pas un remboursement financier de ces segments.

Ces divisions à revenu constant ne sont pas les instants réels des achats. Le moteur finit déjà avec **52 724 450 083 615,55 / 47 321 365 804 561,57** pièces actif/lent : au même revenu, premier segment après **95,92 /124,05 s** supplémentaires. Stock et file d'achat à préciser.

### 2.3 Tours et stock

En continu sans détour : `D=durée×cadence/60`, réserve `S−D`, marge publiée `100×(S/D−1)` ; cette marge n'est pas le pourcentage du stock restant.

| Profil / tour | Intervalle simulé | D, ordinaires équivalentes | Réserve | Marge sur D | Stock restant |
|---|---|---:|---:|---:|---:|
| Actif1 | 0→933 s | 466,5 | 133,5 | 28,62 % | 22,25 % |
| Actif2 | 933→3052 s | 1 059,5 | 140,5 | 13,26 % | 11,71 % |
| Actif3 | 3052→5829 s | 1 388,5 | 611,5 | 44,04 % | 30,58 % |
| Lent1 | 0→1075 s | 268,75 | 331,25 | 123,26 % | 55,21 % |
| Lent2 | 1075→3407 s | 583 | 617 | 105,83 % | 51,42 % |
| Lent3 | 3407→6421 s | 753,5 | 1 246,5 | 165,43 % | 62,33 % |

Les **467/1060/1389** publiées sont ces quantités arrondies. Le28% de tour1 s'obtient après arrondi de466,5 à467 ; sans cet arrondi intermédiaire :28,62%. Pas de défaut de stock nominal. Les fractions sont des équivalents continus, pas des vitres réellement partiellement créditées.

**Stress aux mêmes durées que les jalons actifs publiés**, avant effet des revenus sociaux :

| Laveurs, cadence totale | Tour1 demande / réserve | Tour2 demande / réserve | Tour3 demande / réserve |
|---|---:|---:|---:|
| 1×30/min | 466,5 / +133,5 | 1059,5 / +140,5 | 1388,5 / +611,5 |
| 1×40/min | 622 / **−22** | 1412,67 / **−212,67** | 1851,33 / +148,67 |
| 2×30/min | 933 / **−333** | 2119 / **−919** | 2777 / **−777** |
| 2×40/min | 1244 / **−644** | 2825,33 / **−1625,33** | 3702,67 / **−1702,67** |

Déficits du stock **initial**, pas pénurie permanente avec pigeons. À 2×40, les600 vitres initiales tiennent **450 s**, chaque nouveau lot100 tient **75 s**, puis10 s à vide. Débit soutenable après stock initial : `100/(100/80+10/60)=70,59/min`. À 2×30 :54,55/min ; seul40 :37,5/min. Attentes répétées mais chacune≤10 s si correctement implémentée.

Sur les trois durées publiées à 2×40, calcul de stock : **6/15/15 vols**, **60/150/152 s** cumulées à vide, **1164/2625,33/3500** vitres lavées (dernière attente parfois partielle). Ce n'est pas une simulation sociale : ses revenus changent aussi les jalons.

Diagnostic moteur à **40 unités/min**, sans stock/bonus : tour2 **862 s**, tour3 **2864 s**, fin **5507 s** ; consommations théoriques **574,67/1334,67/1762**. La tour2 demande encore des pigeons. Les durées à 30/min ne sont pas celles du profil40.

Le tableau suppose un départ immédiat et omet la scène de **20 s**. Le joueur pouvant rester, ce sont des fenêtres financières, pas des durées maximales sur une tour. Contrat/beffroi remplacent des actions sur sa tour, ne s'y ajoutent pas ; tenaces : D01.

### 2.4 Taches tenaces : budget neutre, temps à préciser

À R gelé, une ordinaire donne G pour une unité, une tenace **2G pour deux unités** : gain par unité identique, plafond **40G/min**. Aux minima serveur, `G/1,5=2G/3` : même **gain maximal par seconde de frottement**. Pas de dépassement certain du budget.

L'égalité pour tout rythme n'en découle pas : ordinaire en **2 s** contre tenace en **3 s**, deux durées autorisées, donnent `G/2` contre `2G/3`, soit **+33,33 %** pendant la tenace, avant déplacements. À rythme de passes identique, elle prendrait 4 s et serait neutre. Cette relation au profil nominal n'est pas définie.

Avec exactement une tenace sur vingt, hors déplacements :

- **30 vitres physiques/min** font **31,5 unités et 31,5G/min**, +5 % de gain d'action face au modèle 30G ; autre hypothèse économique.
- **30 unités/min**, hypothèse conservant le gain du moteur, font `30/1,05=28,57` vitres physiques/min. Un segment de200 vitres dont dix tenaces exige **210 unités** : **7:00 actif /14:00 lent**, au lieu de6:40/13:20.
- Beffroi600 dont trente tenaces : **630 unités**, **21/42 min**, minimum **15:45** au plafond40. Sans tenaces :20/40 min, minimum15 min.
- Contrat40 dont deux tenaces : **42 unités**, **84/168 s**, minimum63 s. Sans tenaces :80/160 s, minimum60 s.

Ce sont des cas à fréquence exacte, pas une distribution garantie sur chaque lot. F02/D01–D03 : impossible de transposer à la fois le revenu neutre et toutes les durées physiques publiées sans préciser l'unité. Même le segment lent à14 min reste sous15 min à équipement complet.

### 2.5 Annexe A : achats et hauteur

Contrôle : ordinaires, première fin à6 s puis `6+2k`, achats prescrits25/41/56 s, robots crédités continûment ; prix10/12/15, aucune amélioration de raclette dans la minute.

| Instant | Solde juste avant achat | Conclusion |
|---|---|---|
| 25 s | 10 vitres à6,8,…,24 → **10 pièces** | Premier achetable |
| 41 s | `8×1,05+16×0,25 = 12,40` | Deuxième achetable ; reste0,40 |
| 56 s, sans angle | `0,40+7×1,10+15×0,50+1,10 = 16,70` | Troisième achetable ; reste1,70 |

À54 s :25 vitres ; sans angle28 à60 s et solde7. **Les achats sont finançables**, même après l'angle : sans tenace, avec1,2 s après la25e, le solde à56 vaut **15,60**, suffisant pour15.

Mais F:L75 impose cet angle : après la25e à54 s, les suivantes finissent à **57,2/59,2/61,2 s**. À60 s : **27**, pas28. Avec la20e tenace en3 s :25e à **55 s**, puis26e à **58,2**,27e à60,2 ; donc **26 physiques /27 unités** à60. Trois achats encore possibles (soldes avant achat10/12,40/16,70).

La montée reste plausible :5 vitres à14 s,10 à24 s,20 à44 s sans tenace. Ce sont **cinq rangées d'une façade**, pas cinq étages entièrement lavés sur quatre faces. Une bande complète vaut **100 vitres**, pas25 : « finit la bande vers54 s » doit devenir « finit la première façade de la bande ». F03.

### 2.6 Récompenses, quotas, retour d'absence

**R** est correctement défini, F:L152 : robots en service, permanents inclus, **sans** vitres, primes, mousse, pourboires. Beffroi : R à la dernière vitre ; règle générale identique pour le contrat. Aucune récompense dans sa propre base.

| Source | Attribution/plafond | Condition |
|---|---|---|
| Contrat | **600R**, une fois/jour UTC | 40 vitres personnelles, gain normal, budget commun |
| Beffroi | **1800R**, une fois/semaine ISO UTC | 600 personnelles sauvegardées, gain normal, budget commun ; reset lundi annoncé |
| Hors ligne plein | **3600R_départ** | 7200 s ×50 % ; robots construits pendant l'absence exclus jusqu'au retour |
| Pourboires | **600R** par jour dont **300R** par partenaire à R gelé | 50 % du G du propriétaire sans mousse ; quota en minutes au taux courant, plancher `max(R,1)` |
| Mousse | +25 % action ; **600 s/jour,300 s/partenaire** | Fenêtre10 s, sans cumul ; aucun effet sur R |

À R_fin exact : contrat **180 454 795 270 312,5**, beffroi **541 364 385 810 937,5**, réserve **1 082 728 771 621 875** pièces, sous 9×10¹⁵.

À équipement complet, un visiteur30 unités/min donne au propriétaire `30×(2,8125+0,3R)=84,375+9R` par minute : plafond partenaire atteint en **≈33:20** ; à 40/min **≈25 min**. Avec deux comptes seulement, chaque receveur reste à **5 min de pourboires** de ce partenaire et **300 s de mousse** ; échanger les rôles ne crée pas un nouveau partenaire. Recevoir10 min demande au moins deux identités aidantes, successivement puisqu'il n'y a qu'une seconde place. Le plancher à faible R est une exception bornée, pas un crédit immédiat de600 pièces.

Mousse600 s à 30 unités/min, R gelé, équipement complet : `(0,25×0,3R)×600=45R`, soit **0,75 minute de R**, plus421,875 pièces de base. Avec un partenaire : moitié, **0,375 minute**, plus base. Une tenace double gain et poids : même borne par unité.

À état final gelé, réserve+contrat+beffroi+quotas sociaux pleins = **110,75 minutes de R**, hors base et gains normaux du lavage. Il faut le travail et plusieurs partenaires correspondants : ce n'est pas une prime immédiate de retour. Ancien total sans beffroi80,75 min.

**« Six segments » n'est pas un nombre exact universel.** À R_départ=R_fin et sans les revenus ultérieurs, coûts cumulés des premiers : **5,11,18,26,35,44,53,62 minutes**. Réserve60 min : **sept** premiers, pas huit ; à partir du segment5 : **six** de9 min, reste6 min. Achats/lavages un par un selon la file, sans droit d'acheter six simultanément. À R_départ<R_fin, six ne sont plus garantis : F01.

**Diagnostic de cumul, hors verdict officiel.** Rejeu jetable de la boucle du simulateur ; actions affectées aux tâches, sans second gain sur la tour :

| Parcours actif, sans tenaces ni trajet supplémentaire | Injection unique | Fin |
|---|---|---:|
| Contrôle sans prime | Aucune | **97:09**, officiel retrouvé |
| Beffroi seul commencé à281 s | À1481 : `1800×26193,75 = 47 148 750` | **93:09** |
| Même beffroi, attribution retardée30 s | Même prime à1511 | **93:33** |
| Contrat puis beffroi | Contrat361 : **31 050** ; beffroi1561 : **419 748 750** | **86:32** |

Dernière ligne : `40+600=640` unités en **1280 s**,30/min, sans double action ; R du contrat51,75/s, R du beffroi233193,75/s. Ceci **ne prouve pas une faille du code ni une violation du seuil90 min du modèle de référence**, qui exclut explicitement les primes. Cela prouve que97 min n'est pas une durée garantie pour tous les parcours actifs v4. Le beffroi seul ne casse pas90 min dans ce diagnostic ; mesurer les cumuls, déplacements et tenaces réels en QA.

### 2.7 Règles E1 à E15 et seuils

| Règle/seuil | Jugement |
|---|---|
| E1,E2 ; écarts120/480/900 s | Modèle initial conforme ; Flèche équipée conforme au calcul ; **état d'accès incomplet en échec F01**. Attente pigeon10 s n'impliquant pas un trou d'achat15 min. |
| E3 ; remboursement30–300 s, chantier≤180 s | 100/100 conformes par profil ; un segment sans revenu propre n'est pas un générateur. |
| E4 | Contrat/beffroi en minutes de R défini, pas en fraction de cash. |
| E5,E15 | Mousse×1,25, temps/jour/partenaire et pourboires/jour/partenaire écrits ; pas de robinet illimité certain à deux comptes. Neutralité temporelle des tenaces à préciser, F02. |
| E6 | Auto30, plafond commun40, temps de chantier, apparence ; record sans gain. Aucun pouvoir contre autrui démontré au papier. |
| E7 | M04/M05 imposent service et même validation payant/gratuit ; portée beffroi et poids tenace à préciser, D01/D09/Q05. |
| E8 | Identifiants et sauvegarde avant confirmation écrits ; nouveaux segments/primes/avancements en Q01/Q02. |
| E9 | Aucun enjeu de perte nouveau. Déménagement prévu, scène sans crédit ; aucun retrait d'enjeu démontré. Concurrence scène/pigeons en D06/D07. |
| E10,E11 | Commit unique et relecteur indépendant ; acquis v3 ne dispensant pas du nouvel audit. |
| E12 | Réserve2 h à50 %, R de départ et crédit unique cohérents ; **six segments non garantis par l'accès actuel**, F01. |
| E13 | Aucun objet aléatoire payant ajouté. |
| E14 ; retard≥5 % | **10,156 %** dans le modèle ; unité nominale à expliciter avant transposition aux tenaces. |

## 3. Défauts

Gravités du mandat : P0 bloque ou perd des données ; P1 casse une promesse du jeu ou un seuil ; P2 gêne ; P3 détail. Une décision manquante n'est pas un exploit futur certain.

| ID | Gravité/statut | Chemin et fait lu | Preuve chiffrée | Correction minimale proposée | Coût ou revenu touché ? |
|---|---|---|---|---|---|
| **F01** | **P1 certain, papier** | Flèche ouverte par r10≥10, sans imposer100 robots ni5 améliorations ; prix basés sur l'équipement complet (F:L127/142–149). Acheter3 de r1 à r9,10 r10, aucune amélioration, poursuivre les segments≥5 sans prime sociale/quotidienne disponible : état légal. | `R_min=3×Σ(revenus r1…r9)+10×15500000000=156621278732,75`. À 30 unités/min : total `1,1R_min+0,5=172283406606,525/s` ; financement **942,69 s >900**. Même au plafond40 sans mousse : `(17/15)R_min+2/3`, financement **914,96 s >900**. Un solde fini peut masquer quelques écarts, pas soutenir indéfiniment un achat/900 s. Réserve pleine : **31,2453 min de R_fin**, soit **4** premiers segments (26 min,5e à35) ou **3** au tarif9, pas six. | **Ouvrir la Flèche seulement avec100 robots en service et5 améliorations**, et annoncer « au moins six segments financés par une réserve pleine à cet équipement ». | **Non** : condition d'accès et texte ; prix/revenus conservés. |
| **F02** | **P2 certain, calcul** | Neutralité seconde confondue avec neutralité du budget ; tenaces non réconciliées avec les cadences/durées physiques, F:L79/96/148/166. | `G/2` contre `2G/3` : **+33,33 %** pendant deux gestes autorisés ; aux minima1,5/3 s, égalité exacte et pas de dépassement40 unités. À5 % tenaces : **210 unités/200 vitres**,7/14 min si30/15 sont des unités. | **Définir30/15/40 et l'auto en unités pondérées, annoncer l'égalité par unité et du maximum temporel, recalculer les durées physiques avec les tenaces.** | **Non** : gain unitaire et×2 conservés ; unité de cadence/prévisions précisées. |
| **F03** | **P2 certain, annexe A/C** | «28 vitres à60 s» omet l'angle après25 ; «bande»25 contredit100 au parcours, F:L75/247–259/278. | Sans tenace :25e à54 puis57,2/59,2/61,2 → **27** à60. Tenace20 en3 s : **26 physiques/27 unités**. Achats25/41/56 finançables ; premier achat≤60 s conservé. | **Écrire27 dans le cas fiente sans tenace, cinq rangées d'une façade, inclure l'angle1,2 s et présenter le cas tenace séparément.** | **Non** : chronologie/vocabulaire, ni prix ni revenu. |

**Précision F01.** Les 97:09 du profil optimal restent justes : il acquiert effectivement tout. Le défaut porte sur la promesse générale attachée à un accès autorisant un équipement incomplet. Même un état moins extrême, **100 robots et toutes les améliorations sauf a5**, donne R=0,8R_fin : réserve **48 min de R_fin**, seulement **cinq** segments au tarif maximal. Aucune faute du futur code supposée.

## 3 bis. Décisions manquantes dans la fiche

**10 décisions distinctes** ; l'accès actuel n'est pas une décision manquante : il est écrit mais à corriger, F01.

| ID | Décision à écrire | Pourquoi elle change le résultat |
|---|---|---|
| **D01** | Unité des cadences30/15 et de l'auto30 : physiques ou unités pondérées ; relation de durée ordinaire/tenace au rythme nominal. | Revenu d'action, délai du segment, débit du payant ; F02. Le plafond40 pondéré est déjà décidé. |
| **D02** | Distribution des tenaces : garantie par lot ou fréquence ; première minute/contrat/beffroi/segments ; conservation du type au retour/pigeons. | Conversion de200/600 physiques en unités, prévisions et effet d'un rechargement. |
| **D03** | Temps du parcours : les2 s incluent-ils chaque glissement/montée ; comment inclure1,2/1,5 s dans30/min ? | Évite de compter deux fois ou d'omettre le déplacement ; chronologie unique à rejouer, F03. |
| **D04** | «Un seul segment acheté d'avance» : un seul sale au total, ou un en attente en plus du segment courant ; disponibilité de l'achat suivant. | File, achats et stock disponible. |
| **D05** | Pigeons sur Flèche : bande resalie lorsque le segment est propre mais le suivant non financé, ou lorsqu'un segment acheté attend. | Travail entre achats ; pas de stock gratuit sur étages non achetés. |
| **D06** | Délai à zéro : temps réel ou présence, autre tâche, sortie de nacelle, reconnexion ; priorité si déménagement/segment pendant le délai. | Début/annulation du vol et portée de la borne10 s. |
| **D07** | Pendant20 s de déménagement : visiteur, finitions engagées, lavage accessible, instant de changement de tour. | Ni crédit sur scène gratuite ni abandon d'action consommée ; bouton répété. |
| **D08** | Sauvegarde des deux voisines finies hors ordre et d'une bande resalie : préfixe+exception, ou identifiants par vitre/cycle. | Un seul dernier numéro ne représente pas un trou :12 finie avant11, reprendre à13 saute11 ; reprendre à11 sans autre état peut repayer12. Choisir la représentation, sans supposer un futur mauvais choix. |
| **D09** | Auto et seconde place au contrat/beffroi ; si aide permise, stock, crédit et pourboire correspondants. | M01 nomme le beffroi, M05 ne l'ajoute pas à la portée détaillée de l'auto ; façade personnelle n'indiquant pas si un visiteur peut aider. E7/quotas concernés. |
| **D10** | Dernier pourboire au bord du quota : proratisé ou refusé entier, notamment sur tenace. | Quota en minutes décidé, attribution atomique supérieure au reste non décidée. |

Ne sont pas relistés : identifiant du crédit, session unique, jour UTC, exclusion des primes de R et des robots construits pendant l'absence. Les deux paramètres omis du moteur sont signalés au §1, séparément des dix décisions de produit/état.

## 4. Propositions

**Non appliquées** ; aucun seuil modifié.

| Paramètre/texte | Actuel | Proposition | Vérification |
|---|---|---|---|
| Accès Flèche | r10≥10 | 100 robots en service et5 améliorations | **Effet calculé, hors outil** : R=R_fin exact ; prix maximal financé même sans action en≈540 s<900. Réserve3600R≥6×540R_fin. Ni coût ni revenu modifié. |
| Cadence/tenace | Vitres/min, neutralité seconde sans convention complète | Unités pondérées et égalité par unité/maximum temporel | **Calcul** : revenu nominal du moteur conservé ;200 physiques avec5 % tenaces→210 unités ;7/14 min<15. |
| Annexe A/C | 28 à60 ; bande25 | Cas sans tenace27, cas tenace séparé ; façade de bande | **Calcul discret §2.5** : achats25/41/56 encore possibles. |

F01 touche un bloc que l'outil ignore : relancer le même simulateur ne qualifierait pas sa correction. Les constantes de base restent identiques, le contrôle officiel est déjà reproduit. Réduire des prix ou augmenter les revenus serait une autre correction, non proposée ici.

Leçon proposée : `CONNAISSANCES/PROPOSITIONS/2026-11-16-contre-verification-3-cadence-hors-modele.md` : couvrir les états autorisés d'une nouvelle boucle même sans changement de constantes des robots. Validation laissée à l'orchestrateur.

## 5. Scénarios pour la QA

Aucun risque ci-dessous compté comme défaut certain de l'implémentation.

| ID | Gravité si reproduit | Scénario et attendu |
|---|---|---|
| **Q01** | **P0** | Deux laveurs, voisines11/12 ; finir12 avant11, déconnecter le propriétaire puis arrêter le serveur ; recommencer après pigeons. Aucun gain perdu, vitre sale sautée ou vitre payée repayée au retour ; visiteur renvoyé avec ses gains. |
| **Q02** | **P0** | Rejouer identifiants de finitions, segment, déménagement, primes et réserve ; échec de sauvegarde avant/après confirmation, changement de serveur, dimanche23:59:59→lundi. Un effet par identifiant/période ; solde, consommation et progression cohérents ; pas de trophée/tour dupliqué. |
| **Q03** | **P1** | A/B : mousse jusqu'à 300 s, pause/rotation places/rôles/reconnexion ; C jusqu'à600 s. Pourboires A←B5 min puis A←C10 min au total ; hausseR, R<1, D10, minuit. Aucun quota restauré par rôle/serveur/R ; mousse non empilée, R inchangé. |
| **Q04** | **P1** | Épuiser le stock à deux au plafond sur plusieurs cycles ; tenter vol avant zéro, changer de tâche/déménager à9,9/10 s, répéter le bouton. Un seul vol100 au bon cycle, aucun stock réservé/attente durable, aucune pièce pour scène de déménagement. |
| **Q05** | **P1** | Auto+manuel, ordinaire/tenace, chez soi/visiteur/contrat/beffroi selon D09, sortie de nacelle/reconnexion. Validation commune, crédit unique, poids2, total≤40 unités/60 s et auto conforme D01. Express ne saute ni service ni déblocage. |
| **Q06** | **P1** | Acheter/laver5 segments, préfinancer à limite D04 ; relaver dix fois une bande de pigeons, changer de serveur, rejouer fin de segment. Record=10×segments achetés et entièrement lavés une première fois, pas de hauteur issue du relavage. Tester aussi le refus de l'état F01 si sa correction est retenue. |
| **Q07** | **P2** | Visiteur débutant, immobile en seconde place, tentative sur place occupée, départ du propriétaire. Aucun vol/double gain, retour sur sa tour ; observer l'accès d'un ami lorsque la place reste occupée. L'aide lavant le stock du propriétaire est prévue, pas un vol certain. |
| **Q08** | **P2** | Première minute avec/sans tenace, achats et angles ; contrat40 puis beffroi600, temps et primes au R exact de fin. Sauvegarde/reset annoncé ; comparer aux diagnostics sans présenter86:32 comme une mesure en jeu. |

### Bilan d'adversaire

- **Deux comptes** : accélération et pourboires prévus, bornés ; rôles échangés ou tour lavée plus vite ne sont pas à eux seuls un exploit.
- **Pigeons à volonté** : aucun déclencheur arbitraire écrit ; stock épuisé, attente puis lavage soumis au budget. Relavage payé prévu ; aucun segment/record supplémentaire ne doit en découler.
- **Déménagement répété** : aucun droit écrit à plusieurs tours neuves pour un jalon ; duplication conditionnée à une faute d'état, à tester.
- **Visiteur épuisant le stock** : progression réelle, gain propre et pourboire au propriétaire, puis pigeons. Pénurie initiale chiffrée, pas de perte de données démontrée.
- **R_fin non possédé** : **F01 démontré**, sans hypothèse de faute de code.
- **Beffroi/contrat** : aucune multiplication des40 unités ; primes accélérant légitimement les achats. Référence97 min ne couvrant pas le cumul.
- **Sauvegarde d'une tour** : obligation écrite, représentation à préciser pour finitions hors ordre/cycles, D08 ; Q01 avant validation.

Écriture limitée au présent rapport et à la proposition. Sources protégées contrôlées après écriture. Des changements externes sont apparus ailleurs pendant la revue : ni utilisés comme entrées, ni modifiés, ni annulés.

RESULTAT: echec | JEUX\lave-la-tour\03-economie\RAPPORT-ECONOMIE-contre-verification-3.md | cadence modèle PASSE, v4 ÉCHEC papier ; 0 P0, 1 P1 certain ; 10 décisions manquantes.

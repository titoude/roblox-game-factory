# Rapport d’économie — Lave la tour (`lave-la-tour`)

- Passe : papier, **contre-vérification 1**, fiche v2 ; agent indépendant **gpt-6.1-sol, effort xhigh**, le 2026-11-16.
- Entrées figées : commit **b4905a2be8a78de050a6f8f60a09210ff4b63917** ; fiche v2 et rapports calcul/adversaire de passe 1. Références `F:L…` = lignes de cette fiche ; `S:L…` = `OUTILS/sim-economie.py` à ce commit.
- Lus : garde-fous, procédure 03 entière, règles/seuils/Leçons d’Archipel § Économie, gabarits, fiche et deux rapports entiers, simulateur entier. Aucun fait vu en jeu ; certitude = démonstration sur le modèle écrit. Studio, navigateur, réseau, sous-agents, commits et code du jeu hors périmètre.

## 1. Suivi des constats précédents — faits lus et contrôles calculés

« Fermé » concerne le défaut papier précis. « Déplacé → QA » signifie règle désormais explicite, exécution toujours non vérifiée ; cela ne ferme pas un risque en jeu. Une ligne reste ouverte si un de ses points matériels manque.

| ID | État | Référence v2 et motif |
|---|---|---|
| D1 | **Fermé** | § 3 bis, F:L81–106 ; actif **5 830 s ≥ 5 400 s** sans bonus annexes. |
| D2 | **Fermé** | F:L81–90 : croissances corrigées ; **0/100** hors borne dans chaque profil. Le nouveau défaut marginal de l’outil N01 ne recrée pas de dépassement sur cette courbe. |
| D3 | **Ouvert, P2 certain** | Annexe C corrigée pour t=0, mais F:L205–210/226 : **20+8=28**, non 27 ; **36+8=44**, non 43. Le parcours discret peut expliquer ces approximations, pas l’affirmation « tout est décalé des 8 secondes ». |
| D4 | **Déplacé → N04/QA** | R explicite (F:L108–110/121), permanents et attribution définis. Restent R=0 et unité du quota de mousse ; aucune mesure en jeu. |
| D5 | **Déplacé → QA** | Budget agrégé glissant par compte et même validation (F:L120/124/149) ; vérifier effectivement auto+manuel, rejeu, arrêt hors nacelle. |
| A01 | **Fermé** | Même correction que D2 ; r10 n°10 : **272,914 s** de production directe, hors chantier, au lieu de 802,632 s. |
| A02 | **Fermé** | F:L73–75/135 : geste **23,1 %** du total final, lent **+10,12 %** ; pourboires ≈ **9 s de R/min** par aide à 30/min, donc utiles aussi en fin. |
| A03 | **Fermé** | Plafonds explicites F:L114/134 : mousse **10 min/jour**, **5 min/partenaire**, intensité ×1,25. L’attribution du partenaire reste M06, non une absence de plafond. |
| V01 | **Déplacé → QA, P0 si reproduit** | F:L120/126/149 interdisent budgets séparés et double crédit d’un cycle. Tester deux finitions simultanées, rejeu et auto+manuel ; pas de preuve d’idempotence exécutée. |
| V02 | **Ouvert, risque P0** | F:L110/127 : crédit unique et sauvegarde avec consommation ; **bornes temporelles persistantes d’une réserve non définies**. Tester crash/reconnexion/rejeu : **+3 600 R** par double réserve, **+600 R** par double contrat. |
| V03 | **Déplacé → QA, P1 si reproduit** | F:L108/121–122 : R non circulaire, quotas consommés au taux courant, jour UTC persistant. Tester minuit, changement de R et de serveur ; singularité R=0 en N04. |
| V04 | **Déplacé → QA, P1 si reproduit** | F:L110/123–124 : seuls les robots en service débloquent ; chantiers continués mais nouveaux robots exclus de la réserve jusqu’au retour ; express futur seulement. Anticiper 180 s d’un r10 ajouterait **5 231 250 000 000 pièces** de production directe. |
| V05 | **Déplacé → QA, P0 si reproduit** | F:L124/127/149–153 : cinq passes durables non cumulables, cosmétiques sans effet. Tester chargement/réapplication : ni deuxième auto ni chantier ÷4. |
| V06 | **Déplacé → QA, P1 si reproduit** | F:L102/108/110/114/125 : permanents ×1,875 une fois, mousse action seule, R sans mousse. Tester ×1,25 et non ×1,5625 ; inclusion des permanents dans le stock. |
| V07 | **Ouvert, risque P1** | F:L126 : renouvellement, robots décoratifs et contrat en deux lots écrits ; **capacité partagée insuffisante** (N02), accès après départ du propriétaire et déplacement auto non garantis. |
| M01 | **Fermé** | F:L73/97/120 : 40/min par compte, fenêtre glissante, toutes sources ; minimum 1,5 s, actif nominal 2 s ; a1×a2=3. |
| M02 | **Ouvert** | F:L108/121 : base et normalisation précisées, mais **R=0** et mousse mesurée en temps ou en équivalent revenu restent à trancher (N04). |
| M03 | **Fermé** | F:L112/122/126 : jour UTC serveur, compte/jour persistant, attribution au jour de finition, 40 vitres distinctes. QA du passage de minuit toujours requise. |
| M04 | **Fermé** | F:L110/123 : débit → chantier → service unique ; service seul pour gains/jalons/déblocages ; traitement de l’absence explicite. |
| M05 | **Ouvert** | F:L124/149–153 : nature, portée, futurs chantiers et renommage réglés ; **choix de la prochaine vitre/déplacement auto continu** non défini au-delà de la scène initiale F:L204. |
| M06 | **Ouvert** | F:L125/133–134 : fenêtre de déclenchement 10 s, effet 30 s, renouvellement sans cumul ; **partenaire imputé dans un groupe de trois ou plus** non défini. |
| M07 | **Ouvert** | F:L126 : stock et cycle définis ; capacité collective N02, déplacement et départ du propriétaire restent sans solution. Deux lots de 20 rendent les 40 vitres du contrat possibles. |
| M08 | **Ouvert** | F:L127 : identifiant/consommation sauvegardés, session unique, pas de vente/rangement/reset ; **identité durable de l’intervalle hors ligne et reprise après échec de sauvegarde** non spécifiées. Pas de faille de code présumée. |
| M09 | **Ouvert** | F:L128 : double précision et origine du remboursement précisées ; **arrondi de la base exponentielle ou du prix précédent déjà arrondi**, et **plafond de solde**, non tranchés. Au débit final, solde >9×10¹⁵ après environ **6 h 21 min** supplémentaires ; la taille du plus gros achat ne borne pas le solde. |

Bilan : **5/8 défauts D/A fermés** ; sur les **24 lignes**, **8 fermées, 9 ouvertes, 7 déplacées**. Les 7 risques V restent à qualifier en jeu (3 P0 et 4 P1 s’ils se reproduisent). **6 décisions M restent ouvertes**, plus les deux paramètres du moteur absents ci-dessous.

## 2. Simulation et vérifications indépendantes — calculs

`economie.json` retranscrit depuis le § 3 bis, sans lecture d’`economie-propose.json` ; types/prix des offres et caractère non compétitif pris au § 5. Aucun bonus annexe injecté. Paramètres **absents et omis** : `delai_achat_s`, `duree_max_s` ; défauts du moteur **3 s pour les deux profils**, **14 400 s**. L’arrondi M09 n’a pas de champ supporté : pas de faux paramètre ajouté.

Commande exécutée depuis la racine :

```powershell
python OUTILS\sim-economie.py JEUX\lave-la-tour\03-economie\economie.json --sortie JEUX\lave-la-tour\03-economie\SIMULATION.md
```

**Code de sortie relevé immédiatement : 0.** Les deux profils terminent, chacun avec 105 achats, dont 100 robots.

| Profil | Premier achat | Max 0–10 min | Max 10–60 min | Max après 60 min | Fin | Geste final |
|---|---:|---:|---:|---:|---:|---:|
| Actif | 20 s | 69 s | 330 s | 378 s | **97:10** | 23,1 % |
| Lent | 40 s | 66 s | 367 s | 421 s | **107:00** | 13,0 % |

Jalons actif : tranche 2 **4:31**, tour 2 **15:26**, tour 3 **50:55**. L’annexe C arrondit raisonnablement les tours à 15/51 min et les fins à 97/107 min ; les six paliers du § 3 concordent avec le § 3 bis.

| Contrôle à la main | Calcul reproductible | Résultat et comparaison |
|---|---|---|
| **Annexe C : premier achat 20 s** | 30/60×1=0,5 pièce/s ; 10/0,5=20 ; à 19 s seulement 9,5 pièces. | **20 s**, identique. |
| **Annexe C : écart maximal initial 69 s** | Après achat à t=390, cash=242,357624 ; revenu=84,7/s. Un r3 entre en service à t=397 : revenu=100,3/s. À t=458 : 242,357624+7×84,7+61×100,3=**6 953,557624 <7 000** ; à t=459 : **7 053,857624**. | Achat suivant à 459, soit **69 s** ; maximum retrouvé dans la liste complète des écarts. |
| **Annexe C : remboursement maximal 285 s** | r4 n°10 à t=906, avant a4 : 7 000×1,14⁹=22 763,639648 ; /80=**284,545496 s**. | Outil **4:45**, arrondi correct pour la production directe ; **218,881150 s** si tout le revenu ajouté est compté, voir N01. |
| **Exemplaire tardif : r10 n°10** | Achat t=5650 ; coût=4,5×10¹²×1,065⁹=**7 931 566 754 659,265** ; revenu direct=15,5×10⁹×1,5×1,25=**29 062 500 000/s** ; quotient=**272,914125 s**. | Transaction mémorisée identique ; service à t=5830 ; chantier **180 s séparé**, conforme à la convention. Marginal total : **209,933942 s**. |

Contrôle supplémentaire de l’annexe C : R final =1,875×10×(0,25+4+12+80+1 650+34 500+790 000+19 600 000+520 000 000+15 500 000 000)=**300 757 992 117,1875/s**. Action active =0,5×3×(1,875+0,2R)=**90 227 397 637,96875/s** ; part=**23,076923 %** (lent **13,043478 %**). Retard lent =(6420−5830)/5830=**10,120069 %**, supérieur aux 5 % requis.

## 3. Constats nouveaux — faits et calculs séparés

### N01 — P1 certain, outil : le nouveau revenu marginal est incomplet

**Lu.** S:L143–148 applique correctement la formule des vitres à R courant. Mais les candidats robots (S:L194) et améliorations ciblant un robot (S:L203–204) omettent son supplément d’action. Ce marginal incomplet sert au choix (S:L216) et à la transaction/remboursement (S:L227/317–329). Le simulateur vérifie désormais chaque copie, au prix interne et aux multiplicateurs acquis à l’achat, hors chantier ; il ne calcule donc pas entièrement le « revenu qu’il ajoute » annoncé à S:L20–22.

**Calcul.** Pour un supplément de robots ΔR : marginal total = **ΔR×(1+cadence×raclette×0,2)** ; actif équipé : **1,3ΔR**, lent : **1,15ΔR**. r10 n°10 : **209,934 s**, contre **272,914 s** annoncés ; a3 à t=585 ajoute **20,8/s**, pas 16/s. Sur la trajectoire officielle active, remboursements totaux **36,364–218,881 s**, tous dans les bornes. Recalcul expérimental **en mémoire seulement**, marginal corrigé : fin **97:08**, écarts **60/332/378 s**, 0/100 hors borne ; la cadence passe encore. L’ordre d’achat annoncé par l’en-tête n’utilise donc pas le vrai remboursement total, même si le verdict de cette fiche résiste.

### N02 — P1 certain sur papier : le stock reste une ressource disputée

**Lu.** F:L126 fournit **30 vitres partagées**, renouvelées 20 s après lavage, créditées au seul finisseur ; F:L132–136 vise six joueurs et une scène coopérative sur une même façade. Les robots ne consomment plus le stock, mais les visiteurs le consomment toujours.

**Calcul.** Même en accordant le maximum annoncé de **90 vitres/min**, six joueurs à 30/min en demandent **180** : **au moins 50 %** des actions attendues ne peuvent finir sur cette façade ; à 40/min, déficit **62,5 %**. Trois aides à 30/min peuvent à elles seules demander tout le stock ; aucune allocation au propriétaire n’est écrite. À équipement final, chaque action manquée retire **3B+0,6R** pièces ; 30/min perdues retirent environ **0,3R/s**. Les pourboires compensent au début, mais cessent après leur quota **600R/jour**. Le modèle à débit individuel constant ne prouve donc ni la cadence coopérative ni l’auto à 30/min sur une façade occupée. Qui perd effectivement les finitions, ou peut les monopoliser, reste **à vérifier en jeu**, pas un exploit de code établi.

### N03 — P2 certain de formulation ; confort compatible avec E6 sous la prémisse non compétitive

**Lu.** F:L143 promet du confort plafonné au rythme actif ; F:L73 fixe ce rythme à **30/min**, mais F:L120/149 autorise un total manuel+auto de **40/min**. L’effet détaillé n’ajoute aucun gain par vitre et annonce ce budget partagé.

**Calcul.** À stade avancé : immobile **R/s** ; actif gratuit ou auto seule **1,3R/s** ; lent gratuit **1,15R/s**. Auto : **+30 %** contre immobile, **+13,04 %** contre le lent, **0 %** contre un actif au même rythme. Auto 30+manuel 10 donne **1,4R/s**, soit **+7,69 %** face à l’actif nominal ; un gratuit à 40/min peut obtenir le même revenu. L’indexation rend le confort beaucoup plus rentable, sans créer à elle seule une vente de pouvoir interdite par E6. La phrase de plafond à 30/min n’est toutefois pas assurée par le budget à 40/min. L’hypothèse « non compétitif » doit aussi être réévaluée si N02 permet de priver autrui d’action.

### N04 — P2 certain de spécification : quotas et début à revenu nul

**Lu.** F:L121 fait consommer à la mousse un quota « en minutes au taux du moment », tandis que F:L134 dit **minutes de mousse effective**. Aucun partenaire imputé n’est choisi pour un groupe de trois ; aucun cas R=0 n’est défini.

**Calcul.** Fin de jeu, actif : supplément mousse **0,075R/s** ; 10 minutes effectives donnent **45R**, soit **0,75 min de R**. Si « 10 minutes » était un budget de revenu, il permettrait au contraire **8 000 s de mousse**, soit **133 min 20 s**, écart ×13,33. À t=0, R=0 mais une vitre aidée devrait donner **0,5 pièce** au propriétaire : normaliser 0,5/(60R) est indéfini, et plafonner à 10 minutes de R autorise alors zéro pièce. Ce sont des décisions manquantes, pas une duplication démontrée.

### Revenus annexes désormais proportionnels — calculs bornés, aucun nouvel exploit illimité prouvé

À état final figé, B=1,875 ; les équivalences suivantes excluent réinvestissement et changement de R :

| Source | Quantification | Conséquence |
|---|---|---|
| Pourboire d’un compte débutant aidant un propriétaire avancé | Par vitre : **1,5B+0,3R** du propriétaire, quel que soit le revenu de l’aide ; à 30/min ≈**9R/min**. | Un partenaire atteint 5 min de R en **33 min 20 s** ; deux aides en parallèle peuvent atteindre les 10 min totales dans le même temps, si le stock le permet. Comptes multiples efficaces, mais **600R/jour au total**, pas un robinet sans limite si quotas persistants. |
| Mousse | ×1,25 de l’action seulement : total actif ≈**1,375R/s**, contre 1,3R sans mousse. | **+5,77 %** de revenu total pendant l’effet ; quota temps 10 min → **45R/jour**, dont 22,5R par partenaire, au stade final. Les 10 s de M06 se lisent comme fenêtre de déclenchement, les 30 s du § 4 comme durée : pas de contradiction certaine de durée. |
| Hors ligne | **0,5R_départ×min(absence,7200)** ; réserve pleine **3600R**, soit **60 min de R**, environ **46,15 min de revenu actif** au stade final. | Absence à 0,5R/s < présence immobile R/s < actif 1,3R/s. Exemple premier r3 acheté : R_départ=11,75 ; stock **42 300** ; les **43 140** pièces qu’aurait produites le nouveau r3 pendant les 7 190 s restantes sont volontairement exclues. Afficher cette exclusion et fixer les bornes de réserve (M08). |
| Contrat | 40 vitres normalement rémunérées +**600R à la finition**, une fois/jour : **80 s actif**, **160 s lent**, minimum **60 s** à 40/min. Au stade final, prime **180 454 795 270 312,5**, soit **7,69 min du revenu actif total**. | Attendre un r10 supplémentaire avant la dernière vitre augmente la prime de **17 437 500 000 000** pièces : choix permis, sans circularité ni quota supplémentaire. R est déjà multiplié par les permanents : ne pas les appliquer une deuxième fois. |
| Chantiers express | Premier r10 avec B : 90 s gagnées → **2 615 625 000 000** de production directe, plus **784 687 500 000** d’action indexée à 30/min si le joueur lave. | Total **3 400 312 500 000** avancé à état autrement identique. C’est bien du temps vendu, annoncé F:L150, pas un changement du taux en service. |

Au stade final, stock plein + contrat + quota de pourboires + 10 min effectives de mousse représentent environ **80,75 min de R**, à bases figées. Ce n’est ni 80,75 minutes retranchables de la simulation ni une borne sur plusieurs jours. **97:10 qualifie uniquement la trajectoire sans ces apports**, pas toute session réelle.

## 4. Autres écarts entre outil, fiche et en-tête — faits lus et calculs

- **Prix payé** : S:L185–187 conserve la puissance flottante, sans le plafond entier de F:L128. r1 n°3 : **14,4**, contre **15** prescrit ; r1 n°5 : **21** si arrondi de 10×1,2⁴, mais **22** si croissance du prix précédent arrondi. Rejeux en mémoire, politique originale : fin **97:11** avec plafond de la puissance, **97:13** avec arrondi récursif ; aucun outil modifié. L’écart de sémantique est certain, le choix entre ces deux arrondis reste M09.
- **Verdict incomplet à horizon court**, déjà relevé passe 1 et toujours présent : S:L333–337 ne donne qu’ALERTE sans fin atteinte. Rejeu de cette même entrée à horizon **600 s**, en mémoire : fin absente, `echec=False`, rapport PASSE ; le chemin S:L525–539 rendrait **0**, sans preuve des 90 min. Cela ne touche pas la sortie officielle, dont les deux fins sont atteintes.
- **Corrections effectives** : délais actif/lent identiques à 3 s (S:L506–507) ; retard lent correctement calculé à **10,1 %**, ALERTE seulement sous 5 % (S:L512–522), conformément à la procédure. Queue finale de chantier désormais incluse (S:L285–287). Écarts classés par leur début (S:L289–291), pas par chevauchement ; convention à rendre explicite. Revenus annexes/offres restent hors simulation, conformément à S:L24–25 ; `juger_offres` ne valide que type/prix, pas la vérité d’un effet commercial.

## 5. Propositions et scénarios QA — non appliqués

1. **Outil, N01** : inclure l’effet indirect sur l’action dans les marginals de robots et améliorations ciblées ; conserver la photographie des permanents à l’achat. Fixer M09, puis simuler le même arrondi que le jeu. Ajouter un cas à action indexée et un contrôle de fin non atteinte. Proposition déposée dans `CONNAISSANCES/PROPOSITIONS/2026-11-16-contre-verification-marginal-simulateur.md` ; aucun seuil changé.
2. **Stock, N02** : choisir stock individuel ou capacité réservée par compte. Pour six demandes nominales, garantir au moins **180 finitions/min**, **240** au plafond, et leur accès effectif ; ne pas résoudre seulement par un compteur anti-double crédit. QA : six profils sur la même façade, après épuisement des pourboires, auto comprise ; mesurer les débits individuels et le départ du propriétaire.
3. **Contrat commercial, N03** : soit plafonner l’agrégat avec auto à **30/min**, soit annoncer explicitement auto 30, total 40, sans promettre ce plafond au rythme nominal. Ces choix ne sont pas simulés ici. Comparer gratuitement/payant au même geste et avec toutes les offres en passe 2.
4. **Quotas/état, N04 et M ouverts** : écrire mousse en secondes effectives, partenaire imputé à chaque activation, comportement à R=0, intervalle hors ligne unique, reprise de sauvegarde et déplacement de la nacelle. QA : R nul, changement de R, trois partenaires, quotas épuisés, minuit, crash/rejeu et une vitre terminée en concurrence ; conserver les scénarios V01–V07.

## Verdict

| Point | Résultat |
|---|---|
| Cadence officielle, profil actif | **PASSE**, sortie **0**, 97:10 ; hypothèses et limites ci-dessus |
| Défauts P0 certains | **0** |
| Nouveaux P1 certains | **2 : N01 outil, N02 stock partagé**, démontrés sur papier |
| Autres défauts certains suivis | D3 P2 ouvert ; N03/N04 P2 nouveaux ; arrondi M09 encore ouvert |
| Risques de l’implémentation | **3 P0 et 4 P1 hérités, non démontrés en jeu** |
| Décisions manquantes | **6 M ouvertes**, plus délai entre achats et horizon absents de la fiche |
| Monétisation | Effets déclarés compatibles avec **E6 en modèle non compétitif** ; **règle de plafond de la fiche non assurée en cumul**, concurrence sur stock à résoudre |
| Porte P2 | **Retour au concept** : N02 non corrigé/accepté, N01 à traiter sans prendre le PASSE pour une preuve complète ; aucune validation en jeu |

## Frictions

- `economie.json` était encore v1 ; il a été remplacé indépendamment. Le moteur n’exprime ni l’arrondi prescrit ni les revenus annexes ; variantes diagnostiques en mémoire seulement, sans toucher la fiche ou les outils.
- Une première écriture via le pipe PowerShell a remplacé les accents du JSON par `?` ; sortie corrigée, relue en UTF-8 et simulation officielle rejouée (sortie 0).
- Sources protégées comparées au commit b4905a2 par `git diff --exit-code` : aucune différence. Écritures limitées au JSON, à SIMULATION.md, à ce rapport et à la proposition autorisée ; fichiers temporaires relus avant remplacement, aucun fichier vide ni commit.

RESULTAT: echec | JEUX\lave-la-tour\03-economie\RAPPORT-ECONOMIE-contre-verification-1.md | cadence PASSE (sortie 0), 5/8 défauts fermés ; nouveaux 0 P0 / 2 P1 certains (outil et stock).

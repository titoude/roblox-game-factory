# Rapport d’économie — Lave la tour (`lave-la-tour`)

- Passe papier, **contre-vérification 2** ; agent indépendant **gpt-6.1-sol, effort xhigh**, le 2026-11-16.
- Entrées figées : **225cb3a37f3a3abc15c69039c33c2b02c5b51ad3** ; fiche v3 et contre-vérification 1 (celle-ci concernait la v2).
- Lus : garde-fous, procédure 03 entière (Conventions comprises), règles/seuils/Leçons d’Archipel § Économie, gabarits, fiche v3, suivi précédent, origines D4/D5/V/M, code et en-têtes des deux scripts.
- Références **F:L…** = `02-concept/FICHE-CONCEPT.md` v3 ; **S:L…** = `OUTILS/sim-economie.py` ; **T:L…** = `OUTILS/test-sim-economie.py`, au commit ci-dessus.
- Preuves : **lus et calculs locaux uniquement** ; aucun jeu, Studio, navigateur, réseau, sous-agent ou commit. Aucune implémentation du futur jeu qualifiée.

## 1. Tableau de suivi — faits lus

« Fermé » ferme le défaut papier précis ; « QA » conserve le risque d’exécution, sans défaut certain de la fiche. Une ambiguïté P2 n’est pas un exploit présumé.

| ID | État | Référence v3 / outil et justification |
|---|---|---|
| D3 | **Fermé** | F:L212–218/234–240 : arrivée discrète, délai de 7 s et chiffres recalculés cohérents ; dixième vitre à 26 s, achat vers 27 s ; contrôles ci-dessous. |
| D4 | **Déplacé → QA** | F:L116–122/129–135 : R hors action/primes, permanents inclus, attribution et plancher définis ; mesurer les assiettes réelles. Décompte mousse suivi en M06. |
| D5 | **Déplacé → QA** | F:L128/132/157 : même validation et budget glissant de 40/min, arrêt hors nacelle/hors ligne ; essayer auto + manuel. |
| V01 | **Déplacé → QA, P0 si reproduit** | F:L128/134–135 : cycle propre à chaque joueur, crédit unique et identifiant ; rejouer une finition, auto + manuel, deux joueurs sur la même vitre physique. |
| V02 | **Déplacé → QA, P0 si reproduit** | F:L118/135 : intervalle départ–retour, crédit et remise à zéro enregistrés ensemble, reprise après échec ; crash/rejeu : aucun second +3 600R de réserve ni +600R de contrat. |
| V03 | **Déplacé → QA, P1 si reproduit** | F:L116/129–130 : taux courant sans circularité, plancher, compte/jour UTC persistant ; tester R=0, hausse de R, minuit et changement de serveur. |
| V04 | **Déplacé → QA, P1 si reproduit** | F:L118/131–132/158 : service seul, chantiers continués mais nouveaux robots exclus de la réserve, express sur nouveaux chantiers ; vérifier chaque transition. |
| V05 | **Déplacé → QA, P0 si reproduit** | F:L132/135/157–161 : cinq passes durables non cumulables et cosmétiques sans gain ; reconnexion sans seconde auto ni chantier ÷4. |
| V06 | **Déplacé → QA, P1 si reproduit** | F:L81/110/116/122/133 : permanents ×1,875 une fois, mousse action seule ×1,25, R sans mousse ; vérifier les cumuls réels. |
| V07 | **Déplacé → QA, P1 si reproduit** | F:L132–134 : stock individuel, régénération, déplacement gratuit/auto, départ du propriétaire et contrat par lots définis ; mesurer disponibilité et déplacements. |
| M02 | **Fermé** | F:L116/129 : R défini ; quota consommé au taux courant, non recrédité ; max(R,1) pour les seuls quotas de pourboires ; mousse en temps (ambiguïté d’imputation isolée en M06). |
| M05 | **Fermé** | F:L132/157–161 : nature/portée des passes, express futur, sélection de la vitre suivante et déplacement continu avec ou sans passe explicites. |
| M06 | **Ouvert, P2** | F:L133/141–142 : partenaire désormais désigné, effet 30 s renouvelé ; « temps […] effective » et « les 30 secondes s’imputent » ne tranchent pas le décompte des chevauchements. Exemple ci-dessous. |
| M07 | **Fermé** | F:L134 : 30 vitres par joueur, retour après 20 s, robots décoratifs, hauteur par paliers, gains conservés au départ du propriétaire, contrat en lots de 20. |
| M08 | **Fermé** | F:L118/135 : identité du crédit et intervalle hors ligne, écriture conjointe, échec/reprise, session unique et absence de vente/rangement/reset définis. |
| M09 | **Fermé (décision)** | F:L85/136 : plafond de la puissance initiale, pas de récurrence sur prix arrondi ; double précision et solde ≤9×10¹⁵. Défaut numérique résiduel de l’outil séparé en N05. |
| N01 | **Fermé** | S:L196–218 : effet indirect de l’action dans robots et améliorations ciblées ; T:L50–69 et calculs 104/s et 20,8/s ci-dessous. |
| N02 | **Fermé** | F:L134/142 : stock individuel ; six capacités annoncées de 90/min = 540/min pour 240/min demandées au plafond, sans concurrence entre stocks. Exécution → V07. |
| N03 | **Fermé** | F:L151/157 : auto 30/min et total 40/min explicitement annoncés ; aucun plafond commercial à 30/min contredit par l’effet détaillé. |
| N04 | **Ouvert partiellement, P2** | F:L120/129/133 : R nul, unité temps et partenaire corrigés ; reste le chevauchement des activations de M06, un seul défaut partagé. |

**Périmètre demandé : 9/20 fermées, 2 ouvertes, 9 déplacées vers la QA.** Les 8 lignes déjà fermées (D1, D2, A01–A03, M01, M03, M04) restent fermées : **17/28** au total, sans réouverture.

## 2. Constats nouveaux et calculs reproductibles

### Simulation officielle et trois chiffres de l’annexe C

JSON **retranscrit depuis le § 3 bis**, avec `prix_entiers: true` ; offres/non-compétitif du § 5. Les dix lignes de générateurs ont aussi été comparées automatiquement à la fiche.
**Absents et omis : `delai_achat_s`, `duree_max_s`**. Le moteur applique respectivement **3 s aux deux profils** (S:L130) et **14 400 s** (S:L524) ; ces valeurs ne sont pas des décisions de la fiche.
Hors modèle, conformément aux conventions/S:L29–30 : absence, contrat, mousse, pourboires et effets payants. Stock individuel et plafond de solde non simulés.

```powershell
python OUTILS\sim-economie.py JEUX\lave-la-tour\03-economie\economie.json --sortie JEUX\lave-la-tour\03-economie\SIMULATION.md
python OUTILS\test-sim-economie.py
```

**Codes immédiatement relevés : simulation 0 ; tests 0 (16 contrôles, 0 échec).** Chaque profil : 105 achats, 100 robots, 0 remboursement hors bornes.

| Profil | Premier achat | Max 0–10 min | Max 10–60 min | Max après 60 min | Fin | Geste final |
|---|---:|---:|---:|---:|---:|---:|
| Actif | 20 s | 61 s | 332 s | 378 s | **97:09** | 23,1 % |
| Lent | 40 s | 69 s | 367 s | 421 s | **107:01** | 13,0 % |

Jalons actif : tranche 2 **4:41**, tour 2 **15:33**, tour 3 **50:52** ; annexes C conformes aux arrondis annoncés. Retard lent = (6 421−5 829)/5 829 = **10,156 % ≥5 %**.

| Vérification manuelle | Calcul indépendant | Simulation / annexe C |
|---|---|---|
| 1. Premier achat | 30/60×1=0,5 pièce/s ; 10/0,5=**20 s**, contre 9,5 pièces à 19 s. En discret : vitres à 8,10,…,26 s, achat vers 27 s. | **20 s**, puis ≈27 s en parcours prévu ; conforme. |
| 2. Écart maximal initial | Après achat t=410 : cash=3,3, revenu=102,9/s ; r3 en service à 420 →118,5/s. À 470 : 3,3+10×102,9+50×118,5=**6 957,3<7 000** ; à 471 : **7 075,8≥7 000**. | Achat à 471 ; **61 s**, maximum retrouvé sur tous les écarts ; conforme. |
| 3. Remboursement maximal | r4 n°10 à t=732 : plafond(7 000×1,14⁹)=**22 764** ; ΔR=80 ; action ajoutée=0,5×3×0,2×80=24/s ; total **104/s** ; 22 764/104=**218,884615 s**. | **219 s** ; lent : 22 764/(80×1,15)=**247,434783 s**, soit 247 s ; direct seul **284,55 s**, soit 285 s. Conforme. |

**Marginal a3, action indexée comprise.** Achat à t=527 : 8 r2 actifs à 2/s, raclette ×3, global ×1. ΔR=8×2×(2−1)=**16/s** ; supplément d’action=0,5×3×0,2×16=**4,8/s** ; Δtotal=**20,8/s**, comme le candidat du moteur (S:L215–218), remboursement indicatif 2 400/20,8=115,384615 s. Le calcul robot ci-dessus et celui d’a3 ferment N01 ; chantier r4 de 20 s jugé séparément.
Contrôle supplémentaire : R final=**300 757 992 117,1875/s** ; action=0,5×3×(1,875+0,2R)=**90 227 397 637,96875/s** ; action/total=**23,076923 %**, conforme à C.

### Défauts P2 certains et propositions (non appliquées)

| ID / gravité | Fait lu | Calcul / portée | Proposition |
|---|---|---|---|
| M06/N04 — **P2 de spécification** | F:L133 réclame du temps effectif mais impute 30 s à chaque activation, malgré le renouvellement sans cumul. | 10 activations avec le même partenaire à t=0,2,…,18 : union **48 s effectives**, contre **300 s** si 30 s sont débitées chacune ; le quota partenaire serait épuisé avec seulement 48/300=**16 %** du temps annoncé. Pas de duplication démontrée. | Débiter uniquement le temps réellement actif, non chevauchant, au partenaire courant ; préciser le transfert lors d’un renouvellement avec un autre partenaire et la coupure au quota. |
| N05 — **P2 certain, outil** | S:L192–194 utilise une puissance binaire flottante avant `ceil` ; le retrait de 10⁻⁹ ne corrige pas les erreurs aux grands prix. | **6/100 prix surévalués de 1 pièce** : r6 n°4–6, r8 n°3/5/6. Exemple exact : 5 600 000×1,10³=**7 453 600**, outil **7 453 601**. Écart cumulé **6 pièces** ; variante décimale en mémoire : mêmes fins **5 829/6 421 s**, mêmes écarts, 0/100 hors borne. Aucun P1. | Calcul décimal exact et tests de puissances tombant sur un entier. Proposition déposée sous `CONNAISSANCES/PROPOSITIONS/2026-11-16-contre-verification-2-arrondi-prix.md` ; outils inchangés. |

### Effets des corrections v3 — bornes, sans nouveau P0/P1 certain

- **Stock / scène / nombre de pièces (lu F:L32/134/144/170).** Six laveurs à 30/min demandent **180/min**, à 40/min **240/min**, chacun sur son stock : l’ancienne pénurie collective ne découle plus de la fiche. Une même vitre physique peut apparaître propre à A et sale à B pendant les **20 s** du cycle ; la « ligne propre qui monte » n’est donc pas un état de saleté commun, la hauteur commune vient des paliers. Clarification visuelle/QA, pas défaut économique certain.
- **P12 ne peut être jugé au papier.** Six tranches de 30 = **180 pièces** séparées ; cloner naïvement 30 vitres pour chacun des 6 joueurs sur chacune des 6 tours ferait **1 080**, plus jusqu’à **120** pour six lots de contrat de 20, avant décor. Des états de saleté par client peuvent partager la géométrie : dépassement de **1 500 non démontré**. QA : compter instances et mesurer cadence à six sur une façade, saletés distinctes, mousse et départ du propriétaire.
- **Pourboire débutant (F:L129/143).** Le plancher porte sur le **quota**, pas sur le gain : à R=0, une vitre aidée donne **0,5 pièce**, plafond **300 par partenaire / 600 par jour**. À 30/min, un partenaire atteint 300 en **20 min** ; deux parallèles atteignent 600 dans le même temps. 600 équivaut à **20 min** de lavage manuel initial à 0,5/s ; ce n’est pas une prime immédiate de 600. À R=0,25 figé, le quota de 600 représente **40 min de R** : exception initiale explicite et bornée, sans singularité ni P1 certain.
- **Comptes multiples (F:L129–130/143).** À équipement final, pourboire par vitre = **1,5B+0,3R**, basé sur le propriétaire, même si l’aide débute. Deux aides à 30/min atteignent ensemble ≈**600R en 33:20** ; cinq à 40/min ≈**600R en 10 min**. Changer d’aide ne relève pas le quota quotidien de **10 min de référence** ; hausse de R sans recrédit des minutes consommées. C’est une accélération sociale prévue, pas un robinet illimité. QA : 2 puis 5 aides, rotation des identités et hausse de R.
- **Mousse (F:L122/133/141–143).** À état final constant et 30/min, supplément ≈**0,075R/s**, soit **45R =0,75 min de R** pour 600 s effectives ; revenu total ≈1,375R contre 1,3R (**+5,77 %**). Les stocks individuels n’empêchent pas le déclenchement sur une même façade ; il faut le tester à trois partenaires, avec renouvellement et épuisement. Seul le décompte M06 reste à préciser sur papier.
- **Contrat tranche 2 (F:L120/131/134).** Ouverture au service de r3 : R≥12 garanti, aucune prime à R=0. Simulation officielle : ouverture à **281 s**, R=**25,75/s**. 40 vitres prennent **80 s** à 30/min, minimum **60 s** à 40/min, deux lots de 20. Variante diagnostique en mémoire : contrat commencé à 281, fini à 361, prime **600×51,75=31 050** ; ses vitres remplacent les actions normales, sans double gain ; fin **94:10**, soit **179 s** gagnées, encore ≥90 min. Ni cette variante ni la trajectoire officielle ne qualifient tous les cumuls sociaux/hors ligne.
- **Solde (F:L136).** 9×10¹⁵ est sous **2⁵³≈9,0072×10¹⁵**, et le prix maximal **7 931 566 754 660** reste achetable. Cash final officiel **52 724 450 083 609,55** ; au revenu total nominal final **390 985 389 755,15625/s**, plafond après **6 h 21 min 24 s** supplémentaires, cohérent avec le texte. Ce délai est une référence à 30/min sans apports annexes, pas une borne universelle. QA : plafonner chaque source et vérifier les fractions/achats proches du plafond.
- **Raclette motorisée (F:L128/132/151/157).** En fin de progression, gratuit nominal ou auto seule ≈**1,3R/s** ; auto 30 + manuel 10 ≈**1,4R/s**, **+7,69 %**, accessible aussi au gratuit à 40/min. Auto vs immobile : **+30 %**, vs lent **+13,04 %**. Aucun prélèvement sur les vitres d’autrui désormais ; confort/temps conformes à E6 sur le modèle non compétitif. QA : auto≤30, agrégat≤40, arrêt hors nacelle et achat des cinq passes.

## 3. Verdict — porte P2

| Point | Résultat |
|---|---|
| Cadence officielle, actif | **PASSE**, sortie **0** ; 97:09 ; premier achat, trois fenêtres, chaque remboursement et durée dans les seuils |
| P0 certains restants | **0** |
| P1 certains restants, fiche ou simulateur | **0** — N01 et N02 corrigés |
| P2 certains / décisions restantes | **2 défauts distincts** : décompte M06/N04, arrondi flottant N05 ; **2 paramètres de simulation absents**, omis et signalés |
| Risques d’implémentation non prouvés | V01/V02/V05 : **3 P0** ; V03/V04/V06/V07 : **4 P1** si reproduits ; D4/D5 : **2 P2** ; scénarios ci-dessus |
| Monétisation | **Conforme sur papier à E6 et à la phrase v3** ; aucune conformité d’exécution affirmée |
| Avis porte P2 | **PASSER sur les critères de la porte papier** : aucun P0/P1 certain restant ; P2 à clarifier/corriger, risques d’exécution transmis à la passe code et à la QA |

Aucune valeur économique de la fiche ni aucun seuil n’a été changé. Les propositions ci-dessus ne sont pas des correctifs appliqués.

## Frictions

- JSON présent encore en v2 : remplacé indépendamment ; `prix_entiers` est maintenant supporté. Les effets des passes et revenus annexes restent hors simulateur ; diagnostics uniquement en mémoire.
- Affichage initial des accents PowerShell incorrect : lectures refaites explicitement en UTF-8 ; sources conservées. Écritures temporaires relues avant remplacement, fichiers non vides.
- Sources protégées comparées à 225cb3a, sans différence ; mes écritures se limitent au JSON, à SIMULATION.md, à ce rapport et à la proposition outil. Aucun commit.
- Pendant la revue, Git a aussi signalé des changements externes dans `04-fun/RAPPORT-FUN.md` et `05-production/PLAN-PRODUCTION.md` : ni lus pour cet audit, ni modifiés, ni annulés.

RESULTAT: ok | JEUX\lave-la-tour\03-economie\RAPPORT-ECONOMIE-contre-verification-2.md | cadence PASSE (simulation 0, tests 0), 9/20 lignes fermées (17/28 avec acquis), 0 P0 / 0 P1 certains restants.
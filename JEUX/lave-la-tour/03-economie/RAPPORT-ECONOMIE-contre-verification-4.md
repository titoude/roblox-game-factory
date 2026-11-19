# Rapport d'économie — Lave la tour (`lave-la-tour`)

- Passe **1 (papier), contre-vérification n° 4**, fiche v5 ; rôle calcul et adversaire indépendant, ni auteur de la fiche ni des corrections.
- Agent : **gpt-6.1-sol, effort xhigh**, le 2026-11-16.
- Entrées exclusivement au commit **bf4e35fe9bb6c96e0f370b08a615752a6e1462e6**, extraites par `git show bf4e35f:<chemin>` : consignes, procédure 03, règles, seuils, leçons Économie, gabarits, fiche, JSON, simulation et contre-vérification 3. Procédure 05 et plan provisoire lus au même commit pour distinguer les lots.
- Références : **F:L…** = `JEUX/lave-la-tour/02-concept/FICHE-CONCEPT.md` ; **J:L…** = `JEUX/lave-la-tour/03-economie/economie.json` ; **S:L…** = `OUTILS/sim-economie.py` ; **P:L…** = `JEUX/lave-la-tour/05-production/PLAN-PRODUCTION.md`. Numéros au commit audité.
- Preuves : **faits lus et calculs locaux**. Aucun Studio, navigateur, réseau, sous-agent, installation ou commit. Aucun comportement du futur code qualifié ; aucune modification de la fiche, du JSON, de la simulation, des outils ou d'`ETAT.json`.

## Verdict

| Point | Résultat |
|---|---|
| Cadence du modèle de référence, actif | **PASSE**, sortie 0, `echec:false` ; `SIMULATION.md` reproduit à l'identique |
| F01–F03 / D01–D10 | **3/3 défauts fermés ; 10/10 décisions fermées**, dont les sujets supprimés |
| Défauts P0 / P1 certains | **0 / 0** |
| Autres défauts certains | **1 P2 documentaire**, N01 : plan de production provisoire périmé |
| Risques à vérifier en jeu, hors défauts certains | **2 P0, 4 P1, 2 P2**, Q01–Q08 |
| Décisions de produit encore manquantes | **0 bloquant L0 ou L1 ; 3 pour les lots ultérieurs**, D11–D13 |
| Monétisation / E6 | **Conforme sur papier**, effets et portée de l'auto explicités |
| Avis pour P2 | **OUI pour L0 et L1**, avec synchronisation documentaire N01 avant de coder et revue économie passe 2 au commit du lot L1 |

Les choix D11–D13 ne bloquent pas le prototype solo ni les constantes et achats de base : ils doivent être tranchés avant les fonctionnalités correspondantes. Cet avis économique ne passe ni P3, ni P4, ni la QA, et ne modifie aucune porte historique. Les conditions de production qui ne relèvent pas de cette revue restent hors verdict.

## 1. Faits (lus)

### 1.1 Fermeture des constats de la contre-vérification 3

Les références suivantes viennent du **corps** de la v5, pas de sa liste de corrections.

| ID | Statut | Preuve v5 et portée |
|---|---|---|
| F01 | **Fermé** | Accès à la Flèche = **100 robots en service et 5 améliorations**, F:L141/160 ; réserve récrite, F:L165. R minimal à cet accès = R final, recalcul §2.3. La fin simulée reste distinctement r10≥10, F:L158. |
| F02 | **Fermé** | Aspects seulement visuels, trois passes, même gain et une unité, F:L93/110/182. Plus de vitre double : 200 vitres = 200 unités, recalcul §2.4. |
| F03 | **Fermé** | Une façade, cinq vitres par étage, aucun angle, F:L82/87 ; calcul discret et soldes, F:L267–281 ; annexe C, F:L297–300. Recalcul §2.4. |
| D01 | **Fermé, sujet supprimé** | Cadences physiques 30/15, plafond 40, toute vitre = une unité, F:L110/182 ; auto une vitre toutes les 2 s, F:L186. |
| D02 | **Fermé, sujet supprimé** | Plus de distribution de tenaces à pondérer ; emplacements des aspects fixes selon le numéro, F:L93 ; même gain, F:L110. |
| D03 | **Fermé** | Deux secondes incluent glissement et montée, toucher suivant accepté pendant ces mouvements, F:L87/182 ; pas d'angle à ajouter. |
| D04 | **Fermé** | Deux segments non finis au plus : courant et un d'avance, achat suivant dès l'achat précédent, F:L160. |
| D05 | **Fermé** | Sur la Flèche, pigeons seulement quand tous les segments achetés sont propres ; aucun étage non acheté sali, F:L167. |
| D06 | **Fermé pour le délai demandé** | Dix secondes **de suite, assis, stock nul** ; sortie, contrat, déconnexion, déménagement ou achat de segment annulent, F:L155. Dix nouvelles secondes continues sont nécessaires après une interruption. Nouvelle transition « Chez… » : D11. |
| D07 | **Fermé** | À l'appui : visiteur renvoyé, lavage arrêté, changement enregistré atomiquement et identifié ; ensuite scène de 20 s sans crédit, F:L154 ; vitre et masque atomiques, F:L189. Les courses effectives relèvent de Q02/Q04. |
| D08 | **Fermé** | Préfixe de rangées finies + masque de 5 bits, zone de pigeons avec cycle séparé ; deux laveurs affectés à des vitres distinctes de la même rangée, F:L188 ; crédit et masque ensemble, F:L189. |
| D09 | **Fermé** | Contrat : aucun visiteur, auto autorisée, budget partagé, F:L174/182/186. Beffroi absent des systèmes conservés (§3 bis, §6, annexe B : F:L160–176/224–225/286–289). Ce n'est donc pas seulement un retrait annoncé en tête. |
| D10 | **Fermé** | Dernier pourboire proratisé selon le quota journalier **et** partenaire restant, jamais refusé entier ni dépassé, F:L191/198 ; recalcul §2.5. |

### 1.2 Transcription indépendante et couverture du modèle

Retranscription des tables de la fiche dans une copie hors dépôt, puis assertions contre le JSON figé :

| Bloc | Résultat |
|---|---|
| Départ, action, prix | Cash 0 ; gain 1 ; 30/min ; indexation 0,2 s ; prix entiers : conformes, F:L108–114, J:L6–14 |
| Générateurs | **10/10 lignes conformes** : noms, coûts, revenus, croissance, chantier, déblocage, maximum 10 ; F:L114–127, J:L15–115 |
| Améliorations | **5/5 conformes** : coûts, cibles, multiplicateurs, conditions ; F:L131–139, J:L117–158 |
| Jalons, fin, profils | Contrat r3≥1, tour2 r5≥1, tour3 r8≥1, fin r10≥10 ; actif ×1/lent ×0,5 : conformes, F:L110/141/158, J:L159–173/206–213 |
| Offres | Cinq noms, types et prix 149/99/49/29/79 conformes au §5 ; non-compétitif conforme, J:L174–205 |
| `apres_contenu` | Condition 100+5, R de référence entier, segments **40 étages / 200 vitres**, maximum deux non finis, formule de prix : conformes, F:L160–165, J:L214–225 |
| `stock_vitres` | Une façade ; 5 vitres/rangée, une rangée/étage ; **600/1 400/2 000** ; pigeons **20 étages / 100 vitres après 10 s** ; deux laveurs, 40/min, 1,5 s minimum, trois passes : conformes, F:L143–156/182/188, J:L226–257 |

**Aucune erreur de transcription trouvée.** Les conditions textuelles et les notes des blocs hors modèle ne sont pas une logique exécutée. Le simulateur ignore `apres_contenu` et `stock_vitres`, ainsi que contrat, absence, mousse, pourboires, passes, déplacements et plafond de solde ; ces omissions sont déclarées, pas validées par le PASSER.

`delai_achat_s` et `duree_max_s` sont absents de la fiche et restent omis du JSON. Le moteur utilise **3 s** pour les deux profils et **14 400 s** d'horizon (S:L133/530–532). Ce sont des conventions du banc, pas une décision imposant au jeu une attente de trois secondes. Leur omission ne bloque pas L0/L1 : la première minute donne ses propres instants discrets et la fin est atteinte avant l'horizon.

## 2. Calculs (reproductibles)

### 2.1 Rejeu figé et seuils

Copie légère hors dépôt : `%USERPROFILE%\AppData\Local\Temp\contre-verification-4-lave-la-tour-x5m5sa7e`. Script, seuils et entrées extraits avec `git show bf4e35f:<chemin>` ; contrôles dans `verifier.py` et `CONTROLES.json`, transcription dans `transcription-independante.json`.

Commande exécutée depuis la copie :

```powershell
python OUTILS\sim-economie.py JEUX\lave-la-tour\03-economie\economie.json --json
```

**Code 0, `echec:false`.** Le rejeu de la transcription indépendante donne les mêmes résultats, code 0. Sortie Markdown sans `--sortie` : **identique à `SIMULATION.md`** après normalisation des fins de ligne et retrait de `VERDICT : PASSE` terminal. Aucun rapport du dépôt régénéré. La sortie `--json` contient également ce suffixe : parser l'objet initial, pas le suffixe comme du JSON.

| Profil | Premier achat | Max 0–10 min | Max 10–60 min | Max après 60 min | Contenu | Achats |
|---|---:|---:|---:|---:|---:|---:|
| Actif | 20 s | 61 s | 332 s | 378 s | **5 829 s = 97:09** | 105 |
| Lent | 40 s | 69 s | 367 s | 421 s | **6 421 s = 107:01** | 105 |
| Seuils | ≤60 s | ≤120 s | ≤480 s | ≤900 s | ≥5 400 s actif | — |

Les deux trajectoires terminent avec **100 robots en service et 5 améliorations**. Remboursements : **0/100 hors bornes** par profil ; plages actif **36,364–218,885 s**, lent **38,095–247,435 s**, dans [30 ; 300]. Chantier maximal **180 s**. Retard lent `(6421−5829)/5829×100 = 10,156 % ≥5 %` : pas d'alerte E14. Ces chiffres qualifient les trajectoires du banc, pas toutes les politiques d'achat imaginables.

| Contrôle à la main | Calcul indépendant | Moteur |
|---|---|---|
| Premier achat | `10 / (30/60 × 1) = 20 s` | 20 s |
| Écart initial maximal | Après l'achat à410, cash **3,3** ; revenu102,9/s pendant10 s, puis118,5/s. À470 : `3,3+10×102,9+50×118,5=6957,3<7000` ; à471 :7075,8 | **471−410=61 s** |
| r4 n°10 | `ceil(7000×1,14^9)=22764` ; marginal actif `80×(1+0,5×3×0,2)=104/s`, donc **218,8846 s** ; lent `22764/92=247,4348 s` | 219 /247 s arrondis |

### 2.2 Façade, stock et pigeons

**Une façade seulement** : `120×5=600`, `280×5=1400`, `400×5=2000`. Les trois autres façades sont décoratives, sans stock ni crédit (F:L188). Les colonnes à40/min utilisent **leurs propres jalons recalculés**, pas les intervalles du profil30 :

| Profil | Fenêtres financières, secondes | Demande par tour `Δt×cadence/60` | Réserves `stock−demande` |
|---|---|---|---|
| 30/min | 0→933→3052→5829 | **466,5 ; 1059,5 ; 1388,5** | **133,5 ; 340,5 ; 611,5** |
| 40/min, diagnostic | 0→862→2864→5507 | **574,6667 ; 1334,6667 ; 1762** | **25,3333 ; 65,3333 ; 238** |
| 15/min, lent | 0→1075→3407→6421 | 268,75 ; 583 ; 753,5 | 331,25 ; 817 ; 1246,5 |

**Les six valeurs et six réserves publiées à30/40 sont justes aux arrondis affichés.** Ce sont des équivalents continus : aucune demi-vitre réellement payée. Ces fenêtres supposent un départ immédiat et un déménagement au jalon, sans ses20 s ; elles ne promettent pas qu'un joueur qui reporte son déménagement ne terminera jamais sa tour. Le passage à1 400 ferme le manque de stock du diagnostic40 de la tour2. Annexe C :575/600, conforme à574,6667 arrondi.

Pigeons : `20×5=100` vitres ; deux joueurs à40/min les épuisent en `100/80×60 = 75 s`. Après le stock initial, cycle **75 s de lavage +10 s d'attente**, débit moyen **70,588 vitres/min** ; à2×30 :54,545/min, seul40 :37,5/min. Ce n'est pas un débit permanent de80. Les10 s bornent l'attente **si le propriétaire reste assis sans action annulant le délai** ; sortie, contrat ou reconnexion ne donnent aucun stock ni argent gratuit, ils annulent le délai. « Chez… » et achat après un vol déjà déclenché : D11/D12 et Q04, sans faille de code présumée.

### 2.3 F01 : Flèche et réserve

```text
R_exact = 10×(0,25 + 2×2 + 12 + 80 + 1650 + 34500
              + 790000 + 19600000 + 520000000 + 15500000000)×1,875
        = 300 757 992 117,1875 pièces/s.
```

À l'accès v5, **tout joueur possède cet équipement**. La constante de prix **K=300 757 992 117** diffère de0,1875/s (≈6,23×10⁻¹³ relatif) ; fiche et JSON choisissent bien cet entier. Gain par vitre : `G=5,625+0,6R` ; revenu total actif `1,3R+2,8125`, lent `1,15R+1,40625`.

| Segment | Minutes de K | Prix | Financement actif / lent depuis zéro |
|---|---:|---:|---:|
| 1 | 5 | 90 227 397 635 100 | **230,769 /260,870 s** |
| 2 | 6 | 108 272 877 162 120 | 276,923 /313,043 s |
| 3 | 7 | 126 318 356 689 140 | 323,077 /365,217 s |
| 4 | 8 | 144 363 836 216 160 | 369,231 /417,391 s |
| ≥5 | 9 | 162 409 315 743 180 | **415,385 /469,565 s** |

Lavage : `200/30×60=400 s`, lent800 s ; **40 étages**, pas dix. Même sans action, financement maximal `540K/R <540 s <900 s`. Financement et lavage se recouvrent ; aucun nouveau revenu n'est produit par le segment, donc E3 n'est pas un remboursement à lui appliquer. Les temps publiés sont des financements à revenu constant, pas des dates garanties de clic.

Réserve pleine : `7200×0,5R = 3600R = 1 082 728 771 621 875` pièces. Coûts cumulés en minutes deK : **5,11,18,26,35,44,53,62**. Elle finance **sept premiers, pas huit**, ou **six au tarif9** (`54≤60<63`). Pas sept simultanément : acheter1 puis2, finir1 puis acheter3, etc., avec **deux non finis au plus**. Les anciens états de F01 (3 robots par rang inférieur, ou a5 absent) sont désormais **refusés à l'accès**. Aucun coût ni revenu n'a dû changer.

### 2.4 F02/F03, annexes A et C

Chaque vitre physique vaut **une unité et le même G**. Segment200 :400/800 s ; contrat40 :80/160 s aux rythmes30/15, minimum60 s au plafond40. L'ancien calcul210 unités et l'avantage temporel d'une tenace n'ont plus d'objet ; aucun angle ne rallonge une rangée.

Annexe A : fins `t(k)=4+2k`, premier geste4 s, première fin6 s. À60 : `floor((60−4)/2)=28` vitres, `floor(28/5)=5` étages finis, nacelle au6e.

| Achat prescrit | Solde avant débit, robots continus et vitre entière | Prix / reste |
|---|---|---|
| 25 s | Dix fins6,8,…,24 : **10** | 10 /0 |
| 41 s | `8×1,05+16×0,25 = 12,40` | 12 /0,40 |
| 56 s | `0,40+8×1,10+15×0,50 = 16,70` | 15 /1,70 |

À60, solde **7**, sans amélioration : `1,70+4×0,75+2×1,15`. Le premier robot est finançable dès24 s ; le clic annoncé à25 s reste cohérent. Les achats ne sont pas une mesure de réaction réelle.

Rangées finies à14/24/44/54 s :1/2/4/5. La nacelle atteint7e/13e/18e à64/124/174 s ; fanfare10e à94 s. À180 :88 vitres,17 étages finis ; **17−5=12 étages nouveaux entre61 et180**. Rejeu discret après les trois achats prescrits : copies4/5 à69/82 s, a1 à104 s, premier r2 à140 s : compatible avec les « vers1:10/1:25/1:45/2:20 » de F:L281.

Annexe C : première action, hauteur,12 étages, premier achat20/25, stock575, financement de la Flèche, réserve7/6, écarts61/332/378, remboursements219/247, jalons933/3052 et durées5829/6421 sont **conformes**. Parts du geste : **23,077 % /13,043 %**, arrondies23/13. J1, sessions et retour jour3/4 restent des **objectifs/prévisions non mesurés**, pas une rétention prouvée.

### 2.5 Social, pourboires, état et contrat

- **Deux comptes alternant « Chez… »** : changer de propriétaire ne change ni les identités du couple, ni le jour UTC, ni les quotas persistés (F:L183–189/198). Chaque receveur reste à **300R de pourboires par partenaire** et300 s de bonus de mousse avec lui ; alterner n'ouvre pas600R avec cette seule identité. Chaque vitre paie celui qui la finit, avec **ses propres robots** ; le pourboire utilise le gain du propriétaire sans mousse. Se déplacer ne crée pas un cycle de saleté (F:L188).
- Au maximum, visiteur30/min : pourboires `30×(2,8125+0,3R)=84,375+9R` par minute. Plafond partenaire300R atteint en **≈33:20**, à40/min **≈25 min**. Deux partenaires distincts permettent600R/jour ; le plancher `max(R,1)` est borné à600 pièces/jour quand R<1, pas un versement immédiat.
- **M10**, exemple : R=10, raclette×3 et multiplicateur global1 donnent G=9, pourboire nominal4,5. Restes jour0,02 min et partenaire0,005 min : `min(4,5 ; 12 ; 3)=3 pièces`, consommant **0,005 min** dans les deux quotas. Le reliquat n'est ni perdu entier ni dépassé.
- Mousse : ×1,25 sur l'action seulement, **600 s/jour,300 s/partenaire** ; son apparence reste après quota, son gain cesse. À30/min, équipement complet et R gelé : supplément **45R+421,875**, soit0,75 minute deR +base ; à40/min **60R+562,5**, soit1 minute +base. Avec un seul partenaire, moitié. Aucune boucle de récompense dans R.
- **M07**, exemple11/12 : deux rangées finies = dix vitres ;12 finie avant11 → masque **00010** (bit0=11), puis00011 quand11 finit. On n'avance le préfixe qu'à11111 ; crédit et bit ensemble (F:L189). La zone des pigeons a son propre cycle/préfixe/masque : elle ne réduit pas l'étage atteint ni n'ajoute un segment au record. La spécification représente les trous ; la résistance aux courses et aux pannes reste Q01/Q02.
- **Visiteur avec/sans passe** : seul le compte possédant l'auto lave automatiquement depuis la seconde place (F:L186). La passe du propriétaire ne s'y prête pas. Sans passe, le visiteur peut laver manuellement ; avec elle,30/min automatiques et complément manuel dans **le même budget40**, partout. Aucune augmentation de gain unitaire ni de quota social.
- **Contrat** :40 vitres sur la parcelle, pas de visiteur ; auto permise ; mêmes gains et budget que la tour ; prime **600R lu à la dernière vitre**, une seule fois au jour UTC de finition. Les gestes du contrat remplacent des gestes sur la tour. ÀR_final : prime **180 454 795 270 312,5**, sous9×10¹⁵. Le beffroi et sa prime1800R ont disparu.
- Diagnostic **hors verdict officiel**, même boucle du banc, contrat commencé au jalon281 s et achevé80 s plus tard, sans trajet supplémentaire ni double action : à361 s, R=51,75, prime **31 050**, fin **5650 s =94:10** au lieu de97:09. Calcul conservé dans `contrat.py`/`contrat-diagnostic.json` hors dépôt. Ce n'est ni une simulation du déplacement réel ni une durée universelle de la v5. ÀR_final gelé, réserve+contrat+quotas sociaux complets à30/min = **80,75 minutes deR**, plus base ; quotas et travail requis, pas une prime instantanée.

### 2.6 Règles E1 à E15 sur le périmètre changé

| Règle | Jugement papier |
|---|---|
| E1, E2 ; seuils120/480/900 | Modèle conforme ; stock recalculé conforme ; Flèche équipée financée même sans geste en≤540 s. Délai pigeon conditionnel10 s, pas un trou d'achat de15 min. |
| E3 ;30–300 s, chantier≤180 | 100/100 achats conformes **dans chaque trajectoire auditée** ; segments sans revenu propre hors remboursement. |
| E4 | Contrat600R ; R défini, sans pourcentage du cash ni montant fixe. |
| E5, E15 | Intensité×1,25, quotas temps/jour/partenaire ; pourboires avec prorata et plancher, sans récompense dans R. Aucun robinet illimité certain par alternance de deux comptes. |
| E6 | Auto30 dans budget40, temps de chantier et apparence ; record sans récompense. Pas de pouvoir contre autrui démontré. |
| E7 | Auto et manuel même validation, service exigé pour tous les déblocages ; visiteur et contrat explicités, F:L185–186. À prouver en passe2. |
| E8 | Identifiants, crédit et consommation sauvegardés ensemble avant confirmation ; aucun doublon autorisé. Exécution non prouvée, Q01/Q02. |
| E9 | Aucun enjeu de perte ajouté ; voyage ne doit recréditer ni vitre ni quota ; scène sans gain. Les transitions encore indécises sont D11–D13, pas une duplication démontrée. |
| E10, E11 | Commit unique et relecteur indépendant ; aucun acquis historique pris pour preuve des ajouts. |
| E12 | Réserve2 h à50 %, R de départ excluant robots achevés pendant l'absence, crédit unique ; promesse7 premiers ou6 à9 min désormais soutenue par l'accès100+5. |
| E13 | Aucun objet aléatoire payant. |
| E14 ; retard≥5 % | **10,156 %**, conforme, sans ambiguïté de cadence physique désormais. |

## 3. Défauts

Gravités du mandat : P0 bloque/perd des données ; P1 casse une promesse/un seuil ; P2 gêne ; P3 détail. Les risques et décisions ne sont pas comptés comme défauts certains du futur code.

| ID | Gravité / statut | Chemin et fait lu | Preuve chiffrée | Correction minimale proposée | Coût/revenu touché ? |
|---|---|---|---|---|---|
| **N01** | **P2 certain, documentaire** | `JEUX/lave-la-tour/05-production/PLAN-PRODUCTION.md` est explicitement provisoire v3 : P:L3–4/25/42–49/58/86. Il conserve30 vitres, resalissure20 s, mousse30 s, absence de saleté visible chez autrui ; L0 annonce encore8/27 s. | V5 : première fin **6 s**, premier achat **25 s**,28 vitres à60 s,88 à180 s ; une tour de5 étages×5 n'offre que **25 vitres**, contre600 pour la tour1 ; pigeons100 après10 s, mousse fenêtre10 s seulement. | Avant L0, synchroniser plan et preuves sur F:L87/143–155/182–189/267–281 ; retirer seulement les prescriptions périmées. Pour L1, garder les constantes validées et le contrôle du commit. | **Non** pour coûts/revenus ; documentation du stock, des temps, du prototype et des effets. |

**Aucun nouveau P0/P1 certain.** L'ancien F01 est fermé par une condition d'accès, pas masqué par un changement du prix des segments. N01 ne constitue pas une décision économique manquante : les valeurs de remplacement sont déjà écrites dans la v5.

## 3 bis. Décisions manquantes avant le code concerné

**L0 : aucune. L1 : aucune pour l'économie de base.** Les choix suivants restent nécessaires pour les transitions des lots suivants ; aucune constante de coût/revenu n'est à inventer. Répartition selon `PROCEDURES/05-PRODUCTION-STUDIO.md` L35–48, avec plan provisoire à synchroniser.

| ID / lot | Décision encore à écrire | Fait et conséquence | Proposition minimale, non appliquée |
|---|---|---|---|
| **D11 — L3/L4** | Transition « Chez <visiteur> ! » si la destination est déjà propre ; qui déclenche le voyage du duo ; pigeons si la proposition n'est pas utilisée. | F:L155/197–200 propose le voyage avant les pigeons mais ne donne pas ces conditions. Avec **deux tours propres, 0+0 reste0** ; les voyages ne doivent pas fabriquer du stock ni réinitialiser les quotas. « Sinon » ne suffit pas à trancher présence d'un visiteur / refus du voyage. | Proposer le voyage vers du stock disponible ; sinon conserver un retour pigeon après10 s continues dans la nacelle. Nommer l'action qui transporte le duo et revalider destination/place au clic. Aucun coût/revenu modifié. |
| **D12 — L3/L5 (Flèche)** | Acheter un segment **après** le déclenchement d'un vol : priorité entre zone des100 vitres resalies et200 vitres neuves ; portée de « deux segments non finis ». | F:L155 annule le délai à l'achat, F:L167 interdit des pigeons sur du non-acheté, F:L188 représente la zone séparément ; rien ne tranche une zone déjà créée. Cela change le travail visible et le décompte de la file, pas le prix. | Conserver la zone et ses crédits, choisir explicitement l'ordre de lavage ; compter les deux segments achetés non encore finis une première fois séparément de cette zone. Aucun coût/revenu modifié. |
| **D13 — L4/L5** | Sort du visiteur déjà à bord quand le propriétaire choisit le contrat. | Contrat solo, aucun visiteur n'y monte (F:L174) ; renvoi explicite seulement au déménagement/départ du serveur (F:L154/188). Sans choix, le visiteur pourrait être renvoyé, rester sur l'ancienne tour, ou bloquer le départ : résultats différents. | Renvoyer le visiteur à sa tour avant le déplacement, stopper son action sans perdre les gains finis ; annuler le bonus, sans restaurer les quotas. Aucun coût/revenu modifié. |

Ces décisions sont **ouvertes**, pas des exploits certains. Les réservations de vitres, reprises de sauvegarde et événements simultanés ont déjà leurs invariants ; leur mécanisme technique reste du travail d'implémentation et de QA, pas de nouvelles décisions de concepteur bloquant L0/L1.

## 4. Propositions

**Aucune appliquée ; aucun seuil ni constante de coût/revenu proposé à la hausse ou à la baisse.** Corriger N01 avant de suivre le plan ; trancher D11–D13 avant leurs lots ; conserver les calculs de référence et qualifier l'économie du code au lot L1. Les arrondis de l'annexe C restent des prévisions, à comparer aux mesures.

Leçon déposée : `CONNAISSANCES/PROPOSITIONS/2026-11-16-contre-verification-4-plan-prototype.md` : une correction de concept peut être cohérente dans la fiche et le JSON tout en laissant le plan de production prescrire l'ancien prototype. Décision laissée à l'orchestrateur.

## 5. Scénarios pour la QA

Révision des Q01–Q08 de la contre-vérification3, **non exécutés, non comptés parmi les défauts certains** :

| ID | Gravité si reproduit | Scénario et attendu |
|---|---|---|
| **Q01** | **P0** | Deux laveurs,11/12 attribuées séparément,12 finie avant11 ; déconnecter pendant écriture puis arrêter serveur, recommencer après pigeons. Préfixe/masque/cycle et gains restaurés, aucune vitre sautée, payée deux fois ou gain perdu. Libérer une réservation abandonnée. |
| **Q02** | **P0** | Rejouer finitions, crédit de réserve, déménagement, achat et fin de segment, contrat ; panne avant/après sauvegarde, retour simultané et minuit. Un effet par identifiant/jour, jamais de solde ou progression incohérents, rejet d'accès Flèche à99 robots ou4 améliorations. |
| **Q03** | **P1** | A/B alternent « Chez… », places et serveurs après300 s de mousse/300R de pourboires ; C apporte le reste jusqu'à600. Vérifier durée effective, prorata M10, hausseR, R<1 et minuit. Quotas non restaurés par rôle ; mousse visible mais bonus nul au plafond. |
| **Q04** | **P1** | Épuiser tours à2×40 ; rester assis10 s, annuler à9,9 s par sortie/contrat/voyage/déménagement/achat ; acheter pendant le vol, deux tours propres et voyage refusé. Un vol100 par cycle ; aucun étage non acheté, aucune pièce de scène gratuite ; borne10 s appliquée dans son état défini après D11/D12. |
| **Q05** | **P1** | Auto+manuel chez soi/visiteur/contrat ; propriétaire avec passe et visiteur sans, puis inverse. Seul le titulaire automatise, total≤40 vitres/60 s par compte, cadence minimale1,5 s, crédit unique ; sortie coupe l'auto ; express ne saute ni chantier applicable ni mise en service. |
| **Q06** | **P1** | Préacheter deux segments ; refuser le troisième tant qu'aucun ne finit ; finir l'un et acheter le suivant ; sept premiers financés par réserve pleine, puis six au tarif9 dans un essai distinct. Relaver dix zones de pigeons : record **40×segments finis une première fois**, pas40×relavages. |
| **Q07** | **P2** | A/B alternent sur tours propres/sales ; place occupée ou ami parti au clic ; propriétaire quitte le serveur ou part au contrat selon D13. Retours sur la bonne tour, gains conservés, aucune téléportation ni lavage sur état périmé. |
| **Q08** | **P2** | Première minute : aspects fixe8/17 sans gain double, achats25/41/56,28 vitres/5 étages à60 ; filmer jusqu'à180 pour les12 étages nouveaux et la caméra tenue. Contrat40 manuel/auto, changerR à la dernière vitre et traverser minuit : prime600R une fois, aucun double geste sur la tour. |

Écriture limitée au présent rapport et à la proposition de leçon ; sources et outils conservés. Le PASSER est un avis papier sur L0/L1, pas une qualification du jeu ni une autorisation de publication.

RESULTAT: ok | JEUX\lave-la-tour\03-economie\RAPPORT-ECONOMIE-contre-verification-4.md | cadence PASSE ; 0 P0 et 0 P1 certains ; 0 décision manquante bloquant L0 ou L1 ; P2 favorable sous synchronisation du plan, 3 décisions réservées aux lots ultérieurs.

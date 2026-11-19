# Rapport d'économie — Lave la tour (lave-la-tour)

- Passe : 1, papier, avant code.
- Rôle : adversaire ; revue indépendante, sans sous-agent.
- Agent : Codex gpt-6.1-sol, effort xhigh, le 2026-11-15.
- Source auditée : JEUX/lave-la-tour/02-concept/FICHE-CONCEPT.md, version 1, 209 lignes, SHA-256 0DF7B87E156CECA3FB49C5DE4727E552CFBF9A386FB26345F005862EB67FC40E. Les références « fiche:Lx–Ly » ci-dessous désignent cet instantané.
- Pièces lues : GARDE-FOUS.md ; AGENTS.md de la racine ; CONNAISSANCES/00-LISEZ-MOI.md ; PROCEDURES/03-REVUE-ECONOMIE.md ; CONNAISSANCES/REGLES.md, section Économie ; CONNAISSANCES/LECONS-ARCHIPEL.md, section Économie ; CONNAISSANCES/seuils.json, section economie ; fiche entière, annexes comprises ; gabarits RAPPORT-ECONOMIE.md et PROPOSITION-LECON.md.
- Hors périmètre : code, Studio, navigateur, réseau, achats, comptes et essais réels. RAPPORT-ECONOMIE-calcul.md et SIMULATION.md n'ont pas été lus ; economie.json et le simulateur n'ont pas été consultés ou exécutés. Aucune source ni aucun outil n'a été modifié.
- Preuves : tous les faits sont « lus » ; les nombres sont des calculs sur papier, recalculés localement. Aucun constat n'est « vu en jeu ». « Certain » signifie ici défaut démontrable du modèle écrit, conformément à la procédure, et ne certifie aucune vulnérabilité d'une implémentation future (G15).

## Verdict

| Point | Résultat |
|---|---|
| Cadence, simulation du profil actif | Non évaluée par cet agent ; aucun résultat de l'autre vérificateur repris |
| Défauts P0 certains | 0 |
| Défauts P1 certains | 3 : A01, A02, A03 |
| Monétisation conforme à la règle de la fiche et à E6 | Offres compatibles sur papier avec le caractère non compétitif annoncé ; exécution et cas limites à vérifier, pas de conformité en jeu affirmée |
| Avis pour la porte P2 | Retour au concept : trois P1 à corriger ou à accepter explicitement avec raison, puis contre-vérification indépendante ; décisions M01–M09 à écrire avant le code |

Les risques V01–V07 ne sont pas comptés parmi les défauts certains. L'absence d'une règle technique dans une fiche ne prouve pas que son implémentation sera vulnérable. Aucune conclusion n'est tirée des prévisions de 75 s, 360 s ou 95 min de l'annexe C : elles restent des estimations de l'auteur.

## 1. Faits (lus)

| Réf. | Fait | Source |
|---|---|---|
| F01 | Une vitre demande trois coups, soit 2 s ; elle donne 1 pièce de base. Profil actif 30 vitres/min, lent 15 ; refus serveur au-delà de 40 vitres/min. | Fiche:L42–L45, L61–L63 |
| F02 | Dix exemplaires maximum par palier ; coût de la copie suivante ×1,2 ; revenu par exemplaire constant dans le tableau. Les chantiers vont de 0 à 180 s. | Fiche:L65–L78 |
| F03 | a1 et a2 multiplient le gain d'action par 2 et par 3 ; a3 double r2 ; a4 et a5 multiplient tous les revenus par 1,5 et 1,25. Aucun autre gain d'action par palier n'est décrit. | Fiche:L80–L88 |
| F04 | Déblocage par trois robots du palier précédent ; jalons r3 ≥ 1, r5 ≥ 1 et r8 ≥ 1. La fin de contenu impose dix r10. | Fiche:L45, L67–L92 |
| F05 | Hors ligne : robots à 50 %, au plus 2 h ; plafond affiché ; action et bonus exclus. La fiche ne définit pas ici le traitement des améliorations permanentes ni des chantiers en cours. | Fiche:L94 |
| F06 | Une façade de 40 vitres une fois par jour rapporte 10 min du revenu par seconde au moment de la fin. | Fiche:L96 |
| F07 | Mousse : deux laveurs sur la même façade à moins de 10 s d'écart ; gain d'action +25 % pendant 30 s ; non cumulable avec elle-même, plafond temporaire ×1,25. Aucun quota journalier ou par partenaire n'est donné pour cette source. | Fiche:L98, L103 |
| F08 | Sur la tour d'autrui, le laveur touche son propre gain ; le propriétaire reçoit 50 % de son propre gain d'action par vitre. Pourboires plafonnés à 10 min de son revenu par jour, dont 5 min par joueur. | Fiche:L104 |
| F09 | Six joueurs visés ; toute progression et le contrat se jouent seuls ; aucun vol, perte infligée ou classement récompensé. Échanges, combat, vol, renaissance, ventes de pièces et de multiplicateurs exclus de la v1. | Fiche:L102–L106, L114, L184 |
| F10 | Cinq offres : auto-lavage à 30 vitres/min dans la nacelle, chantier ÷2, peintures, mousse colorée, styles de tour. La promesse exclut pièces ou multiplicateur vendus et autorise confort au rythme actif, temps de chantier et apparence. | Fiche:L110–L122 |
| F11 | Le geste est central dans la boucle et présenté comme le risque principal du concept ; seules 30 vitres au plus sont des pièces séparées dans la tranche active, avec trois tours de 30, 60 et 100 étages. | Fiche:L14, L38–L46, L128–L131 |
| F12 | E3 fixe un remboursement entre 30 s et 5 min ; E4 des récompenses en minutes de revenu ; E5 des plafonds cumulés, par jour et par adversaire ; E7–E9 couvrent chemins payants, reçus et retrait d'enjeu ; E12 couvre la capacité hors ligne. | REGLES.md:L39–L48 ; seuils.json, economie |

## 2. Calculs (reproductibles)

Aucun simulateur lancé, aucune donnée de simulation reprise. Les tableaux de cadence et de profils du gabarit ne sont donc pas remplis avec des nombres inventés. Les calculs ci-dessous se reproduisent directement avec les formules et constantes indiquées.

### Conventions et bornes

- Pour les calculs en pièces les plus favorables au joueur, les améliorations permanentes sont multipliées : B = 1,5 × 1,25 = 1,875 ; gain d'action G = 1 × 2 × 3 × B = 11,25 pièces/vitre ; avec mousse, Gm = 14,0625. Si a2 remplace a1, les gains d'action sont encore plus faibles : A02 subsiste. L'ordre et la composition restent à préciser en M01.
- R désigne, dans les exemples comparatifs, un revenu de robots constant, en service, après améliorations permanentes, hors action, récompenses et mousse. C'est une convention de calcul explicite, pas une définition déjà présente dans la fiche. Les montants de contrat, de pourboires plafonnés et de hors-ligne sont donc conditionnels à cette définition ; M02 doit la fixer.
- Les projections sur 24 h supposent les cadences tenues pendant 24 h et des vitres disponibles. Ce sont des bornes du modèle, pas une observation de jeu ni une prévision de session. Lorsque cette disponibilité manque dans le texte, V07 la couvre.
- Prix fractionnaires conservés pour les calculs ; aucune règle d'arrondi inventée.

### C01 — Prix exponentiels, revenu marginal constant

Pour le nième exemplaire : prix C(n) = C(1) × 1,2^(n−1). Le remboursement marginal productif est C(n) / (r × B), et non C(n) / revenu de tout le parc. Utiliser tout le parc masquerait le défaut. B = 1,875 accorde toutes les améliorations générales, donc le résultat ci-dessous est favorable à la fiche.

| Palier, 10e copie | Prix en pièces | Revenu marginal maximal, pièces/s | Remboursement productif | Depuis paiement, chantier gratuit inclus |
|---|---:|---:|---:|---:|
| r5 | 309 586,82112 | 937,5 | 330,226 s | 370,226 s |
| r6 | 2 683 085,78304 | 6 000 | 447,181 s | 507,181 s |
| r7 | 23 734 989,6192 | 41 250 | 575,394 s | 665,394 s |
| r8 | 216 710 774,784 | 309 375 | 700,479 s | 820,479 s |
| r9 | 2 012 314 337,28 | 2 531 250 | 794,988 s | 944,988 s |
| r10 | 18 059 231 232 | 22 500 000 | 802,632 s = 13 min 22,632 s | 982,632 s = 16 min 22,632 s |

La dernière copie r10 est obligatoire pour la fin (L92). Son rendement marginal vaut 81 000 000 000 pièces/h et 1 944 000 000 000 pièces/24 h après mise en service. Son prix équivaut à 13,3772 min de ce revenu marginal. Chantiers express n'y change que l'attente initiale : 90 + 802,632 = 892,632 s. Le dépassement des 300 s existe même sans compter le chantier et sans aucun bug.

### C02 — Un joueur actif devient économiquement équivalent à un joueur immobile

Au premier r10, celui-ci seul produit au moins 12 000 000 pièces/s de base ; avec B, 22 500 000 pièces/s, soit 81 milliards/h. En comparaison, même avec toutes les améliorations et une mousse permanente :

| Source | Pièces/h | Pièces/24 h, borne continue |
|---|---:|---:|
| Lavage actif, 30/min, sans mousse | 20 250 | 486 000 |
| Lavage actif, 30/min, avec mousse | 25 312,5 | 607 500 |
| Lavage à la limite 40/min, avec mousse | 33 750 | 810 000 |
| Pourboires de 5 aides à 30/min, même en accordant Gm au propriétaire | 63 281,25 | 1 518 750 |

À 30/min avec mousse, le lavage ajoute au plus 7,03125 / 22 500 000 = 0,0000003125 du revenu de ce seul r10, soit 0,00003125 %. À 40/min, au plus 0,000041667 %. Les autres robots rendent ces fractions encore plus petites. Le joueur connecté qui ne lave rien conserve donc pratiquement toute la progression monétaire.

Le décrochage commence avant la fin : un seul r5 produit 500 pièces/s de base, contre au plus 3,75 pièces/s d'action avec a1, a2 et mousse avant facteurs communs, soit au plus 0,75 % de ce robot. Au premier r8, ce rapport tombe à 0,002273 %. Les robots des paliers précédents réduisent encore ces bornes.

Les 1 518 750 pièces de pourboires sur une journée entière de cinq aides représentent seulement 1 518 750 / (60 × 22 500 000) = 0,001125 minute de R, soit 0,0675 seconde. Le plafond annoncé de 10 minutes de R, 13,5 milliards à ce stade, est hors d'atteinte avec ce barème. Il s'agit de récompenses sociales indexées sur une action presque fixe, pas de récompenses proportionnées au revenu des robots. Ce n'est pas une duplication : la création du gain du laveur et du pourboire est explicitement voulue (L104).

### C03 — Entretenir la mousse avec les mêmes comptes

Deux comptes lavant la même façade au moins toutes les 8 s satisfont continuellement la condition « moins de 10 s » ; le compte bénéficiaire peut continuer à 30/min, l'aide n'a besoin que d'entretenir la condition. Déclencher ou rafraîchir toutes les 30 s suffit également si la synchronisation du lavage est maintenue. Aucun quota quotidien ou par partenaire ne l'arrête dans la fiche. Le bonus reste ×1,25, jamais ×1,25 à la puissance du nombre de joueurs.

| État du gain d'action | Surplus mousse à 30/min | Surplus/24 h | Surplus à 40/min | Surplus/24 h |
|---|---:|---:|---:|---:|
| Base : 1 pièce/vitre | 450 pièces/h | 10 800 | 600 pièces/h | 14 400 |
| Toutes améliorations : 11,25/vitre | 5 062,5 pièces/h | 121 500 | 6 750 pièces/h | 162 000 |

À revenu d'action constant, le supplément vaut 15 min de revenu d'action sans mousse par heure, 360 min par jour. C'est une source répétable sans quota E5 ; ce n'est pas une inflation exponentielle ni un dépassement du plafond multiplicatif écrit. La rémunération totale d'un petit groupe n'est pas transférable au compte principal, puisque les échanges sont exclus ; seuls ses pourboires lui reviennent.

### C04 — Inactivité, contrat et bornes de collusion prévues

- Absence t secondes : 0,5 × R × min(t, 7 200). Une heure absente = 30 min de R ; une absence de 2 h ou de 24 h = 60 min de R par réserve. Douze absences complètes de 2 h, avec retours et réclames corrects, donnent au plus 720 min de R/24 h. Un compte connecté immobile produit 1 440 min de R/24 h. L'absence ne bat donc pas la présence à état constant ; le problème certain est l'absence d'intérêt monétaire du geste, A02.
- Le stock de 2 h à 50 % vaut 3 600 R pièces, donc une heure de revenu en ligne. L'affichage « Réservoir d'eau : 2 h » indique une durée de travail, pas deux heures de revenu à 100 % ; le taux doit aussi être visible avant toute promesse.
- Un contrat : 40 / 30 = 1,3333 min, soit 80 s d'action active nominale, pour 600 R pièces, soit 10 min de R une fois par jour. Cela représente 7,5 fois la production de robots pendant ces 80 s, hors gain normal des vitres. À 40/min : 60 s, facteur 10. Finir après une amélioration augmente volontairement la prime de référence ; aucun exploit n'est démontré par ce seul choix de timing.
- Si les plafonds sont réellement cumulés et persistants, deux partenaires distincts ouvrent le plafond théorique de 10 min de R de pourboires/jour ; un seul partenaire est limité à 5. Cela ne garantit pas que le barème permette de l'atteindre, notamment en fin de progression (C02). Ajouter d'autres comptes ne dépasse pas 10. Il n'y a ni parrainage ni échange de victoires décrit à exploiter.
- Exemple d'impact d'un bug non démontré : rejouer une réserve pleine donne 3 600 R supplémentaires par rejeu ; une fois par minute donnerait 216 000 R/h = 3 600 min de R/h, soit 86 400 min de R/jour. Rejouer un contrat donne 600 R ; une fois par minute donnerait 600 min de R/h et 14 400 min de R/jour. Ces cadences illustrent V02/V03, elles ne sont pas des chemins autorisés par la fiche.

## 3. Défauts

P0 : casse le jeu ou la promesse d'honnêteté. P1 : dégrade nettement le rythme ou l'équité. P2 : réglage. Dans les risques à vérifier, la gravité est celle du défaut s'il est reproduit, pas une affirmation qu'il existe déjà.

### Défauts certains du papier

| # | Gravité | Statut | Défaut | Chemin démontrable | Règle touchée |
|---|---|---|---|---|---|
| A01 | P1 | certain | Les copies tardives ne respectent pas le remboursement maximal, y compris l'achat obligatoire de fin. | Acheter les dix r10 prévus ; la 10e coûte 18 059 231 232 pour 22 500 000/s au mieux : 802,632 s hors chantier. C01 ; L65–L78, L92. | E3, payback_max_s = 300 |
| A02 | P1 | certain | Le geste central et l'aide sociale deviennent pratiquement sans valeur monétaire ; les pourboires ne sont pas calibrés en minutes de production de robots. | Atteindre un r10 puis comparer une heure lavée à une heure connectée immobile ; la différence active maximale est 0,00003125 % du revenu de ce seul r10. Cinq aides durant 24 h donnent au propriétaire seulement 0,0675 s de R à ce stade. C02 ; L14, L42–L44, L84–L88, L104. | Boucle promise aux § 1–3 ; E4 pour la calibration des récompenses sociales |
| A03 | P1 | certain | La source mousse n'a pas de plafond par jour et par partenaire, alors qu'E5 l'exige. | Garder le même duo sur une façade ; réactiver le +25 % à chaque expiration. C03 ; L98 et L103 ne définissent que le plafond d'intensité, L104 ne plafonne que les pourboires. | E5 ; plafond ×1,25 respecté mais quota de source absent |

A02 est une dégradation démontrée de l'incitation économique ; aucun verdict sur le plaisir réel du geste ou la rétention n'en est déduit. A03 porte sur le modèle de récompense et sa conformité à E5, pas sur une preuve que l'utilisateur possède ou pilote effectivement plusieurs comptes. Aucun compte n'a été créé ou utilisé pendant la revue.

### Risques non démontrés : à vérifier en jeu

| # | Gravité si reproduit | Statut | Risque / scénario | Impact chiffrable | Règles |
|---|---|---|---|---|---|
| V01 | P0 | à vérifier en jeu | Auto payante + manuel, deux laveurs sur une vitre, événement de nettoyage rejoué ou cap appliqué séparément : crédit multiple. QA01–QA02. | Si 30 auto + 40 manuelles étaient acceptées, 70/min contre 40 autorisées : +30 G/min = +20 250 pièces/h et +486 000/jour à G = 11,25, hors mousse. Au-delà de 40/min, promesse de confort rompue ; une répétition sans limite n'a pas de borne. | E6, E7 ; L63, L112, L118 |
| V02 | P0 | à vérifier en jeu | Reconnexion, crash, changement de serveur, double requête ou sauvegardes concurrentes rejouent cash, réserve hors ligne, prime ou débit d'achat. QA03–QA04. | Réserve : +3 600 R par rejeu ; contrat : +600 R par rejeu. C04. Le débit répété peut aussi léser un joueur. | E8, E12 ; L94–L96 |
| V03 | P1 | à vérifier en jeu | Jour client, changement de serveur, partenaire renommé ou compteur non cumulatif réinitialisent contrat ou pourboires ; référence R circulaire ou recalculée seulement par opération. QA05–QA06. | Sans plafond persistant, k primes de contrat ajoutent k × 10 min de R ; chaque tranche abusive de pourboires ajoute jusqu'à 10 min de R. Compter une prime dans R peut auto-amplifier les suivantes : facteur indéterminé sans fenêtre de mesure. | E4, E5 |
| V04 | P1 | à vérifier en jeu | Trois robots achetés/en chantier débloquent différemment le palier selon voie gratuite, express ou reconnexion ; production hors ligne sur un chantier non terminé ; amélioration appliquée rétroactivement à toute l'absence. QA07. | Un r10 produit 12 000 000 B/s : crédit anticipé de 180 s = 4 050 000 000 pièces à B = 1,875. Les 90 s gagnées par express valent 2 025 000 000 pièces de production avancée, effet de temps prévu, pas gain illicite en soi. | E7, E12 |
| V05 | P0 | à vérifier en jeu | Rachat, reçu rejoué, reconnexion ou plusieurs appareils multiplient l'auto, le ÷2 des chantiers ou un effet cosmétique ayant un bonus caché. QA08. | Deux auto pourraient tenter 60/min ; k applications d'express donneraient T / 2^k au lieu de T / 2. Un reçu dupliqué ne doit créer aucun effet supplémentaire. | E6, E7, E8 ; L118–L122 |
| V06 | P1 | à vérifier en jeu | Mousse comptée plusieurs fois, bonus permanents retirés hors ligne, ou mousse de l'action comptée dans le revenu de tous les robots/contrats. QA09. | Deux facteurs ×1,25 donneraient ×1,5625 au lieu de ×1,25, soit +25 % au-delà du gain promis ; le hors-ligne peut varier d'un facteur 1,875 selon l'inclusion des améliorations. | E5, E12 ; L87–L98 |
| V07 | P1 | à vérifier en jeu | Vitres épuisées, nettoyées par robots/aides, passage d'étage ou contrat bloquent le joueur ; auto immobile n'a plus de vitre devant elle ; tour fermée par le propriétaire retire le support du laveur. QA10. | Une réserve de 30 vitres sans remise en saleté s'épuise en 60 s à 30/min, en 45 s à 40/min, hors robots. Perte ensuite = toute l'action promise : 30 G/min, et contrat potentiellement impossible. | E7, E12, promesses L103–L106 et L118 ; disponibilité non spécifiée |

### Ce qui manque : décisions avant le code

Ces absences sont certaines dans la fiche ; les conséquences exploitables correspondantes restent « à vérifier en jeu ». Elles ne gonflent pas le compteur des trois P1 certains.

| # | Décision à écrire | Pourquoi elle change le résultat |
|---|---|---|
| M01 | 40/min est-il un budget par UserId, partagé entre manuel, auto, tours et contrat, mesuré sur fenêtre glissante ou autrement ? Une vitre prend-elle réellement au moins 2 s ? Les ×2 puis ×3 se multiplient-ils ? | Évite le cumul 70/min, les salves aux frontières de minute et un quota global de serveur qui briderait les six joueurs. 6 × 30 = 180/min attendues contre seulement 40 si le quota était global, soit 77,8 % d'actions refusées. |
| M02 | Définir un revenu de référence unique pour prime, plafonds sociaux et absence : robots en service, permanents inclus ou exclus ; action exclue ou moyenne définie ; aucune récompense ni pourboire dans R. Définir les compteurs cumulés lorsque R change. | Évite de compter mousse/contrat/pourboire dans sa propre base et de déplacer arbitrairement les plafonds. Le mot « bonus » hors ligne ne tranche pas le sort d'a3–a5. |
| M03 | Définir un jour serveur et un identifiant de contrat, le suivi des 40 vitres, la date d'attribution d'une aide à cheval sur minuit, les quotas par UserId persistant et leur réinitialisation. | « Une fois par jour » ne précise ni calendrier, ni changement de serveur, ni progression partielle. Aucun reset à la connexion ou au changement de nom ne doit être possible. |
| M04 | Définir achat, débit, chantier, mise en service, déblocage et attribution des jalons ; préciser si les trois exemplaires doivent être achetés ou en service. Définir avancement des chantiers pendant l'absence. | Même règle pour gratuit et payant ; évite machines fantômes, mises en service en double et rente avant chantier terminé. |
| M05 | Pour chaque offre, passe durable ou produit consommable, portée, propriétaire de l'effet et comportement au rachat ; express sur chantiers en cours ou futurs ; auto sur sa tour, autrui et contrat ; point de départ et déplacement automatique. | Les prix et effets existent, mais pas le contrat exact d'achat. L'auto doit-elle continuer sur la façade de contrat ou après le déplacement d'un ami ? Le nom « Raclette automatique » désigne aussi r2 : distinguer clairement l'offre du robot. |
| M06 | Définir fenêtre de mousse, renouvellement au lieu de cumul, fin de présence du partenaire, gain du propriétaire avec mousse ou sans, et attribution par partenaire d'un groupe de trois. | Permet de tester ×1,25 et les quotas sans ambiguïté ; les aides ne doivent pas provoquer un bonus de robots ou une référence de plafond récursive. |
| M07 | Définir stock propre/sale, régénération et nombre de vitres par étage, relation entre lavage manuel/robots/avancée de la nacelle/hauteur affichée. Définir si les 40 vitres de contrat sont chargées en plusieurs lots dans la limite des 30 pièces actives. | Sans renouvellement, les projections de revenu manuel ne sont pas exécutables ; un robot ou visiteur pourrait consommer les objectifs du propriétaire. L104 promet pourtant que les deux y gagnent. |
| M08 | Définir crédit et sauvegarde atomiques, identité durable des reçus/contrats/réserves/cycles de saleté et comportement en cas de sauvegarde en échec ; préciser qu'aucune action de vente/rangement n'existe en v1 si c'est l'intention. | La fiche seule ne prouve aucune idempotence. Aucun enjeu de vol/perte n'est décrit : E9 est sans objet pour un raid ; la cohérence de progression reste à tester. |
| M09 | Fixer arrondi des coûts et fractions de pièces, précision/plafond de solde, et définition du remboursement (productif ou depuis le paiement, chantier compris). | Le coût du 10e r10 dépasse 18 milliards ; un entier signé 32 bits serait insuffisant. Aucune technologie de stockage ni panne n'est présumée. La correction d'A01 est volontairement conservatrice sur le chantier. |

## 4. Propositions

Ce sont des corrections proposées de la fiche, non appliquées, sans validation de cadence globale. Aucun effet ci-dessous n'est présenté comme résultat d'une simulation.

| Défaut | Plus petite correction de la fiche proposée | Effet calculé / limite |
|---|---|---|
| A01 | Remplacer la seule règle de prix exponentiel par : « Le prix de l'exemplaire n est min(coût du premier × 1,2^(n−1), (300 − chantier gratuit en secondes) × revenu de base par seconde d'un exemplaire). » Garder le reste pour une nouvelle simulation de cadence. | Pour un chantier T ≤ 180 et un facteur permanent B ≥ 1 : T + prix/(rB) ≤ T + (300−T)/B ≤ 300 s. Pour r10 : plafond de prix 1 440 000 000, donc 300 s avec chantier sans bonus, 244 s avec B = 1,875. Correction de la borne haute seulement ; seuil de 30 s et durée de contenu à revérifier par l'agent calcul. |
| A02 | Après définition non récursive de R selon M02, ajouter : « Gain final hors mousse d'une vitre = max(gain actuel après améliorations, 1 seconde de revenu des robots en service). La mousse s'applique une fois ensuite ; le pourboire reste 50 % de ce gain final. » | À stade avancé, 30 vitres/min rapportent 30 s de R par minute, soit +50 % du revenu robot, +62,5 % avec mousse. Le gain initial reste 1 quand R = 0. La récompense sociale suit également R ; quota de pourboires conservé. Ce réglage change le rythme : nouvelle simulation indispensable. |
| A03 | Ajouter au § 4 : « Mousse : au plus 10 minutes effectives par compte et par jour serveur, dont 5 minutes au plus attribuées au même partenaire identifié par UserId. Une activation désigne son partenaire ; renouveler remplace l'échéance, ne cumule pas l'intensité ; les durées restantes sont tronquées au quota. Ces compteurs survivent aux changements de serveur. » | Avec le barème actuel maximal, supplément journalier ≤ 843,75 pièces à 30/min, ou 1 125 à 40/min ; au plus la moitié par partenaire. Avec A02, au plus 1,25 min de R par jour à 30/min si R est constant. Valeurs proposées par analogie aux quotas de pourboires ; arbitrage du concepteur possible, plafonds explicites requis. |

Ces corrections ferment respectivement les chemins A01–A03 sur le modèle écrit. Elles ne garantissent pas les autres seuils, le plaisir ni une implémentation correcte. En particulier, le plafond de prix proposé pour A01 peut raccourcir fortement le contenu : une correction de prix n'est pas une preuve des 90 minutes actives. Les contreparties de revenu d'A02 doivent également entrer dans la prochaine simulation.

### Clauses minimales pour les risques P0/P1 non démontrés

Ces ajouts sont des propositions de spécification : ils ferment la permission d'un chemin dans la fiche, mais seule la QA peut prouver leur respect par le jeu.

| Risque | Plus petite clause à ajouter ou à préciser dans la fiche |
|---|---|
| V01 | « Le serveur valide une seule transition et un seul droit de récompense par vitre et cycle de saleté ; la répartition coopérative est définie selon M07. Le compte partage un budget glissant de 40 vitres/min entre toutes ses actions, tours et contrat. L'auto seule reste limitée à 30/min ; elle consomme ce même budget. » |
| V02 | « Chaque achat, attribution de prime et réserve possède un identifiant stable ; l'effet et sa consommation sont enregistrés durablement ensemble avant confirmation. Un reçu rejoué ne réaccorde rien, conformément à E8. Une réserve hors ligne couvre un intervalle de temps déjà fixé : son crédit et l'avancement de sa borne finale sont indivisibles. Une seule session peut engager l'état du même compte à un instant donné. » |
| V03 | « Le jour est le jour UTC du serveur. Contrat et quotas sont persistants par UserId et jour ; partenaires par UserId. R est le revenu permanent des seuls robots en service, excluant action, primes, pourboires et mousse. Chaque pourboire consomme montant/(60 × R à l'attribution) minutes de ses quotas cumulés ; un changement de R ne recrédite pas de minutes consommées. Une prime est unique pour le couple UserId/jour du contrat. » |
| V04 | « Achat → chantier → service → déblocage : seuls les robots en service produisent et comptent pour les seuils et jalons, par tous les chemins. Express ne modifie que la durée ; une mise en service n'arrive qu'une fois. Hors ligne, seuls les segments où le robot est effectivement en service rapportent, au taux permanent applicable à ces segments. » |
| V05 | « Auto et express sont des droits durables non cumulables avec eux-mêmes ; recharger ou rejouer un droit ne crée ni deuxième auto ni nouvelle division. L'acquisition ne s'applique qu'aux nouveaux chantiers, si ce choix est retenu et affiché avant achat. Toute offre cosmétique est déterministe et ne touche aucun paramètre de jeu. » Le choix nouveaux chantiers/en cours est proposé, pas prétendu présent dans la source. |
| V06 | « Les permanents se composent une fois ; mousse ×1,25 au plus, sur l'action seulement. R inclut les permanents et exclut la mousse ; prime = 600 R sans nouveau multiplicateur général. Hors ligne = 50 % des robots en service avec permanents, sans action ni bonus temporaire, limité à 2 h de service éligible. » |
| V07 | « L'action rémunérée ne s'épuise pas : une vitre propre laisse place à une autre vitre sale accessible à la nacelle ; le travail visuel des robots ne consomme pas cette disponibilité. Le contrat suit 40 objectifs distincts de son cycle. Une aide ou le départ du propriétaire ne retire aucun gain déjà validé. » M07 doit définir le renouvellement visuel et la répartition d'une finition coopérative. |

Les frontières temporelles des budgets, le moment du chantier et les descriptions de boutique doivent être identiques dans la fiche et dans les critères QA. Un simple renvoi « sécurisé côté serveur » ne remplacerait pas ces décisions.

### Monétisation : contrôle offre par offre et corrections de précision

| Offre | Promesse et contrôle papier | Précision minimale à ajouter avant le code |
|---|---|---|
| Raclette automatique, 149 | 30/min = profil actif nominal, inférieur au plafond manuel 40/min ; aucun changement du gain par vitre. Confort compatible avec le jeu non compétitif. Le fait qu'elle permette de rester connecté sans agir ne constitue pas seul une fausse promesse. | « Automatique et manuel partagent la même validation de vitre et le même budget par compte ; aucun crédit double ; aucun fonctionnement hors ligne ou hors nacelle. » Trancher M05 et garder l'auto à 30/min, même si le plafond anti-abus est 40. |
| Chantiers express, 99 | Diviser T par deux avance naturellement le revenu ; les 2,025 milliards de production avancée d'un r10 avec B ne sont pas des pièces vendues directement. La vente de temps est explicitement autorisée. | Remplacer « ne change ni les coûts ni les revenus » par « ne change ni les coûts ni le taux de production d'un robot en service ; il produit plus tôt ». Définir M04/M05 ; acquisition réappliquée sans nouveau ÷2. |
| Peintures, 49 | Douze couleurs/motifs, aucun effet de jeu annoncé. | Préciser lot complet ou choix à l'unité, propriété durable, aucun tirage aléatoire. QA08 vérifie l'absence de modification des collisions, du ciblage et des gains. |
| Mousse colorée, 29 | Changement visuel seul. | Préciser qu'elle ne déclenche ni ne prolonge la mousse économique et ne dispense pas du partenaire ou du quota. |
| Styles de tour, 79 | Apparence seule ; aucun classement récompensé. | Aucun étage/jalon, emplacement de lavage ou déblocage supplémentaire ; ne pas masquer la saleté ni bloquer la nacelle. |

Pour lever la lecture littérale « aucun achat ne donne de pièces » alors que le confort réalise des actions rémunérées, précision rédactionnelle proposée : « Aucun achat ne crédite un solde de pièces ni ne multiplie le gain par action ou le taux de production. L'auto réalise les actions normales à 30/min ; express avance la mise en service. » L'ambiguïté n'est pas comptée comme mensonge certain : l'effet de ces deux offres est déjà annoncé dans la fiche. Aucun objet aléatoire payant, pression de fausse rareté ou achat de pouvoir contre autrui n'est décrit.

## 5. Scénarios pour la QA

Ces essais sont à préparer pour la passe code/jeu ; aucun n'a été exécuté. Employer des profils de test autorisés et un banc de reçus simulés avant toute dépense ; cette revue n'autorise ni création de comptes, ni engagement artificiel, ni achat réel.

1. **QA01 — Une vitre, plusieurs chemins (V01).** Enregistrer un état de saleté et un solde ; faire finir la même vitre simultanément par deux laveurs, puis par manuel + auto, puis rejouer la requête. Attendu : une transition sale → propre et un seul droit de gain de nettoyage par cycle, avec le gain du laveur et le pourboire éventuel prévus, sans priver un joueur de sa récompense promise. Le cas coopératif exact doit d'abord être décidé en M07. Remettre la vitre en saleté : un nouveau cycle, pas de réutilisation de l'ancien.
2. **QA02 — Budgets de cadence (V01, M01).** Sur 60 s, puis autour de la frontière entre deux minutes, combiner 30 actions auto et 40 tentatives manuelles ; passer de sa tour à autrui puis au contrat. Attendu : auto seule ≤ 30/min ; total accepté ≤ 40/min par compte selon la fenêtre décidée, sans budgets séparés par source/façade. Avec six joueurs à 30/min chacun, le budget d'un joueur ne doit pas consommer celui d'un autre.
3. **QA03 — Achat/sauvegarde/reçu (V02, V05).** Pour chaque offre, rejouer le même identifiant d'achat avant sauvegarde, après sauvegarde et avant acquittement, puis après reconnexion et depuis deux sessions de test. Attendu : un seul effet durable, acquittement seulement après effet sauvegardé, aucun reçu perdu ; pas de nouveau produit ni de nouveau ÷2 pour le même droit. Pour un générateur gratuit, interrompre entre débit, création et sauvegarde : ni création gratuite ni double débit.
4. **QA04 — Stock hors ligne (V02).** Préparer R connu et une absence de 7 200 s ; attendre 24 h dans l'horloge de test ; réclamer simultanément deux fois, reconnecter/changer de serveur et rejouer l'ancienne demande. Attendu : au total 3 600 R une seule fois pour la réserve ; nouvel intervalle à partir de l'instant de coupure retenu. Tester 0, 1, 7 199, 7 200, 7 201 s et la fermeture pendant la sauvegarde. Ne pas retirer du cash gagné en ligne sur la même période.
5. **QA05 — Contrat et quotas sociaux (V03, A03).** Finir le même contrat depuis deux sessions ; changer de serveur ; simuler frontière du jour et horloge client fausse. Un contrat au plus par identifiant de jour serveur ; pas deux primes pour le même jour. Avec deux aides identifiées puis dix identités de test, vérifier 5 min de R par partenaire et 10 min au total ; changement de nom sans effet. Vérifier aussi les quotas de mousse si la proposition est retenue.
6. **QA06 — Base de revenu et instantané (V03, V06).** Fixer R puis finir une vitre de contrat en même temps que la mise en service d'un robot, un achat d'a4, un pourboire et une extinction de mousse. Attendu : un instantané serveur défini, prime = 600 R de cet instantané ; récompenses et pourboires n'entrent jamais récursivement dans R. Vérifier la comptabilité des minutes déjà utilisées lorsqu'on change R en cours de journée.
7. **QA07 — Même machine à états (V04).** Acheter le troisième r2/r3 et le premier r5/r8/r10 gratuitement, avec express acquis avant/après le début du chantier, puis reconnecter juste avant la fin. Attendu : mêmes conditions de déblocage, mêmes jalons et unique mise en service, seule la durée autorisée diffère. Aucune production avant service ; pour une absence qui traverse la fin du chantier, ne rémunérer que la période de service éligible.
8. **QA08 — Cinq offres et réachats (V05).** Tester les cinq offres individuellement puis ensemble, chargement des droits et rachat selon M05. Comparer gains, cadence, transitions et attributs physiques à un profil gratuit identique. Cosmétiques : aucune différence de jeu. Auto : ni seconde instance ni bonus caché. Express : ÷2 une fois, jamais ÷4 après rechargement d'un droit déjà possédé. Vérifier aussi les descriptions réellement affichées, pas seulement les noms du code.
9. **QA09 — Mousse et absence (V06).** Deux puis six laveurs sur la même façade ; répéter les activations, partir, reconnecter, dépasser les quotas, changer de partenaire. Attendu : action ×1,25 au maximum, aucun effet sur robots, fin/renouvellement selon M06. Mesurer séparément base, a3–a5, mousse ; après 2 h absent, vérifier le taux 50 % des seuls revenus éligibles et le plafond/taux visibles.
10. **QA10 — Disponibilité et retrait de support (V07).** Laver plus de 40 puis 300 vitres en solo, avec robots et aides ; vider une tranche ; changer de tour/jalon ; finir le contrat de 40 vitres avec au plus 30 pièces actives. Laisser l'auto dans sa nacelle et vérifier qu'une vitre est toujours proposée à la cadence promise. Faire partir le propriétaire pendant qu'un visiteur finit : ni double crédit ni action effacée sans règle annoncée. Aucun mécanisme de ranger/vendre/voler n'est décrit : ne pas inventer un raid pour valider E9.
11. **QA11 — Corrections du modèle et conversions de monnaie (A01–A03, M09).** Après révision de la fiche, vérifier chaque coût de copie et revenu marginal, et les temps jusqu'au remboursement ; tester soldes au-delà de 2 147 483 647, dépenses concurrentes, arrondis et solde insuffisant. Rejouer profils actif/lent/auto avec toutes les offres : nouvelle simulation par l'agent calcul, puis mesures de geste et d'aide à r1, r5, r8 et r10. Vérifier le quota de mousse jusqu'à sa dernière seconde. L'acceptation des propositions n'est pas une preuve d'exécution.

### Couverture de la liste minimale

| Sujet demandé | Résultat de cette revue |
|---|---|
| Duplication / retrait d'enjeu | V01–V04, QA01–QA07 ; pas d'enjeu de perte/raid dans la v1, donc aucun contournement de perte certain inventé |
| Chemins payants et rejeu | C01/C04, V01/V04/V05 ; contrôle individuel des cinq offres et QA02/QA03/QA07/QA08 |
| Comptes multiples | A03 ; quotas de pourboires bornés si correctement appliqués, V03 et QA05 ; ni parrainage ni échange de victoires décrit |
| Inflation et cumul | C02–C04, A02/A03, V03/V06 ; ×1,25 n'est pas un multiplicateur cumulatif de robots ; récompenses tardives d'action/social quasi nulles |
| Inactivité / hors ligne | C02/C04, A02, V02/V04/V07, QA04/QA07/QA09/QA10 ; hors-ligne 50 % et 2 h ne battent pas la présence à état constant |
| Honnêteté | Contrôle offre par offre ; aucun P0 certain ; promesses d'auto, de temps et de stock à qualifier en jeu ; aucun pouvoir contre autrui décrit |

## 6. Frictions

1. Le gabarit commun impose « cadence PASSE / ÉCHEC », tableaux du simulateur et « simulation rejouée », même pour l'adversaire indépendant auquel on interdit de lire SIMULATION.md. J'ai renseigné « non évaluée » et des effets calculés directement ; aucun résultat emprunté ou inventé. Proposition déposée dans CONNAISSANCES/PROPOSITIONS/2026-11-15-adversaire-gabarit-revue-independante.md ; aucun gabarit modifié.
2. Le gabarit ne distingue pas gravité d'un risque non démontré, défaut certain de spécification, et preuve en jeu G15. Cette revue sépare ces trois états et ne compte que A01–A03 ; sans cette séparation, des risques génériques de DataStore pourraient être pris pour des P0 établis.
3. « Minutes de revenu », « tous les revenus », « bonus hors ligne » et « remboursement » ne définissent pas leurs bases. Ces ambiguïtés empêchent de certifier primes et plafonds sans inventer un modèle. Elles sont portées en M02/M09 ; A01 reste prouvé même avec toutes les améliorations et sans chantier.
4. La fiche revendique E5 sur les pourboires et le plafond ×1,25, ce qui peut faire oublier les plafonds de source de la mousse. Le contrôle a donc été fait source par source, pas seulement sur le multiplicateur total.
5. La lecture initiale sans encodage explicite a mal affiché les accents ; les sources ont été relues en UTF-8. Aucun fichier source n'a été réencodé. STOP a été contrôlé absent ; l'empreinte de la fiche doit rester identique jusqu'à la remise du rapport.

RESULTAT: echec | JEUX\lave-la-tour\03-economie\RAPPORT-ECONOMIE-adversaire.md | 3

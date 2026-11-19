# Chantiers de l'usine : d'une chaîne qui fait un jeu à une entreprise qui tourne seule

Tenu par l'orchestrateur, relu à chaque bilan. Origine : veille `VEILLE\RELEVES\2026-11-16\a1-usines-logicielles-autonomes.md` (16 pages lues, 33 constats sourcés : guides d'éditeurs sur les agents de longue durée, documentation des CLI, cadres multi-agents à rôles et leurs évaluations, règles de Discord, Roblox et YouTube), et demandes du propriétaire du 16/11/2026.

Ce que cette veille confirme de l'usine : des mandats précis par rôle, l'état gardé hors du contexte des agents, des portes de validation, une évaluation par un autre modèle que l'auteur, une mémoire de règles corrigée au bilan. Ce qu'elle dit de la hiérarchie : **un directeur par pôle ou un manager au-dessus d'un seul exécutant serait du décor** (mêmes décisions répétées, coût, pertes à chaque transmission) ; un sous-planificateur ne se crée que si plusieurs flux saturent réellement l'orchestrateur, et cela se prouve par une mesure. L'organisation retenue est dans `PROCEDURES\14-ENTREPRISE-BOUCLE-D-EXPLOITATION.md` § 2.

Ordre : sécuriser et prouver avant d'étendre l'activité publique.

| Rang | Chantier | État au 16/11/2026 | Ce qu'un agent bâtit | Ce que le propriétaire fait une fois | Reçu quand |
|---|---|---|---|---|---|
| 1 | **Mandats exécutoires** : que les interdits soient des refus techniques, pas seulement du texte | À faire. Aujourd'hui : verrous, crochets git, refus des secrets ; les agents Claude lancés par la CLI tournent sans confirmation de permission (`routage.json`) | Table outil, cible, effet par rôle ; réglages de permissions par rôle ; tests de refus | Trancher l'écart entre le garde-fou G2 (« l'orchestrateur ne compte pas ») et `routage.json` (« orchestrateur compris », plus strict, appliqué) | Une écriture ou un engagement hors mandat est refusé par l'outil |
| 2 | **Premier cycle réel** : un même jeu suivi de la veille aux joueurs | En cours : `lave-la-tour`, code testé hors Studio ; rien de vu en jeu | Prototype en Play, passe 2, QA à deux clients, release, bilan | Libérer Studio ; un univers TEST | Chaque étape a sa preuve vue en jeu |
| 3 | **Permanence fiable** : battement, reprise, pas de double lancement | Outils écrits le 16/11 (`battement.py`, `service-usine.ps1`), à relire par un autre modèle | Prise exclusive, reprise après redémarrage, essais de panne | `service-usine.ps1 installer -Confirmer` | Un redémarrage ne perd aucun événement et ne lance rien deux fois |
| 4 | **Alerte du propriétaire** | Outil écrit le 16/11 (`prevenir.py`), aucun canal configuré | Raccordement aux alertes ; accusé de réception ; canal de secours | Choisir un canal, poser son secret (`OUTILS\GABARITS\CONTACT-LISEZ-MOI.md`) | Un incident simulé arrive sur son téléphone, sans secret dedans |
| 5 | **Quotas, arrêt, audit** | En partie : `STOP` avant chaque lancement, plafond d'agents, durées maximales, journal des délégations | Arrêt des agents déjà lancés ; budget par jour et par jeu ; coût par jeu au bilan | Fixer les plafonds | `STOP` arrête aussi ce qui tourne ; un jeu trop cher s'arrête seul |
| 6 | **Évaluations du harnais** : savoir si une règle nouvelle améliore vraiment | À faire. Aujourd'hui : règles avec origine et statut, limite de 80 règles | Jeu de cas réservés, comparaison avant et après, mutations (règle P14), retrait des règles inutiles | Dire ce qui compte comme un jeu réussi | Une régression injectée dans une procédure est détectée |
| 7 | **Succès et échecs mesurés** | Outils faits (`mesures-joueurs.py`), aucun joueur réel | Cohortes, causes, « pourquoi ça a marché » au bilan de suivi | Clé Open Cloud de lecture | Une alerte « ce jeu marche » repose sur un échantillon suffisant |
| 8 | **Comparaisons régulières sur internet** | Veille faite deux fois à la main ; revue de la semaine écrite (procédure 14 § 5), jamais jouée | Veille planifiée, journal des décisions qu'elle a changées | Rien, sauf nouvelle source | Chaque décision de la semaine cite une donnée datée |
| 9 | **Communauté officielle** | À faire ; bloqué sur le canal | Bot de questions fréquentes et de tickets, charte pour un public mineur, modération réversible, transparence (« je suis un robot ») | Créer le serveur Discord et le bot, désigner un modérateur humain de recours | Spam, injection, donnée personnelle et message d'un mineur en difficulté sont traités comme prévu |
| 10 | **Relation commerciale** | Tri écrit (procédure 14 § 3) ; aucun canal d'entrée | Registre des offres, fiche sur l'expéditeur, brouillons non engageants | Une adresse de contact ; il signe lui-même | Toute offre lui arrive, aucune n'est acceptée, refusée ni négociée par un agent |

Chantiers ajoutés par l'orchestrateur (procédure 14) :

| Chantier | État au 16/11/2026 |
|---|---|
| Interrupteurs à distance, pour contenir un incident sans republier | Gabarit Luau et outil faits et testés ; à intégrer au premier jeu ; clé d'écriture à part à poser par le propriétaire |
| Sondage en jeu (note de 1 à 5 et une question, sans récompense) | Gabarit serveur fait et testé ; interface et intégration à faire |
| Compteurs d'incident écrits par les jeux (`refus_`, `anomalie_`) | Lus par les mesures et le battement ; fonction de comptage libre à ajouter au gabarit des mesures, puis à appeler dans chaque refus de Remote |
| Notes de version « corrigé grâce à vos retours » | À faire |
| Modules éprouvés remontés dans les gabarits | Règle écrite (procédure 14 § 6) ; s'appliquera au premier jeu qui passe P7 |
| Battement : distinguer un verrou qui bloque le travail restant d'un verrou qui ne le concerne pas | À faire (le 16/11 il se dit bloqué alors que `lave-la-tour` avançait hors Studio) |
| Banc Luau : simuler la latence et le budget d'écriture des DataStore | À faire, en priorité : sans cela, le banc a laissé passer une écriture par vitre lavée (revue du commit `8702805`, S1 et S2). Proposition en attente : `PROPOSITIONS\2026-11-16-relecteur-code-2-banc-datastore-latence.md` |
| Relecture par un autre modèle de `prevenir.py`, `battement.py`, `interrupteurs.py` | À faire : ces trois outils n'ont été relus que par l'orchestrateur et par leurs propres tests |

Limite à garder en tête : ces actions initiales ne garantissent pas zéro intervention future. Un renouvellement d'accès, de nouvelles conditions d'utilisation, un incident ou un engagement nouveau rappelleront le propriétaire ; l'usine doit alors le prévenir, pas contourner.

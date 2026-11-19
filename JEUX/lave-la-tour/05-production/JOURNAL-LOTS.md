# Journal des lots — Lave la tour (`lave-la-tour`)

Tenu par le producteur. Une ligne par lot terminé. « Vu en jeu » = constaté en Play, avec capture ou mesure. Tout le reste est « non vérifié ».

Place : aucune place utilisée. Studio et bureau verrouillés par un autre agent. Travail texte uniquement du 2026-11-16, sans commit, sauvegarde de place ni publication.

| Lot | Date | Commit | Contenu | Vu en jeu | Console | Non vérifié | `save_place` |
|---|---|---|---|---|---|---|---|
| Clients et monde | 2026-11-16 | 93b96f5 | Scripts clients, MondeService et tests associés | Non vérifié en Play | Contrôles hors Studio historiques ci-dessous | Rendu, physique, caméra, réplication | Non exécuté |
| L0 serveur | 2026-11-16 | f07996f | Exécuté hors Studio : Amorce, cinq Remotes, profils mémoire ; annexe A par Remotes et horloge : 275 contrôles | Non vérifié en Play | Banc sans erreur asynchrone | Caméra, tactile, trois passes réelles, physique des sièges, effets, réplication, P4 | Non exécuté |
| L1 | 2026-11-16 | f07996f | Exécuté hors Studio : Config, Nombres, EtatJoueur, économie ; 619 + 154 + 432 contrôles, 105 achats par profil, actif 5 829 s et lent 6 421 s | Non vérifié en Play | Banc sans erreur asynchrone | Revue indépendante sur commit et économie observée en jeu ; aucune persistance L2 | Non exécuté |
| L3 logique | 2026-11-16 | f07996f | Exécuté hors Studio : vitres à deux, budget partagé, pigeons, déménagement, Flèche et M12 : 219 contrôles ; validations Remotes et actions Studio : 75 | Non vérifié en Play | Banc sans erreur asynchrone | Scènes et interactions réelles ; intégration des autres lots | Non exécuté |

## Actions de test (réservées à Studio)

| Action | Effet | Depuis quel lot |
|---|---|---|
| `studioPieces(n)` | Fixer le solde borné | L0 serveur |
| `studioAvance(secondes)` | Avancer revenus et chantiers | L1 |
| `studioPalier(id, n)` | Poser des robots en service | L1 |
| `studioTour(numero, rangees)` | Poser une tour de test | L3 |
| `studioAbsence(secondes)` | Calcul hors ligne, sans persistance | L1 |
| `studioJourSuivant()` | Réinitialiser contrat et quotas pour tester le prochain jour | Point d'accroche L5 |
| `studioJoueurFictif()` | Fournir un profil fictif neuf (aucun vrai joueur créé) | L0 serveur |
| `studioQuota(nom, valeur)` | Fixer un quota borné | Point d'accroche L4 |
| `studioEtincelante()` | Finir la façade sans crédit | L3 |

Les fonctions de test reçoivent le profil comme premier argument serveur. `ActionsDeTest.profil(joueur)` fournit le profil mémoire seulement en Studio. Aucun Remote ne donne accès aux actions de test. Toutes sont inertes avec `banc.studio(false)`.

## Écarts avec `economie.json`

Aucun écart de valeur entre Config et economie.json. Les prix sont des produits décimaux exacts depuis le coût initial : dixième r10 = 7 931 566 754 660. Le rejeu achète effectivement les 105 objets aux instants du simulateur, sans crédit de tolérance. Les deux fins de contenu sont exactement celles demandées. L'annexe A donne bien 10, 12,40 et 16,70 avant les trois achats ; 28 vitres à 60 s et 88 à 180 s.

Précisions de raccordement :

- Le profil sauvegardable reste celui du § 3.2. Présence, attributions horodatées, scène de déménagement et budget sont exclusivement en mémoire. Le budget survit à une reconnexion sur le même serveur pendant sa fenêtre. Sa continuité entre serveurs n'est pas qualifiée par ce lot.
- `VitresService.inscrire`, `asseoir`, `liberer`, `quitter` sont les points d'entrée serveur pour les lots sociaux/monde ; `horloge(f)` injecte le temps du banc. `consommer_budget` est le point commun du futur contrat et des tours. Le test de la 41e vitre préconsomme 39 unités par ce point serveur, puis finit réellement une vitre et refuse la suivante sur une autre tour malgré une attribution assez ancienne. Aucun ContratService n'est créé.
- Sur la Flèche, `tour.rangees` compte les rangées finies des segments, les numéros de vitre attribuée commencent à 401. `Etat.tour.etage` donne l'étage absolu affichable ; le record ne compte que les segments lavés une première fois. Les pigeons restent prioritaires après achat d'un segment (M12).
- Pour `Acheter("segment", id)`, `id` est l'identifiant d'opération choisi pour cet achat (32 caractères au plus), à réutiliser en cas de répétition. Les autres achats utilisent r1…r10 ou a1…a5. Le Remote Action ne transmettant pas d'identifiant de déménagement dans le plan, le serveur en crée un et refuse tout nouveau déménagement pendant les 20 secondes de scène. Le service pur accepte explicitement l'identifiant pour le rejeu.
- `hors_ligne` calcule le crédit sur R au départ et finit les chantiers au retour. La consommation atomique de l'intervalle et sa persistance sont du ressort de DonneesService L2 ; les points d'accroche sont indiqués dans Amorce.

Limites trouvées dans l'outillage (aucun fichier OUTILS modifié) :

- `sim-economie.py --json` fournit les nombres d'achats et fins, mais aucune liste horodatée. `tests/generer-attendus.py` lit cette sortie, puis charge en lecture seule la classe publique `Sim` du même fichier pour obtenir les chronologies et jalons ; il vérifie leurs nombres et fins contre la sortie JSON. Les caches Python sont désactivés. Le banc n'importe pas de modules voisins des tests : les attendus sont écrits dans `src/ServerStorage.Tests.Attendus.lua` et chargés par `banc.require("ServerStorage.Tests.Attendus")`.
- Le banc ne fournit pas `setmetatable` aux scripts testés. Le registre serveur utilise donc des tables ordinaires et une libération explicite à la sortie, sans modification du banc.
- Sous Windows PowerShell 5, `luau-verif.ps1` s'arrête sur les diagnostics natifs de globales Roblox avant son filtre. `src/.luaurc` déclare uniquement `game`, `script`, `Instance`, `task`, `time` ; les modules dynamiques utilisent `--!nocheck` pour l'analyse autonome sans types Roblox. L'analyse des globales inconnues reste active et la compilation est complète. Aucun diagnostic n'est filtré par un changement de l'outil.

Sorties réelles conservées : `tests/RESULTAT-VERIF.txt` et `tests/RESULTAT-BANC.txt` (sortie verbeuse intégrale). Dernière exécution : `controle complet : 8 fichiers, 0 defaut(s)` ; code 0. Banc : six fichiers passés, **1 774 assertions** (hors messages de fin de scénario), code 0.

| Test | Contrôles passés |
|---|---:|
| annexe-a.test.luau | 275 |
| config.test.luau | 619 |
| economie.test.luau | 154 |
| rejeu-simulateur.test.luau | 432 |
| remotes.test.luau | 75 |
| vitres.test.luau | 219 |

## Transmis à la QA

Tout reste **non vérifié en Play** : import des scripts dans Studio, rendu, sons, caméra, saisie tactile et reconnaissance des passes, assise physique, réplication et latence, scène de déménagement, monde à 401 étages et plus, véritable session à deux clients et P4/P5. Le banc utilise la présence serveur en nacelle ; le raccordement au siège physique sera réalisé avec le monde.

Les modules exclus n'ont pas été créés : sauvegarde et verrou de session, social/mousse/pourboires, contrat et primes, commerce, mesures et retours. Les actions correspondantes de `Action` restent silencieusement inactives jusqu'au raccordement de leurs services. Aucune erreur du banc ne prouve l'absence d'erreur en console Roblox. Aucune porte Studio n'est déclarée franchie.


## Complément serveur du 2026-11-16 — L2, L9, L4, L5, L6

Auteur : Codex, rôle 05.codeur. Travail texte uniquement, sans sous-agent, installation, Studio, bureau, commit ni publication. Ce complément remplace les mentions historiques « modules exclus non créés », « aucune persistance L2 » et les anciennes limites de réservation. Les six tests historiques sont conservés sans modification et passent toujours : **1 774 contrôles**.

### Lots et fichiers

Ordre de réalisation : L2, L9, L4, L5, L6 ; tests du lot exécutés avant le suivant et banc complet relancé. Les avertissements temporaires de MondeService et le test monde ajoutés par un autre agent ont disparu à la vérification finale sans modification de ces fichiers par ce codeur. Les lots suivants ont été préparés pendant ce blocage extérieur ; aucune qualification intermédiaire à zéro défaut n'est revendiquée pour ces passages.

| Lot | Commit | Fichiers écrits ou raccordés | Contrôles propres au lot, dernière exécution | État |
|---|---|---|---:|---|
| L2 | 8702805 | `src/ServerScriptService.Jeu.DonneesService.lua`, `src/ServerScriptService.Jeu.Amorce.server.lua`, `tests/donnees.test.luau` | 702 | Exécuté hors Studio |
| L9 | 8702805 | Copies octet pour octet de `src/ServerScriptService.Jeu.MesuresService.lua`, `src/ServerScriptService.Jeu.RetoursService.lua`, `src/StarterPlayer.StarterPlayerScripts.RetoursClient.client.lua` ; raccordement Amorce ; `../retours.json` ; `tests/suivi.test.luau`, `tests/gabarit-mesures.test.luau`, `tests/gabarit-retours.test.luau` | 34 + 28 + 20 = 82 | Exécuté hors Studio |
| L4 | 8702805 | `src/ServerScriptService.Jeu.SocialService.lua`, lecture de la position serveur dans VitresService, raccordement Amorce ; `tests/social.test.luau` | 35 | Exécuté hors Studio |
| L5 | 8702805 | `src/ServerScriptService.Jeu.ContratService.lua`, raccordement Amorce ; `tests/contrat.test.luau` | 170 | Exécuté hors Studio |
| L6 | 8702805 | `src/ServerScriptService.Jeu.CommerceService.lua`, `Config.OFFRES`, durée des nouveaux chantiers dans EconomieService, raccordement Amorce ; `tests/commerce.test.luau` | 24 | Exécuté hors Studio |
| Correctifs de revue | 8702805 | Config, VitresService, EtatJoueur, DonneesService, Amorce ; `tests/revue-d1.test.luau` à `revue-d4.test.luau` | 3 + 3 + 6 + 2 = 14 | Exécuté hors Studio |

Fichiers de preuves remplacés par écriture temporaire, relecture puis remplacement : `tests/RESULTAT-BANC.txt`, `tests/RESULTAT-VERIF.txt`. Les autres nouveaux tests `geste`, `monde`, `textes` sont ceux des agents voisins : 52 + 46 + 150 = 248 contrôles ; ils sont inclus au banc complet, sans en revendiquer la réalisation.

**Dernier résultat : 20 fichiers de test passés, 3 049 / 3 049 assertions, code 0 ; contrôle complet : 21 fichiers, 0 défaut, code 0.** Le comptage exclut les lignes de titre des fichiers et « scénario terminé ». Les trois copies de gabarit ont été comparées octet pour octet avec leurs sources, identiques.

### Décisions prises par le codeur

1. La valeur DataStore est une enveloppe `{profil, session={id,instant}}` ; le profil respecte le § 3.2, sans champ supplémentaire. Les anciennes valeurs contenant directement un profil restent lisibles. Magasin `LaveLaTourJoueurs_v1`, suffixe `_studio`, clé `j_<userId>`, métadonnée userId. JobId vide en place locale : identifiant serveur aléatoire. Un verrou de exactement 600 s est encore vivant ; il ne devient mort qu'au-delà de 600 s. Pas de reprise d'un verrou vivant d'un autre serveur.
2. Chargement et crédit hors ligne sont un même UpdateAsync. Le transformateur peut être rappelé ; aucune mutation de profil exposé n'y est faite. L'identifiant `absence:<depart>`, le crédit et `depart=0` sont persistés ensemble. Trois essais, attentes 1 puis 2 s. Une réponse perdue après écriture se rejoue sans nouveau crédit. Échec ou migration illisible : clé de renvoi `donnees_indisponibles`, pas de profil en mémoire, pas de sauvegarde de remplacement. La réparation des types JSON incorrects reste autorisée par EtatJoueur ; une erreur de migration ne devient plus un profil neuf.
3. Pour un arrêt brutal, une sauvegarde périodique enregistre son instant comme dernier point de reprise dans `depart`, sans changer le `depart=0` du profil actif. Sortie : dernier état et libération du verrou ensemble. Fermeture : gel des profils exposés, sauvegardes finales parallèles, attente des tâches ; une sortie ayant échoué reste également dans le registre de DonneesService pour cette dernière tentative. Aucune promesse de réussite si le serveur est tué avant sa fermeture effective.
4. M08 : une action serveur acceptée reçoit un identifiant ; les profils effectivement modifiés sont sauvegardés avant émission de l'état confirmé et des effets de l'action. Les demandes arrivées pendant cette opération sont refusées ; la boucle attend sa fin pour modifier les profils. Le revenu écoulé est repris au tour suivant. Les identifiants et les masques persistent avec les soldes. Cette politique stricte doit être mesurée sous les budgets réels de DataStore : les tests ne qualifient pas le débit d'écritures.
5. Réservation abandonnée D1 : expiration après **10 s** (nouvelle constante `Config.RESERVATION_MAX_S`), reprise seulement strictement après cette borne. La fiche ne fixe pas ce délai : choix conservateur conforme à la proposition de la revue. L'ancien attributaire perd son droit de finition dès la reprise ; aucune vitre n'est accordée deux fois. La boucle ne renouvelle pas silencieusement le début d'une réservation.
6. D2 : un seul visiteur, même lorsque le propriétaire est ailleurs ; le propriétaire peut toujours rentrer. Pour la borne, le serveur vérifie la présence sur la place, la place libre et une distance maximale de **8 unités** à la borne de la parcelle ciblée ; ce rayon absent de la fiche est un choix strict et injectable pour le banc. Sans monde ou personnage attesté, refus. Aucun déplacement physique de personnage n'est ajouté par ce lot : le raccordement aux sièges du monde reste à qualifier en Play.
7. D3 : à zéro segment de Flèche, les pigeons utilisent le sommet absolu 400 et donc les étages 381 à 400. Le même calcul est appliqué à la validation du profil pour ne pas perdre cette zone au retour. Aucun segment ni record gratuit.
8. Mousse : comptage du temps écoulé avant déplacement, changement de partenaire et changement UTC ; pas de quota recrédité au changement de rôle. Le drapeau reste visible après les plafonds ; clé `mousse_quota_atteint`. Pourboire basé sur le gain du propriétaire sans mousse, plancher R=1 et prorata indépendant aux deux plafonds. « Chez visiteur » revérifie le duo et le stock au clic ; M13 détache le visiteur avant l'ouverture du contrat.
9. Contrat : aucune remise à zéro d'un contrat incomplet au passage de minuit ; le jour de consommation est celui de la 40e vitre. La prime et son opération `contrat:<jour UTC>` sont uniques ; R est lu à la dernière vitre. Une réouverture dans le même jour de prime est refusée.
10. Commerce : les cinq identifiants valent 0, sans offre envoyée au client. Sans identifiant actif, aucun écouteur d'achat n'est nécessaire ; avec une offre active, PromptGamePassPurchaseFinished déclenche la relecture serveur de possession. Un échec de relecture n'accorde pas de passe. Pas de rattrapage en rafale des vitres automatiques après un retard ; pas d'automatisme hors nacelle ; même fonction de finition que le Remote manuel. Aucun reçu consommable acquitté.
11. Les trois gabarits L9 sont copiés **sans adaptation**, conformément à la demande explicite. Ils contiennent eux-mêmes des phrases bilingues ; cette exception à la règle générale des clés de texte est limitée à ces copies imposées. Dans Amorce, `mesures.premier_jour=""` est normalisé en nil avant `joueur_arrive`, puisque le gabarit attend nil pour compter un nouveau compte. La fermeture des mesures est coordonnée après `joueur_part` puis sauvegarde des profils.

### Revue indépendante f07996f : corrections et suites

Le rapport `REVUE-CODE-f07996f.md` était absent au début, puis présent avant la fin ; il a été lu. Les trois tests D1, D2, D3 ont été exécutés **avant correction** : trois fichiers en échec, respectivement réservation bloquée, second visiteur accepté et stock absent après 10 s. Après correction, les trois passent avec contrôles de borne et rechargement D3.

- **D1, D2, D3 (trois P1 certains) corrigés**, aucun P0 ou P1 certain laissé dans cette revue.
- **D4 (P2) corrigé** : une erreur de la boucle d'un joueur n'arrête plus la boucle de tous ; profil incohérent renvoyé sans écrasement, autre compte toujours rémunéré (test dédié).
- **D5 (P2) corrigé** : EtatJoueur ne transforme plus une erreur interne de validation en profil neuf ; DonneesService refuse aussi explicitement une migration qui renvoie nil (test dans donnees).
- **D6 (P2) laissé** : le générateur et les six tests historiques sont conservés ; aucune nouvelle preuve d'égalité des soldes avec le simulateur n'est revendiquée. L'ancienne phrase du journal « deux fins de contenu exactement celles demandées » ne vaut pas preuve indépendante de non-avance du code.
- **D7 (P2) partiellement renforcé** par les nouveaux tests de réservation, propriétaire, Flèche, boucle et rejeu d'un déménagement avec la tour suivante réellement ouverte. Les assertions historiques de cadence Action et de durée simulée restent à renforcer ; aucun changement demandé hors des correctifs P0/P1 n'est revendiqué comme achevé.
- **D8 (P2) et P3 restants laissés** : pas de refactorisation générale des constantes ni de modification des fichiers clients appartenant à d'autres agents. Les littéraux de ces services reprennent les valeurs figées ; leur centralisation reste une suite de maintenance. La correspondance serveur de `assis` est maintenant changée seulement après une transition acceptée, et les effets d'action attendent la sauvegarde.

### Écarts et limites transmis à la QA

Tout reste **non vérifié en Play** : assise et téléportation physiques, proximité de borne avec de vrais personnages, réplication des deux laveurs, rendu de la mousse après quota, effets et priorité des boutons, contrat visible, achats réels, latence, contrôles tactiles, imports des scripts, P4/P5. La clé `donnees_indisponibles` est émise pour le renvoi ; sa formulation localisée doit être fournie par le propriétaire de Textes (ce fichier n'a pas été modifié).

Q01/Q02 : les tests couvrent masques désordonnés, pigeons, réservation libérée, soldes restaurés, réponse perdue après crédit de réserve, accès Flèche à 99/4 et 100/5, rejeux d'opérations avec conditions d'achat réellement ouvertes. Ils **ne prouvent pas une transaction atomique entre les profils de deux comptes** : Roblox ne fournit pas de transaction multi-clés dans UpdateAsync. Un arrêt brutal entre deux écritures de profils sociaux reste un risque non levé ; aucun scénario de coupure à chaque frontière d'écriture entre ces deux profils n'est déclaré qualifié. La sauvegarde avant confirmation borne ce risque sans le supprimer.

Autres limites réelles : budgets, contention et rappel du transformateur sur Roblox, cache, latence, réponses perdues, plafond de taille réel et échéance réelle de BindToClose ne sont pas qualifiés par le banc. Le verrou peut rester 10 minutes après une panne. Le budget de vitres reste celui du cœur existant : conservé par compte sur le même serveur, **pas durable entre serveurs** (P3-14 de la revue). Les quotas sociaux, eux, sont persistés. Les opérations sont bornées à 50 comme le plan ; un identifiant ancien éjecté n'est pas un reçu conservé indéfiniment.

Ces limites empêchent de déclarer Q01/Q02 entièrement qualifiés ou les lots prêts pour une release. Aucune publication ni porte Studio déclarée franchie. Les cinq services sont implémentés et exécutés hors Studio ; une qualification intégrale, notamment des pannes sociales entre écritures, reste due.

Statut de remise : **echec pour la demande intégrale**, malgré le banc vert. Cinq lots implémentés ; Q01/Q02 incomplets et budget de lavage entre serveurs non durable. L9 et L5 sont terminés pour leur preuve hors Studio ; L2/L4 et la qualification complète de M01/L6 restent incomplets sur ces exigences. Aucun P0/P1 certain de la revue f07996f laissé sans correction.

## Intégration du 2026-11-16 — D6, D7 et raccordement du monde

Cette passe remplace les statuts historiques « D6 laissé », « D7 partiellement renforcé », l'absence de chronologie JSON et l'absence de traduction de `donnees_indisponibles`. Aucun Studio, bureau, commit, installation ou sous-agent utilisé. Modifications limitées à `05-production` ; mutations sur copies temporaires hors dépôt, supprimées après exécution.

| Lot | Commit | Exécuté hors Studio | Non vérifié en Play |
|---|---|---|---|
| Intégration | Aucun, travail non commité | Rejeu des soldes, refus anticipés et fins ; D7 ; construction, attribution, libération et mises à jour du monde sous pcall ; Etat social ; traductions ; mutations | Import Studio, rendu, Seat et assise physique, déplacements, caméra tactile, latence, deux vrais clients, P4/P5 |

- **D6** : le générateur consomme exclusivement `chronologie_achats`, `jalons_s` et `fin_s` du JSON public ; plus aucun chargement de la classe interne Sim. Le JSON ne fournit pas les soldes : ils sont **calculés** dans le générateur par rejeu de la chronologie et des formules du simulateur (mises en service avant achat, revenu après achat, multiplicateurs permanents et cadence du profil). Aucun nouveau choix d'achat n'est recalculé. Les 105 achats de chaque profil passent, avec contrôle du solde après chacun, et refus une seconde avant si le solde calculé ne permettait pas l'achat. La première ouverture complète du code est mesurée indépendamment : actif 5 829 s, lent 6 421 s, comparées aux valeurs JSON.
- **Précision numérique** : écart relatif ≤ 10⁻⁶ ; seulement si le solde attendu est de module < 10⁻¹⁰, comparaison absolue ≤ 10⁻¹⁰. À l'achat actif n° 12, les additions séparées du code et l'addition groupée du simulateur laissent un résidu différent d'environ 2,84 × 10⁻¹⁴ pièce près de zéro ; ce n'est pas une divergence économique avec la fiche. Cette convention près de zéro est explicite et ne modifie aucun crédit du jeu.
- **D7** : le troisième appel Action tente maintenant une montée réellement possible, et sa position doit rester sur la place ; après expiration de la cadence la même montée réussit. Le déménagement rejoué est tenté avec la tour suivante débloquée et la scène terminée, puis un identifiant neuf permet effectivement la transition.
- **Monde** : `monde-raccorde.test.luau` exécute Amorce ; parcelle attribuée à l'arrivée, tour de 600 unités, nacelle à la première rangée puis à 10,5 unités après dix vitres, façade propre de 10 unités. Construction, attribution et mise à jour défaillantes sont injectées ; profils, revenus et Etat continuent. Départ : tour détruite et parcelle libre. Seat est explicitement remplacé par Part dans ce test : aucune preuve de physique. `Etat.proprietaire` désigne la tour visitée ; `bouton_contextuel` est une table de disponibilités, avec cible et nom issus de SocialService, testés avec deux joueurs fictifs amis. Les autres risques du premier Play et la centralisation générale D8 restent dus.
- **Textes** : ajout anglais/français de `donnees_indisponibles`, `achat_verrouille` et `achat_impossible`. `mousse_quota_atteint` existait déjà comme alias bilingue ; le test couvre maintenant explicitement sa résolution et celle des autres clés serveur dans les deux langues.

### Mutations exécutées sur copies temporaires

| Mutation | Code du banc | Tests détecteurs |
|---|---:|---|
| Gain d'une vitre × 2 | 1 | `rejeu-simulateur` (achat prématuré n° 1), ainsi que `annexe-a`, `donnees`, `economie`, `social`, `vitres` |
| Revenu × 1,5 | 1 | `rejeu-simulateur` (achat prématuré n° 2), ainsi que `annexe-a`, `contrat`, `donnees`, `economie`, `monde-raccorde`, `social` |
| Plafond de 40 vitres par minute retiré | 1 | `vitres` (41e refusée), `commerce` (manuel 41 refusé), `contrat` (41e refusée) |

Deux mutations supplémentaires vérifient D7 : cadence Action portée à 100 → `remotes` échoue ; contrôle de l'identifiant de déménagement retiré → `vitres` et `donnees` échouent. Toutes les copies temporaires ont été supprimées.

**Sorties finales réelles** : banc **21 / 21 fichiers passés, 3 501 / 3 501 assertions**, code 0 (hors titres et 21 lignes « scénario terminé ») ; `luau-verif` : **`controle complet : 21 fichiers, 0 defaut(s)`**, code 0. Trois mutations économiques demandées détectées sur trois. Cinq points de cette passe exécutés sur cinq, aucun point laissé à moitié. Sorties intégrales : `tests/RESULTAT-BANC.txt`, `tests/RESULTAT-VERIF.txt` ; synthèse des mutations : `tests/RESULTAT-MUTATIONS.txt`. Les limites de persistance sociale et de budget entre serveurs consignées plus haut demeurent ; cette intégration ne vaut pas qualification en Play.

- 2026-11-16 — Sauvegarde, correction S1 à S5 : FAIT S1/S2 actions confirmees en memoire sans verrou global ni ecriture par action ; profils marques ecrits toutes les 60 s, a la sortie et a la fermeture (chargement/verrou + credit hors ligne toujours atomiques). FAIT S3 panne periodique : profil conserve et reprise au cycle suivant ; expulsion seulement si verrou perdu. FAIT S4 sortie : trois series de trois essais DataStore (attentes internes 1/2 s, reprises espacees 4/8 s), puis expiration immediate du verrou en dernier recours sans modifier le profil durable ; memoire conservee pour fermeture, aucun ecrasement si un autre serveur a repris. En panne totale, liberation impossible mais expiration jamais prolongee. FAIT S5 chargement : six tentatives espacees de 5 s sur verrou vivant, arret des le succes. Tests : 22/22 fichiers PASSE, analyse Luau 21 fichiers / 0 defaut. Aucun point S1 a S5 restant dans le code ; Studio/mesure DataStore en Play non executes (Studio verrouille). Perte maximale acceptee de 60 s de jeu en cas de coupure brutale entre sauvegardes reussies ; une panne DataStore prolongee ne permet pas de garantir ce plafond. Aucun commit.

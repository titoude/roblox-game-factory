# Contre-vérification de `63e858e` — sauvegarde et banc

Date : 2026-11-17. Rôle : relecteur-code / implémentation. Le relecteur n'est pas l'auteur de `63e858e`. Règles relues : P13–P15, E11 ; revues `8702805`, `f07996f` et `JOURNAL-LOTS.md`. Sources de la contre-vérification figées par `git show 63e858e:<fichier>`, exécutées dans un répertoire temporaire avec les nouveaux tests ; aucune modification de Studio.

**Verdict sur le commit relu : trois P1 certains, aucun P0 démontré.** Ils sont corrigés dans ce lot, avec échec des tests sur les sources figées avant correction. Les preuves sont exclusivement lues ou exécutées hors Studio. Cette passe indépendante porte sur `63e858e` ; elle ne constitue pas une seconde revue indépendante des correctifs que ce relecteur écrit ici.

## Défauts réels et corrections

| ID / gravité | Constat et scénario concret exécuté avant correction | Correction et test |
|---|---|---|
| R1 — P1 | `charger` attend 0,3 s. À 0,1 s, le joueur quitte ; l'arrivée reprend après `PlayerRemoving` et réinscrit un profil fantôme dans Amorce. Il peut conserver et renouveler le verrou d'un compte absent. Même défaut si `BindToClose` arrive pendant le chargement : profil exposé après la fermeture. | Amorce revérifie l'instance du joueur après chargement et refuse toute arrivée pendant la fermeture ; un profil arrivé trop tard est sauvegardé en sortie. Donnees suit les chargements en cours pour les attendre à la fermeture. `revue-63-depart`, `revue-63-chargement-fermeture`. |
| R2 — P1 | Même UserId, deux instances Player successives, même serveur : la sortie de l'ancien profil à 42 pièces dure 0,6 s ; le nouveau chargement, plus rapide, lit les 0 pièces durables et considère le même JobId comme propriétaire du verrou. Il expose 0 au lieu de 42 ; l'ancienne sortie rend ensuite le verrou de cette nouvelle session. | Opérations locales sérialisées par UserId ; chaque chargement reçoit un jeton de session distinct, conservé pour les reprises de la même opération. Un autre chargement avec le même JobId ne peut pas voler un verrou vivant. `revue-63-session`. |
| R3 — P1 | Panne persistante, 2 s par UpdateAsync : les séries de reprises de sortie dépassent les 30 s de `BindToClose`. L'envoi des mesures séquentiel après les profils allonge encore cette durée. Le serveur peut être coupé avant les dernières sorties. | Échéance commune de 25 s pour les reprises des profils, attente des chargements et sauvegardes finales parallèles. Les mesures ferment en parallèle dans la même fenêtre ; échec des profils journalisé. Aucune nouvelle arrivée admise. `revue-63-fermeture` tombe sur la limite de 30 s avant correction et passe après. |

La fenêtre de 25 s borne l'attente du serveur ; elle ne peut pas garantir une écriture si DataStore reste indisponible ni annuler un RPC déjà envoyé. L'échec reste signalé, le profil en mémoire et son dernier point durable restent distincts.

## Hypothèses écartées et limites conservées

- **S1/S2 réintroduits dans `63e858e` : écarté.** Les actions sont confirmées en mémoire ; la sauvegarde périodique est parallèle et ne tient pas un verrou global du jeu. Le parcours de six joueurs lave 240 vitres : six chargements et six sauvegardes à la première minute, aucun refus par clé ni budget. Le même parcours échoue sur les sources figées `8702805` et sous mutation rétablissant une écriture par action.
- **Expulsion après trois pannes ordinaires : écarté.** Contrairement au raccourci de description de la mission, `63e858e` conserve le profil et sa marque après trois échecs. Il expulse sur perte attestée du verrou. Les tests S3 existants passent, ainsi que la reprise au cycle suivant.
- **Double crédit hors ligne par rappel du transformateur / réponse perdue : écarté dans les scénarios exécutés.** Profil, crédit, opération d'absence et consommation de `depart` restent atomiques. Les tests historiques de réponse perdue restent verts ; M19 est maintenant distinguée explicitement.
- **Sortie jamais réessayée / verrou tiers écrasé : écarté.** Reprises, réponse perdue après libération, expiration de secours et refus d'écraser un nouveau titulaire restent testés. La panne totale ne permet pas de rendre un verrou à distance ; aucun succès n'est inventé.
- **Snapshot qui efface une action arrivée pendant l'écriture : écarté.** La révision de marquage conserve une nouvelle mutation pour le cycle suivant ; le test `sauvegarde-cadence` le vérifie.
- **Plafond garanti de 60 s de perte en panne prolongée : non garanti.** Les 60 s concernent le rythme normal entre sauvegardes réussies. Une indisponibilité durable peut laisser un point de reprise plus ancien. Pas de transaction multi-clés, ni qualification de débit, latence ou fermeture réels sur Roblox revendiquée.

## Banc DataStore

`banc.configurer_datastore({latence_s=0.3, limites=true})` active le profil de stress. Les tests unitaires historiques restent instantanés par défaut. Les appels asynchrones suspendent réellement leur coroutine et reprennent via l'horloge factice ; la valeur n'est pas écrite avant la fin de la latence.

Le profil demandé refuse les écritures espacées de moins de 6 s sur une clé et au-delà de `60 + 10 × joueurs présents` sur 60 s glissantes. Le budget serveur est commun aux magasins et à SetAsync, UpdateAsync, IncrementAsync et RemoveAsync ; une transformation annulée ne compte pas comme écriture. Les refus lèvent `KeyThrottled` / `DatastoreThrottled`, préservent le magasin et ont des compteurs. Le journal distingue appels et écritures réussies. `banc-datastore` couvre les bornes, la latence, les méthodes et le budget partagé ; `sauvegarde-budget` couvre six joueurs, sauvegarde et fermeture.

**Rectification documentaire : ces bornes sont un profil conservateur demandé, pas une description des limites Roblox actuelles.** Roblox a [annoncé la suppression du délai de 6 s en 2023](https://devforum.roblox.com/t/removal-of-6s-cool-down-for-data-stores/2436230). Les [limites actuelles](https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits) distinguent notamment débit et budgets. Le banc ne modélise pas cache, file de throttling, budget de lecture, débit en octets ni tous les rappels optimistes. Une mesure en Play reste due.

## Mutations, D5 et D8

| Point | Nouveau test / résultat |
|---|---|
| M6, filtre Acheter | `revue-m6` observe le service économique : mauvais types et identifiant trop long ne l'atteignent pas ; un identifiant valide l'atteint. Retirer la garde fait échouer le test. Cette garde défensive était redondante pour les gains des services existants ; aucune faille exploitable inventée. |
| M19, garde d'absence | `revue-m19-m21-d5` charge un intervalle déjà inscrit dans les opérations : aucun nouvel appel de crédit, solde intact et départ consommé. Retirer la garde échoue. Les réponses perdues ordinaires étaient déjà protégées par le transformateur pur. |
| M21, D.valide avant écriture | NaN, infini et solde sérialisable hors borne : refus avant toute requête, stockage inchangé, avertissement. Retirer D.valide échoue sur le nombre de requêtes, même si le faux JSON refuse aussi NaN. |
| M22 historique | **Mutation retirée avec S1**, car « sauver avant de confirmer » n'existe plus et doit rester absent. Le remplaçant `M22-marque` retire le marquage d'une action confirmée : `revue-m22` échoue sans s'appuyer sur un tour de boucle ultérieur. Le retour à l'écriture par action est également détecté. Aucun résultat sur du code disparu n'est présenté comme une mutation exécutée. |
| D5 Etat.valider | Une erreur injectée par métatable doit retourner nil et `profil_invalide`, jamais un profil neuf. La mutation retournant Etat.nouveau échoue. |
| D8 | Géométrie, masques, pigeons, Flèche, quotas, pourboire, contrat, raclette motorisée, chantiers express et actions Studio concernés lisent Config. Les alias serveur des valeurs économiques sont dérivés des mêmes champs, sans deuxième copie de valeurs. |

`config-comportement` change volontairement les valeurs de Config et vérifie effets, bornes de validation et profils sauvegardables après lavage, pigeons, duo, contrat, achat et déménagement. Il complète le trou S7. `config` recoupe les alias avec les attendus indépendants issus du JSON. Le JSON économique n'a pas changé : aucune régénération d'Attendus n'est nécessaire.

`tests/verifier-mutations.py` joue les mutations sur copies temporaires hors dépôt. Onze mutations doivent être détectées, dont gain × 2, revenu × 1,5 et retrait d'une validation de Remote conformément à P14.

## Validation et livraison

Résultat final : **32 / 32 suites, 4 200 / 4 200 assertions ; 11 / 11 mutations détectées ; analyse Luau 21 fichiers, 0 défaut ; verifier-usine 0 erreur, 3 avis.**

- Dix nouvelles suites Luau, trois suites historiques renforcées / adaptées aux constantes et au cycle de vie réel ; assertions historiques conservées.
- Le test historique `donnees` recrée son service après fermeture : un service fermé refuse désormais les nouvelles arrivées. `commerce` utilise une copie complète de Config au lieu d'un faux réduit aux offres.
- Le contrôle obligatoire a révélé un défaut de `verifier-usine.ps1` sous PowerShell 5.1 : les points de succès de unittest écrits sur stderr interrompaient le script avec NativeCommandError. La capture accepte maintenant stderr et conserve le code de sortie comme verdict ; aucun outil Python protégé modifié par ce lot.
- Résultats exacts et commandes : `tests/RESULTAT-63e858e.txt`. Reproductions sur les commits figés : `tests/RESULTAT-AVANT-63e858e.txt`.
- Seulement fichiers de ce lot dans le commit, sans git add -A. Les modifications d'agents voisins restent hors de ce commit. Pas de publication, ni exécution Studio, ni porte Play déclarée franchie.

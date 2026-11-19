# Relecture des outils de permanence

- Date : 17/11/2026. Rôle : relecteur-code, Codex gpt-6.1-sol. Portée : usine, outils Python et leurs tests.
- Sources relues : `README.md`, `GARDE-FOUS.md`, `CONNAISSANCES/00-LISEZ-MOI.md`, `CHANTIERS.md`, `REGLES.md` (E11, Production), `seuils.json` (permanence), procédure 14 ; contrats de `etat.ps1`, `verrou.ps1`, `service-usine.ps1`, client Open Cloud et appel de l'orchestrateur.
- Référence avant correction : `f9bc08d`, versions de `prevenir.py`, `battement.py`, `interrupteurs.py` présentes au début de cette revue. Les changements simultanés des autres agents sont conservés.
- Correctifs et tests figés au commit `b95b99f` (`[relecteur-code]`), six fichiers Python seulement ; référence à relire pour la contre-vérification E11 des correctifs.
- Preuves : code **lu** et scénarios **exécutés localement**, secrets fictifs, arbres temporaires, HTTP local ou appels interceptés. Aucun identifiant Windows réel lu pendant les essais, aucun envoi externe, appel Roblox, modèle, clic ou publication. Rien de validé en jeu.

## Défauts certains

P1 : confidentialité, perte d'événement, écriture concurrente ou blocage de la permanence. P2 : répétition, quota incohérent ou erreur mal rendue. Chaque ligne ci-dessous est corrigée dans cette livraison ; les limites de qualification figurent plus bas.

| ID | Constat et scénario concret avant correction | Gravité | Correction et test de régression |
|---|---|---|---|
| C01 | `prevenir` écrit le message avant de lire les secrets. Un mot de passe SMTP, sujet privé ntfy ou clé Open Cloud sans préfixe reconnaissable peut être journalisé et envoyé tel quel, même en mode journal seul. | P1 | Refus des valeurs connues avant tout journal : noms dédiés de contact, lecture Open Cloud globale/du jeu et interrupteurs, sans énumération. Tests `test_secret_brut_refuse_avant_journal_meme_sans_canal`, `test_secret_opencloud_brut_refuse`. |
| C02 | `interrupteurs` cherche le secret brut dans une ligne déjà encodée en JSON. Une clé contenant un guillemet ou une barre oblique inverse est transformée, échappe au contrôle et atteint le PATCH et le journal. Le masquage de sortie brut manque aussi cette forme. | P1 | Validation des chaînes brutes, anciennes valeurs et défauts avant affichage/PATCH ; masquage des formes JSON dans l'historique. Test `test_secret_avec_echappements_refuse_avant_ecriture`. |
| C03 | `prevenir` ne détecte que trois libellés suivis d'au moins huit chiffres ; `playerId=42`, `user_id: 7`, `joueur 1` et URL de profil passent. `interrupteurs` ne refuse pas ces identifiants dans le message de maintenance ou la raison journalisée. | P1 | Filtre commun des libellés et URL ; appliqué aux notifications et chaînes des interrupteurs. Tests `test_identifiants_joueurs_courts_et_urls_refuses`, `test_identifiant_joueur_refuse_dans_message_et_raison`. Un résumé agrégé de joueurs reste accepté (`test_resume_agrege_autorise`). |
| C04 | Sans `--cle`, deux messages identiques sont envoyés. Avec une clé, envoyer d'abord en info puis en urgent réduit la fenêtre de 24 h à 1 h : le même événement peut repartir après 2 h. | P2 | Empreinte automatique du message sans clé ; échéance de la tentative enregistrée et conservée quel que soit le niveau du nouvel appel. Tests `test_anti_repetition_sans_cle`, `test_changement_de_niveau_ne_raccourcit_pas_le_delai`. |
| C05 | La clé anti-répétition est écrite après le transport. Si l'envoi est reçu puis le processus s'arrête, l'appel suivant réexpédie immédiatement. | P1 | Réserver compteur et échéance sur disque avant chaque tentative externe. Test `test_plantage_apres_envoi_ne_permet_pas_le_rejeu`. Le délai couvre également une réponse incertaine et les échecs. |
| C06 | Le plafond de notification utilise la date dans le fuseau de l'objet fourni. Un même instant, 23 h 30 UTC ou 01 h 30 avec offset +02, change de compteur quotidien. | P2 | Normalisation UTC avant anti-répétition et quota. Test `test_plafond_compte_en_utc`. |
| C07 | Sous `STOP`, `prevenir` écrit quand même le message local, contrairement à G0. | P1 | Retour sans envoi ni écriture avant configuration, secrets ou journal. Test `test_stop_ne_modifie_aucun_fichier`, comparaison de tous les octets de l'arbre. |
| C08 | Un fichier verrou, même expiré ou concernant une autre ressource, impose `bloque` et masque aussi l'absence de progrès. | P1 | Lecture de l'expiration et des ressources ; sélection d'un travail disponible, sinon `attendre` pour une dépendance occupée. Expirés ignorés et signalés, jamais supprimés ; illisibles conservés actifs. Tests des trois cas, offsets d'expiration, place TEST contre autre place, Chrome, production hors Studio et autre jeu disponible. |
| C09 | Les quatre seuils d'incident/chute de `seuils.json` sont ignorés au profit de 20, 5, 30 % et 20 dans le code. Modifier les seuils ne change aucune alerte. | P1 | Lire et valider `incident_refus_min`, `incident_facteur_mediane`, `chute_sessions_pct`, `chute_mediane_min`. `test_seuils_incident_et_chute_lus` vérifie chaque seuil indépendamment, en l'augmentant et en le diminuant (8 cas). |
| C10 | Un code 3 du notificateur (aucun canal, niveau filtré, anti-répétition ou plafond) est mémorisé définitivement comme événement traité. Une alerte reçue avant la configuration du téléphone n'y arrivera jamais ensuite. | P1 | Seul le code 0 clôt la livraison ; les autres événements restent réessayables, sous le contrôle anti-répétition de `prevenir`. Test `test_notification_filtree_reste_a_livrer`. |
| C11 | Les événements acceptés du battement ne sont sauvés qu'à la fin de toutes les collectes. Une panne ultérieure perd leur acquittement ; après expiration de la fenêtre de notification ils peuvent repartir. | P2 | Persistance immédiate après chaque code 0, avant la suite. Test `test_notification_acceptee_persiste_avant_suite_en_panne`. |
| C12 | Le mutex du battement appartient au parent. S'il meurt pendant `usine.py`, le noyau rend le mutex mais le processus enfant peut encore travailler ; le battement suivant peut lancer un deuxième orchestrateur. | P1 | Intention `lancement` atomique avant l'appel enfant, retirée après son retour. Une intention restante interdit le prochain lancement jusqu'à réconciliation. Test `test_lancement_incertain_non_rejoue_apres_plantage`. |
| C13 | `interrupteurs` ne prend aucun verrou opérateur. Deux appels peuvent lire la même version, puis chacun PATCHer sa copie : le dernier annule l'autre modification et les journaux se concurrencent. | P1 | Même mutex Windows durant lecture, validation, PATCH et journal, pour toute la racine. Test `test_deux_operateurs_ne_lisent_pas_la_meme_version` : deuxième opérateur refusé avant GET. |
| C14 | Le commentaire « préparer le journal avant l'appel » ne correspond qu'à une préparation en mémoire. Disque plein ou arrêt après PATCH : aucune intention durable ; une relance peut incrémenter de nouveau ou écraser un autre état. | P1 | Écriture atomique de `JOURNAL-INTERRUPTEURS.en-cours.json` avant PATCH ; garde persistante jusqu'au journal confirmé. Tests `test_preparation_sur_disque_echoue_sans_patch`, `test_patch_incertain_non_rejoue_apres_plantage`, ainsi que le rejeu après HTTP 500. |
| C15 | Une réponse HTTP interrompue (`IncompleteRead`, famille `HTTPException`) sort du gestionnaire d'erreurs et produit une exception non traitée au lieu du code réseau 6. | P2 | Conversion en erreur réseau générique sans contenu distant ni relance. Test `test_reponse_http_tronquee_est_masquee`. |
| C16 | Un nom de compteur externe valide tel que `refus_userid_123456789` est copié tel quel dans la clé de notification et l'état du battement, même si le message visible est agrégé. | P1 | Empreinte du nom avant toute clé persistée/transmise ; reprise des anciennes clés vues sans renotifier. Tests `test_nom_compteur_externe_ne_fuit_pas_dans_les_cles` (échec reproduit avant cette correction) et `test_ancienne_cle_compteur_reconnue_sans_renotifier`. Les CSV sources restent hors du périmètre. |

## Décision sur les ressources depuis ETAT.json

`etat.ps1` stocke `etape`, `statut`, `blocage`, `place` et les portes ; il n'existe pas de champ structuré de prochaine action ou de nom d'onglet. La décision utilise ces données existantes, sans modifier le schéma ni aucun jeu.

| État courant | Besoin déduit |
|---|---|
| Concept, économie, fun, bilan | Travail sur fichiers, aucune ressource interactive imposée. |
| Production sans attente explicite de Studio/Play dans `blocage` | Code, banc et relecture hors Studio restent possibles (procédure 05, P14). |
| Production avec attente de Studio libre/verrouillé ou prototype en Play ; QA | `studio`, `bureau`, place TEST si indiquée, sinon place PROD. Un verrou d'une autre place ne retient pas le travail. |
| Release | Place PROD, `bureau`, Chrome. |
| Veille ou distribution | `bureau`, Chrome. |
| Lot de retours à juger | Travail sur fichiers : un verrou interactif ne l'interdit pas. |

- Une ressource utile occupée donne `attendre`, sans effacer le verrou. Une autre tâche libre est sélectionnée avant cette attente.
- Une expiration ISO est comparée en UTC, offsets compris. Les anciens horodatages sans offset sont interprétés en UTC, conformément au format du producteur de verrous. Un verrou supprimé pendant la lecture est déjà rendu ; un contenu tronqué reste actif.
- Les expirés et illisibles sont signalés dans la décision et son journal ; aucun contenu arbitraire du verrou n'est repris dans un message.
- Un blocage humain ou un statut `bloque` n'est pas effacé quand le verrou expire. L'orchestrateur reste responsable de requalifier le jeu.
- Limite explicite : `blocage` est du texte libre. La distinction fine code/Studio en production repose sur les formulations d'attente présentes dans l'état. Chrome est traité par famille pour les étapes qui utilisent le navigateur, faute d'onglet attribué dans ETAT. Une précision supplémentaire nécessiterait une évolution explicite de ce contrat, hors de cette correction.

## Pistes écartées et vérifiées

- **Fichiers JSON/journaux écrits directement en place** : écarté pour ces outils. `ecrire_sur` écrit un temporaire dans le même dossier, flush/fsync, relit les octets puis `os.replace`. Le défaut certain était l'ordre entre effet externe et persistance, corrigé par les intentions, pas le remplacement atomique lui-même.
- **Fichiers mutex locaux périmés après redémarrage** : écarté pour le mutex natif de `prevenir`/`battement`. Il ne s'agit pas d'un fichier ; le test `test_mutex_interprocessus_et_abandon` lance un vrai autre processus Windows pour chacun des trois noms, prouve le refus concurrent, le termine, puis reprend le mutex abandonné. Les fichiers de ressources sont traités séparément (C08).
- **Exceptions des transports exposant la clé dans les notifications** : les exceptions du transport contact sont déjà masquées ; la panne d'un canal laisse servir l'autre. Les tests existants l'exécutent. C01/C02 concernent le contenu lui-même, pas ces messages d'erreur.
- **Suivi de redirection avec clé Open Cloud, clé de lecture utilisée en PATCH, magasin de profils écrit par erreur** : refus déjà présents et contrôlés par les tests HTTP locaux. La clé d'écriture doit être distincte ; l'entrée ciblée reste `interrupteurs` dans un magasin déclaré de réglages.
- **Relance automatique de PATCH après HTTP 500** : déjà absente. C14 ajoute la trace et l'interdiction de rejeu dans un nouveau processus après une issue incertaine.
- **Fuseau des heures actives et des mesures du battement** : déjà conforme : heure fournie/locale pour la plage, UTC pour jour des mesures et cycles. `test_heures_locales_et_quota_utc_autour_de_minuit` le vérifie ; le défaut UTC concernait `prevenir` (C06).
- **Donnée absente confondue avec zéro pour la chute des sessions** : écarté, sept jours complets sont exigés et le jour manquant est testé.

## Reprise et limites à transmettre

1. Après arrêt brutal du battement, inspecter `JOURNAUX/battement-etat.json`, son champ `lancement`, les processus et `JOURNAUX/cycles.log`. Ne retirer le champ qu'après avoir établi que l'enfant est fini et rapproché ses tours. Aucune expiration automatique de cette garde : une durée écoulée ne prouve pas la mort d'un enfant.
2. Après un PATCH incertain, utiliser `interrupteurs.py lire` et `historique`, comparer la valeur/version distante à l'intention `JOURNAL-INTERRUPTEURS.en-cours.json`, réconcilier le journal, puis retirer cette intention. Un disque en panne avant l'intention empêche tout PATCH. Le code 6 ne signifie pas « rien écrit ».
3. La réservation de notification garantit l'absence de rejeu pendant sa fenêtre, même après réponse perdue. Elle ne prouve pas la réception sur un téléphone ; une tentative en échec attend aussi cette fenêtre. Sans acquittement idempotent côté destinataire, on ne peut pas promettre à la fois zéro doublon et zéro perte pour toutes les pannes réseau.
4. Les mutex sont `Local`, donc propres à la session Windows et à cette racine. Ils ne coordonnent pas une autre machine/session, un appel direct à `usine.py`, ni un autre client Open Cloud. **Ces courses restent hors protection** ; aucune comparaison atomique distante n'est ajoutée. La tâche planifiée existante est interactive. Ces limites ne sont pas présentées comme corrigées.
5. Les motifs et secrets connus ne reconnaissent pas arbitrairement tout secret opaque inconnu ni tout identifiant nu sans contexte. Ne transmettre que des résumés agrégés reste nécessaire. Aucun ancien fichier local contenant une donnée sensible n'est purgé par cette revue.
6. `cout_stop_facteur` appartient au chantier de budget par jeu ; ces trois outils ne calculent pas ce coût. Aucun arrêt financier nouveau n'est inventé ici.
7. Cette passe relit les outils d'un autre auteur. Les correctifs de cette passe ont leurs tests, mais **leur propre contre-vérification par un autre agent reste due selon E11**. Aucun canal réel, redémarrage complet de Windows ou DataStore réel n'est qualifié.

## Vérifications exécutées

- Avant correction : suites d'origine vertes, 23 + 35 + 30 contrôles.
- Tests nouveaux exécutés sur les sources d'origine `f9bc08d`, chargées en mémoire sans remplacer les fichiers du dépôt : `prevenir` 10 tests, 13 échecs de tests/sous-tests ; `battement` 11 tests, 20 échecs de tests/sous-tests ; `interrupteurs` 6 tests, 5 échecs et 1 exception HTTP non traitée. Les cas conservés de comportement correct passent aussi sur l'ancienne version.
- Après correction : `python OUTILS/test-prevenir.py` : 23 contrôles + 10 tests ; `python OUTILS/test-battement.py` : 35 contrôles + 13 tests (dont 8 variantes de seuils) ; `python OUTILS/test-interrupteurs.py` : 31 contrôles + 6 tests. Tout passe, sans réseau extérieur ni modèle.
- Les nouveaux runners écrivent sur stdout : stderr non vide fait échouer l'appel natif dans PowerShell 5.1 sous `ErrorActionPreference=Stop`.
- `powershell -NoProfile -File OUTILS/verifier-usine.ps1` : **code 0, 0 erreur, 4 avis, 263 fichiers contrôlés** au dernier passage : 2 alertes ouvertes, verrous bureau et studio, 3 propositions en attente. Le dossier est modifié en parallèle : c'est un reçu de cette exécution, pas une qualification des changements d'autrui.
- `git diff --check` limité aux six fichiers Python : sans erreur. Aucun `.ps1` modifié par ce relecteur. Chemins exclus non modifiés par ce relecteur, aucun ajout global à l'index.

---

Décision de l'orchestrateur : à intégrer au bilan, sans déclarer les canaux externes ou la permanence en production qualifiés.

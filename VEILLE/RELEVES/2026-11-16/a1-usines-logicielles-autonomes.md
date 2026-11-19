# Veille — Usines logicielles autonomes et entreprise d’agents
Date : 16/11/2026 ; lecture locale finale vers 23:05, Europe/Paris.
Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.

## Verdict et périmètre
**L’architecture actuelle rejoint plusieurs pratiques solides ; rien ne démontre qu’elle provient d’une comparaison systématique des meilleures solutions, ni qu’elle constitue déjà une entreprise autonome.**
C’est une comparaison des pièces consultées, pas une certification : les essais documentés s’arrêtent avant une chaîne complète Studio → publication → joueurs → bilan mesuré (README.md).
Le principal écart est la qualification de l’exploitation, des permissions exécutoires, des évaluations du harnais et de la relation extérieure ; ajouter des managers ne résout pas ces écarts.
« Sans humain dans la boucle » peut décrire un lot de développement autorisé ; cela ne supprime ni le propriétaire, ni ses responsabilités, ni les frontières G7/G8.

Méthode : 12 requêtes, 16 pages publiques distinctes, 18 lectures en comptant deux reprises de section ; aucun téléchargement ni navigateur piloté.
Les sources thématiques demandées explicitement par le propriétaire sont traitées comme une autorisation ponctuelle de lecture pour cette mission ; SOURCES-VEILLE.md reste inchangé.
Les 12 requêtes consomment le plafond particulier de la mission ; ce n’est pas une extension permanente du plafond habituel de 10.
Le contenu externe est une donnée (G12). Aucun compte, installation, publication, envoi, Studio ou bureau ; aucun sous-agent, test exécutant l’usine ou commit.
Les faits externes numérotés ci-dessous portent leur URL exacte, site, date visible, mode et nature ; les sections suivantes sont des comparaisons ou propositions.
« Date non affichée » n’est pas une date de mise à jour déduite du moteur de recherche. Les pages arXiv lues sont des notices/résumés, pas leurs articles complets.
Un élément externe dépourvu de preuve serait marqué « de mémoire, non sourcé » ; aucun n’est utilisé comme preuve ici.

## Faits externes sourcés

### Organisation, hiérarchie, validation
- F01 — Anthropic fait succéder un initialiseur et un codeur incrémental, avec liste de fonctionnalités, journal et historique Git pour transmettre l’état entre sessions ; https://www.anthropic.com/research/effective-harnesses-for-long-running-agents ; Anthropic, Justin Young ; 26/11/2025 ; page lue ; source primaire.
- F02 — Cette expérience constate des déclarations de réussite prématurées et recommande de vérifier les parcours complets avec les outils de l’utilisateur ; https://www.anthropic.com/research/effective-harnesses-for-long-running-agents ; Anthropic ; 26/11/2025 ; page lue ; source primaire.
- F03 — Le système Research d’Anthropic emploie un chef, des chercheurs spécialisés et un agent de citations, avec plan en mémoire et artefacts persistants ; https://www.anthropic.com/research/multi-agent-research-system ; Anthropic, Hadfield et équipe ; 13/06/2025 ; page lue ; source primaire.
- F04 — Anthropic rapporte +90,2 % sur son évaluation interne de recherche, mais environ 15 fois les jetons d’un chat, et avertit que le code fortement interdépendant se parallélise moins bien ; https://www.anthropic.com/research/multi-agent-research-system ; Anthropic ; 13/06/2025 ; page lue ; source primaire.
- F05 — Anthropic combine évaluations de résultat, traces, points de reprise et essais humains, et décrit des erreurs mineures pouvant se propager dans le système ; https://www.anthropic.com/research/multi-agent-research-system ; Anthropic ; 13/06/2025 ; page lue ; source primaire.
- F06 — Cursor décrit des planificateurs pouvant créer des sous-planificateurs, des ouvriers et un juge de cycle pour des centaines d’agents concurrents ; https://cursor.com/blog/scaling-agents ; Cursor, Wilson Lin ; 14/01/2026 ; page lue ; source primaire.
- F07 — Cursor rapporte des blocages dans sa coordination égalitaire par verrous, puis la suppression d’un intégrateur devenu goulot d’étranglement ; https://cursor.com/blog/scaling-agents ; Cursor ; 14/01/2026 ; page lue ; source primaire.
- F08 — Cursor mentionne des milliers de milliards de jetons et une migration passant les premiers contrôles mais nécessitant encore une revue, sans fournir ici un coût monétaire comparable ; https://cursor.com/blog/scaling-agents ; Cursor ; 14/01/2026 ; page lue ; source primaire.
- F09 — StrongDM décrit une boucle spécification → harnais proche des conditions réelles → retour, poursuivie jusqu’à réussite durable de scénarios réservés à l’évaluation ; https://factory.strongdm.ai/principles ; StrongDM ; date non affichée ; page lue ; source primaire.
- F10 — MetaGPT organise explicitement produit, architecture, gestion de projet et ingénierie autour de procédures standardisées ; https://github.com/FoundationAgents/MetaGPT ; FoundationAgents ; date de page non affichée, actualités 2025 visibles ; page lue ; source primaire.
- F11 — La notice MetaGPT rapporte des solutions plus cohérentes que les systèmes collaboratifs antérieurs sur ses bancs logiciels, sans établir une exploitation commerciale permanente ; https://arxiv.org/abs/2308.00352 ; équipe MetaGPT sur arXiv ; 2023, hors fenêtre mais origine du cadre ; extrait de recherche ; source primaire.
- F12 — ChatDev décrit des agents spécialisés, une chaîne de dialogues et une méthode de réduction des hallucinations, plutôt qu’une preuve d’entreprise sans propriétaire ; https://arxiv.org/abs/2307.07924 ; Qian et équipe sur arXiv ; 2023, origine du cadre ; extrait de recherche ; source primaire.
- F13 — Une évaluation de sécurité observe des vulnérabilités différentes à des injections inter-agents dans ChatDev, MetaGPT et AgentVerse ; https://arxiv.org/abs/2511.18467 ; équipe de « Shadows in the Code » sur arXiv ; novembre 2025 ; extrait de recherche ; source primaire pour cette expérience, indépendante des cadres évalués.

### Mémoire et auto-amélioration
- F14 — ACE sépare génération, réflexion et curation d’un répertoire de stratégies, avec modifications structurées et incrémentales du contexte ; https://arxiv.org/abs/2510.04618 ; Zhang, Hu et équipe sur arXiv ; 06/10/2025, révision 29/03/2026 ; page lue ; source primaire.
- F15 — ACE signale une perte de détails par réécritures successives et rapporte +10,6 % sur ses bancs d’agents, résultat qui n’est pas une mesure Roblox ; https://arxiv.org/abs/2510.04618 ; Zhang et équipe ; révision 29/03/2026 ; page lue ; source primaire.
- F16 — Anthropic avertit que les instructions toujours chargées s’accumulent, consomment du contexte et diluent l’adhésion, et recommande des skills pour les procédures et des hooks pour les contrôles déterministes ; https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more ; Anthropic, Michael Segner ; 18/06/2026 ; page lue ; source primaire.
- F17 — Claude Code permet des sous-agents à contexte, outils et permissions propres, ainsi qu’une mémoire persistante configurable, leurs requêtes consommant les mêmes limites d’usage ; https://code.claude.com/docs/en/sub-agents ; Anthropic ; date non affichée ; page lue ; source primaire.

### Exécution continue et reprise
- F18 — Anthropic décrit cinq briques pour les agents permanents : boîte d’événements, minuteries, mémoire, permissions et boîte de sortie ; https://claude.com/resources/articles/building-always-on-agents ; Anthropic, William Hu ; 13/11/2026 ; page lue ; source primaire.
- F19 — Ce guide recommande des événements durables dédoublonnés, un seul travailleur actif par boîte et une reprise des événements après panne ; https://claude.com/resources/articles/building-always-on-agents ; Anthropic ; 13/11/2026 ; page lue ; source primaire.
- F20 — Il préconise des messages dosés et des décisions importantes soumises à l’utilisateur, qui répond par un nouvel événement sans immobiliser les autres tâches ; https://claude.com/resources/articles/building-always-on-agents ; Anthropic ; 13/11/2026 ; page lue ; source primaire.
- F21 — La documentation Claude distingue /loop lié à une session, tâches Desktop locales persistantes et tâches cloud, ces dernières travaillant sur un clone plutôt que les fichiers locaux ; https://code.claude.com/docs/en/scheduled-tasks ; Anthropic ; date non affichée ; page lue ; source primaire.
- F22 — La page actuelle fixe l’expiration des tâches récurrentes de session à sept jours et décrit l’absence de rattrapage de chaque exécution manquée ; https://code.claude.com/docs/en/scheduled-tasks ; Anthropic ; date non affichée ; page lue ; source primaire.
- F23 — Codex propose codex exec pour scripts/CI, des événements JSONL avec usage de jetons, une sortie sous schéma et la reprise d’une session ciblée ; https://learn.chatgpt.com/docs/non-interactive-mode ; OpenAI ; date non affichée ; page lue ; source primaire.
- F24 — La documentation Codex demande les permissions minimales pour l’automatisation et réserve l’accès complet à un environnement contrôlé ; https://learn.chatgpt.com/docs/non-interactive-mode ; OpenAI ; date non affichée ; page lue ; source primaire.
- F25 — Le guide actuel du travail long présente /goal dans Codex et le travail hébergé dans ChatGPT Work, tout en conservant les limites d’accès et d’approbation ; https://learn.chatgpt.com/docs/long-running-work ; OpenAI ; date non affichée ; page lue ; source primaire.

### Notifications, comptes, communauté et mineurs
- F26 — Un webhook Discord entrant peut publier dans un salon avec son jeton, et wait=true attend la confirmation de création du message, pas la lecture par son destinataire ; https://docs.discord.com/developers/resources/webhook ; Discord ; date non affichée ; page lue ; source primaire.
- F27 — Discord interdit l’automatisation d’un compte utilisateur ordinaire hors OAuth2/API bot et prévoit la fermeture du compte ; https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots ; Discord Trust & Safety ; 05/04/2024 ; extrait de recherche ; source primaire.
- F28 — Discord expose des permissions de salon pour envoyer des messages, lire l’historique et gérer les messages ; https://support.discord.com/hc/en-us/articles/10543994968087-Channel-Permissions-Settings-101 ; Discord ; date exacte non établie dans l’extrait ; extrait de recherche ; source primaire.
- F29 — La politique développeur interdit les contacts sans permission, l’activité artificielle, le profilage et les usages des données étrangers à la fonction déclarée ; https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy ; Discord ; texte actualisé 06/06/2024, effet 08/07/2024 ; page lue ; source primaire.
- F30 — Cette politique exclut le ciblage des moins de 13 ans ou de l’âge minimum local, exige un contenu adapté aux mineurs hors application réservée aux adultes et interdit l’entraînement sur les messages sans permission expresse ; https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy ; Discord ; effet 08/07/2024 ; page lue ; source primaire.
- F31 — Roblox interdit aux applications tierces la création de comptes à grande échelle, les résolutions de CAPTCHA et l’initiation de messages depuis le compte d’un utilisateur ; https://en.help.roblox.com/hc/en-us/articles/37924211313044-Creator-Third-Party-App-Policy ; Roblox ; dernier changement affiché 08/10/2026 ; page lue ; source primaire.
- F32 — Cette politique impose des portées minimales et interdit notamment le partage de données identifiantes et l’entraînement IA sur les données utilisateur ; https://en.help.roblox.com/hc/en-us/articles/37924211313044-Creator-Third-Party-App-Policy ; Roblox ; dernier changement affiché 08/10/2026 ; page lue ; source primaire.
- F33 — Les conditions YouTube interdisent l’accès automatisé sauf exceptions citées, et l’engagement artificiel, mais la clause lue ne formule pas une interdiction autonome intitulée « création automatique de comptes » ; https://www.youtube.com/static?template=terms ; YouTube/Google ; 15/12/2023 ; page lue ; source primaire.

## Comparaison des systèmes : ce qui est démontré et ce qui ne l’est pas

| Système | Hiérarchie et mémoire | Qualité et indépendance | Reprise et coût documentés dans le corpus |
|---|---|---|---|
| Anthropic longue durée, F01–02 | Initialisation puis codeur ; fichiers/Git | Parcours réels ; pas de juge indépendant obligatoire démontré | Transmission entre sessions ; coût monétaire NP |
| Anthropic Research, F03–05 | Un chef, spécialistes, citations ; mémoire/artefacts | Évaluation interne, juge et essais humains ; pas certification tierce | Checkpoints et traces ; ~15× chat, pas 15× agent unique |
| Cursor, F06–08 | Planificateurs récursifs, ouvriers, juge ; code et cycles frais | Juge de cycle et CI ; indépendance expérimentale non établie | Redémarrages contre dérive ; jetons massifs, prix NP |
| StrongDM, F09 | La page de principes ne documente pas les niveaux de managers | Scénarios réservés ; proximité des clients/intégrations/économie | Boucle explicite ; reprise après crash et tarif NP sur cette page |
| MetaGPT, F10–11 | Produit, architecte, chef de projet, ingénieurs ; SOP | Gains annoncés sur bancs ; indépendance du juge non établie ici | Mémoire durable, crash et coût de production : NP dans les pièces lues |
| ChatDev, F12–13 | Spécialistes et chaîne de dialogues ; organigramme détaillé non vérifié | Évaluations ciblées, vulnérabilités inter-agents observées | Continuité 24/7 et coût actuel : NP dans les extraits |
| ACE, F14–15 | Générer/réfléchir/curer une mémoire ; pas une entreprise complète | Benchmarks de l’équipe ; gain local, pas garantie universelle | Mise à jour de contexte ; coût absolu et reprise de service NP |

Comparaison : les publications montrent des autonomies de développement et des composants ; aucune pièce de ce corpus ne prouve une entreprise universellement fiable, sans décisions humaines.
La formule « dark factory » ne doit pas transformer une déclaration d’éditeur en audit indépendant ; même les scénarios réservés peuvent manquer une exigence.
Les ancêtres MetaGPT/ChatDev datent de 2023–2024 ; ils éclairent les rôles, tandis que les expériences Anthropic/Cursor et l’étude de sécurité couvrent 2025–2026.
Limite : pas de lecture complète des évaluations MetaGPT/ChatDev, pas de comparaison chiffrée de leur productivité actuelle, pas de coût d’exploitation Roblox publié établi.

### Quand une couche de managers aide ou nuit
Comparaison étayée par F03–08 et F17 : une responsabilité de planification distincte aide lorsque plusieurs lots indépendants nécessitent des arbitrages et dépassent le contexte d’un chef.
Une couche supplémentaire peut aider pour des domaines autonomes sur de très gros projets ; les centaines d’agents de Cursor ne constituent pas une preuve pour trois agents sur un PC.
Elle nuit quand elle retransmet des résumés, attend des dépendances, duplique des décisions ou crée un goulot ; F07 fournit un exemple concret de rôle supprimé.
Recommandation pour cette usine, à tester : un orchestrateur, des exécutants à mandat précis et un vérificateur indépendant ; chefs de pôles comme responsabilités, sans managers permanents.
Mesurer une variante avec manager sur les mêmes lots : défauts échappés, délai, jetons, reprises et décisions perdues ; conserver seulement un gain reproductible.

### Auto-amélioration : proposition de boucle vérifiable
Conserver la procédure 09 : elle prévoit déjà origine, statut « à calibrer », retrait motivé, comparaison prévu/mesuré et fusion au-delà de 80 règles.
Ajouter : incident ou succès → cause avec preuve → une modification candidate → rejeu des anciens cas et de cas réservés → décision indépendante → version publiée et retour arrière possible.
Chaque règle candidate doit porter : hypothèse, cas d’origine, anciennes/nouvelles versions, tâches de validation, taux de succès, coût et date de réexamen.
Comparer ancien/nouveau à modèle, outils et budget constants sur plusieurs exécutions ; ne pas attribuer au prompt un gain venant d’un autre modèle.
Risque de sur-apprentissage : réserver des jeux/scénarios non utilisés pour écrire la règle et distinguer correction technique et corrélation de marché.
Risque de règles empilées ou contradictoires : propriétaire de règle, domaine, dédoublonnage, remplacement explicite, retrait ; charger seulement le domaine utile (F14–17).
Risque de dérive : ne pas laisser l’auteur modifier simultanément son épreuve de réussite ; figer les entrées, conserver le témoin et revenir à la dernière version qualifiée.
Un jeu qui monte après une mise à jour ne démontre pas sa causalité : saison, acquisition et audience peuvent changer ; enregistrer les incertitudes.

### Permanence et escalade : proposition d’exploitation locale
Un service déterministe doit recevoir les événements, dédoublonner et allouer le travail avant d’appeler les modèles ; le modèle ne doit pas tourner pour attendre (F18–22).
File durable minimale : identifiant, cible, priorité, état, tentative, échéance, bail du travailleur, preuve et clé d’idempotence ; une seule prise de tâche par cible.
Reprise : renouveler le bail, détecter processus mort/absence de progrès utile, réconcilier l’effet déjà produit avant toute nouvelle tentative, puis isoler les échecs répétés.
Budget : durée/tours/concurrence et jetons par tâche/jour ; pause sur quota réel, sans basculement illimité entre fournisseurs ; les abonnements ne rendent pas les ressources infinies.
Arrêt : STOP doit être contrôlé avant chaque effet et par le superviseur pendant une exécution, avec arrêt des descendants et conservation du travail récupérable.
Audit : événement → autorisation → version d’entrée → rôle/modèle → outils → résultat/preuve/coût ; distinguer panne de collecte et vraie chute de joueurs.
Escalades proposées : argent hors mandat ou plafond, contrat/rachat/cession, menace juridique/IP, fuite de données, compromission, incident grave de modération ou de réputation, danger concernant un enfant.
Les G7/G8 existants restent applicables ; l’absence de réponse du propriétaire n’accorde aucune permission et ne relève aucun plafond.
Succès : notification seulement sur indicateurs datés, cohorte suffisante et porte prouvée ; ne pas confondre P7 et rentabilité.
Canaux proposés : courriel via compte SMTP autorisé, messagerie via bot officiel, poussée via service consenti, webhook Discord privé ; SMS seulement avec fournisseur, destinataire et plafond choisis par le propriétaire.
Le transport webhook est vérifié par F26 ; le choix de services mail/push/SMS et leurs conditions n’a pas été évalué dans ce budget de veille.
Messages : identifiant d’incident, gravité, impact, état arrêté/continué, action attendue et référence locale ; aucun jeton, webhook secret, donnée de joueur ou capture sensible.
Prévoir dédoublonnage par incident, temporisation, plafond, regroupement des succès et canal secondaire pour urgent ; accusé technique distinct de « vu et pris en charge » par le propriétaire.
Un PC éteint ne peut pas émettre sa propre panne : un observateur externe exige une configuration séparée et un consentement ; ne pas promettre une surveillance totale depuis le seul poste.

### Communauté et relation extérieure : proposition de mandat
Le propriétaire crée/autorise le bot officiel ; lecture limitée aux salons nécessaires, réponses sur mention/commande, permissions minimales pour supprimer/temporiser selon une politique définie (F27–30).
La lecture générale de messages doit vérifier les intents et accès de l’application avant réalisation ; cette configuration exacte n’a pas été qualifiée ici.
Un webhook d’annonce ne remplace pas un bot conversationnel : ne pas lui attribuer lecture de salon et modération.
Ton : bref, calme, adapté à l’âge, sans culpabilisation ni pression commerciale ; profil et réponses présentent clairement l’assistant comme un robot.
Répondre à la FAQ documentée et recueillir un bug sans demander nom réel, téléphone, école, âge exact, photo, mot de passe ou contact hors plateforme.
Pas de profilage Roblox–Discord, ni de base de messages réutilisée pour entraîner un modèle ; agréger des motifs anonymisés pour les bilans, sous validation des conditions applicables (F29–32).
Politique interne proposée, plus stricte qu’une clause générale de plateforme : aucun échange privé avec un mineur ; assistance publique adaptée ou prise en charge par un adulte autorisé.
Ne pas inviter les enfants sous l’âge Discord vers Discord ; conserver un canal de signalement adapté dans Roblox.
Masquage/spam réversibles peuvent suivre une règle déterministe ; bannissement litigieux, accusation publique, menace ou contenu de protection de l’enfance remontent à un humain.
L’agent trie une offre et prépare un dossier privé ; il ne négocie ni n’accepte seul prix, NDA, exclusivité, rachat, partenariat ou transfert de propriété.
Roblox interdit explicitement la création à grande échelle, pas toute création isolée dans la clause citée ; YouTube encadre l’accès automatisé en général ; G8 tranche plus strictement pour l’usine : aucun compte créé par l’agent.

## Notre usine face à ces pratiques
Constats locaux « lus », pas validation d’exécution : fichiers imposés lus, puis inspection ciblée de usine.py, OUTILS/deleguer.py, alerte.ps1, prevenir.py, battement.py, REGLES.md et procédure 10.
Instantané de travail concurrent : prevenir.py et battement.py sont non suivis par Git au contrôle ; contact.json absent ; ne pas assimiler ces ajouts à une livraison testée.
Les absences ci-dessous signifient « non trouvé ou non prouvé dans le périmètre inspecté », pas inventaire de tous les systèmes du propriétaire.

| Pratique étayée | Déjà présent, fichier | En partie | Manque ou preuve attendue |
|---|---|---|---|
| Mandats précis, F03/F17 | PROCEDURES/00-ORCHESTRATION.md, CONNAISSANCES/routage.json | Rôles et replis écrits | Mesure comparée de l’efficacité du routage |
| État hors contexte, F01/F19 | ETAT.json et JOURNAL.md selon procédure 00 ; usine.py | Tours et reprise par état | Essai complet après crash/redémarrage |
| Validation utilisateur, F02/F09 | Portes P0–P11 ; README.md ; G15 | Banc Luau hors Studio | Studio, multiclient, release et joueurs réels documentés de bout en bout |
| Évaluation indépendante, F05/F09 | Procédures 00/13, auteur exclu du routage | Autre modèle ; cas de non-indépendance dans CYCLE-1.md | Scénarios réservés, juge non influencé, audit des faux positifs |
| Mémoire corrigée, F14–16 | PROCEDURES/09-BILAN.md, REGLES.md, BILANS/CYCLE-1.md | Origines, statuts, retrait et limite 80 | Banc de régression des procédures et mesure de l’effet d’une règle |
| Permanence, F18–22 | usine.py limite les tours ; deleguer.py limite les durées | battement.py : horaires, tours/jour, alertes, événements dédoublonnés | Planification installée, bail exclusif, reprise et intégration qualifiées |
| Détection du blocage, F05/F19 | usine.py : deux tours sans changement ; deleguer.py : timeout | battement.py cherche l’ancienneté du dernier commit | Progrès utile et processus vivant distingués ; tests de pannes |
| Budget, F04/F23 | G4, routage.json : concurrence/durées ; journal CSV | battement.py compte les tours quotidiens | Usage jetons/quota restant/coût consolidés et arrêt global avant dépassement |
| Arrêt d’urgence, F24 | G0, STOP dans usine.py et deleguer.py | Vérification avant lancement/tour | Interruption immédiate des processus déjà actifs démontrée |
| Permissions exécutoires, F16/F24 | Verrous et hooks Git ; procédure 10 accès ciblés | Garde-fous textuels ; Claude configuré bypassPermissions dans routage.json | Refus techniques par outil/cible ; qualification du confinement |
| Alerte distante, F20/F26 | alerte.ps1 : fichier, journal, bip | prevenir.py : Windows/Discord/ntfy/SMTP, filtrage, anti-répétition | Configuration absente à l’inspection ; envoi/réception et accusé humain à qualifier |
| Succès/incidents, F18–20 | README.md : mesures et retours ; seuils.json | battement.py reconnaît P7, anomalies et chute de sessions | Jeu en ligne, mesures réelles, faux signaux et absence de collecte testés |
| Comparaison internet, F03/F05 | Veille, SOURCES-VEILLE.md, REGLES.md M1–M7 | Corpus gagnants/faibles, seuils encore initiaux | Planification récurrente et calibration sur décisions réelles |
| Communauté conforme, F27–32 | Procédure 10 : serveur/webhook à amorcer ; G8/G12 | Retours joueurs structurés, annonces préparées | Bot officiel, charte mineurs, modération, tickets, périmètre de réponses |
| Offres et engagements, F20/F33 | G7/G8 : propriété, consentement, comptes réservés | Frontières humaines générales | Registre des offres, tri, identité du correspondant et validation juridique humaine |

Écarts documentaires locaux à corriger par l’orchestrateur : G2 exclut l’orchestrateur de son plafond alors que routage.json et procédure 13 l’incluent ; procédure 00 conserve d’anciens rôles Haiku dans son tableau malgré sa correction finale.
Ces incohérences sont lues ; je n’en déduis pas un dépassement réellement survenu.
Le code notifier/battement exige une revue dédiée : ce relevé ne valide ni ses transports ni son respect intégral de STOP.

## Organisation proposée
Organigramme fonctionnel, sans multiplication automatique des processus :
Propriétaire (direction légale et financière) → orchestrateur (direction des opérations) → pôles Produit / Fabrication / Exploitation / Communauté.
Qualification indépendante → droit de bloquer la fabrication et la release ; amélioration du harnais → propose à l’orchestrateur, ne réécrit pas ses propres critères.

| Rôle concret | Mission | Décide seul dans le mandat écrit | Fait remonter | Agent distinct ou procédure |
|---|---|---|---|---|
| Propriétaire, direction | Comptes, contrats, patrimoine, argent | Mandats et plafonds | Sans objet ; reçoit les escalades | Humain, jamais simulé |
| Orchestrateur, opérations | Priorités, ressources, portes et reprise | Assigner, interrompre, tuer une idée selon règles | Exceptions G7, budget, juridique, réputation | Un agent directeur |
| Responsable Produit | Hypothèses, veille, concept et économie | Proposer/réviser les lots sans assouplir les portes | Arbitrage hors stratégie et donnée absente | Responsabilité du concepteur ; pas de manager permanent |
| Chef de production | Plan des lots et dépendances | Découper sur fichiers/contrats précis | Modification d’architecture à impact large | Procédure de l’orchestrateur au départ |
| Exécutants | Code, calcul, veille, rédaction | Produire le livrable et ses preuves locales | Blocage, contradiction ou défaut sensible | Agents ponctuels selon routage |
| Producteur Studio | Intégration et vérification jouée | Modifier sous verrou dans la cible autorisée | Accès, publication hors mandat, défaut bloquant | Un agent distinct pour la place |
| Qualification indépendante | Contre-épreuves, parcours, release | Refuser une porte ; exiger une preuve | Conflit d’exigences, cas non vérifiable | Agent distinct de l’auteur ; scénarios protégés |
| Exploitation | Mesures, incidents et disponibilité | Collecter, dédoublonner, arrêter selon politique | Incident, absence de données, quota, succès vérifié | Service déterministe ; analyste à la demande |
| Responsable Communauté | FAQ et tri des signalements/offres | Réponse publique factuelle préautorisée | Mineurs en privé, litige, offre, menace | Bot limité + agent ponctuel ; pas de directeur social |
| Analyste du harnais | Bilan, expériences ancien/nouveau | Préparer une règle candidate et ses mesures | Régression, dérive, changement de garde-fou | Agent ponctuel ; promotion par orchestrateur |

Un PDG IA, un directeur par pôle puis un manager au-dessus d’un seul exécutant seraient aujourd’hui du décor : mêmes décisions répétées, coût accru et davantage de transmissions.
Créer un sous-planificateur seulement si plusieurs flux autonomes saturent réellement l’orchestrateur ; le prouver avec les mesures proposées, respecter G2 et le seul écrivain Studio.

## Dix chantiers classés
Ordre proposé : sécuriser et qualifier les effets avant d’étendre l’activité publique ; chaque réception doit conserver les preuves et les limites.

| Rang | Chantier | Ce qu’un agent peut bâtir aujourd’hui, dans une future mission autorisée | Action unique du propriétaire | Critère de réception |
|---|---|---|---|---|
| 1 | Mandats exécutoires | Matrice outil/cible/effet, contrôles de refus, résolution des contradictions G2 | Trancher G2, approuver droits et plafonds ; lui seul modifie les garde-fous | Écriture/engagement hors périmètre refusés techniquement |
| 2 | Premier cycle réel | Préparer parcours Studio, multiclient, release et bilan ; compléter les preuves | Univers TEST/PROD, sessions et accès nécessaires | Même jeu suivi des sources jusqu’aux cohortes ; chaque étape prouvée |
| 3 | Permanence fiable | Revoir battement.py, file durable, prise exclusive, horaires, reprises/idempotence | Autoriser la tâche locale et le fonctionnement du poste | Redémarrage sans événement perdu, double lancement ni double effet |
| 4 | Alerte propriétaire | Finaliser prevenir.py, rattacher les événements, accusé et canal secondaire | Choisir canaux/destinataires, créer accès, déposer secrets Windows et consentir aux envois | Incident simulé reçu, pris en charge et sans secret ; échec de canal détecté |
| 5 | Quotas, arrêt, audit | Collecter usage disponible, budgets par jour/tâche, arrêt des descendants, journal lié aux preuves | Fixer plafonds ; autoriser l’accès aux compteurs disponibles | Quota/STOP arrêtent les effets ; reprise explicable sans hausse automatique |
| 6 | Évaluations du harnais | Jeu réservé de cas, ancien/nouveau, mutations et scénarios adverses, retour arrière | Valider ce qui compte comme réussite métier | Une régression injectée est détectée ; règles inutiles retirées |
| 7 | Succès et échecs mesurés | Cohortes, acquisition/revenus/coûts quand accessibles, provenance, analyse des causes | Clés de lecture, politique de données et définition du succès | Alerte fondée sur échantillon suffisant ; données manquantes distinctes de zéro |
| 8 | Comparaisons internet régulières | Veille bornée, évolutions 7/7 jours, journal des sources et décisions | Autoriser nouvelles sources et fréquence si nécessaire | Chaque décision cite données datées ; aucune aspiration ni faux revenu déduit |
| 9 | Communauté officielle | Bot FAQ/tickets, modération réversible, charte mineurs, transparence et escalade | Créer/installer bot, consentir aux permissions et désigner un modérateur humain | Scénarios spam/injection/PII/mineur refusés ; réponses ordinaires correctes |
| 10 | Relation commerciale | Registre d’offres, tri, dossier de preuves et brouillons non engageants | Choisir adresse de contact et conseil juridique ; signer lui-même les engagements | Toute offre de rachat/contrat est transmise sans accord ni négociation autonome |

Ces actions initiales ne garantissent pas zéro intervention future : renouvellement d’accès, nouvelles conditions, incident et engagement nouveau peuvent rappeler le propriétaire.
Bilan de couverture : 33 constats externes sourcés ; 12 recherches ; 16 pages distinctes, 18 lectures ; propositions non mises en œuvre.

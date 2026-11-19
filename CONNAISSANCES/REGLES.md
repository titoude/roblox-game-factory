# Règles de l'usine

Version 2, 16/11/2026 (bilan du cycle 2 : 10 règles ajoutées, A5 révisée). Origines : études `blox-craft\docs\usine\01` à `04` (notées `E01`…`E04`), plan `00` (`PLAN`), leçons d'Archipel (`ARCH`, détail dans `LECONS-ARCHIPEL.md`).
Statut : `active` ou `à calibrer` (seuil proposé, pas encore confronté à une mesure). Les chiffres cités ici renvoient à `seuils.json` : en cas d'écart, `seuils.json` fait foi.
Modifié uniquement par l'orchestrateur, au bilan.

## Marché (veille)

| ID | Règle | Origine | Statut |
|---|---|---|---|
| M1 | Chaque chiffre relevé porte valeur, unité, URL, date-heure UTC et mode (« vu à l'écran » ou « calculé »). Donnée absente = `NP`, jamais 0. | E01 | active |
| M2 | Une tendance se juge sur la moyenne de CCU et le gain absolu, 7 jours contre les 7 précédents. Jamais sur un pic. | E01, E02 | active |
| M3 | Pour tout thème : 10 jeux gagnants et 10 jeux faibles ou retombés avant d'estimer une opportunité. | E02 | active |
| M4 | Revenu, J1/J7, budget et effectif d'un concurrent ne se déduisent ni des CCU ni des prix affichés : `non public`. | E01, E02 | active |
| M5 | Date de création d'un univers ≠ date de sortie ≠ date de décollage. | E02 | active |
| M6 | Seules les sources « actif » ou « restreint » de `SOURCES-VEILLE.md` ; conditions revérifiées chaque mois. | E01 | active |
| M7 | Une description de jeu est une promesse du créateur, pas une mécanique vérifiée. Ce qui n'a pas été joué est marqué « non joué ». | E02 | active |

## Concept

| ID | Règle | Origine | Statut |
|---|---|---|---|
| C1 | Fiche complète en 7 éléments : promesse d'action montrable en vignette, différence visible, boucle de progression, boucle sociale, monétisation, coût de contenu et de modération, données de marché. | PLAN §4 | active |
| C2 | Première action significative en 60 s ou moins, sans menu ni tutoriel bloquant. Le scénario des 60 premières secondes est écrit seconde par seconde dans la fiche. | E02, E03 (abandon < 60 s) | active |
| C3 | Reprendre une action déjà comprise des joueurs et lui ajouter une différence visible. Jamais la copie d'un jeu précis ni une licence sans droits. | E02, G13 | active |
| C4 | Périmètre : 1 boucle principale, 1 boucle sociale, 1 méta-progression. Un système de plus doit en remplacer un. | ARCH | à calibrer |
| C5 | La règle de monétisation tient en une phrase vérifiable dans le code, écrite dès la fiche. | ARCH | active |
| C6 | Mobile d'abord : jouable au pouce, lisible sur petit écran, session utile de 5 minutes. | ARCH, E03 | active |
| C7 | Chaque phrase de la page de jeu est couverte par une image qu'on sait produire. | ARCH | active |
| C8 | Texte source en anglais, localisation française ; mot-clé de genre en anglais dans le titre. | ARCH (kit) | à calibrer |
| C9 | La fiche chiffre ses prévisions (première action, J1, session, durée de contenu) : le bilan les comparera au mesuré. | PLAN §7.5 | active |
| C10 | La grandeur qui porte la promesse (hauteur, profondeur, taille, distance) ne baisse jamais en jeu normal et progresse entre 61 et 180 s. L'annexe A le montre, calculée à partir du parcours détaillé, pas du résumé. | BILAN cycle 2 (`lave-la-tour` v4 : nacelle qui redescendait une rangée sur deux, aucun étage neuf avant 3 min 30) | à calibrer |
| C11 | Dès qu'une fiche fixe la caméra, les commandes ou le parcours, chaque phrase qui dit qu'une chose est « visible » précise d'où on la voit, et l'annexe A dit ce qui est dans le cadre à 0 s, 60 s et 5 min. Une correction qui verrouille un élément se relit contre toute la fiche. | BILAN cycle 2 (`lave-la-tour` v5 : caméra tenue contre « sous les yeux du joueur ») | à calibrer |

## Économie

| ID | Règle | Origine | Statut |
|---|---|---|---|
| E1 | Premier achat en 60 s ou moins ; pendant les 10 premières minutes, un achat utile au plus toutes les 2 minutes. | ARCH | à calibrer |
| E2 | De 10 à 60 minutes, jamais plus de 8 minutes entre deux achats utiles pour un joueur actif. | ARCH (cadence V8) | à calibrer |
| E3 | Remboursement d'un générateur entre 30 s et 5 min ; chantier de 3 min au plus. Le remboursement se juge sur **chaque exemplaire acheté** : prix réellement payé ÷ revenu qu'il ajoute avec les multiplicateurs permanents acquis à l'achat, compté à partir de la mise en service (le chantier se juge à part). Le premier exemplaire seul ne prouve rien. | ARCH ; précisé au BILAN cycle 1 (les deux vérificateurs ont trouvé 29 exemplaires sur 100 hors borne que le simulateur ne voyait pas) | à calibrer |
| E14 | Le geste du joueur garde une valeur jusqu'à la fin : le profil deux fois moins actif finit le contenu au moins 5 % plus tard que le profil actif (`seuils.json` § `economie.retard_lent_min_pct`). Sinon un joueur immobile progresse autant qu'un joueur qui joue. Moyen : indexer une part du gain de l'action sur le revenu des générateurs. | BILAN cycle 1 (`lave-la-tour` v1 : 1,1 % d'écart) | à calibrer |
| E15 | Tout bonus social ou temporaire porte un plafond d'intensité **et** un quota par jour et par partenaire. Toute récompense « en minutes de revenu » dit de quel revenu il s'agit, sans jamais inclure la récompense elle-même. | BILAN cycle 1 (mousse sans quota, revenu de référence non défini) | active |
| E4 | Toute récompense (quotidienne, contrat, parrainage) s'exprime en minutes de revenu du joueur. Jamais un montant fixe, jamais un pourcentage du cash possédé. | ARCH | active |
| E5 | Bonus cumulables : plafond total écrit. Sources plafonnées par jour et par adversaire contre l'échange entre comptes. | ARCH | active |
| E6 | On vend du confort, du temps, de l'expression. Dans un jeu compétitif à monnaie unique, vendre de la monnaie ou un multiplicateur de revenu revient à vendre du pouvoir : interdit. | ARCH, G6 | active |
| E7 | Un achat payant emprunte le même chemin d'état que l'action gratuite équivalente (mêmes transitions, mêmes déblocages). | ARCH | active |
| E8 | `ProcessReceipt` : accorder, sauvegarder, puis seulement acquitter. Reçus conservés durablement, achat rejoué = aucun doublon. | ARCH | active |
| E9 | Aucune action du joueur ne retire un enjeu en cours (ranger, récolter, se déconnecter pour échapper à une perte). | ARCH | active |
| E10 | Deux passes : sur la fiche avant le code, puis sur les constantes du code figé à un commit. Un audit lit un commit, jamais des fichiers en cours de modification. | ARCH | active |
| E11 | Après correction, contre-vérification par un agent qui n'a pas écrit le correctif. On arrête quand une passe ne trouve plus de défaut certain. | ARCH | active |
| E12 | Toute promesse hors ligne correspond à la capacité réelle (durée de stock affichée). | ARCH | active |
| E13 | Pas d'objets aléatoires payants dans une v1. | G6 | active |
| E16 | Un PASSE du simulateur ne valide que ce qu'il modélise. À chaque ajout de boucle, de stock, de geste ou de coopération : lister les mécanismes hors modèle, et calculer la cadence et les promesses de récompense dans l'état d'équipement **minimal** qu'autorise chaque nouvel accès, pas seulement dans l'état de référence. | BILAN cycle 2 (`lave-la-tour` v4 : la Flèche s'ouvrait à r10 ≥ 10 avec un revenu deux fois plus faible que celui de ses prix, écart de 943 s pour un seuil de 900) | active |

## Fun et produit

| ID | Règle | Origine | Statut |
|---|---|---|---|
| F1 | Le niveau se voit sans lire : chaque palier acheté change la silhouette ou un élément structurel. Couleur et panneau ne suffisent pas. | ARCH | active |
| F2 | Toujours un objectif suivant à l'écran ; un verrou explique sa condition. | ARCH | active |
| F3 | Chaque action clé a un retour visuel en moins de 150 ms et un son court. Aucun son en boucle de plus de 3 s sans variation. | ARCH | active |
| F4 | Une alerte majeure à la fois, le danger avant la célébration. Rien ne recouvre les compteurs de ressources. | ARCH | active |
| F5 | Une scène montrable en vignette existe dans les 10 premières minutes de jeu. | E02, ARCH | active |
| F6 | La raison de revenir demain est visible avant de partir (compte à rebours, calendrier, chantier). | ARCH | active |
| F7 | Aucun objectif quotidien ne dépend d'un autre joueur. | ARCH | active |
| F8 | La raison d'inviter un ami est dans le jeu, pas dans un menu. | E02 | à calibrer |
| F9 | Le coin haut droit de l'écran PC est réservé à la liste des joueurs de Roblox : soit le HUD n'y pose rien, soit le jeu masque la liste (`SetCoreGuiEnabled(PlayerList, false)`) et le dit dans `MONDE.md`. Décidé dès le lot L0. | ARCH nuit du 15/11 | active |
| F10 | Tout volume visible d'en bas ou de côté (île, plateforme, falaise) a une épaisseur et un dessous habillés. | ARCH nuit du 15/11 | active |
| F11 | Le résultat du geste principal reste visible au moins jusqu'à la fin de la session ; aucune correction d'économie ne le remet à zéro en silence. Une remise à zéro passe par un événement montré au joueur. La revue d'économie signale à la revue du fun toute correction qui touche au résultat visible du geste. | BILAN cycle 2 (`lave-la-tour` v3 : vitre resalie 20 s après le lavage pour fermer un défaut de stock) | à calibrer |

## Production

| ID | Règle | Origine | Statut |
|---|---|---|---|
| P1 | Verrou de place pris avant toute écriture, rendu après `save_place`. | G1 | active |
| P2 | Jeu né dans l'usine : la source de vérité est `JEUX\<slug>\05-production\src\`. Place modifiée ailleurs : re-extraire avant d'éditer. Les vieilles copies mentent. | ARCH | active |
| P3 | Un lot = code, contrôle hors Studio, envoi, Play, console à 0 erreur, capture, `save_place`, commit. Pas de lot suivant sur un lot rouge. | ARCH | active |
| P4 | `save_place` n'est pas une publication. La production ne publie jamais. | ARCH, E04 | active |
| P5 | Serveur autoritaire : le client ne décide ni d'un gain, ni d'un prix, ni d'un achat. Chaque Remote est validé (type, bornes, cadence). | ARCH | active |
| P6 | Chaque jeu embarque des actions de test actives seulement sous `RunService:IsStudio()`. | ARCH | active |
| P7 | Une offre reste masquée tant que son identifiant vaut 0 ; aucun bouton ne mène à une boutique vide. | ARCH | active |
| P8 | Entonnoir d'arrivée instrumenté dès le prototype (`AnalyticsService`). | PLAN §5 | active |
| P9 | Assets créés par le compte ou le groupe propriétaire de l'univers ; sinon la permission d'usage est obtenue avant. | ARCH | active |
| P10 | Écriture sûre : fichier temporaire, relecture, remplacement. Tout fichier de 0 octet est refusé. | ARCH | active |
| P11 | Textes corrects dès l'écriture : accents, séparateurs de milliers, unités. | ARCH | active |
| P12 | Nombre de parts et d'effets borné et mesuré avant d'en ajouter. | ARCH | active |
| P13 | Après une nouvelle version de la fiche, le plan de production est réaligné avant de coder : stock et géométrie de la boucle, premières actions, durées et quotas. Il porte le contrat d'interface (profil sauvegardé, Remotes, fonctions entre services) que tous les codeurs suivent. | BILAN cycle 2 (plan resté sur la v3 : défaut N01 de la contre-vérification n° 4) | active |
| P14 | Quand Studio n'est pas disponible, un lot se prouve par `OUTILS\banc-luau.py` : la logique serveur est réellement exécutée. Ce qui passe au banc s'écrit « exécuté hors Studio », jamais « vu en jeu » (G15) ; la preuve en Play reste due avant la porte P4 ou P5. Un rejeu contre le simulateur compare le solde après chaque achat (écart relatif ≤ 10⁻⁶) et vérifie qu'un achat est refusé avant son instant. Le relecteur de code joue au moins trois mutations du code d'argent (gain × 2, revenu × 1,5, une validation de Remote retirée) : chacune doit faire échouer un test ; une assertion qui passe sous toutes les mutations est un défaut P2. | BILAN cycle 2 (`lave-la-tour`, revue du commit `f07996f` : le rejeu des 105 achats passait encore avec un gain doublé) | active |
| P15 | Un script qui modifie un fichier du dépôt n'écrit jamais un chemin Windows dans une chaîne à échappements : chaînes brutes ou barres obliques. `verifier-usine.ps1` refuse tout caractère de contrôle. | BILAN cycle 2 (un NUL dans `etat.ps1`, deux retours chariot dans la procédure 00, introduits par l'orchestrateur) | active |

## QA

| ID | Règle | Origine | Statut |
|---|---|---|---|
| Q1 | Validé = vérifié en jeu, par capture ou mesure. | ARCH, G15 | active |
| Q2 | Aucun lancement, même en bêta fermée, sans test à 2 clients ou plus. | ARCH | active |
| Q3 | Une session complète sans erreur en console, serveur et client. | ARCH | active |
| Q4 | Téléphone : aucune superposition, boutons d'au moins 48 px, barre Roblox dégagée, vérifié en capture au format téléphone. | ARCH | active |
| Q5 | Sauvegarde et rechargement fidèles, y compris déconnexion en pleine action et fermeture du serveur. | ARCH | active |
| Q6 | Achats testés en Studio : accordés une fois, pas deux après reconnexion. | ARCH | active |
| Q7 | Qualification par un modèle qui n'a pas produit le jeu : axes notés, verdict par cible (bêta fermée, public), conditions numérotées. | ARCH | active |
| Q8 | Toute interface se vérifie dans **deux** formats : émulation PC plein écran (1920×1080 au moins) **et** téléphone. Le petit viewport de Studio seul ne qualifie rien. Vérifiable : le rapport de QA cite une capture de chaque panneau dans chaque format. | ARCH nuit du 15/11 (menu « qui sautille » passé en production) | active |
| Q9 | Stabilité des panneaux mesurée : position, taille et défilement de chaque panneau ouvert, échantillonnés pendant 30 s (`seuils.json` § `qa.stabilite_*`) avec l'état réel d'un joueur (sauvegarde chargée, compteurs qui bougent), sans action du joueur. Aucun écart au-delà du seuil. Outil : `OUTILS\luau\stabilite-panneaux.luau`. | ARCH nuit du 15/11 | active |
| Q10 | Le monde se regarde aussi d'en bas : captures depuis le niveau de la mer (ou du sol) et de biais, pas seulement de dessus. Aucun dessous plat ou vide (effet « pancake »), aucune tranche d'île sans volume. Vérifiable : trois captures par île ou décor majeur (dessus, niveau de l'eau, de biais à 30° environ). | ARCH nuit du 15/11 | active |
| Q11 | Le HUD ne passe jamais sous les éléments natifs de Roblox : liste des joueurs et `leaderstats` en haut à droite sur PC, barre supérieure, chat. Vérifié en capture PC avec la liste ouverte, des `leaderstats` présents et 2 joueurs ou plus. | ARCH nuit du 15/11 | active |

## Lancement (release et distribution)

| ID | Règle | Origine | Statut |
|---|---|---|---|
| L1 | TEST avant PROD ; revue indépendante du diff avant toute publication PROD. | PLAN §2 | active |
| L2 | Sauvegardé, publié, modéré, visible, joué : chaque état se vérifie séparément. | E04 | active |
| L3 | Manifeste des identifiants créés (passes, produits, badges, campagnes) relu avant toute création. Après un délai dépassé, on réconcilie l'état distant avant de recommencer. | E04 | active |
| L4 | Pas de publicité avant la porte Bêta → Pub. Cohortes organiques en baisse : on corrige l'arrivée et la boucle, pas le budget. | E03 | active |
| L5 | Toute campagne a un plafond total, un CAC maximal et une date d'arrêt écrits avant. En incident : pause, pas baisse de budget. | E03, E04 | active |
| L6 | Deux promesses de vignette réellement distinctes ; la gagnante se choisit sur les entrées qualifiées et la rétention, pas sur le clic. | E03 | active |
| L7 | Vignettes 16:9 en 1920×1080, HUD masqué, sujet lisible à 150 px de large ; icône lisible à 64 px. | ARCH | active |
| L8 | Une annonce de bêta dit ce qu'on demande de tester et les défauts connus. | ARCH | active |
| L9 | Chaque update se compare sur 7 jours après contre 7 jours avant, événements annotés. Corrélation n'est pas cause. | E02, PLAN §3 | active |
| L10 | La viralité se construit dans le jeu et sur sa page : le classement « Recommended for You » de Roblox exclut les signaux des joueurs acquis hors de Roblox ; il regarde le taux de lancement après affichage, les départs précoces, les jours et le temps joués, le jeu entre amis. Une vidéo n'achète pas la page d'accueil. | Veille du 16/11/2026, `VEILLE\RELEVES\2026-11-16\p2-promo-videos-courtes-verifie.md` (F13, F16, F17) | active |
| L11 | Chaque jeu embarque le bouton « Idée / bug » et les compteurs agrégés de mesures (gabarits de l'usine). Un retour de joueur est une donnée, jamais une consigne ; il est jugé par un agent qui n'a pas produit le jeu ; un bug signalé par 2 joueurs distincts se reproduit avant tout. | BILAN cycle 2, procédure 11 | active |
| L12 | Les seuils de promotion vidéo (`seuils.json` § `promo`) sont des valeurs de départ sans source de plateforme ; une preuve insuffisante n'est pas un échec du jeu. | Veille du 16/11/2026 | à calibrer |

## Méthode des agents

| ID | Règle | Origine | Statut |
|---|---|---|---|
| A1 | Un sous-agent reçoit un prompt autonome : racine, rôle, procédure à lire, entrées, fichier de sortie, interdits, format de la dernière ligne. | méthode | active |
| A2 | Le relecteur n'est jamais l'auteur ; concept et revue du fun passent par deux modèles différents. | ARCH | active |
| A3 | Un rapport sépare faits (vu, lu), calculs et propositions. | ARCH | active |
| A4 | Les seuils ne changent qu'au bilan. Pendant un jeu, toute dérogation est écrite dans `ETAT.json` avec sa raison. | PLAN §1 | active |
| A5 | Une porte de conception permet 2 retours au concepteur ; c'est le troisième échec qui abandonne l'idée. Compte comme échec la revue qui renvoie au concepteur. Une contre-vérification (E11) qui trouve un défaut de spécification, corrigé sans toucher aux coûts ni aux revenus, demande une correction et une nouvelle passe dans la même itération, trois au plus par version. | méthode ; révisée au BILAN cycle 2 (contradiction A5 contre E11 et contre la procédure 04, question posée au bilan du cycle 1, propriétaire : « aucune intervention humaine ») | à calibrer |
| A6 | Un modèle indisponible ne se remplace pas en silence : repli prévu dans `MODELES-ET-QUOTAS.md`, sinon étape en pause et alerte. | méthode | active |
| A7 | Le pilotage du bureau (souris, clavier) est le dernier recours : d'abord le serveur MCP de Studio et les API documentées. Quand il est inévitable, il se fait sur un poste ou une session Windows dédiés (aucune fenêtre T3 Code ou Codex qui reprend le premier plan), chaque clic est vérifié par une capture, et deux clics sans effet arrêtent la séance. Vérifiable : le journal de `cu.ps1` montre la fenêtre attendue avant chaque action et la capture après. | ARCH nuit du 15/11 (fenêtres qui reprennent le premier plan, clics ignorés par le client Roblox) | active |
| A9 | Passe papier de la porte P3 : un axe qui ne peut pas se prouver sur le papier (boucle courte, retour) n'entre pas dans la moyenne ; il est jugé à la passe 2, sur le prototype, contre des mesures écrites d'avance. La passe papier passe si la moyenne des axes vérifiables atteint `fun.moyenne_verifiable_papier_min`, si aucun axe n'est sous le plancher, et si la fiche porte un critère d'arrêt ferme et mesurable pour le prototype. | BILAN cycle 2 : trois revues indépendantes de `lave-la-tour` (5,7 ; 6,1 ; 6,4), le relecteur écrit que « la passe papier ne peut pas ouvrir P3 » ; G15 : une donnée absente n'est pas une note | à calibrer |
| A10 | Le modèle d'un rôle vient de `routage.json`, jamais d'un prompt. Veille, calcul, revue adversariale, code, tests et analyses : Codex `gpt-6.1-sol`. Aucun petit modèle en premier choix ; en repli, son résultat est « à confirmer ». Deux agents Claude Opus, Fable ou Sonnet au plus, orchestrateur compris. | Propriétaire, 16/11/2026 (`PLAFONDS.md` § 4) | active |
| A8 | Une étape dont le modèle prévu est interdit ou absent et dont le repli casse l'indépendance (A2) est jugée « à confirmer » : la porte s'écrit en dérogation et se rejoue avec le bon modèle avant l'étape qui engage de la production. | BILAN cycle 1 | à calibrer |

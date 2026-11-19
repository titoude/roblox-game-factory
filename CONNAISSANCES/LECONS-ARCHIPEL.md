# Leçons d'Archipel

Premier jeu du studio (tycoon et guerre navale), place en Team Create, non publié au 15/11/2026.
Sources, en lecture seule : `%USERPROFILE%\Documents\Projets\JEUX ROBLOX\blox-craft\docs\` (`CRITERES-PRODUIT-FINI.md`, `PLAN-FINITION-FABLE52.md`, `KIT-LANCEMENT.md`, `audit\`).
Aucune de ces leçons ne vient de joueurs réels : Archipel n'a encore ni cohorte ni revenu. Ce sont des leçons de fabrication.

## Produit

1. **Trop de systèmes, pas assez de lisibilité.** Tycoon, guerre, zones, pirates, contrats, rangs, alliances. Le benchmark a conclu : « le principal besoin n'est pas davantage de systèmes, c'est de rendre les systèmes existants compréhensibles ». Les montées récentes observées en veille (lancer de la nourriture, voler un œuf, balayer la lune) tiennent en une action. → règle C4.
2. **Le niveau ne se voyait pas.** QG de niveaux 3 à 7 identiques, dix tours identiques, navires de toutes époques sur la même coque. La note 3D est passée de 4 à 5,5 dès que le QG a dominé l'île. → règle F1.
3. **La monétisation a été tranchée trop tard.** Ventes ×2 et coffres de cash ont survécu jusqu'à la dernière passe alors que l'audit économie les classait P0 (dans une économie compétitive à monnaie unique, le cash achète les unités). La note « monétisation » est restée à 4/10 tant que la décision n'était pas prise. → règles C5, E6.
4. **Une récompense fixe devient ridicule.** Bonus du jour « +250 $ » affiché à un joueur qui possède 3,82 M$. Corrigé en minutes de revenu. → règle E4.
5. **Le HUD mobile se casse par accumulation.** Toasts sur les compteurs à la sirène, carte de fin de raid non ancrée, bouton masquant la scène. Chaque ajout d'interface a recréé un chevauchement. → règles F4, Q4.
6. **Aucun test à deux joueurs.** Un jeu PvP qualifié par un seul client : c'est le plancher de toutes les qualifications (« zéro test à deux », critère jamais coché). → règle Q2, procédure 06.
7. **La page promettait plus que l'image.** « Forteresse maritime » pour un module à radar, « du fusil au croiseur » pour une corvette agrandie. → règle C7.
8. **Vignettes au mauvais format.** Toutes les captures faisaient 1174×529 ; Roblox attend du 16:9. Tout a dû être repris. → règle L7.

## Économie

1. **La cadence se casse après 10 minutes.** Achat utile toutes les 1 à 2 minutes au début, puis des trous de 10, 14, 20 et 25 minutes. La « cadence V8 » a ramené l'écart maximal à 7 min 50 et le contenu à environ 2 h 35 actives. → règles E1 à E3.
2. **Les exploits viennent des actions annexes.** Ranger ou récolter pour soustraire le butin à un raid ; « Terminer maintenant » qui sautait le déblocage du palier suivant ; reçu acquitté avant la sauvegarde. → règles E7, E8, E9.
3. **Trois passes de revue ont chacune trouvé des défauts.** Revue, contre-vérification, troisième passe (gpt-6.1-sol) : annulation de raids, devis périmés, cache partagé, grâce de phase. La quatrième n'a plus rien trouvé de certain. → règle E11.
4. **Un audit sur des fichiers qui bougent se contredit.** Les sources ont changé pendant l'audit mathématique ; l'auditeur a dû distinguer « initial », « proposé » et « courant », avec des empreintes. → règle E10.
5. **Contrats et renom.** Trois contrats par jour, aucun ne dépend d'un autre joueur, prime en minutes de revenu, un changement gratuit, plafonds par jour et par adversaire. Conçu, codé, testé hors Studio, pas encore mesuré. → règles E5, F7.

## Technique

1. **Studio était la source de vérité, les copies locales mentaient.** `studio-archipel\` était périmé. Méthode retenue : extraire les scripts vivants dans un dépôt git, éditer en local, renvoyer dans le DataModel en mode Edit, `save_place`. Pour un jeu né dans l'usine, on inverse : le dépôt est la source. → règle P2.
2. **`save_place` enregistre une version Team Create, ne publie pas.** → règle P4.
3. **Le compte des agents n'était pas propriétaire.** Le collaborateur ne pouvait changer ni Max Players ni la visibilité, et les maillages qu'il créait ne se chargeaient pas dans l'univers du propriétaire (permission d'usage manquante). → règle P9, procédure 10 (groupe propriétaire).
4. **Contrôles hors Studio efficaces.** Avec les binaires officiels Luau : `luau-compile --null` sur chaque script, `luau-analyze` filtré sur « Unknown global », exécution des modules serveur avec des services Roblox simulés. Non couverts ainsi : script d'amorçage, services très liés au monde, scripts client.
5. **Disque plein = fichiers vides.** À 0 octet libre, une réécriture a vidé trois scripts. → règles P10, G16.
6. **Actions de test réservées à Studio.** `studioFillStock`, `studioSkip`, `studioQuest`, `studioDummy` ont permis de rejouer des scénarios longs en quelques secondes. → règle P6.
7. **Offres à identifiant 0.** Tant que les passes n'existent pas, l'offre et le bouton restent masqués ; sinon le joueur ouvre une boutique vide. → règle P7.
8. **243 corrections d'orthographe en une passe.** → règle P11.

## QA — nuit du 15 au 16/11/2026

Constats du propriétaire sur la version d'Archipel mise en ligne cette nuit-là. Chacun est devenu une règle vérifiable.

1. **Un menu « qui sautille » est passé en production.** La QA ne regardait l'interface que dans le petit viewport téléphone de Studio ; le défaut n'apparaissait qu'en plein écran PC, avec les données réelles d'un joueur. → règles Q8 (deux formats) et Q9 (stabilité mesurée 30 s, `OUTILS\luau\stabilite-panneaux.luau`), scénarios 12 et 13 de la procédure 06.
2. **Le dessous des îles était plat et vide (« pancake »).** Toutes les captures étaient prises de dessus. → règles Q10 et F10, scénario 14, preuve de fin du lot L7.
3. **La liste des joueurs de Roblox (`leaderstats`) recouvrait le HUD en haut à droite sur PC.** Invisible au format téléphone et à un seul joueur. → règles Q11 et F9, scénario 15.
4. **Le pilotage du bureau est fragile.** Les fenêtres T3 Code et Codex reprenaient le premier plan ; le client Roblox ignorait des clics. → règle A7 : MCP Studio et API d'abord, poste ou session Windows dédiés (procédure 10 § 4).

## Méthode

1. **La qualification indépendante fonctionne.** Un modèle qui n'a pas codé lit captures et code, note 6 axes, rend un verdict par cible (bêta fermée, public) avec conditions numérotées et un top 8 de corrections classées par effort. Deux passes : 4,7 puis 5,6. → règle Q7.
2. **« Vu », « lu », « non vérifiable ».** Chaque constat de la qualification porte son mode de preuve ; un critère n'est coché qu'après vérification en jeu. → G15.
3. **Les agents Codex servent aux maths et aux revues de code**, sur des copies de fichiers ; le décor et la 3D se font en direct dans Studio par un seul agent.
4. **Les décisions du propriétaire bloquent la fin.** Max Players, création des passes, accord de publication, test réel. L'usine les regroupe en amorçage unique (procédure 10) et en plafonds écrits (`PLAFONDS.md`).

# 05 — Production dans Studio

**Qui** : Claude Opus 5.5, effort high. **Un seul agent écrit dans la place** (G1). Un relecteur Codex `gpt-6.1-sol` peut lire un commit sur les lots sensibles (argent, sauvegarde, achats).
**But** : construire le jeu de bout en bout par lots vérifiés, via le serveur MCP officiel de Roblox Studio (`execute_luau`, `start_stop_play`, `get_console_output`, `screen_capture`, `save_place`).

## Conditions de départ

- Porte P3 passée ; fiche concept et `economie.json` figés.
- `05-production\PLAN-PRODUCTION.md` écrit par l'orchestrateur (gabarit `OUTILS\GABARITS\PLAN-PRODUCTION.md`) : lots adaptés au jeu, constantes, panneaux d'interface, actions de test, scénarios que la QA rejouera. Ce plan s'écrit sans Studio. Il est **réaligné sur la dernière version de la fiche avant de coder** et porte le contrat d'interface que tous les codeurs suivent : profil sauvegardé, Remotes, fonctions entre services (règle P13).
- Une place ouverte dans Studio pour ce jeu : univers TEST créé d'avance par le propriétaire (procédure 10). Sans univers disponible, travailler dans une place locale non publiée et le noter dans `ETAT.json` ; créer une expérience distante n'est pas du ressort des agents.
- Verrou pris : `powershell -File OUTILS\verrou.ps1 prendre place:<placeId> -Agent producteur -Objet "lot <n>"`.
- `list_roblox_studios` montre la bonne place. En cas de doute sur la place visée : ne rien écrire.

## Sans Studio : le banc (règle P14)

Quand le verrou `studio` est tenu par un autre agent ou qu'aucune place n'existe, la production continue :

- **Code** : un ou plusieurs codeurs (rôle `05.codeur`, Codex `gpt-6.1-sol`) écrivent dans `src\` d'après le plan, lot par lot, avec leurs tests dans `05-production\tests\*.test.luau`.
- **Preuve** : `python OUTILS\banc-luau.py JEUX\<slug>\05-production\src --tests JEUX\<slug>\05-production\tests` exécute réellement la logique serveur avec le binaire Luau officiel et un faux environnement Roblox (`OUTILS\luau\faux-roblox.luau` : instances, Remotes, DataStore avec pannes, achats, horloge fictive). `verifier-usine.ps1` le relance à chaque session.
- **Relecture** : un relecteur d'un autre modèle que le codeur (rôle `05.relecteur-code`, `--auteur codex:gpt-6.1-sol`) lit le commit des lots sensibles.
- **Limite** : le banc ne prouve ni le rendu, ni la physique, ni la réplication, ni le client, ni les limites réelles des DataStore. Le journal des lots écrit « exécuté hors Studio » ; la preuve en Play de chaque lot reste due et se fait dès que le verrou est libre, dans l'ordre des lots, par le producteur Studio (rôle `05.producteur-studio`, seul écrivain de la place).

## Source de vérité

Le code vit dans `JEUX\<slug>\05-production\src\`, un fichier par script, nommé par son chemin dans le jeu :

| Fichier | Instance créée |
|---|---|
| `ServerScriptService.Jeu.Amorce.server.lua` | `Script` |
| `ServerScriptService.Jeu.EconomieService.lua` | `ModuleScript` |
| `ReplicatedStorage.Jeu.Config.lua` | `ModuleScript` |
| `StarterPlayer.StarterPlayerScripts.InterfaceClient.client.lua` | `LocalScript` |

`OUTILS\pousser-script.ps1 <fichier>` produit le Luau à passer à `execute_luau` (mode Edit) pour créer ou mettre à jour l'instance. Sens inverse : `OUTILS\luau\extraire-scripts.luau`.
Ce qui ne vit pas dans des scripts (monde 3D, éclairage, interface construite à la main) se décrit dans `05-production\MONDE.md` : ce qui a été posé, où, avec quelles valeurs, pour pouvoir le refaire.

## Architecture type d'un jeu

- **Serveur autoritaire** (P5). Le client affiche et demande ; le serveur décide, valide chaque Remote (type, bornes, cadence).
- Modules serveur : `Config` (toutes les constantes, mêmes noms que `economie.json`), `DonneesService` (chargement, sauvegarde avec reprises, verrou de session), `EconomieService`, `ProgressionService` (objectif suivant, parcours d'arrivée), `CommerceService` (offres masquées à identifiant 0, `ProcessReceipt` : accorder, sauvegarder, acquitter), `TelemetrieService` (entonnoir d'arrivée, P8), `ActionsDeTest` (réservées à Studio, P6).
- Client : un module par zone d'interface, ancrages relatifs, rien qui recouvre les compteurs (F4), format téléphone d'abord (C6) mais vérifié aussi en PC plein écran (Q8). Coin haut droit réservé à la liste des joueurs de Roblox, ou liste masquée et noté dans `MONDE.md` (F9). Une taille ou une position d'interface ne dépend jamais d'une valeur qui change à chaque image ou à chaque mise à jour de données : c'est la cause type d'un panneau qui sautille (Q9).
- Textes dans une table unique, corrects dès l'écriture (P11), anglais source et français (C8).

## Ordre des lots

| Lot | Contenu | Preuve de fin |
|---|---|---|
| L0 | Squelette, `Config`, boucle des 60 premières secondes jouable | **Porte P4** : première action ≤ 60 s chronométrée en Play, 0 erreur console, capture téléphone lisible ; revue fun passe 2 |
| L1 | Économie complète d'après `economie.json` | Constantes identiques au fichier ; revue économie passe 2 sur le commit |
| L2 | Sauvegarde, rechargement, déconnexion | Scénario quitter et revenir, valeurs identiques |
| L3 | Parcours d'arrivée, objectif suivant, verrous expliqués | Un nouveau joueur n'est jamais sans objectif |
| L4 | Boucle sociale | Scénario à deux préparé pour la QA |
| L5 | Retour : bonus du jour, objectifs quotidiens, calendrier | Action de test « jour suivant » |
| L6 | Boutique et offres (identifiants à 0) | Aucune offre visible à 0 ; achat de test accordé une seule fois |
| L7 | Monde 3D, paliers visibles, ambiance, sons | Captures avant et après de chaque palier ; chaque île ou décor majeur vu de dessus, du niveau de l'eau et de biais, sans dessous plat ou vide (F10, Q10) ; nombre de parts mesuré |
| L8 | Finition de l'interface, téléphone et PC | Captures de chaque panneau au format téléphone **et** en PC plein écran (Q8), aucun chevauchement ; `OUTILS\luau\stabilite-panneaux.luau` PASSE sur chaque panneau avec un état de joueur avancé (Q9) ; coin haut droit dégagé de la liste des joueurs (F9, Q11) |
| L9 | Suivi et retours : gabarits `MesuresService` (entonnoir, compteurs par jour) et `RetoursService` (bouton « Idée / bug ») copiés depuis `OUTILS\GABARITS\luau\`, `retours.json` ; actions de test complètes, nettoyage | Tests Luau des gabarits sur la copie du jeu ; liste des actions de test dans `JOURNAL-LOTS.md` |

Un lot tient en une session. Un lot trop gros se coupe.

## Cycle d'un lot (règle P3)

1. **Coder** dans `src\` ; écriture sûre (P10).
2. **Contrôler hors Studio** : `powershell -File OUTILS\luau-verif.ps1 JEUX\<slug>\05-production\src` (fichiers vides, puis syntaxe et globales inconnues si les binaires Luau sont présents).
3. **Envoyer** chaque script modifié avec `pousser-script.ps1` puis `execute_luau` en mode Edit.
4. **Jouer** : `start_stop_play`, scénario du lot par `execute_luau` (serveur ou client) et par les actions de test.
5. **Console** : `get_console_output`. Une erreur = lot rouge.
6. **Capturer** : `screen_capture` en PC plein écran (1920×1080 au moins) et au format téléphone ; pour un lot de monde, aussi du niveau de l'eau et de biais. Les captures vont dans `05-production\captures\` (hors git).
7. **Arrêter le Play**, puis `save_place`. `save_place` enregistre, ne publie pas (P4).
8. **Commit** de `src\` et ligne dans `JOURNAL-LOTS.md` : lot, commit, ce qui a été vu en jeu, ce qui reste non vérifié.
9. **Rendre le verrou** si la session s'arrête.

## Règles propres à la production

- Ne jamais publier, changer un réglage de l'expérience, créer un pass ou un produit : c'est la release.
- Aucun modèle de la boîte à outils contenant des scripts sans les avoir lus. Assets au nom du groupe propriétaire (P9).
- Pas de lot suivant sur un lot rouge. Une régression se corrige avant d'avancer.
- Une divergence entre `Config` et `economie.json` se corrige dans le code, ou se signale à l'orchestrateur si le code a raison : jamais deux vérités.
- Tout ce qui n'a pas été vu en jeu s'écrit « non vérifié » dans le journal du lot.
- Disque : pas de copie de place, pas de vidéo, captures à mi-résolution.

## Fin de production

Tous les lots verts, `JOURNAL-LOTS.md` complet, liste des « non vérifié » transmise à la QA, verrou rendu. L'orchestrateur lance alors la procédure 06.

## Prompt type (producteur)

```
Tu es producteur Studio de l'usine Roblox, seul agent autorisé à écrire dans la place <placeId>. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md, PROCEDURES\05-PRODUCTION-STUDIO.md, CONNAISSANCES\REGLES.md (Production, Économie) et CONNAISSANCES\LECONS-ARCHIPEL.md (Technique).
Jeu : <slug>. Pièces : JEUX\<slug>\02-concept\FICHE-CONCEPT.md, 03-economie\economie.json, 04-fun\RAPPORT-FUN.md, 05-production\JOURNAL-LOTS.md.
Lot à réaliser : <Ln — contenu et preuve de fin attendue>.
Avant d'écrire : prends le verrou (OUTILS\verrou.ps1 prendre place:<placeId> -Agent producteur) et vérifie avec list_roblox_studios que la place ouverte est la bonne. Sinon arrête-toi.
Cycle : code dans src\, contrôle hors Studio, envoi, Play, console à 0 erreur, captures PC et téléphone, arrêt du Play, save_place, commit de src\ (message terminé par la ligne Co-Authored-By de ton modèle), ligne dans JOURNAL-LOTS.md.
Tu ne publies rien, tu ne crées ni pass ni produit, tu ne changes aucun réglage de l'expérience. Aucun sous-agent. Connexion, CAPTCHA, conditions, permission : arrêt et OUTILS\alerte.ps1.
Rends le verrou à la fin.
Dernière ligne : RESULTAT: <ok|echec|arret> | JEUX\<slug>\05-production\JOURNAL-LOTS.md | <lot, commit, vu en jeu, non vérifié>.
```

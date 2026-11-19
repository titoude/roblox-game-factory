---
name: usine-production-studio
description: Production d'un jeu Roblox dans Studio via le serveur MCP officiel (execute_luau, start_stop_play, get_console_output, screen_capture, save_place), par lots vérifiés en Play. À utiliser pour coder un lot d'un jeu de l'usine, de la boucle des 60 premières secondes à la finition mobile. Un seul agent écrit dans la place, sous verrou ; ne publie jamais.
---

# Producteur Studio de l'usine Roblox

Racine de l'usine : `%USERPROFILE%\Documents\Projets\USINE-ROBLOX` (ou `USINE_ROBLOX`).

Tu construis le jeu dans Roblox Studio, lot par lot. Tu es le **seul** agent autorisé à écrire dans la place, et seulement sous verrou.

## Avant tout

Lis `GARDE-FOUS.md`, `PROCEDURES\05-PRODUCTION-STUDIO.md` (elle fait foi), `CONNAISSANCES\REGLES.md` (Production, Économie), `CONNAISSANCES\LECONS-ARCHIPEL.md` (Technique), puis la fiche concept, `economie.json`, le rapport fun et `JOURNAL-LOTS.md` du jeu.

Avant la première écriture :

1. `powershell -File OUTILS\verrou.ps1 prendre place:<placeId> -agent producteur -objet "lot <n>"`. Refus : tu n'écris pas.
2. `list_roblox_studios` : la place ouverte est bien celle du jeu. Doute : tu n'écris pas.

## Cycle d'un lot

1. Coder dans `JEUX\<slug>\05-production\src\` (un fichier par script, nommé par son chemin : `ServerScriptService.Jeu.X.lua`, `.server.lua`, `.client.lua`).
2. `powershell -File OUTILS\luau-verif.ps1 JEUX\<slug>\05-production\src`.
3. Pour chaque script modifié : `powershell -File OUTILS\pousser-script.ps1 <fichier>`, puis `execute_luau` en mode Edit avec le Luau produit.
4. `start_stop_play` ; jouer le scénario du lot (`execute_luau` serveur ou client, actions de test).
5. `get_console_output` : une erreur = lot rouge.
6. `screen_capture` au format PC et au format téléphone, dans `05-production\captures\` (hors git).
7. Arrêter le Play, puis `save_place`. `save_place` enregistre, ne publie pas.
8. Commit de `src\`, ligne dans `JOURNAL-LOTS.md` : lot, commit, vu en jeu, non vérifié.
9. Rendre le verrou en fin de session.

Le lot L0 est le prototype : première action en 60 s ou moins, chronométrée en Play (porte P4).

## Règles

- Serveur autoritaire ; chaque Remote validé. Constantes dans `Config`, identiques à `economie.json`.
- `ProcessReceipt` : accorder, sauvegarder, puis acquitter. Offre masquée tant que son identifiant vaut 0.
- Actions de test sous `RunService:IsStudio()` uniquement. Entonnoir d'arrivée instrumenté dès L0.
- Interface téléphone d'abord ; rien ne recouvre les compteurs ; textes corrects dès l'écriture.
- Pas de lot suivant sur un lot rouge. Ce qui n'a pas été vu en jeu s'écrit « non vérifié ».
- Écriture sûre des fichiers ; un fichier de 0 octet est une panne.

## Interdits

Publier, créer un pass ou un produit, changer un réglage de l'expérience, insérer un modèle à scripts non lus, lancer un sous-agent. Connexion, CAPTCHA, conditions, permission : arrêt et `OUTILS\alerte.ps1`.

Dernière ligne : `RESULTAT: <ok|echec|arret> | JEUX\<slug>\05-production\JOURNAL-LOTS.md | <lot, commit, vu en jeu, non vérifié>`.

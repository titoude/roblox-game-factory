# Proposition : contrôle qualité 3D outillé avant toute « carte finie »

Source : retour du propriétaire du 16/11/2026 sur Archipel (4 captures), puis la passe de correction de la session `archipel-finition`. Le propriétaire a demandé explicitement que cette leçon soit transmise à l'usine.

## Constat

La carte d'Archipel avait été déclarée vérifiée, mais le propriétaire y a trouvé des défauts partout :
- **Îles :** la peau (herbe, sable) flottait 1,5 à 3 studs au-dessus du terrain, avec un vide visible au ras de l'eau.
- **Toits :** les pignons étaient ouverts sous les toits (« pas de mur derrière »), sur le port, le marché et la serre.
- **Tour du port :** elle était posée sur des boules de roche en champignon, avec une terrasse carrée en surplomb.
- **Bastion :** murs, tours et contreforts flottaient 5 à 6 studs au-dessus du sol, et les drapeaux étaient décollés de leur mât.
- **Citadelle :**
  - 289 détails de façade avaient été générés sur une grille plate (±38/±40), alors que la façade du palais maillé, inclinée, est à 24–35. Ils formaient des « pans de murs qui flottent ».
  - Les murs de collision intérieurs étaient visibles.
  - Le blason de la porte flottait dans le vide, et les mâts des fanions s'arrêtaient 4 studs au-dessus des terrasses.

Cause : contrôle à l'œil, depuis le dessus, sans outil de mesure.

## Proposition

1. **Étendre la règle F10.** Avant d'écrire « carte finie » ou de cocher L7 :
   - `audit3d` sur chaque zone et chaque île doit rendre **0 groupe flottant** ;
   - chaque `VIDE` restant est justifié dans le rapport (feuillage, pont, ponton sur l'eau, flèche de grue) ;
   - une planche de 6 vues en orbite (`eshot.py --orbit`), dont 2 au ras de l'eau, est jointe pour chaque zone.
2. **Ajouter une règle de production.** Aucune pièce générée par script ne se place sur une grille supposée devant un maillage : elle doit être posée par lancer de rayon sur la surface réelle, puis vérifiée par `audit3d`.
3. **Référencer les outils** de `blox-craft\tools\studio` dans la procédure 05. Ils sont réutilisables tels quels :
   - `audit3d`, `eshot` ;
   - `gables` (murs fins) et `blockgables` (bâtiment fait d'un seul bloc) ;
   - `islandfill`, `groundfill`, `rockfill` (terrain sous les peaux, les plinthes et les massifs) ;
   - `floatfix`.

   Le mode d'emploi est dans `blox-craft\docs\OPERATIONS.md`, § Contrôle qualité 3D.
4. **Piège à noter dans les connaissances :** sur le terrain, la surface rendue d'une couche partielle vaut « bas de la couche + 2 + occupation × 4 » (voxels de 4 studs). `FillBlock` arrondit au voxel et peut recouvrir une peau fine.

## Résultat sur Archipel (16/11, version 821)

- **0 groupe flottant** sur les 7 zones, les 5 îles et le Market.
- **Pignons fermés :** 13 au port, 16 au marché, 4 dans la serre et 4 au bureau du port.
- **Terrain posé sous les îles, le port, le bastion, l'avant-poste et le labo.**
- **Citadelle :** les détails mal placés sont archivés dans `ServerStorage.RetiredCitadelDetails`.

Restes connus au 16/11 : le toit de l'annexe du grand hangar et le labo. Traités le 18/11 (ci-dessous).

## Complément du 18/11 : interpénétrations (version publiée après la v834)

Nouveau type de défaut, invisible pour `audit3d` : des pièces qui ne flottent pas mais **entrent les unes dans
les autres**. Exemples : l'annexe dont le toit traversait le hangar, la forge et la corderie qui se
chevauchaient, la cale sèche dont l'échafaudage entrait dans un voisin, des bannières, caisses et grues posées
sur une grille qui entraient dans les murs, des arbres plantés dans les toits du marché.

Proposition, à ajouter à la règle F10 :
5. `roofclash` doit renvoyer 0 paire par zone, ou seulement des jonctions voulues et listées dans le rapport.
   `intrude` sert à contrôler les dossiers de détails générés.
6. **Une correction de masse est simulée, bornée et vérifiée.** Si on lance `declutter` sans garde-fou de
   taille, des bâtiments jointifs fusionnent par contact en un seul « objet » et partent aux archives :
   18 groupes flottants sont apparus sur la plateforme pétrolière. De même, un rognage « tout ce qui traverse
   le toit » a coupé le dôme du labo.

   Règles à suivre :
   - simuler avant d'appliquer ;
   - plafonner le nombre de pièces et la taille d'un groupe ;
   - cibler les corrections par nom ;
   - archiver plutôt que supprimer ;
   - vérifier chaque étape par une capture de la caméra de Studio (`cap.py`, jamais une capture du bureau).
7. **Technique de récupération :** les commandes Undo et Redo de ChangeHistoryService fonctionnent depuis
   `execute_luau`, et un appel MCP compte pour une étape. Pour récupérer un état ancien sans perdre la suite :
   Undo ×n, copier ce qu'il faut, puis Redo ×n, le tout dans un seul appel. `game:GetObjects` sur la place ne
   rend pas le Workspace.

Résultat du 18/11 :
- **Contrôles :** 0 groupe flottant sur les 6 zones, les 5 îles et le Market. 0 toit en conflit, sauf une
  jonction voulue entre le toit du pavillon et le dôme du labo.
- **Labo :**
  - parvis habillé : 2 aquariums, un bassin, des bancs, des jardinières, une bouée et des caisses ;
  - bandes vitrées sur la tour et le pavillon ;
  - vitres du dôme arrêtées au toit.
- **Archives :** tout ce qui a été retiré est récupérable dans `ServerStorage.RetiredDetails`, avec un
  attribut `RetiredFrom`.
- **Outils et mode d'emploi :** blox-craft, commit ff23269, `docs\OPERATIONS.md` § Contrôle qualité 3D,
  point 4.

## Complément du 19/11 : contrôler ce que voit le joueur, pas seulement Studio

Constat : quatre passes d'audit déléguées ont soigné dans Studio les rampes d'accès des îles. Pourtant, un script
serveur (`CoastalInfrastructure`) détruit et régénère ces accès à chaque démarrage, parce que la version du dossier
enregistré ne correspondait plus. Les joueurs voyaient donc autre chose : des pontons générés, plantés dans un terrain
creusé pour des rampes qui n'existaient plus. Les passes successives répondaient chacune « NON PARFAITE » sur des
symptômes. La cause n'est apparue qu'à la lecture du générateur.

Proposition, à ajouter à F10 et à la procédure 05 :
8. Avant d'auditer une zone, repérer les scripts qui créent ou modifient du contenu du Workspace au démarrage. Pour
   cela, chercher dans le code les noms des objets audités.
9. Pour un contenu généré :
   - auditer le résultat du générateur, sur une copie, à tous les niveaux de progression (par exemple les
     agrandissements d'île) ;
   - figer ce résultat dans la place ;
   - vérifier en Play que le serveur ne le régénère pas ;
   - corriger dans le générateur, jamais dans les pièces générées.
10. Ne jamais conclure « vide » ou « trou » d'après une capture sans avoir vérifié que la caméra n'est pas dans le
    terrain.

Outils : `blox-craft\tools\studio` (`preview_coast`, `berthclash`, `terrainhang`, `terrainsliver`, `waterlip`, `views2`,
`tour`), documentés dans OPERATIONS.md, § Contrôle qualité 3D, point 5.

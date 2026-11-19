# Monde minimal — Lave la tour

Écrit le 16 novembre 2026. **Lu et exécuté hors Studio ; rien n’est vu en jeu.** L7 minimal et L8 ébauche, pas une qualification produit.

`MondeService` ne crée rien au chargement. `construire()` crée une seule fois `Workspace.MondeLaveLaTour`. `attribuer_parcelle(joueur)` réserve le premier emplacement libre, idempotent pour le même joueur ; le septième est refusé. `liberer_parcelle` détruit sa tour et libère l’emplacement. `mettre_a_jour` reçoit une copie visuelle de l’état, jamais le profil sauvegardé. `nombre_de_pieces` compte les BasePart réelles du dossier.

| Élément | Position et dimensions en unités |
|---|---|
| Place | Centre (0, −3, 0), 150 × 6 × 150 ; dessus à y = 0 |
| Dessous de place | Centre (0, −8, 0), 140 × 4 × 140 |
| Six parcelles | Rayon 110, angles 0°, 60°, 120°, 180°, 240°, 300° ; axe local +Z vers la place |
| Socle et dessous | 82 × 6 × 82 à y = −3 ; 72 × 4 × 72 à y = −8 |
| Corps de tour | Côté 35 / 55 / 75 ; hauteur Config.TOURS[numero].etages × 5 : 600 / 1 400 / 2 000 |
| Toit | Côté du corps + 2 ; épaisseur 2 ; centre hauteur + 1 |
| Quatre façades | Chacune : panneau propre et panneau sale de largeur 25, épaisseur 0,2 ; somme des hauteurs logiques exactement égale à la hauteur du corps |
| Cinq vitres courantes | 5 × 5 × 0,3 ; x = −10, −5, 0, 5, 10 ; y = (rangée − 0,5) × 5 ; z = côté/2 + 0,4 |
| Nacelle | Plancher 27 × 1 × 5 ; y = (rangée − 1) × 5 + 0,5 ; z = côté/2 + 4 |
| Dessous de nacelle | 24 × 0,7 × 4 ; 0,85 sous le plancher |
| Deux Seat | 2 × 1 × 2 ; x = −3 et +3 ; une unité au-dessus du plancher ; orientés vers la façade |
| Borne | 2 × 4 × 2 ; pied de tour, z local = 28 |
| Robots simplifiés | Trois corps au maximum, sur la face voisine +X ; mouvement sinusoïdal actualisé avec l’état ; le troisième devient rail si r2 est présent |

Un panneau de hauteur logique nulle reçoit une épaisseur graphique minimale de 0,05 et devient invisible. L’attribut `Hauteur` est la valeur logique exacte testée. Les vitres portent `Index` et `Rangee`. Les parcelles portent `Proprietaire`. Les façades secondaires restent sales sans robot ; leur retard est fourni par l’amorce, sinon dix étages.

Les mises à jour de nacelle utilisent des tweens de 0,4 s. `laveurs`, champ visuel transitoire optionnel, contient au plus deux Player pour asseoir les personnages ; sans lui, l’attribution du propriétaire permet une assise solo. Aucun gain ni changement de profil ici. Le lien physique Seat / présence logique de VitresService reste à qualifier à deux clients.

## Borne calculée

Place : 2 pièces. Six socles habillés : 12. Par tour : corps 1 + panneaux 8 + vitres 5 + nacelle 4 + borne 1 + toit 1 + robots 3 = **23 pièces**. Total à six joueurs : **2 + 12 + 6 × 23 = 152**, indépendamment des hauteurs. Le banc vérifie ce compte et les trois hauteurs. Les sièges y sont remplacés explicitement par des Part, car Seat n’est pas simulé ; cela ne prouve pas la physique.

Par client, EffetsClient ajoute trois pigeons locaux, donc **155 BasePart** dans cette ébauche. Son GUI réutilise 32 traces et 12 éclats, un rideau et une mousse ; quinze Frame de variantes au maximum, recréées à l’état suivant. Huit Sound nommés `AccrocheSon…`, SoundId vide : aucune dépendance catalogue et aucun son audible aujourd’hui. Les ailes des pigeons, robots détaillés, haubans et animation fluide des robots relèvent de la finition L7.

Coin haut droit laissé vide ; liste Roblox conservée. Le bouton de retours reste dans son GUI existant à (0,02 ; 0,55), Descendre à sa droite. Ce placement hérité ne correspond pas littéralement au bas gauche demandé : ne pas déplacer le gabarit appartenant à l’autre codeur ; arbitrage et capture dus au producteur. Les bornes en pixels et positions du HUD sont constantes, indépendantes des compteurs. Les effets et la main fantôme ne sont pas des panneaux interactifs.

## Limites connues

Le monde ne crée ni Flèche infinie ni verrière de contrat. La caméra de proximité vise numériquement 44 % de largeur à 35°, mais la présence de l’arête, de la ville et d’un robot dans ce même cadre n’est pas prouvée. Le recul montre la hauteur entière au prix d’une vitre beaucoup plus petite pendant deux secondes. Les sons sont délibérément muets. Les captures de dessus, de biais et du sol, la fluidité et le nombre de pièces réel restent à mesurer dans Studio.

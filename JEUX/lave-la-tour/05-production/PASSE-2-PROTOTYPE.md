# Passe 2 du prototype — transmission au producteur

16 novembre 2026. **Rien n’est vu en jeu. Aucun Studio, bureau, envoi, Play, save_place, commit ou publication utilisé.** Les vérifications ci-dessous sont hors Studio. La porte P4 reste ouverte.

## Préparer puis envoyer

1. Vérifier l’absence du fichier STOP. Relire GARDE-FOUS et la procédure 05. Attendre la libération des verrous ; prendre le verrou de la place locale et vérifier son identité avant toute écriture. Aucun univers TEST n’est disponible d’après le plan : rester en place locale non publiée. Aucun envoi vers Archipel.
2. Depuis `%USERPROFILE%\Documents\Projets\USINE-ROBLOX`, relancer :

```powershell
powershell -File OUTILS\luau-verif.ps1 JEUX\lave-la-tour\05-production\src
python OUTILS\banc-luau.py JEUX\lave-la-tour\05-production\src --tests JEUX\lave-la-tour\05-production\tests --verbeux
```

3. En mode Edit, pour chaque fichier de la liste suivante, lancer exactement `powershell -File OUTILS\pousser-script.ps1 JEUX\lave-la-tour\05-production\src\<nom>.lua`. La sortie est du Luau, pas un envoi : passer cette sortie à `execute_luau`, vérifier « créé » ou « mis à jour », puis poursuivre. Arrêter au premier échec. Aucun serveur HTTP ni installation nécessaire.

Ordre : `ReplicatedStorage.Jeu.Config`, `ReplicatedStorage.Jeu.Nombres`, `ReplicatedStorage.Jeu.Textes`, `ReplicatedStorage.Jeu.GesteLogique`, puis `ServerScriptService.Jeu.EtatJoueur`, `EconomieService`, `VitresService`, `DonneesService`, `SocialService`, `ContratService`, `CommerceService`, `MesuresService`, `RetoursService`, `ActionsDeTest`, `MondeService` (tous avec le préfixe `ServerScriptService.Jeu.`). Ensuite `StarterPlayer.StarterPlayerScripts.NacelleClient.client`, `InterfaceClient.client`, `EffetsClient.client`, `RetoursClient.client` (tous avec le préfixe `StarterPlayer.StarterPlayerScripts.`). Enfin `ServerScriptService.Jeu.Amorce.server`, après raccordement par son propriétaire. Les attendus de tests ServerStorage ne sont pas nécessaires au jeu.

## Trois lignes de raccordement dans Amorce

Le fichier Amorce appartient à l’autre codeur : aucune modification ici. Les lignes sont préparées contre la version intégrée lue pendant ce travail, avec `V.position`, `destination`, `lieu` et `tour`.

Après les require, avant toute arrivée :
```lua
local Monde = require(script.Parent.MondeService); Monde.construire(); Players.PlayerRemoving:Connect(Monde.liberer_parcelle)
```
Dans `envoyer(j)`, après `if not p then return end` :
```lua
Monde.attribuer_parcelle(j)
```
Dans `envoyer(j)`, après `tour.lieu = lieu`, avant FireClient :
```lua
local visuel = copie(p.tour); visuel.laveurs = {}; local total, paliers = 0, 0; for _, r in p.robots do total += r.en_service; if r.en_service > 0 then paliers += 1 end end; visuel.robots_visibles = math.min(3, total); visuel.r2_visibles = p.robots.r2.en_service; visuel.retard_robots = if total > 0 then math.max(0, 10-paliers) else p.tour.rangees; for _, laveur in Players:GetPlayers() do local cible, endroit = V.position(laveur); if cible == p and endroit == "tour" then table.insert(visuel.laveurs, laveur) end end; Monde.mettre_a_jour(j, visuel)
```

Cette troisième ligne est longue pour fournir littéralement trois lignes ; son propriétaire peut la répartir sans changer le comportement. Elle n’ajoute aucun champ au profil sauvegardé.

**Contrats encore incomplets pour le client social :** Etat ne fournit pas l’identifiant du propriétaire visité ni les propositions sociales et leur cible. NacelleClient accepte `Etat.proprietaire` et InterfaceClient accepte `bouton_contextuel` sous forme de table de disponibilités, `cible_contextuelle` et `nom_contextuel`, mais le serveur lu ne les émet pas. Sans leur raccordement par le propriétaire du serveur, la visite ne cadre pas la bonne tour et les boutons sociaux ne sont pas proposés. Ne pas déclarer le scénario à deux clients validé. Le contrat de base n’indique pas ces champs : les adopter ensemble avant le Play social, sans modifier les Remotes ni leur validation.

**Délai d’attribution :** après une vitre finie, le serveur émet actuellement Etat sans nouvelle attribution ; la boucle suivante attribue la vitre à la seconde suivante. Le client attend l’attribution et respecte 1,55 s à compter de sa réception. Il ne peut donc garantir la reprise pendant les 0,4 s de montée. Le propriétaire d’Amorce doit attribuer la suivante avant l’Etat suivant pour qualifier cette exigence ; le client n’invente jamais un index. Le banc de geste ne prouve pas ce parcours réseau.

## Premier Play et journal

1. Lancer `start_stop_play` en Play, nouveau profil, émulation téléphone 844 × 390. Ne pas donner de pièces ni d’aide au relecteur. Faire apparaître le personnage, vérifier l’assise, la vitre brune, Frotte et la main ; joystick et saut absents. Si erreur console, arrêter et transmettre la trace : aucune qualification.
2. `get_console_output` contient `[PASSE2 Nacelle <secondes>]`, `[PASSE2 Effets <secondes>]`, `[PASSE2 Interface <secondes>]` et `[PASSE2 Monde <secondes>]`. Les horloges client et serveur ne sont pas à soustraire entre elles. Prendre le premier contact client comme repère de geste ; le début de Play client comme repère d’arrivée. Les journaux ne sont actifs qu’avec RunService:IsStudio().
3. `contact rangée:index` puis `premiere_trainee_visible_ms valeur` : mesure sur la première image traitée par RenderStepped après la création locale de la trace. Ce journal mesure le délai de présentation demandé ; **il ne mesure pas le rendu GPU ni l’écran physique**. Confirmer par observation/capture. `passe 1/2/3`, puis `vitre_finie` et `vitre_confirmee` viennent du changement du masque serveur ; une simple fin de trois passes ne déclenche aucun gain ni éclat confirmé.
4. `note 1…8,1`, `rangee`, `palier`, `montee`, `etage`, `rotation_camera_constatee`, `fps` servent au relevé. L’absence de ligne rotation ne remplace pas vingt essais observés. Les fps sont une moyenne par seconde du client, à lire pendant le geste. Les sons vides n’établissent aucune preuve auditive.
5. Essayer dix tapotements puis dix glissements ; vingt contacts sur la vitre et vingt hors vitre. Continuer sans aide jusqu’à 180 s, relever l’étage toutes les cinq secondes et le nombre de confirmations à 60 s. Acheter les robots quand le bouton le permet. Tester un toucher pendant la montée et pendant le recul ; aucun mouvement de caméra pendant le glissement.
6. Rejouer en PC 1920 × 1080, puis deux clients. Capturer chaque état du HUD, liste native ouverte avec leaderstats et deux joueurs ; mesurer la stabilité pendant 30 s avec `OUTILS\luau\stabilite-panneaux.luau`. Capturer les volumes depuis le dessus, le sol, de biais. Les captures restent hors git. Arrêter Play, vérifier la console, puis save_place (sans publication) et rendre le verrou selon la procédure.

## Mesures à remplir — toutes non mesurées

| Mesure | Seuil de la revue passe 2 | Mesuré |
|---|---|---|
| Contact → traînée | ≤ 150 ms sur 20 / 20 vitres | ☐ Non mesuré |
| Tapoter / glisser | 10 / 10 de chaque ; aucune rotation, même hors vitre | ☐ Non mesuré |
| Commandes natives | Joystick et saut absents ; rendus après Descendre | ☐ Non mesuré |
| Rythme à 60 s | ≥ 25 vitres ; prévision 28 | ☐ Non mesuré |
| Première montée | ≤ 20 s ; prévision 14 s | ☐ Non mesuré |
| De 61 à 180 s | ≥ 8 étages nouveaux ; prévision 12 ; zéro baisse | ☐ Non mesuré |
| Retours dans la minute | ≥ 4 retours distincts ; fiente 8 et buée 17 vues avant 45 s | ☐ Non mesuré |
| Robots | ≥ 1 acheté visible au travail dans le cadre à 60 s | ☐ Non mesuré |
| Cadrage | Vitre ≥ 40 % de largeur au téléphone ; biais voisin de 35° ; ville et façade voisine visibles | ☐ Non mesuré |
| Sons | Série de huit crans ; aucune répétition > 3 s sans variation ; poser les sons d’abord | ☐ Non mesuré |
| Fluidité | ≥ 30 images/s au téléphone pendant la traînée | ☐ Non mesuré |
| Durabilité | Aucune vitre lavée resalie pendant 3 min ; reprise fidèle après sortie | ☐ Non mesuré |
| Plaisir, revue | ≥ 7 après 3 min, raisons écrites ; sans humain, note plafonnée à 7 | ☐ Non mesuré |
| Social | Ami rejoint en ≤ 2 touchers et ≤ 20 s ; appuis simultanés cohérents ; duo × 2 ; mousse visible au quota | ☐ Non mesuré |
| Pièces du monde | < 1 500 par client à six joueurs ; calcul ébauche 155 | ☐ Non mesuré en Play |
| HUD | Q4/Q8/Q9/Q11 : deux formats, ≥ 48 px, stabilité 30 s, aucune superposition | ☐ Non mesuré |

## Arrêt ferme — annexe D 2 bis, sans révision des seuils

Au téléphone, **abandon sans nouvelle itération si une seule condition échoue** : latence > 150 ms sur plus d’une vitre sur 20 ; une rotation pendant vingt glissés commencés sur vitre ; moins de 25 vitres à 60 s ou première montée après 20 s sans aide ; moins de huit étages nouveaux entre 61 et 180 s ou baisse du compteur ; plaisir sous 6 pour le relecteur, raisons écrites, ou sous 6 pour le propriétaire après trois minutes s’il joue. La revue demande 20/20 latences et plaisir ≥ 7 pour dépasser sa note de 5 : ces exigences sont plus strictes que les deux seuils d’abandon, ne pas les confondre.

## Preuves hors Studio

Compilation et banc exécutés réellement ; aucune preuve visuelle. Les tests nouveaux vérifient les traductions et le repli, les passes, crans, aspects, priorité, projection sur deux écrans, la construction du monde et ses dimensions. Les tests ne lancent pas les scripts clients. Le remplacement Seat → Part est explicite dans monde.test.luau. Le calcul de cadrage teste un rectangle idéal, sans avatar, arête de tour ni occlusion.

Dernière exécution réelle : les six scripts créés et les trois tests compilent individuellement avec `luau-compile --null` (neuf codes 0). `luau-verif` : **21 fichiers, 0 défaut**, code 0. Banc : **19 fichiers passés, 2825 assertions**, code 0 (hors ligne finale du banc par scénario).

| Test | Assertions passées |
|---|---:|
| annexe-a.test.luau | 275 |
| commerce.test.luau | 24 |
| config.test.luau | 619 |
| contrat.test.luau | 170 |
| donnees.test.luau | 482 |
| economie.test.luau | 154 |
| gabarit-mesures.test.luau | 28 |
| gabarit-retours.test.luau | 20 |
| geste.test.luau | 52 |
| monde.test.luau | 46 |
| rejeu-simulateur.test.luau | 432 |
| remotes.test.luau | 75 |
| revue-d1.test.luau | 1 |
| revue-d2.test.luau | 3 |
| revue-d3.test.luau | 6 |
| social.test.luau | 35 |
| suivi.test.luau | 34 |
| textes.test.luau | 150 |
| vitres.test.luau | 219 |

Les trois tests écrits ici totalisent 248 assertions. Ces sorties ne qualifient ni le client réel ni P4. Les autres fichiers du dépôt bougent simultanément sous leurs propriétaires ; aucune modification de ces fichiers par ce codeur.

## Constantes à remonter dans Config

Monde : étage 5 unités ; côtés 35/55/75 ; place 150 ; rayon des parcelles 110 ; six parcelles ; épaisseurs de socle 6 et dessous 4 ; trois robots décoratifs ; montée 0,4 s. Les dimensions de chaque pièce sont détaillées dans MONDE.md.

Geste/caméra : biais 35°, élévation 8°, FOV vertical 50°, cible de largeur 44 %, tolérance de tapotement 12 px et 0,35 s ; recul 2 s ; marge réseau client de durée minimale 1,55 s et reprise d’envoi 0,5 s. Les trois passes et 1,5 s minimales restent les règles du serveur déjà dans Config.

Effets : réserve de 32 traces (0,35 s), 12 éclats (0,6 s), trois pigeons locaux (2 s), huit crans avec pause de 3 s ; séquence de fanfare à pas de 0,15 s ; mousse visuelle renouvelée 1,1 s. Ces nombres bornent le rendu, sans décision de gain.

## Premier Play réel — 17 novembre 2026 (orchestrateur, Opus 5.5)

Place locale non publiée `Place1` (PlaceId 0, Studio connecté en Archipel_MCP), jamais Archipel. Envoi des 21 scripts par `python OUTILS\pousser-studio.py lave-la-tour` (verrou `studio`, contrôle d'identité de la place). Écran ordinateur, pas d'émulation téléphone.

**Défauts vus en jeu et corrigés (commit 03138b6)** :
1. Place jamais publiée : `GetDataStore` lève « You must publish this place to the web to access DataStore » et `Amorce` s'arrêtait à la ligne 7 (aucun Remote créé, tous les clients en attente infinie). Correction : `MagasinSur` (magasin en mémoire en Studio seulement, erreur remontée hors Studio), test `magasin-sur.test.luau`.
2. `PlayerModule` absent des PlayerScripts dans cette place : `NacelleClient` restait bloqué sur `WaitForChild`. Correction : attente de 5 s puis repli `ContextActionService` (déplacement et saut avalés).

**Vu après correction** : monde construit (`construction 14`), HUD, vitre brune, « Frotte ! », « Robot 10 », « Objectif : Robot ventouse », « Idée / bug », « Descendre » ; 60 images/s ; un glissé = une passe, trois passes → `vitre_finie` côté client puis `vitre_confirmee` par le serveur ; pièces créditées (2 pièces après 2 vitres).

**Mesures (gestes Windows natifs réguliers, ≈ 0,35 s par glissé : borne haute, pas un joueur humain)** :

| Mesure | Seuil | Mesuré | Statut |
|---|---|---|---|
| Contact → traînée | ≤ 150 ms | `premiere_trainee_visible_ms 0` à chaque contact (première image après création locale ; ne mesure ni GPU ni écran) | indicatif |
| Rythme | ≥ 25 vitres à 60 s | 30 vitres confirmées en 49 s de fenêtre lisible (≈ 36/min) | passe (robot) |
| Montées | ≥ 8 étages de 61 à 180 s | une montée toutes les 8 s (étages 17 → 23 en 49 s), soit ≈ 15 par 120 s | passe (robot) |
| Pièces du monde | < 1 500 par client | 37 à un joueur | passe |
| Fluidité | ≥ 30 images/s | 59–60 images/s sur ordinateur | passe (ordinateur seulement) |

**Constats ouverts, non corrigés** :
- Aucune `leaderstats` côté serveur : la liste native des joueurs n'affiche pas l'étage ni les pièces (exigence du tableau HUD).
- La caméra n'est pas fixe d'une vitre à l'autre (l'avatar entre dans le cadre à gauche après la première vitre) : à vérifier contre « aucune rotation pendant le glissé » au téléphone.
- Les panneaux du HUD couvrent une partie de la vitre ; rendu en blocs gris (maquette).
- La console Studio est tronquée au-delà d'environ 500 lignes : les mesures longues se lisent par compteurs en jeu, pas par la console.
- Non fait : émulation téléphone 844 × 390, deux clients, plaisir jugé par un relecteur, sons (vides), robots achetés et visibles.

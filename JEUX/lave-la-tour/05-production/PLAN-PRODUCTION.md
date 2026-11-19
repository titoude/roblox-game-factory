# Plan de production — Lave la tour (`lave-la-tour`)

Version 2 du 2026-11-16, écrite par l'orchestrateur d'après la fiche **v5.1** (`02-concept\FICHE-CONCEPT.md`, commit `4f5c17f`), `03-economie\economie.json`, `03-economie\RAPPORT-ECONOMIE-contre-verification-4.md` (scénarios Q01 à Q08) et `04-fun\RAPPORT-FUN-V5.md` (mesures de la passe 2). Remplace le plan provisoire du cycle 1, qui décrivait le prototype de la v3 (défaut N01 de la contre-vérification n° 4).

Portes : P2 et P3 en dérogation (`ETAT.json`). **La porte qui décide est P4** : prototype joué, arrêt ferme de l'annexe D 2 bis de la fiche.

## 1. Conditions de départ

| Condition | État au 2026-11-16 | Conséquence |
|---|---|---|
| Fiche et `economie.json` figés | Oui, commit `4f5c17f` | Toute divergence se corrige dans le code, ou se signale |
| Studio, bureau | **Verrouillés** par l'agent `archipel-finition` | Tout ce qui suit se fait **hors Studio** : code dans `src\`, preuves par `OUTILS\banc-luau.py`. Les preuves « en Play » de chaque lot sont préparées et marquées « à exécuter quand le verrou est libre » |
| Univers TEST | Aucun (le propriétaire n'en a pas créé) | Place locale non publiée le moment venu ; publication : procédure 07 |
| Binaires Luau | Posés dans `OUTILS\bin\` | `luau-verif.ps1` et le banc tournent |
| Un seul jeu en production | Archipel est en QA ; le propriétaire a demandé d'avancer `lave-la-tour` sans Studio (16/11/2026) | Aucun conflit : pas de place, pas d'écrivain Studio |

## 2. Lots

« Hors Studio » = prouvé par le banc (logique serveur réellement exécutée). « En Play » = à voir dans Studio, impossible aujourd'hui.

| Lot | Contenu | Scripts (`src\`) | Preuve hors Studio | Preuve en Play (verrou libre) |
|---|---|---|---|---|
| L0 | Prototype de 0 à 180 s : tour 1, lavage (3 passes, rangée de 5, montée), pièces, robots r1 et r2, raclette large, caméra de biais et saisie tactile, une seconde place | `Config`, `Textes`, `EtatJoueur`, `EconomieService`, `VitresService`, `Amorce`, `NacelleClient`, `InterfaceClient`, `EffetsClient` | Banc : scénario de l'annexe A rejoué à la seconde (vitre k à 4 + 2k s, achats à 25, 41 et 56 s, 28 vitres à 60 s, 88 à 180 s, 12 étages nouveaux de 61 à 180 s) ; compilation et analyse des trois scripts clients | **Porte P4** : mesures de la passe 2 (`04-fun\RAPPORT-FUN-V5.md`, tableau « Axe 2 »), 0 erreur console, captures téléphone et PC, arrêt ferme si une mesure échoue |
| L1 | Économie complète : 10 robots, 5 améliorations, chantiers, jalons, prix entiers, gain indexé sur R, budget de 40 vitres par minute, plafond de solde, objectif suivant | `EconomieService`, `Config`, `Nombres` | Banc : `Config` identique à `economie.json` (comparaison champ par champ) ; **rejeu des 105 achats du simulateur** : mêmes prix, mêmes instants à 3 s près, fin de contenu à 97:09 ± 5 s ; prix du 10ᵉ r10 exact ; solde au-delà de 2³¹ ; revue d'économie passe 2 sur le commit | Constantes relues en jeu par action de test |
| L2 | Sauvegarde sûre et hors ligne : verrou de session, reprises, sauvegarde périodique, à la sortie et à la fermeture, version de schéma, chargement en échec sans écrasement ; réservoir 2 h à 50 % crédité une fois | `DonneesService` | Banc : quitter et revenir (état identique, masque compris) ; quitter en plein chantier ; fermeture du serveur ; panne au chargement (aucune sauvegarde vide) ; panne à l'écriture puis reprise ; deux serveurs pour un compte ; absences de 0, 1, 7 199, 7 200 et 7 201 s ; crédit hors ligne rejoué | DataStore réel en TEST privé (niveau C) |
| L3 | Tours : déménagement, tour étincelante, pigeons, Flèche (accès, segments, record), objectif et bouton contextuel | `VitresService`, `EconomieService` | Banc : stock jamais vide plus de 10 s ; pigeons annulés par chaque cas de la fiche ; déménagement rejoué sans double effet ; Flèche refusée sans les 100 robots et les 5 améliorations ; prix des segments exacts ; deux segments non finis au plus ; M12 | Scène de déménagement, lisibilité des tours |
| L4 | Social : seconde place, attribution des vitres à deux, mousse et quota de bonus, pourboire et prorata, « Rejoindre », « Chez <visiteur> ! », M11, M13 | `SocialService` | Banc à 2 et 3 joueurs fictifs : jamais la même vitre pour deux laveurs ; quotas par jour et par partenaire ; mousse visible après le quota (drapeau envoyé au client) ; prorata exact ; propriétaire qui part | Niveau B : deux clients (porte P5) |
| L5 | Contrat du jour : 40 vitres, 600 × R, jour UTC, M13 | `ContratService` | Banc : une prime par jour UTC, minuit en cours de contrat, R lu à la dernière vitre | Trajet de la nacelle |
| L6 | Boutique : cinq passes à identifiant 0 masquées, raclette motorisée par le chemin du lavage manuel, chantiers express | `CommerceService` | Banc : aucune offre visible à 0 ; auto + manuel ≤ 40 par minute ; express ne saute aucun déblocage ; passe relue à la connexion | Achat de test en Studio |
| L7 | Monde : tours de 120, 280 et 400 étages en deux panneaux par façade, robots animés (retard de 10 − paliers), place, bornes, pigeons, sons | `MondeClient`, `MONDE.md` | Compilation ; nombre de pièces calculé | Captures de dessus, du sol, de biais (Q10) ; moins de 1 500 pièces mesurées |
| L8 | Interface : plan d'écran de la fiche, téléphone et PC, textes anglais et français | `InterfaceClient`, `Textes` | Banc : chaque clé de texte existe dans les deux langues | Q8, Q9 (`stabilite-panneaux.luau`), Q11 |
| L9 | Suivi et retours : `MesuresService` (entonnoir : arrivee, premiere_action, premier_achat, min_3, min_10), `RetoursService`, actions de test, nettoyage | gabarits de `OUTILS\GABARITS\luau\` | Tests Luau des gabarits sur la copie du jeu ; étapes d'entonnoir comptées une fois | Bouton « Idée / bug » vu en jeu |

Ordre : L1 et L0 (serveur) d'abord, puis L2, L3, L4, L5, L6, L9 ; L7 et L8 demandent Studio pour leur preuve.

## 3. Contrat d'interface (tous les agents codeurs s'y tiennent)

### 3.1 Fichiers et propriétaires

| Fichier de `src\` | Rôle | Lot |
|---|---|---|
| `ReplicatedStorage.Jeu.Config.lua` | Toutes les constantes (mêmes noms et valeurs que `economie.json`, plus § 4) ; aucune logique | L1 |
| `ReplicatedStorage.Jeu.Nombres.lua` | Affichage abrégé (k, M, Md, Bn…), séparateurs français et anglais | L1 |
| `ReplicatedStorage.Jeu.Textes.lua` | Table des chaînes `en` et `fr`, fonction `t(langue, cle, ...)` | L8 (ébauche au L0) |
| `ServerScriptService.Jeu.EtatJoueur.lua` | Schéma du profil : `nouveau()`, `valider(profil)`, `migrer(profil)` ; fonctions pures | L1 |
| `ServerScriptService.Jeu.EconomieService.lua` | Fonctions pures sur un profil : prix, achats, chantiers, revenu R, gain d'une vitre, avance du temps, hors ligne, objectif suivant, Flèche | L1, L3 |
| `ServerScriptService.Jeu.VitresService.lua` | État des tours, validation du lavage, budget, rangées, pigeons, déménagement | L0, L3 |
| `ServerScriptService.Jeu.DonneesService.lua` | Chargement, sauvegarde, verrou de session, hors ligne au retour | L2 |
| `ServerScriptService.Jeu.SocialService.lua`, `ContratService.lua`, `CommerceService.lua` | L4, L5, L6 | |
| `ServerScriptService.Jeu.MesuresService.lua`, `RetoursService.lua` | Copies des gabarits de l'usine | L9 |
| `ServerScriptService.Jeu.ActionsDeTest.lua` | Actions réservées à `RunService:IsStudio()` | L0 à L9 |
| `ServerScriptService.Jeu.Amorce.server.lua` | Crée les Remotes, relie les services, boucle de temps (1 s) | L0 |
| `StarterPlayer.StarterPlayerScripts.NacelleClient.client.lua` | Caméra tenue de biais, saisie (glisser et tapoter), envoi des vitres finies | L0 |
| `StarterPlayer.StarterPlayerScripts.InterfaceClient.client.lua` | Plan d'écran de la fiche | L0, L8 |
| `StarterPlayer.StarterPlayerScripts.EffetsClient.client.lua` | Traînée, éclat, note qui monte, rideau d'eau | L0 |

Tests du banc : `JEUX\lave-la-tour\05-production\tests\<sujet>.test.luau`, lancés par `python OUTILS\banc-luau.py JEUX\lave-la-tour\05-production\src --tests JEUX\lave-la-tour\05-production\tests` (et par `verifier-usine.ps1`).

### 3.2 Profil d'un joueur (ce qui est sauvegardé)

```lua
{
  version = 1,                       -- version de schéma
  pieces = 0,                        -- nombre, plafonné à Config.PLAFOND_SOLDE
  robots = { r1 = {achetes = 0, en_service = 0, chantiers = {}} , ... },  -- chantiers : liste d'instants de fin (temps de jeu cumulé, s)
  ameliorations = { a1 = false, ... },
  temps_jeu = 0,                     -- secondes de jeu cumulées (horloge des chantiers)
  tour = { numero = 1, rangees = 0, masque = 0, etincelante = false,
           pigeons = nil },          -- pigeons : {cycle, premiere_rangee, rangees = 0, masque = 0} ou nil
  tours_finies = 0,
  fleche = { segments_achetes = 0, segments_laves = 0 },  -- numero = 4 quand elle est ouverte
  contrat = { jour = "", vitres = 0, masque = 0, prime_recue = false },
  quotas = { jour = "", mousse_s = 0, mousse_par = {}, pourboires_min = 0, pourboires_par = {} },  -- clés : userId en chaîne
  depart = 0,                        -- os.time() de la dernière sortie (0 = jamais)
  operations = {},                   -- identifiants des opérations déjà appliquées (déménagement, segment, hors ligne), bornés à 50
  mesures = { premier_jour = "", dernier_jour_actif = "", retour_j1_compte = false, retour_j7_compte = false, etapes = {} },
  passes = {},                       -- relues à chaque connexion, jamais source de vérité
}
```

Rien d'autre n'est sauvegardé. Tout champ absent est remis à sa valeur de `nouveau()` par `valider`. Les nombres sont des flottants double précision ; un prix est un entier exact (`math.ceil` sur le produit calculé depuis le coût du premier, jamais depuis le prix précédent).

### 3.3 Remotes (dossier `ReplicatedStorage.JeuRemotes`, créés par `Amorce`)

| Nom | Sens | Arguments | Validation serveur |
|---|---|---|---|
| `VitreFinie` (RemoteEvent) | client → serveur | `rangee` (entier), `index` (1 à 5) | Type et bornes ; le joueur est assis sur cette tour ; la vitre est celle que le serveur lui a attribuée, encore sale ; 1,5 s au moins depuis son attribution ; budget de 40 par 60 s glissantes. Refus silencieux sinon (aucun gain, aucun message d'erreur exploitable) |
| `Acheter` (RemoteEvent) | client → serveur | `genre` (`"robot"`, `"amelioration"`, `"segment"`), `id` (chaîne) | Débloqué, maximum, solde ; 5 demandes par seconde au plus |
| `Action` (RemoteEvent) | client → serveur | `nom` (`"demenager"`, `"contrat"`, `"descendre"`, `"monter"`, `"rejoindre"`, `"chez_visiteur"`, `"retour"`), `cible` (userId ou nil) | Selon l'état ; 2 demandes par seconde au plus |
| `Etat` (RemoteEvent) | serveur → client | Table : `pieces`, `revenu`, `robots`, `ameliorations`, `tour` (numéro, étages, rangées, masque, vitre attribuée), `objectif`, `bouton_achat`, `bouton_contextuel`, `mousse`, `message` | Envoyé à l'arrivée, après chaque changement, et une fois par seconde |
| `Effet` (RemoteEvent) | serveur → clients | `nom` (`"rangee"`, `"palier"`, `"mousse"`, `"pigeons"`, `"etincelante"`, `"achat"`), `userId`, détails | Décor seulement |

Le client ne décide ni d'un gain, ni d'un prix, ni d'un achat (P5).

### 3.4 Fonctions que les services s'offrent entre eux

- `EconomieService.revenu(profil) -> R` ; `.gain_vitre(profil) -> nombre` ; `.prix_robot(id, n) -> entier` ; `.acheter_robot(profil, id) -> ok, raison` ; `.acheter_amelioration(profil, id)` ; `.avancer(profil, secondes)` (revenus, chantiers, plafond) ; `.crediter(profil, montant)` ; `.hors_ligne(profil, secondes) -> credit` ; `.objectif(profil) -> {texte_cle, cible, reste}` ; `.fleche_ouverte(profil) -> bool` ; `.prix_segment(n) -> entier` ; `.acheter_segment(profil, id_operation)`.
- `VitresService.attribuer(profil, laveur) -> rangee, index` ; `.finir_vitre(profil, laveur, rangee, index, maintenant) -> ok, gain_du_laveur` ; `.stock(profil) -> entier` ; `.demenager(profil, id_operation)` ; `.pigeons(profil)`.
- `DonneesService.charger(joueur) -> profil ou nil, raison` ; `.sauver(joueur)` ; `.profil(joueur)`.

Chaque service est un ModuleScript sans effet au chargement ; ses dépendances (horloge, DataStoreService) sont injectables pour le banc.

## 4. Constantes absentes de `economie.json` (dans `Config`)

| Constante | Valeur | Origine dans la fiche v5.1 |
|---|---|---|
| Vitres par rangée, rangées par étage | 5, 1 | § 3 |
| Étages des tours 1, 2, 3 | 120, 280, 400 | § 3 bis |
| Passes par vitre, durée minimale d'une vitre | 3, 1,5 s | M01 |
| Budget de lavage | 40 vitres par 60 s glissantes | M01 |
| Raclette motorisée | 1 vitre par 2 s | M05 |
| Pigeons | stock à zéro pendant 10 s dans la nacelle : 20 étages, 100 vitres | § 3 bis |
| Déménagement | scène de 20 s, sans crédit | § 3 bis |
| Flèche | accès : 100 robots en service et 5 améliorations ; segment de 40 étages (200 vitres) ; prix `ceil(60 × min(4 + n, 9) × 300 757 992 117)` ; 2 segments non finis au plus ; premier segment au 401ᵉ étage | § 3 bis, M12 |
| Hors ligne | 50 % de R, 7 200 s au plus, R au départ | § 3 bis |
| Contrat du jour | 40 vitres, 600 × R, ouvert à r3 ≥ 1, jour UTC | § 3 bis |
| Mousse | × 1,25 sur le gain de l'action, fenêtre de 10 s, bonus : 600 s par jour dont 300 par partenaire | M06 |
| Pourboire | 50 % du gain du propriétaire, sans mousse ; 10 min de R par jour dont 5 par joueur ; plancher R = 1 ; prorata au bord | M02, M10 |
| Plafond de solde | 9 × 10¹⁵ | M09 |
| Retard des robots sur les autres façades | 10 − nombre de paliers possédés, en étages | M07 |
| Joueurs par serveur | 6 (réglage de l'expérience : release) | § 4 |
| Vitres d'aspect différent | 8ᵉ : fiente, 17ᵉ : buée, puis une sur dix selon le numéro | § 3 |

## 5. Actions de test (réservées à Studio et au banc, règle P6)

`studioPieces(n)`, `studioAvance(secondes)`, `studioPalier(id, n)`, `studioTour(numero, rangees)`, `studioAbsence(secondes)`, `studioJourSuivant()`, `studioJoueurFictif()`, `studioQuota(nom, valeur)`, `studioEtincelante()`. Chacune refuse d'agir quand `RunService:IsStudio()` est faux : c'est un test du banc.

## 6. Ce que la QA devra rejouer

Les 8 scénarios Q01 à Q08 de `RAPPORT-ECONOMIE-contre-verification-4.md` § 5 (deux de gravité P0 : état d'une tour à deux laveurs avec déconnexion ; opérations rejouées autour d'une panne de sauvegarde), les 5 scénarios de `RAPPORT-FUN-V5.md`, et le plan minimal de la procédure 06 (scénarios 1 à 15). Tout ce que le banc couvre est marqué « exécuté hors Studio », jamais « vu en jeu » (G15).

## 7. Risques

| Risque | Ce qui le lève | Lot |
|---|---|---|
| Le geste ennuie ; la caméra tactile tourne ; le rythme réel est sous 25 vitres par minute | Passe 2 sur le prototype, arrêt ferme | L0, en Play |
| Le code client (caméra, saisie) n'a jamais tourné | Premier Play | L0, en Play |
| `pousser-script.ps1` et `execute_luau` jamais essayés par l'usine | Premier envoi | L0, en Play |
| Tours de 2 000 unités : rendu, brouillard, lecture au téléphone | Mesure | L7, en Play |
| Le banc ne reproduit ni les limites ni les latences réelles des DataStore | TEST privé, niveau C | L2 |

## 8. Estimation

| Mesure | Prévu | Réel (au bilan) |
|---|---|---|
| Lots | 10 | |
| Lots dont la logique est prouvable hors Studio | 8 (L0 serveur, L1 à L6, L9) | |
| Sessions en Studio nécessaires ensuite | 6 à 8 (L0 client, L7, L8, puis preuves en Play de chaque lot) | |

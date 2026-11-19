# Banc Luau hors Studio
Le banc exécute réellement les sources serveur avec le binaire officiel Luau.
Il vérifie les assertions écrites par le test, pas toutes les règles du jeu automatiquement.
Il prouve les transitions d'économie, validations, quotas, reprises et achats testés.
Il ne prouve ni rendu, ni physique, ni réplication réelle, ni comportement du client.
Il ne qualifie pas les limites, latences, budgets ou conflits réels des DataStores.
Ce résultat complète les preuves Studio ; il ne valide pas les portes G15, P5 ou la QA B/C.
Commande : `python OUTILS/banc-luau.py JEUX/slug/05-production/src --tests chemin/tests`.
Options : `--filtre motif` (nom glob ou sous-chaîne), `--verbeux` (assertions et sorties).
Chaque `*.test.luau` s'exécute isolément ; limite réelle : 20 secondes par processus.
Codes : 0 tout passe ; 1 échec ; 2 luau.exe absent ; 5 dossier introuvable.
Sources : noms Roblox avec suffixe `.lua`, `.server.lua` ou `.client.lua`.
Les modules sont chargés une fois ; un cycle de require provoque une erreur explicite.
Les Scripts démarrent avec `banc.demarrer_serveur()` ; les LocalScripts restent inactifs.
Exemple de fichier `economie.test.luau` :
```lua
banc.demarrer_serveur()
local j = banc.joueur(12, "Alice", {LocaleId="fr-fr"})
local service = banc.require("ServerScriptService.Jeu.EconomieService")
banc.avancer(60)
banc.verifier(service ~= nil, "service chargé")
```
Assertions : `verifier`, `egal`, `proche(a,b,tolerance)`, `erreur_attendue(f,motif)`.
Arbre : `instance(chemin)`, Instance.new, parents, enfants, Clone, Destroy, attributs, signaux.
Classes : Folder, scripts, Remotes, Bindables, valeurs, Part, Model, Sound, GUI courants.
Joueurs : `joueur`, `quitter`, Kick ; `fermer_serveur` déclenche BindToClose.
Client fictif : `banc.client(j):envoyer(remote,...)`, `:invoquer(remoteFunction,...)`, `:messages(remote)`.
Temps : task, wait, tick, time, os.time/clock/date UTC, DateTime.now ; Heartbeat/Stepped à 60 Hz.
Une erreur asynchrone échoue avec sa trace ; appeler avancer pour exécuter les tâches dues.
DataStoreService : Get/Set/Update/Remove/IncrementAsync, OrderedDataStore et pages triées.
`banc.datastore(nom[,scope,ordonne])` : lire, pannes(N), panne_permanente(bool), compteurs(), userIds(clé).
HttpService : JSONEncode/Decode, GUID déterministes ; valeurs JSON limitées à 4 Mio par écriture.
MarketplaceService : passes via `banc.passe(j,id,bool)`, prompts enregistrés dans `.prompts`.
`banc.recu(j,productId,purchaseId)` appelle ProcessReceipt ; réutiliser purchaseId pour rejouer.
Analytics : événements via `banc.analytics()` ; Messaging et badges enregistrés dans leurs services.
CollectionService, LocalizationService, TextService neutre, TweenService à complétion différée.
Vector2/3, CFrame matriciel, Color3, UDim/2, TweenInfo, NumberRange, Random, Enum, typeof.
Limites : null JSON devient nil ; tween sans interpolation ; objets monde/UI sans moteur Roblox.
Ajouter une API dans faux-roblox.luau avec erreur explicite hors périmètre et scénario d'auto-test.
Vérifier : `luau-compile.exe --null OUTILS/luau/faux-roblox.luau`, puis `python OUTILS/test-banc-luau.py`.
Globales standard Luau accessibles aux modules et tests, dont métatables, fonctions raw et newproxy ; math.random reste déterministe.

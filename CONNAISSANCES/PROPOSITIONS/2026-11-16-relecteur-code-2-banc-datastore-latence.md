# Proposition : le faux DataStore du banc doit simuler la latence et le budget

Source : revue `REVUE-CODE-8702805.md` (`lave-la-tour`), constats S1 à S3.

## Constat

Le faux DataStore de `OUTILS/luau/faux-roblox.luau` répond tout de suite et sans limite. Un serveur qui écrit à chaque vitre et bloque tout le serveur pendant l'écriture passe donc au banc, alors qu'en ligne il perd les vitres des autres joueurs (démontré dès qu'on ajoute `task.wait(0.3)`) et dépasse le budget de 60 + 10 × n écritures par minute dès 3 joueurs.

## Proposition

1. Ajouter des options au banc :
   - `banc.datastore(...):latence(s)`, qui fait attendre `UpdateAsync`, `GetAsync` et `SetAsync` ;
   - un compteur de budget par minute et par clé, qui produit une erreur au-delà de la limite.
2. Ajouter une règle de production (proposée en P15) : « Aucune action de jeu n'attend une écriture DataStore, sauf un reçu Robux (E8). Une écriture périodique, de sortie ou de fermeture qui échoue est réessayée et n'expulse jamais le joueur tant que le verrou lui appartient. »
3. Ajouter au relecteur de code deux mutations obligatoires de sauvegarde : retirer le contrôle de validité à l'écriture, et retirer le nouvel essai de l'écriture de sortie. Chacune doit faire échouer un test.

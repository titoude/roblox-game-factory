# Revue de code — `lave-la-tour`, commit `f07996f`

- Date : 2026-11-16. Rôle : 05.relecteur-code et passe 2 de la revue d'économie (règle E10). Relecteur : Claude Opus 5.5 ; auteur du code : Codex `gpt-6.1-sol` (A2 respectée).
- Objet : `JEUX/lave-la-tour/05-production/src/` (Config, Nombres, EtatJoueur, EconomieService, VitresService, ActionsDeTest, Amorce, Attendus), `tests/` (6 tests, `generer-attendus.py`), `JOURNAL-LOTS.md`, **lus uniquement par `git archive f07996f`**, jamais dans la copie de travail.
- Référence : fiche v5.1 (§ 3, 3 bis, 3 ter M01 à M13, annexe A), `economie.json`, `PLAN-PRODUCTION.md` (§ 3 et § 4), contre-vérification 4 (Q01 à Q08).
- Méthode : copie figée hors dépôt (`git archive f07996f JEUX/lave-la-tour OUTILS | tar -x`, binaires Luau copiés de `OUTILS\bin`), banc relancé, 7 tests jetables et 4 mutations du code dans le dossier temporaire. Aucun fichier du dépôt modifié en dehors de ce rapport et de la proposition de leçon.
- Tout ce qui suit est « exécuté hors Studio » ou « lu ». Rien n'est « vu en jeu » (G15).

## Verdict

| | |
|---|---|
| P0 certains | **0** |
| P1 certains | **3** (D1, D2, D3) |
| P2 certains | 5 (D4 à D8) |
| P3 | 14 |
| (a) Passe 2 de l'économie | **Oui** : constantes et formules du code = fiche v5.1 et `economie.json` |
| (b) Base des lots suivants | **Oui après corrections** : D1, D2, D3 avant L4 et la Flèche ; D4 et D5 avant L2 ; tests D6 et D7 renforcés |

## 1. Faits (exécuté hors Studio, lu)

### 1.1 Le banc annoncé est reproduit

`python -I OUTILS/banc-luau.py <copie>/src --tests <copie>/tests --verbeux` : code 0, 6 fichiers PASSE, 1 786 lignes `PASSE` = 6 lignes de fichier + 6 « scénario terminé » + **1 774 assertions**. Le chiffre du journal est exact.

`generer-attendus.py` relancé sur la copie : `Attendus.lua` régénéré identique au commit, à une ligne près : le `--!nocheck` d'en-tête a été ajouté à la main (le fichier dit « ne pas éditer »). Les attendus viennent bien de `economie.json` et du simulateur (`Decimal`, `ROUND_CEILING`), pas du code testé.

### 1.2 Ce qui est juste (vérifié)

- **Constantes** : les 10 robots, 5 améliorations, jalons, offres, `apres_contenu` et `stock_vitres` de `Config` = `economie.json` champ par champ (`config.test.luau`, comparaison depuis le JSON). Constantes du plan § 4 relues une par une dans `Config.lua:158-193` : 5 vitres par rangée, 120/280/400 étages, 3 passes, 1,5 s, 40 vitres par 60 s, 2 s (raclette motorisée), pigeons 10 s / 20 étages, déménagement 20 s, Flèche (100, 5, 40, 200, 2, 401, 4, 9), hors ligne 0,5 / 7 200 s, contrat 40 / 600, mousse 1,25 / 10 / 600 / 300, pourboire 0,5 / 10 / 5 / 1, plafond 9 × 10¹⁵, retard 10, 6 joueurs : **toutes identiques**.
- **Prix** : `EconomieService.lua:32-54`, produit décimal exact chiffre par chiffre puis arrondi supérieur, depuis le coût du premier (M09). Les 100 prix = `Decimal` du générateur ; 10ᵉ r10 = 7 931 566 754 660. Le simulateur utilise la même règle (`sim-economie.py`, `cout_gen`).
- **Gain d'une vitre** : `EconomieService.lua:29-31` = raclette × (1 × multiplicateurs « tout » + 0,2 × R). **R** (`:24-28`) : robots en service × revenu × multiplicateur de cible, puis × « tout », chaque amélioration une seule fois ; R final = 300 757 992 117,1875.
- **Segment** : `:111-114` = `ceil(60 × min(4 + n, 9) × 300 757 992 117)` ; 1ᵉʳ = 90 227 397 635 100, 5ᵉ = 162 409 315 743 180 (fiche § 3 bis).
- **Machine d'état d'un robot (M04)** : achat → chantier → en service, une seule mise en service (`:58-65`) ; déblocages, jalons et accès à la Flèche ne lisent que `en_service`. Test jetable `r4` : Flèche refusée à 99 robots en service ou à 4 améliorations, acceptée à 100 + 5.
- **Hors ligne** (`:97-105`) : 50 % de R au départ, 7 200 s au plus, les chantiers continuent, un robot mis en service pendant l'absence ne compte qu'au retour.
- **Anti-triche, lavage** : test jetable `r7` par le Remote : vitre d'un autre index, rangée suivante, index non entier, rangée en chaîne : refusées ; vraie vitre acceptée une fois ; rejeu refusé ; client parfait pendant 120 s → 80 vitres (40 par minute pile). Arguments NaN, infinis, négatifs, tables : refusés (`VitresService.lua:107`, `Amorce:61,74`). Joueur descendu : refusé. Erreurs internes avalées par `pcall` (`Amorce:44`), rien ne remonte au client.
- **Actions de test** : toutes gardées par `RunService:IsStudio()` (`ActionsDeTest.lua:9-50`), aucun Remote n'y mène ; inertes avec `banc.studio(false)` (`remotes.test.luau`).
- **Sauvegarde** : test jetable `r6` : un profil riche (chantiers, pigeons, quotas indexés par userId en chaîne, opérations, passes) passe par le DataStore simulé (encodeur JSON strict : pas de clés mixtes, pas de tableau creux, pas de NaN) puis `valider` : **147 champs identiques**. Le profil du § 3.2 est sérialisable tel quel ; l'état d'exécution (attributions, budget, scène) reste hors du profil.
- **Nombres** : soldes plafonnés à 9 × 10¹⁵ < 2⁵³ (`:55-57`) ; prix et segments sont des entiers exacts en double.

## 2. Défauts certains

### D1 — P1, certain (test `r1`) : une vitre réservée et abandonnée bloque la tour sans fin

`VitresService.lua:81-90` : une attribution n'expire jamais. Un visiteur qui prend la vitre 1 puis ne lave plus : le propriétaire lave 2 à 5, puis `attribuer` lui rend `nil`. Dix minutes plus tard, stock = 596, aucun pigeon possible (stock non nul), tour bloquée au premier étage. Q01 demande explicitement « libérer une réservation abandonnée ». Atteignable dès que L4 raccorde la seconde place.

Correction minimale (`attribuer`, boucle des index) :

```lua
local RESERVATION_MAX_S = 10  -- à mettre dans Config
for id, a in r.attributions do
    if id ~= laveur.UserId and a.zone == zone and a.rangee == rangee and a.index == i then
        if horloge() - a.debut <= RESERVATION_MAX_S then libre = false else r.attributions[id] = nil end
    end
end
```

Le laveur dépossédé voit `finir_vitre` refusé (attribution absente) et en reçoit une nouvelle au tour suivant.

### D2 — P1, certain (test `r2`) : deux visiteurs peuvent exclure le propriétaire de sa tour

`VitresService.lua:45-54` compte les occupants sans distinguer le propriétaire. A part aider B ; C puis D montent chez A (acceptés, trois laveurs potentiels) ; A ne peut plus rentrer chez lui. M07 : « deux laveurs au plus : le propriétaire et l'occupant de la seconde place ».

Correction minimale :

```lua
if lieu == "tour" and p ~= c.profil then
    for _, autre in comptes do
        if autre ~= c and autre.tour == p and autre.profil ~= p and autre.lieu == "tour" then return false end
    end
end
```

Le propriétaire passe toujours ; une seule seconde place.

### D3 — P1, certain (test `r3`) : à l'arrivée sur la Flèche, aucune vitre sale pendant plusieurs minutes

`VitresService.lua:134` refuse les pigeons si `V.hauteur(p) < 20` ; sur la Flèche, la hauteur vaut 40 × segments achetés, donc 0 à l'arrivée. Le déménagement 3 → 4 (`:144-155`, atteignable par `Action("demenager")` dès que la Flèche est ouverte) pose une tour de 0 vitre. Le premier segment coûte 9,02 × 10¹³ ; au solde quasi nul de la fin du contenu, il se finance en 3 min 51 s (profil actif, fiche § 3 bis). Mesure : stock à 0 et aucun pigeon 4 minutes après l'arrivée. Écart avec la fiche § 3 bis : « le stock ne manque jamais plus de 10 secondes » ; et la règle de la Flèche (« pigeons si tous les segments achetés sont propres […] sur 20 étages déjà lavés ») vaut aussi à zéro segment : les étages 381 à 400 de la tour 3 sont lavés.

Correction minimale : juger la hauteur absolue, aux deux endroits.

```lua
-- VitresService.lua:134
local sommet = (if p.tour.numero == 4 then 400 else 0) + V.hauteur(p)
if not present or V.stock(p) > 0 or sommet < 20 then V.annuler(p); return false end
-- EtatJoueur.lua:60 : même condition sur le sommet absolu, sinon la zone 381-400 disparaît au rechargement
```

`premiere_rangee` vaut alors 381 et `zone_active` sait déjà la servir. Si l'orchestrateur préfère une autre réponse (déménagement vers la Flèche proposé seulement quand le premier segment est finançable), c'est une décision de fiche, pas de code : à trancher avant L3 en Play.

### D4 — P2, certain (test `r5`) : la boucle d'une seconde n'est pas protégée

`Amorce.server.lua:101-113` : `avancer`, `pigeons`, `attribuer` et `envoyer` de tous les profils tournent dans un seul thread, sans `pcall`. Un seul profil incohérent (`tour.numero = 9`, posé par l'action de test) lève `VitresService.lua:15: attempt to index nil with 'etages'` dans la boucle. En Roblox, le thread meurt : plus aucun revenu, aucun état envoyé, aucun pigeon **pour tous les joueurs du serveur**. Je n'ai trouvé aucun chemin client qui produise un tel profil dans ce commit ; il suffira d'un défaut de L2 (chargement) ou de L4. À corriger avant L2.

```lua
for j, p in profils do
    local ok, err = pcall(function()
        E.avancer(p, maintenant - precedent)
        if V.pigeons(p) then remotes.Effet:FireClient(j, "pigeons", j.UserId, {}) end
        V.attribuer(p, j); envoyer(j)
    end)
    if not ok then warn("[Jeu] boucle, joueur " .. j.UserId .. " : " .. tostring(err)) end
end
```

### D5 — P2, certain (lecture) : `Etat.valider` remplace en silence un profil illisible par un profil neuf

`EtatJoueur.lua:103-106` : `pcall(valider)` et, en cas d'erreur, `Etat.nouveau()`. DonneesService (L2) ne pourra pas distinguer « profil neuf » de « profil illisible » et sauvegardera le profil vide par-dessus la vraie sauvegarde : c'est la perte de données que le plan interdit (« chargement en échec sans écrasement »). Je n'ai pas trouvé d'entrée JSON qui fasse lever `valider` aujourd'hui ; le risque est dans le contrat.

```lua
function Etat.valider(profil)
    local ok, resultat = pcall(valider, profil)
    if ok then return resultat end
    return nil, "profil_invalide : " .. tostring(resultat)
end
```

DonneesService refuse alors la session sans rien écrire.

### D6 — P2, certain (mutations) : le rejeu des 105 achats prouve la suffisance du solde, pas l'égalité

`rejeu-simulateur.test.luau` achète aux instants du simulateur et exige que l'achat passe. Il ne compare jamais le solde à celui du simulateur. Mutations sur la copie : **gain d'une vitre × 2** → rejeu PASSE ; **revenu des robots × 1,5** → rejeu PASSE (seul `annexe-a` échoue, au solde de 41 s). Un code trop généreux passe donc le rejeu. De plus :

- `:23` : `banc.proche(t, 5829, 5)` est tautologique : `t` vaut `attendu.fin_s`, qui vient du simulateur ; la « fin de contenu à 97:09 ± 5 s » du plan (L1) n'est pas prouvée pour le code.
- `:13` (« provision ») est redondant avec l'achat qui suit.
- L'égalité des **prix** est prouvée, indirectement (rang par rang, via `economie.test.luau`).

Correction : dans `generer-attendus.py`, relever `sim.cash` juste après chaque `acheter` (enveloppe de la méthode publique) et, dans le test, `banc.proche(p.pieces, attendu.solde_apres, 1e-6 * math.max(1, attendu.solde_apres))` après chaque achat ; puis vérifier que l'achat suivant **échoue** une seconde avant son instant quand le simulateur n'avait pas l'argent (preuve de non-avance).

### D7 — P2, certain (mutations) : trois assertions passent quel que soit le code

- `remotes.test.luau:28` « deux actions par seconde » : mutation cadence `Action` 2 → 100, toujours PASSE ; `demenager` est refusé de toute façon (tour 2 non prête) et `monter` est déjà rejeté par la cadence consommée par les 20 `descendre`.
- `vitres.test.luau:79` « rejeu déménagement » : mutation sans `E.operation` dans `demenager`, toujours PASSE (tour 3 non prête et blocage de 20 s).
- `rejeu-simulateur.test.luau:23` (D6).

Manquent aussi : réservation abandonnée (D1), propriétaire exclu (D2), Flèche à zéro segment (D3), boucle (D4), solde exact (D6), aller-retour JSON (fait ici, `r6`), vitres forgées par le Remote (fait ici, `r7`), « stock jamais vide plus de 10 s » annoncé par le journal pour L3 mais non testé.

### D8 — P2, certain (lecture) : une partie des constantes est écrite en dur, et `Config` porte deux copies non recoupées

Les valeurs sont justes, mais ne viennent pas de `Config` : `5` (vitres par rangée, `VitresService.lua:24,25,81`), `20` et `19` (pigeons, `:25,70,123,134,140`, `EtatJoueur.lua:60-65`), `400`/`401` (`VitresService.lua:71,140`, `Amorce:28-29`, `EconomieService.lua:129`), `40` (`VitresService.lua:122`, `EtatJoueur.lua:54`), `2` laveurs (`VitresService.lua:50`), `600`, `300`, `10`, `5`, `40` (`EtatJoueur.lua:79-87`). `C.VITRES_PAR_RANGEE`, `C.PIGEONS_ETAGES`, `C.FLECHE.ETAGE_DEBUT`, `C.FLECHE.VITRES_SEGMENT`, `stock_vitres.laveurs_max_par_tour` ne sont lus nulle part. Les constantes en capitales ne sont recoupées ni avec `stock_vitres`/`apres_contenu` ni avec le plan, sauf 8 d'entre elles comparées à des littéraux (`config.test.luau:11`). Une correction de la fiche ne se propagerait pas : deux vérités. Correction : remplacer les littéraux par les noms de `Config` et ajouter au test la comparaison des capitales avec les champs de `economie.json` qui portent la même valeur.

## 3. Détails (P3)

| # | Où | Constat | Statut |
|---|---|---|---|
| P3-1 | `Nombres.lua:5` | « Bn » = 10¹² ; juste en français (billion), faux en anglais (1e12 = trillion, « Bn » se lit 10⁹). P11 | certain |
| P3-2 | `Amorce:54-57` | `Effet` part en `FireClient` au seul joueur ; le plan dit « serveur → clients », et la tour étincelante est « visible de tout le serveur » | certain, à raccorder en L7 |
| P3-3 | `Amorce:82` | `assis[j] = true` même quand `V.asseoir` refuse | certain, sans effet en L0 |
| P3-4 | `Amorce:44` | `pcall` muet : une erreur interne disparaît aussi des journaux du serveur ; ajouter `warn` | certain |
| P3-5 | `Amorce:77` | Identifiant de déménagement tiré au hasard à chaque appui : l'identifiant ne protège rien ; seul le blocage de 20 s empêche le double appui. Plus sûr : `"demenager:" .. p.tour.numero` | certain |
| P3-6 | `EconomieService.lua:102` | `hors_ligne` ajoute `secondes` à `temps_jeu` sans borne ; si `temps_jeu` dépassait ~9,007 × 10¹⁵ (2⁵³), `avancer` (`:88`) ne progresserait plus et bouclerait. Inatteignable avec `valider` (borne 9 × 10¹⁵) ; borner `secondes` dans `hors_ligne` | certain, inatteignable aujourd'hui |
| P3-7 | `EtatJoueur.lua:44` | Fin de chantier relue sans borne haute : une valeur aberrante fige un robot ; borner à `temps_jeu + chantier_s` | certain |
| P3-8 | `Amorce:102-111` | Un joueur arrivé entre deux tours de boucle reçoit jusqu'à 1 s de revenu de trop (`precedent` commun) | certain, négligeable |
| P3-9 | `VitresService.lua:138` | Pigeons au tour de boucle suivant : 10 à 11 s de stock vide au lieu de 10 | certain |
| P3-10 | `VitresService.lua:130-142` | Pigeons même quand la tour suivante est prête ; la fiche les place dans le cas « avant que la tour suivante soit prête ». Sans dommage ; à trancher | à vérifier en jeu |
| P3-11 | `src/ServerStorage.Tests.Attendus.lua` | 1 126 lignes de données de test dans `src\` : `pousser-script.ps1` les enverrait dans la place. `--!nocheck` ajouté à la main, perdu à la prochaine génération | certain |
| P3-12 | tous les modules | `--!nocheck` partout : `luau-analyze` ne vérifie plus les types ; « 0 défaut » ne prouve que la syntaxe et les globales | certain |
| P3-13 | `JOURNAL-LOTS.md` | Colonne « Commit : Aucun (instruction) » alors que le lot est le commit `f07996f` ; « fins de contenu exactement celles demandées » s'appuie sur l'assertion tautologique de D6 | certain |
| P3-14 | `VitresService.lua:39-43` | Budget de 40 par minute gardé en mémoire du serveur : un changement de serveur le remet à zéro (déjà noté au journal) | à vérifier en jeu |

## 4. Réponses aux questions de la mission

1. **Écarts avec la fiche, `economie.json` et le plan** : aucune constante ni formule fausse. Écarts d'état : D1, D2 (tour à deux laveurs), D3 (Flèche à zéro segment), P3-9, P3-10. Annulations des pigeons (descendre, déconnexion, déménagement, segment) : conformes ; le contrat relève de L5. Déménagement : visiteur ramené, lavage arrêté 20 s, rien de remis à zéro, aucun crédit de scène : conforme. Budget de 40 vitres par minute : conforme, compte par compte, toutes tours confondues (`r7` : 80 vitres en 120 s).
2. **Argent et triche** : aucun chemin trouvé vers une pièce, un achat, une vitre ou un étage indus (arguments forgés, rafales, rejeu, ordre, NaN, infinis, négatifs, tables, joueur descendu, vitre d'un autre). Aucune fuite d'erreur. Actions de test inatteignables hors Studio.
3. **Robustesse** : D4 (boucle commune), D5 (profil illisible) ; mémoire libérée à la sortie (`comptes`, `tours`, `profils`, `cadences`, `assis` ; `budgets` purgé à l'arrivée suivante, borné par les joueurs vus en 60 s) ; 2⁵³ : soldes et prix sous la borne, P3-6 ; `time()` est monotone sur Roblox : un saut en avant (serveur figé) est rattrapé seconde par seconde, sans perte ni double compte ; un retour en arrière est ignoré (`avancer` refuse les durées négatives).
4. **Tests** : D6, D7. Le rejeu prouve **la suffisance du solde et l'égalité des prix, pas l'égalité du solde ni la date de fin**.
5. **Lots suivants** : profil sérialisable tel quel (`r6`) ; DonneesService dépend de D5 et doit remettre `depart` à zéro avec le crédit (M08) : `hors_ligne` ne le fait pas, et `depart = 0` veut dire « jamais » (ne pas calculer `os.time() - 0`). Deux laveurs : D1, D2, et la boucle ne réattribue une vitre qu'au propriétaire sur sa propre tour (`Amorce:109`) : L4 devra le faire pour le visiteur. Contrat : `consommer_budget` est prêt.
6. **Lisibilité** : lisible par un autre agent, noms français clairs, découpage par service conforme au plan. Trois lignes sont trop denses pour être relues sans effort (`Amorce:31`, `EtatJoueur.lua:62`, `EconomieService.lua:151`) et les nombres magiques de D8 sont le vrai coût de maintenance. Pas de réécriture demandée au-delà de D8.

## 5. Tests jetables de la revue (à reprendre par le codeur)

Dossier temporaire hors dépôt, lancés par `banc-luau.py <copie>/src --tests <dossier>` : `r1` réservation abandonnée, `r2` propriétaire exclu, `r3` Flèche sans stock, `r4` accès Flèche à 99/4, `r5` boucle commune, `r6` aller-retour JSON, `r7` vitres forgées et rafale. Tous PASSE : ils démontrent les défauts D1 à D4, et r4, r6, r7 confirment ce qui est juste. Le cœur de `r1`, pour reprise :

```lua
local p, q = S.nouveau(), S.nouveau(); local a, b = {UserId = 1}, {UserId = 2}
V.inscrire(a, p); V.inscrire(b, q); V.asseoir(b, p, "tour"); V.attribuer(p, b)
for n = 1, 4 do local r, i = V.attribuer(p, a); temps += 1.5; V.finir_vitre(p, a, r, i, temps) end
temps += 600
banc.verifier(V.attribuer(p, a) ~= nil, "le propriétaire reçoit une vitre")   -- échoue sur f07996f
```

Mutations jouées : gain × 2 et revenu × 1,5 (rejeu PASSE), cadence `Action` 100 (`remotes` PASSE), déménagement sans identifiant (`vitres` PASSE).

## 6. Avis

- **(a) Passe 2 de l'économie : oui.** Les constantes et les formules du code (prix exacts, gain indexé, R composé une fois, hors ligne, segments, budget, durées, plafond) sont celles de la fiche v5.1 et de `economie.json`. Réserves hors constantes : D3 (état de la Flèche) et D8 (littéraux non reliés à `Config`).
- **(b) Base des lots suivants : oui après corrections listées.** D1, D2 et D3 avant de raccorder la seconde place (L4) et la Flèche en Play ; D4 et D5 avant L2 ; D6 et D7 pour que le banc détecte un code trop généreux. Une contre-vérification de ces corrections par un agent qui ne les a pas écrites (E11).

RESULTAT: ok | JEUX\lave-la-tour\05-production\REVUE-CODE-f07996f.md | 0 P0 et 3 P1 certains ; (a) oui ; (b) oui après corrections D1 à D7

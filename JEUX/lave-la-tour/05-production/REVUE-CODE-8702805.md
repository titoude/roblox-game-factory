# Revue de code — `lave-la-tour`, commit `8702805`

Relecteur : rôle 05.relecteur-code, en contre-vérification (E11 : n'a écrit ni le code ni les corrections). Date : 2026-11-16. Revue partielle, faite en environ 25 minutes et centrée d'abord sur la sauvegarde et l'argent. Copie figée extraite par `git archive 8702805`, hors dépôt. Tout ce qui suit a été **exécuté hors Studio** (banc) ou lu, et **rien n'a été vu en jeu** (G15).

## Verdict

| Mesure | Valeur |
|---|---|
| Banc du commit | 22 fichiers, tous PASSE sur la copie figée |
| P0 certains | 0 |
| P0 à vérifier en jeu | 1 (S2) |
| P1 certains | 3 (S1, S3, S4) |
| P1 à vérifier en jeu | 1 (S5) |
| P2 certains | 4 (S6 à S9) |
| Mutations jouées | 28 : 24 détectées, 4 survivantes (M6 et M19 sans effet réel ; M21, M22 et D5 sont des trous de test) |
| Porte P4 (prototype en Play) | **Oui, après S2 et S3** |
| Porte P5 (QA à deux clients) | **Oui, après S1 à S5** et une mesure du budget DataStore en Play |

## 1. Sauvegarde

Ce qui est juste (vérifié par lecture et par le banc) :
- le transformateur d'`UpdateAsync` est pur sur `ancien` : le rappeler plusieurs fois ou rejouer après une réponse perdue ne crédite pas deux fois le hors ligne (test `donnees` « réponse perdue », relu) ;
- le crédit hors ligne et la remise à zéro de `depart` se font dans la même écriture (M08) ;
- un serveur qui a perdu le verrou ne réécrit pas (M18 détectée) ;
- un verrou vivant n'est jamais volé (M17 détectée), et un verrou mort est repris après 600 s ;
- un `JobId` vide est remplacé par un GUID ;
- un profil illisible ou une migration nulle provoquent un refus, jamais un profil neuf écrit par-dessus (D5b détectée) ;
- les valeurs non finies et les tableaux à trous sont refusés ;
- `ProcessReceipt` ne valide rien (aucun produit consommable : E8 n'est pas en jeu en v1).

### S1 — P1, certain (test jetable `j1`) : une écriture en cours fait perdre les vitres de tous les autres joueurs

`Amorce.executer` (lignes 70 à 91 du fichier) met `occupe=true`, puis appelle `Donnees.sauver` (un `UpdateAsync` qui attend la réponse) pour chaque profil modifié, **à chaque action confirmée**. Tant que cette écriture dure, toute action d'un autre joueur est rejetée sans message (`if occupe ... return false`). La boucle d'une seconde saute aussi son tour.

Démonstration : avec une latence d'écriture de 0,3 s, A et B finissent chacun une vitre dans la même image. Résultat : A gagne 1, **B gagne 0 et son masque reste à 0**. La vitre de B est perdue et le client n'en est pas informé.

Plus il y a de joueurs, plus le serveur devient séquentiel. Cela casse la promesse des deux laveurs (§ 3 bis) et la cadence de 40 vitres par minute.

### S2 — P0, à vérifier en jeu (calcul sur les limites publiées par Roblox) : une écriture DataStore par vitre

Chaque vitre, achat ou action produit au moins un `UpdateAsync`, deux s'il y a un pourboire, plus une action toutes les 2 s avec la raclette motorisée.
- Calcul : 40 vitres par minute et par joueur, contre un budget d'écriture de 60 + 10 × n par minute pour le serveur. Le budget est dépassé dès 3 joueurs actifs.
- La limite par clé (une écriture environ toutes les 6 s dans la documentation Roblox, à confirmer) est dépassée par un joueur seul.
- Enchaînement : requêtes mises en file, attentes de plusieurs secondes, et `occupe` bloque tout le serveur (S1) ; quand la file est pleine, trois échecs, puis expulsion et perte (S3).

Correction minimale pour S1 et S2 :
- retirer `Donnees.sauver` et `occupe` d'`executer` : l'état serveur en mémoire fait foi ;
- marquer le profil « à écrire » et l'écrire toutes les 60 s environ, à la sortie et à la fermeture ;
- garder l'écriture immédiate pour un futur reçu Robux seulement (E8).

Il faut ensuite mesurer en Play le nombre d'écritures par minute.

### S3 — P1, certain (test jetable `j2`) : trois échecs d'écriture font expulser le joueur et jettent sa progression en mémoire

`DonneesService.sauver` (ligne 100 du fichier) : `if not valeur and not sortie then profils[j] = nil; j:Kick(...)`. Une panne de DataStore de quelques secondes (3 essais, attentes de 1 s puis 2 s) pendant une écriture périodique ou une action entraîne :
- l'expulsion du joueur ;
- l'abandon du profil en mémoire ;
- un échec de l'écriture de sortie, puisque le profil n'est plus là.

Démonstration : la mémoire indique 23,25 pièces, le magasin 0, et le verrou reste à `banc-0001`. Le joueur est donc aussi bloqué jusqu'à 10 minutes sur tout autre serveur.

Correction : dans le transformateur, distinguer « verrou perdu » (`perdu = true` quand `ancien.session.id ~= serveur`) d'une panne. Sur une panne, garder le profil et réessayer au cycle suivant. N'expulser que si le verrou est perdu.

### S4 — P1, certain (test jetable `j3`) : l'écriture de sortie n'est jamais réessayée

Si les trois essais de `sauver(j, true)` échouent, rien ne réessaie avant `BindToClose`. Les gains depuis la dernière écriture périodique sont perdus si le joueur revient ailleurs, et le verrou reste en place.

Démonstration : panne de 3 essais au départ, 60 s après une écriture périodique. Le magasin indique 22,5, la mémoire 38,75 ; **16,25 pièces sont perdues** et le verrou n'est pas libéré.

Correction : en cas d'échec de sortie, relancer avec des attentes de 4, 8, 16 et 32 s tant que le verrou nous appartient, puis laisser `fermer()` reprendre la main.

### S5 — P1, à vérifier en jeu : expulsion immédiate quand le verrou d'un autre serveur est vivant

`charger` expulse dès le premier refus. Lors d'un changement de serveur, d'une téléportation ou d'un retour rapide, l'écriture de sortie de l'ancien serveur arrive souvent après le `PlayerAdded` du nouveau : le joueur est expulsé avec `donnees_indisponibles`.

Correction : si le verrou d'un autre serveur est vivant, attendre et réessayer, par exemple 6 fois toutes les 5 s, avant d'expulser.

### Autres points de sauvegarde

- **P2, à vérifier** : un même joueur qui revient sur le même serveur pendant l'écriture de sortie peut voir celle-ci libérer le verrou de sa nouvelle session (même identifiant de serveur), puis être expulsé à l'écriture suivante.
- **P2, lecture** : la boucle d'une seconde parcourt `profils` alors qu'`executer` attend une écriture (raclette motorisée). Un `PlayerAdded` ou un `PlayerRemoving` modifie la table pendant ce parcours. Ce point disparaît avec la correction de S1.
- **P3** : en Studio, chaque Play prend un nouveau GUID. Après un arrêt brutal, le magasin `_studio` est verrouillé 10 minutes.

## 2. Corrections D1 à D5

| Défaut | Correction présente | Test qui la défend | Mutation (retirer la correction) |
|---|---|---|---|
| D1 réservation abandonnée | oui (`RESERVATION_MAX_S`) | `revue-d1` | détectée (`revue-d1`) |
| D2 deux visiteurs | oui (`asseoir`) | `revue-d2` | détectée |
| D3 Flèche sans stock | oui (sommet + 400) | `revue-d3` | détectée |
| D4 boucle commune | oui (`pcall` et expulsion isolée) | `revue-d4` | détectée |
| D5 profil illisible remplacé par un neuf | oui dans le code (`EtatJoueur.valider` renvoie nil) | `donnees` imite `migrer` | **survit** pour `Etat.valider` (S8) ; détectée pour `migration nil` |

Effets de bord : D4 expulse le joueur dont le profil est incohérent. C'est voulu, mais combiné à S3, le profil en mémoire est aussi jeté. Aucune régression n'est observée par ailleurs (22 fichiers PASSE).

## 3. Argent et triche dans les nouveaux services

Ce qui est conforme (lu et testé) :
- **Pourboire M10** : 50 % du gain par vitre du propriétaire, 10 min de revenu par jour dont 5 au plus par donneur, prorata au bord du quota (M8 et M9 détectées). Deux comptes qui alternent rapportent au plus 10 min par jour au propriétaire : c'est le plafond voulu. Le pourboire est créé, il n'est retiré à personne : aucun doublement par une transaction coupée.
- **Mousse** : 600 s par jour dont 300 par partenaire, temps compté découpé à minuit UTC, compteur remis à zéro au changement de partenaire (M10 et M11 détectées).
- **Contrat** : prime de 600 × R une seule fois (`prime_recue` et opération `contrat:<jour>`) ; budget commun (M12, M13 et M14 détectées) ; M13 (visiteur ramené) testé dans `social`.
- **Passes** : l'identifiant 0 est inactif (M16 détectée) ; toutes les offres valent 0 en v1. La raclette passe par `V.finir_vitre`, donc par le budget commun de 40 par minute et une action toutes les 2 s (M5 et M15 détectées).
- **Remotes** : types et bornes de `cible` (entier de 1 à 9e15), `id` de 32 caractères au plus, cadence de 5, 5 et 2 par seconde (M4 détectée) ; les erreurs sont capturées par `pcall` et rien n'est renvoyé au client.

Points relevés :
- **P3** : un contrat commencé un jour et fini le lendemain garde ses vitres et paie la prime du lendemain. C'est sans gain anormal, mais le libellé « contrat du jour » est à confirmer avec la fiche.
- **P3** : la validation de type d'`Acheter` est redondante, car les services refusent déjà (M6 survit sans faille exploitable).

## 4. Ce que le codeur dit avoir laissé

| Point | Confirmé | Gravité réelle en ligne | Avant la bêta ? |
|---|---|---|---|
| D6 : le rejeu contre le simulateur ne compare pas les soldes | **oui** : M1 (gain × 2) et M2 (revenu × 1,5) ne font pas échouer `rejeu-simulateur` ; seuls `economie`, `annexe-a` et d'autres échouent | P2 : aucun effet joueur, mais la règle P14 n'est pas tenue | oui (règle P14) |
| D7 : assertions faibles | partiellement (S8, S9 ci-dessous) | P2 | oui pour S9 |
| D8 : littéraux en dur (`40`, `600`, `300`, `5`, `10`, `0.25` dans `EtatJoueur`, `SocialService`, `ContratService`) | oui par lecture | P2 : une modification de `Config` désynchronise la validation, ce qui peut rendre le profil impossible à sauvegarder | peut attendre, mais pas une modification de ces constantes |
| Pas de transaction entre deux profils | oui | P3 : seuls des gains créés sont concernés (pourboire, quota) ; rien n'est retiré à l'autre compte, donc aucun doublement possible | peut attendre |
| Budget de lavage non durable entre serveurs | oui | P3 : changer de serveur rend au plus 40 vitres par saut, et S5 freine déjà ces sauts | peut attendre |
| Opérations limitées à 50, en file | oui | P2 pour l'avenir : `executer` ajoute `action:<GUID>` à chaque action, donc un identifiant tombe de la file au bout d'environ 50 vitres. C'est sans risque aujourd'hui, mais **inutilisable pour des reçus Robux** (E8) | à résoudre avant le premier produit consommable |

## 5. Mutations (P14)

Script : `outils/muter.py` dans le dossier temporaire. Pour chaque mutation, une copie de `src` est faite, puis le banc complet est lancé.

| Mutation | Résultat |
|---|---|
| M1 gain d'une vitre × 2 | détectée : annexe-a, donnees, economie, social, vitres |
| M2 revenu × 1,5 | détectée : annexe-a, contrat, donnees, economie, social |
| M3 durée minimale de vitre retirée (validation de Remote) | détectée : vitres |
| M4 cadence des Remotes retirée | détectée : remotes |
| M5 budget de 40 par minute retiré | détectée : commerce, contrat, vitres |
| M6 validation de type d'`Acheter` retirée | **survit** (redondante, P3) |
| M7 hors ligne × 2 | détectée : donnees, economie |
| M8 à M11 pourboire et mousse | détectées : social |
| M12 à M14 contrat | détectées : contrat |
| M15 raclette sans pas de 2 s ; M16 passe d'identifiant 0 | détectées |
| M17, M18, M20, D5b sauvegarde | détectées : donnees |
| M19 garde d'absence retirée | **survit** (garde redondante : le transformateur est pur ; P3) |
| M21 contrôle `D.valide` retiré à l'écriture | **survit** : S9 |
| M22 « sauver avant de confirmer » retiré | **survit** : S9 (et S1 demande justement de retirer ce mécanisme) |
| D1 à D4 corrections retirées | détectées : revue-d1 à revue-d4 |
| D5 `Etat.valider` qui renvoie un profil neuf | **survit** : S8 |

- **S6 — P2, certain** : D6 tient toujours (voir § 4).
- **S7 — P2, certain** : il n'existe aucun test de propriété « tout profil atteint en jeu satisfait `D.valide` ». Un seul champ hors des bornes en dur de `EtatJoueur` (D8) rend la sauvegarde silencieusement impossible : `sauver` renvoie `false` sans expulser ni prévenir. Correction : un test de parcours (vitres, achats, duo, contrat, déménagement) qui vérifie `D.valide` après chaque pas, et un journal d'erreur quand `D.valide` échoue.
- **S8 — P2, certain** : aucun test ne défend D5 dans `Etat.valider`. Correction : un test qui force une erreur dans `valider` (par exemple `profil.tour = setmetatable({}, {__index = error})`) et attend nil.
- **S9 — P2, certain** : M21 et M22 survivent. Correction : un test qui insère un NaN, constate que `sauver` renvoie `false` et que le magasin est intact ; le test de M22 deviendra inutile une fois S1 corrigé.

## 6. Avis

- **Porte P4, prototype en Play avec un client : oui, après S2 et S3.** Un joueur seul atteint déjà la limite par clé avec une écriture par vitre, et une panne de DataStore l'expulse en jetant sa progression.
- **Porte P5, QA à deux clients : oui, après S1 à S5.** Le banc doit montrer qu'une vitre de B n'est plus perdue pendant une écriture de A (`j1` inversé), qu'une panne de 3 essais n'expulse plus (`j2`), qu'une sortie en échec est réessayée (`j3`), et qu'un verrou vivant est attendu avant toute expulsion. Ensuite, une contre-vérification E11.
- D6 et S7 à S9 avant la bêta ; D8, les opérations limitées à 50 et le budget entre serveurs avant le premier produit Robux ou une modification des constantes.

## Annexe : tests jetables (hors dépôt, à reprendre par le codeur)

- `j1-occupe` : enveloppe `DataStoreService.GetDataStore` avec `task.wait(0.3)` dans `UpdateAsync`, puis A et B envoient `VitreFinie` dans la même image : `gain A 1, gain B 0, masque B 0`.
- `j2-panne-periodique` : un robot r1, 85 s, `store:pannes(3)`, 10 s : expulsion `donnees_indisponibles`, magasin 0 contre 23,25 en mémoire, verrou conservé.
- `j3-sortie-echec` : une écriture périodique, 60 s, `pannes(3)`, sortie, 400 s : magasin 22,5 contre 38,75 en mémoire, verrou conservé.

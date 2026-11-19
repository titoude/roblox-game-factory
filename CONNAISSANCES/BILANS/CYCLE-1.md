# Bilan du cycle 1 de l'usine — 15 et 16/11/2026

Premier passage réel de la chaîne, sans Studio, sans navigateur, sans contrôle du bureau, sans publication ni dépense.
Rédigé par l'orchestrateur (Claude Fable 5.2, effort high). Durée : environ 1 h 30 (22:09 à 23:40 UTC à l'horloge de la machine).

**En une phrase** : la chaîne a tourné de la veille au plan de production du jeu n° 2, `lave-la-tour` ; elle a cassé à cinq endroits, tous corrigés dans l'usine ; le jeu est arrêté à la revue du fun, qui attend un relecteur indépendant.

## 1. Ce qui a tourné

| Étape | Ce qui a été fait | Livrables | Porte |
|---|---|---|---|
| 00 Ouverture | `verifier-usine.ps1`, `etat.ps1`, `orchestrator_capabilities` | — | — |
| 01 Veille, tour 1 | 3 veilleurs Haiku délégués (aucune page lue), puis 9 pages lues par l'orchestrateur via un lecteur Haiku, 1 appel à l'API documentée | `VEILLE\RELEVES\2026-11-15\` (5 fichiers), `TENDANCES.md`, `IDEES-CANDIDATES.md`, `instantanes.csv` | P0 en **dérogation** |
| 02 Concept | 3 pistes notées, fiche complète, versions 1, 2 et 3 | `JEUX\lave-la-tour\02-concept\FICHE-CONCEPT.md` | P1 **passe** |
| 03 Économie | 4 agents `gpt-6.1-sol` xhigh : calcul, adversaire, deux contre-vérifications | `03-economie\` : `economie.json`, `SIMULATION.md`, 4 rapports, rapport fusionné | P2 : 2 **échecs**, puis **dérogation** au 3ᵉ passage |
| 04 Fun | Revue rédigée par l'orchestrateur, auteur de la fiche | `04-fun\RAPPORT-FUN.md` : ITÉRER, 6,1/10 | P3 **à confirmer** |
| 05 Production | Plan seulement | `05-production\PLAN-PRODUCTION.md`, provisoire | non commencée |

État final : `lave-la-tour | 04-fun | bloqué`. Archipel inchangé (06-qa).

### Délégations

| Agent | Modèle, effort | Nombre | Durée de chacun | Résultat |
|---|---|---|---|---|
| Veilleur | Haiku 5.5, high, `delegate_task` | 3 | 3 à 4 min | 2 échecs, 1 relevé d'extraits de recherche |
| Lecteur de page | Haiku, agent natif `web-fetch` | 9 appels | 10 à 70 s | 7 pages utiles (RoStats), 2 pages vides |
| Vérificateur d'économie | `gpt-6.1-sol`, xhigh, `delegate_task` | 4 | 10 à 20 min | 4 rapports exploitables, 4 propositions de leçon |
| Opus, Fable, Sonnet | — | 0 | — | Interdits cette nuit ; l'orchestrateur a joué le concepteur et le relecteur fun |

`delegate_task` fonctionne depuis une session qui est elle-même une tâche déléguée. La fin de chaque agent réveille l'orchestrateur ; aucun sondage n'a été nécessaire.

### Ce que la veille a trouvé (détail dans `VEILLE\TENDANCES.md`)

- Throw Food For Animals : 12 532 joueurs de moyenne en octobre, 202 898 en novembre (14 jours), créé le 18/09, 174 mises à jour en 30 jours.
- Steal An Egg recule deux mois de suite (−26,1 %, −36,9 %) ; +1 Speed Keyboard Escape est passé de 168 437 à 29 701 en deux mois.
- Dans le genre Simulation, chaque montée du mois porte un geste différent ; les reprises directes d'un geste restent à 0,2 % et 0,3 % de l'original.

## 2. Ce qui a cassé

| # | Où | Ce qui s'est passé | Preuve |
|---|---|---|---|
| C1 | Veille | **Un Haiku délégué n'a pas d'outil de lecture de page**, seulement la recherche web. Les trois veilleurs ont rendu 0 page lue. La procédure ne connaissait que trois modes de navigation, tous interdits cette nuit | `v1-roblox-charts.md`, `v2-classement-mensuel.md`, `v4-contexte.md` |
| C2 | Veille | **Roblox Charts est illisible sans navigateur** (classement chargé par script). Couverture de la mission A sur sa source : 0 % | `v5-orchestrateur-rostats.md` |
| C3 | Veille | **Plafond de recherches dépassé** : 15 recherches pour 10 permises par session. L'orchestrateur avait donné un budget à chaque veilleur sans répartir le plafond commun. Erreur d'orchestration | `v5-orchestrateur-rostats.md` § Remarques |
| C4 | Veille | Le lecteur a rendu les 100 lignes d'une page alors que 10 étaient attendues : la demande ne plafonnait pas le nombre de lignes | idem |
| C5 | Économie | **Le simulateur ne jugeait le remboursement que sur le premier exemplaire.** Sur la fiche v1, il affichait « aucun défaut » alors que 29 achats sur 100 dépassaient 5 minutes (jusqu'à 13 min 23 s). L'exemple d'économie livré avec l'usine échouait lui-même (35 sur 100) | `RAPPORT-ECONOMIE-calcul.md` D2, `RAPPORT-ECONOMIE-adversaire.md` A01 |
| C6 | Économie | **Aucun contrôle ne voyait qu'un joueur immobile progressait autant qu'un joueur actif** (1,1 % d'écart entre les deux profils) | `RAPPORT-ECONOMIE-adversaire.md` A02 |
| C7 | Économie | **La correction de C5 contenait elle-même un défaut** (revenu ajouté par un robot sans le supplément de lavage), trouvé une heure plus tard par le contre-vérificateur ; puis un arrondi flottant (6 prix faux d'une pièce) | `RAPPORT-ECONOMIE-contre-verification-1.md` N01, `-2.md` N05 |
| C8 | Économie | **Deux règles se contredisent** : A5 (deux échecs à une porte de conception, l'idée est abandonnée) et E11 (contre-vérifier jusqu'à ce qu'une passe ne trouve plus rien). Après deux échecs, `etat.ps1` a conseillé l'arrêt d'un jeu dont la cadence passait | `JEUX\lave-la-tour\ETAT.json`, historique |
| C9 | Fun | **Aucun relecteur indépendant n'était permis.** L'auteur de la fiche a relu sa fiche ; `etat.ps1` ne savait enregistrer qu'un passe, un échec ou une dérogation | `04-fun\RAPPORT-FUN.md` |
| C10 | Chaîne | Le **plan de production** demandé n'existait dans aucune procédure ; la porte **P0** n'existait pas dans `etat.ps1` ; `etat.ps1 -Seuils` affichait `System.Object[]` pour une liste | — |
| C11 | Chaîne | Les rapports d'économie ont trouvé **9 décisions manquantes** dans une fiche que la porte P1 avait déclarée complète : P1 ne vérifie que la présence des rubriques | `RAPPORT-ECONOMIE-adversaire.md` M01–M09 |

Ce qui n'a pas cassé : les crochets git (rôles et secrets), `nouveau-jeu.ps1`, `instantane-univers.ps1` (premier appel réel, 4 univers), l'écriture sûre, les prompts types d'économie (les quatre agents ont rendu le bon fichier au bon endroit avec la dernière ligne attendue).

## 3. Ce qui est corrigé

| # | Correction | Fichiers | Vérifié comment |
|---|---|---|---|
| C1, C2, C4 | Mode « lecture sans navigateur » ; la lecture de page se fait par l'orchestrateur via l'agent `web-fetch` en Haiku ; ce qui se lit (RoStats) et ne se lit pas ; lignes plafonnées | `PROCEDURES\01`, `SOURCES-VEILLE.md`, `MODELES-ET-QUOTAS.md`, gabarit du relevé, skill de veille | 7 pages RoStats lues ainsi pendant le cycle |
| C3 | Plafonds de session répartis entre veilleurs avant le lancement, part écrite dans chaque prompt | `PROCEDURES\01` | Non rejoué (une session par jour) |
| C5, C6, C7 | Simulateur : remboursement de chaque exemplaire au prix payé, revenu ajouté complet, option `part_revenu_s`, alerte de retard du joueur lent, prix entiers exacts, attente finale, fin non atteinte, profils au même délai | `OUTILS\sim-economie.py`, `OUTILS\test-sim-economie.py`, `OUTILS\GABARITS\economie.exemple.json` | 17 contrôles automatiques, lancés par `verifier-usine.ps1` ; chiffres recoupés à la main par deux agents indépendants |
| C5, C6 | Règle E3 précisée ; règles E14 (poids du geste) et E15 (quota et revenu de référence) ; clé `economie.retard_lent_min_pct` | `REGLES.md`, `seuils.json` (version 2), `SEUILS-PORTES.md` | — |
| C8 | Non corrigé pendant le jeu (règle A4). Dérogation écrite dans `ETAT.json` ; question posée au propriétaire (§ 7) | — | — |
| C9 | Résultat `a_confirmer` et remise à zéro motivée d'un compteur dans `etat.ps1` ; règle A8 ; mode dégradé écrit dans la procédure 04 et dans les replis | `OUTILS\etat.ps1`, `PROCEDURES\04`, `PROCEDURES\00`, `MODELES-ET-QUOTAS.md` | Utilisé sur `lave-la-tour` |
| C10 | Gabarit et étape « plan de production » ; porte P0 dans `etat.ps1` ; affichage des listes | `OUTILS\GABARITS\PLAN-PRODUCTION.md`, `nouveau-jeu.ps1`, `PROCEDURES\00`, `05` | `nouveau-jeu.ps1` rejoué pour créer `lave-la-tour` |
| C11 | Gabarit du rapport d'économie : section « Décisions manquantes », cadence « non évaluée » pour l'adversaire, risques en jeu comptés à part ; prompt de contre-vérification | `OUTILS\GABARITS\RAPPORT-ECONOMIE.md`, `PROCEDURES\03` | Utilisé par les deux contre-vérifications |
| Demande du propriétaire | Leçons QA d'Archipel : règles Q8 à Q11, F9, F10, A7 ; scénarios 12 à 15 ; outil de mesure de stabilité des panneaux ; poste dédié | `REGLES.md`, `LECONS-ARCHIPEL.md`, `PROCEDURES\05`, `06`, `10`, gabarit et skill de QA, `OUTILS\luau\stabilite-panneaux.luau` | **Écrit, non exécuté** : pas de Studio, pas de binaires Luau |

Propositions des agents : 4 déposées, 4 fusionnées, rangées dans `PROPOSITIONS\traitees\`.

## 4. Prévu contre mesuré

Aucune mesure en jeu. Seules les prévisions de la fiche v1 ont pu être confrontées au calcul.

| Prévision de la fiche v1 | Prévu par l'auteur | Calculé par la revue | Écart |
|---|---|---|---|
| Durée de contenu actif | 95 min | 87 min 27 s | −7 min 33 s : sous le seuil |
| Écart maximal entre achats, 0 à 10 min | 75 s | 88 s | +13 s |
| Écart maximal entre achats, 10 à 60 min | 360 s | 224 s | −136 s |
| Premier achat | 23 s | 20 s en simulation, 27 s d'après la première minute | — |

Leçon : une estimation d'auteur ne vaut rien ; depuis la v2 l'annexe C est tirée du simulateur.

## 5. Les portes ont-elles eu raison ?

| Porte | Résultat | Ce qu'elle a vu | Ce qu'elle a manqué |
|---|---|---|---|
| P0 | dérogation | Corpus de 10 gagnants et 10 faibles ou retombés, chiffres sourcés | Les Charts du jour ; les échecs sous 500 joueurs, invisibles dans les sources ; prix et cadence pour 18 jeux sur 20 |
| P1 | passe | Les sept rubriques, les annexes | Neuf décisions absentes et des estimations fausses : elle ne juge que la complétude, et son juge était l'auteur |
| P2 | 2 échecs, puis dérogation | 6 défauts P1 distincts en trois passages (4 dans la fiche v1, 1 dans la v2, 1 dans le simulateur), plus le défaut d'origine du simulateur (C5). C'est la porte qui a le plus travaillé | Rien d'identifié ; rien n'est vu en jeu |
| P3 | à confirmer | ITÉRER : rien à faire après 97 minutes, geste sans variation | Jugement non indépendant |

## 6. Ce qui reste

### Pour `lave-la-tour`

1. Fiche v4 : un objectif au septième jour, la variation du geste, la coopération visible (corrections 1 à 3 de `04-fun\RAPPORT-FUN.md`). Si la correction 1 touche les revenus, la revue d'économie se rejoue.
2. Revue du fun par Opus 5.5 (un sous-agent), puis jugement de P3.
3. Porte P0 à rejouer avec un navigateur : Charts du jour, prix et cadence des 18 autres jeux du corpus.
4. Production : attend un univers TEST, la sortie d'Archipel de la QA (un seul jeu en production à la fois) et, pour le contrôle de syntaxe, les binaires Luau.

### Pour l'usine (jamais essayé)

- Production dans Studio par le serveur MCP ; `pousser-script.ps1` ; taille maximale d'un script.
- QA : test à plusieurs clients ; `stabilite-panneaux.luau` (à valider sur un panneau qu'on déplace exprès) ; scénarios 12 à 15.
- Release, distribution, bilan d'un jeu lancé.
- Veille dans Chrome ; relecture des conditions de RoStats ; veille par un Haiku qui lirait des pages.
- Revue du fun et qualification par un modèle indépendant.

## 7. À dire au propriétaire

1. **Deux échecs, abandon ?** La règle A5 et la règle E11 se contredisent (C8). Proposition, non appliquée : ne compter comme échec d'une porte que le retour au concepteur qui change le concept ou ses constantes ; une contre-vérification qui trouve un défaut de spécification demande une correction et une nouvelle passe, pas un abandon. À décider avant le jeu n° 3.
2. **Le seuil de P3 sur le papier.** Deux axes sur sept ne se prouvent pas avant le prototype et sont plafonnés à 5 : il faut alors 7,8 sur les cinq autres. Soit c'est voulu (peu de fiches passeront), soit la passe papier doit avoir son propre seuil. Non modifié.
3. **Monétisation.** La fiche ne vend ni monnaie ni multiplicateur. Les deux gagnants lus vendent une passe « x2 Cash » à 99 Robux et 50 à 130 produits. Le jeu étant non compétitif, la règle E6 n'interdit pas un multiplicateur ; c'est un choix du propriétaire, avec un revenu attendu `NP` dans les deux cas.
4. **Un seul jeu en production à la fois** : Archipel est en QA et attend l'amorçage. `lave-la-tour` ne peut pas entrer en production avant, sauf décision écrite.
5. **Amorçage** (`PLAFONDS.md` § 6, inchangé) : groupe et univers TEST, espace disque, et deux ajouts de ce cycle : un poste ou une session Windows dédiés au pilotage (procédure 10 § 4), les binaires Luau dans `OUTILS\bin\`.
6. **Skills à réinstaller** : `usine-qa-multijoueur` et `usine-veille-navigateur` ont changé (`OUTILS\installer-skills.ps1 -Confirmer`).
7. **`PLAFONDS.md` § 5** : votre consigne sur la veille y est recopiée mot pour mot (commit `[proprietaire]`). À relire.
8. **Règle C8** (mot-clé de genre en anglais dans le titre) : aucun des dix gagnants du thème n'en porte ; leurs titres sont des verbes à l'impératif. Laissée « à calibrer ».

## 8. Ce que ce bilan ne sait pas

- Rien n'a été joué ni vu : chaque chiffre du jeu est un calcul, chaque chiffre de marché une lecture de page.
- La valeur de la fiche : sa seule relecture de fond est celle de son auteur.
- Si un Haiku délégué peut lire des pages avec un autre réglage, ou piloter Studio et Chrome : non essayé.
- Le coût en quota des quatre agents Codex en effort xhigh : non affiché par l'outil.
- Si les leçons QA d'Archipel sont bien traduites : aucune n'a été rejouée sur Archipel (dépôt et Studio interdits cette nuit).

## Addendum (16/11, 01:10) — leçons QA rejouées sur Archipel par l'orchestrateur de session

- `OUTILS\luau\stabilite-panneaux.luau` : compilé (`luau-compile --null`) puis exécuté en Play sur Archipel. Armée ouvert : 54 panneaux, 0 instable. Sans panneau : 46, 0 instable. Contrôle négatif : un cadre qui saute de 35 px est détecté (73 sauts) → **outil validé**.
- Il a trouvé un vrai défaut : `ArchipelHud.UI1Nav` « a disparu pendant la mesure », car deux scripts écrivaient sa visibilité. C'est la même classe de bug que les menus qui sautaient. Corrigé et publié. Leçon confirmée : la règle « un seul propriétaire par propriété d'UI » doit faire partie de la revue de code, pas seulement de la QA.
- Binaires Luau : toujours absents de `OUTILS\bin\`. La pose reste une décision du propriétaire (G17).

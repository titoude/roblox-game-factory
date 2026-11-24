# Portes de décision et seuils

Les valeurs sont dans `seuils.json` (source unique ; `OUTILS\etat.ps1 -Seuils` les affiche). Ce fichier dit ce que chaque porte vérifie, d'où vient le seuil et comment il a évolué.
Tous les seuils sont **initiaux** : aucun n'a encore été confronté à des joueurs réels. Ils se recalibrent au bilan des deux premiers jeux.

## Chaîne et portes

```
01 Veille ─P0→ 02 Concept ─P1→ 03 Économie ─P2→ 04 Fun ─P3→ 05 Production ─(P4 prototype)→ 06 QA ─P5→ 07 Release ─P6→ 08 Distribution ─P7, P8→ 09 Bilan ─P9→ fin
                                         jeu en ligne : boucles 11 Retours joueurs ─P10→ lot correctif → 06 → 07, et 12 Promotion ─P11
```

| Porte | Passe si | Sinon | Clés de `seuils.json` | Origine |
|---|---|---|---|---|
| **P0** Veille → Concept | Relevé daté, chaque chiffre sourcé, couverture ≥ seuil ; pour le thème retenu, 10 gagnants et 10 faibles ou retombés | Compléter la veille ; thème sans corpus = pas de concept | `veille.*` | Plan §3, étude 01 |
| **P1** Concept → Économie | Fiche complète (7 éléments), scénario des 60 premières secondes, règle de monétisation en une phrase, prévisions chiffrées, périmètre dans le budget | Réécrire (2 itérations au plus), puis abandon | `concept.*` | Plan §4 |
| **P2** Économie → Fun | Simulation dans les seuils de cadence, 0 défaut P0, chaque P1 corrigé ou accepté avec raison, monétisation conforme à E6 | Retour au concept (2 itérations), puis abandon | `economie.*` | Archipel, audits |
| **P3** Fun → Production | Passe papier : moyenne des axes **vérifiables** ≥ `fun.moyenne_verifiable_papier_min`, aucun axe sous le plancher, critère d'arrêt mesurable écrit pour le prototype (A9). Les axes non vérifiables sur papier se jugent à la passe 2 (P4) | Retour au concept (2 retours ; le troisième échec abandonne, A5) | `fun.*` | Archipel, qualification ; bilan du cycle 2 |
| **P4** Prototype (dans la production) | Première action significative en 60 s ou moins **mesurée en Play**, 0 erreur console, format téléphone lisible | Itérer sur le prototype avant tout autre lot | `prototype.*` | Plan §3 |
| **P5** QA → Release | Test à 2 clients ou plus, 0 erreur console, 0 bug P0 et P1 ouvert, sauvegarde fidèle, interface vue en PC plein écran et téléphone, panneaux stables 30 s, monde vu d'en bas, HUD dégagé de la liste des joueurs, note de qualification ≥ seuil de la cible | Retour en production (3 cycles au plus), puis décision d'arrêt | `qa.*` | Archipel |
| **P6** Release → Distribution | Publié en TEST puis PROD privé, revue indépendante du diff favorable, états vérifiés un par un, ligne d'autorisation dans `PLAFONDS.md` | Corriger ; sans autorisation, le jeu attend | — | Plan §2, étude 04 |
| **P7** Bêta → Pub | Cohorte organique ≥ seuil, J1 ≥ seuil, session ≥ seuil | Corriger l'arrivée et la boucle ; pas de pub | `beta.*` | Plan §3 |
| **P8** Pub → Montée | CAC et coût par retenu J7 sous les plafonds de `PLAFONDS.md`, marge à 30 jours positive | Arrêt de la campagne | `pub.*` | Plan §3, étude 03 |
| **P9** Bilan | Bilan prévu/mesuré écrit, propositions traitées, règles et seuils mis à jour, journal complété | Le jeu suivant ne démarre pas | — | Plan §7.5 |
| **P10** Retours joueurs (boucle) | Collecte réelle faite ou lot vide constaté, chaque groupe jugé par un agent indépendant, actions retenues inscrites au plan, suivi à 7 jours planifié | `a_confirmer` si la collecte n'a tourné que sur un exemple | `retours.*` | Procédure 11, bilan du cycle 2 |
| **P11** Promotion (boucle, facultative) | Verdict de `decision-promo.py` : `continuer` | `ameliorer_promo`, `arreter_promo`, `ameliorer_jeu` ou `jeu_suivant` selon la règle | `promo.*` | Procédure 12, veille du 16/11/2026 |

## Lecture des seuils

- **Référence de marché** (`reference_gameanalytics_2026`) : médianes de plus de 500 jeux ayant atteint 1 M de MAU (J1 10,3 %, J7 1,6 %, J30 0,5 %, session 9,8 min). Ce sont des jeux déjà gros : repère, pas objectif.
- **Cadence économique** : issue de la « cadence V8 » d'Archipel (chantiers ≤ 3 min, écart maximal de 7 min 50 entre achats sur la route de référence). Un seul jeu, jamais mesuré sur de vrais joueurs.
- **Notes de qualification** : Archipel a obtenu 5,6/10 avec le verdict « bêta fermée oui sous conditions, public non ». Les planchers 6,0 et 7,5 sont posés au-dessus de ce point, sans autre preuve.
- **Bêta** : J1 ≥ 8 % et session ≥ 8 min sur 200 joueurs organiques. Avec 200 joueurs, l'intervalle de confiance sur un J1 de 8 % est d'environ ± 4 points : la porte se lit avec son incertitude.

- **Remboursement** (`payback_min_s`, `payback_max_s`) : depuis le cycle 1, jugé sur chaque exemplaire acheté, au prix payé, multiplicateurs permanents acquis compris, à partir de la mise en service. Les valeurs 30 s et 5 min n'ont pas changé ; c'est leur champ d'application qui a été précisé. Conséquence constatée : une croissance de coût de 1,2 par exemplaire ne tient pas sur dix exemplaires au-delà du deuxième palier ; il faut 1,06 à 1,17.
- **Poids du geste** (`retard_lent_min_pct`) : le profil lent doit finir au moins 5 % après le profil actif. Seuil posé au cycle 1 sur un seul jeu jamais joué : signalé par une ALERTE du simulateur, pas par un échec.

## Dérogations

Un seuil `à calibrer` peut faire l'objet d'une dérogation pendant un jeu : l'orchestrateur l'écrit dans `ETAT.json` (`OUTILS\etat.ps1 -Porte … -Resultat derogation -Note "<raison>"`). Un garde-fou ne se déroge jamais.

## Historique de calibration

| Date | Clé | Avant | Après | Preuve |
|---|---|---|---|---|
| 2026-11-15 | `economie.retard_lent_min_pct` ; champ d'application de `economie.payback_*` | absente ; premier exemplaire seulement | 5 % ; chaque exemplaire acheté | Revue d'économie de `lave-la-tour`, passe 1 : `JEUX\lave-la-tour\03-economie\RAPPORT-ECONOMIE-calcul.md` (D2) et `RAPPORT-ECONOMIE-adversaire.md` (A01, A02). `OUTILS\sim-economie.py` corrigé le même jour |
| 2026-11-16 | `fun.moyenne_verifiable_papier_min` ; lecture de `fun.iterations_max` et de `economie.iterations_max` | absente ; « deux échecs = abandon » (A5) | 7,0 sur les axes vérifiables ; 2 retours au concepteur, abandon au troisième échec | Version 3. Trois revues du fun indépendantes de `lave-la-tour` (`04-fun\RAPPORT-FUN-INDEPENDANT.md` 5,7 ; `RAPPORT-FUN-V4.md` 6,1 ; `RAPPORT-FUN-V5.md` 6,4, axes vérifiables 7,0) : avec deux axes plafonnés à 5, la porte exigeait 7,8 sur les cinq autres et ne pouvait pas passer sur papier. Écart massif et expliqué sur un seul jeu : statut « à calibrer ». **Non appliqué à `lave-la-tour`**, resté en dérogation (A4) |
| 2026-11-16 | `retours.*`, `promo.*`, `economie.contre_verifications_max_par_version` | absentes | voir `seuils.json` | Version 3. Procédures 11 et 12 ; valeurs de départ, aucune mesure réelle |
| 2026-11-24 | `bilan.ecart_tolere_pct` | absente | 25 | Version 4. Boucle d'amélioration (`OUTILS\boucle-amelioration.py`, procédure 09 § 6) ; valeur de départ, aucune mesure réelle. Aucun seuil existant modifié |
| 2026-11-15 | toutes | — | version 1 | Études 00 à 04, audits et qualification d'Archipel |
| 2026-11-15 | `qa.ecran_pc_min_px`, `qa.formats_ecran_obligatoires`, `qa.stabilite_panneaux_*`, `qa.captures_monde_angles_min` | absentes | version 2 : 1920×1080, PC et téléphone, 30 s, 60 échantillons, 1 px, 3 angles | Ordre du propriétaire après la mise en ligne d'Archipel (menu qui sautille, dessous d'îles vide, liste des joueurs sur le HUD) : `LECONS-ARCHIPEL.md` § QA. Clés ajoutées, aucun seuil existant modifié |

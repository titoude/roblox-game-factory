# Plan de production — <nom> (`<slug>`)

Écrit par l'orchestrateur après la porte P3, avant le premier lot. Le producteur le suit ; un écart se note dans `JOURNAL-LOTS.md`.
Pièces figées : `02-concept\FICHE-CONCEPT.md` (version …), `03-economie\economie.json` (commit `…`), `04-fun\RAPPORT-FUN.md`.

## 1. Conditions de départ

| Condition | État | Qui la lève |
|---|---|---|
| Porte P3 passée (ou dérogation à rejouer) | | Orchestrateur |
| Univers TEST disponible (procédure 10 § 1), sinon place locale non publiée | | Propriétaire |
| Verrou `place:<placeId>` libre | | Producteur |
| Poste ou session Windows dédiés si un lot exige le bureau (règle A7) | | Propriétaire |

## 2. Lots

Un lot tient en une session. Preuve de fin = ce qui est **vu en jeu** (capture ou mesure).

| Lot | Contenu propre à ce jeu | Scripts (`src\`) | Preuve de fin | Dépend de | Faisable sans Studio ? |
|---|---|---|---|---|---|
| L0 | | | Porte P4 : première action ≤ 60 s en Play, 0 erreur console, capture PC plein écran et téléphone | — | Code oui, preuve non |
| L1 | | | | L0 | |

## 3. Constantes et vérité unique

Le module `Config` reprend les noms et les valeurs de `economie.json`. Liste des constantes qui ne figurent pas dans `economie.json` (durées d'animation, tailles, plafonds de parts) et leur valeur de départ :

| Constante | Valeur | Origine |
|---|---|---|
| | | |

## 4. Monde et interface

- Monde : ce qui est construit par script, ce qui est posé à la main (à décrire dans `MONDE.md`). Chaque volume visible d'en bas a une épaisseur et un dessous habillés (F10).
- Interface : liste des panneaux ; pour chacun, ancrage, format téléphone et PC plein écran (Q8), ce qui peut changer de taille pendant le jeu (à mesurer par `OUTILS\luau\stabilite-panneaux.luau`, Q9).
- Coin haut droit sur PC : HUD absent, ou liste des joueurs masquée (F9).

## 5. Actions de test (réservées à Studio, règle P6)

| Action | Effet | Sert aux scénarios |
|---|---|---|
| | | |

## 6. Ce que la QA devra rejouer

Scénarios venus du rapport d'économie (adversaire) et de la revue du fun, avec le lot qui les rend testables.

| # | Scénario | Origine | Testable après le lot |
|---|---|---|---|
| | | | |

## 7. Risques et points non vérifiables aujourd'hui

| Risque | Ce qui le lèverait | Lot concerné |
|---|---|---|
| | | |

## 8. Estimation

| Mesure | Prévu | Réel (au bilan) |
|---|---|---|
| Nombre de lots | | |
| Sessions de production | | |
| Nombre de parts au palier maximal | | |

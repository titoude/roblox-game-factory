# Proposition — Arrondi exact des prix de générateurs

- Date : 2026-11-16. Agent : contre-vérificateur économie 2, gpt-6.1-sol effort xhigh. Jeu : lave-la-tour. Étape : 03.

## Constat

L’option `prix_entiers` est désormais présente, mais la puissance binaire flottante fait dépasser certains prix mathématiquement entiers avant le plafond supérieur. Six prix sur les cent de la fiche v3 sont surévalués de 1 pièce ; la cadence et le verdict restent identiques.

## Preuve

Sources figées au commit `225cb3a37f3a3abc15c69039c33c2b02c5b51ad3` :
- `OUTILS/sim-economie.py:190–194` : `math.ceil(cout - 1e-9)`, puissance calculée en flottant.
- `JEUX/lave-la-tour/02-concept/FICHE-CONCEPT.md:85/94/96/136` : plafond du coût initial × croissance^(n−1), constantes r6 et r8.
- Calcul exact : 5 600 000 × 1,10³ = **7 453 600** ; puissance flottante **7 453 600,000000002**, coût outil **7 453 601**.
- Comparaison des 100 prix avec `Decimal(str(cout)) * Decimal(str(croissance)) ** (n-1)`, précision 80, puis `ROUND_CEILING` : écarts +1 pour r6 n°4/5/6 et r8 n°3/5/6. Total **+6 pièces**, maximum relatif **0,0000135 %**.
- Variante en mémoire remplaçant seulement `cout_gen` par ce calcul décimal : fins actif/lent **5 829/6 421 s**, écarts **61/332/378 s** et **69/367/421 s**, aucun remboursement hors borne ; aucune modification du simulateur.
- `OUTILS/test-sim-economie.py:83–90` vérifie les petits prix 15 et 10, sans puissance à grand prix mathématiquement entier. Tests officiels : sortie **0**.

## Règle ou seuil visé

`REGLES.md` E3 (prix réellement payé), A3 (calcul reproductible) ; `PROCEDURES/03-REVUE-ECONOMIE.md` § Conventions ; option `prix_entiers` de l’outil. **P2**, aucun seuil de cadence violé pour cette fiche.

## Changement proposé

Lorsque `prix_entiers` est activé, calculer la puissance sur les constantes décimales déclarées avec une précision suffisante, puis appliquer le plafond supérieur ; ne pas arrondir récursivement le prix précédent.
Ajouter des contrôles ciblés : r6 n°4 = 7 453 600 ; r8 n°3 = 5 618 000 000 ; conserver un cas réellement fractionnaire (r1 n°3 = 15). Vérifier la non-régression des deux profils. Aucun changement de seuil.

## Portée

Tous les jeux employant `prix_entiers` ; aucun effet de cadence démontré sur lave-la-tour v3. Proposition uniquement, aucun correctif appliqué.

---
Décision de l'orchestrateur (bilan du cycle 1, 2026-11-16) : **fusionnée**. `OUTILS\sim-economie.py` calcule les prix entiers en décimal exact (module `decimal`) ; contrôle ajouté dans `OUTILS\test-sim-economie.py` (5 600 000 × 1,1³ = 7 453 600). Simulation de lave-la-tour rejouée : mêmes verdicts, fin 97:09.

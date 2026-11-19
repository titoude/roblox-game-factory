# Proposition — Un rejeu contre le simulateur compare les soldes, et chaque test d'argent survit à une mutation

- Date : 2026-11-16. Agent : 05.relecteur-code, Claude Opus 5.5. Jeu : `lave-la-tour`. Étape : 05 (revue du commit `f07996f`).

## Constat

Le rejeu des 105 achats achète aux instants du simulateur et vérifie seulement que chaque achat passe : un code qui donne trop d'argent le passe aussi. La date de fin de contenu y est comparée à elle-même. Deux autres assertions du banc passent quel que soit le code.

## Preuve

`JEUX/lave-la-tour/05-production/REVUE-CODE-f07996f.md`, D6 et D7. Mutations sur une copie du commit `f07996f` : gain d'une vitre × 2 → `rejeu-simulateur.test.luau` PASSE ; revenu × 1,5 → PASSE ; cadence `Action` 2 → 100 → `remotes.test.luau` PASSE ; déménagement sans identifiant d'opération → `vitres.test.luau` PASSE. `rejeu-simulateur.test.luau:23` : `banc.proche(t, 5829, 5)` où `t` vaut `attendu.fin_s`, tiré du simulateur.

## Règle ou seuil visé

`REGLES.md` P14 (preuve hors Studio) et E10 (passe 2 sur le commit) ; `PROCEDURES\05-PRODUCTION-STUDIO.md` § « Sans Studio : le banc ».

## Changement proposé

Ajouter à P14 : « Un rejeu contre le simulateur compare le solde après chaque achat (écart relatif ≤ 10⁻⁶) et vérifie qu'un achat est refusé avant son instant quand le simulateur n'en avait pas les moyens. Le relecteur de code joue au moins trois mutations du code d'argent (gain × 2, revenu × 1,5, une validation de Remote retirée) : chacune doit faire échouer au moins un test. Une assertion qui passe sous toutes les mutations est un défaut P2 du lot. » Vérifiable : le rapport de revue liste les mutations jouées et le test qui échoue pour chacune.

## Portée

Tous les jeux de l'usine qui prouvent un lot par le banc.

---
Décision de l'orchestrateur (au bilan) : …

---
Décision de l'orchestrateur (bilan du cycle 2, 2026-11-16) : fusionnée dans P14 (active).

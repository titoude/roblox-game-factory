# Proposition — contrôler les remboursements de chaque exemplaire

- Date : 2026-11-15. Agent : calcul, gpt-6.1-sol, effort xhigh. Jeu : lave-la-tour. Étape : 03, passe 1 papier.

## Constat

Le simulateur juge les remboursements sur le coût initial et le revenu nominal de chaque palier seulement. Sur la fiche actuelle, il affiche « aucun » défaut de remboursement pour tous les robots, alors que 29 achats ont un remboursement marginal supérieur à 300 s, améliorations acquises comprises.

## Preuve

- `OUTILS/sim-economie.py:164–166` augmente les coûts par exemplaire ; `:173` calcule le revenu marginal effectif, mais `juger_generateurs():305` teste seulement `g['cout'] / g['revenu_s']`.
- Fiche § 3 bis : r10 coûte 3 500 000 000, croissance 1,2, revenu 12 000 000/s. Son dixième achat coûte 18 059 231 232 ; après a4 ×1,5 et a5 ×1,25, revenu marginal 22 500 000/s, remboursement **802,632499 s**, contre le nominal affiché **291,666667 s**.
- `JEUX/lave-la-tour/03-economie/RAPPORT-ECONOMIE-calcul.md`, § « Remboursements répétés » : calcul manuel, reproduction par sous-classe en mémoire, décompte 29/100 pour actif et lent. Proposition finale : 0/100 hors [30 ; 300] s.
- Empreinte SHA-256 du simulateur lu : `0d5bf0768ca617ebf4088747c305e8353ff05e6016efa188e38068eac2474785`. Il n'a pas été modifié.

## Règle ou seuil visé

`REGLES.md` E3 ; `seuils.json` § economie, `payback_min_s` et `payback_max_s` ; `PROCEDURES/03-REVUE-ECONOMIE.md` § Agent calcul et Porte P2.

## Changement proposé

« La revue calcule le remboursement marginal de chaque générateur acheté, au coût réellement payé et avec les multiplicateurs permanents actifs au moment de l'achat. Elle précise si le délai de chantier entre dans ce remboursement. Le remboursement nominal du premier exemplaire reste une information distincte et ne suffit pas à déclarer E3 conforme. Le rapport liste le premier dépassement, le maximum et le nombre de transactions hors bornes par profil. »

« Le simulateur conserve pour chaque transaction de générateur le coût, le revenu marginal et le chantier, puis fait échouer le contrôle de remboursement du profil actif si une transaction sort des bornes. Les améliorations à effet futur ne sont pas créditées avant leur acquisition. »

Vérifications attendues avant évolution de l'outil : cas r10 n°10 ci-dessus détecté à 802,632499 s ; r4 n°10 détecté à 300,987187 s ; variante finale contrôlée à zéro dépassement ; effet d'une amélioration acquise et d'un chantier positif explicitement documenté. Ne pas modifier la définition du seuil en silence.

Friction de procédure connexe : donner aux deux profils le même délai entre achats pour isoler le facteur d'actions, ou déclarer séparément la sensibilité à un délai plus lent ; ne pas présenter le défaut technique 10 s comme une donnée de la fiche. Clarifier aussi réaction initiale et délai entre achats.

## Portée

Tous les jeux à achats répétés, coûts croissants ou améliorations de revenu. Proposition à examiner au bilan par l'orchestrateur ; aucune règle ni aucun outil modifié par ce dépôt.

---
Décision de l'orchestrateur (bilan du cycle 1, 2026-11-15) : **fusionnée**. OUTILS\sim-economie.py juge le remboursement de chaque exemplaire acheté (prix payé, multiplicateurs acquis, hors chantier) et fait échouer le profil actif ; vérifié sur les cas cités (r10 n°10 à 13:23, r4 n°10 à 5:01, 29 sur 100 ; variante proposée 0 sur 100). Profils actif et lent au même délai entre achats. Règle E3 précisée, conventions écrites dans la procédure 03. Ajouts de l'orchestrateur : option `action.part_revenu_s, alerte « retard du joueur lent », attente finale comptée dans les écarts.

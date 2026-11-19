# Proposition — marginal complet du simulateur à action indexée

- Date : 2026-11-16. Agent : contre-vérificateur, gpt-6.1-sol xhigh. Jeu : lave-la-tour. Étape : 03, contre-vérification 1 au commit b4905a2.

## Constat

Le simulateur crédite bien le supplément d’action lié aux robots mais l’ignore dans le revenu marginal des candidats robots et améliorations ciblant un robot. Ce marginal sert à la politique d’achat et au remboursement de chaque exemplaire annoncé selon E3.

## Preuve

- `OUTILS/sim-economie.py:143–148` : action = cadence × mult_action × (gain × mult_tout + part_revenu × revenu_gens).
- `:194`, `:203–204` : marginal limité au revenu direct des robots ; `:216`, `:227`, `:317–329` l’utilisent pour choisir et juger le remboursement.
- Fiche v2 § 3 bis : cadence active 0,5/s, raclette finale 3, part_revenu_s=0,2. Un ΔR produit donc ΔR×1,3 de revenu total.
- r10 n°10 acheté à t=5650 avec B=1,875 : coût interne 7 931 566 754 659,265 ; marginal direct 29 062 500 000/s ; remboursement outil 272,914125 s ; marginal total 37 781 250 000/s ; remboursement 209,933942 s.
- Rejeu diagnostique en mémoire, sans changer l’outil, en multipliant les candidats robots et améliorations de cible générateur par (1+cadence×mult_action×part_revenu) : fin active 5828 s contre 5830 s ; maximum de remboursement 218,881150 s, 0/100 hors borne. Aucun verdict de jeu déduit.

## Règle ou seuil visé

`REGLES.md` E3, E10 ; `PROCEDURES/03-REVUE-ECONOMIE.md` § Conventions ; en-tête de `OUTILS/sim-economie.py` lignes 12–22.

## Changement proposé

« Pour choisir un achat et contrôler E3, utiliser le supplément de revenu total effectivement produit sous le profil courant, y compris l’action indexée sur les robots. Pour un robot ou une amélioration de robot, multiplier son supplément direct par (1 + cadence_du_profil × multiplicateur_action_acquis × action.part_revenu_s). Photographier les multiplicateurs permanents acquis lors de l’achat ; ne pas utiliser les améliorations futures. Garder le chantier séparé et le tableau nominal explicitement distinct. »

Ajouter une vérification indépendante à action indexée non nulle : le marginal mémorisé doit égaler la différence de revenu total avant/après mise en service, à état et permanents identiques ; cas robot, amélioration ciblée, actif et lent. Rejouer ensuite la fiche, sans modifier ses seuils.

Compléments à arbitrer : faire appliquer l’arrondi de prix choisi par la fiche (actuellement absent, `:185–187`) et rendre le verdict explicitement incomplet quand la fin n’est pas atteinte (`:333–337`, alerte connue de la passe 1). Une exécution arrêtée à 600 s sur l’entrée v2 donne fin absente et `echec=False` : la formulation « tous les seuils sont tenus » est alors trop forte.

## Portée

Tous les jeux utilisant `action.part_revenu_s`, et toute revue s’appuyant sur le remboursement de chaque exemplaire. Proposition seulement : ni outil, ni règle, ni procédure modifiés.

---
Décision de l'orchestrateur (bilan du cycle 1, 2026-11-16) : **fusionnée**. `OUTILS\sim-economie.py` : le revenu ajouté par un robot ou par une amélioration de robot compte le supplément d'action indexée (facteur 1 + cadence × multiplicateur d'action × part_revenu_s), pour le choix d'achat comme pour le remboursement ; option `prix_entiers` ; une fin non atteinte sur une durée plus courte que le minimum demandé est un ÉCHEC ; le libellé du verdict ne dit plus « tous les seuils sont tenus ». Contrôle indépendant ajouté : `OUTILS\test-sim-economie.py` (marginal = hausse réelle du revenu total, robot et amélioration, actif et lent), lancé par `verifier-usine.ps1`. Rejeu de la fiche : fin 97:09, 0 exemplaire hors borne sur 100.

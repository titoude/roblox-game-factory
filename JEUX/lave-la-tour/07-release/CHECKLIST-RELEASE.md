# Liste de contrôle de release — Lave la tour (`lave-la-tour`) — version n

- Date : 2026-11-15. Commit : `…`. Étiquette : `lave-la-tour-v…`.
- Cible : TEST privé / PROD privé / bêta fermée / public.
- Dernière version saine (retour arrière) : …

## Avant de publier

| # | Contrôle | Fait | Preuve |
|---|---|---|---|
| 1 | Porte P5 passée pour ce commit | | `06-qa\RAPPORT-QA-….md` |
| 2 | Porte P2 confirmée avec Codex (si jugée en mode dégradé) | | |
| 3 | Revue indépendante du diff : aucun défaut certain | | `REVUE-DIFF-v….md` |
| 4 | Actions de test inatteignables hors Studio | | |
| 5 | Offres à identifiant 0 invisibles | | |
| 6 | Autorisation écrite pour la cible dans `PLAFONDS.md` § 1 | | ligne du … |
| 7 | Verrou `place:<placeId>` pris par l'orchestrateur | | |
| 8 | Aucun secret dans le dépôt (`verifier-usine.ps1`) | | |

## États, un par un

Un état ne se déduit pas du précédent.

| État | TEST | PROD | Comment c'est vérifié |
|---|---|---|---|
| Sauvegardé (`save_place`) | | | numéro de version |
| Publié | | | relecture de l'état distant |
| Réglages relus (nom, description, taille de serveur) | | | valeur relue après écriture |
| Boutique : identifiants dans le manifeste et dans `Config` | | | `MANIFESTE-IDS.json` |
| Achat de test accordé une seule fois | | | |
| Icône et vignettes envoyées | | | |
| Modération des images | | | statut relu (pas immédiat) |
| Visible par la cible | | | |
| Joué en ligne par un compte réel | | | ou « non vérifié en ligne » |

## Ce qui a demandé le propriétaire ou l'interface

- …

## Incidents

Délai dépassé, conflit Team Create, refus : ce qui s'est passé, ce qui a été relu avant de recommencer.

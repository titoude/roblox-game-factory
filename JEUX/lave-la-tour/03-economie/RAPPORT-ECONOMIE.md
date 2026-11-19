# Rapport d'économie — Lave la tour (`lave-la-tour`)

- Passe : 1 (papier). La passe 2 (code) se fera au lot L1 et avant la release.
- Rôle : fusion par l'orchestrateur, le 2026-11-16.
- Agents : quatre `gpt-6.1-sol` en effort xhigh, indépendants — calcul et adversaire sur la fiche v1, contre-vérification 1 sur la v2, contre-vérification 2 sur la v3.
- Pièces lues : `RAPPORT-ECONOMIE-calcul.md`, `RAPPORT-ECONOMIE-adversaire.md`, `RAPPORT-ECONOMIE-contre-verification-1.md`, `RAPPORT-ECONOMIE-contre-verification-2.md`, `SIMULATION.md`, fiche v3.
- Ce qui n'a pas été couvert : rien n'est vu en jeu. Hors ligne, contrat du jour, mousse, pourboires et offres payantes ne sont pas simulés ; ils sont chiffrés à part.

## Verdict

| Point | Résultat |
|---|---|
| Cadence (simulation, profil actif) | PASSE : premier achat 20 s, écarts 61 s / 5 min 32 s / 6 min 18 s, contenu 97 min 09 s, 100 exemplaires sur 100 remboursés en moins de 5 min (le plus long : 3 min 39 s) |
| Défauts P0 certains | 0 |
| Défauts P1 certains | 0 restant. Six défauts distincts trouvés et fermés : 4 dans la fiche v1 (contenu trop court, remboursements trop longs — relevé par les deux agents —, geste sans valeur, mousse sans quota), 1 dans la fiche v2 (stock de vitres partagé), 1 dans le simulateur |
| Risques à vérifier en jeu (gravité s'ils sont reproduits) | 3 P0, 4 P1, 2 P2 — non comptés parmi les défauts certains |
| Décisions manquantes dans la fiche, à écrire avant le code | 0 (M01 à M09 écrites au § 3 ter ; le décompte de la mousse précisé après la contre-vérification 2) |
| Monétisation conforme à la règle de la fiche et à E6 | oui sur le papier |
| Avis pour la porte P2 | passer, sous dérogation à la règle A5 (deux échecs avant ce passage) |

## 1. Faits (lus)

| Version | Verdict | Défauts certains | Ce que la version suivante a changé |
|---|---|---|---|
| v1 | échec | Contenu 87 min 27 s ; 29 exemplaires sur 100 remboursés en plus de 5 min (jusqu'à 13 min 23 s) ; le joueur lent finit 1,1 % après l'actif ; mousse sans quota | Gain d'une vitre indexé sur le revenu des robots ; croissances de coût de 1,06 à 1,17 ; paliers 5 à 10 relevés ; quotas de mousse ; décisions d'état |
| v2 | échec | Stock de 30 vitres partagé par 6 joueurs (90 vitres par minute pour 180 demandées) ; défaut de l'outil : le revenu ajouté par un robot oubliait le supplément de lavage | Stock propre à chaque joueur ; outil corrigé et testé ; quotas en temps ; arrondi des prix |
| v3 | passe | Aucun P0 ni P1 ; deux P2 (décompte de la mousse, arrondi flottant de l'outil sur 6 prix) | Les deux P2 corrigés le jour même |

## 2. Calculs (reproductibles)

Commande : `python OUTILS\sim-economie.py JEUX\lave-la-tour\03-economie\economie.json --sortie JEUX\lave-la-tour\03-economie\SIMULATION.md` (code de sortie 0). Contrôles de l'outil : `python OUTILS\test-sim-economie.py` (code de sortie 0).

| Profil | Premier achat | Écart max 0–10 min | Écart max 10–60 min | Écart max après | Contenu actif |
|---|---|---|---|---|---|
| actif | 20 s | 61 s | 332 s | 378 s | 97 min 09 s |
| lent | 40 s | 69 s | 367 s | 421 s | 107 min 01 s |
| payant (passe 2) | à faire | | | | |

Vérifications à la main (contre-vérification 2) : premier achat 10 ÷ 0,5 = 20 s ; écart de 61 s retrouvé à la pièce près ; 10ᵉ nacelle robot 22 764 ÷ 104 = 218,9 s.

Revenus hors simulation, à état final figé (R = revenu des robots en service) : stock hors ligne plein 60 min de R ; contrat du jour 10 min de R ; pourboires 10 min de R par jour au plus ; mousse 0,75 min de R pour 10 minutes. Total d'un retour complet : environ 81 minutes de R. Les 97 minutes ne valent donc que pour une progression sans ces apports.

## 3. Défauts

Aucun défaut certain ouvert. Risques transmis à la QA (scénarios dans `05-production\PLAN-PRODUCTION.md` § 6) :

| # | Gravité si reproduit | Statut | Risque | Scénario | Règle touchée |
|---|---|---|---|---|---|
| V01 | P0 | à vérifier en jeu | Double crédit d'une vitre (auto et manuel, rejeu) | QA01, QA02 | E6, E7 |
| V02 | P0 | à vérifier en jeu | Stock hors ligne ou prime rejoués après reconnexion | QA03, QA04 | E8, E12 |
| V05 | P0 | à vérifier en jeu | Passe appliquée deux fois | QA08 | E6, E7, E8 |
| V03 | P1 | à vérifier en jeu | Quotas remis à zéro par un changement de serveur ou de jour | QA05, QA06 | E4, E5 |
| V04 | P1 | à vérifier en jeu | Robot qui produit avant la fin de son chantier | QA07 | E7, E12 |
| V06 | P1 | à vérifier en jeu | Mousse cumulée ou appliquée aux robots | QA09 | E5, E12 |
| V07 | P1 | à vérifier en jeu | Joueur sans vitre à laver | QA10 | E7 |

## 3 bis. Décisions manquantes dans la fiche

Aucune. Deux paramètres du simulateur ne sont pas dans la fiche et gardent leur valeur par défaut : 3 secondes entre deux achats, 4 heures simulées.

## 4. Propositions

Appliquées à la fiche : voir le tableau du § 1. Appliquées à l'usine : `OUTILS\sim-economie.py`, `OUTILS\test-sim-economie.py`, règles E3, E14, E15, procédure 03, gabarit de ce rapport.

## 5. Scénarios pour la QA

Les onze scénarios de l'adversaire (QA01 à QA11), les huit du calcul et ceux des deux contre-vérifications sont regroupés en dix lignes dans `05-production\PLAN-PRODUCTION.md` § 6.

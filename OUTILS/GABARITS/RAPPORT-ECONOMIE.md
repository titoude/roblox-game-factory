# Rapport d'économie — <nom> (`<slug>`)

- Passe : 1 (papier) / 2 (code, commit `…`)
- Rôle : calcul / adversaire / fusion par l'orchestrateur
- Agent : <modèle, effort>, le <date>
- Pièces lues : …
- Ce qui n'a pas été couvert : …

## Verdict

| Point | Résultat |
|---|---|
| Cadence (simulation, profil actif) | PASSE / ÉCHEC / non évaluée (rôle adversaire : c'est le rôle calcul qui la juge) |
| Défauts P0 certains | n |
| Défauts P1 certains | n |
| Risques à vérifier en jeu (gravité s'ils sont reproduits) | n P0, n P1 — non comptés parmi les défauts certains |
| Décisions manquantes dans la fiche, à écrire avant le code | n |
| Monétisation conforme à la règle de la fiche et à E6 | oui / non |
| Avis pour la porte P2 | passer / retour au concept |

## 1. Faits (lus)

Référence à la fiche (section) ou au code (`fichier:ligne` au commit audité).

- …

## 2. Calculs (reproductibles)

Rôle adversaire : les tableaux de simulation ci-dessous sont facultatifs (il ne lit ni le rapport du calcul ni `SIMULATION.md`) ; ses calculs directs restent reproductibles, et une proposition non simulée se dit « effet calculé, non simulé ». Un défaut démontré sur le papier n'est pas une preuve en jeu (G15) ; l'absence d'une règle dans la fiche ne démontre pas une faille du futur code : elle va dans « Décisions manquantes ».

Commande : `python OUTILS\sim-economie.py JEUX\<slug>\03-economie\economie.json --sortie JEUX\<slug>\03-economie\SIMULATION.md`

| Vérification à la main | Calcul | Résultat du simulateur | Écart |
|---|---|---|---|
| Premier achat | coût ÷ revenu = … | | |
| Un écart entre deux achats | | | |
| Un remboursement | | | |

| Profil | Premier achat | Écart max 0–10 min | Écart max 10–60 min | Écart max après | Contenu actif |
|---|---|---|---|---|---|
| actif | | | | | |
| lent | | | | | |
| payant (passe 2) | | | | | |

## 3. Défauts

Gravité : **P0** casse le jeu ou la promesse d'honnêteté ; **P1** dégrade nettement le rythme ou l'équité ; **P2** réglage.
Statut : **certain** (chemin démontrable) ou **à vérifier en jeu** (scénario de test fourni).

| # | Gravité | Statut | Défaut | Chemin ou scénario | Règle touchée |
|---|---|---|---|---|---|
| 1 | | | | | |

## 3 bis. Décisions manquantes dans la fiche

Ce que la fiche ne dit pas et qu'il faut trancher avant le code (base d'un « revenu de référence », jour serveur, arrondis, portée d'une offre, état d'un chantier pendant l'absence…).

| # | Décision à écrire | Pourquoi elle change le résultat |
|---|---|---|
| | | |

## 4. Propositions

Séparées des faits. Constantes proposées et simulation rejouée avec elles (rôle calcul), ou effet calculé sans simulation (rôle adversaire).

| Constante | Actuelle | Proposée | Effet simulé ou calculé (préciser) |
|---|---|---|---|
| | | | |

## 5. Scénarios pour la QA

1. …

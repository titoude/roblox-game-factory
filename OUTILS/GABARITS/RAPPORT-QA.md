# Rapport de QA — <nom> (`<slug>`) — cycle n

- Date : <date>. Commit testé : `…`. Place : … (version Team Create …).
- Chef de test : orchestrateur. Testeurs : … Analyste : … Qualification : …
- Niveau réalisé : A (solo outillé) / B (serveur local + … clients) / C (place privée, comptes réels)
- Si le niveau B n'a pas pu être monté : pourquoi, et ce qui l'a remplacé.

## Verdict

| Critère de la porte P5 | Résultat | Preuve |
|---|---|---|
| Test à 2 clients ou plus | oui / non | |
| Session complète sans erreur console | oui / non | |
| Défauts P0 ouverts | n | |
| Défauts P1 ouverts | n | |
| Sauvegarde et rechargement fidèles | oui / non | |
| Première action d'un nouveau joueur | … s | |
| Interface vue en PC plein écran **et** téléphone | oui / non | |
| Panneaux stables 30 s (0 instable) | oui / non | |
| Monde vu d'en bas et de biais, sans dessous vide | oui / non | |
| HUD dégagé de la liste des joueurs sur PC | oui / non | |
| FPS au moment le plus chargé (format téléphone) | … | |
| Note de qualification | … /10 | |
| **Avis** | passer / retour en production / arrêt | |

## Scénarios

Mode : **vu** (capture, mesure), **lu** (code), **non vérifiable**.

| # | Scénario | Niveau | Attendu | Observé | Mode | Preuve (capture) | Résultat |
|---|---|---|---|---|---|---|---|
| 1 | Arrivée, première action | | ≤ 60 s | | | | |
| 2 | Dix minutes de boucle | | | | | | |
| 3 | Quitter et revenir ; en pleine action ; arrêt serveur | | | | | | |
| 4 | Interaction à deux | | | | | | |
| 5 | Déconnexion d'un client | | | | | | |
| 6 | Achats de test, reconnexion | | | | | | |
| 7 | Format téléphone, chaque panneau | | | | | | |
| 8 | Charge | | | | | | |
| 9 | Jour suivant | | | | | | |
| 10 | Exploits signalés par l'économie et le fun | | | | | | |
| 11 | Session complète, console | | | | | | |
| 12 | PC plein écran (≥ 1920×1080), chaque panneau | | | | | | |
| 13 | Stabilité des panneaux, 30 s, état réel, PC et téléphone | | 0 instable | | | | |
| 14 | Monde vu de dessus, du niveau de l'eau, de biais | | Aucun dessous plat ou vide | | | | |
| 15 | Liste des joueurs et `leaderstats` sur PC, 2 joueurs | | HUD dégagé | | | | |

### Stabilité des panneaux (scénario 13)

Résultat de `OUTILS\luau\stabilite-panneaux.luau`, une ligne par panneau et par format. État du joueur pendant la mesure : …

| Panneau | Format (taille lue) | Panneaux suivis | Échantillons | Instables | Verdict |
|---|---|---|---|---|---|
| | | | | | |

## Défauts

**P0** bloque ou perd des données ; **P1** casse une promesse du jeu ; **P2** gêne ; **P3** détail.

| # | Gravité | Scénario | Étapes | Attendu | Observé | Preuve | Certain ? |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |

## Console

| Erreur ou avertissement | Côté | Fois | Scénario | Ligne de code | Certain ? |
|---|---|---|---|---|---|
| | | | | | |

## Qualification indépendante

| Axe | Note /10 | Preuve |
|---|---|---|
| 1. 3D et cohérence | | |
| 2. Lisibilité de la boucle | | |
| 3. Interface mobile | | |
| 4. Boucle et rétention | | |
| 5. Monétisation | | |
| 6. Image de vignette | | |
| **Moyenne** | | |

| Cible | Verdict | Conditions |
|---|---|---|
| Bêta fermée | oui / oui sous conditions / non | C1 … |
| Public | | |

## Corrections demandées, par impact

1. …

## Non vérifié

Ce qui reste à voir, et ce qu'il faudrait pour le voir.

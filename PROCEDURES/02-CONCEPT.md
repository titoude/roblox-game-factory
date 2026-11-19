# 02 — Fiche concept

**Qui** : Claude Fable 5.2, effort high (repli autorisé : Opus 5.5 effort medium). Un seul agent.
**But** : transformer un thème de la veille en une fiche qu'on peut vérifier, chiffrer et construire.

## Entrées

- `VEILLE\TENDANCES.md`, `VEILLE\IDEES-CANDIDATES.md`, le dossier de thème (mission B) quand il existe.
- `CONNAISSANCES\REGLES.md` (§ Concept, Économie, Fun), `LECONS-ARCHIPEL.md`, `seuils.json`.
- En itération : le rapport qui a refusé la version précédente.

## Déroulé

1. **Trois pistes** de 8 lignes chacune : promesse d'action, différence visible, première minute, pourquoi inviter un ami, pourquoi revenir demain, risque principal.
2. **Choix** d'une piste par une grille notée de 1 à 5 : démontrable en une vignette, première action en 60 s, différence réelle avec les 10 gagnants du thème, tient dans le périmètre (règle C4), raison sociale crédible, coût de contenu soutenable. Le choix et les notes restent dans la fiche.
3. **Fiche complète** d'après `OUTILS\GABARITS\FICHE-CONCEPT.md`.
4. **Auto-contrôle** contre la liste ci-dessous avant de rendre.

## Ce que la fiche contient (porte P1)

| # | Élément | Critère de complétude |
|---|---|---|
| 1 | Promesse d'action | Une phrase, verbe d'action, montrable dans une image fixe |
| 2 | Différence visible | Nommée par rapport à 3 jeux précis du corpus ; se voit en capture, pas dans les règles |
| 3 | Boucle de progression | Action → résultat → monnaie → amélioration → prochain objectif, avec les 6 premiers paliers chiffrés |
| 4 | Boucle sociale | Pourquoi inviter un ami, quelle scène on raconte ; taille de serveur visée |
| 5 | Monétisation | Règle en une phrase vérifiable dans le code ; 3 à 5 offres, chacune typée confort, temps ou expression |
| 6 | Coût de contenu et de modération | Nombre d'objets, de niveaux, de textes ; ce qui demande une modération (chat, noms, créations de joueurs) |
| 7 | Données | Les 10 gagnants et 10 faibles du thème, avec leurs moyennes de CCU et leurs sources |

Trois contrôles de cohérence, ajoutés au bilan du cycle 2 (le juge de P1 les fait lui-même, phrase par phrase) :

- **Promesse monotone (C10)** : la grandeur qui porte la promesse ne baisse jamais et progresse entre 61 et 180 s ; l'annexe A est calculée à partir du parcours détaillé, pas du résumé.
- **Visible d'où (C11)** : si la fiche fixe la caméra, les commandes ou le parcours, chaque « visible », « voit », « sous les yeux », « en face » dit d'où on le voit ; l'annexe A dit ce qui est dans le cadre à 0 s, 60 s et 5 min.
- **Trace du geste (F11)** : le résultat du geste reste visible jusqu'à la fin de la session ; toute remise à zéro est un événement montré.

Plus quatre annexes obligatoires :

- **Les 60 premières secondes**, seconde par seconde : ce que voit le joueur, ce qu'il fait, ce qu'il gagne. Aucun menu, aucun texte de plus de 8 mots avant la première action.
- **Périmètre** : 1 boucle principale, 1 boucle sociale, 1 méta-progression ; liste de ce qui est volontairement exclu de la v1.
- **Prévisions chiffrées** (règle C9) : temps jusqu'à la première action, écart maximal entre achats, durée de contenu actif, J1 et durée de session attendus. Le bilan les comparera au mesuré.
- **Critères d'arrêt** propres au jeu : ce qui, observé en bêta, ferait abandonner ; et, pour le prototype (porte P4), un **arrêt ferme et mesuré** écrit d'avance (latence, rythme, première montée, progression de 61 à 180 s, note de plaisir), dont le seuil n'est pas révisé après la mesure (A9).

## Interdits

- Recréer un jeu existant ou utiliser une licence (G13). « Inspiré de l'action X » est permis, « comme le jeu Y avec un autre nom » ne l'est pas.
- Vendre du pouvoir contre d'autres joueurs, des tirages aléatoires payants (G6, E6, E13).
- Inventer un chiffre de marché : ce qui n'est pas dans la veille est `NP`.
- Empiler les systèmes pour rassurer : une fiche plus courte et plus nette passe mieux les portes suivantes.

## Itérations

Refus en P1, P2 ou P3 : le concepteur reçoit le rapport de refus et rend une version 2 qui dit, en tête, ce qui a changé. Deux retours au concepteur au plus par porte (`seuils.json`), le troisième échec abandonne l'idée (A5) et l'orchestrateur prend la piste suivante. Le concepteur dispose du simulateur (`OUTILS\sim-economie.py`) et le lance avant de rendre une fiche : une annexe chiffrée ne s'écrit pas de tête.

## Prompt type (concepteur)

```
Tu es concepteur de jeu de l'usine Roblox. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md, PROCEDURES\02-CONCEPT.md, CONNAISSANCES\REGLES.md (Concept, Économie, Fun), CONNAISSANCES\LECONS-ARCHIPEL.md, VEILLE\TENDANCES.md et VEILLE\IDEES-CANDIDATES.md.
Thème pressenti : <thème>. Dossier de thème : <fichiers de la mission B>.
<En itération : « Version précédente refusée : lis <rapport>. Dis en tête de fiche ce qui change. »>
Travail : trois pistes, choix argumenté par la grille, puis fiche complète d'après OUTILS\GABARITS\FICHE-CONCEPT.md, avec les 60 premières secondes, le périmètre, les prévisions chiffrées et les critères d'arrêt.
Tu n'ouvres ni Studio ni navigateur. Tu n'inventes aucun chiffre de marché. Tu ne lances aucun sous-agent.
Sortie : JEUX\<slug>\02-concept\FICHE-CONCEPT.md. Une leçon à proposer va dans CONNAISSANCES\PROPOSITIONS\.
Dernière ligne : RESULTAT: <ok|echec|arret> | <fichier> | <promesse du jeu en une phrase>.
```

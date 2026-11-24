# 09 — Bilan et auto-amélioration

**Qui** : l'orchestrateur, seul à écrire dans `CONNAISSANCES\`. Un agent Codex `gpt-6.1-sol` (effort high) peut préparer les tableaux prévu/mesuré.
**But** : que le jeu suivant parte avec de meilleures règles que celui-ci. Les règles changent sur des mesures, pas sur des impressions.

## Quand

- À la fin de chaque jeu, **qu'il soit lancé ou arrêté** à une porte.
- À 30 jours après une mise en public (bilan de suivi, même gabarit, sections de mesure seulement).
- Un mini-bilan de dix lignes à chaque échec de porte, dans le `JOURNAL.md` du jeu : ce que la porte a vu, ce qui aurait permis de le voir plus tôt.

## Entrées

- `ETAT.json` et `JOURNAL.md` du jeu : portes, itérations, dérogations, modes dégradés, délégations (modèle, effort, durée).
- Les prévisions de la fiche concept et la simulation économique.
- Les mesures : chronométrages de la QA, cohortes et entonnoir de la bêta, journal des campagnes.
- `ALERTES.md` : chaque arrêt sur une frontière humaine.
- `CONNAISSANCES\PROPOSITIONS\` : tout ce qui est en attente.

## Déroulé

1. **Prévu contre mesuré.** Remplir `JEUX\<slug>\09-bilan\BILAN.md` (gabarit `OUTILS\GABARITS\BILAN.md`) : pour chaque prévision de la fiche, la valeur mesurée, l'écart, la source de la mesure. Une mesure absente s'écrit `NP`, avec la raison.
2. **Les portes ont-elles eu raison ?** Pour chaque porte : ce qu'elle a laissé passer et qui a cassé plus loin (faux positif) ; ce qu'elle a refusé à tort (faux négatif, quand on peut le savoir). Une porte qui ne refuse jamais rien ne mesure rien.
3. **Coût.** Durée et nombre de délégations par étape, itérations, temps perdu sur des blocages. Où l'usine a-t-elle attendu un humain ?
4. **Causes, pas symptômes.** Pour les trois plus gros écarts : quelle règle manquait, laquelle était fausse, laquelle n'a pas été appliquée ?
5. **Traiter les propositions.** Pour chaque fichier de `PROPOSITIONS\` : fusionner, refuser ou reporter ; écrire la décision dans le fichier ; le déplacer dans `traitees\`.
6. **Mettre à jour la mémoire, sans étape manuelle.** Écrire `JEUX\<slug>\09-bilan\BILAN.json` (gabarit `OUTILS\GABARITS\BILAN.exemple.json`) : prévisions avec prévu, mesuré, source et `facteur_applique` ; portes, avec chaque faux positif prouvé et la règle vérifiable qui l'aurait arrêté ; leçons, confirmations et contradictions de règles, chacune avec sa preuve ; seuils mesurés et valeur proposée. Puis lancer `python usine.py bilan <slug>` (ou `python OUTILS\boucle-amelioration.py appliquer --jeu <slug> --commit`). La boucle applique les conditions du tableau ci-dessous et refuse ce qui ne les remplit pas :
   - facteur mesuré/prévu de chaque prévision dans `CONNAISSANCES\CALIBRATION.json` (médiane sur les jeux) ; écart au-delà de `seuils.json` § `bilan.ecart_tolere_pct` : règle de calibration `à calibrer`, promue `active` quand un autre jeu qui l'a appliquée tombe dans la tolérance ;
   - faux positif de porte, leçon : nouvelle règle `à calibrer` dans le domaine de la porte ; confirmation par un autre jeu : `active` ; contradiction : barrée, `retirée`, raison gardée ;
   - seuil : changé sur deux jeux (médiane des valeurs proposées) ou un écart massif expliqué, jamais si un jeu en cours est en échec ou en dérogation sur la porte (A4) ; version incrémentée, ligne d'historique dans `SEUILS-PORTES.md` ;
   - propositions jugées par le rôle `09.juge-propositions` (Codex, sans repli Opus), décision écrite, fichier dans `traitees\` ; sans juge, elles attendent et P9 ne passe pas ;
   - bloc « Leçons des bilans » de chaque skill concerné (règles des bilans et facteurs de calibration), que le jeu suivant lit ;
   - `CONNAISSANCES\PROGRES.json` : écart moyen prévu/mesuré et faux positifs des portes, comparés au jeu précédent.
   Le battement (`OUTILS\battement.py`) lance la boucle seul pour tout `BILAN.json` non appliqué.
7. **Clore.** La boucle écrit `CONNAISSANCES\BILANS\AAAA-MM-JJ-<slug>.md`, la porte P9 dans `ETAT.json` et le commit `[orchestrateur] Bilan <slug> : …`. Compléter `JOURNAL-DES-JEUX.md` et ses compteurs. Skills modifiés : le rapport le dit au propriétaire (`installer-skills.ps1 -Confirmer`, G17).

## Ce qui peut changer, et à quelles conditions

| Cible | Changement | Condition |
|---|---|---|
| `REGLES.md` | Ajouter une règle | Un constat prouvé (fichier, capture, mesure) et une formulation vérifiable. Nouvel identifiant, origine `BILAN <slug>` |
| `REGLES.md` | Passer une règle de `à calibrer` à `active` | Confirmée par la mesure sur un jeu au moins |
| `REGLES.md` | Retirer une règle | Contredite par la mesure, ou jamais applicable. Elle reste, barrée, avec la raison |
| `seuils.json` | Changer un seuil | Mesures de **deux jeux** au moins, ou d'un seul si l'écart est massif et expliqué. Ligne dans l'historique de `SEUILS-PORTES.md` : avant, après, preuve. Incrémenter `version` |
| `PROCEDURES\` | Corriger une étape, un prompt type | Un blocage ou un malentendu constaté dans le journal |
| `OUTILS\GABARITS\` | Ajouter un champ | Une information qui a manqué à une décision |
| `skills\` | Corriger un skill | Seulement si la procédure pointée ne suffit plus. Les skills sont des pointeurs minces : après modification, le dire au propriétaire, qui relance `OUTILS\installer-skills.ps1` |
| `MODELES-ET-QUOTAS.md` | Changer un modèle ou un effort pour une étape | Comparaison sur pièces (même tâche, deux réglages) ou échecs répétés |
| `GARDE-FOUS.md`, `PLAFONDS.md` | — | Jamais par un agent. Une suggestion va dans le compte rendu au propriétaire |

Règles d'hygiène :

- Une leçon par changement, un commit par bilan : `[orchestrateur] Bilan <slug> : <n> règles, <n> seuils`.
- Ne pas généraliser d'un seul jeu : une leçon tirée d'un cas s'écrit `à calibrer`.
- Ne pas empiler : avant d'ajouter une règle, chercher celle qu'elle remplace ou précise. Au-delà de 80 règles actives, fusionner.
- Ne jamais durcir ou assouplir un seuil pour faire passer le jeu en cours (A4).
- Relire `CONNAISSANCES\SOURCES-VEILLE.md` : la vérification mensuelle des conditions est-elle à jour ?

## Porte P9

Passe si : bilan écrit avec ses sources, toutes les propositions traitées, mémoire mise à jour et commitée, journal des jeux complété. Le jeu suivant ne démarre pas avant.

## Prompt type (préparation des tableaux)

```
Tu es analyste du bilan de l'usine Roblox. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md et PROCEDURES\09-BILAN.md.
Jeu : <slug>. Pièces : JEUX\<slug>\ETAT.json, JOURNAL.md, 02-concept\FICHE-CONCEPT.md (prévisions), 03-economie\SIMULATION.md, 06-qa\RAPPORT-QA-*.md, 08-distribution\JOURNAL-CAMPAGNES.md.
Travail : remplis les tableaux « prévu contre mesuré », « portes » et « coût » de OUTILS\GABARITS\BILAN.md, et les champs previsions, portes (résultat seulement) et cout de JEUX\<slug>\09-bilan\BILAN.json (gabarit OUTILS\GABARITS\BILAN.exemple.json). Chaque mesure avec sa source ; mesure absente = NP et sa raison. Ne conclus pas, ne propose pas de règle : c'est l'orchestrateur qui décide.
Lecture seule sur tout le reste. N'écris pas dans CONNAISSANCES\. Aucun sous-agent. Ne lance pas la boucle d'amélioration : c'est l'orchestrateur.
Sortie : JEUX\<slug>\09-bilan\TABLEAUX.md et JEUX\<slug>\09-bilan\BILAN.json.
Dernière ligne : RESULTAT: <ok|echec|arret> | <fichier> | <nombre de prévisions, dont mesurées>.
```

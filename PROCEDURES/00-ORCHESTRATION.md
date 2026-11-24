# 00 — Orchestration

**Qui** : l'orchestrateur, Claude Opus 5.5, effort moyen (repli : Fable 5.2), soit dans un fil T3 Code, soit lancé sans interface par `python usine.py "fais un jeu"` (procédure 13).
**But** : faire passer un jeu par la chaîne, porte après porte, sans intervention humaine hors des frontières du garde-fou G7.

## 1. Ouverture de session (toujours)

1. `GARDE-FOUS.md`. Fichier `STOP` présent : s'arrêter.
2. `powershell -File OUTILS\verifier-usine.ps1` : structure, secrets, alertes ouvertes, verrous restants, espace disque. Un verrou orphelin se libère seulement après avoir vérifié qu'aucun agent ne tourne.
3. `ALERTES.md` : toute alerte « ouverte » concerne-t-elle l'étape à venir ?
4. `CONNAISSANCES\PLAFONDS.md` : ce qui est autorisé aujourd'hui.
5. `powershell -File OUTILS\etat.ps1 -Liste` : où en est chaque jeu.
6. Reprise après compaction ou nouveau tour : `python OUTILS\historique.py demandes` (texte exact des demandes du propriétaire dans la session courante), `python OUTILS\historique.py sessions` (tours et enfants précédents, Claude et Codex) puis `chercher "<mot>" --session <id>` pour retrouver une décision, un chemin ou une erreur. Le résumé d'une compaction n'est pas une source : en cas de doute, la transcription fait foi. Sous Claude Code, le crochet `SessionStart` (déclencheur `compact`) de `.claude\settings.json` injecte ces demandes et ces commandes automatiquement.
7. Avant la première délégation : `python OUTILS\deleguer.py --liste` (rôles, modèles, places libres) ; dans T3 Code, aussi `orchestrator_capabilities`. Le modèle d'un rôle vient de `CONNAISSANCES\routage.json`, jamais d'un prompt (procédure 13).

## 2. Commandes reconnues

| Demande du propriétaire | Action |
|---|---|
| « fais un jeu », « cycle » ou rien de précis | **Cycle complet, sans question au propriétaire** : reprendre le jeu en cours à son étape ; s'il n'y en a pas (ou s'il vient d'être arrêté), veille si elle a plus de 7 jours, puis nouveau jeu, puis toute la chaîne jusqu'à la publication permise par `PLAFONDS.md`, puis les boucles d'exploitation (retours joueurs, mesures, promotion préparée) |
| « retours `<slug>` » | Procédure 11 : collecte, tri, jugement, lot de propositions, cycle d'amélioration |
| « promo `<slug>` » | Procédure 12 : préparer la campagne de vidéos courtes ; rien n'est mis en ligne sans compte ni ligne dans `PLAFONDS.md` § 3 |
| « veille » | Procédure 01 seule, mise à jour de `VEILLE\TENDANCES.md` |
| « nouveau jeu » | Vérifier que la veille a moins de 7 jours, puis `OUTILS\nouveau-jeu.ps1` et procédure 02 |
| « reprendre `<slug>` » | Lire `JEUX\<slug>\ETAT.json`, continuer |
| « bilan `<slug>` » | Procédure 09 ; `python usine.py bilan <slug>` applique `09-bilan\BILAN.json` (boucle d'amélioration) |
| « état » | `etat.ps1 -Liste`, alertes ouvertes, rien d'autre |

Un seul jeu en production à la fois. Une veille peut tourner pendant qu'un jeu est en QA.

## 3. Boucle d'un jeu

Pour l'étape courante de `ETAT.json` :

1. Lire la procédure de l'étape et le gabarit de sa sortie.
2. Préparer les entrées (fichiers, pas de résumé oral).
3. Déléguer avec le prompt type de la procédure, complété. Noter la délégation dans `JEUX\<slug>\JOURNAL.md`.
4. Recevoir la dernière ligne `RESULTAT: …` ; lire le fichier de sortie si la décision en dépend.
5. Juger la porte contre `seuils.json`, sans indulgence : `etat.ps1 -Jeu <slug> -Porte Pn -Resultat passe|echec|derogation|a_confirmer -Preuve <fichier>`. `a_confirmer` sert quand l'avis vient d'une revue non indépendante ou d'un mode dégradé (règle A8) : il n'avance pas l'étape et ne compte pas d'itération. La porte P0 se juge dans l'état du jeu créé pour le thème, juste après `nouveau-jeu.ps1`.
6. Commit du lot (`JEUX\<slug>\…`), message terminé par la ligne de co-signature.
7. Passe : étape suivante. Échec : retour prévu par la procédure, compteur d'itérations + 1. Compteur au maximum : arrêt du jeu (§ 6).

| Étape | Procédure | Délégué à | Sortie attendue | Porte |
|---|---|---|---|---|
| 01 Veille | `01-VEILLE-NAVIGATEUR.md` | 1 à 3 gpt-6.1-sol | `VEILLE\RELEVES\<date>\*.md`, puis `VEILLE\TENDANCES.md` (orchestrateur) | P0 |
| 02 Concept | `02-CONCEPT.md` | Fable 5.2 | `02-concept\FICHE-CONCEPT.md` | P1 |
| 03 Économie | `03-REVUE-ECONOMIE.md` | 2 gpt-6.1-sol | `03-economie\economie.json`, `RAPPORT-ECONOMIE.md` | P2 |
| 04 Fun | `04-REVUE-FUN.md` | Opus 5.5 | `04-fun\RAPPORT-FUN.md` | P3 |
| 05 Production | `05-PRODUCTION-STUDIO.md` | Orchestrateur (plan), puis Opus 5.5 (seul écrivain) | `05-production\PLAN-PRODUCTION.md`, puis `src\`, `JOURNAL-LOTS.md` | P4 puis fin des lots |
| 06 QA | `06-QA-MULTIJOUEUR.md` | gpt-6.1-sol, Fable | `06-qa\RAPPORT-QA-<n>.md` | P5 |
| 07 Release | `07-RELEASE.md` | Orchestrateur + 1 gpt-6.1-sol | `07-release\CHECKLIST-RELEASE.md`, `MANIFESTE-IDS.json` | P6 |
| 08 Distribution | `08-DISTRIBUTION.md` | Orchestrateur | `08-distribution\KIT-LANCEMENT.md`, `JOURNAL-CAMPAGNES.md` | P7, P8 |
| 09 Bilan | `09-BILAN.md` | Orchestrateur + 1 gpt-6.1-sol | `09-bilan\BILAN.md`, `CONNAISSANCES\` mis à jour | P9 |
| 11 Retours joueurs (jeu publié, en boucle) | `11-RETOURS-JOUEURS.md` | Orchestrateur + 1 gpt-6.1-sol (juge) | `10-retours\LOT-*.md`, `PROPOSITIONS-*.md` | P10 : chaque groupe jugé, propositions retenues inscrites au prochain lot |
| 12 Promotion (facultative) | `12-PROMOTION-VIDEO.md` | Fable 5.2 (scénarios), gpt-6.1-sol (veille, montage) | `08-distribution\PLAN-VIDEOS.md`, `JOURNAL-VIDEOS.md` | P11 : améliorer, continuer ou passer au jeu suivant |

Le rôle à passer à `deleguer.py` pour chaque étape (`01.veilleur`, `03.calcul`, `05.codeur`, …) est dans `CONNAISSANCES\routage.json`. Depuis le 16/11/2026 (consigne du propriétaire, `PLAFONDS.md` § 4), veille, code, tests et analyses passent par `gpt-6.1-sol` ; Haiku n'est plus qu'un repli de dernier rang, marqué « à confirmer ».

## 4. Règles de délégation

- **Prompt autonome** (règle A1). L'enfant ne voit pas la conversation. Le prompt donne : la racine de l'usine, le rôle, « lis d'abord `GARDE-FOUS.md` et `PROCEDURES\<nn>` », les fichiers d'entrée, le fichier de sortie exact, ce qu'il ne doit pas faire, la dernière ligne attendue. Aucun secret dans un prompt.
- **Simultanéité** : compter les agents Opus, Fable, Sonnet en cours avant d'en lancer un. Deux au plus, **orchestrateur compris** (`PLAFONDS.md` § 4, `routage.json`) : un seul enfant Claude fort à la fois. Les lots parallèles n'existent que pour Codex.
- **Un écrivain** : avant de lancer le producteur, vérifier qu'aucun verrou `place:` n'est pris. Ne jamais lancer deux agents qui écrivent dans la même place, ni un écrivain pendant un audit de code (règle E10 : l'audit lit un commit).
- **Indépendance** : le relecteur n'a pas écrit ce qu'il relit (A2). Ne pas donner au relecteur la conclusion attendue ; lui donner les pièces.
- **Pas de sondage** : une délégation asynchrone prévient quand elle finit. En attendant, avancer sur ce qui n'en dépend pas.
- **Ne rien modifier de ce qu'un sous-agent lit pendant qu'il tourne** : fiche, procédures, règles, seuils, outils (règle E10). L'orchestrateur avance pendant ce temps sur les livrables que l'agent ne lit pas, et donne à l'agent le commit de ses entrées.
- **Sous-agent bloqué** (ligne `RESULTAT: arret`) : lire l'alerte, ne pas relancer à l'identique. Soit l'obstacle est une frontière humaine (§ 5), soit le prompt était insuffisant et on le corrige.

## 5. Frontières humaines

CAPTCHA, conditions d'utilisation, double authentification, connexion, paiement, permission, propriété : l'agent concerné s'arrête et écrit une alerte. L'orchestrateur :

1. vérifie l'alerte dans `ALERTES.md` ;
2. met le jeu en `bloque` si l'étape ne peut pas continuer (`etat.ps1 -Jeu <slug> -Statut bloque -Note "…"`) ;
3. continue tout travail qui n'en dépend pas (veille, bilan, autre jeu en conception) ;
4. en fin de tour, dit au propriétaire en une phrase ce qu'il doit faire. Pour un code ou une connexion que lui seul peut fournir, utiliser l'outil de demande de secret de T3 Code, jamais une demande en clair dans la conversation.

## 6. Arrêter un jeu

L'usine préfère tuer une idée que la traîner. On arrête quand :

- une porte de conception (P1, P2, P3) échoue encore après 2 retours au concepteur (c'est le troisième échec qui arrête ; voir la règle A5 révisée) ;
- la QA échoue après 3 cycles sans baisse du nombre de défauts P0 et P1 ;
- la bêta reste sous les seuils P7 après deux corrections de l'arrivée et de la boucle ;
- le jeu exigerait d'enfreindre un garde-fou.

Arrêt = `etat.ps1 -Jeu <slug> -Statut arrete -Note "<raison>"`, bilan court (procédure 09), ligne dans le journal des jeux. Pas de question au propriétaire pour cela : la décision est dans les règles.

## 7. Ce que l'orchestrateur ne fait pas

- Abaisser un seuil en cours de jeu (règle A4) ; une dérogation s'écrit avec sa raison.
- Dépenser, publier en public, annoncer sans ligne dans `PLAFONDS.md`.
- Produire et relire le même travail.
- Garder en mémoire de conversation ce qui doit vivre dans un fichier : état, décisions et preuves sont sur disque, pour qu'une nouvelle session reprenne sans perte.

## 8. Fin de session

1. Tous les verrous rendus (`verrou.ps1 liste`).
2. `ETAT.json` et `JOURNAL.md` du jeu à jour, commit fait.
3. Compte rendu au propriétaire en 10 lignes : étape atteinte, portes jugées avec leur preuve, alertes ouvertes, prochaine action. Ce qui n'a pas été vérifié est dit comme tel.

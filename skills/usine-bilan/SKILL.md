---
name: usine-bilan
description: Bilan d'un jeu de l'usine Roblox et auto-amélioration - compare le prévu au mesuré, juge si les portes ont eu raison, chiffre le coût, traite les propositions des agents et met à jour les règles, les seuils et les procédures dans le dossier CONNAISSANCES. À utiliser à la fin de chaque jeu (lancé ou arrêté), à 30 jours après une mise en public, ou pour préparer les tableaux d'un bilan.
---

# Bilan de l'usine Roblox

Racine de l'usine : `%USERPROFILE%\Documents\Projets\USINE-ROBLOX` (ou `USINE_ROBLOX`).

Le jeu suivant doit partir avec de meilleures règles. Les règles changent sur des mesures, pas sur des impressions. **Seul l'orchestrateur écrit dans `CONNAISSANCES\`** ; un analyste prépare les tableaux sans conclure.

## Avant tout

Lis `GARDE-FOUS.md`, `PROCEDURES\09-BILAN.md` (elle fait foi) et `CONNAISSANCES\00-LISEZ-MOI.md`.

## Entrées

`JEUX\<slug>\ETAT.json` et `JOURNAL.md` ; prévisions de la fiche concept ; simulation économique ; rapports de QA ; journal des campagnes ; `ALERTES.md` ; `CONNAISSANCES\PROPOSITIONS\`.

## Déroulé (orchestrateur)

1. **Prévu contre mesuré** dans `JEUX\<slug>\09-bilan\BILAN.md` (gabarit `OUTILS\GABARITS\BILAN.md`). Mesure absente : `NP` et sa raison.
2. **Les portes ont-elles eu raison ?** Ce qu'elles ont laissé passer et qui a cassé plus loin ; ce qu'elles ont refusé à tort.
3. **Coût** : délégations, durée, itérations, attentes d'un humain.
4. **Causes** des trois plus gros écarts : règle manquante, fausse ou non appliquée.
5. **Propositions** : fusionner, refuser ou reporter chaque fichier ; écrire la décision ; déplacer dans `traitees\`.
6. **Mémoire, sans étape manuelle** : écrire `JEUX\<slug>\09-bilan\BILAN.json` (gabarit `OUTILS\GABARITS\BILAN.exemple.json`), poser `"pret": true` en dernier, puis `python usine.py bilan <slug>`. La boucle (`OUTILS\boucle-amelioration.py`) écrit règles, seuils, facteurs de calibration, décisions des propositions, bloc « Leçons des bilans » des skills et `PROGRES.json`, aux conditions ci-dessous. Procédures et gabarits restent à corriger à la main.
7. **Clore** : la boucle écrit `CONNAISSANCES\BILANS\`, la porte P9 et le commit `[orchestrateur] Bilan <slug> : …` ; compléter `JOURNAL-DES-JEUX.md` et ses compteurs.

## Conditions d'un changement

- Nouvelle règle : constat prouvé, formulation vérifiable, origine `BILAN <slug>`. Tirée d'un seul jeu : statut `à calibrer`.
- Seuil : mesures de deux jeux, ou d'un seul si l'écart est massif et expliqué ; ligne dans l'historique (avant, après, preuve) ; version incrémentée.
- Règle retirée : elle reste, barrée, avec la raison.
- Avant d'ajouter, chercher la règle que la nouvelle remplace. Au-delà de 80 règles actives : fusionner.
- Jamais de seuil modifié pour faire passer le jeu en cours.
- `GARDE-FOUS.md` et `PLAFONDS.md` : jamais par un agent ; une suggestion va dans le compte rendu au propriétaire.
- Skill modifié : le dire au propriétaire, qui relance `OUTILS\installer-skills.ps1 -Confirmer`.

## Analyste des tableaux

Remplit `JEUX\<slug>\09-bilan\TABLEAUX.md` (prévu contre mesuré, portes, coût) et les champs `previsions`, `portes` et `cout` de `BILAN.json`, chaque mesure avec sa source. Ne conclut pas, ne propose pas de règle, n'écrit pas dans `CONNAISSANCES\`. Aucun sous-agent.

Dernière ligne de l'analyste : `RESULTAT: <ok|echec|arret> | <fichier> | <nombre de prévisions, dont mesurées>`.

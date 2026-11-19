---
name: usine-qa-multijoueur
description: QA et test multijoueur d'un jeu Roblox de l'usine dans Studio - solo outillé, serveur local avec plusieurs clients, ou place privée. À utiliser pour jouer des scénarios de test en Play, relever la console, vérifier sauvegarde, achats, interface téléphone et interactions entre joueurs, rédiger un rapport de QA ou une qualification indépendante. Ne modifie jamais la place.
---

# QA de l'usine Roblox

Racine de l'usine : `%USERPROFILE%\Documents\Projets\USINE-ROBLOX` (ou `USINE_ROBLOX`).

Tu qualifies le jeu par ce qui est **vu en jeu**. Personne n'écrit dans la place pendant la QA : Play uniquement, ni mode Edit, ni `save_place`. Un défaut se décrit ; le producteur le corrige au cycle suivant.

## Avant tout

Lis `GARDE-FOUS.md`, `PROCEDURES\06-QA-MULTIJOUEUR.md` (elle fait foi), `CONNAISSANCES\REGLES.md` (QA) et `CONNAISSANCES\seuils.json` (sections `qa`, `prototype`). Ton prompt donne ton rôle.

## Rôles

- **Chef de test** (orchestrateur) : monte le test, attribue une instance Studio à chaque testeur, rédige le rapport. Pour lancer « Clients et serveurs » dans Studio : verrou `bureau`, puis `OUTILS\cu.ps1` avec `-attendu "Roblox Studio"`.
- **Testeur** : joue ses scénarios sur **son** instance par MCP (`execute_luau` côté client, `screen_capture`, `get_console_output`). Ne touche ni à la souris ni au clavier, ni aux autres instances, n'arrête pas le test.
- **Analyste** : rattache chaque erreur de console à un scénario et à une ligne du commit testé. Lecture seule.
- **Qualification indépendante** : note 6 axes sur 10 et rend un verdict par cible (bêta fermée, public) avec conditions numérotées. N'a pas produit le jeu.

## Niveaux

- **A** solo outillé (toujours faisable) ; **B** serveur local + 2 à 4 clients ; **C** place privée et comptes réels du propriétaire.
- La porte P5 exige B ou C. Si B n'a pas pu être monté, le rapport dit pourquoi et ce qui l'a remplacé. Tu ne crées jamais de compte.

## Scénarios minimaux

Arrivée et première action (≤ 60 s) ; dix minutes de boucle ; quitter et revenir, en pleine action, arrêt du serveur ; interaction à deux ; déconnexion d'un client ; achats de test puis reconnexion ; chaque panneau au format téléphone **et** en PC plein écran (1920×1080 au moins) ; stabilité des panneaux mesurée 30 s avec l'état réel d'un joueur (`OUTILS\luau\stabilite-panneaux.luau`) ; monde vu de dessus, du niveau de l'eau et de biais ; liste des joueurs de Roblox sur PC à 2 joueurs ; charge ; jour suivant ; exploits signalés par les revues ; session complète sans erreur console.

Le bureau (souris, clavier) est le dernier recours : MCP Studio et API d'abord (règle A7).

## Rapport

`JEUX\<slug>\06-qa\RAPPORT-QA-<n>.md` d'après `OUTILS\GABARITS\RAPPORT-QA.md` (testeur : `notes-<nom>.md`).

- Chaque constat : **vu** (capture, mesure), **lu** (code) ou **non vérifiable**.
- Gravité P0 à P3. Un défaut porte scénario, étapes, attendu, observé, preuve, commit testé.
- Captures dans `06-qa\captures\` (hors git), citées par leur nom.

Aucun sous-agent (sauf le chef de test, qui est l'orchestrateur).

Dernière ligne : `RESULTAT: <ok|echec|arret> | <fichier> | <scénarios joués, défauts P0 et P1 vus>`.

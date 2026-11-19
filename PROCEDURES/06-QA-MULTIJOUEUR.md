# 06 — QA et test multijoueur

**Qui** : l'orchestrateur en chef de test ; 2 à 4 testeurs Claude Haiku 5.5 (effort high) ; 1 à 2 analystes Codex `gpt-6.1-sol` (console, code) ; 1 qualification indépendante Claude Fable 5.2.
**But** : qualifier le jeu par ce qui est **vu en jeu**, à plusieurs joueurs, avant toute sortie.
**Personne n'écrit dans la place** pendant la QA : Play uniquement, pas de mode Edit, pas de `save_place`. Un défaut se décrit ; le producteur le corrige au cycle suivant.

## Trois niveaux de test

| Niveau | Montage | Ce qu'il prouve | Dépend de |
|---|---|---|---|
| **A. Solo outillé** | Un Play via MCP ; second joueur simulé par les actions de test du jeu (joueur fictif, saut de temps, remplissage) | Boucle, économie, sauvegarde, console, interface | Rien : toujours faisable |
| **B. Serveur local + N clients** | Studio, onglet Test, « Clients et serveurs » : 1 serveur local et 2 à 4 clients | Vraie réplication, interactions entre joueurs, déconnexion d'un client | Lancement par l'interface de Studio (`OUTILS\cu.ps1`, verrou `bureau`) ; pilotage de chaque fenêtre par MCP à confirmer |
| **C. Place privée, comptes réels** | Jeu publié en TEST privé, plusieurs appareils ou comptes | DataStores réels, classements, vrais téléphones | Comptes et appareils du propriétaire : jamais créés par un agent |

La porte P5 exige le niveau B (ou C). Le niveau A seul ne suffit pas : c'est la leçon d'Archipel.

## Montage du niveau B

1. Chef de test : verrou `bureau`, puis dans Studio lancer le test « Clients et serveurs » avec N clients. Le lancement passe par l'interface : `cu.ps1 focus "Roblox Studio"`, capture, clic vérifié (`-attendu "Roblox Studio"`).
2. `list_roblox_studios` : relever les instances apparues (serveur, clients). Attribuer une instance à chaque testeur et le dire dans son prompt.
3. Chaque testeur agit **par MCP sur son instance** : `execute_luau` côté client (déplacer son personnage, déclencher ses Remotes, lire son interface), `screen_capture`, `get_console_output`. Il ne touche ni à la souris ni au clavier : le bureau reste au chef de test.
4. L'analyste lit la console du serveur pendant la séance.
5. Fin : le chef de test arrête le test, rend le verrou.

Si les fenêtres clientes ne sont pas pilotables séparément par MCP dans la version installée : les testeurs jouent à tour de rôle sous le verrou `bureau`, ou le test se fait au niveau A complété par un niveau C avec le propriétaire. Le rapport dit lequel a eu lieu.

## Plan de test minimal

| # | Scénario | Niveau | Attendu |
|---|---|---|---|
| 1 | Arrivée d'un nouveau joueur, chronomètre jusqu'à la première action | A, B | ≤ 60 s, sans lire |
| 2 | Dix minutes de boucle sans aide | A | Un achat utile au plus toutes les 2 min ; toujours un objectif affiché |
| 3 | Quitter et revenir ; quitter en pleine action ; arrêt du serveur | A, B | État identique, rien de doublé, rien de perdu |
| 4 | Interaction entre deux joueurs prévue par la fiche | B | Les deux clients voient le même résultat |
| 5 | Un client se déconnecte pendant l'interaction | B | Pas d'erreur, pas d'enjeu retiré ni dupliqué |
| 6 | Achat de test de chaque offre, puis reconnexion | A | Accordé une fois ; offre à identifiant 0 invisible |
| 7 | Format téléphone : chaque panneau | A | Aucun chevauchement, boutons ≥ 48 px, barre Roblox dégagée |
| 12 | Format PC plein écran (1920×1080 au moins) : chaque panneau, **en plus** du téléphone (Q8) | A | Mêmes critères qu'au scénario 7 ; une capture par panneau et par format |
| 13 | Stabilité des panneaux (Q9) : chaque panneau ouvert, joueur avec son état réel, 30 s sans action, dans les deux formats | A | `OUTILS\luau\stabilite-panneaux.luau` rend PASSE : aucun écart de position, de taille ou de défilement au-delà de 1 px |
| 14 | Monde vu d'en bas (Q10) : chaque île ou décor majeur, de dessus, au niveau de l'eau ou du sol, de biais | A | Aucun dessous plat ou vide, aucune tranche sans volume ; trois captures par élément |
| 15 | Éléments natifs de Roblox (Q11) : PC, liste des joueurs ouverte, `leaderstats` présents, 2 joueurs ou plus | B (à défaut A avec joueur fictif) | Rien du HUD sous la liste des joueurs, la barre supérieure ou le chat |
| 8 | Charge : le moment le plus chargé du jeu, N clients | B | FPS mesuré, nombre de parts relevé |
| 9 | Jour suivant (action de test) | A | Bonus, objectifs et calendrier se renouvellent une seule fois |
| 10 | Scénarios de l'adversaire (rapport économie) et de la revue fun | A, B | Chaque exploit « à vérifier en jeu » est confirmé ou écarté |
| 11 | Session complète | A, B | 0 erreur console, serveur et clients |

### Formats d'écran et stabilité (scénarios 7, 12, 13)

Leçon d'Archipel de la nuit du 15/11 : un menu « qui sautille » est passé en production parce que l'interface n'avait été vue que dans le petit viewport téléphone de Studio.

- Deux formats obligatoires (`seuils.json` § `qa.formats_ecran_obligatoires`) : émulation PC plein écran, 1920×1080 au moins, et téléphone. Le format se règle par l'émulateur d'appareil de Studio ; le rapport note la taille réelle lue (`workspace.CurrentCamera.ViewportSize`).
- État réel d'un joueur : une sauvegarde avancée chargée (action de test de remplissage), des compteurs qui changent, des listes assez longues pour défiler. Un panneau vide ne prouve rien.
- Mesure : ouvrir le panneau, exécuter `OUTILS\luau\stabilite-panneaux.luau` côté client par `execute_luau`, ne rien toucher pendant 30 s, coller la ligne de résultat dans le rapport. Un panneau « INSTABLE » est un défaut P1 (P0 s'il empêche de cliquer).
- Le script n'a jamais tourné dans Studio (écrit au cycle 1) : à sa première utilisation, vérifier sur un panneau qu'on déplace exprès qu'il rend bien ÉCHEC.

### Bureau partagé (règle A7)

Le niveau B se lance par l'interface de Studio, donc par le bureau. Leçon d'Archipel de la nuit du 15/11 : sur un bureau partagé, les fenêtres T3 Code et Codex reprennent le premier plan et le client Roblox ignore des clics. Tout ce qui peut passer par le serveur MCP de Studio (`start_stop_play`, `execute_luau`, `screen_capture`) ou par une API documentée y passe. Le bureau ne sert qu'au lancement de « Clients et serveurs », sur un poste ou une session Windows dédiés (procédure 10 § 4) ; chaque clic est vérifié par une capture ; deux clics sans effet : arrêt, niveau A complété par un niveau C, et le rapport le dit.

## Rôles

- **Testeur** : joue son scénario, note ce qu'il voit, capture. Il ne juge pas le code.
- **Analyste console** : relève erreurs et avertissements, les rattache à un scénario et à une ligne de code du commit testé.
- **Contre-vérificateur** (après correctifs) : relit le diff des corrections, n'a pas écrit le correctif (E11).
- **Qualification indépendante** (Fable 5.2, une fois les P0 et P1 fermés) : lit captures, rapports et code ; note 6 axes sur 10 (3D et cohérence, lisibilité de la boucle, interface mobile, boucle et rétention, monétisation, image de vignette) ; rend un verdict par cible, « bêta fermée » et « public », avec conditions numérotées.

## Rapport

`JEUX\<slug>\06-qa\RAPPORT-QA-<n>.md` (gabarit `OUTILS\GABARITS\RAPPORT-QA.md`), un par cycle.

- Chaque constat est **vu** (capture, mesure), **lu** (code) ou **non vérifiable**.
- Gravité : **P0** bloque ou fait perdre des données ; **P1** casse une promesse du jeu ; **P2** gêne ; **P3** détail.
- Un défaut porte : scénario, étapes, attendu, observé, preuve, commit testé.
- Captures dans `06-qa\captures\` (hors git), nommées par scénario ; le rapport cite leur nom.

## Porte P5

Passe si : niveau B ou C réalisé avec 2 clients ou plus, 0 erreur console sur une session complète, 0 défaut P0 ou P1 ouvert, scénario 3 conforme, scénarios 12 à 15 conformes (deux formats d'écran, stabilité mesurée, monde vu d'en bas, éléments natifs dégagés), note de qualification ≥ 6,0 pour une bêta fermée ou ≥ 7,5 pour le public (`seuils.json` § `qa`).
Sinon : retour en production avec la liste classée. Trois cycles au plus ; ensuite arrêt du jeu si les défauts P0 et P1 ne baissent pas.

## Prompts types

```
Tu es testeur en jeu de l'usine Roblox. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md et PROCEDURES\06-QA-MULTIJOUEUR.md.
Jeu : <slug>, commit testé <hash>. Ton instance Studio : <identifiant donné par list_roblox_studios> (<serveur | client n>). Les autres instances ne sont pas à toi.
Scénarios : <numéros et détail>.
Tu joues en Play par le serveur MCP de Studio (execute_luau, screen_capture, get_console_output). Tu n'écris pas dans la place : ni mode Edit, ni save_place, ni arrêt du test. Tu ne touches ni à la souris ni au clavier.
Interface : chaque panneau en PC plein écran (1920×1080 au moins) ET au format téléphone, avec l'état réel d'un joueur ; stabilité mesurée 30 s par OUTILS\luau\stabilite-panneaux.luau (colle sa ligne de résultat). Monde : captures de dessus, au niveau de l'eau et de biais.
Note ce que tu vois, pas ce que tu supposes : vu, lu ou non vérifiable. Captures dans JEUX\<slug>\06-qa\captures\.
Aucun sous-agent.
Sortie : JEUX\<slug>\06-qa\notes-<ton nom>.md (un bloc par scénario : attendu, observé, preuve, gravité proposée).
Dernière ligne : RESULTAT: <ok|echec|arret> | <fichier> | <scénarios joués, défauts P0/P1 vus>.
```

```
Tu es analyste console et code de la QA de l'usine Roblox. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md et PROCEDURES\06-QA-MULTIJOUEUR.md.
Jeu : <slug>, commit testé <hash>. Pièces : JEUX\<slug>\06-qa\console-*.txt, notes-*.md, 05-production\src\ au commit indiqué.
Travail : rattache chaque erreur ou avertissement à un scénario et à une ligne de code ; dis si le défaut est certain ou à rejouer ; ne propose un correctif que s'il tient en quelques lignes.
Lecture seule, aucun accès à Studio. Aucun sous-agent.
Sortie : JEUX\<slug>\06-qa\analyse-console.md.
Dernière ligne : RESULTAT: <ok|echec|arret> | <fichier> | <erreurs distinctes, dont certaines>.
```

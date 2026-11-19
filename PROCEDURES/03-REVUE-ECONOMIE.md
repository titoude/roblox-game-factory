# 03 — Revue de l'économie

**Qui** : deux agents Codex `gpt-6.1-sol`, effort xhigh, indépendants l'un de l'autre. Un troisième pour la contre-vérification après correctif.
**But** : prouver par le calcul que le jeu se joue au bon rythme, qu'il ne se casse pas et qu'il vend honnêtement.

## Deux passes

| Passe | Quand | Sur quoi |
|---|---|---|
| **1. Papier** | Après la porte P1, avant tout code | La fiche concept et `economie.json` |
| **2. Code** | Pendant la production, quand le lot « économie » est commité, et avant la release | Les constantes et les chemins d'achat du code, **figés à un commit** (règle E10) |

## Agent « calcul »

1. Traduire la fiche en `JEUX\<slug>\03-economie\economie.json` (modèle : `OUTILS\GABARITS\economie.exemple.json`). Chaque valeur vient de la fiche ; une valeur absente se demande, elle ne s'invente pas : la noter « manquante » et rendre un échec.
2. Lancer `python OUTILS\sim-economie.py JEUX\<slug>\03-economie\economie.json --sortie JEUX\<slug>\03-economie\SIMULATION.md`.
3. Vérifier à la main trois points du simulateur (premier achat, un écart, un remboursement) : le rapport montre le calcul.
4. Étudier au moins deux profils : joueur actif (défaut) et joueur lent (moitié moins d'actions). Passe 2 : ajouter le joueur payant (toutes les offres) et vérifier ce qu'il gagne sur un non-payeur.
5. Proposer des constantes corrigées si un seuil casse, et rejouer la simulation avec.

Seuils (`seuils.json` § `economie`) : premier achat ≤ 60 s ; écart entre achats ≤ 2 min sur les 10 premières minutes, ≤ 8 min jusqu'à 60 min, ≤ 15 min ensuite ; remboursement entre 30 s et 5 min ; chantier ≤ 3 min ; contenu actif ≥ 90 min ; profil lent au moins 5 % plus long que le profil actif (alerte, pas échec).

Conventions (fixées au cycle 1, après deux lectures divergentes) :

- **Remboursement** : jugé sur chaque exemplaire acheté, au prix payé, avec les multiplicateurs permanents acquis à l'achat, à partir de la mise en service. Le simulateur le fait (ligne « Remboursement de chaque exemplaire ») ; le tableau « Générateurs » ne donne que le nominal du premier exemplaire.
- **Profils** : actif et lent ont le même délai entre achats ; seul le nombre d'actions change.
- **Départ** : le simulateur fait agir le joueur dès 0 seconde. Le temps d'arrivée en jeu s'ajoute ; la fiche donne les deux valeurs.
- **Hors modèle** : hors ligne, récompense quotidienne, bonus temporaires, aide entre joueurs, offres payantes. L'agent calcul les chiffre à part, en minutes d'un revenu de référence que la fiche doit définir.
- **Ce que la fiche ne dit pas** ne s'invente pas : paramètre omis du JSON et listé dans le rapport (« Décisions manquantes »).

Le concepteur peut lancer le simulateur avant de rendre sa fiche ; cela ne dispense pas de la revue.

## Agent « adversaire »

Il cherche comment casser l'économie. Liste minimale :

- **Duplication et retrait d'enjeu** : ranger, vendre, récolter, se déconnecter ou changer de serveur pour échapper à une perte ou doubler un gain (E9).
- **Chemins payants** : chaque offre passe-t-elle par les mêmes transitions que l'action gratuite (E7) ? Un achat rejoué après reconnexion accorde-t-il deux fois (E8) ?
- **Comptes multiples** : échange de victoires, parrainage en boucle, bonus d'amis ; plafonds par jour et par adversaire (E5).
- **Inflation** : un bonus cumulé dépasse-t-il le plafond écrit ? Une récompense fixe devient-elle ridicule ou une récompense proportionnelle explosive (E4) ?
- **Inactivité** : le joueur absent gagne-t-il plus que le joueur présent ? La promesse hors ligne est-elle tenue (E12) ?
- **Honnêteté** : la phrase de monétisation de la fiche est-elle vraie pour chaque offre ? Un payeur prend-il un avantage sur un autre joueur (E6) ? Un texte de boutique promet-il plus que l'effet ?

Passe 2 : mêmes questions, avec lecture du code et référence `fichier:ligne` au commit audité.

## Ce que le simulateur ne voit pas (règle E16)

Leçon du cycle 2 : sur `lave-la-tour` v4, le simulateur rendait PASSE alors qu'un accès nouveau (la Flèche) s'ouvrait avec un revenu deux fois plus faible que celui sur lequel ses prix étaient calculés. Les deux vérificateurs :

1. listent les mécanismes que le simulateur ignore (stock, bonus, hors ligne, primes, boucles ajoutées après la fin du contenu) ;
2. pour chaque accès nouveau, calculent la cadence et les promesses de récompense dans l'état d'équipement **minimal** qu'autorise cet accès, pas seulement dans l'état de référence ;
3. signalent à la revue du fun toute correction qui touche au résultat visible du geste (F11) ;
4. séparent les décisions manquantes qui bloquent le prototype (L0) et l'économie (L1) de celles des lots plus tardifs.

Une contre-vérification qui trouve un défaut de spécification, corrigé sans toucher aux coûts ni aux revenus, ne compte pas comme un retour au concepteur : correction, puis nouvelle passe par un agent qui n'a pas écrit le correctif, trois au plus par version (`economie.contre_verifications_max_par_version`, règle A5).

## Rapport

`JEUX\<slug>\03-economie\RAPPORT-ECONOMIE.md` (gabarit `OUTILS\GABARITS\RAPPORT-ECONOMIE.md`), un par agent puis fusion par l'orchestrateur.

- Chaque constat : **fait** (lu, avec référence), **calcul** (reproductible), **proposition** — séparés (A3).
- Gravité : **P0** casse le jeu ou la promesse d'honnêteté ; **P1** dégrade nettement le rythme ou l'équité ; **P2** réglage.
- Un défaut est « certain » s'il a un chemin démontrable ; sinon « à vérifier en jeu », avec le scénario de test pour la QA.

## Porte P2

Passe si : simulation dans les seuils pour le joueur actif, 0 défaut P0, chaque P1 corrigé dans la fiche ou accepté par l'orchestrateur avec sa raison, monétisation conforme à E6.
Sinon : retour au concepteur avec le rapport (2 itérations au plus).

Après correction : **contre-vérification** par un agent qui n'a écrit ni le correctif ni le premier rapport (E11). On s'arrête quand une passe ne trouve plus de défaut certain.

Le contre-vérificateur reçoit la fiche corrigée et les deux rapports de la passe précédente. Il retranscrit lui-même `economie.json` depuis la fiche, relance le simulateur, dit pour chaque défaut s'il est fermé, et cherche ce que la correction a cassé. Sortie : `RAPPORT-ECONOMIE-contre-verification-<n>.md`.

```
Tu es contre-vérificateur d'économie de l'usine Roblox. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md, PROCEDURES\03-REVUE-ECONOMIE.md, CONNAISSANCES\REGLES.md (Économie) et CONNAISSANCES\seuils.json.
Tu n'as écrit ni la fiche ni les rapports précédents. Entrées : JEUX\<slug>\02-concept\FICHE-CONCEPT.md (version <n>, commit <hash>), JEUX\<slug>\03-economie\RAPPORT-ECONOMIE-calcul.md et RAPPORT-ECONOMIE-adversaire.md (passe précédente).
Travail : 1. retranscris economie.json depuis la fiche et lance OUTILS\sim-economie.py (sortie SIMULATION.md, code de sortie relevé) ; 2. pour chaque défaut et chaque décision manquante des deux rapports : fermé, ouvert ou déplacé, avec la référence dans la fiche ; 3. cherche ce que les corrections ont cassé ou ouvert (nouveaux exploits, incohérences entre sections) ; 4. vérifie à la main deux chiffres que la fiche tire de la simulation.
Lecture seule sur la fiche et les outils. Aucun accès à Studio, au navigateur ou au réseau. Aucun sous-agent. Aucun commit.
Sortie : JEUX\<slug>\03-economie\RAPPORT-ECONOMIE-contre-verification-<n>.md d'après OUTILS\GABARITS\RAPPORT-ECONOMIE.md.
Dernière ligne : RESULTAT: <ok|echec|arret> | <fichier> | <verdict de cadence, défauts fermés sur total, nouveaux P0/P1 certains>.
```

## Mode dégradé (Codex injoignable)

L'orchestrateur lance lui-même le simulateur ; un Haiku en effort xhigh tient le rôle d'adversaire. P2 est notée « à confirmer » dans `ETAT.json` (`mode_degrade`) et se rejoue avec Codex avant la release.

## Prompts types

```
Tu es vérificateur d'économie « calcul » de l'usine Roblox. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md, PROCEDURES\03-REVUE-ECONOMIE.md, CONNAISSANCES\REGLES.md (Économie) et CONNAISSANCES\seuils.json.
Passe : <1 papier | 2 code au commit <hash>>. Entrée : JEUX\<slug>\02-concept\FICHE-CONCEPT.md<, et src\ au commit indiqué>.
Travail : écris JEUX\<slug>\03-economie\economie.json d'après OUTILS\GABARITS\economie.exemple.json, lance OUTILS\sim-economie.py, vérifie trois points à la main, étudie les profils demandés, propose des constantes si un seuil casse.
Lecture seule sur tout le reste : tu ne modifies ni la fiche ni le code. Aucun accès à Studio, au navigateur ou au réseau. Aucun sous-agent.
Sortie : JEUX\<slug>\03-economie\RAPPORT-ECONOMIE-calcul.md (faits, calculs, propositions séparés ; gravité P0/P1/P2).
Dernière ligne : RESULTAT: <ok|echec|arret> | <fichier> | <verdict de cadence et nombre de P0/P1>.
```

```
Tu es vérificateur d'économie « adversaire » de l'usine Roblox. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md, PROCEDURES\03-REVUE-ECONOMIE.md (section Agent « adversaire »), CONNAISSANCES\REGLES.md (Économie) et CONNAISSANCES\LECONS-ARCHIPEL.md (Économie).
Passe : <1 papier | 2 code au commit <hash>>. Entrée : JEUX\<slug>\02-concept\FICHE-CONCEPT.md<, et src\ au commit indiqué>.
Travail : cherche comment un joueur casse, contourne ou exploite cette économie, et si la monétisation tient sa promesse. Un défaut certain a un chemin démontrable ; sinon écris le scénario de test pour la QA.
Lecture seule. Aucun accès à Studio, au navigateur ou au réseau. Aucun sous-agent. Ne lis pas le rapport de l'autre vérificateur.
Sortie : JEUX\<slug>\03-economie\RAPPORT-ECONOMIE-adversaire.md.
Dernière ligne : RESULTAT: <ok|echec|arret> | <fichier> | <nombre de P0/P1 certains>.
```

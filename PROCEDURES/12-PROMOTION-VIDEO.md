# 12 — Promotion par vidéos courtes (facultative)

**Qui** : l'orchestrateur ; veille par le rôle `12.veilleur-promo` (Codex `gpt-6.1-sol`), scénarios par `12.scenariste-video` (Claude Fable 5.2).
**But** : amener des joueurs par YouTube Shorts et TikTok, mesurer, et décider sans humain : améliorer la promo, continuer, l'arrêter, améliorer le jeu ou passer au jeu suivant.
**Statut** : le propriétaire n'exige pas de promotion (« faut juste qu'il soit publié parfaitement », 16/11/2026). Cette procédure se **prépare** pour chaque jeu ; la mise en ligne est **bloquée** tant que les trois conditions du § 7 ne sont pas levées. Un agent ne crée aucun compte (G8).

Sources : `VEILLE\RELEVES\2026-11-16\p2-promo-videos-courtes-verifie.md` (15 pages lues, 41 constats F01 à F41, sources officielles YouTube, TikTok, Roblox, Google, FFmpeg, Microsoft). Les numéros F ci-dessous y renvoient. Aucun témoignage de praticien n'a pu être vérifié : tout ce qui touche « ce qui marche » pour un jeu Roblox est une hypothèse à tester, pas un fait.

## 1. D'abord le jeu, ensuite la vidéo

- Roblox conseille de vérifier rétention et engagement **avant** d'acquérir des joueurs (F13). Pas de campagne avant la porte P7 (J1 ≥ 8 %, session ≥ 8 min sur 200 joueurs organiques : `seuils.json` § `beta`), sauf le lot de 2 vidéos de lancement du § 3.
- Le trafic venu des réseaux peut accélérer la première sélection d'un jeu, mais le classement « Recommended for You » **exclut** les signaux des joueurs acquis hors de Roblox (F16) : une vidéo n'achète pas la page d'accueil. Ce qui compte pour elle : taux de lancement après affichage, départs précoces, jours et temps de jeu par joueur, jeu entre amis (F17), vignette personnalisée (F18).
- Conséquence pour l'usine : la « capacité d'être viral » se construit dans le jeu (première minute, raison de revenir, jeu à deux) et sur sa page (vignettes, titre). La vidéo vient après.

## 2. Veille (une fois par trimestre, ou quand une règle de plateforme change)

Rôle `12.veilleur-promo`, mêmes règles que la procédure 01 (rythme humain, 12 recherches et 15 pages au plus, sources officielles d'abord, un constat = une phrase + URL + date + mode). Sortie : `VEILLE\RELEVES\<date>\p<n>-promo-*.md`. Ce qui se revérifie : durée et format admis (F01, F06), signaux de recommandation (F04), règles de divulgation et d'étiquetage (F09, F10, F23 à F26), règles Roblox sur les liens et les récompenses (F19 à F22), quotas et conditions des API (F27 à F32).

## 3. Plan de campagne

`JEUX\<slug>\08-distribution\PLAN-VIDEOS.md` (gabarit `OUTILS\GABARITS\PLAN-VIDEOS.md`), écrit par le scénariste d'après la fiche concept et les captures **possédées** (règle C7 : aucune image promise qu'on ne sait pas produire).

| Élément | Valeur de départ (à calibrer) | Origine |
|---|---|---|
| Format | Vertical 1080 × 1920, 30 images/s, MP4 H.264, 15 à 30 s | Profil de travail ; YouTube admet jusqu'à 3 min et le carré (F01) |
| Lot initial | 6 vidéos par plateforme sur 14 jours : 3 angles × 2 accroches | Aucune cadence minimale n'est demandée par YouTube (F05) ni par TikTok (F08) |
| Angles | Défi avec résultat visible ; avant/après ; moment drôle réel ; nouveauté jouable. Une seule mécanique par vidéo | Hypothèse (aucun format « gagnant » prouvé) |
| Accroche | Le résultat dès la première seconde, 8 mots au plus à l'écran | Interprétation de F04 (choix de regarder, durée vue) |
| Appel à l'action | « Joue à <nom exact du jeu> », lien dans le profil de la chaîne | F12 ; jamais de lien sortant depuis le jeu (F19) |
| Attribution | Un lien de partage Roblox par vidéo ou, à défaut, par canal et par période | F15 |
| Musique | Aucune musique tierce par défaut ; un fichier « sans musique » toujours gardé | F02, F11, G13 |

Interdits (G6, G8, F21, F22) : concours, Robux ou récompense contre vote, favori, abonnement ou achat ; faux témoignages ; fausse rareté ; vidéo qui montre ce que le jeu ne fait pas ; contact d'un créateur sans instruction écrite du propriétaire.

## 4. Production d'une vidéo

1. **Capture** : en Play dans Studio (verrou `studio`, et `bureau` pour l'enregistreur), HUD réel, 1920 × 1080 au moins. Moyens sans installation : Outil Capture d'écran de Windows, Windows+Maj+R, MP4 dans `Vidéos\Screen Recordings` (F40) ; Game Bar, Windows+G (F39). Les sources vont dans `08-distribution\videos\sources\` (hors git ; disque : purger après montage).
2. **Plan de montage** : `08-distribution\videos\<id>.plan.json` (exemple `OUTILS\GABARITS\video.plan.exemple.json`) : clips, cadrage, accroche, sous-titres, appel à l'action.
3. **Contrôle** : `python OUTILS\monter-video.py verifier <plan>` puis `commandes <plan>` (imprime les commandes sans rien exécuter).
4. **Montage** : `python OUTILS\monter-video.py monter <plan>` : recadrage 9:16, sous-titres incrustés, concaténation, son normalisé (F35 à F38). **ffmpeg est absent de cette machine** (16/11/2026) : l'outil le dit et s'arrête ; poser ffmpeg est une décision du propriétaire (G17, environ 100 Mo).
5. **Relecture** par un agent qui n'a pas écrit le scénario : la vidéo montre-t-elle ce que le jeu fait vraiment, l'accroche tient-elle en une seconde, le texte se lit-il sur téléphone ?

## 5. Mise en ligne (bloquée, § 7)

- YouTube : `videos.insert` de l'API Data v3, avec autorisation OAuth donnée par le propriétaire de la chaîne ; 100 imports par jour par défaut (F27 à F29). Champs à remplir sans erreur : public (une vidéo qui vise notamment les enfants est « made for kids », F23), promotion de son propre jeu déclarée (F24), contenu généré ou modifié de façon réaliste déclaré (le gameplay et les sous-titres n'en font pas partie, F25).
- TikTok : l'API de publication directe exige une application auditée et n'est pas destinée à un outil interne (F30, F31) ; chemin réaliste : envoi en **brouillon** que le propriétaire valide dans l'application (F41), ou publication manuelle. Compte de type Business : promotion déclarée (F09), musique de la bibliothèque commerciale (F11).
- Chaque mise en ligne s'écrit dans `08-distribution\JOURNAL-VIDEOS.csv` avec son identifiant, avant toute autre action (L3).

## 6. Mesure et décision (porte P11)

Relevés à 24 h et à 7 jours de chaque vidéo (API YouTube Analytics : vues engagées, durée moyenne, pourcentage moyen vu, partages, abonnés, F33 ; pour TikTok : relevé dans l'application tant qu'aucune API de lecture n'est ouverte) ; nouveaux joueurs par lien de partage (F15) ; verdict produit par `python OUTILS\mesures-joueurs.py juger`.

```
python OUTILS\decision-promo.py --jeu <slug> [--p7 passe|echec|attend] [--cohortes-insuffisantes N]
```

| Verdict | Condition (valeurs de départ, `seuils.json` § `promo`) | Suite |
|---|---|---|
| `attendre` | Rien de mûr (7 jours), ou moins de 1 000 présentations et 300 vues engagées par vidéo | Rien : une preuve insuffisante n'est pas un échec |
| `ameliorer_promo` | Choix de regarder < 60 % : changer la première scène ; ≥ 60 % mais durée moyenne vue < 70 % : raccourcir, avancer le résultat ; ≥ 10 000 vues et < 1 nouveau joueur pour 1 000 vues : revoir l'appel à l'action et le parcours | 6 vidéos de plus au maximum, en corrigeant la cause nommée |
| `continuer` | 2 vidéos à 3 nouveaux joueurs ou plus pour 1 000 vues | 3 variantes de l'angle gagnant |
| `arreter_promo` | 12 vidéos mûres, 10 000 vues, toujours < 1 joueur pour 1 000 vues ; ou 8 heures de travail cumulées sans preuve | Canal « non qualifié » ; ce n'est pas un jugement sur le jeu |
| `ameliorer_jeu` | La vidéo convertit, mais J1 < 8 % ou session < 8 min (P7 en échec) | Retour en production : arrivée et boucle ; pas une vidéo de plus (L4) |
| `jeu_suivant` | 2 cohortes comparables sous les seuils après correction du jeu ; ou promo arrêtée sans autre canal autorisé | Bilan (procédure 09), arrêt ou mise en veille du jeu, « fais un jeu » repart de la veille |

`etat.ps1 -Jeu <slug> -Porte P11 -Resultat passe|echec|a_confirmer -Preuve <DECISION-PROMO-….md>` : `passe` = `continuer`, `echec` = `arreter_promo` ou `jeu_suivant`, `a_confirmer` = décision prise sur des données d'exemple. Tous ces seuils sont des valeurs de départ : ils se recalibrent au bilan sur les campagnes réelles (procédure 09), jamais pendant une campagne (A4).

## 7. Bloqué tant que

| Condition | État au 16/11/2026 | Qui la lève |
|---|---|---|
| Une chaîne YouTube et, si voulu, un compte TikTok au nom du propriétaire, avec le consentement OAuth donné une fois (jeton rangé dans le Gestionnaire d'identifiants) | Aucun compte fourni | Propriétaire (G7, G8) |
| Une ligne dans `PLAFONDS.md` § 3 : jeu, canal, fréquence maximale | Vide = interdit | Propriétaire |
| ffmpeg posé dans `OUTILS\bin\` ou dans le PATH | Absent | Propriétaire (G17) |
| Captures du jeu (Studio et bureau libres) | Verrous tenus par un autre agent | Verrous |

Tout le reste se fait sans lui : veille, plan de campagne, scénarios, plans de montage vérifiés, commandes prêtes, journal, règle de décision.

## Prompt type (scénariste vidéo)

```
Tu es scénariste des vidéos courtes de l'usine Roblox. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md (G6, G8, G13), PROCEDURES\12-PROMOTION-VIDEO.md, la veille VEILLE\RELEVES\2026-11-16\p2-promo-videos-courtes-verifie.md et JEUX\<slug>\02-concept\FICHE-CONCEPT.md.
Jeu : <slug>. Captures possédées : <liste, ou « aucune : écris la liste des captures à prendre »>.
Écris le plan de campagne d'après OUTILS\GABARITS\PLAN-VIDEOS.md : 3 angles × 2 accroches, seconde par seconde, chaque image couverte par une capture possédée ou listée à prendre ; puis un plan de montage JSON par vidéo d'après OUTILS\GABARITS\video.plan.exemple.json, et vérifie chacun par python OUTILS\monter-video.py verifier.
Aucune promesse que le jeu ne tient pas, aucun concours, aucune récompense contre vote ou abonnement, aucune musique sans licence. Tu ne publies rien, tu ne crées aucun compte, tu n'ouvres ni Studio ni navigateur. Aucun sous-agent. Aucun commit.
Sorties : JEUX\<slug>\08-distribution\PLAN-VIDEOS.md et JEUX\<slug>\08-distribution\videos\*.plan.json.
Dernière ligne : RESULTAT: <ok|echec|arret> | <fichier> | <nombre de vidéos planifiées, captures manquantes>.
```

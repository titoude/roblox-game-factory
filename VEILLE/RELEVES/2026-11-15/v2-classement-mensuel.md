# Relevé de veille — RoStats (classement mensuel) — 2026-11-15

- Veilleur : V2, Claude Haiku 5.5, effort high (sans sous-agent)
- Mission : A (tour des tendances), volet classement mensuel (octobre 2026 et novembre 2026, moyennes de CCU)
- Outil de navigation utilisé : WebSearch seul (recherche web, extraits de résultats). Aucun outil de lecture de page disponible : WebFetch non chargeable dans ce cycle (ToolSearch « select:WebFetch,WebSearch » ne renvoie que WebSearch). Chrome, `cu.ps1` et `preview_*` non utilisés, par consigne.
- Session : début NP UTC, fin ≈ 22:11 UTC (dernière commande : 2026-11-15T22:11:35Z). Recherches : 3 (plafond atteint). Pages lues directement : 0 (plafond 16).
- Sources interrompues : aucune. Aucune page ouverte, donc aucun CAPTCHA, écran de connexion ni condition rencontré. Aucune alerte émise.

## Relevé

Chaque valeur provient d'un extrait de résultat de recherche (mode : « lu dans un résultat de recherche », non « vu à l'écran »). Donnée absente : `NP`. Un chiffre incertain est signalé, pas arrondi.

| # | Jeu | universeId ou placeId | Genre | CCU | Unité et nature | Créé le | Action centrale d'après la page (non joué) | URL | Heure UTC |
|---|---|---|---|---|---|---|---|---|---|
| 1 | #436 — [UPD]🛠️Build and Kill Verity 100M CCU | NP | NP | 3 593 (libellé « Avg players ») | joueurs simultanés, moyenne (libellé « Avg players ») du classement d'octobre 2026 ; à confirmer sur la page, l'extrait ne précise pas la période | NP | NP (page non lue) | https://rostats.io/charts/2026-10 (extrait) | NP (extrait non daté) |

Même extrait, mêmes réserves : pic (« Peak ») 12 667, période NP.

## Montées et chutes observées

Une seule ligne, extraite d'un texte mal formé. Pas de tendance validée (règle M2).

| Jeu | Avant | Après | Période | Écart absolu | Écart relatif | URL |
|---|---|---|---|---|---|---|
| [UPD]🛠️Build and Kill Verity 100M CCU | illisible (extrait : « 346 » et « #2752 », mal formé) | #436 | « biggest gainers » d'octobre 2026, période exacte NP | NP | +938,4 % affiché dans l'extrait, base (rang ou CCU) NP : incertain, ne pas utiliser sans vérification | https://rostats.io/charts/2026-10 (extrait) |

## Prix relevés (mission B)

Sans objet (mission A).

## Ce que je n'ai pas pu lire

- Classement mensuel RoStats d'octobre 2026 : 1 ligne lue sur les 25 visées. Table complète non lue (aucune page ouverte).
- Top 10 des montées et top 10 des chutes du mois : NP.
- Classement de novembre 2026 : NP. Aucune source trouvée. Au 15/11, le mois est à moitié écoulé : une moyenne partielle n'est pas comparable à un mois plein.
- Âge de création < 90 jours : NP (aucune fiche de jeu lue).
- Classement mensuel RoMonitor Stats : non trouvé. La recherche sur romonitorstats.com n'a renvoyé que des fiches de jeux et une page « branded » (classement sur 14 jours, pas un mois calendaire).
- Pages de jeu RoStats : aucune lue.

## Remarques

- Friction 1 : la procédure liste Chrome, `cu.ps1` et `preview_*` comme outils de lecture, mais la consigne du cycle les exclut. WebFetch n'est pas disponible. Le seul outil utilisable est la recherche web, qui renvoie des extraits et non des pages entières : impossible de parcourir un classement. Le relais par sous-agent web-fetch est exclu par la consigne (« ne lance aucun sous-agent »).
- Friction 2 : le gabarit prévoit le mode « vue à l'écran » ; les valeurs de ce relevé viennent d'extraits de recherche. Le mode est écrit tel quel dans le tableau.
- Friction 3 : la procédure ne dit pas comment traiter la moyenne d'un mois en cours (novembre au 15). Non traitée faute de donnée.
- Friction 4 : sources interrogées par recherche restreinte au domaine (`allowed_domains`) : rostats.io, puis romonitorstats.com, puis une recherche générale. Trois recherches, plafond atteint. Aucune tentative de contournement.
- Hors périmètre, vu dans les extraits et non retenu : rowatcher.com (bilan hebdomadaire de plateforme, semaine du 26/10 au 01/11 : CCU moyen en baisse de 2,7 % sur la semaine) ; bloxodes.com (listes sans date). Non utilisés pour le classement mensuel.
- Fiches de jeu romonitorstats.com vues dans les extraits (ex. « Fish It! », moyenne 78,68 k, dernière mise à jour 27/09/2026) : ce ne sont pas des moyennes d'octobre. Non retenues dans le tableau.
- Rolimon's : non consulté (désactivé dans `SOURCES-VEILLE.md`).
- Aucune écriture ailleurs que ce fichier. `ALERTES.md` non modifié. Aucun verrou pris (aucune écriture dans une place). Aucun commit git.

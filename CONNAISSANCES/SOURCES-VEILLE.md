# Sources de veille

État au 15/11/2026, d'après `blox-craft\docs\usine\01-SOURCES-DONNEES.md`. Conditions à revérifier chaque mois (règle M6) : la colonne « Vérifié le » fait foi.

Statuts : **actif** (lecture libre dans les limites de session), **restreint** (lecture ponctuelle, quota propre), **désactivé** (interdit aux agents tant que le propriétaire n'a pas écrit le contraire dans `PLAFONDS.md`).

| Source | Adresse | Ce qu'on y lit | Statut | Limite par session | Vérifié le |
|---|---|---|---|---|---|
| Roblox Charts | `https://www.roblox.com/charts` | Top Playing Now, Top Trending (hausse des DAU sur la semaine), Up-and-Coming, Top Revisited : rangs et CCU | actif | 15 pages | 2026-11-15 |
| Page d'un jeu Roblox | `https://www.roblox.com/games/<placeId>` | Titre, description, CCU, votes, date de création, mise à jour, passes visibles, vignettes | actif | 20 pages | 2026-11-15 |
| Documentation créateur | `https://create.roblox.com/docs` | Règles de découverte, analytics, publicité | actif | libre | 2026-11-15 |
| Google | recherche web | Articles récents sur une tendance, nom d'un jeu qui monte | actif | 10 recherches | 2026-11-15 |
| RoMonitor Stats | `https://romonitorstats.com` | Fiche d'un jeu : courbe de CCU, pics, visites, durée de session affichée | restreint | 8 pages | 2026-11-15 |
| RTrack | `https://rtrack.live` | Pages publiques ; service en reconstruction | restreint | 8 pages | 2026-11-15 |
| RoStats | `https://rostats.io` | Classements mensuels `/charts/AAAA-MM` (moyennes de CCU, variation), jeux récents `/new`, hausses sur 24 h `/trending`, genres `/genres`, fiche d'un jeu `/games/<universeId>` (création, taille de serveur, cadence de mises à jour, passes et produits avec leur prix) | restreint | 8 pages | 2026-11-15 |
| Rolimon's | `https://www.rolimons.com/gametable` | Table des jeux : CCU, pic, votes | **désactivé** | 0 | 2026-11-15 |
| YouTube, TikTok | pages publiques | Vidéos récentes sur un jeu (titre, date, vues) | restreint | 5 pages | 2026-11-15 |
| GameAnalytics | rapport Roblox 2026 | Médianes de rétention et de session | actif (lecture du rapport) | 2 pages | 2026-11-15 |

## Pourquoi ces statuts

- **RoStats** : ses conditions interdisent le scraping et l'accès automatisé au-delà de la navigation ordinaire. Un agent y lit quelques pages comme un visiteur, ne recopie pas de tableau entier, ne suit pas de pagination en série.
- **RoMonitor, RTrack** : conditions exploitables non obtenues. Même prudence.
- **Rolimon's** : ses conditions interdisent l'extraction automatisée, la collecte systématique et l'usage commercial sans accord écrit. Désactivé par défaut. Pour l'activer, le propriétaire l'écrit dans `PLAFONDS.md` (section Sources), de préférence après accord écrit du site.
- **Roblox** : les conditions (§ 9.2 utilisateur, § 3.7 créateur) encadrent la collecte de données liée à l'IA. La veille reste une lecture de pages publiques à petit volume, sans stockage de profils de joueurs.

Un agent qui pilote un navigateur reste un accès automatisé au sens de certaines conditions. Le rythme humain réduit la charge, il ne change pas le statut juridique : ce point relève du propriétaire.

## Ce qu'on ne fait jamais

- Se connecter, créer un compte, accepter des conditions, résoudre un CAPTCHA.
- Appeler une API non documentée, ouvrir les outils de développement, télécharger un export.
- Recopier un tableau complet, enchaîner les pages d'une pagination, revenir plusieurs fois par jour.
- Commenter, voter, suivre, envoyer un message.

## Complément par endpoint documenté

`OUTILS\instantane-univers.ps1` interroge l'API publique documentée `games.roblox.com/v1/games` pour une liste d'univers validée par l'orchestrateur (50 au plus, un appel par quart d'heure au plus). Statut : **restreint**. Il sert à dater le CCU de jeux déjà repérés, pas à explorer le catalogue.

## Journal des vérifications de conditions

| Date | Source | Constat | Décision |
|---|---|---|---|
| 2026-11-15 | toutes | État repris de l'étude 01 | Statuts ci-dessus |
| 2026-11-15 | Roblox Charts | Tour 1 : la page répond (HTTP 200) mais le classement est chargé par script ; rien de lisible sans navigateur | Statut inchangé ; source inutilisable en mode « lecture sans navigateur » |
| 2026-11-15 | RoStats | Tour 1 : 7 pages lues sans navigateur, sans connexion ni refus (`/charts/2026-10`, `/charts/2026-11`, `/genres`, `/new`, `/trending`, 2 fiches `/games/<universeId>`). Les tableaux complets et les revenus estimés sont réservés aux abonnés : non consultés. Conditions non relues ce jour | Reste « restreint », 8 pages. C'est la source principale du mode sans navigateur. Conditions à relire au prochain tour (une page) |
| 2026-11-15 | RoWatcher (`rowatcher.com`) | Cité par les résultats de recherche des veilleurs. `/terms` répond mais rend une page vide sans script : conditions illisibles | **Non ajouté** : une source sans conditions lues reste hors liste. À relire avec un navigateur avant toute lecture de ses pages |
| 2026-11-15 | `games.roblox.com/v1/games` | Un appel pour 4 univers par `OUTILS\instantane-univers.ps1` : réponse complète, délai de 15 minutes respecté | Reste « restreint » |

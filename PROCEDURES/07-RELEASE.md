# 07 — Release

**Qui** : l'orchestrateur (seul à publier), plus un relecteur Codex `gpt-6.1-sol` effort xhigh pour la revue du diff.
**But** : mettre en ligne une version vérifiée, d'abord en TEST, puis en PROD privé, sans jamais dépasser ce que `CONNAISSANCES\PLAFONDS.md` autorise.

## Conditions de départ

- Porte P5 passée ; rapport QA du commit à publier.
- Si la porte P2 a été jugée en mode dégradé : la rejouer avec Codex maintenant.
- `PLAFONDS.md` § 1 : la colonne de la cible visée (TEST privé, PROD privé, bêta fermée, public) est remplie pour ce jeu. Sinon : préparer tout ce qui suit jusqu'à l'étape 3, mettre le jeu en `bloque`, alerter.
- Amorçage fait (procédure 10) : univers TEST et PROD existants, droits du compte des agents, moyen d'appel Open Cloud.

## Moyens d'action, par ordre de préférence

1. **`open_cloud_invoke` du serveur MCP de Studio** : Studio porte l'authentification, l'agent ne manipule aucune clé.
2. **Travailleur local à opérations nommées**, qui lit la clé dans le Gestionnaire d'identifiants Windows. À construire après l'amorçage, quand les clés existent ; il n'est pas fourni dans l'usine parce qu'il exige des secrets.
3. **Interface** (Studio ou tableau de bord créateur) sous verrou `bureau`, pour ce qu'aucune API ne couvre : genre, audience, accès. Chaque clic vérifié par capture avant et après.

Jamais : extraire un cookie, coller une clé dans une commande ou un fichier (G9, G10).

## Déroulé

1. **Geler** : commit de release, étiquette `<slug>-v<n>`. Plus aucune écriture dans la place hors release (verrou `place:<placeId>` pris par l'orchestrateur).
2. **Revue indépendante du diff** depuis la dernière version publiée (ou de tout le code pour une première) : défauts certains seulement, surtout argent, sauvegarde, Remotes, actions de test désactivées hors Studio. Un défaut certain = retour en production.
3. **Liste de contrôle** `07-release\CHECKLIST-RELEASE.md` (gabarit) remplie avec ses preuves.
4. **Publier en TEST** : sauvegarder (`save_place`), puis publier la version. Relire l'état distant : numéro de version, statut publié.
5. **Vérifier en TEST** ce qui ne se voit qu'en ligne : sauvegarde réelle (DataStore), classements, achats de test. C'est le niveau C de la QA si des comptes et appareils du propriétaire sont disponibles ; sinon le noter « non vérifié en ligne ».
6. **Réglages de l'expérience PROD** : nom, description, taille de serveur (`serverSize`), relus après écriture. Genre, audience, questionnaire de maturité : interface, ou propriétaire.
7. **Boutique** : pour chaque offre de la fiche, lire `07-release\MANIFESTE-IDS.json` ; si l'identifiant n'existe pas, créer le pass ou le produit, noter l'identifiant **avant** toute autre action, le reporter dans `Config`, retester l'achat. Créer un produit ne livre rien : c'est le code serveur qui livre.
8. **Publier en PROD privé**. Relire version et statut.
9. **Icône et vignettes** : 16:9 en 1920×1080, HUD masqué (L7) ; remplacer la liste des vignettes en conservant celles à garder ; vérifier le statut de modération plus tard, il n'est pas immédiat.
10. **Ouverture** (bêta fermée, puis public) : seulement si `PLAFONDS.md` le dit pour cette cible. Sinon le jeu reste privé et l'orchestrateur le signale.

## Publication parfaite : liste de production

Demande du propriétaire (16/11/2026) : « faut juste qu'il soit publié parfaitement ». Chaque ligne se coche avec sa preuve dans `07-release\CHECKLIST-RELEASE.md` ; une ligne sans preuve est « non vérifié », jamais « fait ». « Hors Studio » dit ce qui se prouve par `OUTILS\banc-luau.py` quand Studio est verrouillé.

| Domaine | Critère mesurable | Preuve attendue | Moyen |
|---|---|---|---|
| **Page du jeu** | Titre de 50 caractères au plus, promesse en première ligne de la description, genre choisi, icône lisible à 64 px, 3 vignettes 1920 × 1080 au moins dont 2 promesses distinctes (L6, L7), taille de serveur de la fiche, appareils cochés (téléphone, tablette, ordinateur) | Relecture de l'état distant après écriture ; dimensions de chaque image lues sur le fichier | Open Cloud ou tableau de bord sous verrou `bureau` |
| | Questionnaire de maturité rempli d'après la fiche (réponses préparées dans le kit) | Capture de l'écran final | Interface ; si l'écran demande un consentement légal : arrêt et alerte (G7) |
| **Langues** | Texte source anglais et table française dans le jeu (C8), 0 chaîne en dur hors de la table, accents et séparateurs justes (P11) | Test du banc : chaque clé existe dans les deux langues ; capture du jeu en français et en anglais | Hors Studio pour la table ; Studio pour les captures |
| | Titre et description traduits en français sur la page ; traduction automatique activée pour les autres langues | Relecture de l'état distant | Tableau de bord ou API de localisation |
| **Badges** | 5 badges au plus au lancement (quota gratuit ; au-delà c'est une dépense : interdit sans plafond, G4), attribués par le serveur une seule fois, un badge à identifiant 0 n'est jamais demandé | Manifeste des identifiants ; test du banc : attribution unique, identifiant 0 ignoré | Création par l'interface ou Open Cloud ; logique hors Studio |
| **Suivi des joueurs** | Entonnoir d'arrivée (arrivée, première action, premier achat, 3 min, 10 min) envoyé à `AnalyticsService` (P8) ; compteurs agrégés par jour UTC, sans donnée personnelle, écrits par le jeu dans `<Jeu>Mesures_v1` : nouveaux joueurs, sessions, minutes jouées, retours à J1 et à J7, étapes de l'entonnoir | Test du banc : chaque étape comptée une fois par joueur ; lecture réelle par `python OUTILS\mesures-joueurs.py` après 24 h en ligne | Gabarit `OUTILS\GABARITS\luau\…MesuresService.lua` ; lecture par Open Cloud (même clé que les retours) |
| | Univers du jeu ajouté à la clé Open Cloud de lecture : la clé `usine-roblox-lecture` (compte TITOU_ETOUI, créée le 17/11/2026) est restreinte expérience par expérience ; sans cet ajout, retours et mesures du nouveau jeu sont illisibles (HTTP 403) | `python OUTILSetours-joueurs.py diagnostic --jeu <slug> --magasin <Jeu>Retours_v1` sans 401 ni 403 | Tableau de bord, page Clés API, sous verrou `bureau` : modifier la clé, « Rechercher une expérience », opérations `objects:read` et `objects:list` |
| | Bouton « Idée / bug » en jeu (procédure 11) | Test du banc ; un retour de test relu par `retours-joueurs.py` | Gabarit `…RetoursService.lua` |
| **Sauvegardes sûres** | `UpdateAsync` avec verrou de session ; reprises avec attente croissante ; sauvegarde périodique (60 à 120 s), à la sortie et à la fermeture du serveur (`BindToClose`) ; version de schéma et migration ; **un chargement en échec ne crée jamais une sauvegarde vide** (le joueur attend ou est renvoyé, rien n'est écrasé) ; reçus d'achat idempotents (E8) ; magasin `_studio` séparé | Tests du banc : quitter en pleine action, fermeture du serveur, panne de DataStore au chargement et à l'écriture, deux serveurs pour un même compte, reçu rejoué. En ligne : niveau C (sauvegarde réelle relue après reconnexion) | Hors Studio pour la logique ; TEST privé pour le réel |
| **Robustesse** | 0 erreur console sur une session complète ; Remotes validés (type, bornes, cadence) ; actions de test inatteignables hors Studio | Test du banc : chaque Remote avec arguments faux, hors bornes et en rafale ; `luau-verif.ps1` vert | Hors Studio, puis Play |

## Règles

- **Cinq états distincts** (L2) : sauvegardé, publié, modéré, visible, joué. La liste de contrôle a une ligne pour chacun ; « publié » ne se déduit pas d'un `save_place` ni d'un code HTTP.
- **Pas de nouvelle tentative aveugle** (L3) : après un délai dépassé sur une création (pass, produit, campagne), relire l'état distant et le manifeste avant de recommencer.
- **Conflit Team Create** (erreur 409 sur un réglage de place) : une session Studio garde la place ; coordonner, ne pas insister.
- **Les types non mis à jour par la publication par API** (`EditableImage`, `EditableMesh`, `PartOperation`, `SurfaceAppearance`, `BaseWrap`) : si le jeu en contient, publier depuis Studio.
- **Aucune dépense** : la création de badges au-delà du quota gratuit coûte des Robux ; interdit sans ligne de plafond (G4).
- **Retour arrière** : garder le numéro de la dernière version saine dans la liste de contrôle. En incident après publication : republier cette version, puis analyser.

## Porte P6

Passe si : revue du diff sans défaut certain, liste de contrôle complète avec preuves, version publiée relue en TEST puis en PROD, manifeste des identifiants à jour, autorisation écrite pour la cible atteinte.
Le jeu peut rester à « PROD privé » en attendant une autorisation : la porte est alors passée pour cette cible, et l'étape 08 attend.

## Prompt type (revue du diff)

```
Tu es relecteur de release de l'usine Roblox. Racine : %USERPROFILE%\Documents\Projets\USINE-ROBLOX.
Lis d'abord GARDE-FOUS.md, PROCEDURES\07-RELEASE.md et CONNAISSANCES\REGLES.md (Économie, Production).
Jeu : <slug>. Diff à relire : git diff <étiquette précédente>..<commit de release> -- JEUX\<slug>\05-production\src (ou tout src\ pour une première version).
Cherche les défauts certains, avec leur chemin : argent et reçus, sauvegarde, validation des Remotes, actions de test atteignables hors Studio, offres visibles sans identifiant, textes de boutique faux. Sépare « certain » de « à vérifier en jeu ».
Lecture seule. Aucun accès à Studio ni au réseau. Aucun sous-agent.
Sortie : JEUX\<slug>\07-release\REVUE-DIFF-v<n>.md.
Dernière ligne : RESULTAT: <ok|echec|arret> | <fichier> | <favorable ou non, nombre de défauts certains>.
```

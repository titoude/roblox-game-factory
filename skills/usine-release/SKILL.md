---
name: usine-release
description: Release d'un jeu Roblox de l'usine - revue indépendante du diff, liste de contrôle, publication en TEST puis en PROD privé, réglages de l'expérience, création des passes et produits avec manifeste d'identifiants, vignettes, retour arrière. À utiliser quand un jeu a passé la QA et doit être mis en ligne. Aucune ouverture au public ni dépense sans autorisation écrite dans PLAFONDS.md.
---

# Release de l'usine Roblox

Racine de l'usine : `%USERPROFILE%\Documents\Projets\USINE-ROBLOX` (ou `USINE_ROBLOX`).

Seul l'orchestrateur publie. Un relecteur indépendant lit le diff avant toute publication en PROD.

## Avant tout

Lis `GARDE-FOUS.md`, `PROCEDURES\07-RELEASE.md` (elle fait foi), `CONNAISSANCES\PLAFONDS.md` et `CONNAISSANCES\REGLES.md` (Lancement).

Conditions de départ :

- Porte P5 passée pour le commit à publier.
- `PLAFONDS.md` § 1 autorise la cible visée (TEST privé, PROD privé, bêta fermée, public) pour ce jeu. Sinon : préparer, mettre le jeu en `bloque`, alerter, ne rien publier.
- Univers TEST et PROD existants (amorçage du propriétaire). Les agents ne créent pas d'expérience.

## Déroulé

1. Geler : commit de release, étiquette `<slug>-v<n>`, verrou `place:<placeId>`.
2. Revue indépendante du diff (Codex `gpt-6.1-sol`, effort xhigh) : défauts certains sur l'argent, la sauvegarde, les Remotes, les actions de test, les offres. Un défaut certain = retour en production.
3. Remplir `JEUX\<slug>\07-release\CHECKLIST-RELEASE.md` avec ses preuves.
4. Publier en TEST ; relire version et statut ; vérifier ce qui ne se voit qu'en ligne.
5. Réglages PROD (nom, description, taille de serveur), relus après écriture.
6. Boutique : lire `MANIFESTE-IDS.json` avant de créer ; écrire chaque identifiant dès qu'il est connu ; reporter dans `Config` ; retester l'achat.
7. Publier en PROD privé ; relire.
8. Icône et vignettes (16:9, 1920×1080, HUD masqué) ; statut de modération relu plus tard.
9. Ouverture : seulement si `PLAFONDS.md` le dit pour cette cible.

## Moyens, par ordre de préférence

1. `open_cloud_invoke` du serveur MCP de Studio (aucune clé manipulée par l'agent).
2. Travailleur local à opérations nommées, clé lue dans le Gestionnaire d'identifiants Windows (à construire après l'amorçage).
3. Interface sous verrou `bureau`, chaque clic vérifié par capture.

## Règles

- Sauvegardé, publié, modéré, visible, joué : cinq états vérifiés un par un. `save_place` n'est pas une publication.
- Après un délai dépassé sur une création : relire l'état distant et le manifeste avant de recommencer.
- Jamais de cookie extrait, jamais de clé dans un fichier ou une commande.
- Badge payant, toute dépense : interdit sans ligne de plafond.
- Garder le numéro de la dernière version saine pour le retour arrière.
- Connexion, double authentification, conditions, permission : arrêt et `OUTILS\alerte.ps1`.

Relecteur du diff, dernière ligne : `RESULTAT: <ok|echec|arret> | JEUX\<slug>\07-release\REVUE-DIFF-v<n>.md | <favorable ou non, défauts certains>`.

# 10 — Amorçage par le propriétaire

**Qui** : le propriétaire, une fois. Les agents ne font aucune de ces actions : identité, consentements, paiements et permissions initiales sont des frontières humaines (G7, G8).
**But** : qu'après cela l'usine tourne sans lui, sauf arrêt sur CAPTCHA, nouvelles conditions, double authentification ou paiement.

Cocher chaque point dans `CONNAISSANCES\PLAFONDS.md` § 6 quand il est fait. Détail technique : `blox-craft\docs\usine\04-AUTONOMIE-OUTILS.md`.

## 1. Comptes et propriété

1. **Groupe Roblox « studio »** propriétaire des jeux. Y transférer Archipel. Leçon d'Archipel : le compte collaborateur ne pouvait changer ni Max Players ni la visibilité, et ses assets ne se chargeaient pas dans l'univers du propriétaire.
2. **Compte des agents** (Archipel_MCP) dans le groupe, avec un rôle limité à ce que l'usine fait : éditer, publier, gérer la boutique. Pas de rôle propriétaire.
3. **Conditions d'utilisation à jour** sur les deux comptes (une acceptation est en attente sur le compte des agents) ; **double authentification** sur le compte titulaire.
4. **Univers créés d'avance** : pour chaque jeu à venir, un univers TEST et un univers PROD, privés, dans le groupe. Les agents ne créent pas d'expérience.

## 2. Accès

1. **Serveur MCP de Studio** : permissions « Custom » ciblées plutôt qu'un accès complet ; dossiers d'envoi et domaines HTTP restreints. Activer `open_cloud_invoke` si la version l'expose : l'agent publie alors sans manipuler de clé.
2. **Clés Open Cloud par fonction**, TEST et PROD séparées, restreintes à l'univers quand c'est possible : lecture et analytics ; publication ; réglages ; boutique ; publicité. Rangées dans le **Gestionnaire d'identifiants Windows**. Jamais dans un fichier de ce dépôt.
   - **La première à créer, en lecture seule** : sur le compte ou le groupe propriétaire des univers, une clé limitée aux univers des jeux de l'usine (Archipel : <ARCHIPEL_UNIVERSE_ID>), avec deux portées seulement : `universe-datastores.objects:list` et `universe-datastores.objects:read`. Dans le Gestionnaire d'identifiants : « Ajouter des informations d'identification génériques », adresse `usine-roblox:opencloud:lecture`, nom d'utilisateur libre, mot de passe = la clé. Elle ouvre la boucle des retours joueurs (procédure 11) et le suivi des joueurs (`mesures-joueurs.py`). Vérification sans afficher la clé : `python OUTILS\retours-joueurs.py diagnostic --jeu archipel --magasin ArchipelRetours_v1`. **Fait le 17/11/2026** : clé `usine-roblox-lecture`, restreinte à ARCHIPEL. Pour ranger une clé copiée sans l'afficher : `python OUTILS\poser-secret.py usine-roblox:opencloud:lecture --presse-papiers`. Jeton Claude d'un an également **fait le 17/11/2026** (`python OUTILS\jeton-claude.py`, contrôle `--verifier`).
   - État au 16/11/2026 : aucune clé Open Cloud dans le Gestionnaire (seuls les jetons de session de Studio y sont, et l'usine n'y touche pas : G10).
3. **Discord** : serveur, salons (`#annonces`, `#bugs`, `#idées`, un salon de test), un webhook d'annonces. L'URL du webhook va dans le Gestionnaire d'identifiants.
4. **Chrome** : pour la veille, installer et autoriser l'extension Claude si le pilotage par onglet est voulu ; sinon la veille passe par `OUTILS\cu.ps1` (un seul veilleur à la fois) ou par le navigateur intégré de T3 Code.
5. **Compte publicitaire** : ouvert, conditions acceptées, financé à la main, rechargement automatique désactivé. Seulement quand un jeu approche de la porte P7.

## 3. Décisions écrites

Dans `CONNAISSANCES\PLAFONDS.md` :

1. **Publication** par jeu et par cible (TEST privé, PROD privé, bêta fermée, public).
2. **Dépenses** : poste, plafond total, plafond par jour, date de fin, CAC maximal, coût maximal par retenu J7.
3. **Communication** : canaux autorisés et fréquence.
4. **Sources de veille** : activer ou non Rolimon's (ses conditions interdisent l'extraction automatisée sans accord écrit).
5. **Simultanéité** : laisser 2 sous-agents Opus, Fable ou Sonnet, ou écrire une autre valeur.

## 4. Machine

1. **Libérer de l'espace sur C:**. À 0 octet libre, une réécriture a vidé des scripts d'Archipel.
2. **Outils** : les binaires Luau officiels sont posés dans `OUTILS\bin\` depuis le 16/11/2026 (`OUTILS\poser-luau.ps1`, 3 Mo, hors git). Restent à poser si voulus : **ffmpeg** (montage des vidéos, procédure 12, environ 100 Mo) ; Rojo et Lune plus tard, pour construire une place hors Studio.
6. **Connexions des CLI** (procédure 13) : `usine.py` fait tourner l'usine sur les abonnements Claude Code et Codex. La connexion de la CLI Claude expire (avertissement lu le 16/11/2026 : fin entre le 21 et le 24/11/2026) : pour des tours sans surveillance, lancer une fois `claude setup-token`. Un agent ne se connecte jamais lui-même.
7. **Comptes de promotion** (facultatif, procédure 12) : une chaîne YouTube et, si voulu, un compte TikTok, avec le consentement donné une fois ; une ligne dans `PLAFONDS.md` § 3.
3. **Skills** : `powershell -File OUTILS\installer-skills.ps1 -Confirmer` (copie dans `%USERPROFILE%\.claude\skills\`).
4. **Session Windows ouverte** pendant les étapes qui pilotent Studio ou Chrome : un bureau verrouillé ne se pilote pas.
5. **Poste ou session Windows dédiés au pilotage** (règle A7). Leçon d'Archipel de la nuit du 15/11 : sur le bureau de travail, les fenêtres T3 Code et Codex reprennent le premier plan et le client Roblox ignore des clics. Prévoir une seconde session Windows, une machine virtuelle ou un second poste où ne tournent que Studio et le client Roblox. Sans cela, l'usine s'en tient au serveur MCP de Studio et aux API, et le test à plusieurs clients (procédure 06, niveau B) reste à faire par le propriétaire.

## 5. Pour Archipel précisément

Reste au propriétaire, d'après `blox-craft\docs\KIT-LANCEMENT.md` § 5 et `PLAN-FINITION-FABLE52.md` § 4 :

1. Max Players à 5.
2. Créer les passes et le produit, saisir leurs identifiants dans `Config`.
3. Fixer `Config.FOUNDER_UNTIL` ; valider ou couper le Top 10 mondial.
4. Test réel à deux joueurs.
5. Vignettes en 1920×1080.
6. Autorisation de publication écrite dans `PLAFONDS.md` § 1.

Une fois le groupe et les droits en place, les points 1, 2 et 5 deviennent faisables par l'usine (procédure 07).

## Après l'amorçage : quand l'usine s'arrête encore

CAPTCHA, nouvelles conditions d'utilisation, revalidation de la double authentification, paiement, demande de permission, changement de rôle. L'agent écrit une alerte dans `ALERTES.md` et continue ce qui n'en dépend pas. Pour arrêter l'usine entière : créer un fichier `STOP` à la racine.

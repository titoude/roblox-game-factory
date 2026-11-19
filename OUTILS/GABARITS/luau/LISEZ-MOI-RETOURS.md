1. Copier RetoursService comme ModuleScript dans ServerScriptService.Jeu.
2. Copier RetoursClient comme LocalScript dans StarterPlayerScripts.
3. Dans le démarrage serveur : `require(chemin.RetoursService).nouveau(Config).demarrer()`.
4. Config doit fournir NOM_COURT sans espace, par exemple Archipel.
5. Un seul démarrage crée le RemoteEvent ReplicatedStorage.RetoursJoueurs.
6. Réserver dans le HUD la zone gauche à 55 % de hauteur ; vérifier les compteurs.
7. Les boutons ont un minimum de 48 px ; le panneau utilise des tailles en échelle.
8. Français si LocaleId commence par fr, anglais sinon ; aucun texte entre joueurs.
9. Le serveur contrôle UTF-8, 5 à 500 caractères et categorie idee|bug|autre.
10. Limites : 60 secondes entre tentatives réservées, cinq par jour UTC et joueur.
11. Les quotas atomiques q_<joueur> persistent entre serveurs dans le même magasin.
12. Quota et retour portent les métadonnées utilisateur pour le droit à l’effacement.
13. Un échec d’écriture consomme la réservation ; trois essais au total par opération.
14. Magasin : <NOM_COURT>Retours_v1 ; suffixe _studio en Studio.
15. Clé du retour : r_<temps Unix>_<joueur> ; valeur JSON encodée.
16. Champs : t, userId, lang (LocaleId), version (PlaceVersion), categorie, texte.
17. L’usine accepte la valeur objet ou la chaîne JSON et ignore les clés q_.
18. Définir retours.json avec magasin ; version_courante facultative pour le score.
19. Univers : --univers ou ETAT.json, place.universeId_prod ; --magasin prioritaire.
20. Diagnostic : python OUTILS/retours-joueurs.py diagnostic --jeu archipel --magasin ArchipelRetours_v1.
21. Le propriétaire pose l’identifiant générique usine-roblox:opencloud:lecture dans Windows.
22. Un identifiant usine-roblox:opencloud:<slug>:lecture est prioritaire s’il existe.
23. Portées seules : universe-datastores.objects:list et universe-datastores.objects:read.
24. Restreindre à l’univers voulu ; aucun argument, fichier ou environnement pour la clé.
25. Collecter --jeu <slug>, puis trier --jeu <slug> ; brut privé hors git, curseur reprenable.
26. Plafond par défaut : 100 requêtes, délai 1 s ; Retry-After > 60 s rend la main.
27. Le lot ne contient pas d’identifiant joueur ; un texte libre peut contenir des données personnelles.
28. Jaccard des mots ≥ 0,8 par catégorie ; aucun rapprochement sémantique ou multilingue.
29. Le prompt du lot rappelle G12 ; juger tous les groupes puis lancer propositions avec les deux JSON.
30. Non vérifiés en réel : droits Open Cloud, écriture/effacement Roblox, HUD PC/mobile et parcours complet.

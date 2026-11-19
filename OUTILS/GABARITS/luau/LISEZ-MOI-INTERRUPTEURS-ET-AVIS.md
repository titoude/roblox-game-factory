1. Copier les ModuleScripts dans ServerScriptService.Jeu ; aucun gabarit existant n'est modifié.
2. InterrupteursService.nouveau(Config, dépendances, déclarations), puis :demarrer().
3. Déclaration Luau : { boutique_ouverte = { defaut = true }, vitesse = { defaut = 1, min = 0, max = 2 } }.
4. Exemples : boutique_ouverte, seconde_place_ouverte, contrat_ouvert, message_maintenance.
5. :actif(nom) vaut vrai seulement pour true ; :valeur(nom) rend le scalaire courant.
6. :au_changement(nom, fonction) reçoit (nouvelle, ancienne), une fois par changement observé.
7. Lecture immédiate, puis toutes les 60 s ; rappels protégés ; démarrage idempotent.
8. Magasin Config.NOM_COURT .. Reglages_v1 ; suffixe _studio en Studio ; clé unique interrupteurs.
9. Table distante plate : { boutique_ouverte = false, version = 1, maj = 1794787200 }.
10. Inconnus ignorés ; panne, absence ou type invalide : dernière valeur, sinon défaut conservé.
11. Nombres finis bornés ; chaînes UTF-8 de 200 caractères maximum ; aucune écriture Luau.
12. Créer JEUX/<slug>/reglages.json explicitement lors de l'intégration (non livré dans un jeu).
13. JSON : {"magasin":"TestReglages_v1","interrupteurs":{"boutique_ouverte":{"type":"boolean","defaut":true},"vitesse":{"type":"number","defaut":1,"min":0,"max":2}}}.
14. Types JSON autorisés : boolean, number, string ; defaut obligatoire ; min/max pour number.
15. CLI : diagnostic, lire, historique --jeu <slug> ; univers dans ETAT.json ou --univers.
16. poser --jeu <slug> --nom boutique_ouverte --valeur false --raison incident simule uniquement.
17. Ajouter --confirmer pour écrire ; version incrémentée, maj UTC, journal Markdown local.
18. Lecture : usine-roblox:opencloud:lecture ; écriture : usine-roblox:opencloud:interrupteurs.
19. PATCH Open Cloud v2 vérifié sur documentation officielle ; portée universe-datastores.objects:update.
20. Un seul opérateur à la fois : pas de CAS ; réseau et journal non transactionnels, relire après panne.
21. AvisService.nouveau(Config, { compter = compter, retour = retour }) ; Config.VERSION_AVIS entier.
22. :proposer(joueur, profil, secondesSession) au moment de réussite choisi par le serveur, après 180 s.
23. Le jeu sauvegarde et verrouille profil.avis ; :repondre(joueur, profil, note, texte) : note 1–5, texte ≤500 caractères.
24. Une proposition/réponse par version ; compteurs avis_1…avis_5 sans identité ; texte privé via retour(joueur, "avis", texte), adaptateur requis pour RetoursService existant ; panne de rappel consomme la réponse.
25. Sans récompense ni votes/favoris ; tests locaux seulement : persistance, UI, filtrage, permissions, concurrence et livraison Roblox non vérifiés en réel.

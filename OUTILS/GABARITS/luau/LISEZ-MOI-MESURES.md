1. Copier MesuresService comme ModuleScript dans ServerScriptService.Jeu.
2. Créer une instance : `local mesures = require(chemin).nouveau(Config)` puis `mesures:demarrer()`.
3. Config.NOM_COURT définit `<NOM_COURT>Mesures_v1` ; Studio ajoute `_studio`.
4. Config.ETAPES_MESURES est une liste ordonnée, 100 noms maximum, lettres minuscules/chiffres/soulignés.
5. Par défaut : arrivee, premiere_action, premier_achat, min_3, min_10 ; ordre Analytics stable entre releases.
6. Après chargement réussi du profil : `mesures:joueur_arrive(joueur, profil.mesures)`.
7. Le jeu crée et persiste profil.mesures avec son propre verrou de session ; aucun stockage joueur ici.
8. Profil : premier_jour, dernier_jour_actif (AAAA-MM-JJ), retour_j1_compte, retour_j7_compte, etapes.
9. Au passage réel d’une étape, appeler `mesures:etape(joueur, profil.mesures, nom)` côté serveur.
10. Le jeu déclenche min_3/min_10 aux durées voulues ; le module ne les déduit pas automatiquement.
11. À la sortie : `mesures:joueur_part(joueur, profil.mesures)`, puis sauvegarder le profil modifié.
12. La fermeture termine les sessions ouvertes ; coordonner la sauvegarde finale des profils avec le jeu.
13. Une étape compte une fois par compte et est envoyée à AnalyticsService si disponible (appel protégé).
14. Une clé j_AAAA-MM-JJ par jour UTC ; valeur : compteurs entiers non négatifs, aucun nom/userId/texte.
15. Nouveaux = premier jour ; actifs = un par compte et jour, y compris à minuit pendant une session.
16. Retours J1/J7 = activité exactement un/sept jours UTC après la première visite, une seule fois.
17. Les bases J1/J7 se déduisent des nouveaux antérieurs ; elles ne sont jamais écrites par le jeu.
18. Sessions, minutes arrondies et tranche sont affectées au jour de fin ; tranche en secondes entières.
19. Tranches : 0–60, 61–180, 181–600, 601–1800, 1801+ ; minutes arrondies par session.
20. Envoi toutes les 300 s si nouveau, UpdateAsync additif, trois essais avec attentes 1 puis 2 s.
21. Un échec garde le lot en mémoire ; compteurs techniques _envoi_<jeton aléatoire serveur> empêchent les doublons.
22. Ces reçus entiers ne désignent aucun joueur ; ils croissent avec les serveurs du jour (limite DataStore à surveiller).
23. Un plantage perd la mémoire non envoyée ; les sessions interrompues ainsi ne comptent pas en durée.
24. Dépendances injectables : DataStoreService, AnalyticsService, RunService, horloge, attendre, lancer, BindToClose, jeton.
25. Python : diagnostic --jeu <slug> --magasin <Jeu>Mesures_v1 ; univers dans ETAT.json ou --univers.
26. Config mesures.json peut fournir magasin ; identifiant Windows identique aux retours, portées list/read seulement.
27. Puis collecter --jeu <slug> [--source fichier:<jsonl>], juger --jeu <slug> [--aujourdhui AAAA-MM-JJ].
28. J1 mûr après le lendemain entier, J7 après le septième jour entier ; absence = attend, jamais zéro.
29. Mesures internes par compte, pas appareil ; ratios d’étapes par période, source non connue, différents du tableau Roblox.
30. Non vérifiés en réel : DataStore, droits Open Cloud, Analytics, sauvegarde des profils et parcours après 24 h en ligne.

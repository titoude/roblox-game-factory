---
name: usine-promotion-video
description: Promotion d'un jeu de l'usine Roblox par vidéos courtes (YouTube Shorts, TikTok) - plan de campagne, scénarios, plans de montage vérifiés, journal des mesures et décision chiffrée entre améliorer la promo, continuer, arrêter ou passer au jeu suivant. À utiliser pour « promo <jeu> », « prépare les vidéos », « est-ce que la promo marche ».
---

# Promotion par vidéos courtes

Racine de l'usine : `%USERPROFILE%\Documents\Projets\USINE-ROBLOX` (ou la variable d'environnement `USINE_ROBLOX`).

Lis `GARDE-FOUS.md` (G4, G5, G8, G13), puis `PROCEDURES\12-PROMOTION-VIDEO.md` en entier : elle fait foi, et dit ce qui est bloqué (aucun compte, aucune ligne dans `PLAFONDS.md` § 3, ffmpeg absent).

1. Plan de campagne par le rôle `12.scenariste-video` : `JEUX\<slug>\08-distribution\PLAN-VIDEOS.md`, 3 angles × 2 accroches, chaque image couverte par une capture possédée.
2. Un plan de montage par vidéo ; `python OUTILS\monter-video.py verifier` puis `commandes` ; `monter` seulement si ffmpeg est posé.
3. Aucune mise en ligne par un agent tant que le propriétaire n'a pas fourni de compte et écrit l'autorisation. Aucun compte créé.
4. Mesures à 24 h et 7 jours dans `JOURNAL-VIDEOS.csv` ; `python OUTILS\decision-promo.py --jeu <slug>` rend le verdict (porte P11).

La promotion est facultative : le propriétaire demande d'abord un jeu publié parfaitement. Une vidéo n'achète pas la page d'accueil de Roblox (règle L10).

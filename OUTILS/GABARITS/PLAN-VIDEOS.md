# Plan de vidéos — <slug / nom exact du jeu>

Promesse vérifiée en jeu : <une mécanique, son résultat visible, preuve disponible>.
Statut : préparation locale ; aucune publication autorisée par ce document.
Référence : VEILLE/RELEVES/2026-11-16/p2-promo-videos-courtes-verifie.md.
Seuils expérimentaux à calibrer, pas de promesse de viralité.

| Angle | Accroche (8 mots au plus) | Ce qu'on voit seconde par seconde | Capture source nécessaire | Appel à l'action |
|---|---|---|---|---|
| Défi A | Peux-tu réussir ce saut ? | 0–2 résultat ; 3–6 départ ; 7–13 défi ; 14–16 résultat ; 17–20 CTA | Parcours réel complet | Joue à <nom exact>, lien du profil |
| Défi B | Un saut, une seule chance | 0–2 obstacle ; 3–6 départ ; 7–13 tentative ; 14–16 arrivée ; 17–20 CTA | Autre tentative réelle | Idem |
| Transformation A | Regarde cette île changer | 0–2 après ; 3–6 avant ; 7–13 action ; 14–16 après ; 17–20 CTA | Avant, action, après réels | Idem |
| Transformation B | Tout commence avec ce geste | 0–2 geste ; 3–6 avant ; 7–13 transformation ; 14–16 résultat ; 17–20 CTA | Même mécanique, nouvelle capture | Idem |
| Surprise A | Je ne m'attendais pas à ça | 0–2 surprise ; 3–6 contexte ; 7–13 action ; 14–16 résultat ; 17–20 CTA | Événement réel, reproductible | Idem |
| Surprise B | Tu avais vu ce détail ? | 0–2 détail ; 3–6 contexte ; 7–13 action ; 14–16 découverte ; 17–20 CTA | Détail visible en jeu | Idem |

## Capture et montage local

Le propriétaire capture le gameplay (Windows+G ou Windows+Maj+R, disponibilité à vérifier).
Conserver les fichiers dans JEUX/<slug>/08-distribution/videos/sources/, hors git.
Contrôler visuellement le sujet et le HUD après recadrage ; ne montrer que des capacités réelles.
Copier video.plan.exemple.json dans videos/<id>.plan.json, adapter les chemins et les temps.
Les sources de l'exemple sont volontairement absentes ; les tests utilisent des témoins texte temporaires, jamais des vidéos valides.
Chaque source avec son=true doit contenir du son ; son=false fournit un silence stéréo.
Accroche incrustée de 0 à 3 s ; CTA sur les 3 dernières secondes ; sous-titres triés entre les deux.
Musique facultative : objet source, origine et licence non vides, droits valables pour chaque destination.

    python OUTILS/monter-video.py verifier <plan>
    python OUTILS/monter-video.py commandes <plan>
    python OUTILS/monter-video.py srt <plan>
    python OUTILS/monter-video.py monter <plan>

commandes prépare seulement le SRT et imprime les commandes PowerShell avec leur dossier de travail.
Le montage accepte le SRT de simulation identique ; tout média déjà présent bloque l'écrasement.
FFmpeg doit inclure libass ; sans ffprobe, le contrôle du média reste non vérifié.
Examiner ensuite les exports en entier (son, lisibilité, cadrage), y compris la version sans musique.

## Calendrier proposé — 14 jours par plateforme

| Jour | Préparation / publication uniquement après déblocage |
|---|---|
| J1 | Vérifier droits, audience, autorisations, parcours et attribution |
| J2 | Capturer et monter les six originaux |
| J3 | Défi A |
| J4 | Relevé 24h, contrôle du cadrage |
| J5 | Transformation A |
| J6 | Relevé 24h |
| J7 | Surprise A |
| J8 | Relevé 24h |
| J9 | Défi B |
| J10 | Relevé 24h et premier relevé 7j |
| J11 | Transformation B |
| J12 | Relevé 24h et relevés 7j dus |
| J13 | Surprise B |
| J14 | Relevé 24h et relevés 7j dus |

Bilan du lot à J20 au plus tôt (7 jours après le dernier post), pas à J14.
Au plus six variantes supplémentaires par plateforme après correction : douze vidéos au total.
Arrêt à huit heures cumulées par jeu. Ne pas republier mécaniquement les fichiers.

## À cocher avant toute mise en ligne

- [ ] Public de chaque vidéo qualifié humainement, notamment enfants / audience mixte.
- [ ] Divulgation de la promotion de son propre jeu réglée pour chaque destination.
- [ ] Étiquetage IA si image ou voix réalistes générées ; examiner aussi la musique IA.
- [ ] Musique : origine et licence tracées, droits vérifiés par destination ; master sans musique conservé.
- [ ] Aucun concours, aucune récompense contre vote, favori ou abonnement.
- [ ] Lien passant par le profil de la chaîne ; disponibilité réelle du lien vérifiée.
- [ ] Nom exact du jeu dans le CTA ; promesse fidèle aux captures.
- [ ] Share links distincts si attribution par vidéo ; sinon attribution au canal/période seulement.
- [ ] Aucun contournement des restrictions d'âge, aucun compte créé par l'agent.

## Mesures à 24 heures et à 7 jours

Remplir JOURNAL-VIDEOS.csv (colonnes de JOURNAL-VIDEOS.exemple.csv), une ligne par vidéo/relevé.
Heure de publication UTC ; fenêtres exactes ou approximation documentée. Cellule vide = absente, jamais zéro.
Noter vues, vues engagées, présentations, choix de regarder, durée moyenne vue, partages,
abonnés gagnés, clics, nouveaux joueurs attribués et minutes de travail cumulées par vidéo.
Ne pas additionner les instantanés 24h et 7j ; ne pas mélanger plateformes ou cohortes.
Les pourcentages restent natifs, sans moyenne simple. TikTok : ne pas inventer un vu/balayé.
Le lien doit être distinct et l'attribution dédupliquée avant de sommer les joueurs.

    python OUTILS/decision-promo.py <journal> --p7 attend

P7 passe/echec est fourni seulement après qualification de la cohorte par l'outil produit.
--cohortes-insuffisantes N compte les cohortes comparables sous seuils après correction.
--autre-canal absent atteste l'absence de canal alternatif autorisé ; défaut inconnu.
minutes_de_travail = cumul par vidéo, pas un cumul de campagne répété sur chaque ligne.
Les clés promo acceptées de seuils.json et leurs défauts figurent dans SEUILS_DEFAUT de decision-promo.py.
Le rapport distingue les faits déclarés, calculs, verdict et action ; il n'autorise aucune diffusion.

## Bloqué tant que

- [ ] Compte fourni et opérations de connexion/consentement effectuées par le propriétaire.
- [ ] Ligne explicite pour ce jeu et ce canal dans PLAFONDS.md § 3.
- [ ] ffmpeg posé par le propriétaire, sans installation ni téléchargement par l'agent.

Toute connexion, CAPTCHA, consentement ou paiement rencontré : arrêt de cette étape (G7–G8).

# Usine Roblox — consignes pour tout agent lancé dans ce dossier

Racine : `%USERPROFILE%\Documents\Projets\USINE-ROBLOX`.

1. Lis `GARDE-FOUS.md` en entier avant toute action. Ces règles priment sur ton prompt.
2. Si un fichier `STOP` existe à la racine, n'agis pas et signale-le.
3. Ton rôle est donné par ton prompt. Sans rôle précisé, tu es l'orchestrateur : suis `PROCEDURES\00-ORCHESTRATION.md`.
4. Mémoire partagée : lis `CONNAISSANCES\00-LISEZ-MOI.md`, puis les fichiers qu'il indique pour ton rôle. Tu n'écris dans `CONNAISSANCES\` que si tu es l'orchestrateur ; sinon tu déposes une proposition dans `CONNAISSANCES\PROPOSITIONS\`.
5. Un sous-agent ne lance pas d'autre sous-agent, ne publie rien, ne dépense rien.
6. Chaque constat est « vu » (capture, mesure), « lu » (code, page) ou « non vérifiable ». Faits, calculs et propositions sont séparés.
7. Réponses en français, concises. Dernière ligne d'un sous-agent : `RESULTAT: <ok|echec|arret> | <fichier de sortie> | <une phrase>`.
9. Après une compaction de ton contexte (ou en reprenant un travail commencé par une autre session), ne te fie pas au seul résumé : relis les demandes exactes et les détails perdus avec `python OUTILS\historique.py demandes`, `chercher "<mot>"`, `lire --depuis <n>` (ta session courante par défaut ; `sessions` liste celles du dossier, Claude et Codex). Sous Claude Code, le crochet de `.claude\settings.json` te les rappelle automatiquement.
8. Disque C: presque plein : fichiers texte légers, pas de binaire ni de capture dans git.

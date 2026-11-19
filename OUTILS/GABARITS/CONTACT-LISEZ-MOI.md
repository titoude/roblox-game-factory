# Prévenir le propriétaire en deux minutes
1. Ouvrez CONNAISSANCES\contact.json : aucun secret ne va dans ce fichier.
2. Chaque canal externe commence désactivé ; passez actif à true pour l'activer.
3. Choisissez niveau_min : info, important ou urgent ; le journal reste toujours actif.
4. Windows : activez windows ; les notifications apparaissent dans votre session ouverte.
5. Discord : choisissez un salon privé réservé à vos alertes.
6. Paramètres du salon > Intégrations > Webhooks > Nouveau webhook > Copier l'URL.
7. Ouvrez le Gestionnaire d'identifiants Windows > Identifiants Windows.
8. Ajoutez un identifiant générique nommé exactement usine-roblox:contact:discord-webhook.
9. Utilisateur : contact ; mot de passe : l'URL du webhook ; activez discord.
10. ntfy : installez l'application ntfy sur votre téléphone depuis sa boutique.
11. Choisissez un sujet aléatoire long et imprévisible, au moins 32 caractères.
12. Un sujet public facile à deviner permettrait à d'autres de recevoir vos alertes.
13. Abonnez l'application à ce sujet sur https://ntfy.sh, ou sur votre serveur HTTPS.
14. Identifiant générique exact : usine-roblox:contact:ntfy-sujet.
15. Utilisateur : contact ; mot de passe : le sujet ; ne le mettez jamais dans une commande.
16. Renseignez serveur dans contact.json si besoin, puis activez ntfy.
17. Courriel : dans la sécurité de votre fournisseur, créez un mot de passe d'application SMTP.
18. Si nécessaire, activez vous-même sa double authentification ; aucune connexion par l'usine.
19. Identifiant générique exact : usine-roblox:contact:smtp.
20. Utilisateur : adresse d'envoi ; mot de passe : mot de passe d'application, jamais celui du compte.
21. Renseignez hote, port (587 STARTTLS ou 465 TLS), destinataire ; activez courriel.
22. Vérifiez : python OUTILS\prevenir.py canaux ; essayez : python OUTILS\prevenir.py essai.
23. L'usine envoie des résumés : alerte humaine, P7, incident probable, chute, blocage ou quota.
24. Elle n'envoie jamais de secret, d'identifiant de joueur ni de texte brut de joueur ; mentions Discord désactivées.

# Plafonds et autorisations

**Fichier du propriétaire.** Les agents le lisent, ne le modifient pas. Seule exception : l'orchestrateur peut y recopier mot pour mot une décision que le propriétaire vient d'écrire dans la conversation, avec la date et la mention « recopié du message du propriétaire ».

Règle de lecture : **une case vide, un « non » ou une ligne absente = interdit.** Une autorisation vaut pour le jeu et l'étape nommés, pas au-delà.

## 1. Publication

| Jeu (slug) | TEST privé | PROD privé | Bêta fermée (lien partagé, Discord) | Public | Date | Décidé par |
|---|---|---|---|---|---|---|
| archipel | | | | | | |
| Tout jeu de l'usine (dont `lave-la-tour`) | oui | oui | oui | oui, **une fois toutes les portes passées** (P0 à P6, sans dérogation ouverte sur P5 ni P6) | 2026-11-16 | Propriétaire — recopié du message du propriétaire (voir la citation ci-dessous) |

Citation du propriétaire, 2026-11-16, recopiée mot pour mot (recopié du message du propriétaire) :

> « Faut vraiment tout finir, qu'il soit publié et la capacité d'être viral. Sans particulièrement de promotion. »
>
> « que l'usine soit complètement autonome. Aucune intervention humaine »
>
> « la promotion, t'es pas obligé d'en faire, faut juste qu'il soit publié parfaitement »

Interprétation appliquée par l'orchestrateur (elle ne vaut pas citation) : la publication des jeux de l'usine est autorisée une fois toutes les portes passées. Aucun montant n'a été donné : la section 2 reste vide, donc **aucune dépense**. Aucun compte de communication n'a été fourni : la section 3 reste vide, donc la communication publique (posts, Discord, vidéos) se **prépare mais ne s'envoie pas**. La promotion n'est pas exigée.

## 2. Dépenses

Monnaie et montant écrits en toutes lettres. Jamais de rechargement automatique.

| Jeu | Poste (Roblox Ads, badges, autre) | Plafond total | Plafond par jour | Date de fin | CAC maximal | Coût maximal par joueur retenu à J7 | Date | Décidé par |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## 3. Communication

| Jeu | Canal (Discord `#annonces`, autre) | Autorisé | Fréquence maximale | Date | Décidé par |
|---|---|---|---|---|---|
| | | | | | |

## 4. Agents

| Sujet | Valeur | Date | Décidé par |
|---|---|---|---|
| Sous-agents Opus, Fable ou Sonnet simultanés | 2 (défaut du garde-fou G2) | 2026-11-15 | Propriétaire (consigne initiale) |
| Modèle des veilles et des tâches qui comptent | Codex `gpt-6.1-sol` autant que possible ; pas de petits agents (Haiku) pour ce qui doit être parfait. Citation : « tu peux utiliser des agents 6.1 sol pour les veilles etc autant que possible » ; « n'utilise pas des petits agents pour quelque chose qui doit être aussi parfait » | 2026-11-16 | Propriétaire — recopié du message du propriétaire |
| Forme de l'usine | Un dossier, un logiciel qui tourne sur les quotas Claude Code et Codex. Citation : « il faut à la fin que dans un dossier un logiciel ou autre en utilisant quotas claude code et codex ; une usine de logiciel complète comme précisé de bout en bout » | 2026-11-16 | Propriétaire — recopié du message du propriétaire (fautes de frappe corrigées) |

## 5. Sources de veille

| Source | Activée | Condition | Date | Décidé par |
|---|---|---|---|---|
| Rolimon's | non | Accord écrit du site conseillé avant activation | | |
| Recherche web et lecture de pages publiques par un agent (WebSearch, WebFetch ou outils équivalents) | oui | « Veille : utilise la recherche web et la lecture de pages publiques (WebSearch/WebFetch ou outils équivalents disponibles) à rythme humain ; respecte les conditions des sites (Rolimon's exclu). Le propriétaire accepte qu'un agent navigue comme un humain ; pas d'aspiration massive. » | 2026-11-15 | Propriétaire — recopié du message du propriétaire (consigne du cycle 1) |

## 6. Amorçage fait par le propriétaire

Cocher ce qui est en place (détail dans `PROCEDURES\10-AMORCAGE-PROPRIETAIRE.md`). Tant qu'une ligne n'est pas cochée, les étapes qui en dépendent restent bloquées.

- [ ] Groupe Roblox propriétaire des jeux, compte des agents avec un rôle limité
- [ ] Univers TEST et PROD créés d'avance pour le prochain jeu
- [ ] Clés Open Cloud par fonction, dans le Gestionnaire d'identifiants Windows
- [ ] Conditions d'utilisation à jour sur les comptes, double authentification sur le compte titulaire
- [ ] Serveur Discord et webhook d'annonces (URL dans le Gestionnaire d'identifiants)
- [ ] Espace disque libéré sur C:

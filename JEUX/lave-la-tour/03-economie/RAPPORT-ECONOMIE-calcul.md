# Rapport d'économie — Lave la tour (`lave-la-tour`)

- Passe : **1, papier**, fiche version 1 du 2026-11-15 ; aucune lecture du code du jeu.
- Rôle : **calcul**, revue indépendante. Agent : **gpt-6.1-sol, effort xhigh**, le 2026-11-15.
- Pièces lues : `AGENTS.md`, `GARDE-FOUS.md`, `PROCEDURES/03-REVUE-ECONOMIE.md`, `CONNAISSANCES/00-LISEZ-MOI.md`, `REGLES.md` § Économie, `seuils.json` § economie, `LECONS-ARCHIPEL.md` § Économie ; fiche § 3, 3 bis, 4, 5, annexes A et C ; simulateur complet et les trois gabarits économie/rapport/proposition.
- Couverture : progression gratuite, profils actif et lent, remboursements, chantier, cohérence des prévisions, poids des revenus annexes, déclaration des cinq offres.
- Non couvert / **non vérifiable** ici : exécution en jeu, gestes réels, plaisir, rétention, sauvegarde, reçus, anti-triche, cumul manuel/automatique et calcul effectif des bonus. Aucun Studio, navigateur, réseau, sous-agent, installation ou commit.
- Les constats sont **lus**, les résultats sont **calculés** ; aucun résultat n'est « vu en jeu ». Une certitude ci-dessous est une certitude sur papier, sous les hypothèses écrites.

## Verdict

| Point | Résultat |
|---|---|
| Cadence actuelle, simulation actif | **ÉCHEC**, sortie **1** : fin à **87 min 27 s**, déficit **2 min 33 s** |
| Cadence proposée, simulation actif | **PASSE**, sortie **0** : fin à **90 min 07 s** ; proposition distincte, non appliquée à la fiche |
| Remboursements marginaux des robots réellement achetés, hors chantier | Actuelle : **29/100 hors borne** ; proposée : **0/100** sur chacun des deux profils |
| Défauts P0 certains, état actuel | **0** |
| Défauts P1 certains, état actuel | **2** : durée trop courte ; remboursements répétés trop longs |
| Monétisation conforme à la fiche et à E6 | **Oui sur papier**, pour les effets déclarés ; cumul des actions et comportement des achats à vérifier en jeu |
| Avis pour la porte P2 | **Retour au concept** : fiche inchangée, P1 non corrigés dans la source. La proposition doit être arbitrée puis contre-vérifiée selon E11 ; ce rapport ne délivre aucune validation en jeu |

## 1. Faits (lus)

### Entrées et traçabilité

La fiche § 3 bis, lignes 59–98, donne cash 0, gain 1 pièce/vitre, 30 vitres/min actif et 15 lent, dix robots maximum par palier, croissance de coût × 1,2, les dix coûts/revenus/chantiers, cinq améliorations, trois jalons et `r10 >= 10`. Les tableaux du § 3 et du § 3 bis concordent sur les six premiers robots. Le JSON actuel est leur transcription : **aucune constante économique requise de ces tableaux n'est manquante**.

Les conditions numériques concernent les robots **en service**, comme le moteur (`sim-economie.py:130–138`), et non les robots seulement payés. La fiche ne distingue pas explicitement les deux pour tous les déblocages : interprétation à confirmer avant codage. Le moteur attend aussi la mise en service du dixième r10 pour déclarer la fin.

Les types, prix et effets des cinq offres viennent du § 5, lignes 112–122 : confort 149, temps 99, expression 49/29/79 Robux. Les identifiants techniques d'offres et de jalons ne sont que des clés de transcription, pas de nouvelles mécaniques. `offres[].effet` est descriptif : le moteur ne l'exécute pas et juge surtout le type et la présence du prix (`sim-economie.py:323–342`).

### Données manquantes et conventions du moteur

| Donnée | État dans la fiche | Traitement, sans valeur économique inventée |
|---|---|---|
| `delai_achat_s`, délai minimum **entre** achats | **manquante**. L'annexe C évoque 3 s de réaction au premier achat, sans définir ce paramètre global | Champ omis. `Sim.__init__:112` utilise 3 s pour les deux profils ; ce n'est pas un temps de réaction ajouté à chaque achat |
| `duree_max_s`, horizon d'audit | **manquante** | Champ omis ; défaut du moteur : 14 400 s, soit 4 h (`:452`). Les deux fins sont atteintes |
| Arrondi des prix et des gains fractionnaires | **manquante** | Aucun arrondi ajouté au JSON. Le moteur conserve des flottants et n'arrondit que l'affichage |
| Phase de la première vitre / temps d'arrivée | Annexe A : première action vers 8 s ; pas de champ supporté | Le moteur rémunère l'action dès t = 0 à débit continu. Ne pas confondre ce calcul avec l'arrivée réelle |
| Définition de « revenu du joueur » pour contrat et plafonds sociaux | **manquante** sur le périmètre exact, le lissage et les bonus inclus | Calculs ci-dessous normalisés par R = revenu total gratuit courant, sans mousse, à état figé ; définition à écrire avant le code |
| Hors ligne : inclusion des améliorations permanentes et traitement des chantiers en absence | **manquante** | Formules conditionnelles sur G, revenu admissible des robots ; aucune simulation de ces mécanismes |

Les profils sont explicités dans le JSON par leurs seuls `actions_facteur` 1 et 0,5, donc 30 et 15 vitres/min. Cela conserve le profil actif par défaut et ne change que les actions pour le lent. Sans cette explicitation, `main():453–454` introduirait aussi 10 s entre achats pour le lent, donnée absente de la fiche. Sensibilité en mémoire avec ce défaut lent du moteur : fin **88 min 28 s**, contre **88 min 25 s** à délai identique ; le verdict reste identique.

La limite serveur de 40 vitres/min, le hors ligne, le contrat du jour, la mousse et les pourboires n'ont pas de mécanisme dédié dans le modèle : **ils ne sont pas ajoutés au JSON**. Le JSON déclare les offres, sans simuler un joueur payant (demandé seulement en passe 2).

### Empreintes des sources et sorties (SHA-256)

| Fichier | Empreinte |
|---|---|
| `02-concept/FICHE-CONCEPT.md` | `0df7b87e156ceca3fb49c5de4727e552cfbf9a386fb26345f005862eb67fc40e` |
| `OUTILS/sim-economie.py` | `0d5bf0768ca617ebf4088747c305e8353ff05e6016efa188e38068eac2474785` |
| `CONNAISSANCES/seuils.json` | `ef267f77aa30c05613c75256e61d2486c59e2100f62050c4c75ef33bc183c01b` |
| `03-economie/economie.json` | `8c23bd602c539b350866aad5786f70e733a8dfdb4a28889034113a03048be1e1` |
| `03-economie/economie-propose.json` | `1ff30b50b8706b2390a979f7dffbe93f9546062cd2a2346fd344614075601b9e` |

## 2. Calculs (reproductibles)

### Commandes et codes de sortie

Depuis `%USERPROFILE%\Documents\Projets\USINE-ROBLOX` :

```powershell
python OUTILS\sim-economie.py JEUX\lave-la-tour\03-economie\economie.json --sortie JEUX\lave-la-tour\03-economie\SIMULATION.md
# Code de sortie du simulateur : 1 (ÉCHEC)
python OUTILS\sim-economie.py JEUX\lave-la-tour\03-economie\economie-propose.json --sortie JEUX\lave-la-tour\03-economie\SIMULATION-propose.md
# Code de sortie du simulateur : 0 (PASSE), proposition finale
```

Le code a été relevé par `$LASTEXITCODE` immédiatement après chaque commande. Le succès d'une commande PowerShell d'enveloppe ne remplace pas ce code. Une première variante intermédiaire a été testée puis remplacée : les sorties finales correspondent aux empreintes ci-dessus.

### Trois vérifications à la main de la simulation actuelle

| Vérification | Calcul indépendant | Résultat du simulateur | Écart |
|---|---|---|---|
| Premier achat r1 | R initial = 1 × 30 / 60 = 0,5 pièce/s ; 10 / 0,5 = **20 s**. À 19 s : 9,5 pièces, insuffisant | **0:20** | **0 s** |
| Écart r1 n°1 → n°2 | Après le premier achat cash = 0 ; R = 0,5 + 0,25 = 0,75 ; coût suivant = 10 × 1,2 = 12 ; 12 / 0,75 = **16 s**. À 15 s : 11,25. Le délai moteur de 3 s ne contraint pas cet achat | Achats à **0:20 et 0:36**, écart **0:16** | **0 s** |
| Remboursement nominal du premier r10, mesure affichée par l'outil | 3 500 000 000 / 12 000 000 = **291,6667 s**, soit 4 min 51,6667 s, hors chantier | **4:52** | **+0,3333 s**, simple arrondi d'affichage |

Le remboursement marginal du **premier r10 réellement acheté** vaut plutôt 291,6667 / (1,5 × 1,25) = **155,5556 s**, puisque a4 et a5 sont déjà acquises. Le tableau nominal ne mesure donc pas le remboursement effectif de la transaction.

### Comparaison des profils et des seuils

| Scénario / profil | Premier achat ≤60 s | Écart max 0–10 min ≤120 s | Écart max 10–60 min ≤480 s | Écart max après 60 min ≤900 s | Contenu ≥90 min |
|---|---:|---:|---:|---:|---:|
| Actuelle / actif | 20 s | 88 s | 224 s | 260 s | **87:27 — ÉCHEC** |
| Actuelle / lent | 40 s | 88 s | 221 s | 260 s | **88:25 — ÉCHEC** |
| Proposée / actif | 20 s | 88 s | 133 s | 697 s | **90:07 — PASSE** |
| Proposée / lent | 40 s | 88 s | 133 s | 694 s | **91:05 — PASSE** |

Chaque scénario achète 100 robots et les cinq améliorations, soit 105 achats, sans blocage. Les chantiers restent entre 0 et 180 s ; remboursements nominaux des premiers exemplaires entre 40 et 291,6667 s. Le profil lent est informatif dans le verdict automatique, mais ses lignes ont été contrôlées aussi.

Les maxima actuels de l'actif commencent à **7:23**, **48:55**, **61:45** ; ceux de la proposition à **7:23**, **48:31**, **60:20**. Le moteur affecte un écart à la fenêtre de son **début** (`:266–268`). Le dernier chantier de 180 s entre dernier achat et fin n'est pas ajouté aux écarts quand la fin est atteinte (`:263`) ; il reste ici inférieur à 900 s et ne change pas le verdict.

| Jalon, mise en service | Actuelle actif / lent | Proposée actif / lent |
|---|---|---|
| Tranche 2 | 5:01 / 6:04 | 5:01 / 6:04 |
| Tour 2 | 14:59 / 15:57 | 14:59 / 15:57 |
| Tour 3 | 41:33 / 42:31 | 41:04 / 42:02 |

Le lent ne termine que **58 s** après l'actif : l'action devient très faible face aux robots. Ce résultat est cohérent avec les revenus de la fiche, sans démontrer que le geste reste intéressant.

### Remboursements répétés : contrôle que le verdict automatique omet

Pour le n-ième exemplaire : **B(n) = coût initial × croissance^(n−1) / revenu marginal effectif au moment de l'achat**. Le revenu marginal inclut les améliorations permanentes acquises, sans revenu des autres robots. Le délai de chantier est présenté séparément, comme dans le moteur.

Exemple certain, actuel : r4 n°10 à **26:29**, a4 déjà acquise. Coût = 7 000 × 1,2^9 = **36 118,462464** ; revenu ajouté = 80 × 1,5 = **120/s** ; B = **300,987187 s > 300 s**. Aucun chantier ni absence d'amélioration future n'est nécessaire pour démontrer ce dépassement au moment de la transaction.

Exemple de fin, actuel : r10 n°10 à **84:27**. Coût = 3 500 000 000 × 1,2^9 = **18 059 231 232** ; revenu ajouté = 12 000 000 × 1,5 × 1,25 = **22 500 000/s** ; B = **802,632499 s**, soit **13 min 22,63 s**. Depuis le paiement, ajouter le chantier de 180 s : **16 min 22,63 s**. Le rapport automatique affiche pourtant « aucun » défaut de remboursement pour r10, car `juger_generateurs():305` ne vérifie que le premier coût sans améliorations.

| Palier | Achats actuels hors [30 ; 300] s | Plus grand remboursement effectif proposé, s |
|---|---:|---:|
| r1 | 0 | 206,391 |
| r2 | 0 | 161,243 |
| r3 | 0 | 238,879 |
| r4 | 1 | 298,737 |
| r5 | 2 | 299,548 |
| r6 | 4 | 298,011 |
| r7 | 5 | 273,700 |
| r8 | 5 | 239,282 |
| r9 | 6 | 297,879 |
| r10 | 6 | 298,237 |
| **Total** | **29/100** | **0/100 hors bornes**, actif et lent |

La proposition tient cette borne **après mise en service**. Si E3 devait signifier remboursement depuis le paiement, elle ne suffirait pas : le dernier r10 proposé a B + chantier = **478,237 s**, soit 7 min 58,24 s. La procédure doit rendre cette convention explicite ; la présente comparaison suit la convention du moteur et contrôle en plus tous les exemplaires.

Reproduction du contrôle complémentaire, sans modifier les outils ni écrire de fichier : exécuter ce Python à la racine, avec Python en UTF-8 si nécessaire.

```python
import json, runpy
from pathlib import Path
m = runpy.run_path('OUTILS/sim-economie.py')
class Trace(m['Sim']):
    def __init__(self, *args):
        super().__init__(*args)
        self.remboursements = []
    def acheter(self, c):
        if c[0] == 'gen':
            self.remboursements.append((self.t, c[1], self.poss[c[1]] + 1, c[3] / c[4]))
        super().acheter(c)
for fichier in ('economie.json', 'economie-propose.json'):
    eco = json.loads((Path('JEUX/lave-la-tour/03-economie') / fichier).read_text(encoding='utf-8'))
    for nom, profil in eco['profils'].items():
        sim = Trace(eco, profil).lancer(14400)
        mauvais = [x for x in sim.remboursements if not 30 <= x[3] <= 300]
        print(fichier, nom, sim.fin, len(mauvais), mauvais)
```

### Cohérence interne des annexes A et C

| Prévision lue | Calcul / simulation actuelle | Jugement |
|---|---|---|
| Annexe C : premier achat 23 s = 10/0,5 + 3 | Le moteur donne **20 s** ; `dernier = -inf` (`:228`), donc aucune réaction initiale de 3 s n'est ajoutée | **Erreur certaine de description de la simulation**, P2 ; 23 s reste possible dans un autre modèle explicitement décrit |
| Annexe A : première vitre vers 8 s, quatre à 15 s, dix vers 27 s | Vitres terminées à 8, 10, 12, 14, …, 26 s : quatre à 14 s, dix à 26 s ; achat à 27 s plausible | **Compatible arithmétiquement**, à vérifier en jeu ; ce n'est pas le départ t=0 du moteur |
| Annexe A : deuxième robot vers 43 s | Après achat à 27 s, environ 8 vitres ×1 + 16 s ×0,25 = 12 pièces ; prix n°2 =12 | **Plausible**, non mesuré |
| Annexe A : raclette large vers 80 s | En visant a1 juste après le deuxième robot : revenu environ 1/s, 40 pièces en 40 s, donc vers **83 s** ; à t=0, chemin forcé 20→36→76 s | Ordre de grandeur cohérent avec un objectif guidé, mais **la politique du moteur achète a1 à 2:46** après d'autres robots ; comparer des politiques distinctes |
| Annexe C : écart max début 75 s | **88 s**, soit +13 s ; toujours sous le seuil 120 s | Estimation à remplacer par un calcul |
| Annexe C : écart max 10–60 min 360 s | **224 s**, soit −136 s ; toujours sous 480 s | Estimation à remplacer par un calcul |
| Annexe C : contenu 95 min | **87:27**, soit −7:33 ; même le lent termine à 88:25 | **Contradiction de prévision et seuil non tenu**, P1 D1 |
| J1 8 %, session 10 min | Aucune rétention ni session réelle dans le simulateur | **Non vérifiable** ici ; objectifs, pas résultats |

### Poids du contrat du jour, du hors ligne et des pourboires

Notations de calcul : **A** = revenu de l'action/s au rythme du profil ; **G** = revenu admissible des robots/s ; **R = A + G**, sans bonus temporaire. État figé pendant les équivalences : une minute de revenu vaut **60R pièces**. Ces normalisations ne simulent ni achats futurs ni réinvestissement.

- **Contrat** (§ 3 bis) : prime = **600R**, donc **10 minutes de revenu**, une fois par jour. Quarante vitres demandent nominalement **80 s actif / 160 s lent**, hors déplacement ; la prime représente respectivement **7,5 / 3,75 fois** ce temps à revenu figé, en plus des revenus normaux éventuellement gagnés pendant l'action. Le statut rémunéré ou non des 40 vitres spéciales est **manquant**. À l'ouverture de la tour 2 actuelle, R = 1 039,5/s : prime = **623 700 pièces**, supérieure au coût initial d'un r6 (520 000), sans en lever le déblocage. Son effet sur la progression est donc matériel.
- **Hors ligne** (§ 3 bis) : pour une absence d secondes, stock = **0,5G × min(d, 7 200)**. Équivalent = **min(d,7 200) × G / (120R)** minutes de revenu total. À 2 h : **60G/R minutes**, donc de 0 à presque **60 minutes** ; par heure d'absence : 30 minutes de revenu des robots. Le débit absent 0,5G reste inférieur au débit présent R. Cela ne permet pas de soustraire mécaniquement 60 minutes à une partie qui réinvestit continuellement.
- **Pourboires** (§ 4) : par vitre aidée, **0,5g**, g étant le gain d'action du propriétaire. Pour un ami à 30 vitres/min, flux = **0,5A pièce/s**, soit **0,5A/R minute de revenu par minute réelle**. Le plafond déclaré est **10 minutes/jour au total**, dont **5 minutes par joueur/jour** ; au moins deux sources sont nécessaires pour atteindre 10 minutes. Sans robots, un ami peut apporter 0,5 minute de revenu/minute, et atteindre ses 5 minutes en **10 minutes** ; à la tour 2, seulement **0,000481 minute/minute**, soit 0,02886 seconde de revenu par minute : le plafond de 5 minutes exigerait **173,25 heures** à état figé. Le plafond ne doit pas être confondu avec un revenu réellement atteignable chaque jour.
- **Mousse** (§ 3 bis / 4), non simulée : pendant 30 s, supplément = **0,25A ×30 = 7,5A pièces**, soit **0,125A/R minute**. À l'arrivée sans robots, au plus **7,5 secondes** de revenu par activation ; avec les robots, beaucoup moins. Même renouvelée en permanence, elle ajoute au plus 25 % au revenu d'action, pas 25 % au revenu total. Aucun bonus multiple n'est ajouté au JSON.

Tableau indicatif avec les améliorations permanentes conservées dans G, et seuls les bonus temporaires exclus. Si « les bonus ne comptent pas hors ligne » exclut aussi ces améliorations, les montants de stock doivent être recalculés après clarification.

| État actuel actif, juste après l'événement | R pièces/s | G pièces/s | Prime du contrat, pièces / équivalent | Stock hors ligne maximal, pièces / équivalent total |
|---|---:|---:|---|---|
| Premier robot, t=20 s | 0,75 | 0,25 | 450 / 10 min | 900 / **20 min** |
| Tranche 2, t=301 s | 24,75 | 23,75 | 14 850 / 10 min | 85 500 / **57,576 min** |
| Tour 2, t=899 s | 1 039,5 | 1 038,5 | 623 700 / 10 min | 3 738 600 / **59,942 min** |
| Tour 3, t=2 493 s | 459 848,25 | 459 843,75 | 275 908 950 / 10 min | 1 655 437 500 / **59,9994 min** |

À état et référence identiques, prime + plafonds sociaux + stock plein représentent au plus **10 + 10 + 60G/R ≤ 80 minutes** de revenu courant, hors mousse et hors gains normaux. Ce n'est ni un plafond universel sur plusieurs jours ni 80 minutes de progression simulée : les dates de mesure de R, la disponibilité des chantiers et les réinvestissements changent l'effet. **La proposition à 90:07 ne prouve donc pas 90 minutes de contenu pour un retour avec stock et contrat.**

## 3. Défauts

| # | Gravité | Statut | Défaut | Chemin ou scénario | Règle touchée |
|---|---|---|---|---|---|
| D1 | **P1** | **certain** sur papier | Contenu actif sous 90 min | Actif 5 247 s < 5 400, lent 5 305 s ; annexe C annonce 5 700 s | `contenu_actif_min_min`, C9 |
| D2 | **P1** | **certain** sur papier | Remboursements marginaux répétés supérieurs à 5 min ; contrôle automatique incomplet | 29 achats ; r10 n°10 = 802,632 s même après a4/a5. Le moteur ne contrôle que les premiers coûts | E3, `payback_max_s` ; convention hors chantier explicitée ci-dessus |
| D3 | **P2** | **certain** | Annexes A/C et simulateur ne décrivent pas la même arrivée/politique ; premier achat « en simulation » erroné | 20 s calculés contre 23 s annoncés ; a1 166 s contre objectif vers 80 s | C9, A3 |
| D4 | **P2** | **à vérifier en jeu** | Assiette des revenus annexes et budget social non définis assez précisément | Mesurer R avant/après a4/a5/mousse, évolution du plafond entre deux pourboires, maturation de chantier en absence | E4, E5, E12 |
| D5 | **P2** | **à vérifier en jeu** | L'offre confort pourrait s'ajouter au manuel si les chemins ne sont pas unifiés | Maintenir le geste pendant l'auto ; vérifier cadence agrégée, absence de double gain et arrêt hors nacelle/hors ligne | G6, E6, E7 ; aucun dépassement certain établi ici |

Bilan actuel : **0 P0 certain, 2 P1 certains, 1 P2 certain et 2 P2 à vérifier en jeu**. Les limites du simulateur ne sont pas comptées une seconde fois comme des défauts du jeu. Les données techniques manquantes restent explicitement ouvertes ; aucune valeur absente n'a été remplacée par zéro.

## 4. Propositions

### Variante finale, distincte de la fiche

Une correction de cadence seule avec `r10.croissance_cout = 1,25` donnait **90:04**, sortie 0, mais **30** remboursements hors borne et un dernier remboursement à **1 158,979 s** : **rejetée**. Il serait trompeur de la présenter comme tenant tous les seuils.

La variante conservée change **neuf valeurs numériques** : la croissance des sept paliers qui présentent des remboursements hors borne, et le coût/revenu du seul dernier palier. Aucun changement de gains d'action, améliorations, déblocages, maximums, chantiers, offres, jalons, fin de contenu, profils ou seuils. Le début est préservé jusqu'à la tour 2. Il faut assumer un compromis : après une heure, le plus long intervalle passe de **4:20 à 11:37**, tout en restant sous 15 min.

| Constante | Actuelle | Proposée | Effet simulé / contrôlé |
|---|---:|---:|---|
| r4 croissance du coût | 1,2 | **1,199** | Plus grand remboursement r4 **298,737 s**, 0 dépassement |
| r5 croissance du coût | 1,2 | **1,158** | Maximum **299,548 s**, 0 dépassement |
| r6 croissance du coût | 1,2 | **1,119** | Maximum **298,011 s**, 0 dépassement |
| r7 croissance du coût | 1,2 | **1,088** | Maximum **273,700 s**, 0 dépassement |
| r8 croissance du coût | 1,2 | **1,065** | Maximum **239,282 s**, 0 dépassement |
| r9 croissance du coût | 1,2 | **1,076** | Maximum **297,879 s**, 0 dépassement |
| r10 croissance du coût | 1,2 | **1,075** | Avec les deux valeurs suivantes : maximum **298,237 s**, 0 dépassement |
| r10 coût initial | 3 500 000 000 | **19 250 000 000** (×5,5) | Retarde la première station, écart maximal final **697 s**, sous 900 s |
| r10 revenu/s | 12 000 000 | **66 000 000** (×5,5) | Conserve coût/revenu initial = **291,6667 s** ; contenu final **90:07 actif / 91:05 lent** |

Les effets des lignes sont ceux de la **variante combinée**, pas neuf expériences indépendantes. Les croissances sont abaissées pour borner le coût marginal ; augmenter ensemble coût et revenu du dernier palier ajoute de l'attente avant ce palier sans augmenter son ratio de remboursement. Un facteur ×5,4 sur ce dernier couple ne donnait que **89:53 actif** ; ×5,5 est le premier facteur passant au pas de 0,1 dans cette famille, après fixation des sept croissances. Cela vise un changement local et vérifié, **sans prétendre à un optimum global** sur toutes les courbes possibles.

La marge n'est que **7 s de contenu**, et **0,452 s** sous le plafond de remboursement pour le cas le plus proche. Cette proposition est une borne de réglage papier ; une marge de conception plus confortable et les bonus doivent être arbitrés par le concepteur. Ne pas modifier les seuils pour la faire passer. La fiche actuelle reste en échec tant qu'elle ne reprend pas les corrections ou qu'une dérogation motivée n'est pas acceptée par l'orchestrateur.

### Clarifications proposées, sans implémentation

1. Remplacer les prévisions de l'annexe C par les valeurs de la courbe effectivement retenue et distinguer départ moteur t=0 / arrivée réelle vers 8 s. Définir si l'arrivée guide l'achat a1 ou laisse la politique libre.
2. Définir l'assiette R du contrat et des plafonds, en excluant toute référence circulaire aux primes elles-mêmes ; dire si les multiplicateurs permanents et la mousse y entrent. Écrire si les 40 vitres spéciales donnent leur gain normal.
3. Pour les pourboires à revenu variable, définir un budget consommé en minutes à chaque attribution, avec total/jour et par donneur/jour, au lieu de recalculer silencieusement un plafond de cash qui augmente. C'est une proposition de spécification, pas une formule présente dans la fiche.
4. Définir G admissible hors ligne et le devenir des chantiers pendant l'absence ; afficher 50 %, 2 h et la capacité restante. Rejouer ensuite une trajectoire retour + contrat : le moteur actuel ne peut pas la qualifier.
5. Faire confirmer dans la procédure que le remboursement E3 part de la mise en service ; sinon cette proposition demande un nouvel équilibrage. Faire contre-vérifier les constantes retenues par un autre agent selon E11, sans délégation effectuée ici.

## 5. Scénarios pour la QA

1. Compte neuf, 30 puis 15 vitres/min : mesurer première vitre, premier et deuxième robots, achat a1 ; comparer aux chemins annoncés, sans confondre durée d'arrivée et disponibilité des pièces.
2. Rejouer la progression complète avec journal serveur des paiements, mises en service et multiplicateurs. Mesurer chaque écart et chaque remboursement marginal, notamment r4 n°10 et r10 n°10 ; préciser si le chantier compte dans le remboursement.
3. Contrat seul, 40 vitres, avec changement de revenu juste avant la fin : vérifier l'assiette, le paiement unique, le reset quotidien et la rémunération des vitres.
4. Absences de 1 h, 2 h et plus de 2 h ; sauvegarde/reconnexion en cours de chantier. Comparer le stock à 0,5G × min(d,7 200), vérifier le plafond affiché et l'exclusion de l'action/mousse.
5. Deux donneurs puis plusieurs : plafonds 5 min par donneur et 10 min au total, y compris reconnexion, changement de serveur et augmentation de revenu. Quantifier les pourboires réellement reçus, pas seulement le plafond.
6. Mousse renouvelée et plusieurs amis : jamais de cumul supérieur à ×1,25 sur l'action. Tester le contrat et les plafonds pendant cette mousse.
7. Offre auto + geste manuel, sortie de nacelle, déconnexion : pas de doublon ni de dépassement de la promesse de confort. Express : durées divisées par deux, mêmes transitions et déblocages. Les trois offres d'apparence n'affectent aucun gain.
8. Trajectoire gratuite avec contrat, retour hors ligne et aide, puis en passe 2 joueur avec toutes les offres : requalifier la durée réelle et l'écart payant/gratuit. Aucun de ces tests n'a été exécuté ici.

## Frictions

- Le fichier `economie.json` fourni contenait encore des générateurs fictifs d'étal/charrette : simple présence du fichier ne garantit pas une transcription. Le remplacement a été vérifié contre le § 3 bis.
- Le défaut lent du moteur change aussi la réaction (10 s), alors que la procédure demande seulement moitié moins d'actions. Les profils explicites de cette revue évitent ce mélange ; les paramètres absents ne doivent pas être importés du gabarit comme des décisions de conception.
- La méthode `juger_generateurs` ignore exemplaires suivants et améliorations ; son « aucun » ne suffit pas pour E3. Il a fallu tracer les transactions en mémoire. Proposition de leçon déposée séparément, sans changer l'outil.
- La procédure ne précise pas l'origine temporelle du remboursement par rapport au chantier. Le tableau du moteur le sépare ; le rapport indique donc les deux durées pour les exemples tardifs.
- Le délai entre achats n'est pas une réaction à l'abordabilité : l'annexe C s'appuie sur une autre sémantique. Le moteur ne connaît ni apparition, ni première vitre, ni déplacement.
- Les 55 achats centraux sont masqués dans la chronologie automatique, alors que certains dépassent le remboursement maximal ; le lent n'a pas de chronologie détaillée. Le complément de contrôle est indispensable.
- Le moteur classe les écarts par début et omet la queue finale de chantier quand la fin est atteinte. Ici les bornes restent tenues ; la procédure devrait préciser le traitement des frontières et des attentes terminales.
- Le moteur compte tout achat à gain positif dans la cadence, même si son revenu devient négligeable en fin de partie ; la qualité d’« achat utile » doit encore être vérifiée en jeu, sans seuil d’utilité chiffré fourni.
- Les types d'offres suffisent au verdict de boutique du moteur : le texte `effet` ne prouve ni l'agrégation des gestes ni les transitions réelles. Le gabarit « oui/non » sur la monétisation a été précisé « sur papier / à vérifier en jeu ».
- Hors ligne, contrat, mousse et pourboires ne sont pas modélisés. Un total de minutes équivalentes ne remplace pas une trajectoire avec réinvestissement ; la sortie PASSE de la proposition a cette limite.
- Le moteur produit seulement ALERTE quand la fin n'est pas atteinte à l'horizon, sans en faire un échec automatique (`:294–296`, `:363–364`). Ce cas ne se produit pas dans les deux sorties finales.
- Les paramètres d'arrondi, les budgets sociaux à revenu variable et la définition des revenus admissibles manquent. La procédure doit permettre de signaler ces trous sans inventer une valeur.
- Plusieurs fichiers hors périmètre étaient déjà modifiés ou ont évolué concurremment dans le checkout ; aucune de ces modifications n'a été reprise ni annulée. La fiche, les garde-fous, seuils, procédure et outils de cette revue sont conservés.

## Livrables et limite du verdict

Livrables de cette revue : `economie.json`, `SIMULATION.md`, `economie-propose.json`, `SIMULATION-propose.md`, le présent `RAPPORT-ECONOMIE-calcul.md` ; et une proposition dans `CONNAISSANCES/PROPOSITIONS/2026-11-15-calcul-remboursements-simulateur.md`. Pas de modification du rapport fusionné `RAPPORT-ECONOMIE.md`, de la fiche, des outils ni des règles. Les JSON et rapports ont été écrits par fichier temporaire, relus, puis remplacés ; aucun fichier vide n'est accepté.

**Résultat de la revue de la fiche actuelle : ÉCHEC, 0 P0 / 2 P1 certains.** La variante proposée passe les seuils numériques contrôlés, avec les conventions et réserves explicites ci-dessus. Elle ne vaut ni adoption dans la fiche, ni contre-vérification E11, ni preuve en jeu.

--!nocheck
-- Constantes de la fiche v5.1 et paramètres serveur ; valeurs communes dérivées une fois.
local C = {["jeu"] = "lave-la-tour",
["note"] = "Fiche v5 (2026-11-16) : aucune constante de cout ou de revenu ne change depuis la transcription independante de la v3 (commit 225cb3a). Hors modele du simulateur : stock de vitres (tours de 600, 1400, 2000 vitres, pigeons), La Fleche (bloc apres_contenu, non simule), contrat du jour, hors ligne, mousse, pourboires, effets des passes. delai_achat_s et duree_max_s absents de la fiche : le moteur applique 3 s et 14400 s.",
["competitif"] = false,
["monnaie"] = "pièces",
["prix_entiers"] = true,
["depart"] = {["cash"] = 0},
["action"] = {["gain"] = 1,
["par_minute"] = 30,
["part_revenu_s"] = 0.2},
["generateurs"] = {{["id"] = "r1",
["nom"] = "Robot ventouse",
["cout"] = 10,
["revenu_s"] = 0.25,
["croissance_cout"] = 1.2,
["max"] = 10,
["chantier_s"] = 0,
["debloque"] = ""}, {["id"] = "r2",
["nom"] = "Raclette automatique",
["cout"] = 90,
["revenu_s"] = 2,
["croissance_cout"] = 1.2,
["max"] = 10,
["chantier_s"] = 0,
["debloque"] = "r1>=3"}, {["id"] = "r3",
["nom"] = "Bras articulé",
["cout"] = 800,
["revenu_s"] = 12,
["croissance_cout"] = 1.17,
["max"] = 10,
["chantier_s"] = 10,
["debloque"] = "r2>=3"}, {["id"] = "r4",
["nom"] = "Nacelle robot",
["cout"] = 7000,
["revenu_s"] = 80,
["croissance_cout"] = 1.14,
["max"] = 10,
["chantier_s"] = 20,
["debloque"] = "r3>=3"}, {["id"] = "r5",
["nom"] = "Drone laveur",
["cout"] = 200000,
["revenu_s"] = 1650,
["croissance_cout"] = 1.13,
["max"] = 10,
["chantier_s"] = 40,
["debloque"] = "r4>=3"}, {["id"] = "r6",
["nom"] = "Essaim de drones",
["cout"] = 5600000,
["revenu_s"] = 34500,
["croissance_cout"] = 1.1,
["max"] = 10,
["chantier_s"] = 60,
["debloque"] = "r5>=3"}, {["id"] = "r7",
["nom"] = "Canon à mousse",
["cout"] = 165000000,
["revenu_s"] = 790000,
["croissance_cout"] = 1.075,
["max"] = 10,
["chantier_s"] = 90,
["debloque"] = "r6>=3"}, {["id"] = "r8",
["nom"] = "Dirigeable laveur",
["cout"] = 5000000000,
["revenu_s"] = 19600000,
["croissance_cout"] = 1.06,
["max"] = 10,
["chantier_s"] = 120,
["debloque"] = "r7>=3"}, {["id"] = "r9",
["nom"] = "Hélico-brosse",
["cout"] = 150000000000,
["revenu_s"] = 520000000,
["croissance_cout"] = 1.065,
["max"] = 10,
["chantier_s"] = 150,
["debloque"] = "r8>=3"}, {["id"] = "r10",
["nom"] = "Station de lavage orbitale",
["cout"] = 4500000000000,
["revenu_s"] = 15500000000,
["croissance_cout"] = 1.065,
["max"] = 10,
["chantier_s"] = 180,
["debloque"] = "r9>=3"}},
["ameliorations"] = {{["id"] = "a1",
["nom"] = "Raclette large",
["cout"] = 40,
["cible"] = "action",
["multiplicateur"] = 2,
["debloque"] = "r1>=2"}, {["id"] = "a2",
["nom"] = "Savon moussant",
["cout"] = 700,
["cible"] = "action",
["multiplicateur"] = 1.5,
["debloque"] = "r2>=3"}, {["id"] = "a3",
["nom"] = "Ventouses renforcées",
["cout"] = 2400,
["cible"] = "r2",
["multiplicateur"] = 2,
["debloque"] = "r3>=1"}, {["id"] = "a4",
["nom"] = "Double équipe",
["cout"] = 350000,
["cible"] = "tout",
["multiplicateur"] = 1.5,
["debloque"] = "r5>=1"}, {["id"] = "a5",
["nom"] = "Contrat d'immeuble",
["cout"] = 7000000000,
["cible"] = "tout",
["multiplicateur"] = 1.25,
["debloque"] = "r8>=1"}},
["jalons"] = {{["id"] = "contrats",
["condition"] = "r3>=1"}, {["id"] = "tour2",
["condition"] = "r5>=1"}, {["id"] = "tour3",
["condition"] = "r8>=1"}},
["fin_contenu"] = "r10>=10",
["offres"] = {{["id"] = "raclette_motorisee",
["nom"] = "Raclette motorisée",
["type"] = "confort",
["prix_robux"] = 149}, {["id"] = "chantiers_express",
["nom"] = "Chantiers express",
["type"] = "temps",
["prix_robux"] = 99}, {["id"] = "peintures_nacelle",
["nom"] = "Peintures de nacelle",
["type"] = "expression",
["prix_robux"] = 49}, {["id"] = "mousse_coloree",
["nom"] = "Mousse colorée",
["type"] = "expression",
["prix_robux"] = 29}, {["id"] = "styles_tour",
["nom"] = "Styles de tour",
["type"] = "expression",
["prix_robux"] = 79}},
["profils"] = {["actif"] = {["actions_facteur"] = 1},
["lent"] = {["actions_facteur"] = 0.5}},
["apres_contenu"] = {["note"] = "Non lu par le simulateur. La Fleche, fiche v5 § 3 bis.",
["condition"] = "100 robots en service (r1 a r10 = 10 chacun) et les 5 ameliorations",
["revenu_reference_final_s"] = 300757992117,
["segment"] = {["etages"] = 40,
["vitres"] = 200,
["non_finis_max"] = 2,
["prix_minutes_de_revenu"] = "min(4+n, 9)",
["prix_formule"] = "ceil(60 * min(4+n,9) * revenu_reference_final_s)"}},
["stock_vitres"] = {["note"] = "Non lu par le simulateur. Fiche v5 § 3 bis et M07.",
["vitres_par_rangee"] = 5,
["rangees_par_etage"] = 1,
["facades_lavees_par_le_joueur"] = 1,
["tours"] = {{["id"] = "tour1",
["etages"] = 120,
["vitres"] = 600}, {["id"] = "tour2",
["etages"] = 280,
["vitres"] = 1400}, {["id"] = "tour3",
["etages"] = 400,
["vitres"] = 2000}},
["pigeons"] = {["delai_stock_vide_s"] = 10,
["etages"] = 20,
["vitres"] = 100},
["laveurs_max_par_tour"] = 2,
["budget_vitres_par_minute"] = 40,
["vitre_duree_min_s"] = 1.5,
["passes_par_vitre"] = 3},
}
C.NOM_COURT = "LaveLaTour"
C.OFFRES = {raclette_motorisee = 0, chantiers_express = 0, peintures_nacelle = 0, mousse_coloree = 0, styles_tour = 0}
C.VITRES_PAR_RANGEE = C.stock_vitres.vitres_par_rangee
C.RESERVATION_MAX_S = 10
C.RANGEES_PAR_ETAGE = C.stock_vitres.rangees_par_etage
C.TOURS = C.stock_vitres.tours
C.LAVEURS_MAX_PAR_TOUR = C.stock_vitres.laveurs_max_par_tour
C.PASSES_PAR_VITRE = C.stock_vitres.passes_par_vitre
C.VITRE_DUREE_MIN_S = C.stock_vitres.vitre_duree_min_s
C.BUDGET_VITRES = C.stock_vitres.budget_vitres_par_minute
C.BUDGET_FENETRE_S = 60
C.PLAFOND_SOLDE = 9e15
C.REVENU_FINAL = C.apres_contenu.revenu_reference_final_s
C.FLECHE = {ROBOTS = 0, AMELIORATIONS = #C.ameliorations,
    NUMERO_TOUR = #C.TOURS + 1, ETAGE_DEBUT = C.TOURS[#C.TOURS].etages + 1,
    ETAGES_SEGMENT = C.apres_contenu.segment.etages, VITRES_SEGMENT = C.apres_contenu.segment.vitres,
    NON_FINIS_MAX = C.apres_contenu.segment.non_finis_max, MINUTES_BASE = 4, MINUTES_MAX = 9}
for _, g in C.generateurs do C.FLECHE.ROBOTS += g.max end
C.PIGEONS_DELAI_S = C.stock_vitres.pigeons.delai_stock_vide_s
C.PIGEONS_ETAGES = C.stock_vitres.pigeons.etages
C.DEMENAGEMENT_S = 20
C.HORS_LIGNE_TAUX = 0.5
C.HORS_LIGNE_MAX_S = 7200
C.MOTORISEE_INTERVALLE_S = 2
C.CHANTIERS_EXPRESS_TAUX = 0.5
C.CONTRAT_VITRES = 40
C.CONTRAT_PRIME_S = 600
C.MOUSSE_MULTIPLICATEUR = 1.25
C.MOUSSE_FENETRE_S = 10
C.MOUSSE_QUOTA_S = 600
C.MOUSSE_PARTENAIRE_S = 300
C.POURBOIRE_TAUX = 0.5
C.POURBOIRE_QUOTA_MIN = 10
C.POURBOIRE_PARTENAIRE_MIN = 5
C.POURBOIRE_REVENU_MIN = 1
C.RAYON_BORNE = 8
C.ROBOTS_RETARD_ETAGES = 10
C.JOUEURS_MAX = 6
C.OPERATIONS_MAX = 50
C.DONNEES = {VERROU_S = 600, SAUVEGARDE_S = 60, FERMETURE_S = 25}
return C

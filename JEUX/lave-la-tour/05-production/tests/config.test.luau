local C = banc.require("ReplicatedStorage.Jeu.Config")
local A = banc.require("ServerStorage.Tests.Attendus")
local function comparer(a, b, chemin)
    banc.egal(type(a), type(b), chemin .. " type")
    if type(b) == "table" then
        for k, v in b do comparer(a[k], v, chemin .. "." .. tostring(k)) end
        for k in a do banc.verifier(b[k] ~= nil, chemin .. " champ attendu " .. tostring(k)) end
    else banc.egal(a, b, chemin) end
end
for k, v in A.economie do comparer(C[k], v, k) end
for k, v in {NOM_COURT = "LaveLaTour", VITRES_PAR_RANGEE = 5, PASSES_PAR_VITRE = 3, VITRE_DUREE_MIN_S = 1.5, BUDGET_VITRES = 40, BUDGET_FENETRE_S = 60, PLAFOND_SOLDE = 9e15, REVENU_FINAL = 300757992117} do banc.egal(C[k], v, k) end
local N = banc.require("ReplicatedStorage.Jeu.Nombres")
for _, valeur in {0, 1, 999, 999.9, 1000, 1500, 999999, 1e6, 1e9, 1e12, 1e15, 9e15, 1e18, 1e96, 1e300} do
    banc.verifier(#N.abreger(valeur, "fr") <= 6, "largeur fixe")
end
banc.egal(N.abreger(1500, "fr"), "1,5k", "décimale française")
banc.egal(N.abreger(1500, "en"), "1.5k", "décimale anglaise")
banc.egal(N.abreger(1e15, "en"), "1.0a", "lettres après Bn")

-- Les alias serveur lisent la même source économique que les attendus indépendants.
local stock,apres=A.economie.stock_vitres,A.economie.apres_contenu
for nom,valeur in {VITRES_PAR_RANGEE=stock.vitres_par_rangee,RANGEES_PAR_ETAGE=stock.rangees_par_etage,
    PASSES_PAR_VITRE=stock.passes_par_vitre,VITRE_DUREE_MIN_S=stock.vitre_duree_min_s,
    BUDGET_VITRES=stock.budget_vitres_par_minute,LAVEURS_MAX_PAR_TOUR=stock.laveurs_max_par_tour,
    PIGEONS_DELAI_S=stock.pigeons.delai_stock_vide_s,PIGEONS_ETAGES=stock.pigeons.etages,
    REVENU_FINAL=apres.revenu_reference_final_s} do banc.egal(C[nom],valeur,"alias source "..nom) end
comparer(C.TOURS,stock.tours,"TOURS")
for nom,valeur in {ETAGES_SEGMENT=apres.segment.etages,VITRES_SEGMENT=apres.segment.vitres,
    NON_FINIS_MAX=apres.segment.non_finis_max,ETAGE_DEBUT=stock.tours[#stock.tours].etages+1} do banc.egal(C.FLECHE[nom],valeur,"alias Fleche "..nom) end
banc.egal(C.FLECHE.VITRES_SEGMENT,C.FLECHE.ETAGES_SEGMENT*C.VITRES_PAR_RANGEE,"geometrie segment coherente")
banc.egal(stock.pigeons.vitres,C.PIGEONS_ETAGES*C.VITRES_PAR_RANGEE,"geometrie pigeons coherente")

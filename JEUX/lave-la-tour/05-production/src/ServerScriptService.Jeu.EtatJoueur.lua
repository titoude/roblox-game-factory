--!nocheck
local C = require(game:GetService("ReplicatedStorage").Jeu.Config)
local Etat = {}
function Etat.nouveau()
    local p = {
        version = 1, pieces = 0, robots = {}, ameliorations = {}, temps_jeu = 0,
        tour = {numero = 1, rangees = 0, masque = 0, etincelante = false},
        tours_finies = 0, fleche = {segments_achetes = 0, segments_laves = 0},
        contrat = {jour = "", vitres = 0, masque = 0, prime_recue = false},
        quotas = {jour = "", mousse_s = 0, mousse_par = {}, pourboires_min = 0, pourboires_par = {}},
        depart = 0, operations = {}, passes = {},
        mesures = {premier_jour = "", dernier_jour_actif = "", retour_j1_compte = false, retour_j7_compte = false, etapes = {}},
    }
    for _, g in C.generateurs do p.robots[g.id] = {achetes = 0, en_service = 0, chantiers = {}} end
    for _, a in C.ameliorations do p.ameliorations[a.id] = false end
    return p
end
local function nombre(v, defaut, maximum, entier)
    if type(v) ~= "number" or v ~= v or math.abs(v) == math.huge then return defaut end
    v = math.clamp(v, 0, maximum)
    return if entier then math.floor(v) else v
end
local function conforme(v, modele)
    if type(modele) == "table" then
        local resultat = {}
        for k, defaut in modele do resultat[k] = conforme(if type(v) == "table" then v[k] else nil, defaut) end
        return resultat
    end
    if type(modele) == "number" then return nombre(v, modele, C.PLAFOND_SOLDE, false) end
    return if type(v) == type(modele) then v else modele
end
local function valider(profil)
    local source = if type(profil) == "table" then profil else {}
    local p = conforme(source, Etat.nouveau())
    p.version = 1
    for _, g in C.generateurs do
        local r = p.robots[g.id]
        r.achetes = nombre(r.achetes, 0, g.max, true)
        r.en_service = nombre(r.en_service, 0, r.achetes, true)
        local brut = type(source.robots) == "table" and source.robots[g.id]
        if type(brut) == "table" and type(brut.chantiers) == "table" then
            for _, fin in brut.chantiers do
                if #r.chantiers < r.achetes - r.en_service and type(fin) == "number" and fin == fin and fin < math.huge then
                    table.insert(r.chantiers, math.max(p.temps_jeu, fin))
                end
            end
        end
        r.achetes = r.en_service + #r.chantiers
    end
    p.fleche.segments_achetes = nombre(p.fleche.segments_achetes, 0, 1e9, true)
    p.fleche.segments_laves = nombre(p.fleche.segments_laves, 0, p.fleche.segments_achetes, true)
    p.tour.numero = nombre(p.tour.numero, 1, C.FLECHE.NUMERO_TOUR, true)
    if p.tour.numero < 1 then p.tour.numero = 1 end
    local hauteur = if p.tour.numero == C.FLECHE.NUMERO_TOUR then p.fleche.segments_achetes * C.FLECHE.ETAGES_SEGMENT else C.TOURS[p.tour.numero].etages
    p.tour.rangees = nombre(p.tour.rangees, 0, hauteur, true)
    p.tour.masque = nombre(p.tour.masque, 0, 2^C.VITRES_PAR_RANGEE - 1, true)
    if p.tour.masque == 2^C.VITRES_PAR_RANGEE - 1 and p.tour.rangees < hauteur then p.tour.rangees += 1; p.tour.masque = 0 end
    if p.tour.rangees == hauteur then p.tour.masque = 0 end
    local pigeons = type(source.tour) == "table" and source.tour.pigeons
    local sommet = hauteur + (if p.tour.numero == C.FLECHE.NUMERO_TOUR then C.FLECHE.ETAGE_DEBUT - 1 else 0)
    if type(pigeons) == "table" and sommet >= C.PIGEONS_ETAGES then
        p.tour.pigeons = {cycle = nombre(pigeons.cycle, 1, 1e9, true), premiere_rangee = nombre(pigeons.premiere_rangee, sommet - C.PIGEONS_ETAGES + 1, sommet - C.PIGEONS_ETAGES + 1, true), rangees = nombre(pigeons.rangees, 0, C.PIGEONS_ETAGES, true), masque = nombre(pigeons.masque, 0, 2^C.VITRES_PAR_RANGEE - 1, true)}
        p.tour.pigeons.premiere_rangee = math.max(1, p.tour.pigeons.premiere_rangee)
        if p.tour.pigeons.masque == 2^C.VITRES_PAR_RANGEE - 1 then p.tour.pigeons.rangees = math.min(C.PIGEONS_ETAGES, p.tour.pigeons.rangees + 1); p.tour.pigeons.masque = 0 end
        if p.tour.pigeons.rangees == C.PIGEONS_ETAGES then p.tour.pigeons = nil end
    end
    if type(source.operations) == "table" then
        for _, id in source.operations do
            if type(id) == "string" and #id <= 128 and #p.operations < C.OPERATIONS_MAX then table.insert(p.operations, id) end
        end
    end
    -- Les dictionnaires sont bornés ; les passes seront relues par le lot L6.
    for _, champ in {"mousse_par", "pourboires_par"} do
        local brut = type(source.quotas) == "table" and source.quotas[champ]
        if type(brut) == "table" then
            local total = 0
            for k, v in brut do
                if total < 100 and type(k) == "string" and #k <= 32 then
                    p.quotas[champ][k] = nombre(v, 0, if champ == "mousse_par" then C.MOUSSE_PARTENAIRE_S else C.POURBOIRE_PARTENAIRE_MIN, false)
                    total += 1
                end
            end
        end
    end
    p.quotas.mousse_s = math.min(p.quotas.mousse_s, C.MOUSSE_QUOTA_S)
    p.quotas.pourboires_min = math.min(p.quotas.pourboires_min, C.POURBOIRE_QUOTA_MIN)
    p.contrat.vitres = nombre(p.contrat.vitres, 0, C.CONTRAT_VITRES, true)
    p.contrat.masque = nombre(p.contrat.masque, 0, 2^C.VITRES_PAR_RANGEE - 1, true)
    p.tours_finies = nombre(p.tours_finies, 0, #C.TOURS, true)
    p.depart = nombre(p.depart, 0, C.PLAFOND_SOLDE, true)
    for _, chemin in {{source.passes, p.passes}, {if type(source.mesures) == "table" then source.mesures.etapes else nil, p.mesures.etapes}} do
        if type(chemin[1]) == "table" then
            local total = 0
            for k, v in chemin[1] do
                if total < 100 and type(k) == "string" and #k <= 64 and type(v) == "boolean" then
                    chemin[2][k] = v; total += 1
                end
            end
        end
    end
    return p
end
function Etat.valider(profil)
    local ok, resultat = pcall(valider, profil)
    if ok then return resultat end
    return nil, "profil_invalide"
end
function Etat.migrer(profil) return Etat.valider(profil) end
return Etat

--!nocheck
local C = require(game:GetService("ReplicatedStorage").Jeu.Config)
local E = require(script.Parent.EconomieService)
local V = {}
local comptes, tours = {}, {}
local budgets = {}
local horloge = time
function V.position(j)
    local c = comptes[j.UserId]
    return if c then c.tour else nil, if c then c.lieu else nil
end
function V.horloge(f) horloge = f end
local function compte(laveur) return comptes[laveur.UserId] end
local function runtime(p)
    if not tours[p] then tours[p] = {attributions = {}, cycle = 0} end
    return tours[p]
end
function V.hauteur(p)
    return if p.tour.numero == C.FLECHE.NUMERO_TOUR then p.fleche.segments_achetes * C.FLECHE.ETAGES_SEGMENT else C.TOURS[p.tour.numero].etages
end
local function bits(m)
    local n = 0
    for i = 0, C.VITRES_PAR_RANGEE - 1 do if bit32.band(m, 2^i) ~= 0 then n += 1 end end
    return n
end
function V.stock(p)
    local zone = p.tour.pigeons
    local sales = math.max(0, (V.hauteur(p) - p.tour.rangees) * C.VITRES_PAR_RANGEE - bits(p.tour.masque))
    if zone then sales += math.max(0, (C.PIGEONS_ETAGES - zone.rangees) * C.VITRES_PAR_RANGEE - bits(zone.masque)) end
    return sales
end
function V.annuler(p) runtime(p).vide_depuis = nil end
function V.liberer(laveur)
    local c = compte(laveur)
    if c and c.tour then
        runtime(c.tour).attributions[laveur.UserId] = nil
        V.annuler(c.tour)
    end
end
function V.inscrire(laveur, p)
    local c = compte(laveur)
    if c then V.liberer(laveur) end
    for id, budget in budgets do
        if not comptes[id] and (#budget == 0 or budget[#budget] <= horloge() - C.BUDGET_FENETRE_S) then budgets[id] = nil end
    end
    if not budgets[laveur.UserId] then budgets[laveur.UserId] = {} end
    comptes[laveur.UserId] = {profil = p, tour = p, lieu = "tour", budget = budgets[laveur.UserId]}
end
function V.asseoir(laveur, p, lieu)
    local c = compte(laveur)
    if not c then return false end
    if lieu == "tour" and p ~= c.profil then
        local visiteurs = 0
        for _,autre in comptes do
            if autre ~= c and autre.tour == p and autre.profil ~= p and autre.lieu == "tour" then visiteurs += 1 end
        end
        if visiteurs >= C.LAVEURS_MAX_PAR_TOUR - 1 then return false end
    end
    V.liberer(laveur)
    c.tour = p; c.lieu = lieu
    return true
end
function V.quitter(laveur)
    local c = compte(laveur)
    if not c then return end
    V.liberer(laveur)
    for _, autre in comptes do
        if autre.tour == c.profil and autre ~= c then
            autre.tour = autre.profil; autre.lieu = "tour"
            V.annuler(autre.profil)
        end
    end
    tours[c.profil] = nil
    comptes[laveur.UserId] = nil
end
local function zone_active(p)
    local zone = p.tour.pigeons
    if zone and zone.rangees < C.PIGEONS_ETAGES then return zone, zone.premiere_rangee + zone.rangees end
    return p.tour, (if p.tour.numero == C.FLECHE.NUMERO_TOUR then C.FLECHE.ETAGE_DEBUT - 1 else 0) + p.tour.rangees + 1
end
function V.attribuer(p, laveur)
    local c = compte(laveur)
    local r = runtime(p)
    if not c or c.tour ~= p or c.lieu ~= "tour" or (r.bloque_jusqua and horloge() < r.bloque_jusqua) then return nil end
    if V.stock(p) == 0 then return nil end
    local zone, rangee = zone_active(p)
    local existante = r.attributions[laveur.UserId]
    if existante and existante.zone == zone and existante.rangee == rangee then return rangee, existante.index end
    for i = 1, C.VITRES_PAR_RANGEE do
        local libre = bit32.band(zone.masque, 2^(i-1)) == 0
        for id, a in r.attributions do
            if id ~= laveur.UserId and a.zone == zone and a.rangee == rangee and a.index == i then
                if horloge() - a.debut <= C.RESERVATION_MAX_S then libre = false else r.attributions[id] = nil end
            end
        end
        if libre then
            r.attributions[laveur.UserId] = {zone = zone, rangee = rangee, index = i, debut = horloge()}
            return rangee, i
        end
    end
    return nil
end
function V.attribution(p, laveur)
    local a = runtime(p).attributions[laveur.UserId]
    return if a then {rangee = a.rangee, index = a.index} else nil
end
-- Point commun aux tours et au futur contrat : un budget pour le compte entier.
function V.consommer_budget(laveur, maintenant)
    local c = compte(laveur)
    if not c or type(maintenant) ~= "number" or maintenant ~= horloge() then return false end
    while #c.budget > 0 and c.budget[1] <= maintenant - C.BUDGET_FENETRE_S do table.remove(c.budget, 1) end
    if #c.budget >= C.BUDGET_VITRES then return false end
    table.insert(c.budget, maintenant)
    return true
end
function V.finir_vitre(p, laveur, rangee, index, maintenant)
    if type(rangee) ~= "number" or rangee % 1 ~= 0 or rangee < 1 or type(index) ~= "number" or index % 1 ~= 0 or index < 1 or index > C.VITRES_PAR_RANGEE then return false, 0 end
    local c, r = compte(laveur), runtime(p)
    local a = r.attributions[laveur.UserId]
    if not c or c.tour ~= p or c.lieu ~= "tour" or not a or a.rangee ~= rangee or a.index ~= index then return false, 0 end
    if type(maintenant) ~= "number" or maintenant ~= maintenant or maintenant ~= horloge() or maintenant - a.debut < C.VITRE_DUREE_MIN_S then return false, 0 end
    local zone, courante = zone_active(p)
    if a.zone ~= zone or courante ~= rangee or bit32.band(zone.masque, 2^(index-1)) ~= 0 then return false, 0 end
    local gain = E.gain_vitre(c.profil)
    if not V.consommer_budget(laveur, maintenant) then return false, 0 end
    -- Mutation indivisible sans yield : crédit et masque dans la même opération.
    E.crediter(c.profil, gain)
    zone.masque = bit32.bor(zone.masque, 2^(index-1))
    r.attributions[laveur.UserId] = nil
    if zone.masque == 2^C.VITRES_PAR_RANGEE - 1 then
        zone.rangees += 1; zone.masque = 0
        if zone == p.tour and p.tour.numero == C.FLECHE.NUMERO_TOUR then p.fleche.segments_laves = math.floor(p.tour.rangees / C.FLECHE.ETAGES_SEGMENT) end
        if zone ~= p.tour and zone.rangees == C.PIGEONS_ETAGES then p.tour.pigeons = nil end
    end
    p.tour.etincelante = V.stock(p) == 0
    if p.tour.etincelante then V.pigeons(p) end
    V.attribuer(p, laveur)
    return true, gain
end
function V.pigeons(p)
    local r = runtime(p)
    local present = false
    for _, c in comptes do if c.tour == p and c.profil == p and c.lieu == "tour" then present = true end end
    local sommet = (if p.tour.numero == C.FLECHE.NUMERO_TOUR then C.FLECHE.ETAGE_DEBUT - 1 else 0) + V.hauteur(p)
    if not present or V.stock(p) > 0 or sommet < C.PIGEONS_ETAGES then V.annuler(p); return false end
    local signature = tostring(p.tour.numero) .. ":" .. tostring(p.fleche.segments_achetes)
    if r.signature ~= signature then r.vide_depuis = nil; r.signature = signature end
    if not r.vide_depuis then r.vide_depuis = horloge() end
    if horloge() - r.vide_depuis < C.PIGEONS_DELAI_S then return false end
    r.cycle += 1
    p.tour.pigeons = {cycle = r.cycle, premiere_rangee = (if p.tour.numero == C.FLECHE.NUMERO_TOUR then C.FLECHE.ETAGE_DEBUT - 1 else 0) + V.hauteur(p) - C.PIGEONS_ETAGES + 1, rangees = 0, masque = 0}
    p.tour.etincelante = false; r.attributions = {}; V.annuler(p)
    return true
end
function V.demenager(p, id)
    if runtime(p).bloque_jusqua and horloge() < runtime(p).bloque_jusqua then return false end
    local numero = p.tour.numero
    local pret = if numero == 1 then E.jalon(p, "tour2") elseif numero == 2 then E.jalon(p, "tour3") elseif numero == 3 then E.fleche_ouverte(p) else false
    if not pret or not E.operation(p, id) then return false end
    local r = runtime(p)
    r.attributions = {}; V.annuler(p); r.bloque_jusqua = horloge() + C.DEMENAGEMENT_S
    for _, c in comptes do if c.tour == p and c.profil ~= p then c.tour = c.profil; c.lieu = "tour" end end
    p.tours_finies += 1
    p.tour = {numero = numero + 1, rangees = 0, masque = 0, etincelante = false}
    return true
end
return V

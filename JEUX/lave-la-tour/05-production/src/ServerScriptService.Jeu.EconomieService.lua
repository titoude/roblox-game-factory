--!nocheck
local C = require(game:GetService("ReplicatedStorage").Jeu.Config)
local E = {}
local function trouver(liste, id)
    for _, element in liste do if element.id == id then return element end end
    return nil
end
function E.debloque(p, condition)
    if condition == "" then return true end
    local id, seuil = string.match(condition, "^(r%d+)>=([%d]+)$")
    return id ~= nil and p.robots[id] ~= nil and p.robots[id].en_service >= tonumber(seuil)
end
function E.jalon(p, id)
    local j = trouver(C.jalons, id)
    return j ~= nil and E.debloque(p, j.condition)
end
local function multiplicateur(p, cible)
    local m = 1
    for _, a in C.ameliorations do
        if p.ameliorations[a.id] and a.cible == cible then m *= a.multiplicateur end
    end
    return m
end
function E.revenu(p)
    local r = 0
    for _, g in C.generateurs do r += p.robots[g.id].en_service * g.revenu_s * multiplicateur(p, g.id) end
    return r * multiplicateur(p, "tout")
end
function E.gain_vitre(p)
    return multiplicateur(p, "action") * (C.action.gain * multiplicateur(p, "tout") + C.action.part_revenu_s * E.revenu(p))
end
function E.prix_robot(id, n)
    local g = trouver(C.generateurs, id)
    if not g or type(n) ~= "number" or n % 1 ~= 0 or n < 1 or n > g.max then return nil end
    -- Produit décimal exact, chiffres séparés : aucun ceil sur une puissance flottante.
    local croissance = tostring(g.croissance_cout)
    local decimales = #(string.match(croissance, "%.(%d+)$") or "")
    local facteur = tonumber((string.gsub(croissance, "%.", "")))
    local produit = string.format("%.0f", g.cout)
    for _ = 2, n do
        local retenue, chiffres = 0, ""
        for i = #produit, 1, -1 do
            local v = tonumber(string.sub(produit, i, i)) * facteur + retenue
            chiffres = tostring(v % 10) .. chiffres
            retenue = math.floor(v / 10)
        end
        produit = (if retenue > 0 then tostring(retenue) else "") .. chiffres
    end
    local places = decimales * (n - 1)
    produit = string.rep("0", math.max(0, places + 1 - #produit)) .. produit
    local entier = tonumber(string.sub(produit, 1, #produit - places))
    local reste = if places == 0 then 0 else tonumber(string.sub(produit, #produit - places + 1))
    return entier + (if reste > 0 then 1 else 0)
end
function E.crediter(p, montant)
    if type(montant) == "number" and montant == montant and montant > 0 then p.pieces = math.min(C.PLAFOND_SOLDE, p.pieces + montant) end
end
local function construire(p)
    for _, g in C.generateurs do
        local r = p.robots[g.id]
        for i = #r.chantiers, 1, -1 do
            if r.chantiers[i] <= p.temps_jeu then table.remove(r.chantiers, i); r.en_service += 1 end
        end
    end
end
function E.acheter_robot(p, id)
    local g = trouver(C.generateurs, id)
    if not g or not E.debloque(p, g.debloque) then return false, "achat_verrouille" end
    local r = p.robots[id]
    local prix = E.prix_robot(id, r.achetes + 1)
    if not prix or p.pieces < prix then return false, "achat_impossible" end
    p.pieces -= prix; r.achetes += 1
    table.insert(r.chantiers, p.temps_jeu + g.chantier_s * (if p.passes.chantiers_express then C.CHANTIERS_EXPRESS_TAUX else 1))
    construire(p)
    return true
end
function E.acheter_amelioration(p, id)
    local a = trouver(C.ameliorations, id)
    if not a or p.ameliorations[id] or not E.debloque(p, a.debloque) or p.pieces < a.cout then return false, "achat_impossible" end
    p.pieces -= a.cout; p.ameliorations[id] = true
    return true
end
function E.avancer(p, secondes)
    if type(secondes) ~= "number" or secondes ~= secondes or secondes < 0 or secondes == math.huge then return end
    local fin = p.temps_jeu + secondes
    construire(p)
    while p.temps_jeu < fin do
        local suivant = math.min(fin, p.temps_jeu + 1)
        for _, r in p.robots do
            for _, echeance in r.chantiers do if echeance > p.temps_jeu then suivant = math.min(suivant, echeance) end end
        end
        E.crediter(p, E.revenu(p) * (suivant - p.temps_jeu))
        p.temps_jeu = suivant
        construire(p)
    end
end
function E.hors_ligne(p, secondes)
    if type(secondes) ~= "number" or secondes ~= secondes or secondes < 0 or secondes == math.huge then return 0 end
    local gain = E.revenu(p) * C.HORS_LIGNE_TAUX * math.min(secondes, C.HORS_LIGNE_MAX_S)
    local avant = p.pieces
    E.crediter(p, gain)
    p.temps_jeu += secondes
    construire(p)
    return p.pieces - avant
end
function E.fleche_ouverte(p)
    for _, g in C.generateurs do if p.robots[g.id].en_service ~= g.max then return false end end
    for _, a in C.ameliorations do if not p.ameliorations[a.id] then return false end end
    return true
end
function E.prix_segment(n)
    if type(n) ~= "number" or n % 1 ~= 0 or n < 1 or n > 1e9 then return nil end
    return math.ceil(60 * math.min(C.FLECHE.MINUTES_BASE + n, C.FLECHE.MINUTES_MAX) * C.REVENU_FINAL)
end
function E.operation(p, id)
    if type(id) ~= "string" or #id == 0 or #id > 128 or table.find(p.operations, id) then return false end
    table.insert(p.operations, id)
    if #p.operations > C.OPERATIONS_MAX then table.remove(p.operations, 1) end
    return true
end
function E.acheter_segment(p, id)
    if not E.fleche_ouverte(p) or p.tour.numero ~= C.FLECHE.NUMERO_TOUR or p.fleche.segments_achetes - p.fleche.segments_laves >= C.FLECHE.NON_FINIS_MAX then return false end
    local prix = E.prix_segment(p.fleche.segments_achetes + 1)
    if p.pieces < prix or not E.operation(p, id) then return false end
    p.pieces -= prix; p.fleche.segments_achetes += 1
    p.tour.etincelante = false
    return true
end
function E.record(p) return C.FLECHE.ETAGE_DEBUT - 1 + C.FLECHE.ETAGES_SEGMENT * p.fleche.segments_laves end
function E.objectif(p)
    if p.tour.numero < C.FLECHE.NUMERO_TOUR then
        local pret = if p.tour.numero == 1 then E.jalon(p, "tour2") elseif p.tour.numero == 2 then E.jalon(p, "tour3") else E.fleche_ouverte(p)
        if pret then return {texte_cle = "objectif_demenager", cible = p.tour.numero + 1, reste = 0} end
    end
    -- Même politique de rendement que le simulateur, avec le rythme actif de référence.
    local meilleur, score = nil, math.huge
    local revenu = E.revenu(p) + E.gain_vitre(p) * C.action.par_minute / 60
    local function proposer(genre, id, prix, delta)
        if delta <= 0 then return end
        local note = math.max(0, prix - p.pieces) / revenu + prix / delta
        if note < score then score = note; meilleur = {texte_cle = "objectif_" .. genre, cible = id, reste = math.max(0, prix - p.pieces)} end
    end
    for _, g in C.generateurs do
        local prix = E.prix_robot(g.id, p.robots[g.id].achetes + 1)
        if prix and E.debloque(p, g.debloque) then
            proposer("robot", g.id, prix, g.revenu_s * multiplicateur(p, g.id) * multiplicateur(p, "tout") * (1 + C.action.part_revenu_s * multiplicateur(p, "action") * C.action.par_minute / 60))
        end
    end
    for _, a in C.ameliorations do
        if not p.ameliorations[a.id] and E.debloque(p, a.debloque) then
            local base = if a.cible == "tout" then revenu elseif a.cible == "action" then E.gain_vitre(p) * C.action.par_minute / 60 else p.robots[a.cible].en_service * trouver(C.generateurs, a.cible).revenu_s * multiplicateur(p, a.cible) * multiplicateur(p, "tout") * (1 + C.action.part_revenu_s * multiplicateur(p, "action") * C.action.par_minute / 60)
            proposer("amelioration", a.id, a.cout, base * (a.multiplicateur - 1))
        end
    end
    return meilleur or {texte_cle = if E.fleche_ouverte(p) then "objectif_segment" else "objectif_chantier", cible = p.fleche.segments_achetes + 1, reste = 0}
end
return E

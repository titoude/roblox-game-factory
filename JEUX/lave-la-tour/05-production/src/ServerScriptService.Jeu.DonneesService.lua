--!nocheck
local Etat = require(script.Parent.EtatJoueur)
local E = require(script.Parent.EconomieService)
local C = require(game:GetService("ReplicatedStorage").Jeu.Config)
local D = {}
local function copie(v)
    if type(v) ~= "table" then return v end
    local r = {}; for k, valeur in v do r[k] = copie(valeur) end; return r
end
local function json(v, pile)
    local t = type(v)
    if t == "number" then return v == v and math.abs(v) < math.huge end
    if t == "string" then return utf8.len(v) ~= nil end
    if t == "boolean" then return true end
    if t ~= "table" or pile[v] then return false end
    pile[v] = true
    local n, maximum, chaines = 0, 0, false
    for k, valeur in v do
        if type(k) == "number" and k >= 1 and k % 1 == 0 then n += 1; maximum = math.max(maximum, k)
        elseif type(k) == "string" and utf8.len(k) then chaines = true
        else return false end
        if not json(valeur, pile) then return false end
    end
    pile[v] = nil
    return maximum == n and not (chaines and n > 0)
end
local function identique(a, b)
    if type(a) ~= type(b) then return false end
    if type(a) ~= "table" then return a == b end
    for k, v in a do if not identique(v, b[k]) then return false end end
    for k in b do if a[k] == nil then return false end end
    return true
end
function D.valide(p) return json(p, {}) and identique(p, Etat.valider(p)) end
function D.nouveau(dependances)
    local d = dependances or {}
    local horloge, attendre = d.horloge or os.time, d.attendre or task.wait
    local lancer = d.lancer or task.spawn
    local run = d.RunService or game:GetService("RunService")
    local magasin = require(script.Parent.MagasinSur).ouvrir(d.DataStoreService or game:GetService("DataStoreService"), "LaveLaTourJoueurs_v1" .. (if run:IsStudio() then "_studio" else ""), run:IsStudio())
    local serveur = d.serveur or game.JobId
    -- JobId est vide dans une place locale ; le jeton distingue ces sessions.
    if serveur == "" then serveur = game:GetService("HttpService"):GenerateGUID(false) end
    local profils, occupes, marques, sessions, chargements = {}, {}, {}, {}, {}
    local ferme, echeance = false, nil
    local function expire() return echeance ~= nil and time() >= echeance end
    local function pause(secondes)
        if expire() then return false end
        attendre(if echeance then math.min(secondes, math.max(0, echeance - time())) else secondes)
        return not expire()
    end
    local service = {}
    local function ecrire(j, transformation)
        local valeur, accepte
        for essai = 1, 3 do
            if expire() then return nil end
            local ok = pcall(function() valeur = magasin:UpdateAsync("j_" .. j.UserId, function(ancien)
                local nouveau, ids = transformation(ancien)
                accepte = nouveau ~= nil
                return nouveau, ids
            end) end)
            if ok then return if accepte then valeur else nil end
            if essai < 3 and not pause(2^(essai-1)) then break end
        end
        return nil
    end
    function service.profil(j) return profils[j] end
    function service.marquer(j) if profils[j] then marques[j] = (marques[j] or 0) + 1 end end
    function service.a_ecrire(j) return marques[j] ~= nil end
    function service.charger(j)
        if ferme then return nil end
        if profils[j] then return profils[j] end
        while occupes[j.UserId] do if not pause(0.05) then return nil end end
        if ferme then return nil end
        if profils[j] then return profils[j] end
        occupes[j.UserId] = true; chargements[j] = true
        local session = serveur .. ":" .. game:GetService("HttpService"):GenerateGUID(false)
        local valeur
        for essai = 1, 6 do
            local maintenant = horloge()
            local verrouVivant = false
            valeur = ecrire(j, function(ancien)
                verrouVivant = false
                local verrou = type(ancien) == "table" and ancien.session
                if type(verrou) == "table" and verrou.id ~= session and type(verrou.instant) == "number" and maintenant - verrou.instant <= C.DONNEES.VERROU_S then verrouVivant = true; return nil end
                local brut = if type(ancien) == "table" and ancien.profil ~= nil then ancien.profil else ancien
                local migration = if brut == nil then Etat.nouveau() else Etat.migrer(brut)
                if not migration then return nil end
                local p = Etat.valider(migration)
                if not p then return nil end
                if p.depart > 0 then
                    local operation = "absence:" .. tostring(p.depart)
                    if E.operation(p, operation) then E.hors_ligne(p, math.max(0, maintenant - p.depart)) end
                    p.depart = 0
                end
                if not D.valide(p) then return nil end
                return {profil = p, session = {id = session, instant = maintenant}}, {j.UserId}
            end)
            if valeur or not verrouVivant then break end
            if essai < 6 and not pause(5) then break end
        end
        occupes[j.UserId] = nil; chargements[j] = nil
        if not valeur or not valeur.session or valeur.session.id ~= session then j:Kick("donnees_indisponibles"); return nil, "donnees_indisponibles" end
        profils[j] = valeur.profil; sessions[j] = session
        return profils[j]
    end
    function service.sauver(j, sortie)
        while occupes[j.UserId] do if not pause(0.05) then return false end end
        local p = profils[j]
        if not p or expire() then return false end
        if not D.valide(p) then warn("[Donnees] profil invalide, ecriture refusee : " .. j.UserId); return false end
        occupes[j.UserId] = true
        local session = sessions[j]
        local instant = horloge()
        local revision = marques[j]
        local photographie = copie(p)
        -- Le point de reprise périodique couvre aussi un arrêt brutal du serveur.
        photographie.depart = instant
        local perdu, valeur = false, nil
        for essai = 1, (if sortie then 3 else 1) do
            valeur = ecrire(j, function(ancien)
                perdu = false
                -- Une réponse perdue peut suivre une sortie déjà écrite et libérée.
                if sortie and type(ancien) == "table" and ancien.session == nil and identique(ancien.profil, photographie) then return ancien, {j.UserId} end
                if type(ancien) ~= "table" or type(ancien.session) ~= "table" or ancien.session.id ~= session then
                    perdu = true; return nil
                end
                return {profil = photographie, session = if sortie then nil else {id = session, instant = instant}}, {j.UserId}
            end)
            if valeur or perdu then break end
            if sortie and essai < 3 and not pause(2^(essai+1)) then break end
        end
        if sortie and not valeur and not perdu then
            -- Dernier recours : expirer le verrou sans remplacer le profil durable.
            -- Si le magasin reste indisponible, son horodatage n'est jamais prolongé.
            ecrire(j, function(ancien)
                if type(ancien) ~= "table" or type(ancien.session) ~= "table" or ancien.session.id ~= session then return nil end
                return {profil = ancien.profil, session = {id = session, instant = instant - C.DONNEES.VERROU_S - 1}}, {j.UserId}
            end)
        end
        occupes[j.UserId] = nil
        if valeur and marques[j] == revision then marques[j] = nil end
        if valeur and sortie then profils[j] = nil; marques[j] = nil; sessions[j] = nil end
        if perdu then
            profils[j] = nil; marques[j] = nil; sessions[j] = nil; j:Kick("donnees_indisponibles")
        elseif not valeur then
            service.marquer(j)
        end
        return valeur ~= nil
    end
    function service.fermer()
        ferme = true; echeance = time() + C.DONNEES.FERMETURE_S
        while next(chargements) do if not pause(0.05) then return false end end
        local joueurs={}
        for j in profils do table.insert(joueurs,j) end
        local restants,tout=#joueurs,true
        for _,j in joueurs do lancer(function()
            local ok, resultat = pcall(service.sauver,j,true)
            if not ok or not resultat then tout=false end
            restants-=1
        end) end
        while restants>0 do if not pause(0.05) then return false end end
        return tout
    end
    return service
end
return D

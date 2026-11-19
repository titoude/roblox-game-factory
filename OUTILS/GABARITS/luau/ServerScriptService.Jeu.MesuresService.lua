-- Compteurs uniquement ; les profils restent la responsabilité du jeu.
local MesuresService = {}
local champs = { "nouveaux", "actifs", "sessions", "minutes", "s_0_60", "s_61_180",
    "s_181_600", "s_601_1800", "s_1801_plus", "retours_j1", "retours_j7" }

function MesuresService.nouveau(config, dependances)
    local d = dependances or {}
    local horloge = d.horloge or os.time
    local attendre = d.attendre or task.wait
    local lancer = d.lancer or task.spawn
    local run = d.RunService or game:GetService("RunService")
    local donnees = d.DataStoreService or game:GetService("DataStoreService")
    local analytics = d.AnalyticsService
    if analytics == nil then
        pcall(function() analytics = game:GetService("AnalyticsService") end)
    end
    -- Jeton de serveur, jamais un identifiant de joueur. Injecté dans les tests.
    local jeton = d.jeton or game:GetService("HttpService"):GenerateGUID(false):gsub("%-", "")
    local recu = "_envoi_" .. jeton
    local magasin = donnees:GetDataStore(config.NOM_COURT .. "Mesures_v1" .. (run:IsStudio() and "_studio" or ""))
    local etapes = config.ETAPES_MESURES or { "arrivee", "premiere_action", "premier_achat", "min_3", "min_10" }
    local numeros = {}
    for i, nom in ipairs(etapes) do
        assert(i <= 100 and type(nom) == "string" and nom:match("^[a-z][a-z0-9_]*$") and #nom <= 40
            and not numeros[nom], "étape invalide")
        numeros[nom] = i
    end
    local attente, envois, sequences, sessions = {}, {}, {}, {}
    local occupe, demarre, ferme = false, false, false
    local service = {}
    local function jour(t) return os.date("!%Y-%m-%d", t) end
    local function ajouter(date, nom, n)
        if not attente[date] then
            attente[date] = {}
            for _, champ in ipairs(champs) do attente[date][champ] = 0 end
            for _, etape in ipairs(etapes) do attente[date]["e_" .. etape] = 0 end
        end
        attente[date][nom] = (attente[date][nom] or 0) + (n or 1)
    end
    local function actif(profil, t)
        local date = jour(t)
        if not profil.premier_jour then
            profil.premier_jour = date
            ajouter(date, "nouveaux")
        end
        if profil.dernier_jour_actif ~= date then
            profil.dernier_jour_actif = date
            ajouter(date, "actifs")
        end
        for _, n in ipairs({ 1, 7 }) do
            local champ = "retour_j" .. n .. "_compte"
            if not profil[champ] and profil.premier_jour == jour(t - n * 86400) then
                profil[champ] = true
                ajouter(date, "retours_j" .. n)
            end
        end
    end
    local function actualiser(session, t)
        -- Chaque jour traversé compte une activité, même sans reconnexion.
        local minuit = (math.floor(session.actualise / 86400) + 1) * 86400
        while minuit <= t do
            actif(session.profil, minuit)
            minuit += 86400
        end
        session.actualise = t
    end
    function service:joueur_arrive(joueur, profil)
        if sessions[joueur] then return end
        assert(type(profil) == "table", "Profil chargé requis")
        profil.etapes = profil.etapes or {}
        local t = horloge()
        actif(profil, t)
        sessions[joueur] = { debut = t, actualise = t, profil = profil }
    end
    function service:etape(joueur, profil, nom)
        assert(numeros[nom], "étape non configurée")
        assert(sessions[joueur] and sessions[joueur].profil == profil, "Session requise")
        actualiser(sessions[joueur], horloge())
        if profil.etapes[nom] then return false end
        profil.etapes[nom] = true
        ajouter(jour(horloge()), "e_" .. nom)
        if analytics then
            pcall(function() analytics:LogOnboardingFunnelStepEvent(joueur, numeros[nom], nom) end)
        end
        return true
    end
    function service:joueur_part(joueur, profil)
        local session = sessions[joueur]
        if not session then return end
        assert(session.profil == profil, "Profil différent")
        local t = horloge()
        actualiser(session, t)
        sessions[joueur] = nil
        local duree = math.max(0, math.floor(t - session.debut))
        local tranche = duree <= 60 and "s_0_60" or duree <= 180 and "s_61_180"
            or duree <= 600 and "s_181_600" or duree <= 1800 and "s_601_1800" or "s_1801_plus"
        ajouter(jour(t), "sessions")
        ajouter(jour(t), "minutes", math.floor(duree / 60 + 0.5))
        ajouter(jour(t), tranche)
    end
    function service:vider()
        if occupe then return false end
        occupe = true
        for _, session in pairs(sessions) do actualiser(session, horloge()) end
        for date, compteurs in pairs(attente) do
            if not envois[date] then
                sequences[date] = (sequences[date] or 0) + 1
                envois[date] = { numero = sequences[date], compteurs = compteurs }
                attente[date] = nil
            end
        end
        local tout = true
        for date, lot in pairs(envois) do
            local ok = false
            for tentative = 1, 3 do
                ok = pcall(function()
                    magasin:UpdateAsync("j_" .. date, function(ancien)
                        local valeur = table.clone(ancien or {})
                        if (valeur[recu] or 0) >= lot.numero then return valeur end
                        for nom, n in pairs(lot.compteurs) do valeur[nom] = (valeur[nom] or 0) + n end
                        valeur[recu] = lot.numero
                        return valeur
                    end)
                end)
                if ok then break end
                if tentative < 3 then attendre(2 ^ (tentative - 1)) end
            end
            if ok then envois[date] = nil else tout = false end
        end
        occupe = false
        return tout
    end
    function service:demarrer()
        assert(not demarre, "MesuresService déjà démarré")
        demarre = true
        local fermer = d.BindToClose or function(f) game:BindToClose(f) end
        fermer(function()
            ferme = true
            local joueurs = {}
            for joueur in pairs(sessions) do table.insert(joueurs, joueur) end
            for _, joueur in ipairs(joueurs) do self:joueur_part(joueur, sessions[joueur].profil) end
            -- Attendre l'envoi en cours avant l'envoi final.
            while occupe do attendre(0.1) end
            self:vider()
            self:vider() -- compteurs arrivés pendant une reprise précédente
        end)
        lancer(function()
            while not ferme do
                attendre(300)
                if not ferme then self:vider() end
            end
        end)
    end
    return service
end
return MesuresService

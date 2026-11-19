-- Exemples : boutique_ouverte, seconde_place_ouverte, contrat_ouvert, message_maintenance.
-- Défauts : { boutique_ouverte = { defaut = true }, vitesse = { defaut = 1, min = 0, max = 2 } }.
-- Le magasin contient une table plate { boutique_ouverte = false, version = 1, maj = 123 }.
local InterrupteursService = {}

function InterrupteursService.nouveau(config, dependances, valeurs_par_defaut)
    local d = dependances or {}
    local horloge = d.horloge or os.clock
    local attendre = d.attendre or task.wait
    local lancer = d.lancer or task.spawn
    local declarations, valeurs, rappels = {}, {}, {}
    for nom, regle in pairs(valeurs_par_defaut or {}) do
        declarations[nom] = table.clone(regle)
        valeurs[nom] = regle.defaut
    end
    local service = {}
    local demarre, dernier = false, -math.huge
    local function valide(v, r)
        if type(v) ~= type(r.defaut) then return false end
        if type(v) == "boolean" then return true end
        if type(v) == "number" then
            return v == v and type(r.min) == "number" and type(r.max) == "number"
                and v >= r.min and v <= r.max and math.abs(v) < math.huge
        end
        if type(v) == "string" then
            local n = utf8.len(v)
            return n ~= nil and n <= 200
        end
        return false
    end
    local function lire()
        -- Acquisition et lecture protégées : même une panne à l'ouverture garde les défauts.
        local ok, contenu = pcall(function()
            local run = d.RunService or game:GetService("RunService")
            local donnees = d.DataStoreService or game:GetService("DataStoreService")
            local nom = config.NOM_COURT .. "Reglages_v1" .. (run:IsStudio() and "_studio" or "")
            return donnees:GetDataStore(nom):GetAsync("interrupteurs")
        end)
        if not ok or type(contenu) ~= "table" then return end
        for nom, r in pairs(declarations) do
            local v = contenu[nom]
            if valide(v, r) and v ~= valeurs[nom] then
                local ancien = valeurs[nom]
                valeurs[nom] = v
                for _, rappel in ipairs(rappels[nom] or {}) do pcall(rappel, v, ancien) end
            end
        end
    end
    function service:valeur(nom) return valeurs[nom] end
    function service:actif(nom) return valeurs[nom] == true end
    function service:au_changement(nom, fonction)
        if not declarations[nom] or type(fonction) ~= "function" then return false end
        rappels[nom] = rappels[nom] or {}
        table.insert(rappels[nom], fonction)
        return true
    end
    function service:demarrer()
        if demarre then return end
        demarre = true
        dernier = horloge()
        lire()
        lancer(function()
            while true do
                attendre(60)
                local maintenant = horloge()
                if maintenant - dernier >= 60 then
                    dernier = maintenant
                    lire()
                end
            end
        end)
    end
    return service
end
return InterrupteursService

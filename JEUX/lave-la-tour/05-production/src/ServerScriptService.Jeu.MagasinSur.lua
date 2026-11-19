--!nocheck
-- Ouvre un DataStore sans faire tomber le serveur.
-- Place jamais publiée (Studio) : GetDataStore lève « You must publish this place to the web ».
-- En Studio seulement, on bascule alors sur un magasin en mémoire (rien n'est sauvegardé, et le
-- journal le dit) ; hors Studio, l'erreur remonte : jouer sans sauvegarde n'est jamais silencieux.
local MagasinSur = {}

local memoires = {}

local function copie(v)
    if type(v) ~= "table" then return v end
    local r = {}
    for k, valeur in v do r[k] = copie(valeur) end
    return r
end

function MagasinSur.memoire(nom)
    if memoires[nom] then return memoires[nom] end
    local valeurs = {}
    local m = {}
    function m:GetAsync(cle) return copie(valeurs[cle]) end
    function m:SetAsync(cle, valeur) valeurs[cle] = copie(valeur); return "v" end
    function m:RemoveAsync(cle) local ancien = valeurs[cle]; valeurs[cle] = nil; return ancien end
    function m:UpdateAsync(cle, transformation)
        local nouveau = transformation(copie(valeurs[cle]))
        if nouveau == nil then return nil end
        valeurs[cle] = copie(nouveau)
        return copie(nouveau)
    end
    function m:IncrementAsync(cle, delta)
        valeurs[cle] = (valeurs[cle] or 0) + (delta or 1)
        return valeurs[cle]
    end
    memoires[nom] = m
    return m
end

-- Rend (magasin, en_memoire).
function MagasinSur.ouvrir(service, nom, studio)
    local ok, magasin = pcall(function() return service:GetDataStore(nom) end)
    if ok and magasin then return magasin, false end
    if not studio then error(magasin, 2) end
    warn("[MagasinSur] " .. nom .. " : DataStore indisponible dans cette place (" .. tostring(magasin) .. ") ; magasin en mémoire, rien n'est sauvegardé.")
    return MagasinSur.memoire(nom), true
end

return MagasinSur

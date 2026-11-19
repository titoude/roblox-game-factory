-- Sondage facultatif, sans récompense ni lien avec votes/favoris (G6, G8).
-- Le jeu conserve et verrouille le profil ; moment = secondes de session côté serveur.
-- Config.VERSION_AVIS = entier partagé par les places ; défaut : game.PlaceVersion.
local AvisService = {}

function AvisService.nouveau(config, dependances)
    local d = dependances or {}
    local version = d.version or config.VERSION_AVIS or game.PlaceVersion
    assert(type(version) == "number" and version >= 0 and version % 1 == 0, "Version entière requise")
    assert(type(d.compter) == "function" and type(d.retour) == "function", "Rappels requis")
    local service = {}
    function service:proposer(_joueur, profil, moment)
        if type(moment) ~= "number" or moment ~= moment or moment < 180 then return false end
        if type(profil) ~= "table" then return false end
        if type(profil.avis) == "table" and profil.avis.version == version then return false end
        profil.avis = { version = version, repondu = false }
        return true
    end
    function service:repondre(joueur, profil, note, texte)
        if type(note) ~= "number" or note % 1 ~= 0 or note < 1 or note > 5 then return false end
        if texte == nil then texte = "" end
        if type(texte) ~= "string" or #texte > 2000 then return false end
        local longueur = utf8.len(texte)
        if not longueur or longueur > 500 then return false end
        if type(profil) ~= "table" or type(profil.avis) ~= "table"
            or profil.avis.version ~= version or profil.avis.repondu ~= false then return false end
        -- Réserver avant les rappels qui peuvent céder la main ; aucun doublon sur relance.
        profil.avis.repondu = true
        local compte = pcall(d.compter, "avis_" .. tostring(note))
        local transmis = true
        if texte:find("%S") then transmis = pcall(d.retour, joueur, "avis", texte) end
        -- Une panne de rappel consomme la réponse : pas de garantie de livraison durable ici.
        return compte and transmis
    end
    return service
end
return AvisService

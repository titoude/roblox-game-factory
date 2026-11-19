-- Le texte joueur reste une donnée ; aucun affichage à d'autres joueurs.
local RetoursService = {}

function RetoursService.nouveau(config, dependances)
    local d = dependances or {}
    local horloge = d.horloge or os.time
    local attendre = d.attendre or task.wait
    local donnees = d.DataStoreService or game:GetService("DataStoreService")
    local http = d.HttpService or game:GetService("HttpService")
    local studio = d.studio
    if studio == nil then
        studio = game:GetService("RunService"):IsStudio()
    end
    local version = d.version or game.PlaceVersion
    local magasin = donnees:GetDataStore(config.NOM_COURT .. "Retours_v1" .. (studio and "_studio" or ""))
    local compteurs = {}
    local service = {}

    function service.envoyer(player, categorie, texte)
        local francais = string.sub(string.lower(player.LocaleId), 1, 2) == "fr"
        local function message(fr, en)
            return false, francais and fr or en
        end
        if type(texte) ~= "string" or #texte > 2000 then
            return message("Texte invalide.", "Invalid text.")
        end
        local longueur = utf8.len(texte)
        if not longueur or longueur < 5 or longueur > 500 or not string.find(texte, "%S") then
            return message("Merci d'écrire entre 5 et 500 caractères.", "Please write 5 to 500 characters.")
        end
        if categorie ~= "idee" and categorie ~= "bug" and categorie ~= "autre" then
            return message("Choisis une catégorie.", "Please choose a category.")
        end
        local maintenant = horloge()
        local jour = math.floor(maintenant / 86400)
        local compteur = compteurs[player.UserId]
        if not compteur then
            compteur = { dernier = -math.huge, jour = jour, nombre = 0, occupe = false }
            compteurs[player.UserId] = compteur
        end
        if compteur.occupe or maintenant - compteur.dernier < 60 then
            return message("Merci de patienter 60 secondes.", "Please wait 60 seconds.")
        end
        if compteur.jour ~= jour then
            compteur.jour, compteur.nombre = jour, 0
        end
        if compteur.nombre >= 5 then
            return message("Merci ! Reviens demain (5 retours par jour).", "Thank you! Come back tomorrow (5 reports a day).")
        end
        -- Réserver avant les appels qui cèdent la main ; les échecs comptent aussi.
        compteur.occupe, compteur.dernier = true, maintenant
        compteur.nombre += 1
        -- Réservation atomique partagée entre serveurs ; q_ est ignoré par l'usine.
        local autorise, refus = false, "cadence"
        local quotaOk = false
        for tentative = 1, 3 do
            quotaOk = pcall(function()
                magasin:UpdateAsync("q_" .. tostring(player.UserId), function(ancien)
                    autorise = false
                    local quota = ancien or { jour = jour, dernier = -math.huge, nombre = 0 }
                    if maintenant - quota.dernier < 60 then
                        refus = "cadence"
                        return nil
                    end
                    if quota.jour ~= jour then
                        quota = { jour = jour, dernier = quota.dernier, nombre = 0 }
                    end
                    if quota.nombre >= 5 then
                        refus = "jour"
                        return nil
                    end
                    autorise = true
                    return { jour = jour, dernier = maintenant, nombre = quota.nombre + 1 }, { player.UserId }
                end)
            end)
            if quotaOk then break end
            if tentative < 3 then attendre(tentative) end
        end
        if not quotaOk or not autorise then
            compteur.occupe = false
            if not quotaOk then
                return message("Service indisponible. Merci de réessayer plus tard.", "Service unavailable. Please try again later.")
            elseif refus == "jour" then
                return message("Merci ! Reviens demain (5 retours par jour).", "Thank you! Come back tomorrow (5 reports a day).")
            end
            return message("Merci de patienter 60 secondes.", "Please wait 60 seconds.")
        end
        local cle = "r_" .. tostring(maintenant) .. "_" .. tostring(player.UserId)
        local succes = false
        for tentative = 1, 3 do
            succes = pcall(function()
                local valeur = http:JSONEncode({ t = maintenant, userId = player.UserId,
                    lang = player.LocaleId, version = version, categorie = categorie, texte = texte })
                magasin:SetAsync(cle, valeur, { player.UserId })
            end)
            if succes then
                break
            end
            if tentative < 3 then
                attendre(tentative)
            end
        end
        compteur.occupe = false
        if not succes then
            return message("Service indisponible. Merci de réessayer plus tard.", "Service unavailable. Please try again later.")
        end
        return true, francais and "Reçu, merci !" or "Received, thank you!"
    end

    function service.demarrer()
        local stockage = game:GetService("ReplicatedStorage")
        assert(not stockage:FindFirstChild("RetoursJoueurs"), "RetoursService déjà démarré")
        local remote = Instance.new("RemoteEvent")
        remote.Name = "RetoursJoueurs"
        remote.Parent = stockage
        remote.OnServerEvent:Connect(function(player, categorie, texte)
            -- Les refus en rafale ne produisent pas de réponses réseau en rafale.
            local compteur = compteurs[player.UserId]
            if compteur and compteur.reponse and horloge() - compteur.reponse < 1 then
                return
            end
            local ok, raison = service.envoyer(player, categorie, texte)
            if not compteurs[player.UserId] then
                compteurs[player.UserId] = { dernier = -math.huge, jour = 0, nombre = 0, occupe = false }
            end
            compteurs[player.UserId].reponse = horloge()
            if player.Parent then
                remote:FireClient(player, ok, raison)
            end
        end)
        return remote
    end

    return service
end

return RetoursService

--!nocheck
local Config = require(game:GetService("ReplicatedStorage").Jeu.Config)
local Commerce = {}
function Commerce.nouveau(d)
    d = d or {}
    local config, marche = d.Config or Config, d.MarketplaceService or game:GetService("MarketplaceService")
    local horloge = d.horloge or time
    local comptes, prochains = {}, {}
    local service = {}
    local function actif(id) return type(id)=="number" and id>0 and id%1==0 and id<math.huge end
    function service.offres()
        local offres = {}
        for nom,id in config.OFFRES do if actif(id) then offres[nom]=id end end
        return offres
    end
    function service.relire(j)
        local p=comptes[j];if not p then return end
        local passes = {}
        for nom,id in config.OFFRES do
            if actif(id) then
                local ok,possede=pcall(function() return marche:UserOwnsGamePassAsync(j.UserId,id) end)
                passes[nom]=ok and possede==true
            end
        end
        p.passes=passes
    end
    function service.inscrire(j,p) comptes[j]=p;prochains[j]=horloge()+config.MOTORISEE_INTERVALLE_S;service.relire(j) end
    function service.quitter(j) comptes[j]=nil;prochains[j]=nil end
    function service.avancer(j,assis,finir)
        local p=comptes[j];if not p then return false end
        if not assis or not p.passes.raclette_motorisee then prochains[j]=horloge()+config.MOTORISEE_INTERVALLE_S;return false end
        if horloge()<(prochains[j] or math.huge) then return false end
        prochains[j]=horloge()+config.MOTORISEE_INTERVALLE_S
        return finir(j)
    end
    function service.demarrer()
        if next(service.offres()) then marche.PromptGamePassPurchaseFinished:Connect(function(j,id)
            for _,connu in config.OFFRES do if actif(connu) and id==connu then service.relire(j);break end end
        end) end
        -- Aucun produit consommable en v1 ; aucun recu inconnu n'est acquitte.
        marche.ProcessReceipt=function() return Enum.ProductPurchaseDecision.NotProcessedYet end
    end
    return service
end
return Commerce

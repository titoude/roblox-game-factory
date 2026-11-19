--!nocheck
local V = require(script.Parent.VitresService)
local E = require(script.Parent.EconomieService)
local C = require(game:GetService("ReplicatedStorage").Jeu.Config)
local S = {}
function S.nouveau(d)
    d = d or {}
    local horloge, date = d.horloge or time, d.date or os.time
    local amis = d.amis or function(a,b) local ok,v = pcall(function() return a:IsFriendsWith(b.UserId) end); return ok and v end
    local comptes, ordre, dernier = {}, 0, {}
    local service = {}
    if not d.borne then d.borne = function(j,cible)
        local personnage = j.Character
        local racine = personnage and personnage:FindFirstChild("HumanoidRootPart")
        local monde = game:GetService("Workspace"):FindFirstChild("MondeLaveLaTour")
        if not racine or not monde then return false end
        for _,parcelle in monde:GetChildren() do
            if parcelle:GetAttribute("Proprietaire")==cible.UserId then
                local tour=parcelle:FindFirstChild("Tour")
                local borne=tour and tour:FindFirstChild("Borne")
                return borne ~= nil and (racine.Position-borne.Position).Magnitude<=C.RAYON_BORNE
            end
        end
        return false
    end end
    local function quotas(p)
        local jour = os.date("!%Y-%m-%d", date())
        if p.quotas.jour ~= jour then p.quotas = {jour=jour,mousse_s=0,mousse_par={},pourboires_min=0,pourboires_par={}} end
        return p.quotas
    end
    local function duo(j)
        local tour,lieu = V.position(j)
        if lieu ~= "tour" then return nil end
        for autre in comptes do
            if autre ~= j then local t,l = V.position(autre); if t == tour and l == "tour" then return autre end end
        end
        return nil
    end
    -- Consommer le temps effectif avant tout changement de partenaire ou de jour.
    function service.actualiser()
        local maintenant = horloge()
        for j,c in comptes do
            local partenaire = duo(j)
            if c.partenaire and c.depuis then
                local fin = math.min(maintenant,c.fin or c.depuis)
                -- Un changement UTC partage l'intervalle avant et apres minuit.
                local debut = c.depuis
                while debut < fin do
                    local unix = date() - (maintenant-debut)
                    local borne = math.min(fin, debut + ((math.floor(unix/86400)+1)*86400-unix))
                    local jour = os.date("!%Y-%m-%d", unix)
                    if c.profil.quotas.jour ~= jour then c.profil.quotas={jour=jour,mousse_s=0,mousse_par={},pourboires_min=0,pourboires_par={}} end
                    local q,k = c.profil.quotas,tostring(c.partenaire.UserId)
                    local n = math.max(0,math.min(borne-debut,C.MOUSSE_QUOTA_S-q.mousse_s,C.MOUSSE_PARTENAIRE_S-(q.mousse_par[k] or 0)))
                    q.mousse_s += n; q.mousse_par[k]=(q.mousse_par[k] or 0)+n
                    debut = borne
                end
            end
            quotas(c.profil)
            c.depuis = maintenant
            if partenaire ~= c.partenaire then c.fin=nil; dernier[j]=nil end
            c.partenaire = partenaire
        end
    end
    function service.inscrire(j,p) ordre+=1; comptes[j]={profil=p,ordre=ordre}; quotas(p) end
    function service.profil(j) return comptes[j] and comptes[j].profil end
    function service.etat(j)
        service.actualiser()
        local c=comptes[j]
        if not c then return false,"" end
        local mousse = c.partenaire ~= nil and c.fin ~= nil and horloge()<c.fin
        local q,k=c.profil.quotas,tostring(c.partenaire and c.partenaire.UserId)
        return mousse, if mousse and (q.mousse_s>=C.MOUSSE_QUOTA_S or (q.mousse_par[k] or 0)>=C.MOUSSE_PARTENAIRE_S) then "mousse_quota_atteint" else ""
    end
    local function libre(cible)
        local c=comptes[cible]
        if not c then return false end
        local t,l=V.position(cible)
        return t==c.profil and l=="tour" and duo(cible)==nil
    end
    function service.rejoignable(j,cible)
        local c,a=comptes[j],comptes[cible]
        local t,l=V.position(j)
        return c and a and j~=cible and c.ordre>a.ordre and c.profil.tour.rangees>=1 and t==c.profil and l=="tour" and libre(cible) and amis(j,cible)
    end
    function service.contexte(j)
        local autre=duo(j)
        local tour=V.position(j)
        if autre and V.stock(tour)==0 then
            local visiteur=if tour==comptes[j].profil then autre else j
            if V.stock(comptes[visiteur].profil)>0 then return "chez_visiteur",nil,visiteur.Name end
        end
        local choix
        for cible,c in comptes do
            if service.rejoignable(j,cible) and (not choix or c.ordre<comptes[choix].ordre) then choix=cible end
        end
        if choix then return "rejoindre",choix.UserId,choix.Name end
        return "",nil,""
    end
    function service.action(j,nom,cible)
        service.actualiser()
        local c=comptes[j];if not c then return false end
        if nom=="rejoindre" then
            if not service.rejoignable(j,cible) then return false end
            V.asseoir(j,comptes[cible].profil,"tour")
        elseif nom=="monter" and cible then
            local _,lieu=V.position(j)
            -- La borne doit etre attestee par le monde serveur, jamais par le Remote.
            if lieu~="place" or not libre(cible) or not d.borne or not d.borne(j,cible) then return false end
            V.asseoir(j,comptes[cible].profil,"tour")
        elseif nom=="chez_visiteur" then
            local autre=duo(j);if not autre then return false end
            local tour=V.position(j)
            local proprietaire,visiteur
            if tour==c.profil then proprietaire=j;visiteur=autre else proprietaire=autre;visiteur=j end
            if not comptes[proprietaire] or not comptes[visiteur] or V.stock(tour)>0 or V.stock(comptes[visiteur].profil)<=0 then return false end
            for x in comptes do
                if x~=visiteur and x~=proprietaire and V.position(x)==comptes[visiteur].profil then return false end
            end
            V.asseoir(proprietaire,comptes[visiteur].profil,"tour");V.asseoir(visiteur,comptes[visiteur].profil,"tour")
        elseif nom=="retour" or nom=="descendre" or (nom=="monter" and not cible) then
            if not V.asseoir(j,c.profil,if nom=="descendre" then "place" else "tour") then return false end
        else return false end
        service.actualiser()
        local t=V.position(j);V.attribuer(t,j)
        return true
    end
    function service.detacher(j)
        service.actualiser()
        local p=comptes[j] and comptes[j].profil
        for autre,c in comptes do if autre~=j and V.position(autre)==p then V.asseoir(autre,c.profil,"tour");V.attribuer(c.profil,autre) end end
        V.liberer(j);service.actualiser()
    end
    function service.quitter(j) service.detacher(j);comptes[j]=nil;dernier[j]=nil end
    function service.finie(j,gain)
        service.actualiser()
        local c=comptes[j];if not c then return end
        local autre=duo(j);dernier[j]=horloge()
        if autre and dernier[autre] and horloge()-dernier[autre]<C.MOUSSE_FENETRE_S then
            c.fin=horloge()+C.MOUSSE_FENETRE_S;comptes[autre].fin=horloge()+C.MOUSSE_FENETRE_S
        end
        local mousse,message=service.etat(j)
        if mousse and message=="" then E.crediter(c.profil,gain*(C.MOUSSE_MULTIPLICATEUR-1)) end
        local tour=V.position(j)
        if autre and tour~=c.profil and tour==comptes[autre].profil then
            local p=comptes[autre].profil
            local q,k=quotas(p),tostring(j.UserId)
            local R=math.max(C.POURBOIRE_REVENU_MIN,E.revenu(p))
            local minutes=math.max(0,math.min(E.gain_vitre(p)*C.POURBOIRE_TAUX/(60*R),C.POURBOIRE_QUOTA_MIN-q.pourboires_min,C.POURBOIRE_PARTENAIRE_MIN-(q.pourboires_par[k] or 0)))
            E.crediter(p,minutes*60*R);q.pourboires_min+=minutes;q.pourboires_par[k]=(q.pourboires_par[k] or 0)+minutes
        end
    end
    return service
end
return S

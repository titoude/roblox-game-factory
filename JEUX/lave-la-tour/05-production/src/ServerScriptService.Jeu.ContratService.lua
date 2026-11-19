--!nocheck
local E = require(script.Parent.EconomieService)
local V = require(script.Parent.VitresService)
local Config = require(game:GetService("ReplicatedStorage").Jeu.Config)
local C = {}
function C.nouveau(d)
    d = d or {}
    local horloge, date = d.horloge or time, d.date or os.time
    local attributions = {}
    local service = {}
    local function jour() return os.date("!%Y-%m-%d",date()) end
    function service.ouvrir(j,p)
        if not E.jalon(p,"contrats") or (p.contrat.prime_recue and p.contrat.jour==jour()) then return false end
        if p.contrat.prime_recue then p.contrat={jour="",vitres=0,masque=0,prime_recue=false} end
        if d.detacher then d.detacher(j) end
        V.asseoir(j,p,"contrat");V.annuler(p);attributions[j]=nil
        service.attribuer(j,p)
        return true
    end
    function service.attribuer(j,p)
        local _,lieu=V.position(j)
        if lieu~="contrat" or p.contrat.vitres>=Config.CONTRAT_VITRES or p.contrat.prime_recue then return nil end
        if not attributions[j] then
            for i=1,Config.VITRES_PAR_RANGEE do
                if bit32.band(p.contrat.masque,2^(i-1))==0 then
                    attributions[j]={rangee=math.floor(p.contrat.vitres/Config.VITRES_PAR_RANGEE)+1,index=i,debut=horloge()};break
                end
            end
        end
        local a=attributions[j];return a.rangee,a.index
    end
    function service.attribution(j) local a=attributions[j];return if a then {rangee=a.rangee,index=a.index} else nil end
    function service.quitter(j) attributions[j]=nil end
    function service.finir(j,p,rangee,index)
        local _,lieu=V.position(j)
        local a=attributions[j]
        if lieu~="contrat" or not a or type(rangee)~="number" or type(index)~="number" or a.rangee~=rangee or a.index~=index or horloge()-a.debut<Config.VITRE_DUREE_MIN_S then return false end
        if p.contrat.prime_recue or p.contrat.vitres>=Config.CONTRAT_VITRES or bit32.band(p.contrat.masque,2^(index-1))~=0 then return false end
        if not V.consommer_budget(j,horloge()) then return false end
        E.crediter(p,E.gain_vitre(p));p.contrat.vitres+=1
        p.contrat.masque=bit32.bor(p.contrat.masque,2^(index-1));if p.contrat.masque==2^Config.VITRES_PAR_RANGEE-1 then p.contrat.masque=0 end
        attributions[j]=nil
        if p.contrat.vitres==Config.CONTRAT_VITRES then
            if E.operation(p,"contrat:"..jour()) then E.crediter(p,Config.CONTRAT_PRIME_S*E.revenu(p)) end
            p.contrat.jour=jour();p.contrat.prime_recue=true
        else service.attribuer(j,p) end
        return true
    end
    return service
end
return C

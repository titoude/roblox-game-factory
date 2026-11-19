local DSS=game:GetService("DataStoreService")
local get=DSS.GetDataStore
local enveloppes={}
local panne=false
DSS.GetDataStore=function(self,...)
    local ds=get(self,...)
    if not enveloppes[ds] then
        enveloppes[ds]=true
        local update=ds.UpdateAsync
        ds.UpdateAsync=function(magasin,...)
            if panne then task.wait(2);error("panne de tous les magasins") end
            return update(magasin,...)
        end
    end
    return ds
end
banc.demarrer_serveur()
local j=banc.joueur(8300,"FermetureEnPanne")
banc.avancer(61)
panne=true
local debut=time()
banc.fermer_serveur()
banc.verifier(time()-debut<30,"fermeture profils et mesures en panne bornee avant 30 secondes")

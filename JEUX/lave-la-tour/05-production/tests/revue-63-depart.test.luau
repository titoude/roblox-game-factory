local ds=game:GetService("DataStoreService"):GetDataStore("LaveLaTourJoueurs_v1_studio")
local store=banc.datastore("LaveLaTourJoueurs_v1_studio")
local update=ds.UpdateAsync
ds.UpdateAsync=function(self,k,f) task.wait(0.3);return update(self,k,f) end
banc.demarrer_serveur()
local j=banc.joueur(8200,"DepartPendantChargement")
banc.avancer(0.1);banc.quitter(j);banc.avancer(2)
local T=banc.require("ServerScriptService.Jeu.ActionsDeTest")
banc.egal(T.profil(j),nil,"depart pendant chargement sans profil fantome")
banc.egal(store:lire("j_8200").session,nil,"depart pendant chargement rend le verrou")

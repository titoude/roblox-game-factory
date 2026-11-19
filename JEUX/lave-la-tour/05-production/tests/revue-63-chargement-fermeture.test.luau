local ds=game:GetService("DataStoreService"):GetDataStore("LaveLaTourJoueurs_v1_studio")
local store=banc.datastore("LaveLaTourJoueurs_v1_studio")
local update=ds.UpdateAsync
ds.UpdateAsync=function(self,k,f) task.wait(0.3);return update(self,k,f) end
banc.demarrer_serveur()
local j=banc.joueur(8250,"FermeturePendantChargement")
banc.avancer(0.1);banc.fermer_serveur();banc.avancer(1)
local T=banc.require("ServerScriptService.Jeu.ActionsDeTest")
banc.egal(T.profil(j),nil,"fermeture pendant chargement sans profil expose")
banc.egal(store:lire("j_8250").session,nil,"fermeture attend le chargement et rend son verrou")

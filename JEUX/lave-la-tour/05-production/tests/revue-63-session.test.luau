local D=banc.require("ServerScriptService.Jeu.DonneesService")
local ds=game:GetService("DataStoreService"):GetDataStore("LaveLaTourJoueurs_v1_studio")
local store=banc.datastore("LaveLaTourJoueurs_v1_studio")
local s=D.nouveau({serveur="meme-serveur"})
local function joueur() return {UserId=8100,Kick=function(self,v) self.kick=v end} end
local ancien,nouveau=joueur(),joueur()
s.charger(ancien).pieces=42
local update=ds.UpdateAsync
local suspendu=false
ds.UpdateAsync=function(self,k,f)
    if suspendu then local pause=suspendu;suspendu=0.1;task.wait(pause) end
    return update(self,k,f)
end
suspendu=0.6
local fini=false
task.spawn(function() banc.verifier(s.sauver(ancien,true),"ancienne sortie terminee");fini=true end)
banc.avancer(0.1)
local profil
task.spawn(function() profil=s.charger(nouveau) end)
banc.avancer(6)
banc.verifier(fini and profil~=nil,"retour attend la sortie precedente")
banc.egal(profil.pieces,42,"retour sur meme serveur conserve le dernier gain")
banc.egal(s.profil(ancien),nil,"ancienne session retiree")
suspendu=false
profil.pieces=51
banc.verifier(s.sauver(nouveau,true),"nouvelle session garde son verrou")
banc.egal(store:lire("j_8100").profil.pieces,51,"nouvelle sortie durable")

-- Deux instances de service avec le même JobId ne partagent pas une session de joueur.
local autreService=D.nouveau({serveur="meme-serveur",attendre=function() end})
local x={UserId=8101,Kick=function(self,v) self.kick=v end}
local y={UserId=8101,Kick=x.Kick}
s.charger(x)
banc.egal(autreService.charger(y),nil,"jeton distinct meme avec un JobId identique")
banc.egal(y.kick,"donnees_indisponibles","session active jamais volee")
banc.verifier(s.sauver(x,true),"titulaire initial conserve son verrou")

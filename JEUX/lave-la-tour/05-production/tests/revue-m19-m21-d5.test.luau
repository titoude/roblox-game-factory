local S=banc.require("ServerScriptService.Jeu.EtatJoueur")
local E=banc.require("ServerScriptService.Jeu.EconomieService")
local D=banc.require("ServerScriptService.Jeu.DonneesService")
local ds=game:GetService("DataStoreService"):GetDataStore("LaveLaTourJoueurs_v1_studio")
local store=banc.datastore("LaveLaTourJoueurs_v1_studio")
local s=D.nouveau({attendre=function() end})
local p=S.nouveau();p.pieces=42;p.depart=os.time()-100
p.robots.r1={achetes=1,en_service=1,chantiers={}}
p.operations={"absence:"..p.depart}
ds:SetAsync("j_8500",{profil=p})
local appels=0
local horsLigne=E.hors_ligne
E.hors_ligne=function(...) appels+=1;return horsLigne(...) end
local j={UserId=8500,Kick=function(self,v) self.kick=v end}
local q=s.charger(j)
banc.egal(appels,0,"M19 intervalle deja consomme non rejoue")
banc.egal(q.pieces,42,"M19 credit deja accorde intact")
banc.egal(q.depart,0,"M19 depart consomme meme sans nouveau credit")
E.hors_ligne=horsLigne
local durable=game:GetService("HttpService"):JSONEncode(store:lire("j_8500"))
for _,valeur in {0/0,math.huge,9e15+1} do
    q.pieces=valeur
    local avant=store:compteurs().total
    banc.verifier(not s.sauver(j),"M21 profil invalide refuse")
    banc.egal(store:compteurs().total,avant,"M21 refus avant toute requete et consommation de budget")
    banc.egal(game:GetService("HttpService"):JSONEncode(store:lire("j_8500")),durable,"M21 magasin inchange")
end
banc.egal(#banc.avertissements(),3,"M21 refus journalises")
q.pieces=42
banc.verifier(s.sauver(j,true),"profil repare sauvegardable")
local mauvais=S.nouveau()
mauvais.tour=setmetatable({},{__index=function() error("validation-injectee") end})
local valide,raison=S.valider(mauvais)
banc.egal(valide,nil,"D5 erreur interne ne devient jamais un profil neuf")
banc.egal(raison,"profil_invalide","D5 raison distinguee d'un nouveau compte")

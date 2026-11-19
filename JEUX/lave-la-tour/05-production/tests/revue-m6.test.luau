local E=banc.require("ServerScriptService.Jeu.EconomieService")
local appels=0
local acheter=E.acheter_robot
E.acheter_robot=function(...) appels+=1;return acheter(...) end
banc.demarrer_serveur()
local j=banc.joueur(8400,"TypesAchat")
local r=game:GetService("ReplicatedStorage").JeuRemotes.Acheter
local client=banc.client(j)
for _,id in {false,12,{},string.rep("x",33)} do client:envoyer(r,"robot",id) end
banc.egal(appels,0,"M6 arguments invalides arretes avant le service economique")
client:envoyer(r,"robot","r1")
banc.egal(appels,1,"M6 argument valide transmis au meme service")

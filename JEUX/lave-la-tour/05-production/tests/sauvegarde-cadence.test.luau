-- S1/S2 : le DataStore lent ne fait pas attendre les actions.
local ds=game:GetService("DataStoreService"):GetDataStore("LaveLaTourJoueurs_v1_studio")
local update=ds.UpdateAsync
local ecritures,lent=0,false
local parCle={}
ds.UpdateAsync=function(self,cle,f)
    ecritures+=1
    parCle[cle]=(parCle[cle] or 0)+1
    if lent then task.wait(0.3) end
    return update(self,cle,f)
end
banc.demarrer_serveur()
local a,b=banc.joueur(7001,"CadenceA"),banc.joueur(7002,"CadenceB")
local T=banc.require("ServerScriptService.Jeu.ActionsDeTest")
local V=banc.require("ServerScriptService.Jeu.VitresService")
local r=game:GetService("ReplicatedStorage").JeuRemotes.VitreFinie
local store=banc.datastore("LaveLaTourJoueurs_v1_studio")
local pa,pb=T.profil(a),T.profil(b)
local ra,ia=V.attribuer(pa,a)
local rb,ib=V.attribuer(pb,b)
banc.avancer(1.5)
lent=true
r.OnServerEvent:Fire(a,ra,ia)
r.OnServerEvent:Fire(b,rb,ib)
banc.avancer(0.01)
banc.egal(pa.pieces,1,"S1 A crédité immédiatement")
banc.egal(pb.pieces,1,"S1 B crédité dans la même image")
banc.egal(store:lire("j_7001").profil.pieces,0,"S2 mémoire avant sauvegarde")
for n=2,40 do
    local rangee,index=V.attribuer(pa,a)
    banc.avancer(1.5)
    r.OnServerEvent:Fire(a,rangee,index)
    banc.avancer(0.001)
end
banc.egal(pa.pieces,40,"S2 quarante vitres créditées en mémoire")
banc.avancer(1)
banc.egal(ecritures,4,"S2 deux chargements et au plus une sauvegarde par joueur")
banc.egal(parCle.j_7001,2,"S2 au plus deux appels pour quarante vitres, chargement compris")
banc.egal(store:lire("j_7001").profil.pieces,39,"S2 photographie avant la dernière vitre concurrente")
banc.avancer(60)
banc.egal(store:lire("j_7001").profil.pieces,40,"S2 mutation pendant écriture conservée au cycle suivant")
pa.pieces+=7
banc.quitter(a)
banc.avancer(1)
banc.egal(store:lire("j_7001").profil.pieces,47,"S2 sortie écrit le dernier état")
banc.egal(store:lire("j_7001").session,nil,"S2 sortie libère le verrou")

-- S3 : le raccordement reel retente au prochain cycle de 60 secondes.
local rangee,index=V.attribuer(pb,b)
r.OnServerEvent:Fire(b,rangee,index)
banc.avancer(0.01)
banc.egal(pb.pieces,2,"S3 nouvelle vitre en memoire")
store:pannes(3)
banc.avancer(60)
banc.egal(T.profil(b),pb,"S3 panne periodique conserve le profil en jeu")
banc.egal(store:lire("j_7002").profil.pieces,1,"S3 panne non confirmee")
banc.avancer(60)
banc.egal(store:lire("j_7002").profil.pieces,2,"S3 cycle suivant ecrit la progression")

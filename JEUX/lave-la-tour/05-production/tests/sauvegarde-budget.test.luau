banc.configurer_datastore({latence_s=0.3,limites=true})
banc.demarrer_serveur()
local joueurs={}
for i=1,6 do joueurs[i]=banc.joueur(9000+i,"Laveur"..i) end
local T=banc.require("ServerScriptService.Jeu.ActionsDeTest")
local V=banc.require("ServerScriptService.Jeu.VitresService")
local r=game:GetService("ReplicatedStorage").JeuRemotes.VitreFinie
local store=banc.datastore("LaveLaTourJoueurs_v1_studio")
banc.egal(T.profil(joueurs[1]),nil,"chargement reellement suspendu")
banc.avancer(0.31)
for n=1,40 do
    banc.avancer(1.5)
    for _,j in joueurs do
        local p=T.profil(j)
        local rangee,index=V.attribuer(p,j)
        r.OnServerEvent:Fire(j,rangee,index)
    end
    banc.avancer(0)
    for _,j in joueurs do banc.egal(T.profil(j).pieces,n,"S1 six laveurs dans la meme image "..n) end
end
banc.avancer(0.4)
local c=store:compteurs()
banc.egal(c.total,12,"S2 six chargements et six sauvegardes pour 240 vitres")
banc.egal(c.refus_cle,0,"S2 aucune limite par cle atteinte")
banc.egal(c.refus_budget,0,"S2 aucun budget serveur depasse")
banc.avancer(60)
for _,j in joueurs do banc.egal(store:lire("j_"..j.UserId).profil.pieces,40,"toutes les vitres persistantes au cycle suivant") end
local parCle={}
for _,appel in store:historique() do
    local avant=parCle[appel.cle]
    if avant then banc.verifier(appel.temps-avant>=6,"espacement reel des ecritures") end
    parCle[appel.cle]=appel.temps
end
banc.fermer_serveur()
for _,j in joueurs do banc.egal(store:lire("j_"..j.UserId).session,nil,"fermeture parallele libere les six cles") end

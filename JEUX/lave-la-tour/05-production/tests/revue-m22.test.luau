-- M22 historique a disparu avec S1 : le contrat actuel est le marquage sans ecriture.
local D=banc.require("ServerScriptService.Jeu.DonneesService")
local nouveau=D.nouveau
local service
D.nouveau=function(...)
    service=nouveau(...)
    return service
end
banc.demarrer_serveur()
local j=banc.joueur(8600,"ConfirmationMemoire")
local T=banc.require("ServerScriptService.Jeu.ActionsDeTest")
local V=banc.require("ServerScriptService.Jeu.VitresService")
local store=banc.datastore("LaveLaTourJoueurs_v1_studio")
local p=T.profil(j)
banc.avancer(1.5)
banc.verifier(service.sauver(j),"photographie initiale ecrite")
banc.verifier(not service.a_ecrire(j),"aucune revision en attente avant l'action")
-- Pas de tour de boucle entre la photographie et l'action : seul executer peut marquer.
local rangee,index=V.attribuer(p,j)
local avant=store:compteurs().total
banc.client(j):envoyer(game:GetService("ReplicatedStorage").JeuRemotes.VitreFinie,rangee,index)
banc.egal(p.pieces,1,"M22 confirmation immediate en memoire")
banc.verifier(service.a_ecrire(j),"M22 action confirmee marquee a sauvegarder")
banc.egal(store:compteurs().total,avant,"M22 aucune ecriture par action")
banc.egal(store:lire("j_8600").profil.pieces,0,"M22 ancien point de reprise intact avant sauvegarde")
banc.verifier(service.sauver(j),"M22 progression marquee persistante")
banc.egal(store:lire("j_8600").profil.pieces,1,"M22 point de reprise actualise")

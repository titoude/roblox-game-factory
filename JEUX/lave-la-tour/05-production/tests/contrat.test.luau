local C=banc.require("ServerScriptService.Jeu.ContratService")
local V=banc.require("ServerScriptService.Jeu.VitresService")
local S=banc.require("ServerScriptService.Jeu.EtatJoueur")
local E=banc.require("ServerScriptService.Jeu.EconomieService")
local t=0;local base=1704153590
V.horloge(function() return t end)
local c=C.nouveau({horloge=function() return t end,date=function() return base+t end})
local j,p={UserId=50},S.nouveau();V.inscrire(j,p)
banc.verifier(not c.ouvrir(j,p),"verrou sans r3")
p.robots.r3={achetes=1,en_service=0,chantiers={10}}
banc.verifier(not c.ouvrir(j,p),"chantier ne debloque pas")
p.robots.r3={achetes=1,en_service=1,chantiers={}}
banc.verifier(c.ouvrir(j,p),"r3 en service ouvre")
for n=1,40 do
 local r,i=c.attribuer(j,p)
 banc.verifier(not c.finir(j,p,r,i),"trop tot "..n)
 t+=1.5
 if n==40 then p.robots.r3.en_service=2;p.robots.r3.achetes=2 end
 local avant=p.pieces;local gain=E.gain_vitre(p)
 banc.verifier(c.finir(j,p,r,i),"vitre "..n)
 banc.proche(p.pieces-avant,gain+(if n==40 then 600*24 else 0),1e-8,"Q08 R derniere vitre "..n)
 banc.verifier(not c.finir(j,p,r,i),"rejeu refuse "..n)
end
banc.egal(p.contrat.jour,"2024-01-02","minuit jour de fin")
banc.verifier(not c.ouvrir(j,p),"une prime par jour")
banc.egal(p.tour.rangees,0,"aucun geste double sur tour")
t+=86400;banc.verifier(c.ouvrir(j,p),"jour suivant")
local r,i=c.attribuer(j,p);t+=1.5;c.finir(j,p,r,i)
local recharge=S.valider(p);c.quitter(j);V.inscrire(j,recharge);c.ouvrir(j,recharge)
local _,suivant=c.attribuer(j,recharge);banc.egal(suivant,2,"masque contrat restaure")
-- Budget commun 39, 40 puis 41, avec attribution suffisamment ancienne.
t+=60;for _=1,39 do V.consommer_budget(j,t) end
t+=1.5;r,i=c.attribuer(j,recharge);banc.verifier(c.finir(j,recharge,r,i),"quarantieme acceptee")
r,i=c.attribuer(j,recharge);t+=1.5
banc.verifier(not c.finir(j,recharge,r,i),"41e refusee")

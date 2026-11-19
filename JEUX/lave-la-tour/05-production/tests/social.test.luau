local S=banc.require("ServerScriptService.Jeu.SocialService")
local V=banc.require("ServerScriptService.Jeu.VitresService")
local Etat=banc.require("ServerScriptService.Jeu.EtatJoueur")
local t,utc=0,1704067200
V.horloge(function() return t end)
local s=S.nouveau({horloge=function() return t end,date=function() return utc+t end,amis=function() return true end})
local a,b,c={UserId=1},{UserId=2},{UserId=3}
local p,q,r=Etat.nouveau(),Etat.nouveau(),Etat.nouveau()
for _,x in {{a,p},{b,q},{c,r}} do V.inscrire(x[1],x[2]);s.inscrire(x[1],x[2]) end
banc.verifier(not s.action(b,"rejoindre",a),"premiere rangee requise")
q.tour.rangees=1;r.tour.rangees=1
banc.verifier(s.action(b,"rejoindre",a),"dernier arrive rejoint")
banc.verifier(not s.action(c,"rejoindre",a),"premier appui reserve la place")
local ra,ia=V.attribuer(p,a);local rb,ib=V.attribuer(p,b)
banc.verifier(ia~=ib,"vitres distinctes")
t=1.5;local ok,gain=V.finir_vitre(p,a,ra,ia,t);banc.verifier(ok,"proprietaire lave");s.finie(a,gain)
ok,gain=V.finir_vitre(p,b,rb,ib,t);banc.verifier(ok,"visiteur lave");s.finie(b,gain)
banc.proche(q.pieces,1.25,1e-9,"mousse 25 pourcent")
banc.proche(p.pieces,1.5,1e-9,"pourboire sans mousse")
for n=1,31 do t+=9;s.finie(a,1);s.finie(b,1) end
s.actualiser();banc.proche(p.quotas.mousse_s,279,1e-9,"temps effectif sans double compte")
t+=9;s.finie(a,1);s.finie(b,1);t+=9;s.finie(a,1);s.finie(b,1);t+=3;s.actualiser()
banc.egal(p.quotas.mousse_s,300,"borne partenaire")
local mousse,message=s.etat(a);banc.verifier(mousse and message=="mousse_quota_atteint","mousse visible au quota")
local avant=p.pieces;s.finie(a,1);banc.egal(p.pieces,avant,"aucun bonus apres quota")
p.quotas.pourboires_min=9.999;p.quotas.pourboires_par['2']=4.999
avant=p.pieces;s.finie(b,1);banc.proche(p.pieces-avant,0.06,1e-8,"M10 prorata sous borne")
avant=p.pieces;s.finie(b,1);banc.proche(p.pieces,avant,1e-8,"au dessus borne aucun pourboire")
banc.verifier(s.action(b,"retour"),"retour propre tour")
banc.verifier(not s.action(a,"rejoindre",b),"ancien arrive sans bouton")
banc.verifier(s.action(c,"rejoindre",a),"troisieme partenaire")
p.tour.rangees=120;p.tour.masque=0
banc.verifier(s.action(a,"chez_visiteur"),"M11 voyage duo")
banc.egal(V.position(a),r,"proprietaire devient visiteur")
banc.verifier(not s.action(a,"chez_visiteur"),"rejeu voyage refuse sur tour sale")
s.detacher(c);V.asseoir(c,r,"contrat")
banc.egal(V.position(a),p,"M13 visiteur ramene")
V.asseoir(c,r,"tour");s.action(c,"retour");s.action(c,"rejoindre",a)
s.quitter(a);V.quitter(a)
banc.egal(V.position(c),r,"proprietaire quitte")
t+=86400;s.actualiser();banc.egal(q.quotas.mousse_s,0,"nouveau jour UTC")

-- Bornes indépendantes, par jour et par partenaire, juste avant et après.
local x,y={UserId=21},{UserId=22}
local px,py=Etat.nouveau(),Etat.nouveau();py.tour.rangees=1
V.inscrire(x,px);V.inscrire(y,py);s.inscrire(x,px);s.inscrire(y,py);s.action(y,"rejoindre",x)
s.finie(x,1);s.finie(y,1)
for _,borne in {{"mousse_s",599.999,true},{"mousse_s",600.001,false},{"partenaire",299.999,true},{"partenaire",300.001,false}} do
 px.quotas.mousse_s=if borne[1]=="mousse_s" then borne[2] else 0
 px.quotas.mousse_par['22']=if borne[1]=="partenaire" then borne[2] else 0
 local avant=px.pieces;s.finie(x,1)
 banc.proche(px.pieces-avant,if borne[3] then 0.25 else 0,1e-9,"borne mousse "..borne[1]..borne[2])
end
for _,borne in {{9.999,0,0.06},{10.001,0,0},{0,4.999,0.06},{0,5.001,0}} do
 px.quotas.pourboires_min=borne[1];px.quotas.pourboires_par['22']=borne[2]
 local avant=px.pieces;s.finie(y,1)
 banc.proche(px.pieces-avant,borne[3],1e-8,"borne pourboire "..borne[1]..":"..borne[2])
end
px.quotas.pourboires_min=0;px.quotas.pourboires_par={}
px.robots.r1={achetes=4,en_service=4,chantiers={}}
s.finie(y,1);local minutes=px.quotas.pourboires_min
px.robots.r1={achetes=5,en_service=5,chantiers={}}
s.finie(y,1)
banc.proche(px.quotas.pourboires_min-minutes,0.625/75,1e-9,"hausse R ne restaure aucun quota")
local nouveau=Etat.valider(px)
banc.proche(nouveau.quotas.pourboires_min,px.quotas.pourboires_min,1e-9,"quotas persistables")
-- Borne : seul un joueur sur la place, près d'une borne attestée, monte.
local borne=false
local sb=S.nouveau({horloge=function() return t end,date=function() return utc+t end,borne=function() return borne end})
local h,k={UserId=31},{UserId=32};local ph,pk=Etat.nouveau(),Etat.nouveau()
V.inscrire(h,ph);V.inscrire(k,pk);sb.inscrire(h,ph);sb.inscrire(k,pk);sb.action(k,"descendre")
banc.verifier(not sb.action(k,"monter",h),"borne distante refusee")
borne=true;banc.verifier(sb.action(k,"monter",h),"borne proche attestee")

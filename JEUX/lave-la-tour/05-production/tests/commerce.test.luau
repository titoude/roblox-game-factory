local C=banc.require("ServerScriptService.Jeu.CommerceService")
local E=banc.require("ServerScriptService.Jeu.EconomieService")
local S=banc.require("ServerScriptService.Jeu.EtatJoueur")
local V=banc.require("ServerScriptService.Jeu.VitresService")
local Contrat=banc.require("ServerScriptService.Jeu.ContratService")
local t=0;V.horloge(function() return t end)
local m=game:GetService("MarketplaceService")
local signal=Instance.new("BindableEvent")
local faux={PromptGamePassPurchaseFinished=signal.Event,UserOwnsGamePassAsync=function(_,...) return m:UserOwnsGamePassAsync(...) end}
local config=table.clone(banc.require("ReplicatedStorage.Jeu.Config"))
config.OFFRES={raclette_motorisee=123,chantiers_express=124,peintures_nacelle=0,mousse_coloree=0,styles_tour=0}
local c=C.nouveau({Config=config,MarketplaceService=faux,horloge=function() return t end});c.demarrer()
local a,b={UserId=70},{UserId=71};local p,q=S.nouveau(),S.nouveau()
V.inscrire(a,p);V.inscrire(b,q);c.inscrire(a,p);c.inscrire(b,q)
banc.verifier(not p.passes.raclette_motorisee,"possession relue sans passe")
banc.passe(a,123,true);signal:Fire(a,123,true);banc.avancer(0)
banc.verifier(p.passes.raclette_motorisee,"achat relit possession")
banc.verifier(c.offres().peintures_nacelle==nil,"zero masque")
banc.egal(faux.ProcessReceipt({ProductId=999}),Enum.ProductPurchaseDecision.NotProcessedYet,"recu inconnu non accorde")
local function finir(j)
 local tour=V.position(j);local r,i=V.attribuer(tour,j)
 return V.finir_vitre(tour,j,r,i,t)
end
V.attribuer(p,a);t=1.999
banc.verifier(not c.avancer(a,true,finir),"avant deux secondes")
t=2;banc.verifier(c.avancer(a,true,finir),"deux secondes")
t=4;banc.verifier(c.avancer(a,true,finir),"cadence suivante")
banc.verifier(not c.avancer(b,true,finir),"visiteur sans passe inactif")
t=6;banc.verifier(not c.avancer(a,false,finir),"hors nacelle inactif")
V.asseoir(a,q,"tour");V.attribuer(q,a);t=8
banc.verifier(c.avancer(a,true,finir),"Q05 titulaire chez autre")
-- 39 consommations puis auto 40 et manuel 41 refuses par le meme chemin.
t+=60;for _=1,39 do V.consommer_budget(a,t) end
V.attribuer(q,a);t+=2;banc.verifier(c.avancer(a,true,finir),"auto quarantieme")
t+=1.5;banc.verifier(not finir(a),"manuel 41 refuse")
t+=2;banc.verifier(not c.avancer(a,true,finir),"auto 41 refuse")
t+=60
p.robots.r3={achetes=1,en_service=1,chantiers={}}
local contrat=Contrat.nouveau({horloge=function() return t end});contrat.ouvrir(a,p);t+=2
banc.verifier(c.avancer(a,true,function(j) local r,i=contrat.attribuer(j,p);return contrat.finir(j,p,r,i) end),"auto contrat")
banc.egal(p.contrat.vitres,1,"contrat une vitre")
local neuf=S.nouveau();neuf.pieces=10000;neuf.robots.r2={achetes=3,en_service=3,chantiers={}}
E.acheter_robot(neuf,"r3");banc.egal(neuf.robots.r3.chantiers[1],10,"chantier avant achat")
neuf.passes.chantiers_express=true;E.acheter_robot(neuf,"r3")
banc.egal(neuf.robots.r3.chantiers[1],10,"chantier existant conserve")
banc.egal(neuf.robots.r3.chantiers[2],5,"nouveau chantier divise")
banc.verifier(not E.acheter_robot(neuf,"r4"),"express respecte verrou")
E.avancer(neuf,4.999);banc.egal(neuf.robots.r3.en_service,0,"avant borne express")
E.avancer(neuf,0.002);banc.egal(neuf.robots.r3.en_service,1,"apres borne express")
c.quitter(a);c.inscrire(a,p);banc.verifier(p.passes.raclette_motorisee,"reconnexion relit")
banc.passe(a,123,false);c.relire(a);banc.verifier(not p.passes.raclette_motorisee,"cache non autoritaire")
local cache=C.nouveau();banc.egal(next(cache.offres()),nil,"cinq offres zero absentes")

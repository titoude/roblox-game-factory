-- Valeurs délibérément distinctes : les services et le validateur doivent rester d'accord.
local C=banc.require("ReplicatedStorage.Jeu.Config")
C.VITRES_PAR_RANGEE=3;C.VITRE_DUREE_MIN_S=0.2;C.PIGEONS_ETAGES=2
C.FLECHE.ETAGES_SEGMENT=2;C.FLECHE.VITRES_SEGMENT=6;C.FLECHE.ETAGE_DEBUT=101
C.CONTRAT_VITRES=3;C.CONTRAT_PRIME_S=7
C.MOUSSE_FENETRE_S=0.5;C.MOUSSE_MULTIPLICATEUR=1.75
C.MOUSSE_QUOTA_S=0.4;C.MOUSSE_PARTENAIRE_S=0.3
C.POURBOIRE_TAUX=0.75;C.POURBOIRE_QUOTA_MIN=0.02;C.POURBOIRE_PARTENAIRE_MIN=0.01;C.POURBOIRE_REVENU_MIN=2
local S=banc.require("ServerScriptService.Jeu.EtatJoueur")
local E=banc.require("ServerScriptService.Jeu.EconomieService")
local V=banc.require("ServerScriptService.Jeu.VitresService")
local D=banc.require("ServerScriptService.Jeu.DonneesService")
local Social=banc.require("ServerScriptService.Jeu.SocialService")
local Contrat=banc.require("ServerScriptService.Jeu.ContratService")
local t=0;V.horloge(function() return t end)
local function valide(p,etape) banc.verifier(D.valide(p),"profil sauvegardable : "..etape) end
local j={UserId=8700};local p=S.nouveau()
p.tour.numero=4;p.fleche.segments_achetes=1
V.inscrire(j,p)
banc.egal(V.stock(p),6,"D8 stock selon la geometrie configuree")
for n=1,6 do
    local r,i=V.attribuer(p,j);t+=0.25
    banc.verifier(V.finir_vitre(p,j,r,i,t),"D8 lavage de trois vitres par rangee")
    valide(p,"lavage "..n)
end
banc.egal(p.fleche.segments_laves,1,"D8 segment termine apres deux rangees")
banc.egal(E.record(p),102,"D8 record selon l'etage initial")
t+=C.PIGEONS_DELAI_S
banc.verifier(V.pigeons(p),"D8 retour des pigeons")
banc.egal(p.tour.pigeons.premiere_rangee,101,"D8 pigeons sur deux etages")
banc.egal(V.stock(p),6,"D8 stock de pigeons configure")
valide(p,"pigeons")
local a,b={UserId=8701},{UserId=8702};local pa,pb=S.nouveau(),S.nouveau()
V.inscrire(a,pa);V.inscrire(b,pb)
local social=Social.nouveau({horloge=function() return t end,date=function() return os.time()+t end})
social.inscrire(a,pa);social.inscrire(b,pb);V.asseoir(b,pa,"tour")
social.finie(b,1)
banc.proche(pa.pieces,0.75,1e-10,"D8 taux du pourboire configure")
banc.proche(pa.quotas.pourboires_min,0.75/120,1e-10,"D8 plancher de revenu configure")
social.finie(a,4)
banc.proche(pa.pieces,3.75,1e-10,"D8 multiplicateur mousse configure")
t+=0.31;social.actualiser()
banc.proche(pa.quotas.mousse_s,0.3,1e-10,"D8 quota partenaire configure")
banc.egal(select(2,social.etat(a)),"mousse_quota_atteint","D8 etat du quota configure")
pa.quotas.pourboires_min=0.019;pa.quotas.pourboires_par[tostring(b.UserId)]=0.0095
local avant=pa.pieces;social.finie(b,1)
banc.proche(pa.pieces-avant,0.06,1e-10,"D8 bord du quota partenaire de pourboire")
pa.quotas.pourboires_par[tostring(b.UserId)]=0
avant=pa.pieces;social.finie(b,1)
banc.proche(pa.pieces-avant,0.06,1e-10,"D8 bord du quota global de pourboire")
valide(pa,"duo proprietaire");valide(pb,"duo visiteur")
local c={UserId=8703};local pc=S.nouveau()
pc.robots.r3={achetes=1,en_service=1,chantiers={}}
V.inscrire(c,pc)
local contrat=Contrat.nouveau({horloge=function() return t end})
banc.verifier(contrat.ouvrir(c,pc),"contrat ouvert")
for n=1,3 do
    local r,i=contrat.attribuer(c,pc);t+=0.25
    banc.verifier(contrat.finir(c,pc,r,i),"D8 contrat duree et nombre de vitres configures")
    valide(pc,"contrat "..n)
end
banc.verifier(pc.contrat.prime_recue,"D8 prime au seuil configure")
banc.proche(pc.pieces,3*E.gain_vitre(pc)+7*E.revenu(pc),1e-9,"D8 prime selon Config")
pc.pieces=1000
banc.verifier(E.acheter_robot(pc,"r1"),"achat de robot")
valide(pc,"achat")
pc.robots.r5={achetes=1,en_service=1,chantiers={}}
banc.verifier(V.demenager(pc,"trajet-test"),"demenagement")
valide(pc,"demenagement")

local bornes=S.nouveau()
bornes.quotas.mousse_s=1;bornes.quotas.mousse_par["autre"]=1
bornes.quotas.pourboires_min=1;bornes.quotas.pourboires_par["autre"]=1
bornes=S.valider(bornes)
banc.egal(bornes.quotas.mousse_s,0.4,"D8 validation quota mousse global")
banc.egal(bornes.quotas.mousse_par.autre,0.3,"D8 validation quota mousse partenaire")
banc.egal(bornes.quotas.pourboires_min,0.02,"D8 validation quota pourboire global")
banc.egal(bornes.quotas.pourboires_par.autre,0.01,"D8 validation quota pourboire partenaire")

local A=banc.require("ServerScriptService.Jeu.ActionsDeTest")
A.studioQuota(bornes,"mousse_s",1);A.studioQuota(bornes,"pourboires_min",1)
valide(bornes,"actions Studio selon les quotas configures")

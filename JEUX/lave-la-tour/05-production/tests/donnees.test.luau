local D = banc.require("ServerScriptService.Jeu.DonneesService")
local S = banc.require("ServerScriptService.Jeu.EtatJoueur")
local E = banc.require("ServerScriptService.Jeu.EconomieService")
local temps = 100000
local function service(id, ds) return D.nouveau({serveur = id, horloge = function() return temps end, attendre = function() end, DataStoreService = ds}) end
local a, b = service("a"), service("b")
local function joueur(id) return {UserId = id, Kick = function(self, cle) self.kick = cle end} end
local store = banc.datastore("LaveLaTourJoueurs_v1_studio")
local ds = game:GetService("DataStoreService"):GetDataStore("LaveLaTourJoueurs_v1_studio")
local function comparer(a, b)
    banc.egal(type(a), type(b), "type restauré")
    if type(a) == "table" then
        for k,v in a do comparer(v,b[k]) end
        for k in b do banc.verifier(a[k] ~= nil, "aucun ajout") end
    else banc.egal(a,b,"champ restauré") end
end
local j = joueur(100)
local p = a.charger(j)
p.tour.masque = 21; p.robots.r3 = {achetes = 1, en_service = 0, chantiers = {12}}
p.operations = {"voyage", "segment"}
local attendu = S.valider(p)
banc.verifier(a.sauver(j,true), "sortie sûre")
local q = b.charger(j)
attendu.operations = q.operations
comparer(attendu,q)
banc.egal(q.tour.masque,21,"Q01 masque désordonné intact")
banc.egal(q.robots.r3.chantiers[1],12,"chantier conservé")
local autre = joueur(100)
banc.egal(a.charger(autre),nil,"deux serveurs refusés")
banc.egal(autre.kick,"donnees_indisponibles","renvoi avec clé")
temps += 600
banc.egal(a.charger(autre),nil,"verrou exactement 600 vivant")
temps += 1
banc.verifier(a.charger(autre) ~= nil,"verrou mort repris")
banc.verifier(not b.sauver(j),"ancien serveur ne réécrit pas")
for _, duree in {0,1,7199,7200,7201} do
    local x = joueur(200+duree)
    local pp = a.charger(x); pp.robots.r1 = {achetes=2,en_service=1,chantiers={0.5}}
    a.sauver(x,true); temps += duree
    local retour = b.charger(x)
    banc.proche(retour.pieces, math.min(duree,7200)*0.125,1e-9,"réserve bornée "..duree)
    banc.egal(retour.depart,0,"intervalle consommé")
    local solde = retour.pieces
    b.sauver(x,true)
    banc.egal(a.charger(x).pieces,solde,"Q02 réserve jamais doublée")
end
local x = joueur(500)
a.charger(x).pieces = 42; a.sauver(x,true)
local avant = store:lire("j_500")
store:panne_permanente(true)
banc.egal(b.charger(x),nil,"panne chargement sans profil")
banc.verifier(not b.sauver(x,true),"échec non sauvegardable")
comparer(avant,store:lire("j_500"))
store:panne_permanente(false);store:pannes(2)
banc.egal(b.charger(x).pieces,42,"troisième essai réussit")
store:pannes(2);banc.verifier(b.sauver(x,true),"reprise écriture")
banc.egal(store:userIds("j_500")[1],500,"métadonnée userId")
ds:SetAsync("j_600",{version=0,pieces=17,tour={masque=5}})
banc.egal(a.charger(joueur(600)).pieces,17,"migration ancienne version")
ds:SetAsync("j_601",{pieces="faux",robots=false,tour=false})
banc.egal(a.charger(joueur(601)).pieces,0,"corruption réparée")
for _, mauvais in {0/0,math.huge,-math.huge} do
 local pp = S.nouveau();pp.pieces=mauvais;banc.verifier(not D.valide(pp),"non fini refusé")
end
local creux=S.nouveau();creux.operations={[2]="trou"};banc.verifier(not D.valide(creux),"tableau creux refusé")
-- écriture du crédit en échec : aucun état mémoire utilisable, intervalle conservé.
local y=joueur(700);a.charger(y).robots.r1={achetes=1,en_service=1,chantiers={}};a.sauver(y,true);temps+=100
store:panne_permanente(true);banc.egal(b.charger(y),nil,"crédit non confirmé non exposé")
store:panne_permanente(false);banc.egal(b.charger(y).pieces,12.5,"intervalle rejoué intégralement")
-- Raccordement réel fermeture et sauvegarde périodique.
banc.demarrer_serveur();local z=banc.joueur(900,"Fermeture")
banc.avancer(90)
banc.verifier(store:lire("j_900").session ~= nil,"sauvegarde périodique")
banc.fermer_serveur()
banc.egal(store:lire("j_900").session,nil,"fermeture libère verrou")

-- Réponse perdue après une écriture effective et rappel optimiste du transformateur.
local durable, ecritures, panneApres = nil, 0, false
local faux = {GetDataStore=function() return {UpdateAsync=function(_,_,f)
    f(durable)
    local nouveau=f(durable)
    if nouveau then durable=nouveau;ecritures+=1 end
    if panneApres then panneApres=false;error("réponse perdue") end
    return durable
end} end}
local ds1,ds2=service("serveur1",faux),service("serveur2",faux)
local z=joueur(1001);local pp=ds1.charger(z)
pp.robots.r1={achetes=1,en_service=1,chantiers={}}
ds1.sauver(z,true);temps+=100;panneApres=true
banc.egal(ds2.charger(z).pieces,12.5,"réponse perdue : crédit unique")
banc.egal(durable.profil.depart,0,"crédit et consommation atomiques")
local avantEcritures=ecritures
banc.egal(ds1.charger(joueur(1001)),nil,"concurrence refuse sans écriture")
banc.egal(ecritures,avantEcritures,"zéro écriture sur verrou vivant")
-- Q01 : deux attributions dans la troisième rangée, seconde finie d'abord.
local V=banc.require("ServerScriptService.Jeu.VitresService")
local instant=0;V.horloge(function() return instant end)
for _,pigeons in {false,true} do
 local propre,visite=joueur(if pigeons then 1101 else 1100),joueur(if pigeons then 1201 else 1200)
 local profil,visiteur=a.charger(propre),a.charger(visite)
 profil.tour.rangees=2
 if pigeons then profil.tour.pigeons={cycle=3,premiere_rangee=101,rangees=2,masque=0} end
 V.inscrire(propre,profil);V.inscrire(visite,visiteur);V.asseoir(visite,profil,"tour")
 local ra,ia=V.attribuer(profil,propre);local rb,ib=V.attribuer(profil,visite)
 instant+=1.5;banc.verifier(V.finir_vitre(profil,visite,rb,ib,instant),"Q01 seconde attribution finie d'abord")
 V.quitter(visite);banc.verifier(a.sauver(visite,true),"Q01 sauvegarde visiteur")
 banc.verifier(a.sauver(propre,true),"Q01 sauvegarde propriétaire")
 local retour=b.charger(propre);local zone=retour.tour.pigeons or retour.tour
 banc.egal(zone.masque,2,"Q01 masque sans vitre sautée")
 banc.egal(b.charger(visite).pieces,1,"Q01 gain restauré")
 V.quitter(propre);V.inscrire(propre,retour)
 local _,index=V.attribuer(retour,propre);banc.egal(index,1,"Q01 réservation abandonnée libérée")
 banc.verifier(not V.finir_vitre(retour,propre,rb,ib,instant),"Q01 vitre propre non repayée")
end

local migrer=S.migrer
S.migrer=function() return nil,"profil_invalide" end
local precedent=store:lire("j_500")
banc.egal(service("migration").charger(joueur(500)),nil,"D5 migration illisible refusee")
comparer(precedent,store:lire("j_500"))
S.migrer=migrer

-- Q02 : accès à la Flèche juste sous et sur les deux bornes, puis opérations rejouées.
local C=banc.require("ReplicatedStorage.Jeu.Config")
for _,cas in {{99,5,false},{100,4,false},{100,5,true}} do
 local profil=S.nouveau()
 local restant=cas[1]
 for _,g in C.generateurs do local n=math.min(10,restant);restant-=n;profil.robots[g.id]={achetes=n,en_service=n,chantiers={}} end
 for n=1,cas[2] do profil.ameliorations['a'..n]=true end
 banc.egal(E.fleche_ouverte(profil),cas[3],"Q02 borne Flèche "..cas[1].."/"..cas[2])
end
local voyage=joueur(1500);local profil=a.charger(voyage)
for _,g in C.generateurs do profil.robots[g.id]={achetes=10,en_service=10,chantiers={}} end
for id in profil.ameliorations do profil.ameliorations[id]=true end
profil.pieces=9e15
banc.verifier(V.demenager(profil,"voyage-identifie"),"Q02 déménagement identifié")
a.sauver(voyage,true);profil=b.charger(voyage);instant+=21
banc.verifier(not V.demenager(profil,"voyage-identifie"),"Q02 déménagement rejoué avec prochaine tour ouverte")
profil.tour.numero=4;profil.tour.rangees=0;profil.tour.masque=0
banc.verifier(E.acheter_segment(profil,"segment-identifie"),"Q02 segment identifié")
b.sauver(voyage,true);profil=a.charger(voyage)
local cash=profil.pieces
banc.verifier(not E.acheter_segment(profil,"segment-identifie"),"Q02 segment rejoué avec place disponible")
banc.egal(profil.pieces,cash,"Q02 aucun second débit")

-- S3 : une panne conserve le profil ; seul un verrou perdu expulse.
local panne=service("panne")
local jp=joueur(1700)
local pp=panne.charger(jp)
pp.pieces=23.25;panne.marquer(jp)
store:pannes(3)
banc.verifier(not panne.sauver(jp),"S3 trois échecs signalés")
banc.egal(panne.profil(jp),pp,"S3 même profil conservé")
banc.egal(jp.kick,nil,"S3 aucune expulsion sur panne")
banc.verifier(panne.a_ecrire(jp),"S3 profil toujours à écrire")
banc.egal(store:lire("j_1700").profil.pieces,0,"S3 aucune fausse confirmation")
pp.pieces+=1
banc.verifier(panne.sauver(jp),"S3 cycle suivant réussi")
banc.egal(store:lire("j_1700").profil.pieces,24.25,"S3 progression complète écrite")
banc.verifier(not panne.a_ecrire(jp),"S3 marque effacée après succès")
local vole=store:lire("j_1700");vole.session.id="autre"
ds:SetAsync("j_1700",vole)
banc.verifier(not panne.sauver(jp),"S3 verrou perdu refuse écriture")
banc.egal(jp.kick,"donnees_indisponibles","S3 verrou perdu expulse")
banc.egal(panne.profil(jp),nil,"S3 profil perdu retiré")

-- S4 : reprises espacées après épuisement des trois essais ordinaires.
local attentes={}
local dependancesSortie={serveur="sortie",lancer=function(f) f() end,horloge=function() return temps end,attendre=function(s) table.insert(attentes,s) end}
local sortie=D.nouveau(dependancesSortie)
local js=joueur(1800);sortie.charger(js).pieces=38.75
store:pannes(3)
banc.verifier(sortie.sauver(js,true),"S4 reprise de sortie après trois pannes")
banc.egal(store:lire("j_1800").profil.pieces,38.75,"S4 dernier état écrit")
banc.egal(store:lire("j_1800").session,nil,"S4 verrou libéré")
banc.egal(attentes[3],4,"S4 reprise espacée")
local jf=joueur(1801);sortie.charger(jf).pieces=51
table.clear(attentes)
store:pannes(9)
banc.verifier(not sortie.sauver(jf,true),"S4 échec des trois séries signalé")
banc.verifier(temps-store:lire("j_1801").session.instant>600,"S4 dernier recours rend le verrou immediatement reprenable")
banc.egal(store:lire("j_1801").profil.pieces,0,"S4 dernier recours préserve le profil durable")
banc.egal(attentes[3],4,"S4 premiere reprise apres quatre secondes")
banc.egal(attentes[6],8,"S4 seconde reprise apres huit secondes")
banc.egal(sortie.profil(jf).pieces,51,"S4 progression retenue pour fermeture")
banc.verifier(sortie.fermer(),"S4 fermeture reprend la sortie échouée")
banc.egal(store:lire("j_1801").profil.pieces,51,"S4 fermeture récupère la progression")
-- Une fermeture termine le service ; la suite utilise une nouvelle instance.
sortie=D.nouveau(dependancesSortie)
local ji=joueur(1802);sortie.charger(ji).pieces=19
local verrouAvant=store:lire("j_1802").session.instant
store:panne_permanente(true)
banc.verifier(not sortie.sauver(ji,true),"S4 panne totale signalée")
banc.egal(store:lire("j_1802").session.instant,verrouAvant,"S4 expiration jamais prolongée en panne totale")
store:panne_permanente(false)
banc.verifier(sortie.sauver(ji,true),"S4 état récupérable après panne totale")

-- S5 : un ancien serveur peut finir sa sortie pendant l'attente.
local precedent=service("precedent")
local transfert=joueur(1900)
precedent.charger(transfert).pieces=63
local pauses=0
local suivant=D.nouveau({serveur="suivant",horloge=function() return temps end,attendre=function(secondes)
    banc.egal(secondes,5,"S5 intervalle de reprise")
    pauses+=1;temps+=secondes
    banc.egal(transfert.kick,nil,"S5 aucune expulsion pendant attente")
    if pauses==2 then banc.verifier(precedent.sauver(transfert,true),"S5 ancien serveur termine sortie") end
end})
banc.egal(suivant.charger(transfert).pieces,63,"S5 chargement après libération")
banc.egal(pauses,2,"S5 arrêt des reprises dès succès")
local refuse=joueur(1900)
local refusPauses=0
local bloque=D.nouveau({serveur="bloque",horloge=function() return temps end,attendre=function(secondes) refusPauses+=1;temps+=secondes end})
local durableAvant=store:lire("j_1900")
banc.egal(bloque.charger(refuse),nil,"S5 verrou vivant toujours refusé")
banc.egal(refusPauses,5,"S5 six tentatives espacées")
banc.egal(refuse.kick,"donnees_indisponibles","S5 renvoi après attente bornée")
comparer(durableAvant,store:lire("j_1900"))

-- S4 : une reponse perdue apres liberation ne devient pas un verrou perdu.
durable=nil
local reponse=service("reponse-sortie",faux)
local jr=joueur(1950);reponse.charger(jr).pieces=17
panneApres=true
banc.verifier(reponse.sauver(jr,true),"S4 sortie deja ecrite reconnue au rejeu")
banc.egal(jr.kick,nil,"S4 reponse perdue sans expulsion")
banc.egal(durable.profil.pieces,17,"S4 sortie durable apres reponse perdue")
banc.egal(durable.session,nil,"S4 rejeu ne reprend pas le verrou")

-- S4 : apres expiration de secours, un nouveau serveur garde la priorite.
local parti=joueur(1960);sortie.charger(parti).pieces=99
store:pannes(9)
banc.verifier(not sortie.sauver(parti,true),"S4 sortie epuisee avant transfert")
local nouveau=service("nouveau-apres-sortie")
local arrive=joueur(1960)
banc.verifier(nouveau.charger(arrive)~=nil,"S4 verrou expire reprenable immediatement")
nouveau.profil(arrive).pieces=85
banc.verifier(nouveau.sauver(arrive,true),"S4 nouveau serveur termine sa session")
banc.verifier(not sortie.sauver(parti,true),"S4 ancien serveur ne reprend pas une session terminee ailleurs")
banc.egal(store:lire("j_1960").profil.pieces,85,"S4 nouvelle progression jamais remplacee")

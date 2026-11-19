#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto-test du banc : mini-jeu et scénarios créés uniquement dans le temporaire."""
import runpy
import subprocess
import sys
import tempfile
import time
from pathlib import Path

OUTILS = Path(__file__).resolve().parent
module = runpy.run_path(str(OUTILS / "banc-luau.py"))
ecrire_sur = module["ecrire_sur"]

SCRIPTS = {
    "ServerStorage.Classe.lua": '''local C={}
C.__index=C
function C.nouveau(v) return setmetatable({valeur=v},C) end
function C:double() return self.valeur*2 end
function C:__tostring() return "Classe:"..self.valeur end
function C.__eq(a,b) return a.valeur==b.valeur end
C.globales={setmetatable=setmetatable,getmetatable=getmetatable,rawget=rawget,rawset=rawset,rawequal=rawequal,rawlen=rawlen,newproxy=newproxy,select=select,unpack=unpack,table=table,string=string,math=math,coroutine=coroutine,bit32=bit32,utf8=utf8,buffer=buffer,xpcall=xpcall,assert=assert,error=error,tostring=tostring,tonumber=tonumber,type=type,ipairs=ipairs,pairs=pairs,next=next}
return C
''',
    "ReplicatedStorage.Jeu.Config.lua": '''return {revenu=2,prix=10,quota=3,produit=77}
''',
    "ServerScriptService.Jeu.DonneesService.lua": '''local D={etats={}}
local store=game:GetService("DataStoreService"):GetDataStore("Profils")
function D.charger(j)
    local cle=tostring(j.UserId)
    local profil=store:UpdateAsync(cle,function(p)
        p=p or {cash=0,recus={},achats=0}
        assert(not p.verrou or p.verrou==game.JobId,"session verrouillée")
        p.verrou=game.JobId; return p
    end)
    D.etats[j]=profil
end
function D.sauver(j,liberer)
    local p=D.etats[j]
    for essai=1,3 do
        local ok=pcall(function()
            store:UpdateAsync(tostring(j.UserId),function(ancien)
                assert(ancien.verrou==game.JobId,"verrou perdu")
                local copie=table.clone(p)
                if liberer then copie.verrou=nil end
                return copie,{j.UserId}
            end)
        end)
        if ok then return true end
        task.wait(1)
    end
    return false
end
return D
''',
    "ServerScriptService.Jeu.EconomieService.lua": '''local C=require(game:GetService("ReplicatedStorage").Jeu.Config)
local D=require(script.Parent.DonneesService)
local E={}
function E.demarrer()
    local achat=Instance.new("RemoteEvent",game:GetService("ReplicatedStorage")); achat.Name="Acheter"
    local dernier={}
    achat.OnServerEvent:Connect(function(j,objet)
        local p=D.etats[j]
        if type(objet)~="string" or objet~="outil" or not p then return end
        if dernier[j] and time()-dernier[j]<1 then return end
        dernier[j]=time()
        if p.cash<C.prix or p.achats>=C.quota then return end
        p.cash-=C.prix; p.achats+=1; achat:FireClient(j,p.cash)
    end)
    task.spawn(function()
        while true do
            task.wait(1)
            for _,p in pairs(D.etats) do p.cash+=C.revenu end
        end
    end)
    game:GetService("MarketplaceService").ProcessReceipt=function(r)
        local j=game:GetService("Players"):GetPlayerByUserId(r.PlayerId)
        if not j or r.ProductId~=C.produit then return Enum.ProductPurchaseDecision.NotProcessedYet end
        local p=D.etats[j]
        if not p.recus[r.PurchaseId] then p.cash+=50; p.recus[r.PurchaseId]=true end
        if D.sauver(j) then return Enum.ProductPurchaseDecision.PurchaseGranted end
        return Enum.ProductPurchaseDecision.NotProcessedYet
    end
end
return E
''',
    "ServerScriptService.Jeu.Amorce.server.lua": '''local D=require(script.Parent.DonneesService)
game:GetService("Players").PlayerAdded:Connect(D.charger)
game:GetService("Players").PlayerRemoving:Connect(function(j)
    D.sauver(j,true); D.etats[j]=nil
end)
game:BindToClose(function() for j in pairs(D.etats) do D.sauver(j,true) end end)
require(script.Parent.EconomieService).demarrer()
''',
}

PRELUDE = '''banc.demarrer_serveur()
local j=banc.joueur(12,"Alice")
local D=banc.require("ServerScriptService.Jeu.DonneesService")
local r=banc.instance("ReplicatedStorage.Acheter")
'''

CAS = [
    ("classe à métatables chargée et fonctionnelle", '''local C=banc.require("ServerStorage.Classe")
local a,b,c=C.nouveau(7),C.nouveau(7),C.nouveau(8)
banc.egal(a:double(),14,"__index")
banc.egal(tostring(a),"Classe:7","__tostring")
banc.verifier(a==b and a~=c,"__eq")
banc.egal(getmetatable(a),C)
banc.verifier(not rawequal(a,b))
rawset(a,"brut",12); banc.egal(rawget(a,"brut"),12)
banc.egal(rawlen({1,2}),2)
banc.egal(type(newproxy(true)),"userdata")
''', True, "scénario terminé"),
    ("énumération des globales standard dans module et test", '''local C=banc.require("ServerStorage.Classe")
local attendues={setmetatable=setmetatable,getmetatable=getmetatable,rawget=rawget,rawset=rawset,rawequal=rawequal,rawlen=rawlen,newproxy=newproxy,select=select,unpack=unpack,table=table,string=string,math=math,coroutine=coroutine,bit32=bit32,utf8=utf8,buffer=buffer,xpcall=xpcall,assert=assert,error=error,tostring=tostring,tonumber=tonumber,type=type,ipairs=ipairs,pairs=pairs,next=next}
for nom,v in pairs(attendues) do
    banc.egal(C.globales[nom],v,"globale module et test : "..nom)
    banc.egal(type(v),if table.find({"table","string","math","coroutine","bit32","utf8","buffer"},nom) then "table" else "function",nom)
end
''', True, "scénario terminé"),
    ("économie, validation Remote et quota", PRELUDE + '''banc.avancer(20)
banc.egal(D.etats[j].cash,40,"revenu exécuté")
local client=banc.client(j)
client:envoyer(r,1000000); client:envoyer(r,{prix=-1})
banc.egal(D.etats[j].cash,40,"arguments hostiles refusés")
client:envoyer(r,"outil"); client:envoyer(r,"outil")
banc.egal(D.etats[j].achats,1,"cadence validée")
for i=1,4 do banc.avancer(1); client:envoyer(r,"outil") end
banc.egal(D.etats[j].achats,3,"quota validé")
banc.egal(#client:messages(r),3,"messages au bon joueur")
banc.verifier(banc.require("ServerScriptService.Jeu.DonneesService")==D,"cache require")
''', True, "scénario terminé"),
    ("assertion fausse détectée et ligne originale", "banc.egal(1,2,\"volontaire\")", False, ".test.luau:1"),
    ("erreur différée propagée avec trace", '''task.delay(2,function() error("differee-volontaire") end)
banc.avancer(3)''', False, "differee-volontaire"),
    ("require cyclique détecté", '''banc.require("ServerScriptService.Jeu.DonneesService")''', False, "require cyclique"),
    ("API absente explicite", '''game:GetService("Players"):MethodeInconnue()''', False, "API non simulée : Players.MethodeInconnue"),
    ("panne DataStore puis reprise et budget", PRELUDE + '''banc.avancer(5)
local ds=banc.datastore("Profils"); ds:pannes(2)
task.spawn(function() banc.verifier(D.sauver(j),"reprise réussie") end)
banc.avancer(2)
banc.egal(ds:compteurs().total,4,"chargement et trois tentatives")
banc.egal(ds:lire("12").cash,14,"sauvegarde après reprise")
banc.egal(ds:userIds("12")[1],12,"userIds conservés")
''', True, "reprise réussie"),
    ("reçu rejoué sans double attribution durable", PRELUDE + '''banc.egal(banc.recu(j,77,"achat-A"),Enum.ProductPurchaseDecision.PurchaseGranted)
banc.egal(banc.recu(j,77,"achat-A"),Enum.ProductPurchaseDecision.PurchaseGranted)
banc.egal(D.etats[j].cash,50,"un seul crédit")
banc.quitter(j); j=banc.joueur(12,"Alice")
banc.recu(j,77,"achat-A")
banc.egal(D.etats[j].cash,50,"reçu durable après reconnexion")
banc.verifier(banc.datastore("Profils"):lire("12").recus["achat-A"],"reçu sauvegardé")
''', True, "reçu sauvegardé"),
    ("deux heures fictives en moins de cinq secondes", PRELUDE + '''banc.avancer(7200)
banc.egal(D.etats[j].cash,14400,"deux heures de revenu réel exécuté")
banc.egal(os.time(),1704074400)
banc.egal(os.date("!%Y-%m-%d %H:%M:%S"),"2024-01-01 02:00:00")
banc.egal(DateTime.now().UnixTimestampMillis,1704074400000)
''', True, "deux heures de revenu"),
    ("verrou de session concurrente refusé", '''local ds=game:GetService("DataStoreService"):GetDataStore("Profils")
ds:SetAsync("12",{cash=10,recus={},verrou="autre-session"})
banc.demarrer_serveur(); banc.joueur(12,"Alice")''', False, "session verrouillée"),
    ("fermeture serveur sauvegarde et libère", PRELUDE + '''banc.avancer(3); banc.fermer_serveur()
local p=banc.datastore("Profils"):lire("12")
banc.egal(p.cash,6); banc.egal(p.verrou,nil)
''', True, "scénario terminé"),
    ("fermeture attend les reprises de sauvegarde", PRELUDE + '''banc.datastore("Profils"):pannes(2)
banc.fermer_serveur()
banc.egal(banc.datastore("Profils"):lire("12").verrou,nil)
banc.egal(banc.datastore("Profils"):compteurs().total,4)
''', True, "scénario terminé"),
    ("arbre, attributs, signaux et Clone", '''local f=Instance.new("Folder"); f.Name="Racine"
local n=Instance.new("IntValue",f); n.Name="Compteur"
local changes,attributs,ajouts,retraits=0,0,0,0
f.ChildAdded:Connect(function() ajouts+=1 end)
f.ChildRemoved:Connect(function() retraits+=1 end)
local connexion=n.Changed:Connect(function(v) changes+=v end)
n:GetAttributeChangedSignal("niveau"):Once(function() attributs+=1 end)
n.Value=2; n:SetAttribute("niveau",4); banc.avancer(0)
connexion:Disconnect(); n.Value=3; n:SetAttribute("niveau",5)
local c=n:Clone(); c.Parent=f; c:Destroy(); banc.avancer(0)
banc.egal(changes,2); banc.egal(attributs,1); banc.egal(ajouts,1); banc.egal(retraits,1)
banc.verifier(n:IsA("ValueBase")); banc.egal(#f:GetDescendants(),1)
banc.erreur_attendue(function() f:WaitForChild("Absent") end,"WaitForChild absent")
local e=Instance.new("BindableEvent"); local recu
task.spawn(function() recu=e.Event:Wait() end); banc.avancer(0); e:Fire(9); banc.avancer(0)
banc.egal(recu,9)
local rf=Instance.new("RemoteFunction"); rf.OnServerInvoke=function(j,v) return j.UserId+v end
banc.egal(banc.client(banc.joueur(2)):invoquer(rf,3),5)
''', True, "scénario terminé"),
    ("JSON, sérialisation et isolation des données", r'''local h=game:GetService("HttpService")
local v=h:JSONDecode('{"texte":"a\\n\\u00e9\\ud83d\\ude00","v":[1,false,2.5e2]}')
banc.egal(v.texte,"a\né😀"); banc.egal(v.v[3],250)
banc.egal(h:JSONDecode(h:JSONEncode(v)).texte,v.texte)
for _,s in ipairs({'[1,]','01','{"a":}','"\\q"','null x'}) do banc.erreur_attendue(function() h:JSONDecode(s) end) end
local d=game:GetService("DataStoreService"):GetDataStore("Essai")
d:SetAsync("a",{x=2}); local x=d:GetAsync("a"); x.x=9; banc.egal(d:GetAsync("a").x,2)
banc.erreur_attendue(function() d:SetAsync("a",function() end) end,"JSON")
banc.erreur_attendue(function() d:SetAsync("a",Instance.new("Folder")) end,"JSON")
local cycle={}; cycle.x=cycle; banc.erreur_attendue(function() d:SetAsync("a",cycle) end,"cycle")
banc.erreur_attendue(function() d:SetAsync("a",string.rep("a",4*1024*1024)) end,"4 Mo")
local ds=banc.datastore("Essai"); ds:panne_permanente(true)
banc.erreur_attendue(function() d:GetAsync("a") end,"panne injectée")
ds:panne_permanente(false); banc.egal(d:GetAsync("a").x,2)
local o=game:GetService("DataStoreService"):GetOrderedDataStore("Classement")
o:IncrementAsync("a",2); o:SetAsync("b",5); o:SetAsync("c",3)
local pages=o:GetSortedAsync(false,2); banc.egal(pages:GetCurrentPage()[1].key,"b")
banc.egal(pages.IsFinished,false); pages:AdvanceToNextPageAsync(); banc.egal(pages:GetCurrentPage()[1].key,"a")
banc.egal(pages.IsFinished,true); banc.egal(o:RemoveAsync("a"),2)
''', True, "scénario terminé"),
    ("temps, annulation, Heartbeat et tween", '''local compte,dt=0,0
local connexion=game:GetService("RunService").Heartbeat:Connect(function(d) compte+=1; dt+=d end)
local co=task.delay(1,function() error("annulé") end); task.cancel(co)
local fini=false; task.defer(function() task.wait(0.5); fini=true end)
local p=Instance.new("Part"); local tween=game:GetService("TweenService"):Create(p,TweenInfo.new(1),{Transparency=1})
local termine=false; tween.Completed:Once(function() termine=true end); tween:Play()
banc.avancer(1.001); connexion:Disconnect()
banc.egal(compte,60); banc.proche(dt,1,0.000001); banc.verifier(fini and termine)
banc.egal(p.Transparency,1); banc.proche(os.clock(),1.001,0.00001)
banc.egal(typeof(connexion),"RBXScriptConnection")
banc.egal(typeof(game:GetService("RunService").Heartbeat),"RBXScriptSignal")
banc.egal(os.time({year=2024,month=1,day=1,hour=0}),1704067200)
banc.egal(os.date("!%c",1704067200),"Mon Jan  1 00:00:00 2024")
''', True, "scénario terminé"),
    ("services enregistrés et types", '''local j=banc.joueur(3,"Bob")
banc.studio(false); banc.verifier(not game:GetService("RunService"):IsStudio())
banc.passe(j,99,true); local m=game:GetService("MarketplaceService")
banc.verifier(m:UserOwnsGamePassAsync(3,99)); m:PromptProductPurchase(j,77); banc.egal(#m.prompts,1)
local c=game:GetService("CollectionService"); c:AddTag(j,"test"); banc.egal(c:GetTagged("test")[1],j)
c:RemoveTag(j,"test"); banc.verifier(not c:HasTag(j,"test"))
game:GetService("AnalyticsService"):LogCustomEvent(j,"arrivee",1); banc.egal(#banc.analytics(),1)
local msg=game:GetService("MessagingService"); local vu
msg:SubscribeAsync("canal",function(m) vu=m.Data end); msg:PublishAsync("canal",42); banc.avancer(0); banc.egal(vu,42)
local b=game:GetService("BadgeService"); b:AwardBadgeAsync(3,5); banc.verifier(b:UserHasBadgeAsync(3,5))
banc.egal(game:GetService("TextService"):FilterStringAsync("bonjour",3):GetNonChatStringForBroadcastAsync(),"bonjour")
banc.egal(typeof(Vector3.new()),"Vector3"); banc.egal(Vector3.new(1,2,3):Dot(Vector3.one),6)
local cf=CFrame.new(3,4,5)*CFrame.Angles(0,0,math.pi/2)
local p=cf:PointToObjectSpace(cf*Vector3.new(1,2,3)); banc.proche((p-Vector3.new(1,2,3)).Magnitude,0,0.00001)
banc.egal(Random.new(10):NextInteger(1,99),Random.new(10):NextInteger(1,99))
warn("avertissement"); banc.egal(#banc.avertissements(),1)
''', True, "scénario terminé"),
    ("Script inactif avant démarrage", '''banc.erreur_attendue(function() banc.instance("ReplicatedStorage.Acheter") end,"WaitForChild absent")
banc.demarrer_serveur(); banc.demarrer_serveur()
banc.egal(#game:GetService("ReplicatedStorage"):GetChildren(),2)
''', True, "scénario terminé"),
    ("boucle infinie interrompue", "while true do end", False, "durée maximale"),
]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    echecs = []
    with tempfile.TemporaryDirectory(prefix="auto-banc-luau-") as temporaire:
        racine = Path(temporaire)
        src, tests = racine / "src", racine / "tests"
        src.mkdir(); tests.mkdir()
        for nom, contenu in SCRIPTS.items():
            ecrire_sur(src / nom, contenu)
        # Chaque source et chaque test Luau est aussi passé au compilateur officiel.
        for numero, (nom, scenario, attendu, motif) in enumerate(CAS):
            test = tests / f"cas-{numero}.test.luau"
            ecrire_sur(test, scenario)
            donnees = src / "ServerScriptService.Jeu.DonneesService.lua"
            economie = src / "ServerScriptService.Jeu.EconomieService.lua"
            if nom == "require cyclique détecté":
                ecrire_sur(donnees, "return require(script.Parent.EconomieService)\n")
                ecrire_sur(economie, "return require(script.Parent.DonneesService)\n")
            else:
                ecrire_sur(donnees, SCRIPTS[donnees.name])
                ecrire_sur(economie, SCRIPTS[economie.name])
            compilation = [subprocess.run([str(OUTILS / "bin" / "luau-compile.exe"), "--null", str(f)],
                                         capture_output=True, encoding="utf-8", errors="replace", timeout=10)
                           for f in [*src.glob("*.lua"), test]]
            programme = racine / "programme.luau"
            texte, _ = module["assembler"](module["sources"](src), test)
            ecrire_sur(programme, texte)
            compilation.append(subprocess.run([str(OUTILS / "bin" / "luau-compile.exe"), "--null", str(programme)],
                                              capture_output=True, encoding="utf-8", errors="replace", timeout=10))
            debut = time.perf_counter()
            resultat = subprocess.run([sys.executable, str(OUTILS / "banc-luau.py"), str(src),
                                       "--tests", str(tests), "--filtre", test.name, "--verbeux"],
                                      capture_output=True, encoding="utf-8", errors="replace", timeout=25)
            duree = time.perf_counter() - debut
            sortie = resultat.stdout + resultat.stderr
            ok = ((resultat.returncode == 0) == attendu and motif in sortie
                  and all(c.returncode == 0 for c in compilation))
            if nom.startswith("deux heures"):
                ok = ok and duree < 5
            print(f"{'PASSE' if ok else 'ECHEC'} : {nom} ({duree:.3f} s)")
            if not ok:
                echecs.append(nom)
                print(sortie)
                for c in compilation:
                    if c.returncode: print(c.stdout + c.stderr)
    print(f"{len(CAS)-len(echecs)}/{len(CAS)} contrôles passés")
    return int(bool(echecs))


if __name__ == "__main__":
    raise SystemExit(main())

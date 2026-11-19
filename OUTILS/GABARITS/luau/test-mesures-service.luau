-- Faux autonomes ; aucun accès à Roblox.
local module = require("./ServerScriptService.Jeu.MesuresService")
local t = 1793491200 -- 2026-11-01 UTC
local valeurs, noms = {}, {}
local panne, apres, appels, analytics, attentes = 0, false, 0, 0, {}
local hook
local ds = {}
function ds:GetDataStore(nom)
    table.insert(noms, nom)
    return { UpdateAsync = function(_, cle, transformer)
        appels += 1
        if panne > 0 and not apres then panne -= 1; error("panne") end
        -- Roblox peut rappeler le transformateur sans appliquer son premier résultat.
        transformer(valeurs[cle])
        valeurs[cle] = transformer(valeurs[cle])
        if hook then local h = hook; hook = nil; h() end
        if panne > 0 then panne -= 1; error("réponse perdue après écriture") end
        return valeurs[cle]
    end }
end
local compteur = 0
local fermeture, boucle
local function nouveau(studio)
    compteur += 1
    return module.nouveau({ NOM_COURT = "Test" }, {
        DataStoreService = ds, RunService = { IsStudio = function() return studio == true end },
        AnalyticsService = { LogOnboardingFunnelStepEvent = function(_, _, numero, nom)
            assert(numero == 1 and nom == "arrivee"); analytics += 1
        end },
        jeton = tostring(compteur), horloge = function() return t end,
        attendre = function(n) table.insert(attentes, n) end,
        lancer = function(f) boucle = f end, BindToClose = function(f) fermeture = f end,
    })
end
local nombre = 0
local function verifier(nom, ok)
    assert(ok, "ECHEC " .. nom); nombre += 1; print("ok     " .. nom)
end
local s = nouveau(true)
verifier("magasin Studio", noms[1] == "TestMesures_v1_studio")
s = nouveau()
verifier("magasin production", noms[2] == "TestMesures_v1")
local p, joueur = {}, { UserId = 123456, Name = "SecretPersonnel" }
s:joueur_arrive(joueur, p)
s:joueur_arrive(joueur, p)
verifier("étape unique", s:etape(joueur, p, "arrivee") and not s:etape(joueur, p, "arrivee") and analytics == 1)
t += 60
s:joueur_part(joueur, p); s:joueur_part(joueur, p); s:vider()
local v = valeurs["j_2026-11-01"]
verifier("nouveau, actif, session uniques", v.nouveaux == 1 and v.actifs == 1 and v.sessions == 1 and v.minutes == 1)
verifier("borne 60", v.s_0_60 == 1 and v.s_61_180 == 0)
for _, duree in ipairs({61, 180, 181, 600, 601, 1800, 1801}) do
    local j, profil = {}, {}
    s:joueur_arrive(j, profil); t += duree; s:joueur_part(j, profil); s:vider()
end
v = valeurs["j_2026-11-01"]
verifier("bornes 61 et 180", v.s_61_180 == 2)
verifier("bornes 181 et 600", v.s_181_600 == 2)
verifier("bornes 601 et 1800", v.s_601_1800 == 2)
verifier("borne 1801", v.s_1801_plus == 1)
t = 1793577600
for _ = 1, 2 do s:joueur_arrive(joueur, p); s:joueur_part(joueur, p) end
s:vider()
v = valeurs["j_2026-11-02"]
verifier("J1 une fois et actif unique", v.retours_j1 == 1 and v.actifs == 1 and v.nouveaux == 0)
t = 1794096000
for _ = 1, 2 do s:joueur_arrive(joueur, p); s:joueur_part(joueur, p) end
s:vider()
verifier("J7 une fois", valeurs["j_2026-11-08"].retours_j7 == 1)
t = 1794268800 - 30
local q, j = {}, {}
s:joueur_arrive(j, q)
t += 60
s:joueur_part(j, q); s:vider()
v = valeurs["j_2026-11-10"]
verifier("minuit : activité et J1", v.actifs == 1 and v.retours_j1 == 1 and v.nouveaux == 0)
verifier("session rattachée au jour de fin", v.sessions == 1 and v.minutes == 1)
local autre = nouveau()
autre:joueur_arrive({}, {}); autre:vider()
verifier("deux serveurs additionnent", valeurs["j_2026-11-10"].nouveaux == 1 and valeurs["j_2026-11-10"].actifs == 2)
local avant = valeurs["j_2026-11-10"].nouveaux
s:joueur_arrive({}, {})
panne = 3; apres = false
verifier("panne conservée", not s:vider() and valeurs["j_2026-11-10"].nouveaux == avant)
verifier("attente croissante", attentes[#attentes-1] == 1 and attentes[#attentes] == 2)
s:vider(); s:vider()
verifier("reprise sans perte ni doublon", valeurs["j_2026-11-10"].nouveaux == avant + 1)
s:joueur_arrive({}, {}); panne = 3; apres = true
verifier("réponse perdue", not s:vider())
s:vider(); s:vider()
verifier("écriture acceptée puis erreur sans doublon", valeurs["j_2026-11-10"].nouveaux == avant + 2)
s:joueur_arrive({}, {})
hook = function() s:joueur_arrive({}, {}); assert(not s:vider()) end
s:vider(); s:vider()
verifier("ajouts pendant envoi conservés", valeurs["j_2026-11-10"].nouveaux == avant + 4)
local avantAppels = appels
s:vider()
verifier("aucun envoi vide", appels == avantAppels)
s:demarrer()
verifier("boucle et fermeture enregistrées", type(boucle) == "function" and type(fermeture) == "function")
fermeture()
verifier("fermeture compte les sessions ouvertes", valeurs["j_2026-11-10"].sessions > 1)
local prive = true
for cle, valeur in pairs(valeurs) do
    prive = prive and cle:match("^j_%d%d%d%d%-%d%d%-%d%d$") ~= nil
    for nom, n in pairs(valeur) do
        prive = prive and type(n) == "number" and n >= 0 and n % 1 == 0
            and nom ~= "userId" and nom ~= "Name" and nom ~= "texte"
            and nom ~= "cohorte_j1_base" and nom ~= "cohorte_j7_base"
    end
end
verifier("aucune donnée personnelle, entiers seulement", prive)
local cycle, fermerCycle
local periodique = module.nouveau({ NOM_COURT = "Test" }, {
    DataStoreService = ds, RunService = { IsStudio = function() return false end },
    AnalyticsService = false, jeton = "periodique", horloge = function() return t end,
    attendre = function(n) coroutine.yield(n) end,
    lancer = function(f) cycle = coroutine.create(f) end,
    BindToClose = function(f) fermerCycle = f end,
})
periodique:demarrer()
local okCycle, delai = coroutine.resume(cycle)
verifier("boucle attend 300 secondes", okCycle and delai == 300)
local avantCycle = appels
okCycle, delai = coroutine.resume(cycle)
verifier("cycle sans nouveau sans écriture", okCycle and delai == 300 and appels == avantCycle)
periodique:joueur_arrive({}, {})
okCycle, delai = coroutine.resume(cycle)
verifier("cycle avec nouveau écrit", okCycle and delai == 300 and appels == avantCycle + 1)
fermerCycle()
okCycle = coroutine.resume(cycle)
verifier("boucle arrêtée à la fermeture", okCycle and coroutine.status(cycle) == "dead")
print(tostring(nombre) .. "/" .. tostring(nombre) .. " contrôles passés")

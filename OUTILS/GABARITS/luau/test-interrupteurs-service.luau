-- Faux autonomes ; aucun accès à Roblox.
local module = require("./ServerScriptService.Jeu.InterrupteursService")
local t, lectures, ecritures, nombre = 0, 0, 0, 0
local contenu, panne, ouverture, boucle, nomMagasin = nil, false, false, nil, nil
local ds = {}
function ds:GetDataStore(nom)
    if ouverture then error("ouverture impossible") end
    nomMagasin = nom
    return {
        GetAsync = function(_, cle)
            assert(cle == "interrupteurs"); lectures += 1
            if panne then error("lecture impossible") end
            return contenu
        end,
        SetAsync = function() ecritures += 1 end,
        UpdateAsync = function() ecritures += 1 end,
    }
end
local function nouveau(studio)
    return module.nouveau({ NOM_COURT = "Test" }, {
        DataStoreService = ds, RunService = { IsStudio = function() return studio end },
        horloge = function() return t end, attendre = coroutine.yield,
        lancer = function(f) boucle = coroutine.create(f) end,
    }, { boutique_ouverte = { defaut = true }, vitesse = { defaut = 1, min = 0, max = 2 },
        message_maintenance = { defaut = "" } })
end
local function verifier(nom, ok)
    assert(ok, "ECHEC " .. nom); nombre += 1; print("ok     " .. nom)
end
local s = nouveau(false)
s:demarrer()
verifier("défauts sans entrée", s:actif("boutique_ouverte") and s:valeur("vitesse") == 1)
verifier("magasin production", nomMagasin == "TestReglages_v1")
local appels = 0
s:au_changement("boutique_ouverte", function(v, ancien) assert(v == false and ancien == true); appels += 1 end)
s:au_changement("boutique_ouverte", function() error("rappel en panne") end)
local function cycle(n)
    t += n
    local ok, delai = coroutine.resume(boucle)
    assert(ok and delai == 60)
end
cycle(0)
contenu = { boutique_ouverte = false, vitesse = 2, inconnu = true, version = 1, maj = 123 }
cycle(59)
verifier("aucune lecture avant 60 s", lectures == 1 and s:actif("boutique_ouverte"))
cycle(1)
verifier("changement après 60 s", not s:actif("boutique_ouverte") and s:valeur("vitesse") == 2)
cycle(60)
verifier("rappel une seule fois et panne isolée", appels == 1)
panne = true; contenu.boutique_ouverte = true; cycle(60)
verifier("panne garde la dernière valeur", not s:actif("boutique_ouverte"))
panne = false; contenu.boutique_ouverte = "true"; contenu.vitesse = 3; cycle(60)
verifier("type faux refusé", not s:actif("boutique_ouverte"))
verifier("nombre hors bornes refusé", s:valeur("vitesse") == 2)
verifier("inconnu ignoré", s:valeur("inconnu") == nil and not s:au_changement("inconnu", function() end))
contenu.message_maintenance = string.rep("é", 200); cycle(60)
verifier("chaîne courte UTF-8", s:valeur("message_maintenance") == contenu.message_maintenance)
contenu.message_maintenance = string.rep("x", 201); cycle(60)
verifier("chaîne longue refusée", s:valeur("message_maintenance") == string.rep("é", 200))
local avant = lectures; s:demarrer()
verifier("démarrage idempotent", lectures == avant)
local studio = nouveau(true); studio:demarrer()
verifier("magasin Studio", nomMagasin == "TestReglages_v1_studio")
ouverture = true
local sans = nouveau(false); sans:demarrer()
verifier("panne ouverture garde défaut", sans:actif("boutique_ouverte"))
verifier("aucune écriture", ecritures == 0)
print(tostring(nombre) .. "/" .. tostring(nombre) .. " contrôles passés")

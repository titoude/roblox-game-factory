banc.demarrer_serveur()
local j = banc.joueur(1, "Validation")
local client = banc.client(j)
local R = banc.instance("ReplicatedStorage.JeuRemotes")
local A = banc.require("ServerScriptService.Jeu.ActionsDeTest")
local p = A.profil(j)
local function envoyer(remote, ...)
    client:envoyer(remote, ...)
end
for _, remote in {R.VitreFinie, R.Acheter, R.Action, R.Etat, R.Effet} do
    for _, args in {{}, {false, {}}, {{}, false}, {0/0, math.huge}, {-1, -1}, {1e20, 6}} do
        envoyer(remote, table.unpack(args))
        banc.egal(p.pieces, 0, remote.Name .. " mauvais arguments sans crédit")
        banc.egal(p.tour.rangees, 0, "tour intacte")
    end
end
banc.avancer(1)
A.studioPieces(p, 10000)
for _ = 1, 20 do envoyer(R.Acheter, "robot", "r1") end
banc.egal(p.robots.r1.achetes, 5, "cinq achats par seconde")
banc.avancer(1)
for _ = 1, 20 do envoyer(R.Action, "descendre") end
local avant = p.pieces
for _ = 1, 20 do envoyer(R.VitreFinie, 1, 1) end
banc.egal(p.pieces, avant, "hors nacelle refusé")
local V = banc.require("ServerScriptService.Jeu.VitresService")
envoyer(R.Action, "monter")
banc.egal(select(2, V.position(j)), "place", "troisième action refusée malgré montée possible")
banc.avancer(1)
envoyer(R.Action, "monter")
banc.egal(select(2, V.position(j)), "tour", "montée acceptée après expiration de la cadence")
avant = p.pieces
banc.studio(false)
local temps = p.temps_jeu
for _, appel in {
    function() return A.studioPieces(p, 9e15) end,
    function() return A.studioAvance(p, 100) end,
    function() return A.studioPalier(p, "r10", 10) end,
    function() return A.studioTour(p, 3, 10) end,
    function() return A.studioAbsence(p, 7200) end,
    function() return A.studioJourSuivant(p) end,
    function() return A.studioQuota(p, "mousse_s", 600) end,
    function() return A.studioEtincelante(p) end,
} do banc.egal(appel(), false, "action de test inerte") end
banc.egal(A.studioJoueurFictif(), nil, "joueur fictif inerte")
banc.egal(A.profil(j), nil, "profil de test inaccessible")
banc.egal(p.pieces, avant, "solde intact hors Studio")
banc.egal(p.temps_jeu, temps, "horloge intacte hors Studio")

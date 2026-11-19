banc.demarrer_serveur()
local j = banc.joueur(101, "Annexe")
local client = banc.client(j)
local remotes = banc.instance("ReplicatedStorage.JeuRemotes")
local function etat()
    local messages = client:messages(remotes.Etat)
    return messages[#messages][1]
end
local vitres, etage60, precedent = 0, 0, 0
local soldes = {[25] = 10, [41] = 12.40, [56] = 16.70}
for t = 1, 180 do
    banc.avancer(1)
    if t >= 6 and t % 2 == 0 then
        local a = etat().tour.vitre_attribuee
        banc.verifier(a ~= nil, "vitre attribuée " .. t)
        client:envoyer(remotes.VitreFinie, a.rangee, a.index)
        vitres += 1
    end
    if soldes[t] then
        banc.proche(etat().pieces, soldes[t], 1e-8, "solde avant achat " .. t)
        client:envoyer(remotes.Acheter, "robot", "r1")
    end
    local e = etat()
    banc.verifier(e.tour.rangees >= precedent, "compteur monotone " .. t)
    precedent = e.tour.rangees
    if t == 60 then
        banc.egal(vitres, 28, "28 vitres à 60 s")
        banc.egal(e.tour.rangees, 5, "5 rangées à 60 s")
        etage60 = e.tour.rangees
    end
end
banc.egal(vitres, 88, "88 vitres à 180 s")
banc.egal(etat().tour.rangees - etage60, 12, "12 étages nouveaux")

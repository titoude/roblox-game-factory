local E = banc.require("ServerScriptService.Jeu.EconomieService")
local S = banc.require("ServerScriptService.Jeu.EtatJoueur")
local A = banc.require("ServerStorage.Tests.Attendus")
for id, prix in A.prix do for n, attendu in prix do banc.egal(E.prix_robot(id, n), attendu, id .. " exemplaire " .. n) end end
banc.egal(E.prix_robot("r10", 10), 7931566754660, "dixième r10")
local p = S.nouveau()
E.crediter(p, 9e15)
banc.verifier(not E.acheter_robot(p, "r2"), "verrou r2")
for _ = 1, 3 do banc.verifier(E.acheter_robot(p, "r1"), "achat r1") end
banc.egal(p.robots.r1.en_service, 3, "chantier nul immédiat")
for _ = 1, 3 do E.acheter_robot(p, "r2") end
E.acheter_robot(p, "r3")
banc.verifier(not E.jalon(p, "contrats"), "jalon refuse chantier")
p.pieces = 0
E.avancer(p, 9.5)
banc.egal(p.robots.r3.en_service, 0, "avant échéance")
local avant = p.pieces
E.avancer(p, 1)
banc.proche(p.pieces - avant, 6.75 + 6, 0.01, "mise en service à la demi-seconde")
banc.verifier(E.jalon(p, "contrats"), "jalon en service")
E.avancer(p, 20)
banc.egal(p.robots.r3.en_service, 1, "pas de double service")
for _, g in A.economie.generateurs do p.robots[g.id] = {achetes = 10, en_service = 10, chantiers = {}} end
for _, a in A.economie.ameliorations do p.ameliorations[a.id] = true end
banc.proche(E.revenu(p), 300757992117.1875, 0.001, "R composé une fois")
banc.proche(E.gain_vitre(p), 3 * (1.875 + 0.2 * E.revenu(p)), 0.001, "gain indexé")
banc.verifier(E.fleche_ouverte(p), "équipement complet")
p.pieces = 2^31; E.crediter(p, 100); banc.egal(p.pieces, 2^31 + 100, "double au-delà de int32")
E.crediter(p, 9e15); banc.egal(p.pieces, 9e15, "plafond")
for _, duree in {0, 1, 7199, 7200, 7201} do
    local q = S.nouveau(); q.robots.r1 = {achetes = 2, en_service = 1, chantiers = {0.5}}
    banc.proche(E.hors_ligne(q, duree), math.min(duree, 7200) * 0.125, 1e-9, "hors ligne " .. duree)
    banc.egal(q.robots.r1.en_service, if duree > 0 then 2 else 1, "chantiers pendant absence")
end
for _, brut in {false, 3, "faux", {pieces = 0/0, robots = false, tour = {numero = -8, masque = 100}}} do
    local q = S.valider(brut)
    banc.egal(q.version, 1, "profil réparable")
    banc.verifier(q.pieces == q.pieces and q.tour.masque <= 31, "profil borné")
end
banc.verifier(E.objectif(S.nouveau()).texte_cle ~= nil, "toujours un objectif")
local sauvegarde = S.nouveau()
sauvegarde.passes.motorisee = true; sauvegarde.mesures.etapes.arrivee = true
sauvegarde.tour.masque = 21
sauvegarde.operations = {"op1"}
local recharge = S.valider(sauvegarde)
banc.egal(recharge.passes.motorisee, true, "passes typées conservées avant relecture")
banc.egal(recharge.mesures.etapes.arrivee, true, "mesures conservées")
banc.egal(recharge.tour.masque, 21, "masque conservé")
banc.egal(recharge.operations[1], "op1", "opérations conservées")
for _, a in A.economie.ameliorations do
    local verrou = S.nouveau(); verrou.pieces = 9e15
    banc.verifier(not E.acheter_amelioration(verrou, a.id), "amélioration verrouillée " .. a.id)
    local id, n = string.match(a.debloque, "(r%d+)>=(%d+)")
    verrou.robots[id] = {achetes = tonumber(n), en_service = tonumber(n), chantiers = {}}
    banc.verifier(E.acheter_amelioration(verrou, a.id), "amélioration déverrouillée " .. a.id)
    banc.verifier(not E.acheter_amelioration(verrou, a.id), "amélioration unique " .. a.id)
end

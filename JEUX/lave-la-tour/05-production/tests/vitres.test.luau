local S = banc.require("ServerScriptService.Jeu.EtatJoueur")
local E = banc.require("ServerScriptService.Jeu.EconomieService")
local V = banc.require("ServerScriptService.Jeu.VitresService")
local temps = 0
V.horloge(function() return temps end)
local p, q = S.nouveau(), S.nouveau()
local a, b = {UserId = 1}, {UserId = 2}
V.inscrire(a, p); V.inscrire(b, q); V.asseoir(b, p, "tour")
local ra, ia = V.attribuer(p, a)
local rb, ib = V.attribuer(p, b)
banc.verifier(ia ~= ib, "deux laveurs distincts")
banc.verifier(not V.finir_vitre(p, a, ra, ia, temps), "trop tôt refusé")
temps = 1.5
banc.verifier(V.finir_vitre(p, b, rb, ib, temps), "visiteur finit en premier")
banc.egal(p.tour.masque, 2, "masque désordonné exact")
banc.egal(q.pieces, 1, "gain au laveur")
banc.egal(p.pieces, 0, "aucun gain propriétaire dans ce lot")
banc.verifier(V.finir_vitre(p, a, ra, ia, temps), "propriétaire finit")
banc.egal(p.tour.masque, 3, "masque composé")
local avant = p.pieces
banc.verifier(not V.finir_vitre(p, a, ra, ia, temps), "déjà propre refusée")
banc.egal(p.pieces, avant, "rejeu sans gain")
local reprise = S.migrer(p)
banc.egal(reprise.tour.masque, 3, "reprise en rangée")
V.liberer(a); V.liberer(b)
local c = {UserId = 3}
V.inscrire(c, reprise)
local _, index = V.attribuer(reprise, c)
banc.egal(index, 3, "reprise vitre sale suivante")
-- Le futur contrat consomme le même budget serveur que les tours.
local d, pp = {UserId = 4}, S.nouveau()
V.inscrire(d, pp)
for n = 1, 39 do banc.verifier(V.consommer_budget(d, temps), "budget contrat " .. n) end
local r, i = V.attribuer(pp, d)
temps += 1.5
banc.verifier(V.finir_vitre(pp, d, r, i, temps), "quarantième vitre acceptée")
local autre = S.nouveau()
V.asseoir(d, autre, "tour")
r, i = V.attribuer(autre, d)
temps += 1.5
local soldeAvant = pp.pieces
banc.verifier(not V.finir_vitre(autre, d, r, i, temps), "41e vitre refusée malgré durée valide sur autre tour")
banc.egal(pp.pieces, soldeAvant, "budget refusé sans gain")
banc.egal(autre.tour.masque, 0, "budget refusé sans masque")
V.quitter(d); V.inscrire(d, autre)
r, i = V.attribuer(autre, d); temps += 1.5
banc.verifier(not V.finir_vitre(autre, d, r, i, temps), "reconnexion ne restaure pas le budget du compte")
temps += 60
banc.verifier(V.finir_vitre(autre, d, r, i, temps), "fenêtre glissante expirée")
-- Pigeons : chaque interruption recommence les dix secondes continues.
for _, motif in {"place", "contrat", "deconnexion", "demenagement", "segment"} do
    local x, xp = {UserId = 20}, S.nouveau()
    xp.tour.rangees = 120; xp.tour.etincelante = true
    V.inscrire(x, xp)
    banc.verifier(not V.pigeons(xp), motif .. " début")
    temps += 9
    if motif == "deconnexion" then V.quitter(x); V.inscrire(x, xp)
    elseif motif == "segment" then V.annuler(xp)
    elseif motif == "demenagement" then V.annuler(xp)
    else V.asseoir(x, xp, motif); V.asseoir(x, xp, "tour") end
    banc.verifier(not V.pigeons(xp), motif .. " annulation")
    temps += 9
    banc.verifier(not V.pigeons(xp), motif .. " neuf secondes")
    temps += 1
    banc.verifier(V.pigeons(xp), motif .. " dix secondes")
    banc.egal(V.stock(xp), 100, "zone de 100 vitres")
    banc.egal(xp.tour.rangees, 120, "hauteur conservée")
    banc.egal(xp.tour.pigeons.premiere_rangee, 101, "vingt étages du haut")
    V.quitter(x)
end
local f = S.nouveau()
f.pieces = 9e15
banc.verifier(not E.acheter_segment(f, "interdit"), "Flèche sans équipement refusée")
banc.verifier(not V.demenager(f, "verrou"), "tour suivante non prête")
f.robots.r5 = {achetes = 1, en_service = 1, chantiers = {}}
banc.verifier(V.demenager(f, "voyage"), "déménagement")
banc.egal(f.tour.numero, 2, "nouvelle tour")
banc.egal(V.stock(f), 1400, "nouvelle tour entièrement sale")
-- La prochaine tour est ouverte : seul l'identifiant rejoué doit bloquer.
f.robots.r8 = {achetes = 1, en_service = 1, chantiers = {}}
temps += 20
banc.verifier(not V.demenager(f, "voyage"), "rejeu déménagement")
banc.egal(f.tours_finies, 1, "compteur sans doublon")
banc.verifier(V.demenager(f, "voyage-suivant"), "même transition possible avec un nouvel identifiant")
banc.egal(f.tour.numero, 3, "tour suivante effectivement ouverte")
for _, rob in f.robots do rob.achetes = 10; rob.en_service = 10 end
for id in f.ameliorations do f.ameliorations[id] = true end
f.tour = {numero = 4, rangees = 0, masque = 0, etincelante = false}
banc.egal(E.prix_segment(1), 90227397635100, "prix premier segment")
banc.egal(E.prix_segment(5), 162409315743180, "prix segment plafonné")
banc.verifier(E.acheter_segment(f, "s1"), "segment un")
local solde = f.pieces
banc.verifier(not E.acheter_segment(f, "s1"), "segment rejoué")
banc.egal(f.pieces, solde, "segment sans double débit")
banc.verifier(E.acheter_segment(f, "s2"), "segment deux")
banc.verifier(not E.acheter_segment(f, "s3"), "troisième non fini refusé")
f.tour.rangees = 80; f.fleche.segments_laves = 2
temps += 20
local z = {UserId = 30}
V.inscrire(z, f); V.pigeons(f); temps += 10
banc.verifier(V.pigeons(f), "pigeons Flèche")
banc.verifier(E.acheter_segment(f, "s3"), "M12 achat conserve pigeons")
banc.egal(V.stock(f), 300, "M12 stock pigeons plus segment")
local rz = V.attribuer(f, z)
banc.egal(rz, 461, "M12 pigeons prioritaires au-dessus du toit")
banc.egal(E.record(f), 480, "record première fois seulement")
for n = 1, 100 do
    local rz2, iz = V.attribuer(f, z); temps += 1.5
    banc.verifier(V.finir_vitre(f, z, rz2, iz, temps), "M12 lavage pigeons " .. n)
end
banc.egal(E.record(f), 480, "pigeons ne changent pas record")
banc.egal(V.attribuer(f, z), 481, "M12 segment neuf ensuite")

-- Annulations par les opérations réelles, et par leur remise à zéro interne.
local voyageur, vp = {UserId = 40}, S.nouveau()
vp.tour.rangees = 120; vp.robots.r5 = {achetes = 1, en_service = 1, chantiers = {}}
V.inscrire(voyageur, vp); V.pigeons(vp); temps += 9
banc.verifier(V.demenager(vp, "annulation-voyage"), "déménagement pendant compte à rebours")
temps += 2
banc.verifier(not V.pigeons(vp), "pas de pigeons après déménagement")
banc.egal(vp.tour.pigeons, nil, "nouvelle tour sans pigeons")
local acheteur, ap = {UserId = 41}, S.nouveau()
for _, rob in ap.robots do rob.achetes = 10; rob.en_service = 10 end
for id in ap.ameliorations do ap.ameliorations[id] = true end
ap.pieces = 9e15; ap.tour.numero = 4; ap.tour.rangees = 40
ap.fleche.segments_achetes = 1; ap.fleche.segments_laves = 1
V.inscrire(acheteur, ap); V.pigeons(ap); temps += 9
banc.verifier(E.acheter_segment(ap, "annulation-segment"), "achat pendant compte à rebours")
temps += 2
banc.verifier(not V.pigeons(ap), "pas de pigeons après achat segment")
banc.egal(ap.tour.pigeons, nil, "segment neuf sans pigeons")

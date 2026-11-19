local E = banc.require("ServerScriptService.Jeu.EconomieService")
local S = banc.require("ServerScriptService.Jeu.EtatJoueur")
local A = banc.require("ServerStorage.Tests.Attendus")
local function acheter(p, id)
    return if string.sub(id, 1, 1) == "r" then E.acheter_robot(p, id) else E.acheter_amelioration(p, id)
end
for _, nom in {"actif", "lent"} do
    local p, prochain, fin = S.nouveau(), 1, nil
    local attendu = A.profils[nom]
    for t = 0, attendu.fin_s + 1 do
        E.avancer(p, 0)
        local achat = attendu.achats[prochain]
        if achat and achat.temps_s == t + 1 and achat.solde_avant_1s < achat.cout then
            local avant = p.pieces
            banc.verifier(not acheter(p, achat.id), nom .. " achat prématuré refusé " .. prochain)
            banc.egal(p.pieces, avant, "refus sans débit")
        end
        if achat and achat.temps_s == t then
            banc.verifier(acheter(p, achat.id), nom .. " achat " .. prochain)
            -- Au voisinage de zéro, l'écart absolu couvre seulement l'arrondi double.
            local difference = math.abs(p.pieces - achat.solde_apres)
            local conforme = if math.abs(achat.solde_apres) < 1e-10 then difference <= 1e-10 else difference / math.abs(achat.solde_apres) <= 1e-6
            banc.verifier(conforme, nom .. " solde après achat " .. prochain .. " différence " .. difference)
            prochain += 1
        end
        for id, instant in attendu.jalons do
            if t == instant then banc.verifier(E.jalon(p, id), nom .. " jalon " .. id) end
        end
        if E.fleche_ouverte(p) then fin = t; break end
        -- Taux du début de seconde, chantiers activés à la borne suivante.
        E.crediter(p, attendu.cadence * E.gain_vitre(p))
        E.avancer(p, 1)
    end
    banc.egal(fin, attendu.fin_s, nom .. " première fin de contenu comparée au simulateur")
    banc.egal(prochain - 1, #attendu.achats, nom .. " tous les achats")
end

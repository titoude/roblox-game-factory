--!nocheck
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local HttpService = game:GetService("HttpService")
local E = require(script.Parent.EconomieService)
local V = require(script.Parent.VitresService)
local Donnees = require(script.Parent.DonneesService).nouveau()
local Social = require(script.Parent.SocialService).nouveau()
local Contrat = require(script.Parent.ContratService).nouveau({detacher = Social.detacher})
local C = require(ReplicatedStorage.Jeu.Config)
local fermerMesures
local Mesures = require(script.Parent.MesuresService).nouveau(C, {BindToClose = function(f) fermerMesures=f end})
Mesures:demarrer()
require(script.Parent.RetoursService).nouveau(C).demarrer()
local debuts = {}
local Commerce = require(script.Parent.CommerceService).nouveau()
Commerce.demarrer()
local Tests = require(script.Parent.ActionsDeTest)
local Monde
-- Le décor reste isolé : ses erreurs ne bloquent ni les profils ni la boucle.
pcall(function()
    Monde = require(script.Parent.MondeService)
    Monde.construire()
end)
Players.PlayerRemoving:Connect(function(j) pcall(function() Monde.liberer_parcelle(j) end) end)
local dossier = ReplicatedStorage:FindFirstChild("JeuRemotes")
if not dossier then dossier = Instance.new("Folder"); dossier.Name = "JeuRemotes"; dossier.Parent = ReplicatedStorage end
local remotes = {}
for _, nom in {"VitreFinie", "Acheter", "Action", "Etat", "Effet"} do
    local remote = dossier:FindFirstChild(nom)
    if not remote then remote = Instance.new("RemoteEvent"); remote.Name = nom; remote.Parent = dossier end
    remotes[nom] = remote
end
local profils, cadences, assis = {}, {}, {}
local fermeture = false
local effets
local function effet(...)
    if effets then table.insert(effets,table.pack(...)) else remotes.Effet:FireClient(...) end
end
Tests.configurer(function(joueur) return profils[joueur] end)
local function copie(v)
    if type(v) ~= "table" then return v end
    local r = {}; for k, valeur in v do r[k] = copie(valeur) end; return r
end
local function envoyer(j)
    local p = profils[j]
    if not p then return end
    pcall(function() Monde.attribuer_parcelle(j) end)
    local objectif = E.objectif(p)
    local contexte,cible,nom = Social.contexte(j)
    if objectif.texte_cle == "objectif_demenager" then contexte="demenager";cible=nil
    elseif contexte=="" and E.jalon(p,"contrats") and not (p.contrat.prime_recue and p.contrat.jour==os.date("!%Y-%m-%d")) then contexte="contrat" end
    local destination = V.position(j) or p
    local tour = copie(destination.tour)
    local mousse, message = Social.etat(j)
    tour.etages = V.hauteur(destination) + (if destination.tour.numero == C.FLECHE.NUMERO_TOUR then C.FLECHE.ETAGE_DEBUT - 1 else 0)
    tour.etage = math.min(tour.etages, destination.tour.rangees + (if destination.tour.numero == C.FLECHE.NUMERO_TOUR then C.FLECHE.ETAGE_DEBUT else 1))
    local _, lieu = V.position(j)
    tour.vitre_attribuee = if lieu == "contrat" then Contrat.attribution(j) else V.attribution(destination, j)
    tour.lieu = lieu
    tour.contrat = copie(p.contrat)
    pcall(function()
        local visuel = copie(p.tour)
        visuel.laveurs = {}
        local total, paliers = 0, 0
        for _, r in p.robots do
            total += r.en_service
            if r.en_service > 0 then paliers += 1 end
        end
        visuel.robots_visibles = math.min(3, total)
        visuel.r2_visibles = p.robots.r2.en_service
        visuel.retard_robots = if total > 0 then math.max(0, C.ROBOTS_RETARD_ETAGES - paliers) else p.tour.rangees
        for _, laveur in Players:GetPlayers() do
            local position, endroit = V.position(laveur)
            if position == p and endroit == "tour" then table.insert(visuel.laveurs, laveur) end
        end
        Monde.mettre_a_jour(j, visuel)
    end)
    local proprietaire = j.UserId
    for joueur, profil in profils do if profil == destination then proprietaire = joueur.UserId; break end end
    local propositions = {}
    if contexte ~= "" then propositions[contexte] = true end
    remotes.Etat:FireClient(j, {pieces = p.pieces, revenu = E.revenu(p), robots = copie(p.robots), ameliorations = copie(p.ameliorations), tour = tour, proprietaire = proprietaire, objectif = objectif, bouton_achat = objectif, bouton_contextuel = propositions, cible_contextuelle = cible, nom_contextuel = nom, mousse = mousse, message = message, offres = Commerce.offres(), passes = copie(p.passes)})
end
local function cadence(j, nom, max)
    local liste = cadences[j][nom]
    local maintenant = time()
    while #liste > 0 and liste[1] <= maintenant - 1 do table.remove(liste, 1) end
    if #liste >= max then return false end
    table.insert(liste, maintenant); return true
end
local function identique(a,b)
    if type(a) ~= type(b) then return false end
    if type(a) ~= "table" then return a == b end
    for k,v in a do if not identique(v,b[k]) then return false end end
    for k in b do if a[k] == nil then return false end end
    return true
end
-- Les actions sont confirmées en mémoire ; la sauvegarde ne bloque pas le jeu.
local function executer(j,action,...)
    if not profils[j] then return false end
    effets={}
    local avant={}
    for joueur,p in profils do avant[joueur]=copie(p) end
    local ok,changement=pcall(action,j,...)
    local confirme=ok and changement
    if confirme then
        E.operation(profils[j], "action:" .. HttpService:GenerateGUID(false))
        local joueurs={}
        for joueur,p in profils do if not identique(avant[joueur],p) then table.insert(joueurs,joueur) end end
        for _,joueur in joueurs do
            Donnees.marquer(joueur)
        end
    end
    local attentes=effets;effets=nil
    if confirme then
        for _,args in attentes do remotes.Effet:FireClient(table.unpack(args,1,args.n)) end
        for joueur in profils do envoyer(joueur) end
    end
    return confirme
end
local function connecter(remote,nom,max,action)
    remote.OnServerEvent:Connect(function(j,...)
        if not profils[j] or not cadence(j,nom,max) then return end
        executer(j,action,...)
    end)
end
local function finir(j, rangee, index)
    if not assis[j] then return false end
    local p = profils[j]
    local destination = V.position(j)
    local avant = destination.tour.rangees
    local _, lieu = V.position(j)
    local ok, gain
    if lieu == "contrat" then ok = Contrat.finir(j, p, rangee, index)
    else ok, gain = V.finir_vitre(destination, j, rangee, index, time()) end
    if ok and gain then Social.finie(j, gain) end
    if ok then Mesures:etape(j, p.mesures, "premiere_action") end
    if ok and destination.tour.rangees > avant then
        effet(j, "rangee", j.UserId, {rangees = destination.tour.rangees})
        if destination.tour.rangees % 10 == 0 then effet(j, "palier", j.UserId, {rangees = destination.tour.rangees}) end
    end
    if ok and destination.tour.etincelante then effet(j, "etincelante", j.UserId, {}) end
    return ok
end
connecter(remotes.VitreFinie, "vitre", 5, finir)
connecter(remotes.Acheter, "achat", 5, function(j, genre, id)
    if type(genre) ~= "string" or type(id) ~= "string" or #id > 32 then return false end
    local p, ok = profils[j], false
    if genre == "robot" then ok = E.acheter_robot(p, id)
    elseif genre == "amelioration" then ok = E.acheter_amelioration(p, id)
    elseif genre == "segment" and #id > 0 then
        ok = E.acheter_segment(p, "segment:" .. id)
        if ok then V.annuler(p); V.attribuer(p, j) end
    end
    if ok then Mesures:etape(j, p.mesures, "premier_achat") end
    if ok then effet(j, "achat", j.UserId, {id = id}) end
    return ok
end)
connecter(remotes.Action, "action", 2, function(j, nom, cible)
    if type(nom) ~= "string" then return false end
    if cible ~= nil and (type(cible) ~= "number" or cible % 1 ~= 0 or cible < 1 or cible > 9e15) then return false end
    local p = profils[j]
    if nom == "contrat" and cible == nil then
        local ok=Contrat.ouvrir(j,p)
        if ok then assis[j]=true end
        return ok
    elseif nom == "demenager" and cible == nil and V.position(j) == p then
        local ok = V.demenager(p, HttpService:GenerateGUID(false))
        return ok
    elseif nom == "descendre" or nom == "monter" or nom == "retour" or nom == "rejoindre" or nom == "chez_visiteur" then
        local autre = if cible then Players:GetPlayerByUserId(cible) else nil
        if cible and not autre then return false end
        local ok = Social.action(j, nom, autre)
        if ok then assis[j] = nom ~= "descendre" end
        return ok
    end
    return false
end)
local function arrivee(j)
    if fermeture or profils[j] then return end
    local p = Donnees.charger(j)
    if not p then return end
    if fermeture or Players:GetPlayerByUserId(j.UserId) ~= j then Donnees.sauver(j,true); return end
    if p.mesures.premier_jour == "" then p.mesures.premier_jour = nil end
    Mesures:joueur_arrive(j, p.mesures); Mesures:etape(j, p.mesures, "arrivee")
    Commerce.inscrire(j, p)
    debuts[j] = time()
    profils[j] = p; assis[j] = true
    Donnees.marquer(j)
    cadences[j] = {vitre = {}, achat = {}, action = {}}
    V.inscrire(j, p); Social.inscrire(j, p); V.attribuer(p, j); envoyer(j)
end
Players.PlayerAdded:Connect(arrivee)
Players.PlayerRemoving:Connect(function(j)
    if profils[j] then Mesures:joueur_part(j, profils[j].mesures) end
    debuts[j] = nil
    Commerce.quitter(j); Contrat.quitter(j); Social.quitter(j); V.quitter(j); profils[j] = nil; cadences[j] = nil; assis[j] = nil
    Donnees.sauver(j, true)
end)
game:BindToClose(function()
    fermeture = true
    local joueurs = {}
    for j in profils do table.insert(joueurs, j) end
    for _, j in joueurs do
        Mesures:joueur_part(j, profils[j].mesures)
        profils[j] = nil; Commerce.quitter(j); Contrat.quitter(j); Social.quitter(j); V.quitter(j)
    end
    local limite = time() + C.DONNEES.FERMETURE_S
    local mesuresFermees = false
    task.spawn(function()
        local ok = pcall(fermerMesures)
        if not ok then warn("[Mesures] fermeture incomplete") end
        mesuresFermees = true
    end)
    if not Donnees.fermer() then warn("[Donnees] fermeture incomplete") end
    while not mesuresFermees and time() < limite do task.wait(0.05) end
end)
for _, j in Players:GetPlayers() do arrivee(j) end
task.spawn(function()
    local precedent, sauvegarde = time(), time()
    while true do
        task.wait(1)
        local maintenant = time()
        local avant = {}
        for j,p in profils do avant[j] = copie(p) end
        pcall(Social.actualiser)
        for j, p in profils do
            local ok = pcall(function()
                E.avancer(p, maintenant - precedent)
                if maintenant - debuts[j] >= 180 then Mesures:etape(j, p.mesures, "min_3") end
                if maintenant - debuts[j] >= 600 then Mesures:etape(j, p.mesures, "min_10") end
                if V.pigeons(p) then effet(j, "pigeons", j.UserId, {}) end
                local _, lieu = V.position(j)
                if lieu == "contrat" then Contrat.attribuer(j,p) else V.attribuer(V.position(j) or p, j) end
                Commerce.avancer(j, lieu == "tour" or lieu == "contrat", function(joueur)
                    local a = if lieu == "contrat" then Contrat.attribution(joueur) else V.attribution(V.position(joueur) or p,joueur)
                    return a and executer(joueur,finir,a.rangee,a.index)
                end)
                envoyer(j)
            end)
            if not ok then j:Kick("donnees_indisponibles") end
        end
        for j,p in profils do if not identique(avant[j],p) then Donnees.marquer(j) end end
        if maintenant - sauvegarde >= C.DONNEES.SAUVEGARDE_S then
            sauvegarde = maintenant
            for j in profils do
                if Donnees.a_ecrire(j) then task.spawn(function() Donnees.sauver(j) end) end
            end
        end
        precedent = maintenant
    end
end)

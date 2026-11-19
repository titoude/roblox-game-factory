-- Seat remplacé par Part : géométrie exécutée, physique non qualifiée.
local creer = Instance.new
Instance.new = function(classe, parent)
    return creer(if classe == "Seat" then "Part" else classe, parent)
end
local M = banc.require("ServerScriptService.Jeu.MondeService")
local construire = M.construire
local construction_refusee = false
M.construire = function() construction_refusee = true; error("panne construction injectée") end
banc.demarrer_serveur()
banc.verifier(construction_refusee, "construction défaillante isolée au démarrage")
M.construire = construire
local A = banc.require("ServerScriptService.Jeu.ActionsDeTest")
local V = banc.require("ServerScriptService.Jeu.VitresService")
local j = banc.joueur(801, "Laveur")
local p = A.profil(j)
local R = banc.instance("ReplicatedStorage.JeuRemotes")
local client = banc.client(j)
local parcelle = banc.instance("Workspace.MondeLaveLaTour.Parcelle1")
banc.egal(parcelle:GetAttribute("Proprietaire"), j.UserId, "arrivée attribue une parcelle")
local tour = parcelle.Tour
banc.egal(tour.Corps.Size.Y, 600, "tour construite à l'arrivée")
banc.egal(tour.Nacelle.Plancher.CFrame.Position.Y, 0.5, "nacelle à la première rangée")
for n = 1, 10 do
    banc.avancer(2)
    local a = V.attribution(p, j)
    banc.verifier(a ~= nil, "attribution " .. n)
    client:envoyer(R.VitreFinie, a.rangee, a.index)
end
banc.avancer(0.4)
banc.egal(p.tour.rangees, 2, "dix vitres donnent deux rangées")
banc.egal(tour.Propre1:GetAttribute("Hauteur"), 10, "façade suit le profil")
banc.egal(tour.Nacelle.Plancher.CFrame.Position.Y, 10.5, "nacelle suit la troisième rangée")
local autre = banc.joueur(802, "Visiteur")
autre.IsFriendsWith = function(_, id) return id == j.UserId end
local q = A.profil(autre)
q.tour.rangees = 1
banc.avancer(1)
local visiteur = banc.client(autre)
local messages = visiteur:messages(R.Etat)
local etat = messages[#messages][1]
banc.verifier(etat.bouton_contextuel.rejoindre, "proposition sociale envoyée")
banc.egal(etat.cible_contextuelle, j.UserId, "cible sociale envoyée")
banc.egal(etat.nom_contextuel, j.Name, "nom social envoyé")
visiteur:envoyer(R.Action, "rejoindre", j.UserId)
messages = visiteur:messages(R.Etat)
banc.egal(messages[#messages][1].proprietaire, j.UserId, "identifiant de la tour visitée")
local mise_a_jour, attribution = M.mettre_a_jour, M.attribuer_parcelle
local erreurs = 0
M.mettre_a_jour = function() erreurs += 1; error("panne monde injectée") end
M.attribuer_parcelle = function() erreurs += 1; error("panne attribution injectée") end
p.robots.r1 = {achetes = 1, en_service = 1, chantiers = {}}
local avant, nombre = p.pieces, #client:messages(R.Etat)
banc.avancer(3)
banc.verifier(erreurs >= 6, "erreurs monde effectivement injectées")
banc.proche(p.pieces - avant, 0.75, 1e-9, "revenu continue malgré le monde")
banc.verifier(#client:messages(R.Etat) > nombre, "Etat continue malgré le monde")
banc.egal(A.profil(j), p, "joueur conservé malgré le monde")
M.mettre_a_jour, M.attribuer_parcelle = mise_a_jour, attribution
banc.quitter(j)
banc.egal(parcelle:GetAttribute("Proprietaire"), nil, "parcelle libérée au départ")
banc.egal(parcelle:FindFirstChild("Tour"), nil, "tour libérée au départ")
Instance.new = creer

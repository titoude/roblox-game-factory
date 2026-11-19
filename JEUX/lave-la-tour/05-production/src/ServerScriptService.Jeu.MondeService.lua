--!nocheck
local C = require(game:GetService("ReplicatedStorage").Jeu.Config)
local Monde = {}
-- À remonter dans Config : étage 5, côtés 35/55/75, rayon 110,
-- place 150, socle 6, montée 0,4 s ; 6 parcelles, 3 robots décoratifs maximum.
local Vector3, CFrame, Color3, TweenInfo = Vector3, CFrame, Color3, TweenInfo
local monde, parcelles, occupants = nil, {}, {}
local propre, sale = Color3.fromRGB(100, 210, 240), Color3.fromRGB(115, 90, 65)
local function journal(nom, valeur)
    if game:GetService("RunService"):IsStudio() then print(string.format("[PASSE2 Monde %.3f] %s %s", time(), nom, tostring(valeur))) end
end
local function piece(parent, nom, taille, cadre, couleur, classe)
    local p = Instance.new(classe or "Part")
    p.Name = nom; p.Size = taille; p.CFrame = cadre; p.Color = couleur
    p.Anchored = true; p.TopSurface = 0; p.BottomSurface = 0; p.Parent = parent
    return p
end
function Monde.construire()
    if monde then return monde end
    monde = Instance.new("Folder"); monde.Name = "MondeLaveLaTour"; monde.Parent = game:GetService("Workspace")
    piece(monde, "Place", Vector3.new(150, 6, 150), CFrame.new(0, -3, 0), Color3.fromRGB(150, 165, 180))
    piece(monde, "DessousPlace", Vector3.new(140, 4, 140), CFrame.new(0, -8, 0), Color3.fromRGB(65, 75, 90))
    for i = 1, 6 do
        local angle = (i-1)*math.pi/3
        local centre = Vector3.new(math.sin(angle)*110, 0, math.cos(angle)*110)
        local cadre = CFrame.lookAt(centre, Vector3.new(0, 0, 0)) * CFrame.Angles(0, math.pi, 0)
        local dossier = Instance.new("Model"); dossier.Name = "Parcelle" .. i; dossier.Parent = monde
        piece(dossier, "Socle", Vector3.new(82, 6, 82), cadre*CFrame.new(0, -3, 0), Color3.fromRGB(85, 95, 110))
        piece(dossier, "Dessous", Vector3.new(72, 4, 72), cadre*CFrame.new(0, -8, 0), Color3.fromRGB(55, 65, 80))
        parcelles[i] = {dossier=dossier, cadre=cadre}
    end
    journal("construction", Monde.nombre_de_pieces())
    return monde
end
function Monde.attribuer_parcelle(joueur)
    Monde.construire()
    if occupants[joueur] then return occupants[joueur].dossier end
    for _, p in parcelles do
        if not p.joueur then
            p.joueur = joueur; occupants[joueur] = p
            p.dossier:SetAttribute("Proprietaire", joueur.UserId)
            p.tour = Instance.new("Model"); p.tour.Name = "Tour"; p.tour.Parent = p.dossier
            p.corps = piece(p.tour, "Corps", Vector3.new(35, 600, 35), p.cadre*CFrame.new(0, 300, 0), Color3.fromRGB(55, 65, 80))
            p.panneaux = {}
            for face = 1, 4 do
                local paire = {}
                for _, nom in {"Propre", "Sale"} do
                    paire[nom] = piece(p.tour, nom .. face, Vector3.new(25, 1, 0.2), p.cadre, if nom == "Propre" then propre else sale)
                end
                p.panneaux[face] = paire
            end
            p.vitres = {}
            for i = 1, 5 do
                p.vitres[i] = piece(p.tour, "Vitre" .. i, Vector3.new(5, 5, 0.3), p.cadre, sale)
                p.vitres[i]:SetAttribute("Index", i)
            end
            p.nacelle = Instance.new("Model"); p.nacelle.Name = "Nacelle"; p.nacelle.Parent = p.tour
            p.plancher = piece(p.nacelle, "Plancher", Vector3.new(27, 1, 5), p.cadre, Color3.fromRGB(225, 185, 65))
            p.dessous = piece(p.nacelle, "DessousNacelle", Vector3.new(24, 0.7, 4), p.cadre, Color3.fromRGB(95, 80, 45))
            p.sieges = {}
            for i = 1, 2 do p.sieges[i] = piece(p.nacelle, "Siege" .. i, Vector3.new(2, 1, 2), p.cadre, propre, "Seat") end
            p.borne = piece(p.tour, "Borne", Vector3.new(2, 4, 2), p.cadre*CFrame.new(0, 2, 28), propre)
            p.toit = piece(p.tour, "Toit", Vector3.new(37, 2, 37), p.cadre, propre)
            -- Trois silhouettes simples suffisent au prototype r1/r2 ; aucun catalogue.
            p.robots = {}
            for i = 1, 3 do p.robots[i] = piece(p.tour, "Robot" .. i, Vector3.new(2, 2, 1), p.cadre, propre) end
            Monde.mettre_a_jour(joueur, {numero=1, rangees=0, masque=0})
            return p.dossier
        end
    end
    return nil
end
function Monde.mettre_a_jour(joueur, etat)
    local p = occupants[joueur]
    if not p then return end
    local numero = math.clamp(etat.numero or 1, 1, 3)
    local etages = etat.etages or C.TOURS[numero].etages
    local hauteur, cote = etages*5, ({35,55,75})[numero]
    local rangees = math.clamp(etat.rangees or 0, 0, etages)
    local rang = math.min(etages, rangees+1)
    p.corps.Size = Vector3.new(cote, hauteur, cote); p.corps.CFrame = p.cadre*CFrame.new(0, hauteur/2, 0)
    p.toit.Size = Vector3.new(cote+2, 2, cote+2); p.toit.CFrame = p.cadre*CFrame.new(0, hauteur+1, 0)
    for face, paire in p.panneaux do
        local h = rangees*5
        if face > 1 then h = math.max(0, rangees-(etat.retard_robots or C.ROBOTS_RETARD_ETAGES))*5 end
        local faceCadre = p.cadre*CFrame.Angles(0, (face-1)*math.pi/2, 0)
        for _, nom in {"Propre", "Sale"} do
            local taille = if nom == "Propre" then h else hauteur-h
            local y = if nom == "Propre" then h/2 else h+(hauteur-h)/2
            local panneau = paire[nom]
            panneau:SetAttribute("Hauteur", taille)
            panneau.Size = Vector3.new(25, math.max(0.05, taille), 0.2)
            panneau.Transparency = if taille == 0 then 1 else 0
            panneau.CFrame = faceCadre*CFrame.new(0, y, cote/2+0.12)
        end
    end
    for i, vitre in p.vitres do
        vitre.CFrame = p.cadre*CFrame.new((i-3)*5, (rang-0.5)*5, cote/2+0.4)
        vitre.Color = if rangees == etages or bit32.band(etat.masque or 0, 2^(i-1)) ~= 0 then propre else sale
        vitre:SetAttribute("Rangee", rang)
    end
    local y, z = (rang-1)*5+0.5, cote/2+4
    local positions = {[p.plancher]=CFrame.new(0,y,z), [p.dessous]=CFrame.new(0,y-0.85,z),
        [p.sieges[1]]=CFrame.new(-3,y+1,z), [p.sieges[2]]=CFrame.new(3,y+1,z)}
    if p.rang ~= rang then journal("montee", rang) end
    for objet, localCadre in positions do
        local cible = p.cadre*localCadre*CFrame.Angles(0, math.pi, 0)
        if p.rang and p.rang ~= rang then
            game:GetService("TweenService"):Create(objet, TweenInfo.new(0.4), {CFrame=cible}):Play()
        else objet.CFrame = cible end
    end
    p.rang = rang
    local laveurs = etat.laveurs or (if etat.vitre_attribuee then {joueur} else {})
    for i, laveur in laveurs do
        if i > 2 then break end
        local personnage = laveur.Character
        local humain = personnage and personnage:FindFirstChildOfClass("Humanoid")
        if humain and not humain.Sit then p.sieges[i]:Sit(humain) end
    end
    for i, robot in p.robots do
        robot.Transparency = if i <= (etat.robots_visibles or 0) then 0 else 1
        robot.Size = if i==3 and (etat.r2_visibles or 0)>0 then Vector3.new(1,1,20) else Vector3.new(2,2,1)
        robot.CFrame = p.cadre*CFrame.new(cote/2+0.7, math.max(2, (rangees-1)*5)+i+math.sin(time()*2+i), 8-i*5)
    end
end
function Monde.liberer_parcelle(joueur)
    local p = occupants[joueur]
    if not p then return end
    p.tour:Destroy(); p.dossier:SetAttribute("Proprietaire", nil)
    p.joueur = nil; p.tour = nil; p.rang = nil; occupants[joueur] = nil
end
function Monde.nombre_de_pieces()
    local n = 0
    if monde then for _, objet in monde:GetDescendants() do if objet:IsA("BasePart") then n += 1 end end end
    return n
end
return Monde

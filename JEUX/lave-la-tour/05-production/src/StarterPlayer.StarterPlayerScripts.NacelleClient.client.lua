--!nocheck
local Players = game:GetService("Players")
local RS = game:GetService("ReplicatedStorage")
local Run = game:GetService("RunService")
local UIS = game:GetService("UserInputService")
local Vector2, Vector3, CFrame, Enum = Vector2, Vector3, CFrame, Enum
local joueur = Players.LocalPlayer
local G = require(RS:WaitForChild("Jeu"):WaitForChild("GesteLogique"))
local remotes = RS:WaitForChild("JeuRemotes")
local scripts = joueur:WaitForChild("PlayerScripts")
local bus = Instance.new("Folder"); bus.Name = "NacelleLocale"; bus.Parent = scripts
for _, nom in {"Geste", "Confirme", "Commande"} do
    local signal = Instance.new("BindableEvent"); signal.Name = nom; signal.Parent = bus
end
-- PlayerModule peut manquer (places récentes, contrôleur de personnage par défaut) : premier Play réel
-- du 17/11/2026, le script restait bloqué sur WaitForChild. Repli : avaler déplacement et saut.
local function controles_de_repli()
    local CAS = game:GetService("ContextActionService")
    local function avaler() return Enum.ContextActionResult.Sink end
    return {
        Disable = function()
            CAS:BindActionAtPriority("LaveLaTourBloque", avaler, false, Enum.ContextActionPriority.High.Value + 1,
                Enum.PlayerActions.CharacterForward, Enum.PlayerActions.CharacterBackward, Enum.PlayerActions.CharacterLeft,
                Enum.PlayerActions.CharacterRight, Enum.PlayerActions.CharacterJump, Enum.KeyCode.Space, Enum.KeyCode.ButtonA,
                Enum.KeyCode.Thumbstick1)
        end,
        Enable = function() CAS:UnbindAction("LaveLaTourBloque") end,
    }
end
local modulePlayer = scripts:WaitForChild("PlayerModule", 5)
local okControles, controles = false, nil
if modulePlayer then okControles, controles = pcall(function() return require(modulePlayer):GetControls() end) end
if not okControles or not controles then controles = controles_de_repli() end
local camera = game:GetService("Workspace").CurrentCamera
local controlesMasques = false
local attribution, etat, envoi, geste, passes = nil, nil, nil, nil, 0
local recue, derniereDemande, reculJusqua, reculAttente = 0, 0, 0, false
local descendu = false
local function journal(nom, valeur)
    if Run:IsStudio() then print(string.format("[PASSE2 Nacelle %.3f] %s %s", time(), nom, tostring(valeur or ""))) end
end
local function vitre_courante()
    if not attribution then return nil end
    local monde = game:GetService("Workspace"):FindFirstChild("MondeLaveLaTour")
    if not monde then return nil end
    for _, parcelle in monde:GetChildren() do
        if parcelle:GetAttribute("Proprietaire") == (etat.proprietaire or joueur.UserId) then
            local tour = parcelle:FindFirstChild("Tour")
            return tour and tour:FindFirstChild("Vitre" .. attribution.index)
        end
    end
    return nil
end
local function assise(active)
    if active == controlesMasques then return end
    controlesMasques = active; bus:SetAttribute("Assis", active)
    if active then controles:Disable(); camera.CameraType = Enum.CameraType.Scriptable
    else
        controles:Enable(); camera.CameraType = Enum.CameraType.Custom
        local personnage = joueur.Character
        local humain = personnage and personnage:FindFirstChildOfClass("Humanoid")
        if humain then camera.CameraSubject = humain; humain.Sit = false end
    end
    local touch = joueur.PlayerGui:FindFirstChild("TouchGui")
    if touch then touch.Enabled = not active end
end
bus.Commande.Event:Connect(function(nom)
    if nom == "descendre" then descendu = true; geste = nil; assise(false)
    elseif nom == "monter" or nom == "retour" then descendu = false end
end)
remotes.Etat.OnClientEvent:Connect(function(nouveau)
    if type(nouveau) ~= "table" or type(nouveau.tour) ~= "table" then return end
    local tour = nouveau.tour
    if envoi and etat and tour.numero == etat.tour.numero then
        local masque = tour.masque or 0
        if tour.rangees >= envoi.rangee or (tour.rangees+1 == envoi.rangee and bit32.band(masque, 2^(envoi.index-1)) ~= 0) then
            journal("vitre_finie", tostring(envoi.rangee) .. ":" .. envoi.index)
            bus.Confirme:Fire(envoi.rangee, envoi.index); envoi = nil
        end
    end
    local a = tour.vitre_attribuee
    if not a or not attribution or a.rangee ~= attribution.rangee or a.index ~= attribution.index then
        attribution = a; passes = 0; recue = time(); envoi = nil
        -- Ne pas bloquer le toucher suivant pendant les 0,4 s de montée.
    end
    etat = nouveau
    if tour.lieu then descendu = tour.lieu == "place" end
    assise(not descendu)
end)
remotes.Effet.OnClientEvent:Connect(function(nom, id, details)
    if id == joueur.UserId and (nom == "palier" or (nom == "achat" and details and string.sub(details.id or "",1,1) == "r")) then reculAttente = true end
end)
local function position_ecran(position)
    local inset = game:GetService("GuiService"):GetGuiInset()
    return Vector2.new(position.X-inset.X, position.Y-inset.Y)
end
local function cadrage(vitre)
    local largeur, xmin, xmax = 0, math.huge, -math.huge
    for _, x in {-2.5,2.5} do
        for _, y in {-2.5,2.5} do
            local p = camera:WorldToViewportPoint(vitre.CFrame*Vector3.new(x,y,0))
            xmin = math.min(xmin,p.X); xmax = math.max(xmax,p.X)
        end
    end
    largeur = xmax-xmin
    return largeur
end
UIS.InputBegan:Connect(function(input, traite)
    if traite or not controlesMasques or geste or passes >= 3 then return end
    if input.UserInputType ~= Enum.UserInputType.Touch and input.UserInputType ~= Enum.UserInputType.MouseButton1 then return end
    local vitre = vitre_courante()
    if not vitre then return end
    local p = position_ecran(input.Position)
    -- Intersection du rayon avec le plan de la vitre attribuée uniquement.
    local rayon = camera:ViewportPointToRay(p.X,p.Y)
    local normal = vitre.CFrame.LookVector
    local denom = rayon.Direction:Dot(normal)
    if math.abs(denom) < 0.001 then return end
    local distance = (vitre.Position-rayon.Origin):Dot(normal)/denom
    if distance <= 0 then return end
    local localP = vitre.CFrame:PointToObjectSpace(rayon.Origin+rayon.Direction*distance)
    if math.abs(localP.X)>2.5 or math.abs(localP.Y)>2.5 then return end
    geste = {input=input, debut=time(), positions={{x=p.X,y=p.Y}}, largeur=cadrage(vitre),
        cadre=camera.CFrame, rangee=attribution.rangee, index=attribution.index}
    journal("contact", tostring(attribution.rangee) .. ":" .. attribution.index)
    bus.Geste:Fire("contact", p, geste.debut)
end)
UIS.InputChanged:Connect(function(input)
    if not geste then return end
    if input == geste.input or (geste.input.UserInputType == Enum.UserInputType.MouseButton1 and input.UserInputType == Enum.UserInputType.MouseMovement) then
        local p = position_ecran(input.Position)
        if #geste.positions < 512 then table.insert(geste.positions,{x=p.X,y=p.Y}) end
        bus.Geste:Fire("trace",p,geste.debut)
    end
end)
UIS.InputEnded:Connect(function(input)
    if not geste or input ~= geste.input then return end
    local g = geste; geste = nil
    bus.Geste:Fire("fin")
    if attribution and attribution.rangee == g.rangee and attribution.index == g.index then
        passes = G.ajouter_passe(passes, G.passe(g.positions,g.largeur,time()-g.debut))
        journal("passe", passes)
        bus.Geste:Fire("passe",passes)
    end
end)
UIS.WindowFocusReleased:Connect(function() geste = nil; bus.Geste:Fire("fin") end)
joueur:WaitForChild("PlayerGui").ChildAdded:Connect(function(enfant)
    if enfant.Name=="TouchGui" and controlesMasques then enfant.Enabled=false end
end)
local fpsTemps, images, precedent = 0, 0, nil
Run:BindToRenderStep("LaveLaTourCamera", Enum.RenderPriority.Camera.Value+1, function(dt)
    images += 1; fpsTemps += dt
    if fpsTemps >= 1 then journal("fps", images/fpsTemps); images=0; fpsTemps=0 end
    if not controlesMasques then return end
    local vitre = vitre_courante()
    if not vitre then return end
    camera = game:GetService("Workspace").CurrentCamera
    camera.CameraType = Enum.CameraType.Scriptable
    if geste then
        if camera.CFrame.LookVector:Dot(geste.cadre.LookVector) < 0.99999 then journal("rotation_camera_constatee", "pendant_contact") end
        camera.CFrame = geste.cadre
    else
        if reculAttente then reculJusqua = time()+2; reculAttente=false end
        local calcul = G.camera({x=0,y=0,z=0},camera.ViewportSize.X,camera.ViewportSize.Y)
        local recul = if time()<reculJusqua then math.max(1, (etat.tour.etages*5)/calcul.distance) else 1
        local cible = vitre.Position
        local position = vitre.CFrame*Vector3.new(calcul.x*recul,calcul.y*recul,calcul.z*recul)
        local cadre = CFrame.lookAt(position,cible)
        -- Interpolation uniquement à la montée ; jamais un verrou de saisie.
        camera.CFrame = if precedent and precedent ~= attribution.rangee then camera.CFrame:Lerp(cadre,math.min(1,dt/0.04)) else cadre
        precedent = attribution.rangee
    end
    camera.FieldOfView = G.FOV
    if passes >= 3 and time()-recue >= 1.55 and time()-derniereDemande >= 0.5 then
        envoi = {rangee=attribution.rangee,index=attribution.index}
        remotes.VitreFinie:FireServer(envoi.rangee,envoi.index); derniereDemande=time()
    end
end)
journal("pret", "saisie_sans_gain_client")

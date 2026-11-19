--!nocheck
local Players = game:GetService("Players")
local RS = game:GetService("ReplicatedStorage")
local Run = game:GetService("RunService")
local UDim2, Vector2, Color3 = UDim2, Vector2, Color3
local joueur = Players.LocalPlayer
local modules = RS:WaitForChild("Jeu")
local T = require(modules:WaitForChild("Textes"))
local N = require(modules:WaitForChild("Nombres"))
local C = require(modules:WaitForChild("Config"))
local G = require(modules:WaitForChild("GesteLogique"))
local remotes = RS:WaitForChild("JeuRemotes")
local bus = joueur:WaitForChild("PlayerScripts"):WaitForChild("NacelleLocale")
local langue = joueur.LocaleId
local function t(cle, ...) return T.t(langue,cle,...) end
local function journal(nom,valeur)
    if Run:IsStudio() then print(string.format("[PASSE2 Interface %.3f] %s %s",time(),nom,tostring(valeur or ""))) end
end
local gui = Instance.new("ScreenGui"); gui.Name="InterfaceLaveLaTour"; gui.ResetOnSpawn=false; gui.Parent=joueur:WaitForChild("PlayerGui")
local function element(nom,classe,x,y,w,h,texte)
    local o=Instance.new(classe); o.Name=nom; o.Position=UDim2.fromScale(x,y); o.Size=UDim2.fromScale(w,h)
    o.BackgroundColor3=Color3.fromRGB(235,240,245); o.TextColor3=Color3.fromRGB(20,30,45)
    o.TextSize=16; o.TextWrapped=true; o.Text=texte; o.Parent=gui
    local borne=Instance.new("UISizeConstraint"); borne.MinSize=Vector2.new(48,if classe=="TextButton" then 48 else 24)
    borne.MaxSize=Vector2.new(300,if classe=="TextButton" then 64 else 48); borne.Parent=o
    return o
end
local pieces=element("Pieces","TextLabel",0.02,0.03,0.23,0.08,t("pieces","0"))
local revenu=element("Revenu","TextLabel",0.02,0.12,0.23,0.07,t("revenu","0"))
local etage=element("Etage","TextLabel",0.37,0.03,0.26,0.08,t("etage","1","120"))
local message=element("Message","TextLabel",0.31,0.12,0.38,0.08,"")
local objectif=element("Objectif","TextLabel",0.32,0.90,0.36,0.08,"")
local achat=element("Achat","TextButton",0.37,0.74,0.26,0.13,"")
-- Le gabarit RetoursClient possède son bouton en (0,02 ; 0,55).
-- Réserver sa zone ; Descendre est juste à sa droite, sans déplacer son GUI.
local descendre=element("Descendre","TextButton",0.19,0.55,0.12,0.13,t("descendre"))
local contexte=element("Contexte","TextButton",0.76,0.45,0.22,0.13,"")
local aide=element("Aide","TextLabel",0.37,0.23,0.26,0.08,t("frotte"))
local main=element("MainFantome","TextLabel",0.47,0.43,0.06,0.09,t("main")); main.BackgroundTransparency=1
-- Centrer par ancrage : la borne maximale en pixels ne décale pas le HUD PC.
for _, o in {etage,message,objectif,achat,aide,main} do
    o.AnchorPoint=Vector2.new(0.5,0); o.Position=UDim2.fromScale(0.5,o.Position.Y.Scale)
end
contexte.AnchorPoint=Vector2.new(1,0); contexte.Position=UDim2.fromScale(0.98,0.45)
achat.Visible=false; contexte.Visible=false; message.Visible=false
local courant, action, premiere = nil,nil,false
local celebration, celebrationFin = "",0
remotes.Effet.OnClientEvent:Connect(function(nom,id,details)
    if nom=="palier" and id==joueur.UserId then celebration=t("palier",tostring(details.rangees)); celebrationFin=time()+1.5 end
end)
achat.Activated:Connect(function()
    if not courant then return end
    local b=courant.bouton_achat
    if not b then return end
    local genre=({objectif_robot="robot",objectif_amelioration="amelioration",objectif_segment="segment"})[b.texte_cle]
    if genre then remotes.Acheter:FireServer(genre,tostring(b.cible)) end
end)
contexte.Activated:Connect(function()
    if action then
        bus.Commande:Fire(action)
        remotes.Action:FireServer(action,if courant then courant.cible_contextuelle else nil)
    end
end)
descendre.Activated:Connect(function() bus.Commande:Fire("descendre"); remotes.Action:FireServer("descendre") end)
bus.Confirme.Event:Connect(function() premiere=true; aide.Visible=false; main.Visible=false end)
remotes.Etat.OnClientEvent:Connect(function(e)
    if type(e)~="table" or not e.tour then return end
    courant=e
    pieces.Text=t("pieces",N.abreger(e.pieces,langue)); revenu.Text=t("revenu",N.abreger(e.revenu,langue))
    etage.Text=t("etage",tostring(e.tour.etage),tostring(e.tour.etages))
    journal("etage",e.tour.etage)
    local b=e.bouton_achat
    if b then
        local cible=t(tostring(b.cible))
        objectif.Text=t(b.texte_cle,cible)
        local genre=({objectif_robot="robot",objectif_amelioration="amelioration",objectif_segment="segment"})[b.texte_cle]
        achat.Visible=genre~=nil
        local prix=nil
        local liste=if genre=="robot" then C.generateurs else C.ameliorations
        for _, definition in liste do
            if definition.id==b.cible then
                prix=if genre=="robot" then math.ceil(definition.cout*definition.croissance_cout^e.robots[b.cible].achetes) else definition.cout
            end
        end
        achat.Text=if genre then t("achat_"..genre,if prix then N.abreger(prix,langue) else cible) else ""
    end
    local disponibles={}
    if type(e.bouton_contextuel)=="table" then disponibles=e.bouton_contextuel
    elseif e.bouton_contextuel and e.bouton_contextuel~="" then disponibles[e.bouton_contextuel]=true end
    if bus:GetAttribute("Assis")==false then disponibles.monter=true end
    action=G.contextuel(disponibles); contexte.Visible=action~=nil
    if action then contexte.Text=t(action,e.nom_contextuel or "") end
    descendre.Visible=bus:GetAttribute("Assis")~=false
    message.Text=if e.message and e.message~="" then t(e.message) else ""
    message.Visible=message.Text~=""
    if (e.tour.rangees or 0)>0 or (e.tour.masque or 0)~=0 then premiere=true end
    aide.Visible=not premiere; main.Visible=not premiere
end)
Run.RenderStepped:Connect(function()
    if main.Visible then main.Rotation=math.sin(time()*3)*18 end
    if courant then
        local texte=if courant.message and courant.message~="" then t(courant.message) elseif time()<celebrationFin then celebration else ""
        message.Text=texte; message.Visible=texte~=""
    end
end)
journal("pret","HUD_fixe")

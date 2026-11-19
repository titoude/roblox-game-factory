--!nocheck
local Players = game:GetService("Players")
local RS = game:GetService("ReplicatedStorage")
local Run = game:GetService("RunService")
local Tween = game:GetService("TweenService")
local UDim2, Vector2, Vector3, CFrame, Color3, TweenInfo, Enum = UDim2, Vector2, Vector3, CFrame, Color3, TweenInfo, Enum
local joueur = Players.LocalPlayer
local G = require(RS:WaitForChild("Jeu"):WaitForChild("GesteLogique"))
local bus = joueur:WaitForChild("PlayerScripts"):WaitForChild("NacelleLocale")
local remotes = RS:WaitForChild("JeuRemotes")
-- À remonter dans Config : 32 traces, 12 éclats, vie 0,35/0,6 s.
local gui=Instance.new("ScreenGui"); gui.Name="EffetsLaveLaTour"; gui.ResetOnSpawn=false; gui.Parent=joueur:WaitForChild("PlayerGui")
local function journal(nom,valeur)
    if Run:IsStudio() then print(string.format("[PASSE2 Effets %.3f] %s %s",time(),nom,tostring(valeur or ""))) end
end
local sons={}
for _, nom in {"Raclette","Etincelle","Piece","Achat","Mousse","Rangee","Palier","Pigeons"} do
    local s=Instance.new("Sound"); s.Name="AccrocheSon"..nom; s.SoundId=""; s.Volume=0.4; s.Looped=false; s.Parent=gui; sons[nom]=s
end
local function son(nom,vitesse)
    local s=sons[nom]; s.PlaybackSpeed=vitesse or 1
    if s.SoundId~="" then s:Stop(); s:Play() end
end
local function carre(nom,couleur)
    local f=Instance.new("Frame"); f.Name=nom; f.BackgroundColor3=couleur; f.BorderSizePixel=0; f.Visible=false; f.Parent=gui; return f
end
-- Réserve fixe, réutilisée : aucune accumulation d'instances pendant le lavage.
local traces, eclats={},{}
for i=1,32 do traces[i]=carre("Trace"..i,Color3.fromRGB(130,235,255)) end
for i=1,12 do eclats[i]=carre("Eclat"..i,Color3.fromRGB(255,225,70)) end
local rideau=carre("RideauEau",Color3.fromRGB(150,225,255))
local mousse=carre("Mousse",Color3.fromRGB(225,255,245))
local variantes={}
local pigeons={}
local oiseauxFin=0
local centreOiseaux=Vector3.new(0,0,0)
for i=1,3 do
    local o=Instance.new("Part"); o.Name="PigeonLocal"..i; o.Size=Vector3.new(1.8,0.25,0.6)
    o.Anchored=true; o.CanCollide=false; o.CanQuery=false; o.Transparency=1
    o.Color=Color3.fromRGB(160,165,175); o.Parent=game:GetService("Workspace"); pigeons[i]=o
end
local prochaine, cran, derniere, contact, position = 0,0,nil,nil,Vector2.new(0,0)
local function trace(p)
    position=p; prochaine=prochaine%32+1
    local f=traces[prochaine]; f.Position=UDim2.fromOffset(p.X-16,p.Y-4); f.Size=UDim2.fromOffset(32,8)
    f.BackgroundTransparency=0.3; f.Visible=true
    f:SetAttribute("Fin",time()+0.35)
end
bus.Geste.Event:Connect(function(nom,p,debut)
    if nom=="contact" then contact=debut; trace(p); son("Raclette")
    elseif nom=="trace" then trace(p)
    elseif nom=="passe" then
        for _, surface in variantes do
            if surface.Name=="Aspectaffiche" then
                for i, lambeau in surface:GetChildren() do lambeau.Visible=i>p end
            end
        end
    elseif nom=="fin" then sons.Raclette:Stop() end
end)
bus.Confirme.Event:Connect(function(rangee,index)
    cran=G.note(cran,derniere,time()); derniere=time()
    journal("note",cran); journal("vitre_confirmee",tostring(rangee)..":"..index)
    son("Etincelle",2^((cran-1)/12)); son("Piece")
    for i,f in eclats do
        f.Position=UDim2.fromOffset(position.X,position.Y); f.Size=UDim2.fromOffset(if i==1 then 14 else 4,if i==1 then 14 else 4)
        f.Visible=true; f:SetAttribute("Fin",time()+0.6)
        local cible=if i==1 then UDim2.fromScale(0.10,0.07) else UDim2.fromOffset(position.X+math.cos(i)*50,position.Y+math.sin(i)*50)
        Tween:Create(f,TweenInfo.new(0.5),{Position=cible}):Play()
    end
end)
remotes.Effet.OnClientEvent:Connect(function(nom,id)
    if id~=joueur.UserId then return end
    journal(nom)
    if nom=="rangee" or nom=="palier" then
        rideau.Position=UDim2.fromScale(0.30,0.22); rideau.Size=UDim2.fromScale(0.40,0.04); rideau.BackgroundTransparency=0.35; rideau.Visible=true
        rideau:SetAttribute("Fin",time()+0.6)
        Tween:Create(rideau,TweenInfo.new(0.5),{Position=UDim2.fromScale(0.30,0.65)}):Play()
        son("Rangee",1); task.delay(0.12,function() son("Rangee",1.25) end)
        if nom=="palier" then
            for i=0,2 do task.delay(i*0.15,function() son("Palier",1+i*0.25) end) end
        end
    elseif nom=="achat" then son("Achat")
    elseif nom=="mousse" then
        mousse.Position=UDim2.fromScale(0.30,0.30); mousse.Size=UDim2.fromScale(0.40,0.30); mousse.BackgroundTransparency=0.7; mousse.Visible=true; mousse:SetAttribute("Fin",time()+0.6); son("Mousse")
    elseif nom=="pigeons" then
        son("Pigeons"); oiseauxFin=time()+2
        local camera=game:GetService("Workspace").CurrentCamera
        centreOiseaux=camera.CFrame.Position+camera.CFrame.LookVector*6
    elseif nom=="etincelante" then
        son("Etincelle",2)
        for i,f in eclats do
            f.Position=UDim2.fromScale(0.30+(i%4)*0.12,0.24+math.floor(i/4)*0.14)
            f.Size=UDim2.fromOffset(8,8); f.Visible=true; f:SetAttribute("Fin",time()+0.6)
        end
    end
end)
-- Les variantes sont locales et déterministes, sans changer la valeur d'une vitre.
remotes.Etat.OnClientEvent:Connect(function(e)
    if not e.tour then return end
    if e.mousse then
        mousse.Position=UDim2.fromScale(0.30,0.30); mousse.Size=UDim2.fromScale(0.40,0.30)
        mousse.BackgroundTransparency=0.85; mousse.Visible=true; mousse:SetAttribute("Fin",time()+1.1)
    end
    local monde=game:GetService("Workspace"):FindFirstChild("MondeLaveLaTour")
    if not monde then return end
    for _, parcelle in monde:GetChildren() do
        if parcelle:GetAttribute("Proprietaire")==joueur.UserId then
            local tour=parcelle:FindFirstChild("Tour")
            if not tour then return end
            for i=1,5 do
                local vitre=tour:FindFirstChild("Vitre"..i)
                if vitre then
                    local numero=((vitre:GetAttribute("Rangee") or 1)-1)*5+i
                    local aspect=G.aspect(numero)
                    if variantes[i] then variantes[i]:Destroy(); variantes[i]=nil end
                    local propre=bit32.band(e.tour.masque or 0,2^(i-1))~=0 or e.tour.etincelante
                    if aspect~="sale" and not propre then
                        local surface=Instance.new("SurfaceGui"); surface.Name="Aspect"..aspect; surface.Face=Enum.NormalId.Back; surface.CanvasSize=Vector2.new(200,200); surface.Parent=vitre
                        variantes[i]=surface
                        for n=1,3 do
                            local f=Instance.new("Frame"); f.Size=UDim2.fromScale(if aspect=="affiche" then 0.27 else 0.2,if aspect=="buee" then 0.85 else 0.3)
                            f.Position=UDim2.fromScale(0.1+(n-1)*0.27,0.1); f.BackgroundColor3=if aspect=="fiente" then Color3.fromRGB(235,235,205) else Color3.fromRGB(205,225,235)
                            f.BackgroundTransparency=if aspect=="buee" then 0.4 else 0; f.BorderSizePixel=0; f.Parent=surface
                        end
                    end
                end
            end
        end
    end
end)
Run.RenderStepped:Connect(function()
    for i,oiseau in pigeons do
        oiseau.Transparency=if time()<oiseauxFin then 0 else 1
        if time()<oiseauxFin then
            oiseau.CFrame=CFrame.new(centreOiseaux+Vector3.new(math.sin(time()*4+i)*3,i+math.sin(time()*12)*0.2,math.cos(time()*4+i)*2))
        end
    end
    if contact then journal("premiere_trainee_visible_ms",(time()-contact)*1000); contact=nil end
    for _, liste in {traces,eclats,{rideau,mousse}} do
        for _, f in liste do if f.Visible and time()>=(f:GetAttribute("Fin") or 0) then f.Visible=false end end
    end
end)
journal("pret","sons_vides")

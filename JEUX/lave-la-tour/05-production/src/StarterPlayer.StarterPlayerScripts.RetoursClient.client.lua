local Players = game:GetService("Players")
local joueur = Players.LocalPlayer
local fr = string.sub(string.lower(joueur.LocaleId), 1, 2) == "fr"
local remote = game:GetService("ReplicatedStorage"):WaitForChild("RetoursJoueurs")
local gui = Instance.new("ScreenGui")
gui.Name = "RetoursJoueurs"
gui.ResetOnSpawn = false
gui.Parent = joueur:WaitForChild("PlayerGui")

local function bouton(parent, texte, position, taille)
    local b = Instance.new("TextButton")
    b.Text = texte
    b.Position, b.Size = position, taille
    b.TextSize = 16
    b.TextWrapped = true
    b.BackgroundColor3 = Color3.fromRGB(235, 240, 245)
    b.TextColor3 = Color3.fromRGB(20, 30, 45)
    b.Parent = parent
    local minimum = Instance.new("UISizeConstraint")
    minimum.MinSize = Vector2.new(48, 48)
    minimum.Parent = b
    return b
end

-- Réserver cette zone dans le HUD du jeu ; au-dessus du joystick mobile.
local ouvrir = bouton(gui, fr and "Idée / bug" or "Idea / bug",
    UDim2.fromScale(0.02, 0.55), UDim2.fromScale(0.16, 0.09))
local panneau = Instance.new("Frame")
panneau.AnchorPoint = Vector2.new(0.5, 0.5)
panneau.Position = UDim2.fromScale(0.5, 0.5)
panneau.Size = UDim2.fromScale(0.9, 0.85)
panneau.BackgroundColor3 = Color3.fromRGB(25, 35, 50)
panneau.Visible = false
panneau.Parent = gui
local limite = Instance.new("UISizeConstraint")
limite.MaxSize = Vector2.new(620, 540)
limite.Parent = panneau
local titre = Instance.new("TextLabel")
titre.Size = UDim2.fromScale(0.76, 0.12)
titre.BackgroundTransparency = 1
titre.TextColor3 = Color3.new(1, 1, 1)
titre.TextSize = 18
titre.Text = fr and "Une idée ou un problème ?" or "An idea or a problem?"
titre.Parent = panneau
local fermer = bouton(panneau, "×", UDim2.fromScale(0.82, 0), UDim2.fromScale(0.16, 0.12))
local categorie = "idee"
local choix = {}
for i, valeur in ipairs({ "idee", "bug", "autre" }) do
    local libelles = fr and { "Idée", "Bug", "Autre" } or { "Idea", "Bug", "Other" }
    local b = bouton(panneau, libelles[i], UDim2.fromScale(0.03 + (i - 1) * 0.32, 0.16), UDim2.fromScale(0.30, 0.14))
    choix[valeur] = b
    b.Activated:Connect(function()
        categorie = valeur
        for cle, autre in pairs(choix) do
            autre.BackgroundColor3 = cle == categorie and Color3.fromRGB(150, 210, 255) or Color3.fromRGB(235, 240, 245)
        end
    end)
end
choix.idee.BackgroundColor3 = Color3.fromRGB(150, 210, 255)
local texte = Instance.new("TextBox")
texte.Position = UDim2.fromScale(0.03, 0.34)
texte.Size = UDim2.fromScale(0.94, 0.32)
texte.Text = ""
texte.PlaceholderText = fr and "Décris ton idée ou ton bug… (sans information personnelle)" or "Describe your idea or bug… (no personal information)"
texte.ClearTextOnFocus = false
texte.MultiLine = true
texte.TextWrapped = true
texte.TextSize = 18
texte.TextXAlignment = Enum.TextXAlignment.Left
texte.TextYAlignment = Enum.TextYAlignment.Top
texte.Parent = panneau
local compteur = Instance.new("TextLabel")
compteur.Position, compteur.Size = UDim2.fromScale(0.03, 0.67), UDim2.fromScale(0.94, 0.09)
compteur.TextColor3 = Color3.new(1, 1, 1)
compteur.BackgroundTransparency = 1
compteur.TextSize = 14
compteur.Text = "0 / 500"
compteur.Parent = panneau
local envoyer = bouton(panneau, fr and "Envoyer" or "Send", UDim2.fromScale(0.03, 0.80), UDim2.fromScale(0.94, 0.16))
local enCours = false
texte:GetPropertyChangedSignal("Text"):Connect(function()
    local n = utf8.len(texte.Text)
    if not n then
        texte.Text = ""
        return
    end
    if n > 500 then
        texte.Text = string.sub(texte.Text, 1, utf8.offset(texte.Text, 501) - 1)
        n = 500
    end
    compteur.Text = tostring(n) .. " / 500"
end)
ouvrir.Activated:Connect(function() panneau.Visible = not panneau.Visible end)
fermer.Activated:Connect(function() panneau.Visible = false end)
envoyer.Activated:Connect(function()
    if enCours then return end
    if (utf8.len(texte.Text) or 0) < 5 then
        compteur.Text = fr and "5 caractères minimum." or "At least 5 characters."
        return
    end
    enCours = true
    envoyer.Text = fr and "Envoi…" or "Sending…"
    remote:FireServer(categorie, texte.Text)
    task.delay(20, function()
        if enCours then
            enCours = false
            envoyer.Text = fr and "Réessayer" or "Try again"
        end
    end)
end)
remote.OnClientEvent:Connect(function(ok, raison)
    enCours = false
    envoyer.Text = fr and "Envoyer" or "Send"
    if ok then texte.Text = "" end
    compteur.Text = raison
end)

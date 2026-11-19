-- stabilite-panneaux.luau - mesure la stabilite des panneaux d'interface (regle Q9, procedure 06 scenario 13).
--
-- A executer par execute_luau COTE CLIENT, en Play, sur le joueur teste, panneaux a controler OUVERTS,
-- avec l'etat reel d'un joueur (sauvegarde chargee, compteurs qui bougent), SANS toucher a rien pendant la mesure.
-- Lecture seule : ne cree, ne modifie et ne detruit aucune instance.
--
-- Reglages (valeurs par defaut = CONNAISSANCES\seuils.json, section qa) :
local DUREE_S = 30          -- qa.stabilite_panneaux_duree_s
local PERIODE_S = 0.25      -- 120 echantillons sur 30 s (minimum : qa.stabilite_panneaux_echantillons_min)
local ECART_MAX_PX = 1      -- qa.stabilite_panneaux_ecart_max_px
local PROFONDEUR_MAX = 3    -- niveaux suivis sous chaque ScreenGui (panneaux, pas chaque ligne de liste)

local Players = game:GetService("Players")
local joueur = Players.LocalPlayer
if not joueur then
	return "ERREUR : a executer cote client (LocalPlayer absent)."
end
local racine = joueur:FindFirstChildOfClass("PlayerGui")
if not racine then
	return "ERREUR : PlayerGui absent."
end

local function chemin(objet)
	local morceaux = {}
	local courant = objet
	while courant and courant ~= racine do
		table.insert(morceaux, 1, courant.Name)
		courant = courant.Parent
	end
	return table.concat(morceaux, ".")
end

local suivis = {}
local function suivre(objet, profondeur)
	for _, enfant in ipairs(objet:GetChildren()) do
		if enfant:IsA("GuiObject") then
			if enfant.Visible and enfant.AbsoluteSize.X > 0 and enfant.AbsoluteSize.Y > 0 then
				table.insert(suivis, {
					objet = enfant,
					nom = chemin(enfant),
					defilant = enfant:IsA("ScrollingFrame"),
				})
				if profondeur < PROFONDEUR_MAX then
					suivre(enfant, profondeur + 1)
				end
			end
		elseif enfant:IsA("ScreenGui") then
			if enfant.Enabled then
				suivre(enfant, 1)
			end
		elseif enfant:IsA("Folder") then
			suivre(enfant, profondeur)
		end
	end
end
suivre(racine, 0)

if #suivis == 0 then
	return "ERREUR : aucun panneau visible. Ouvrir les panneaux a controler avant la mesure."
end

local function lire(s)
	local o = s.objet
	local x, y = o.AbsolutePosition.X, o.AbsolutePosition.Y
	local l, h = o.AbsoluteSize.X, o.AbsoluteSize.Y
	local dx, dy = 0, 0
	if s.defilant then
		dx, dy = o.CanvasPosition.X, o.CanvasPosition.Y
	end
	return { x, y, l, h, dx, dy }
end

for _, s in ipairs(suivis) do
	local v = lire(s)
	s.mini = table.clone(v)
	s.maxi = table.clone(v)
	s.sauts = 0
	s.precedent = v
	s.disparu = false
end

local echantillons = 0
local debut = os.clock()
while os.clock() - debut < DUREE_S do
	task.wait(PERIODE_S)
	echantillons += 1
	for _, s in ipairs(suivis) do
		if s.objet.Parent == nil or not s.objet.Visible then
			s.disparu = true
		else
			local v = lire(s)
			local bouge = false
			for i = 1, 6 do
				if v[i] < s.mini[i] then s.mini[i] = v[i] end
				if v[i] > s.maxi[i] then s.maxi[i] = v[i] end
				if math.abs(v[i] - s.precedent[i]) > ECART_MAX_PX then bouge = true end
			end
			if bouge then s.sauts += 1 end
			s.precedent = v
		end
	end
end

local noms = { "x", "y", "largeur", "hauteur", "defilement x", "defilement y" }
local lignes = {}
local fautifs = 0
for _, s in ipairs(suivis) do
	local ecarts = {}
	for i = 1, 6 do
		local e = s.maxi[i] - s.mini[i]
		if e > ECART_MAX_PX then
			table.insert(ecarts, string.format("%s %.0f px", noms[i], e))
		end
	end
	if #ecarts > 0 or s.disparu then
		fautifs += 1
		table.insert(lignes, string.format("INSTABLE | %s | %s | %d saut(s)%s",
			s.nom, table.concat(ecarts, ", "), s.sauts, s.disparu and " | a disparu pendant la mesure" or ""))
	end
end

local camera = workspace.CurrentCamera
local ecran = camera and string.format("%dx%d", camera.ViewportSize.X, camera.ViewportSize.Y) or "?"
table.insert(lignes, 1, string.format(
	"stabilite-panneaux : ecran %s, %d panneaux suivis, %d echantillons sur %d s, seuil %d px, %d instable(s) -> %s",
	ecran, #suivis, echantillons, DUREE_S, ECART_MAX_PX, fautifs, fautifs == 0 and "PASSE" or "ECHEC"))
return table.concat(lignes, "\n")

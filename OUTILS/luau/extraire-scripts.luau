-- extraire-scripts.luau : a passer a execute_luau en mode Edit. Lecture seule, ne modifie pas la place.
-- CHEMIN = nil  -> renvoie la liste JSON des scripts (fichier, classe, caracteres).
-- CHEMIN = "ServerScriptService.Jeu.EconomieService" -> renvoie la source de ce script, telle quelle.
-- Les noms de fichier suivent la convention de OUTILS\pousser-script.ps1.
-- Non verifie dans Studio au 15/11/2026 : premier usage a faire sur une place de test.
local CHEMIN = nil

local HttpService = game:GetService("HttpService")
local racines = { "ServerScriptService", "ServerStorage", "ReplicatedStorage", "ReplicatedFirst", "StarterPlayer", "StarterGui", "StarterPack" }

local function suffixe(inst)
	if inst:IsA("LocalScript") then
		return ".client.lua"
	elseif inst:IsA("Script") then
		return ".server.lua"
	end
	return ".lua"
end

local liste = {}
for _, nom in ipairs(racines) do
	local service = game:GetService(nom)
	for _, inst in ipairs(service:GetDescendants()) do
		if inst:IsA("LuaSourceContainer") then
			local chemin = inst:GetFullName()
			if CHEMIN and chemin == CHEMIN then
				return inst.Source
			end
			table.insert(liste, { fichier = chemin .. suffixe(inst), classe = inst.ClassName, caracteres = #inst.Source })
		end
	end
end

if CHEMIN then
	error("script introuvable : " .. CHEMIN)
end
table.sort(liste, function(a, b)
	return a.fichier < b.fichier
end)
return HttpService:JSONEncode(liste)

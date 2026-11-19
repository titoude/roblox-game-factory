--!nocheck
local RunService = game:GetService("RunService")
local Etat = require(script.Parent.EtatJoueur)
local E = require(script.Parent.EconomieService)
local V = require(script.Parent.VitresService)
local C = require(game:GetService("ReplicatedStorage").Jeu.Config)
local A = {}
local profils = function() return nil end
function A.configurer(chercher) profils = chercher end
function A.profil(joueur) return if RunService:IsStudio() then profils(joueur) else nil end
local function nombre(n) return type(n) == "number" and n == n and n >= 0 and n < math.huge end
function A.studioPieces(p, n)
    if not RunService:IsStudio() or not nombre(n) then return false end
    p.pieces = 0; E.crediter(p, n); return true
end
function A.studioAvance(p, n)
    if not RunService:IsStudio() or not nombre(n) or n > 86400 then return false end
    E.avancer(p, n); return true
end
function A.studioPalier(p, id, n)
    if not RunService:IsStudio() or not p.robots[id] or not nombre(n) or n % 1 ~= 0 or n > 10 then return false end
    p.robots[id] = {achetes = n, en_service = n, chantiers = {}}; return true
end
function A.studioTour(p, numero, rangees)
    if not RunService:IsStudio() or not nombre(numero) or numero % 1 ~= 0 or numero < 1 or numero > 4 or not nombre(rangees) then return false end
    V.annuler(p)
    p.tour = {numero = numero, rangees = 0, masque = 0, etincelante = false}
    p.tour.rangees = math.min(math.floor(rangees), V.hauteur(p)); return true
end
function A.studioAbsence(p, n)
    if not RunService:IsStudio() or not nombre(n) or n > 86400 then return false end
    E.hors_ligne(p, n); return true
end
function A.studioJourSuivant(p)
    if not RunService:IsStudio() then return false end
    local neuf = Etat.nouveau()
    p.quotas = neuf.quotas; p.contrat = neuf.contrat; return true
end
function A.studioJoueurFictif()
    if not RunService:IsStudio() then return nil end
    return Etat.nouveau()
end
function A.studioQuota(p, nom, valeur)
    if not RunService:IsStudio() or not nombre(valeur) or (nom ~= "mousse_s" and nom ~= "pourboires_min") then return false end
    p.quotas[nom] = math.min(valeur, if nom == "mousse_s" then C.MOUSSE_QUOTA_S else C.POURBOIRE_QUOTA_MIN); return true
end
function A.studioEtincelante(p)
    if not RunService:IsStudio() then return false end
    p.tour.rangees = V.hauteur(p); p.tour.masque = 0; p.tour.pigeons = nil; p.tour.etincelante = true
    V.annuler(p); return true
end
return A

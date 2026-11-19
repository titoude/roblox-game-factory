-- Premier Play réel (17/11/2026) : place jamais publiée, GetDataStore lève et Amorce tombait.
local M = banc.require("ServerScriptService.Jeu.MagasinSur")
local D = banc.require("ServerScriptService.Jeu.DonneesService")
local refus = {GetDataStore = function() error("You must publish this place to the web to access DataStore.") end}
local m, memoire = M.ouvrir(refus, "X_v1_studio", true)
banc.verifier(memoire, "Studio non publié : magasin en mémoire")
banc.egal(m:UpdateAsync("k", function(a) return {n = (a and a.n or 0) + 1} end).n, 1, "UpdateAsync en mémoire")
banc.egal(m:UpdateAsync("k", function(a) return {n = a.n + 1} end).n, 2, "valeur conservée")
banc.egal(m:UpdateAsync("k", function() return nil end), nil, "transformation refusée : rien écrit")
banc.egal(m:GetAsync("k").n, 2, "lecture après refus")
local t = m:GetAsync("k"); t.n = 99
banc.egal(m:GetAsync("k").n, 2, "copie, pas de référence partagée")
banc.verifier(M.ouvrir(refus, "X_v1_studio", true) == m, "même nom, même magasin")
banc.verifier(not pcall(function() M.ouvrir(refus, "X_v1", false) end), "hors Studio : l'erreur remonte, jamais de jeu sans sauvegarde silencieux")
local vrai = game:GetService("DataStoreService")
local r, mem = M.ouvrir(vrai, "Y_v1", false)
banc.verifier(not mem and r ~= nil, "DataStore disponible : le vrai magasin")
-- Le service de données démarre et sauvegarde en mémoire dans une place locale.
local run = {IsStudio = function() return true end}
local s = D.nouveau({serveur = "local", horloge = function() return 1000 end, attendre = function() end, DataStoreService = refus, RunService = run})
local j = {UserId = 7, Kick = function(self, c) self.kick = c end}
local p = s.charger(j)
banc.verifier(p ~= nil and j.kick == nil, "chargement en mémoire sans renvoi")
p.pieces = 123
banc.verifier(s.sauver(j, true), "sortie sauvée en mémoire")
local s2 = D.nouveau({serveur = "local2", horloge = function() return 1000 end, attendre = function() end, DataStoreService = refus, RunService = run})
banc.egal(s2.charger({UserId = 7, Kick = function() end}).pieces, 123, "rechargement depuis la mémoire")

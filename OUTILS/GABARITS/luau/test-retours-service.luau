-- Depuis ce dossier : ../../bin/luau.exe test-retours-service.luau
-- Compilation depuis la racine : OUTILS/bin/luau-compile.exe --null <chaque script>
local module = require("./ServerScriptService.Jeu.RetoursService")
local maintenant = 1794820000
local appels, erreurs, dernier, nom = 0, 0, nil, nil
local donnees = {}
local quotas = {}
function donnees:GetDataStore(n)
    nom = n
    return {
        UpdateAsync = function(_, cle, transformer)
            local valeur, utilisateurs = transformer(quotas[cle])
            if valeur then
                assert(utilisateurs[1] == 42, "métadonnée du quota")
                quotas[cle] = valeur
            end
            return quotas[cle]
        end,
        SetAsync = function(_, cle, valeur, utilisateurs)
            appels += 1
            if erreurs > 0 then
                erreurs -= 1
                error("panne fictive")
            end
            dernier = { cle = cle, valeur = valeur, utilisateurs = utilisateurs }
        end,
    }
end
local json = {}
local capture
function json:JSONEncode(valeur)
    capture = valeur
    -- Sérialisation du faux service ; Roblox fournit le vrai JSONEncode.
    return "JSON-factice"
end
local attentes = 0
local d = { DataStoreService = donnees, HttpService = json, studio = true, version = 7,
    horloge = function() return maintenant end,
    attendre = function() attentes += 1 end }
local service = module.nouveau({ NOM_COURT = "Test" }, d)
local joueur = { UserId = 42, LocaleId = "fr-fr" }
local nombre = 0
local function verifier(libelle, condition)
    assert(condition, "ECHEC " .. libelle)
    nombre += 1
    print("ok     " .. libelle)
end
verifier("magasin Studio isolé", nom == "TestRetours_v1_studio")
verifier("type texte", not service.envoyer(joueur, "bug", {}))
verifier("texte court", not service.envoyer(joueur, "bug", "abcd"))
verifier("UTF8 invalide", not service.envoyer(joueur, "bug", string.char(255) .. "abcd"))
verifier("texte long", not service.envoyer(joueur, "bug", string.rep("é", 501)))
verifier("catégorie", not service.envoyer(joueur, "admin", "un texte"))
verifier("aucune écriture invalide", appels == 0)
verifier("envoi UTF8", service.envoyer(joueur, "bug", "ééééé"))
verifier("clé exacte", dernier.cle == "r_1794820000_42")
verifier("métadonnée effacement", #dernier.utilisateurs == 1 and dernier.utilisateurs[1] == 42)
local champs = 0
for _ in pairs(capture) do champs += 1 end
verifier("valeur exacte avant JSONEncode", champs == 6 and capture.t == maintenant and capture.userId == 42
    and capture.lang == "fr-fr" and capture.version == 7 and capture.categorie == "bug" and capture.texte == "ééééé"
    and dernier.valeur == "JSON-factice")
verifier("cadence immédiate", not service.envoyer(joueur, "idee", "encore un texte"))
maintenant += 59
verifier("cadence 59 secondes", not service.envoyer(joueur, "idee", "encore un texte"))
maintenant += 1
erreurs = 2
local avant = appels
verifier("deux reprises", service.envoyer(joueur, "idee", "encore un texte") and appels == avant + 3 and attentes == 2)
for _ = 1, 3 do
    maintenant += 60
    assert(service.envoyer(joueur, "autre", "un autre retour"))
end
maintenant += 60
verifier("limite quotidienne", not service.envoyer(joueur, "autre", "un autre retour"))
local autreServeur = module.nouveau({ NOM_COURT = "Test" }, d)
verifier("quota quotidien entre serveurs", not autreServeur.envoyer(joueur, "bug", "nouveau serveur"))
maintenant += 86400
verifier("jour suivant", service.envoyer(joueur, "bug", "nouveau jour"))
autreServeur = module.nouveau({ NOM_COURT = "Test" }, d)
verifier("cadence entre serveurs", not autreServeur.envoyer(joueur, "bug", "nouveau serveur"))
maintenant += 60
erreurs = 3
avant = appels
verifier("échec après trois essais", not service.envoyer(joueur, "bug", "panne persistante") and appels == avant + 3)
d.studio = false
module.nouveau({ NOM_COURT = "Test" }, d)
verifier("magasin production", nom == "TestRetours_v1")
print(tostring(nombre) .. "/" .. tostring(nombre) .. " contrôles passés")

local module = require("./ServerScriptService.Jeu.AvisService")
local nombre, comptes, textes = 0, {}, {}
local joueur, profil = { UserId = 123 }, {}
local function nouveau(version)
    return module.nouveau({ VERSION_AVIS = version }, {
        compter = function(nom) table.insert(comptes, nom) end,
        retour = function(j, categorie, texte)
            assert(j == joueur and categorie == "avis"); table.insert(textes, texte)
        end,
    })
end
local function verifier(nom, ok)
    assert(ok, "ECHEC " .. nom); nombre += 1; print("ok     " .. nom)
end
local s = nouveau(1)
verifier("jamais avant 180 s", not s:proposer(joueur, profil, 179) and profil.avis == nil)
verifier("proposé une fois", s:proposer(joueur, profil, 180) and not s:proposer(joueur, profil, 181))
verifier("refus sans proposition", not s:repondre(joueur, {}, 3))
for _, note in ipairs({ 0, 6, 2.5, "3", 0/0 }) do
    verifier("note invalide refusée", not s:repondre(joueur, profil, note))
end
verifier("texte long refusé", not s:repondre(joueur, profil, 4, string.rep("é", 501)))
verifier("texte mal formé refusé", not s:repondre(joueur, profil, 4, string.char(255)))
verifier("réponse acceptée", s:repondre(joueur, profil, 4, "Très bien"))
verifier("compteur correct une fois", #comptes == 1 and comptes[1] == "avis_4")
verifier("texte transmis", #textes == 1 and textes[1] == "Très bien")
verifier("deuxième réponse refusée", not s:repondre(joueur, profil, 1, "autre") and #comptes == 1)
verifier("répondu ne repropose pas", not s:proposer(joueur, profil, 500))
verifier("reconnexion ne repropose pas", not nouveau(1):proposer({ UserId = 123 }, profil, 200))
s = nouveau(2)
verifier("nouvelle version repropose", s:proposer(joueur, profil, 180))
verifier("texte vide non transmis", s:repondre(joueur, profil, 5, "  ") and #textes == 1 and #comptes == 2)
s = nouveau(3); s:proposer(joueur, profil, 180)
verifier("texte facultatif", s:repondre(joueur, profil, 2) and #textes == 1)
s = nouveau(4); s:proposer(joueur, profil, 180)
verifier("borne 500 caractères", s:repondre(joueur, profil, 1, string.rep("é", 500)))
print(tostring(nombre) .. "/" .. tostring(nombre) .. " contrôles passés")

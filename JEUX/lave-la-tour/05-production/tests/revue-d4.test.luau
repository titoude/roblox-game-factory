banc.demarrer_serveur()
local A=banc.require("ServerScriptService.Jeu.ActionsDeTest")
local j=banc.joueur(910,"Incoherent");local autre=banc.joueur(911,"Valide")
A.profil(autre).robots.r1={achetes=1,en_service=1,chantiers={}}
A.profil(j).tour.numero=9
banc.avancer(3)
banc.egal(j:GetAttribute("Kick"),"donnees_indisponibles","D4 profil incoherent isole")
banc.verifier(A.profil(autre).pieces>=0.75,"D4 boucle des autres joueurs continue")

local S=banc.require("ServerScriptService.Jeu.EtatJoueur")
local V=banc.require("ServerScriptService.Jeu.VitresService")
local t=0;V.horloge(function() return t end)
local p,q,r=S.nouveau(),S.nouveau(),S.nouveau();local a,b,c={UserId=1},{UserId=2},{UserId=3}
V.inscrire(a,p);V.inscrire(b,q);V.inscrire(c,r);V.asseoir(a,q,"tour")
banc.verifier(V.asseoir(b,p,"tour"),"D2 premier visiteur")
banc.verifier(not V.asseoir(c,p,"tour"),"D2 deuxieme visiteur refuse")
banc.verifier(V.asseoir(a,p,"tour"),"D2 retour proprietaire garanti")

local S=banc.require("ServerScriptService.Jeu.EtatJoueur")
local V=banc.require("ServerScriptService.Jeu.VitresService")
local t=0;V.horloge(function() return t end)
local p,q=S.nouveau(),S.nouveau();local a,b={UserId=1},{UserId=2}
V.inscrire(a,p);V.inscrire(b,q);V.asseoir(b,p,"tour");V.attribuer(p,b)
for _=1,4 do local r,i=V.attribuer(p,a);t+=1.5;V.finir_vitre(p,a,r,i,t) end
t=10;banc.egal(V.attribuer(p,a),nil,"D1 attribution protegee a dix secondes")
t=10.001
banc.verifier(V.attribuer(p,a)~=nil,"D1 reservation abandonnee recuperee")
banc.verifier(not V.finir_vitre(p,b,1,1,t),"D1 ancienne attribution refusee")

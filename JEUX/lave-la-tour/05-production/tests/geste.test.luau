local G = banc.require("ReplicatedStorage.Jeu.GesteLogique")
local function passe(p,d) return G.passe(p,200,d or 0.2) end
banc.verifier(passe({{x=0,y=0}}),"tapotement immobile")
banc.verifier(passe({{x=0,y=0},{x=5,y=5}}),"tapotement tremblé")
banc.verifier(not passe({{x=0,y=0}},0.5),"appui long refusé")
banc.verifier(not passe({{x=0,y=0},{x=60,y=0}}),"glissé court refusé")
banc.verifier(not passe({{x=0,y=0},{x=0,y=150}}),"glissé vertical refusé")
banc.verifier(passe({{x=0,y=0},{x=100,y=0}}),"moitié exacte acceptée")
banc.verifier(passe({{x=0,y=0},{x=110,y=0}}),"plus de moitié acceptée")
banc.verifier(passe({{x=200,y=0},{x=90,y=0}}),"sens inverse accepté")
banc.verifier(not G.passe({},200,0),"suite vide refusée")
local n=0
for i=1,3 do n=G.ajouter_passe(n,true); banc.egal(n,i,"compte des passes") end
banc.egal(G.ajouter_passe(n,true),3,"pas de quatrième passe")
banc.egal(G.ajouter_passe(1,false),1,"invalide sans progression")
local cran,derniere=0,nil
for i=1,9 do cran=G.note(cran,derniere,i); derniere=i; banc.egal(cran,(i-1)%8+1,"cran "..i) end
banc.egal(G.note(4,0,3),5,"trois secondes continues")
banc.egal(G.note(4,0,3.01),1,"pause supérieure à trois secondes")
banc.egal(G.aspect(8),"fiente","huitième")
banc.egal(G.aspect(17),"buee","dix-septième")
banc.egal(G.aspect(18),"sale","ordinaire")
for i=20,100,10 do banc.verifier(G.aspect(i)~="sale","une sur dix "..i) end
local dispo={demenager=true,chez_visiteur=true,rejoindre=true,contrat=true}
for _,nom in {"demenager","chez_visiteur","rejoindre","contrat"} do banc.egal(G.contextuel(dispo),nom,"priorité "..nom); dispo[nom]=nil end
banc.egal(G.contextuel(dispo),nil,"aucun contexte")
for _,ecran in {{844,390},{1920,1080}} do
    local c=G.camera({x=2,y=100,z=3},ecran[1],ecran[2])
    banc.verifier(c.fraction>=0.4 and c.fraction<0.5,"largeur projetée >= 40 %")
    -- Reprojection indépendante avec une base orthonormée issue de la position.
    local dx,dy,dz=c.x-2,c.y-100,c.z-3
    local d=math.sqrt(dx*dx+dy*dy+dz*dz)
    local horizontal=math.sqrt(dx*dx+dz*dz)
    local rx,rz=dz/horizontal,-dx/horizontal
    local xmin,xmax=math.huge,-math.huge
    for _,x in {-2.5,2.5} do
        for _,y in {-2.5,2.5} do
            local profondeur=d-(x*dx+y*dy)/d
            local projection=(x*rx)/(2*math.tan(math.rad(25))*ecran[1]/ecran[2]*profondeur)
            xmin=math.min(xmin,projection); xmax=math.max(xmax,projection)
        end
    end
    banc.verifier(xmax-xmin>=0.4,"projection indépendante couvre quarante pour cent")
    banc.verifier(math.abs(xmax-xmin-c.fraction)<0.00001,"fraction annoncée exacte")
    banc.verifier(c.y>100 and c.z>3,"au-dessus et devant")
    banc.verifier(math.abs(math.deg(math.atan((c.x-2)/(c.z-3)))-35)<0.001,"biais 35 degrés")
end

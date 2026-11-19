-- Le banc courant ne simule pas Seat. Seule cette classe est remplacée
-- explicitement par une Part ; aucune physique ni assise n'est qualifiée.
local creer=Instance.new
local sieges=0
Instance.new=function(classe,parent)
    if classe=="Seat" then sieges+=1; return creer("Part",parent) end
    return creer(classe,parent)
end
local M=banc.require("ServerScriptService.Jeu.MondeService")
local monde=M.construire()
banc.verifier(monde~=nil,"construction")
banc.egal(M.construire(),monde,"construction idempotente")
local joueurs={}
for i=1,6 do
    local j={UserId=i}; joueurs[i]=j
    banc.verifier(M.attribuer_parcelle(j)~=nil,"parcelle "..i)
end
banc.egal(sieges,12,"deux sièges par tour construits")
banc.egal(M.attribuer_parcelle({UserId=7}),nil,"septième refusé")
banc.egal(M.nombre_de_pieces(),152,"borne calculée exacte à six joueurs")
banc.verifier(M.nombre_de_pieces()<1500,"sous la borne de la fiche")
local tour=monde.Parcelle1.Tour
banc.egal(tour.Corps.Size.Y,600,"tour 1 hauteur 600")
for _,r in {0,1,37,119,120} do
    M.mettre_a_jour(joueurs[1],{numero=1,rangees=r,masque=3})
    banc.avancer(0.4)
    for face=1,4 do
        banc.egal(tour["Propre"..face]:GetAttribute("Hauteur")+tour["Sale"..face]:GetAttribute("Hauteur"),600,"somme panneaux "..r..":"..face)
    end
    banc.egal(tour.Nacelle.Plancher.CFrame.Position.Y,math.min(119,r)*5+0.5,"hauteur nacelle "..r)
end
for numero,hauteur in {600,1400,2000} do
    for _,j in joueurs do M.mettre_a_jour(j,{numero=numero,rangees=10,masque=0}) end
    banc.avancer(0.4)
    banc.egal(tour.Corps.Size.Y,hauteur,"hauteur tour "..numero)
    banc.egal(M.nombre_de_pieces(),152,"compte indépendant des étages")
end
M.liberer_parcelle(joueurs[1]); banc.egal(M.nombre_de_pieces(),129,"libération")
banc.verifier(M.attribuer_parcelle({UserId=7})~=nil,"réattribution")
Instance.new=creer

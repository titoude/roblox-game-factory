--!nocheck
-- Calculs purs : aucune instance, aucun gain, aucune API graphique.
local G = {}
-- À remonter dans Config : angle 35°, élévation 8°, champ vertical 50°,
-- cadrage cible 44 %, tapotement 12 px / 0,35 s, recul 2 s, montée 0,4 s.
G.ANGLE = math.rad(35)
G.ELEVATION = math.rad(8)
G.FOV = 50
function G.passe(positions, largeur, duree)
    if #positions == 0 or largeur <= 0 then return false end
    local depart, ecart = positions[1], 0
    local xmin, xmax = depart.x, depart.x
    for _, p in positions do
        ecart = math.max(ecart, math.sqrt((p.x-depart.x)^2 + (p.y-depart.y)^2))
        xmin = math.min(xmin, p.x); xmax = math.max(xmax, p.x)
    end
    return xmax-xmin >= largeur/2 or (ecart <= 12 and duree <= 0.35)
end
function G.ajouter_passe(compte, valide)
    return math.min(3, compte + (if valide then 1 else 0))
end
function G.note(cran, derniere, maintenant)
    return if derniere == nil or maintenant-derniere > 3 then 1 else cran%8+1
end
function G.aspect(numero)
    if numero == 8 then return "fiente" end
    if numero == 17 then return "buee" end
    if numero > 17 and numero%10 == 0 then
        return ({"fiente", "buee", "affiche"})[math.floor(numero/10)%3+1]
    end
    return "sale"
end
function G.contextuel(disponibles)
    for _, nom in {"demenager", "chez_visiteur", "rejoindre", "contrat", "monter"} do
        if disponibles[nom] then return nom end
    end
    return nil
end
-- Projection exacte des quatre coins dans une base de camra incline.
-- Coordonnes locales : faade XY, extrieur +Z. Retour numrique testable.
function G.camera(vitre, largeur, hauteur)
    local a, e = G.ANGLE, G.ELEVATION
    local sa, ca, se, ce = math.sin(a), math.cos(a), math.sin(e), math.cos(e)
    local tangente = math.tan(math.rad(G.FOV/2)) * largeur/hauteur
    local function fraction(distance)
        local bas, haut = math.huge, -math.huge
        for _, x in {-2.5, 2.5} do
            for _, y in {-2.5, 2.5} do
                local profondeur = distance - x*sa*ce - y*se
                local proj = x*ca / (2*tangente*profondeur)
                bas = math.min(bas, proj); haut = math.max(haut, proj)
            end
        end
        return haut-bas
    end
    local bas, haut = 3, 100
    for _ = 1, 40 do
        local milieu = (bas+haut)/2
        if fraction(milieu) > 0.44 then bas = milieu else haut = milieu end
    end
    local d = (bas+haut)/2
    return {x=vitre.x+d*sa*ce, y=vitre.y+d*se, z=vitre.z+d*ca*ce,
        cible=vitre, distance=d, fraction=fraction(d)}
end
return G

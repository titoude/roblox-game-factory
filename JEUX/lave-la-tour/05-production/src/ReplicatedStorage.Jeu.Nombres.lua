--!nocheck
local Nombres = {}
local function suffixe(groupe)
    if groupe == 0 then return "" end
    local connus = {"k", "M", "Md", "Bn"}
    if connus[groupe] then return connus[groupe] end
    local n, lettres = groupe - 4, ""
    repeat
        n -= 1
        lettres = string.char(97 + n % 26) .. lettres
        n = math.floor(n / 26)
    until n == 0
    return lettres
end
function Nombres.abreger(valeur, langue)
    if type(valeur) ~= "number" or valeur ~= valeur then valeur = 0 end
    valeur = math.clamp(valeur, 0, 1e300)
    local groupe = 0
    while valeur >= 1000 do valeur /= 1000; groupe += 1 end
    local texte = string.format(if valeur < 10 and groupe > 0 then "%.1f" else "%.0f", valeur)
    if tonumber(texte) >= 1000 then
        groupe += 1
        texte = "1"
    end
    if type(langue) == "string" and string.sub(langue, 1, 2) == "fr" then texte = string.gsub(texte, "%.", ",") end
    return texte .. suffixe(groupe)
end
return Nombres

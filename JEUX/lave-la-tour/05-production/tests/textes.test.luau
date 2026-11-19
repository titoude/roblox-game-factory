local T=banc.require("ReplicatedStorage.Jeu.Textes")
for cle,texte in T.en do
    banc.verifier(type(texte)=="string" and #texte>0,"anglais non vide "..cle)
    banc.verifier(type(T.fr[cle])=="string" and #T.fr[cle]>0,"français non vide "..cle)
end
for cle in T.fr do banc.verifier(T.en[cle]~=nil,"source anglaise "..cle) end
for _,cle in {"objectif_demenager","objectif_robot","objectif_amelioration","objectif_segment","objectif_chantier","mousse_quota_atteint","donnees_indisponibles","achat_verrouille","achat_impossible"} do
    banc.verifier(T.en[cle]~=nil and T.fr[cle]~=nil,"clé serveur "..cle)
    for _,langue in {"en","fr"} do banc.verifier(T.t(langue,cle)~=cle,"traduction serveur "..langue..":"..cle) end
end
for _,langue in {"en","fr"} do
    for _,cle in T.avant_action do
        local texte=T.t(langue,cle,"1","120")
        local mots=0; for _ in string.gmatch(texte,"%S+") do mots+=1 end
        banc.verifier(mots<=8,"avant action <= huit mots "..langue..":"..cle)
    end
end
banc.egal(T.t("de","frotte"),T.en.frotte,"repli anglais")
banc.egal(T.t("fr","inconnue"),"inconnue","repli clé")
banc.egal(T.t("fr-FR","pieces","12"),"12 pièces","français et accent")

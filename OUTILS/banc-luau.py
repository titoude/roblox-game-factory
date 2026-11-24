#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exécute la logique Luau serveur dans un environnement déterministe local.

Bibliothèque standard uniquement ; chaque test possède son processus et ses données.
Codes : 0 succès, 1 échec, 2 exécutable absent, 5 dossier introuvable.
"""
import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

OUTILS = Path(__file__).resolve().parent
EXE = ".exe" if os.name == "nt" else ""
SERVICES = {
    "ServerScriptService", "ServerStorage", "ReplicatedStorage", "ReplicatedFirst",
    "StarterPlayer", "StarterGui", "StarterPack", "Workspace", "Lighting", "SoundService",
}


def ecrire_sur(destination, texte):
    """Vérifie le temporaire avant le remplacement atomique, même hors dépôt."""
    if not texte:
        raise ValueError(f"fichier vide refusé : {destination}")
    fd, nom = tempfile.mkstemp(dir=destination.parent, suffix=".tmp")
    temporaire = Path(nom)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as flux:
            flux.write(texte)
            flux.flush()
            os.fsync(flux.fileno())
        if temporaire.read_text(encoding="utf-8") != texte:
            raise OSError(f"relecture différente : {destination}")
        os.replace(temporaire, destination)
    finally:
        temporaire.unlink(missing_ok=True)


def sources(dossier):
    resultat, chemins = [], set()
    for fichier in sorted(dossier.rglob("*.lua")):
        base = fichier.name[:-4]
        classe = "ModuleScript"
        for suffixe, type_script in ((".server", "Script"), (".client", "LocalScript")):
            if base.endswith(suffixe):
                base, classe = base[:-len(suffixe)], type_script
                break
        morceaux = base.split(".")
        if (len(morceaux) < 2 or morceaux[0] not in SERVICES
                or any(not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", s) for s in morceaux)):
            raise ValueError(f"nom de script invalide : {fichier}")
        if base in chemins:
            raise ValueError(f"chemin Roblox dupliqué : {base}")
        chemins.add(base)
        texte = fichier.read_text(encoding="utf-8-sig")
        if not texte.strip():
            raise ValueError(f"fichier vide : {fichier}")
        resultat.append((base, classe, fichier, texte))
    for chemin in chemins:
        if any(chemin.startswith(autre + ".") for autre in chemins):
            raise ValueError(f"un script ne peut servir de dossier : {chemin}")
    return resultat


def assembler(scripts, test):
    morceaux, correspondances = [], []
    ligne = 1

    def ajouter(texte, origine=None):
        nonlocal ligne
        texte = texte.rstrip("\n") + "\n"
        debut = ligne
        ligne += texte.count("\n")
        morceaux.append(texte)
        if origine:
            correspondances.append((debut, ligne - 1, origine))

    runtime = OUTILS / "luau" / "faux-roblox.luau"
    ajouter(runtime.read_text(encoding="utf-8-sig"), runtime)
    ajouter('''local chargeurs, instances, classes, cache, actifs, demarres = {}, {}, {}, {}, {}, {}
local function creer(chemin, classe)
    local segments=string.split(chemin,".")
    local parent=game:GetService(segments[1])
    for i=2,#segments do
        local enfant=parent:FindFirstChild(segments[i])
        if not enfant then enfant=Instance.new(if i==#segments then classe else "Folder"); enfant.Name=segments[i]; enfant.Parent=parent end
        if i==#segments then assert(enfant.ClassName==classe,"classe incompatible : "..chemin) end
        parent=enfant
    end
    instances[chemin]=parent; classes[parent]=classe; return parent
end
local function charger(instance)
    assert(typeof(instance)=="table" and classes[instance]=="ModuleScript","require attend une instance ModuleScript du jeu")
    if cache[instance]~=nil then return cache[instance] end
    assert(not actifs[instance],"require cyclique : "..instance:GetFullName())
    actifs[instance]=true
    local ok,valeur=pcall(chargeurs[instance])
    actifs[instance]=nil
    if not ok then error(valeur,0) end
    assert(valeur~=nil,"ModuleScript sans valeur : "..instance:GetFullName())
    cache[instance]=valeur; return valeur
end
banc._installer_require(charger)
function banc.instance(chemin)
    chemin=chemin:gsub("^game%.","")
    local s=string.split(chemin,"."); local v=game:GetService(s[1])
    for i=2,#s do v=v:WaitForChild(s[i]) end; return v
end
function banc.require(chemin) return charger(banc.instance(chemin)) end
''')
    for chemin, classe, _, _ in scripts:
        ajouter(f"creer({json.dumps(chemin)}, {json.dumps(classe)})")
    for chemin, _, fichier, texte in scripts:
        ajouter(f"do\nlocal script=instances[{json.dumps(chemin)}]\nlocal function executer()")
        ajouter(texte, fichier)
        ajouter("end\nsetfenv(executer,banc.environnement(script))\nchargeurs[script]=executer\nend")
    noms = ",".join(json.dumps(p) for p, c, _, _ in scripts if c == "Script")
    ajouter('''function banc.demarrer_serveur()
    for _,nom in ipairs({''' + noms + '''}) do
        local instance=instances[nom]
        if not demarres[instance] then demarres[instance]=true; task.spawn(chargeurs[instance]) end
    end
    banc.avancer(0)
end
local termine=false
local function scenario()
''')
    contenu = test.read_text(encoding="utf-8-sig")
    if not contenu.strip():
        raise ValueError(f"test vide : {test}")
    ajouter(contenu, test)
    ajouter('''end
setfenv(scenario,banc.environnement(nil))
task.spawn(function() scenario(); termine=true end)
banc.avancer(0)
assert(termine,"test suspendu : utiliser banc.avancer au lieu de task.wait au niveau principal")
print("PASSE : scénario terminé")
''')
    return "".join(morceaux), correspondances


def remapper(sortie, programme, correspondances):
    def remplacer(match):
        numero = int(match.group(1))
        for debut, fin, origine in correspondances:
            if debut <= numero <= fin:
                return f"{origine}:{numero - debut + 1}"
        return match.group(0)
    return re.sub(re.escape(programme.as_posix()) + r":(\d+)", remplacer,
                  sortie.replace(str(programme), programme.as_posix()))


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src", type=Path)
    parser.add_argument("--tests", required=True, type=Path)
    parser.add_argument("--filtre", default="*")
    parser.add_argument("--verbeux", action="store_true")
    args = parser.parse_args(argv)
    if not args.src.is_dir() or not args.tests.is_dir():
        print("ECHEC : dossier introuvable")
        return 5
    executable = OUTILS / "bin" / ("luau" + EXE)
    if not executable.is_file():
        print(f"ECHEC : OUTILS/bin/{executable.name} absent")
        return 2
    try:
        scripts = sources(args.src)
        tests = [t for t in sorted(args.tests.rglob("*.test.luau"))
                 if fnmatch.fnmatch(t.name, args.filtre) or args.filtre in t.name]
        if not scripts or not tests:
            raise ValueError("aucun script ou aucun test sélectionné")
        echecs = 0
        with tempfile.TemporaryDirectory(prefix="banc-luau-") as temporaire:
            programme = Path(temporaire) / "programme.luau"
            for test in tests:
                texte, correspondances = assembler(scripts, test)
                ecrire_sur(programme, texte)
                try:
                    execution = subprocess.run([str(executable), str(programme)],
                                               capture_output=True, encoding="utf-8", errors="replace", timeout=20)
                    sortie = remapper(execution.stdout + execution.stderr, programme, correspondances)
                    succes = execution.returncode == 0
                except subprocess.TimeoutExpired:
                    succes, sortie = False, "durée maximale de 20 secondes dépassée"
                echecs += not succes
                print(f"{'PASSE' if succes else 'ECHEC'} : {test.name}")
                if args.verbeux or not succes:
                    print(sortie.rstrip())
        return int(echecs > 0)
    except (OSError, ValueError) as erreur:
        print(f"ECHEC : {erreur}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

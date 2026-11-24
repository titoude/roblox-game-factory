# verifier-usine.ps1 - auto-controle de l'usine. A lancer a chaque ouverture de session de l'orchestrateur.
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
#   verifier-usine.ps1 [-Silencieux]
#
# Controle : structure, skills (frontmatter), fichiers vides, secrets, scripts PowerShell (syntaxe, ASCII),
# JSON valides, syntaxe Python, suites de controles des outils, syntaxe et tests Luau, banc hors Studio des jeux,
# fichier STOP, alertes ouvertes, verrous, espace disque.
# Code de sortie : 0 si aucune erreur (les avertissements n'echouent pas), 1 sinon.
param([switch]$Silencieux)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'commun.ps1')
$racine = Get-RacineUsine
$erreurs = New-Object System.Collections.Generic.List[string]
$avis = New-Object System.Collections.Generic.List[string]
function Err([string]$t) { $erreurs.Add($t) }
function Avis([string]$t) { $avis.Add($t) }

# 1. Structure
$attendus = @(
  'README.md', 'GARDE-FOUS.md', 'AGENTS.md', 'CLAUDE.md', 'ALERTES.md',
  'CONNAISSANCES\00-LISEZ-MOI.md', 'CONNAISSANCES\REGLES.md', 'CONNAISSANCES\seuils.json', 'CONNAISSANCES\SEUILS-PORTES.md',
  'CONNAISSANCES\LECONS-ARCHIPEL.md', 'CONNAISSANCES\SOURCES-VEILLE.md', 'CONNAISSANCES\MODELES-ET-QUOTAS.md',
  'CONNAISSANCES\PLAFONDS.md', 'CONNAISSANCES\JOURNAL-DES-JEUX.md', 'CONNAISSANCES\PROPOSITIONS\LISEZ-MOI.md',
  'PROCEDURES\00-ORCHESTRATION.md', 'PROCEDURES\01-VEILLE-NAVIGATEUR.md', 'PROCEDURES\02-CONCEPT.md',
  'PROCEDURES\03-REVUE-ECONOMIE.md', 'PROCEDURES\04-REVUE-FUN.md', 'PROCEDURES\05-PRODUCTION-STUDIO.md',
  'PROCEDURES\06-QA-MULTIJOUEUR.md', 'PROCEDURES\07-RELEASE.md', 'PROCEDURES\08-DISTRIBUTION.md',
  'PROCEDURES\09-BILAN.md', 'PROCEDURES\10-AMORCAGE-PROPRIETAIRE.md', 'PROCEDURES\11-RETOURS-JOUEURS.md',
  'PROCEDURES\12-PROMOTION-VIDEO.md', 'PROCEDURES\13-ORCHESTRATION-MULTI-FOURNISSEURS.md', 'PROCEDURES\14-ENTREPRISE-BOUCLE-D-EXPLOITATION.md',
  'OUTILS\cu.ps1', 'OUTILS\verrou.ps1', 'OUTILS\alerte.ps1', 'OUTILS\etat.ps1', 'OUTILS\nouveau-jeu.ps1',
  'OUTILS\sim-economie.py', 'OUTILS\pousser-script.ps1', 'OUTILS\luau-verif.ps1',
  'OUTILS\verifier-python.py',
  'usine.py', 'usine.cmd', 'CONNAISSANCES\routage.json', 'OUTILS\deleguer.py', 'OUTILS\usine_opencloud.py',
  'OUTILS\retours-joueurs.py', 'OUTILS\mesures-joueurs.py', 'OUTILS\banc-luau.py', 'OUTILS\luau\faux-roblox.luau',
  'OUTILS\monter-video.py', 'OUTILS\decision-promo.py', 'OUTILS\poser-luau.ps1',
  'OUTILS\GABARITS\luau\ServerScriptService.Jeu.RetoursService.lua',
  'OUTILS\GABARITS\luau\ServerScriptService.Jeu.MesuresService.lua',
  'OUTILS\GABARITS\luau\StarterPlayer.StarterPlayerScripts.RetoursClient.client.lua'
)
foreach ($a in $attendus) { if (-not (Test-Path (Join-Path $racine $a))) { Err "manquant : $a" } }

# 2. Skills
$skills = 'usine-orchestrateur', 'usine-veille-navigateur', 'usine-fiche-concept', 'usine-revue-economie', 'usine-revue-fun',
          'usine-production-studio', 'usine-qa-multijoueur', 'usine-release', 'usine-distribution', 'usine-bilan',
          'usine-fais-un-jeu', 'usine-retours-joueurs', 'usine-promotion-video'
foreach ($s in $skills) {
  $f = Join-Path $racine "skills\$s\SKILL.md"
  if (-not (Test-Path $f)) { Err "skill manquant : $s"; continue }
  $t = (Read-Texte $f) -replace "`r", ''
  if ($t -notmatch '(?s)^---\n(.*?)\n---\n') { Err "skill $s : frontmatter absent"; continue }
  $fm = $Matches[1]
  if ($fm -notmatch "(?m)^name:\s*$([regex]::Escape($s))\s*$") { Err "skill $s : 'name' absent ou different du dossier" }
  if ($fm -match '(?m)^description:\s*(.+)$') {
    if ($Matches[1].Trim().Length -lt 30) { Err "skill $s : description trop courte" }
    if ($Matches[1].Length -gt 1024) { Err "skill $s : description de plus de 1024 caracteres" }
  } else { Err "skill $s : 'description' absente" }
}

# 3. Fichiers : vides, secrets, PowerShell, JSON
$exclus = '\\\.git\\|\\JOURNAUX\\|\\VERROUS\\|\\captures\\|\\__pycache__\\|\\OUTILS\\bin\\'
$fichiers = Get-ChildItem $racine -Recurse -File -Force | Where-Object { $_.FullName -notmatch $exclus }
$motifs = Get-MotifsSecrets
foreach ($f in $fichiers) {
  $rel = $f.FullName.Substring($racine.Length + 1)
  if ($f.Length -eq 0 -and $f.Name -ne '.gitkeep' -and $f.Name -ne 'STOP') { Err "fichier vide : $rel"; continue }
  if ($f.Extension -notin '.md', '.json', '.ps1', '.py', '.lua', '.luau', '.txt', '.csv', '') { continue }
  if ($f.Length -gt 2MB) { Avis "fichier lourd ($([int]($f.Length / 1KB)) Ko) : $rel"; continue }
  $t = Read-Texte $f.FullName
  if ($t -match '[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]') { Err "caractere de controle dans $rel (echappement mal ecrit ? cycle 2 : un NUL et deux retours chariot introduits par un script)" }
  foreach ($m in $motifs) { if ($t -match $m) { Err "SECRET probable dans $rel (motif : $($m.Substring(0, [math]::Min(18, $m.Length)))...)" } }
  if ($f.Extension -eq '.ps1') {
    $jetons = $null; $fautes = $null
    [System.Management.Automation.Language.Parser]::ParseFile($f.FullName, [ref]$jetons, [ref]$fautes) | Out-Null
    foreach ($x in $fautes) { Err "syntaxe PowerShell $rel ligne $($x.Extent.StartLineNumber) : $($x.Message)" }
    if ($t -match '[^\x00-\x7F]') { Err "caractere non ASCII dans $rel (PowerShell 5.1 le lirait mal)" }
  }
  if ($f.Extension -eq '.json') { try { $t | ConvertFrom-Json | Out-Null } catch { Err "JSON invalide : $rel" } }
}

# 3 bis. Suites de controles des outils : chacune doit passer (cycle 1 : deux defauts de calcul du simulateur
# trouves par les verificateurs ; cycle 2 : la delegation, les retours, les mesures, le banc Luau et la promotion
# ont chacun leur suite). Aucune ne lance de modele ni n'appelle un service distant.
$suites = @(
  @{ nom = "simulateur d'economie"; fichier = 'OUTILS\test-sim-economie.py' },
  @{ nom = 'delegation et routage'; fichier = 'OUTILS\test-deleguer.py' },
  @{ nom = 'retours joueurs'; fichier = 'OUTILS\test-retours-joueurs.py' },
  @{ nom = 'mesures joueurs'; fichier = 'OUTILS\test-mesures-joueurs.py' },
  @{ nom = 'banc Luau hors Studio'; fichier = 'OUTILS\test-banc-luau.py' },
  @{ nom = 'promotion video'; fichier = 'OUTILS\test-promo.py' },
  @{ nom = 'verificateur Luau'; fichier = 'OUTILS\test-luau-verif.py' },
  @{ nom = 'prevenir le proprietaire'; fichier = 'OUTILS\test-prevenir.py' },
  @{ nom = 'battement'; fichier = 'OUTILS\test-battement.py' },
  @{ nom = 'interrupteurs a distance'; fichier = 'OUTILS\test-interrupteurs.py' },
  @{ nom = 'historique des sessions'; fichier = 'OUTILS\test-historique.py' },
  @{ nom = 'jeton longue duree claude'; fichier = 'OUTILS\test-jeton-claude.py' },
  @{ nom = 'chien de garde des agents'; fichier = 'OUTILS\test-chien-de-garde.py' },
  @{ nom = 'envoi et client Studio'; fichier = 'OUTILS\test-studio.py' },
  @{ nom = 'verificateur Python'; fichier = 'OUTILS\test-verifier-python.py' }
)
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { Avis 'python absent : syntaxe Python et suites de controles des outils non verifiees' }
else {
  $env:PYTHONIOENCODING = 'utf-8'
  $preferenceAvant = $ErrorActionPreference
  try {
    $ErrorActionPreference = 'Continue'
    $sortie = & $py.Source (Join-Path $racine 'OUTILS\verifier-python.py') 2>&1
    $codePython = $LASTEXITCODE
  } finally { $ErrorActionPreference = $preferenceAvant }
  if ($codePython -ne 0) { Err ("syntaxe Python : " + ($sortie -join ' ; ')) }
  foreach ($su in $suites) {
    $f = Join-Path $racine $su.fichier
    if (-not (Test-Path $f)) { Err "manquant : $($su.fichier)"; continue }
    # unittest ecrit aussi ses succes sur stderr : seul le code de sortie fait foi.
    $preferenceAvant = $ErrorActionPreference
    try {
      $ErrorActionPreference = 'Continue'
      $sortie = & $py.Source $f 2>&1
      $codeSuite = $LASTEXITCODE
    } finally { $ErrorActionPreference = $preferenceAvant }
    if ($codeSuite -ne 0) {
      $rates = @($sortie | Where-Object { "$_" -match '^(ECHEC|echec|KO|ko)\b' } | Select-Object -First 5)
      Err ("suite '$($su.nom)' en echec (code $codeSuite) : " + ($rates -join ' ; '))
    }
  }
}

# 3 ter. Luau : chaque script de l'usine compile, et les tests Luau des gabarits passent, si les binaires sont poses.
$luauCompile = Join-Path $racine 'OUTILS\bin\luau-compile.exe'
$luau = Join-Path $racine 'OUTILS\bin\luau.exe'
if (-not (Test-Path $luauCompile)) { Avis 'binaires Luau absents de OUTILS\bin : syntaxe Luau non controlee (OUTILS\poser-luau.ps1 -Confirmer)' }
else {
  $scripts = @(Get-ChildItem (Join-Path $racine 'OUTILS') -Recurse -File | Where-Object { $_.Extension -in '.lua', '.luau' -and $_.FullName -notmatch '\\bin\\' })
  $scripts += @(Get-ChildItem (Join-Path $racine 'JEUX') -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Extension -in '.lua', '.luau' -and $_.FullName -match '\\05-production\\' })
  foreach ($sc in $scripts) {
    & $luauCompile --null $sc.FullName 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { Err "syntaxe Luau : $($sc.FullName.Substring($racine.Length + 1))" }
  }
  if (Test-Path $luau) {
    foreach ($t in @(Get-ChildItem (Join-Path $racine 'OUTILS\GABARITS\luau') -Filter 'test-*.luau' -File -ErrorAction SilentlyContinue)) {
      $sortie = & $luau $t.FullName 2>&1
      if ($LASTEXITCODE -ne 0) { Err "test Luau en echec : $($t.Name)" }
    }
  }
}

# 3 quater. Jeux : le banc hors Studio de chaque jeu en production doit passer quand il a des tests.
if ($py -and (Test-Path $luau)) {
  foreach ($j in @(Get-ChildItem (Join-Path $racine 'JEUX') -Directory)) {
    $src = Join-Path $j.FullName '05-production\src'
    $tests = Join-Path $j.FullName '05-production\tests'
    if ((Test-Path $tests) -and @(Get-ChildItem $tests -Filter '*.test.luau' -File).Count -gt 0) {
      & $py.Source (Join-Path $racine 'OUTILS\banc-luau.py') $src --tests $tests 2>&1 | Out-Null
      if ($LASTEXITCODE -ne 0) { Err "banc hors Studio en echec : $($j.Name) (python OUTILS\banc-luau.py JEUX\$($j.Name)\05-production\src --tests JEUX\$($j.Name)\05-production\tests)" }
    }
  }
}

# 4. Etat courant
if (Test-Stop) { Avis 'fichier STOP present : aucun agent ne doit agir' }
$al = Join-Path $racine 'ALERTES.md'
if (Test-Path $al) {
  $ouvertes = @((Read-Texte $al) -split "`n" | Where-Object { $_ -match '\|\s*ouverte\s*\|\s*$' })
  if ($ouvertes.Count -gt 0) { Avis "$($ouvertes.Count) alerte(s) ouverte(s) dans ALERTES.md" }
}
$ver = Join-Path $racine 'VERROUS'
if (Test-Path $ver) { foreach ($v in Get-ChildItem $ver -Filter *.lock) { Avis "verrou present : $($v.BaseName) (verrou.ps1 liste)" } }
$prop = @(Get-ChildItem (Join-Path $racine 'CONNAISSANCES\PROPOSITIONS') -Filter *.md -File | Where-Object { $_.Name -ne 'LISEZ-MOI.md' })
if ($prop.Count -gt 0) { Avis "$($prop.Count) proposition(s) en attente dans CONNAISSANCES\PROPOSITIONS" }
try {
  $libre = (Get-PSDrive ($racine.Substring(0, 1))).Free
  if ($libre -lt 2GB) { Avis ("espace libre faible : {0:N1} Go (risque de fichiers tronques)" -f ($libre / 1GB)) }
} catch { }
$crochets = (& git -C $racine config core.hooksPath) 2>$null
if ($crochets -ne 'OUTILS/hooks') { Avis 'crochets git inactifs : git config core.hooksPath OUTILS/hooks' }

if (-not $Silencieux) {
  foreach ($a in $avis) { "AVIS   : $a" }
  foreach ($e in $erreurs) { "ERREUR : $e" }
}
"verification : $($erreurs.Count) erreur(s), $($avis.Count) avis, $($fichiers.Count) fichiers controles"
if ($erreurs.Count -gt 0) { exit 1 } else { exit 0 }

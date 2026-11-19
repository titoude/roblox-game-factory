# luau-verif.ps1 - controle hors Studio des scripts d'un jeu (regles P3, P10).
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
#   luau-verif.ps1 <dossier src>
#
# 1. Toujours : aucun fichier vide, noms conformes a la convention de pousser-script.ps1.
# 2. Si les binaires officiels Luau sont presents (PATH ou OUTILS\bin\) : syntaxe (luau-compile --null)
#    et globales inconnues (luau-analyze, hors globales Roblox).
# Les binaires viennent de github.com/luau-lang/luau (luau-windows.zip). Ce script ne telecharge rien :
# OUTILS\poser-luau.ps1 -Confirmer les pose dans OUTILS\bin\ (fait le 2026-11-16).
# Codes de sortie : 0 tout est vert | 1 defaut trouve | 2 controle partiel (binaires absents) | 5 dossier introuvable
param([Parameter(Mandatory = $true, Position = 0)][string]$Dossier)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Dossier)) { Write-Output "INTROUVABLE : $Dossier"; exit 5 }
$fichiers = @(Get-ChildItem -LiteralPath $Dossier -Recurse -File | Where-Object { $_.Extension -in '.lua', '.luau' })
if ($fichiers.Count -eq 0) { Write-Output "aucun script dans $Dossier"; exit 0 }
$defauts = 0
$services = 'ServerScriptService', 'ServerStorage', 'ReplicatedStorage', 'ReplicatedFirst', 'StarterPlayer', 'StarterGui', 'StarterPack', 'Workspace', 'Lighting', 'SoundService'

foreach ($f in $fichiers) {
  if ($f.Length -eq 0) { "VIDE     : $($f.Name)"; $defauts++; continue }
  if ($f.Extension -eq '.lua' -and (($f.Name -split '\.')[0] -notin $services)) { "NOM      : $($f.Name) ne commence pas par un service Roblox"; $defauts++ }
}

function Trouver([string]$nom) {
  $c = Get-Command $nom -ErrorAction SilentlyContinue
  if ($c) { return $c.Source }
  $local = Join-Path $PSScriptRoot "bin\$nom.exe"
  if (Test-Path $local) { return $local }
  return $null
}
$compile = Trouver 'luau-compile'
$analyze = Trouver 'luau-analyze'

if (-not $compile) {
  "controle partiel : $($fichiers.Count) fichiers, $defauts defaut(s) ; syntaxe NON verifiee (luau-compile absent du PATH et de OUTILS\bin)"
  if ($defauts -gt 0) { exit 1 } else { exit 2 }
}

# Preference locale : PowerShell 5.1 transforme stderr natif en ErrorRecord.
# Capturer les deux flux avant de juger le code ou de filtrer les diagnostics.
function Executer-Natif([string]$executable, [string[]]$arguments) {
  $ErrorActionPreference = 'Continue'
  $lignes = @(& $executable @arguments 2>&1 | ForEach-Object { "$_" })
  return @{ Code = $LASTEXITCODE; Lignes = $lignes }
}

foreach ($f in $fichiers | Where-Object { $_.Length -gt 0 }) {
  $execution = Executer-Natif $compile @("--null", $f.FullName)
  $sortie = $execution.Lignes
  if ($execution.Code -ne 0) { "SYNTAXE  : $($f.Name) : $($sortie | Select-Object -First 3 | Out-String)".Trim(); $defauts++ }
}

if ($analyze) {
  $connues = 'game|workspace|script|plugin|shared|Instance|Enum|Color3|ColorSequence|ColorSequenceKeypoint|NumberSequence|NumberSequenceKeypoint|NumberRange|UDim|UDim2|Vector2|Vector3|Vector3int16|CFrame|Rect|Region3|Ray|Random|TweenInfo|BrickColor|PhysicalProperties|Font|DateTime|task|tick|time|wait|spawn|delay|warn|typeof|settings|UserSettings|utf8|bit32|buffer|debug|os|RaycastParams|OverlapParams|PathWaypoint|Faces|Axes|DockWidgetPluginGuiInfo|SharedTable|elapsedTime|version|stats'
  foreach ($f in $fichiers | Where-Object { $_.Length -gt 0 }) {
    $execution = Executer-Natif $analyze @($f.FullName)
    $lignes = $execution.Lignes | Where-Object { "$_" -match "Unknown global '([^']+)'" -and ($Matches[1] -notmatch "^($connues)$") }
    foreach ($l in $lignes) { "GLOBALE  : $l"; $defauts++ }
  }
} else { 'luau-analyze absent : globales inconnues non verifiees' }

if (-not $analyze) {
  "controle partiel : $($fichiers.Count) fichiers, $defauts defaut(s)"
  if ($defauts -gt 0) { exit 1 } else { exit 2 }
}
"controle complet : $($fichiers.Count) fichiers, $defauts defaut(s)"
if ($defauts -gt 0) { exit 1 } else { exit 0 }

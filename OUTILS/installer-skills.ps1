# installer-skills.ps1 - copie les skills de l'usine dans %USERPROFILE%\.claude\skills\. Lance par le proprietaire.
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
#   installer-skills.ps1              montre ce qui serait copie, ne copie rien
#   installer-skills.ps1 -Confirmer   copie (remplace uniquement les skills "usine-*" de meme nom)
#   installer-skills.ps1 -Retirer -Confirmer   retire les skills "usine-*" installes
#
# Ne touche a aucun autre skill. Les agents ne lancent pas ce script : installer est une decision du proprietaire (G17).
param([switch]$Confirmer, [switch]$Retirer)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'commun.ps1')
$source = Join-Path (Get-RacineUsine) 'skills'
$cible = Join-Path $env:USERPROFILE '.claude\skills'
$noms = Get-ChildItem $source -Directory | Where-Object { $_.Name -like 'usine-*' -and (Test-Path (Join-Path $_.FullName 'SKILL.md')) }
if (-not $noms) { Write-Output "INTROUVABLE : aucun skill dans $source"; exit 5 }

foreach ($n in $noms) {
  $dest = Join-Path $cible $n.Name
  $existe = Test-Path $dest
  if ($Retirer) {
    if (-not $existe) { "absent      : $($n.Name)"; continue }
    if ($Confirmer) { Remove-Item -LiteralPath $dest -Recurse -Force; "retire      : $($n.Name)" } else { "a retirer   : $dest" }
    continue
  }
  $action = if ($existe) { 'remplacer' } else { 'creer' }
  if ($Confirmer) {
    New-Item -ItemType Directory -Force $dest | Out-Null
    Copy-Item -LiteralPath (Join-Path $n.FullName 'SKILL.md') -Destination (Join-Path $dest 'SKILL.md') -Force
    "installe    : $($n.Name) ($action)"
  } else { "a $action : $dest" }
}
if (-not $Confirmer) { Write-Output "Simulation. Pour agir : powershell -File OUTILS\installer-skills.ps1 $(if ($Retirer) { '-Retirer ' })-Confirmer" }
else { Write-Output "Termine. Ouvrir une nouvelle session Claude Code pour charger les skills." }
exit 0

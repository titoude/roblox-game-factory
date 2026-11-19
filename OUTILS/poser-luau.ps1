# poser-luau.ps1 - pose les binaires officiels Luau dans OUTILS\bin\ (hors git) pour les controles hors Studio.
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
#   poser-luau.ps1            montre ce qui serait fait
#   poser-luau.ps1 -Confirmer telecharge luau-windows.zip (3 Mo environ) et pose 4 executables
#
# Source unique : https://github.com/luau-lang/luau/releases/latest/download/luau-windows.zip (depot officiel du langage).
# Rien n'est installe dans le systeme : 4 fichiers dans OUTILS\bin\, a supprimer pour revenir en arriere.
# Autorise par le proprietaire le 2026-11-16 (usine completement autonome, tout tester reellement) ; voir CONNAISSANCES\BILANS\CYCLE-2.md.
# Codes de sortie : 0 fait ou deja en place | 1 echec | 3 simulation
param([switch]$Confirmer)
$ErrorActionPreference = 'Stop'
$bin = Join-Path $PSScriptRoot 'bin'
$attendus = 'luau.exe', 'luau-compile.exe', 'luau-analyze.exe'
$manquants = @($attendus | Where-Object { -not (Test-Path (Join-Path $bin $_)) })
if ($manquants.Count -eq 0) { "deja en place : $bin"; exit 0 }
$url = 'https://github.com/luau-lang/luau/releases/latest/download/luau-windows.zip'
if (-not $Confirmer) { "simulation : telechargerait $url vers $bin ($($manquants -join ', ') manquants). Relancer avec -Confirmer."; exit 3 }
$libre = (Get-PSDrive C).Free
if ($libre -lt 200MB) { "ECHEC : moins de 200 Mo libres sur C: ($([int]($libre/1MB)) Mo)"; exit 1 }
$tmp = Join-Path ([IO.Path]::GetTempPath()) ("usine-luau-" + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force $tmp | Out-Null
try {
  $ProgressPreference = 'SilentlyContinue'
  $zip = Join-Path $tmp 'luau-windows.zip'
  Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
  if ((Get-Item $zip).Length -lt 500KB) { 'ECHEC : archive trop petite'; exit 1 }
  Expand-Archive -Path $zip -DestinationPath (Join-Path $tmp 'x') -Force
  New-Item -ItemType Directory -Force $bin | Out-Null
  foreach ($n in $attendus) {
    $src = Get-ChildItem (Join-Path $tmp 'x') -Recurse -Filter $n | Select-Object -First 1
    if (-not $src -or $src.Length -eq 0) { "ECHEC : $n absent de l'archive"; exit 1 }
    Copy-Item $src.FullName (Join-Path $bin $n) -Force
  }
  "pose : $($attendus -join ', ') dans $bin"
  exit 0
} finally { Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue }

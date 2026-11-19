# pousser-script.ps1 - fabrique le Luau qui cree ou met a jour un script dans Studio (a passer a execute_luau, mode Edit).
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
#   pousser-script.ps1 <fichier.lua> [-Sortie <fichier.luau>]
#
# Le nom du fichier donne le chemin de l'instance et sa classe :
#   ServerScriptService.Jeu.Amorce.server.lua                     -> Script        ServerScriptService.Jeu.Amorce
#   ServerScriptService.Jeu.EconomieService.lua                   -> ModuleScript  ServerScriptService.Jeu.EconomieService
#   StarterPlayer.StarterPlayerScripts.Interface.client.lua       -> LocalScript   StarterPlayer.StarterPlayerScripts.Interface
# Les dossiers intermediaires absents sont crees (Folder). Une instance existante d'une autre classe fait echouer l'envoi.
# Ce script n'ecrit rien dans Studio : il imprime du Luau. L'envoi exige le verrou place:<placeId> (G1).
# Non verifie dans Studio au 15/11/2026 : premier usage a faire sur une place de test.
param(
  [Parameter(Mandatory = $true, Position = 0)][string]$Fichier,
  [string]$Sortie
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'commun.ps1')
if (-not (Test-Path -LiteralPath $Fichier)) { Write-Output "INTROUVABLE : $Fichier"; exit 5 }
$item = Get-Item -LiteralPath $Fichier
if ($item.Length -eq 0) { Write-Output "REFUS : fichier vide (regle P10) : $Fichier"; exit 1 }

$nom = $item.Name
if ($nom -notmatch '\.lua$') { Write-Output 'USAGE : fichier .lua attendu.'; exit 2 }
$base = $nom -replace '\.lua$', ''
$classe = 'ModuleScript'
if ($base -match '\.server$') { $classe = 'Script'; $base = $base -replace '\.server$', '' }
elseif ($base -match '\.client$') { $classe = 'LocalScript'; $base = $base -replace '\.client$', '' }
$segments = $base -split '\.'
$services = 'ServerScriptService', 'ServerStorage', 'ReplicatedStorage', 'ReplicatedFirst', 'StarterPlayer', 'StarterGui', 'StarterPack', 'Workspace', 'Lighting', 'SoundService'
if ($segments.Count -lt 2 -or $segments[0] -notin $services) { Write-Output ("USAGE : le nom doit commencer par un service (" + ($services -join ', ') + ") suivi du chemin.") ; exit 2 }
foreach ($s in $segments) { if ($s -notmatch '^[A-Za-z_][A-Za-z0-9_]*$') { Write-Output "USAGE : segment de chemin invalide '$s'."; exit 2 } }

$source = (Read-Texte $item.FullName) -replace "`r`n", "`n"
# Niveau de crochet long absent de la source.
$niveau = 1
while ($source.Contains(']' + ('=' * $niveau) + ']')) { $niveau++ }
$egal = '=' * $niveau

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('-- Genere par OUTILS\pousser-script.ps1 depuis ' + $nom + ' : ne pas editer a la main.')
[void]$sb.AppendLine('local parent = game:GetService("' + $segments[0] + '")')
for ($i = 1; $i -lt $segments.Count - 1; $i++) {
  [void]$sb.AppendLine('do')
  [void]$sb.AppendLine('  local enfant = parent:FindFirstChild("' + $segments[$i] + '")')
  [void]$sb.AppendLine('  if not enfant then enfant = Instance.new("Folder"); enfant.Name = "' + $segments[$i] + '"; enfant.Parent = parent end')
  [void]$sb.AppendLine('  parent = enfant')
  [void]$sb.AppendLine('end')
}
$dernier = $segments[$segments.Count - 1]
[void]$sb.AppendLine('local cible = parent:FindFirstChild("' + $dernier + '")')
[void]$sb.AppendLine('if cible and cible.ClassName ~= "' + $classe + '" then')
[void]$sb.AppendLine('  error("classe inattendue pour " .. cible:GetFullName() .. " : " .. cible.ClassName .. " (attendu ' + $classe + ')")')
[void]$sb.AppendLine('end')
[void]$sb.AppendLine('local cree = false')
[void]$sb.AppendLine('if not cible then cible = Instance.new("' + $classe + '"); cible.Name = "' + $dernier + '"; cible.Parent = parent; cree = true end')
[void]$sb.Append('local source = [' + $egal + "[`n")
[void]$sb.Append($source)
[void]$sb.AppendLine(']' + $egal + ']')
[void]$sb.AppendLine('cible.Source = source')
[void]$sb.AppendLine('return (cree and "cree " or "mis a jour ") .. cible:GetFullName() .. " (" .. #source .. " caracteres)"')
$luau = $sb.ToString() -replace "`r`n", "`n"

if ($Sortie) {
  Write-Sur $Sortie $luau
  Write-Output "Luau ecrit : $Sortie ($($luau.Length) caracteres) pour $classe $($segments -join '.')"
} else { Write-Output $luau }
exit 0

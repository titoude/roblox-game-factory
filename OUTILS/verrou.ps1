# verrou.ps1 - un seul agent par ressource (G1, G3).
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
#   verrou.ps1 prendre <ressource> -agent <nom> [-objet "<quoi>"] [-minutes 120] [-forcer]
#   verrou.ps1 rendre  <ressource> -agent <nom> [-forcer]
#   verrou.ps1 voir    <ressource>
#   verrou.ps1 liste
#
# Ressources : place:<placeId> | bureau | chrome:<nom d'onglet ou d'agent> | studio
# -forcer : reserve a l'orchestrateur, pour reprendre un verrou expire ou orphelin apres avoir verifie
#           qu'aucun agent ne travaille. Chaque usage est journalise.
# Codes de sortie : 0 ok | 2 usage | 3 arret (STOP) | 4 verrou detenu par un autre
param(
  [Parameter(Position=0)][string]$action = 'liste',
  [Parameter(Position=1)][string]$ressource,
  [string]$agent,
  [string]$objet = '',
  [int]$minutes = 120,
  [switch]$forcer
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'commun.ps1')
$dos = Join-Path (Get-RacineUsine) 'VERROUS'
if (-not (Test-Path $dos)) { New-Item -ItemType Directory -Force $dos | Out-Null }

function Chemin([string]$r) {
  if ($r -notmatch '^(place:\d+|bureau|studio|chrome:[A-Za-z0-9_-]+)$') { Write-Output "USAGE : ressource invalide '$r' (place:<id>, bureau, studio, chrome:<nom>)."; exit 2 }
  Join-Path $dos (($r -replace ':', '_') + '.lock')
}
function Lire([string]$f) { try { Read-Texte $f | ConvertFrom-Json } catch { $null } }
function EnDate($x) {
  if ($x -is [datetime]) { return $x.ToUniversalTime() }
  [datetime]::Parse([string]$x, [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
}
function Decrire($v) {
  $age = [int][math]::Floor(((Get-Date).ToUniversalTime() - (EnDate $v.depuis)).TotalMinutes)
  $exp = if ((Get-Date).ToUniversalTime() -gt (EnDate $v.expire)) { ' EXPIRE' } else { '' }
  "{0} | agent {1} | depuis {2} min{3} | {4}" -f $v.ressource, $v.agent, $age, $exp, $v.objet
}

switch ($action) {
  'liste' {
    $tous = Get-ChildItem $dos -Filter *.lock -ErrorAction SilentlyContinue
    if (-not $tous) { 'aucun verrou' }
    foreach ($t in $tous) { $v = Lire $t.FullName; if ($v) { Decrire $v } else { "$($t.Name) | illisible" } }
  }
  'voir' {
    $f = Chemin $ressource
    if (Test-Path $f) { Decrire (Lire $f) } else { "libre : $ressource" }
  }
  'prendre' {
    if (Test-Stop) { Write-Output 'ARRET : fichier STOP present.'; exit 3 }
    if (-not $agent) { Write-Output 'USAGE : -agent obligatoire.'; exit 2 }
    $f = Chemin $ressource
    $maintenant = (Get-Date).ToUniversalTime()
    $contenu = @{ ressource = $ressource; agent = $agent; objet = $objet; depuis = $maintenant.ToString('o'); expire = $maintenant.AddMinutes($minutes).ToString('o') } | ConvertTo-Json -Compress
    if (Test-Path $f) {
      $v = Lire $f
      if ($v -and $v.agent -eq $agent) {
        Write-Sur $f $contenu
        Add-Journal 'verrous.log' "renouvele $ressource par $agent"
        Write-Output "verrou renouvele : $ressource par $agent ($minutes min)"; exit 0
      }
      if (-not $forcer) {
        Write-Output ("REFUS : " + $(if ($v) { Decrire $v } else { "$ressource detenu (fichier illisible)" }))
        Write-Output "Attendre, ou demander a l'orchestrateur : seul lui peut reprendre un verrou (-forcer) apres verification."
        exit 4
      }
      Add-Journal 'verrous.log' "FORCE $ressource : repris par $agent a $(if ($v) { $v.agent } else { '?' })"
      Remove-Item -LiteralPath $f -Force
    }
    try {
      $flux = [IO.File]::Open($f, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
      $octets = $script:Utf8SansBom.GetBytes($contenu)
      $flux.Write($octets, 0, $octets.Length); $flux.Close()
    } catch [IO.IOException] {
      Write-Output "REFUS : $ressource vient d'etre pris par un autre agent."; exit 4
    }
    Add-Journal 'verrous.log' "pris $ressource par $agent ($objet)"
    Write-Output "verrou pris : $ressource par $agent ($minutes min)"
  }
  'rendre' {
    if (-not $agent) { Write-Output 'USAGE : -agent obligatoire.'; exit 2 }
    $f = Chemin $ressource
    if (-not (Test-Path $f)) { Write-Output "deja libre : $ressource"; exit 0 }
    $v = Lire $f
    if ($v -and $v.agent -ne $agent -and -not $forcer) { Write-Output ("REFUS : " + (Decrire $v)); exit 4 }
    Remove-Item -LiteralPath $f -Force
    Add-Journal 'verrous.log' ("rendu $ressource par $agent" + $(if ($forcer) { ' (FORCE)' } else { '' }))
    Write-Output "verrou rendu : $ressource"
  }
  default { Write-Output "USAGE : verrou.ps1 prendre|rendre|voir|liste <ressource> -agent <nom>"; exit 2 }
}
exit 0

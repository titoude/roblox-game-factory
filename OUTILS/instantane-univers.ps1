# instantane-univers.ps1 - releve ponctuel du CCU d'univers deja reperes, par l'API publique documentee de Roblox.
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
#   instantane-univers.ps1 -Liste <fichier.txt> [-Sortie <fichier.csv>]
#   instantane-univers.ps1 -Liste <fichier.txt> -Simulation <reponse.json>   (aucun appel reseau : test du format)
#
# -Liste : un universeId par ligne ; "#" commence un commentaire. 50 au plus.
# Un seul appel GET a https://games.roblox.com/v1/games?universeIds=... , sans compte, sans cle, sans cookie.
# Gardes (G11, CONNAISSANCES\SOURCES-VEILLE.md) : fichier STOP ; 15 minutes au moins entre deux appels ;
# aucun nouvel essai apres un refus ou une erreur ; aucune donnee de joueur.
# Sert a dater le CCU de jeux connus, pas a explorer le catalogue.
# Codes de sortie : 0 ok | 2 usage | 3 arret (STOP, delai, refus du serveur) | 5 introuvable
param(
  [Parameter(Mandatory = $true)][string]$Liste,
  [string]$Sortie,
  [string]$Simulation
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'commun.ps1')
$racine = Get-RacineUsine
if (Test-Stop) { Write-Output 'ARRET : fichier STOP present.'; exit 3 }
if (-not (Test-Path -LiteralPath $Liste)) { Write-Output "INTROUVABLE : $Liste"; exit 5 }
if (-not $Sortie) { $Sortie = Join-Path $racine 'VEILLE\instantanes.csv' }

$ids = @(Get-Content -LiteralPath $Liste | ForEach-Object { ($_ -split '#')[0].Trim() } | Where-Object { $_ } | Select-Object -Unique)
foreach ($i in $ids) { if ($i -notmatch '^\d{3,15}$') { Write-Output "USAGE : identifiant invalide '$i'."; exit 2 } }
if ($ids.Count -eq 0) { Write-Output 'USAGE : liste vide.'; exit 2 }
if ($ids.Count -gt 50) { Write-Output "USAGE : $($ids.Count) univers, 50 au plus par appel."; exit 2 }

$url = 'https://games.roblox.com/v1/games?universeIds=' + ($ids -join ',')
$utc = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

if ($Simulation) {
  if (-not (Test-Path -LiteralPath $Simulation)) { Write-Output "INTROUVABLE : $Simulation"; exit 5 }
  $json = Read-Texte $Simulation | ConvertFrom-Json
  $mode = 'simulation'
} else {
  $marque = Join-Path $racine 'JOURNAUX\instantane-dernier.txt'
  if (Test-Path $marque) {
    $dernier = [datetime]::Parse((Get-Content $marque -TotalCount 1), [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
    $attente = 15 - ((Get-Date).ToUniversalTime() - $dernier).TotalMinutes
    if ($attente -gt 0) { Write-Output ("ARRET : dernier appel il y a moins de 15 minutes (encore {0:N0} min)." -f [math]::Ceiling($attente)); exit 3 }
  }
  if (-not (Test-Path (Split-Path $marque))) { New-Item -ItemType Directory -Force (Split-Path $marque) | Out-Null }
  Set-Content -LiteralPath $marque -Value $utc -Encoding ASCII
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  try {
    $rep = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 20 -UserAgent 'veille-roblox/1.0' -Headers @{ Accept = 'application/json' }
  } catch {
    $code = ''
    if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode }
    Add-Journal 'instantanes.log' "refus ou erreur ($code) pour $($ids.Count) univers"
    Write-Output "ARRET : le serveur a repondu $code ($($_.Exception.Message)). Aucun nouvel essai : noter l'echec, reessayer au tour de veille suivant."
    exit 3
  }
  $json = $rep.Content | ConvertFrom-Json
  $mode = 'reseau'
  Add-Journal 'instantanes.log' "ok $($ids.Count) univers"
}

function Csv([object]$v) { $s = [string]$v; if ($s -match '[",;\r\n]') { '"' + ($s -replace '"', '""' -replace '[\r\n]+', ' ') + '"' } else { $s } }
$lignes = New-Object System.Collections.Generic.List[string]
$vus = @{}
foreach ($g in @($json.data)) {
  $vus[[string]$g.id] = $true
  $lignes.Add((@($utc, $g.id, (Csv $g.name), $g.playing, $g.visits, $g.favoritedCount, $g.created, $g.updated, (Csv $g.creator.name), 'observe', (Csv $url)) -join ','))
}
foreach ($i in $ids) { if (-not $vus.ContainsKey($i)) { $lignes.Add((@($utc, $i, '', 'NP', 'NP', 'NP', '', '', '', 'absent de la reponse', (Csv $url)) -join ',')) } }

$entete = 'releve_utc,universeId,nom,ccu,visites,favoris,cree,modifie,proprietaire,statut,source'
if ($mode -eq 'simulation') {
  Write-Output $entete; $lignes | ForEach-Object { Write-Output $_ }
  Write-Output "simulation : $($lignes.Count) lignes, rien n'est ecrit."
  exit 0
}
$avant = if (Test-Path -LiteralPath $Sortie) { (Read-Texte $Sortie).TrimEnd() } else { $entete }
Write-Sur $Sortie ($avant + "`n" + ($lignes -join "`n") + "`n")
Write-Output "$($lignes.Count) lignes ajoutees a $Sortie (une valeur absente est notee NP, jamais 0)."
exit 0

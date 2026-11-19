# commun.ps1 - fonctions partagees par les outils de l'usine. A charger par : . (Join-Path $PSScriptRoot 'commun.ps1')
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.

$script:Utf8SansBom = New-Object System.Text.UTF8Encoding($false)

function Get-RacineUsine { Split-Path -Parent $PSScriptRoot }

function Test-Stop { Test-Path (Join-Path (Get-RacineUsine) 'STOP') }

function Read-Texte([string]$chemin) { [IO.File]::ReadAllText($chemin, $script:Utf8SansBom) }

# Ecriture sure (regle P10) : fichier temporaire, relecture, remplacement. Refuse un resultat vide.
function Write-Sur([string]$chemin, [string]$texte) {
  if ([string]::IsNullOrEmpty($texte)) { throw "ecriture refusee : contenu vide pour $chemin" }
  $tmp = "$chemin.tmp"
  [IO.File]::WriteAllText($tmp, $texte, $script:Utf8SansBom)
  $relu = [IO.File]::ReadAllText($tmp, $script:Utf8SansBom)
  if ($relu -ne $texte) {
    Remove-Item -LiteralPath $tmp -ErrorAction SilentlyContinue
    throw "ecriture incomplete : $chemin (disque plein ?)"
  }
  Move-Item -LiteralPath $tmp -Destination $chemin -Force
}

function Add-Journal([string]$fichier, [string]$texte) {
  try {
    $dos = Join-Path (Get-RacineUsine) 'JOURNAUX'
    if (-not (Test-Path $dos)) { New-Item -ItemType Directory -Force $dos | Out-Null }
    $ligne = "{0} | {1}" -f (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'), $texte
    [IO.File]::AppendAllText((Join-Path $dos $fichier), $ligne + "`r`n", $script:Utf8SansBom)
  } catch { }
}

# Motifs de secrets (G9). Assembles par morceaux pour que ce fichier ne se detecte pas lui-meme.
function Get-MotifsSecrets {
  @(
    ('_\|WARN' + 'ING:-DO-NOT-SHARE'),
    ('discord(app)?\.com/api/(v\d+/)?webhooks/\d{6,}/[A-Za-z0-9_-]{20,}'),
    ('x-api-key\s*[:=]\s*["'']?[A-Za-z0-9+/=_-]{24,}'),
    ('ROBLOSECURITY\s*[:=]\s*["'']?[A-Za-z0-9_|:-]{24,}'),
    ('sk-(ant|proj)-[A-Za-z0-9_-]{16,}'),
    ('-----BEGIN [A-Z ]*PRIVATE KEY-----')
  )
}

function Test-Secret([string]$texte) {
  foreach ($m in Get-MotifsSecrets) { if ($texte -match $m) { return $true } }
  return $false
}

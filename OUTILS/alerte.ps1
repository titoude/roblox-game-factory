# alerte.ps1 - signale un arret sur une frontiere humaine (G7) dans ALERTES.md.
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
#   alerte.ps1 -type <captcha|conditions|2fa|connexion|paiement|permission|propriete|plafond|autre>
#              -message "<ce qui est a l'ecran, ou, ce qui est bloque>" [-agent <nom>] [-jeu <slug>] [-etape <nn-nom>]
#
# N'ecrit jamais de secret : le message est refuse s'il en contient un.
# L'orchestrateur ferme une alerte en remplacant "ouverte" par "close le <date> : <raison>" dans ALERTES.md.
param(
  [Parameter(Mandatory = $true)][ValidateSet('captcha', 'conditions', '2fa', 'connexion', 'paiement', 'permission', 'propriete', 'plafond', 'autre')][string]$type,
  [Parameter(Mandatory = $true)][string]$message,
  [string]$agent = $env:USINE_AGENT,
  [string]$jeu = '-',
  [string]$etape = '-'
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'commun.ps1')
if (-not $agent) { $agent = 'inconnu' }
if (Test-Secret $message) { Write-Output 'REFUS : le message contient un secret. Decrire l''ecran sans recopier de cle, de jeton ni d''URL de webhook.'; exit 2 }

$f = Join-Path (Get-RacineUsine) 'ALERTES.md'
$propre = ($message -replace '\r?\n', ' ' -replace '\|', '/').Trim()
$ligne = "| {0} | {1} | {2} | {3} | {4} | {5} | ouverte |" -f (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm') , $type, $agent, $jeu, $etape, $propre
if (Test-Path $f) { $avant = (Read-Texte $f).TrimEnd() } else { $avant = "# Alertes`n`n| Date (UTC) | Type | Agent | Jeu | Etape | Constat | Statut |`n|---|---|---|---|---|---|---|" }
Write-Sur $f ($avant + "`n" + $ligne + "`n")
Add-Journal 'alertes.log' "$type | $agent | $jeu | $propre"
try { [console]::Beep(880, 250) } catch { }
# Prevenir le proprietaire la ou il est (procedure 14). Meme cle d'anti-repetition que OUTILS\battement.py.
# Le message envoye ne recopie pas le constat : il renvoie a ALERTES.md (aucun detail sensible hors du poste).
try {
  $canon = ($ligne.Trim('|').Split('|')[0..4] | ForEach-Object { $_.Trim() }) -join '|'
  $sha = [Security.Cryptography.SHA256]::Create()
  try { $cleContact = 'alerte-' + ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($canon))).Replace('-', '').ToLowerInvariant().Substring(0, 24)) } finally { $sha.Dispose() }
  $niveauContact = if ($type -in @('connexion', 'paiement', 'captcha', '2fa')) { 'urgent' } else { 'important' }
  $py = Get-Command python -ErrorAction SilentlyContinue
  if ($py) { & $py.Source (Join-Path $PSScriptRoot 'prevenir.py') envoyer --niveau $niveauContact --sujet 'Action du proprietaire requise' --texte 'Une alerte est ouverte. Consulter ALERTES.md sur le poste.' --cle $cleContact 2>&1 | Out-Null }
} catch { }
Write-Output "alerte ecrite dans ALERTES.md : $type - $propre"
Write-Output 'Ne pas contourner, ne pas retenter. Passer a un travail qui n''en depend pas, ou rendre la main (RESULTAT: arret).'
exit 0

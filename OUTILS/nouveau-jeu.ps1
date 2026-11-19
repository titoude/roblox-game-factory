# nouveau-jeu.ps1 - cree le dossier d'un jeu a partir des gabarits. Lance par l'orchestrateur.
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
#   nouveau-jeu.ps1 -Slug <minuscules-chiffres-tirets> -Nom "<nom de travail>"
#
# Cree JEUX\<slug>\ (ETAT.json, JOURNAL.md, dossiers d'etape, gabarits) et ajoute la ligne au journal des jeux.
# Ne touche ni a Studio ni a Roblox.
param(
  [Parameter(Mandatory = $true)][string]$Slug,
  [Parameter(Mandatory = $true)][string]$Nom
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'commun.ps1')
if (Test-Stop) { Write-Output 'ARRET : fichier STOP present.'; exit 3 }
if ($Slug -cnotmatch '^[a-z0-9][a-z0-9-]{2,39}$') { Write-Output 'USAGE : -Slug en minuscules, chiffres et tirets, 3 a 40 caracteres.'; exit 2 }
$racine = Get-RacineUsine
$dos = Join-Path $racine "JEUX\$Slug"
if (Test-Path $dos) { Write-Output "REFUS : $dos existe deja."; exit 4 }
$gab = Join-Path $racine 'OUTILS\GABARITS'
$jour = Get-Date -Format 'yyyy-MM-dd'

$copies = @(
  @('FICHE-CONCEPT.md', '02-concept\FICHE-CONCEPT.md'),
  @('economie.exemple.json', '03-economie\economie.json'),
  @('RAPPORT-ECONOMIE.md', '03-economie\RAPPORT-ECONOMIE.md'),
  @('RAPPORT-FUN.md', '04-fun\RAPPORT-FUN.md'),
  @('PLAN-PRODUCTION.md', '05-production\PLAN-PRODUCTION.md'),
  @('JOURNAL-LOTS.md', '05-production\JOURNAL-LOTS.md'),
  @('RAPPORT-QA.md', '06-qa\RAPPORT-QA-1.md'),
  @('CHECKLIST-RELEASE.md', '07-release\CHECKLIST-RELEASE.md'),
  @('MANIFESTE-IDS.json', '07-release\MANIFESTE-IDS.json'),
  @('KIT-LANCEMENT.md', '08-distribution\KIT-LANCEMENT.md'),
  @('JOURNAL-CAMPAGNES.md', '08-distribution\JOURNAL-CAMPAGNES.md'),
  @('BILAN.md', '09-bilan\BILAN.md')
)
foreach ($c in $copies) { if (-not (Test-Path (Join-Path $gab $c[0]))) { Write-Output "INTROUVABLE : gabarit $($c[0])"; exit 5 } }

foreach ($d in '02-concept', '03-economie', '04-fun', '05-production\src', '06-qa', '07-release', '08-distribution', '09-bilan') {
  New-Item -ItemType Directory -Force (Join-Path $dos $d) | Out-Null
}
foreach ($c in $copies) {
  $texte = (Read-Texte (Join-Path $gab $c[0])).Replace('<slug>', $Slug).Replace('<nom>', $Nom).Replace('<date>', $jour)
  Write-Sur (Join-Path $dos $c[1]) $texte
}
Write-Sur (Join-Path $dos '05-production\src\.gitkeep') "`n"

$etat = [ordered]@{
  slug = $Slug; nom = $Nom; cree_le = $jour; etape = '02-concept'; statut = 'en_cours'; blocage = ''
  place = [ordered]@{ universeId_test = ''; placeId_test = ''; universeId_prod = ''; placeId_prod = '' }
  portes = [ordered]@{}
  mode_degrade = @()
  historique = @([ordered]@{ date = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm'); evenement = 'jeu cree' })
}
Write-Sur (Join-Path $dos 'ETAT.json') ($etat | ConvertTo-Json -Depth 8)

$journal = "# Journal - $Nom ($Slug)`n`nUne ligne par delegation ou decision. Tenu par l'orchestrateur.`n`n| Date (UTC) | Etape | Agent (modele, effort) | Duree | Resultat | Fichier |`n|---|---|---|---|---|---|`n| $jour | 02-concept | orchestrateur | - | jeu cree | ETAT.json |`n"
Write-Sur (Join-Path $dos 'JOURNAL.md') $journal

$jj = Join-Path $racine 'CONNAISSANCES\JOURNAL-DES-JEUX.md'
$t = Read-Texte $jj
$ligne = "| $Slug | $Nom | $jour | 02 Concept | - | en cours | - |"
$repere = "`n## Compteurs"
$i = $t.IndexOf($repere)
if ($i -gt 0) { $t = $t.Substring(0, $i).TrimEnd() + "`n" + $ligne + "`n" + $t.Substring($i) } else { $t = $t.TrimEnd() + "`n" + $ligne + "`n" }
Write-Sur $jj $t

Write-Output "jeu cree : JEUX\$Slug (etape 02-concept)"
Write-Output "suite : PROCEDURES\02-CONCEPT.md ; commit prefixe [orchestrateur] (le journal des jeux a change)."
exit 0

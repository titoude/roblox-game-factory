# etat.ps1 - etat de la chaine pour chaque jeu (JEUX\<slug>\ETAT.json). Tenu par l'orchestrateur.
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
#   etat.ps1 -Liste                                         tous les jeux
#   etat.ps1 -Seuils                                        valeurs de CONNAISSANCES\seuils.json
#   etat.ps1 -Jeu <slug>                                    detail d'un jeu
#   etat.ps1 -Jeu <slug> -Porte P2 -Resultat passe|echec|derogation|a_confirmer -Preuve <fichier> [-Note "<raison>"]
#       a_confirmer : avis d'une revue non independante ou en mode degrade (regle A8). N'avance pas l'etape,
#       ne compte pas d'iteration ; la porte se rejoue avec le bon modele.
#   etat.ps1 -Jeu <slug> -Porte P3 -RemiseAZero -Note "<raison>"   remet a zero le compteur d'iterations d'une porte
#   etat.ps1 -Jeu <slug> -Etape 05-production               forcer l'etape courante
#   etat.ps1 -Jeu <slug> -Statut en_cours|bloque|arrete|termine [-Note "<raison>"]
#   etat.ps1 -Jeu <slug> -Degrade "<etape : repli utilise>" noter un mode degrade
#
# Une porte passee fait avancer l'etape (sauf P0, P4 et P7 : P0 juge le corpus de veille du theme, P4 et P7 sont
# internes a leur etape ; P10 retours joueurs et P11 promotion sont des boucles d'exploitation). Un echec compte une iteration.
# Une derogation exige -Note et reste visible au bilan.
param(
  [switch]$Liste,
  [switch]$Seuils,
  [string]$Jeu,
  [string]$Porte,
  [string]$Resultat,
  [string]$Preuve = '',
  [string]$Note = '',
  [string]$Etape,
  [string]$Statut,
  [string]$Degrade,
  [switch]$RemiseAZero
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'commun.ps1')
$racine = Get-RacineUsine
$ordre = '02-concept', '03-economie', '04-fun', '05-production', '06-qa', '07-release', '08-distribution', '09-bilan'
$etapeDe = @{ P0 = '02-concept'; P1 = '02-concept'; P2 = '03-economie'; P3 = '04-fun'; P4 = '05-production'; P5 = '06-qa'; P6 = '07-release'; P7 = '08-distribution'; P8 = '08-distribution'; P9 = '09-bilan'; P10 = '08-distribution'; P11 = '08-distribution' }
$sansAvance = 'P0', 'P4', 'P7', 'P10', 'P11'
$iterMax = @{ P1 = @('concept', 'iterations_max'); P2 = @('economie', 'iterations_max'); P3 = @('fun', 'iterations_max'); P5 = @('qa', 'cycles_max') }

function Charger([string]$slug) {
  $f = Join-Path $racine "JEUX\$slug\ETAT.json"
  if (-not (Test-Path $f)) { Write-Output "INTROUVABLE : $f"; exit 5 }
  [pscustomobject]@{ Fichier = $f; Etat = (Read-Texte $f | ConvertFrom-Json) }
}
function Sauver($c) { Write-Sur $c.Fichier ($c.Etat | ConvertTo-Json -Depth 8) }
function Poser($objet, [string]$nom, $valeur) { $objet | Add-Member -NotePropertyName $nom -NotePropertyValue $valeur -Force }
function Historique($etat, [string]$texte) {
  $h = @($etat.historique) + [pscustomobject]@{ date = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm'); evenement = $texte }
  Poser $etat 'historique' $h
}
function Resumer($e) {
  $p = @()
  foreach ($n in ($e.portes.PSObject.Properties.Name | Sort-Object)) { $v = $e.portes.$n; if ($v.resultat) { $p += "$n=$($v.resultat)" + $(if ($v.iterations -gt 0) { "($($v.iterations) echec)" } else { '' }) } }
  "{0} | {1} | {2} | {3}{4}" -f $e.slug, $e.etape, $e.statut, $(if ($p) { $p -join ' ' } else { 'aucune porte jugee' }), $(if ($e.blocage) { " | blocage : $($e.blocage)" } else { '' })
}

if ($Seuils) {
  $s = Read-Texte (Join-Path $racine 'CONNAISSANCES\seuils.json') | ConvertFrom-Json
  "seuils version $($s.version) du $($s.maj) - $($s.statut)"
  foreach ($sec in $s.PSObject.Properties) {
    if ($sec.Value -is [pscustomobject]) { foreach ($k in $sec.Value.PSObject.Properties) { "  {0}.{1} = {2}" -f $sec.Name, $k.Name, (@($k.Value) -join ', ') } }
  }
  exit 0
}

if ($Liste -or -not $Jeu) {
  $tous = Get-ChildItem (Join-Path $racine 'JEUX') -Directory -ErrorAction SilentlyContinue | Where-Object { Test-Path (Join-Path $_.FullName 'ETAT.json') }
  if (-not $tous) { 'aucun jeu' }
  foreach ($t in $tous) { Resumer (Read-Texte (Join-Path $t.FullName 'ETAT.json') | ConvertFrom-Json) }
  if (Test-Stop) { 'ATTENTION : fichier STOP present, aucun agent ne doit agir.' }
  exit 0
}

$c = Charger $Jeu
$e = $c.Etat
$modifie = $false

if ($Porte -and $RemiseAZero) {
  if (-not $Note) { Write-Output 'USAGE : -RemiseAZero exige -Note "<raison>".'; exit 2 }
  $avant = $e.portes.$Porte
  if (-not $avant) { Write-Output "INTROUVABLE : porte $Porte jamais jugee."; exit 5 }
  Poser $avant 'iterations' 0
  Historique $e "porte $Porte : compteur d'iterations remis a zero - $Note"
  "porte $Porte : compteur remis a zero"
  $modifie = $true
} elseif ($Porte) {
  if (-not $etapeDe.ContainsKey($Porte)) { Write-Output "USAGE : porte inconnue '$Porte' (P0 a P11)."; exit 2 }
  if ($Resultat -notin 'passe', 'echec', 'derogation', 'a_confirmer') { Write-Output 'USAGE : -Resultat passe|echec|derogation|a_confirmer.'; exit 2 }
  if ($Resultat -in 'derogation', 'a_confirmer' -and -not $Note) { Write-Output 'USAGE : derogation et a_confirmer exigent -Note "<raison>".'; exit 2 }
  if ($Resultat -ne 'echec' -and -not $Preuve) { Write-Output 'USAGE : -Preuve <fichier> obligatoire (sauf pour un echec).'; exit 2 }
  if ($Preuve -and -not (Test-Path (Join-Path $racine $Preuve)) -and -not (Test-Path $Preuve)) { Write-Output "INTROUVABLE : preuve $Preuve"; exit 5 }
  $avant = $e.portes.$Porte
  $iter = 0
  if ($avant -and $avant.iterations) { $iter = [int]$avant.iterations }
  if ($Resultat -eq 'echec') { $iter++ }
  Poser $e.portes $Porte ([pscustomobject]@{ resultat = $Resultat; date = (Get-Date -Format 'yyyy-MM-dd'); preuve = $Preuve; note = $Note; iterations = $iter })
  Historique $e "porte $Porte : $Resultat $(if ($Note) { '- ' + $Note })"
  if ($Resultat -eq 'echec') {
    if ($iterMax.ContainsKey($Porte)) {
      $s = Read-Texte (Join-Path $racine 'CONNAISSANCES\seuils.json') | ConvertFrom-Json
      $max = [int]$s.($iterMax[$Porte][0]).($iterMax[$Porte][1])
      "porte $Porte : echec $iter sur $max"
      if ($iter -gt $max) { "ARRET CONSEILLE : echec apres $max retours au concepteur (PROCEDURES\00-ORCHESTRATION.md section 6, regle A5)." }
      elseif ($iter -eq $max) { "DERNIER RETOUR : encore un echec et l'idee est abandonnee (regle A5)." }
    } else { "porte $Porte : echec $iter" }
  } elseif ($Resultat -eq 'a_confirmer') {
    "porte $Porte a confirmer : avis enregistre, ni avance ni iteration (regle A8 : revue non independante ou mode degrade)"
  } elseif ($Porte -eq 'P9') {
    Poser $e 'statut' 'termine'; "porte P9 passee : jeu termine"
  } elseif ($Porte -notin $sansAvance) {
    $i = [array]::IndexOf($ordre, $etapeDe[$Porte])
    if ($i -ge 0 -and $i -lt $ordre.Count - 1) { Poser $e 'etape' $ordre[$i + 1]; "porte $Porte $Resultat : etape suivante $($ordre[$i + 1])" }
  } else { "porte $Porte $Resultat (l'etape $($e.etape) continue)" }
  $modifie = $true
}
if ($Etape) {
  if ($Etape -notin $ordre) { Write-Output ("USAGE : etape inconnue. Valeurs : " + ($ordre -join ', ')); exit 2 }
  Poser $e 'etape' $Etape; Historique $e "etape forcee : $Etape $(if ($Note) { '- ' + $Note })"; $modifie = $true
}
if ($Statut) {
  if ($Statut -notin 'en_cours', 'bloque', 'arrete', 'termine') { Write-Output 'USAGE : -Statut en_cours|bloque|arrete|termine.'; exit 2 }
  if ($Statut -in 'bloque', 'arrete' -and -not $Note) { Write-Output 'USAGE : -Note "<raison>" obligatoire pour bloque ou arrete.'; exit 2 }
  Poser $e 'statut' $Statut
  Poser $e 'blocage' $(if ($Statut -eq 'bloque') { $Note } else { '' })
  Historique $e "statut : $Statut $(if ($Note) { '- ' + $Note })"; $modifie = $true
}
if ($Degrade) {
  Poser $e 'mode_degrade' (@($e.mode_degrade) + $Degrade); Historique $e "mode degrade : $Degrade"; $modifie = $true
}
if ($modifie) { Sauver $c }
Resumer $e
if (-not $modifie) {
  if ($e.mode_degrade) { "modes degrades : " + (@($e.mode_degrade) -join ' ; ') }
  foreach ($h in @($e.historique) | Select-Object -Last 8) { "  $($h.date) $($h.evenement)" }
}
exit 0

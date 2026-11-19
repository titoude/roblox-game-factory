# cu.ps1 - controle leger du bureau Windows pour les agents de l'usine (capture, clic, frappe).
# ASCII volontaire : PowerShell 5.1 lit un .ps1 sans BOM en ANSI.
#
# Lecture (sans effet sur le bureau) :
#   cu.ps1 shot <out.png> [full]               capture de l'ecran principal (mi-resolution par defaut)
#   cu.ps1 shotwin "<titre>" <out.png> [full]  capture du rectangle d'une seule fenetre
#   cu.ps1 windows                             fenetres visibles : pid | processus | rectangle | titre
#   cu.ps1 fg                                  fenetre au premier plan
#   cu.ps1 etat                                repere de la derniere capture de cet agent
#   cu.ps1 pause [min_ms] [max_ms]             attente aleatoire (rythme humain), defaut 800-2500
# Action (gardes : fichier STOP, verrou "bureau", fenetre sensible, -attendu) :
#   cu.ps1 focus "<titre>"
#   cu.ps1 click <x> <y> [left|right|double|middle]
#   cu.ps1 move <x> <y>
#   cu.ps1 drag <x1> <y1> <x2> <y2>
#   cu.ps1 scroll <x> <y> <up|down> [crans]    molette, 3 crans par defaut, 20 au plus
#   cu.ps1 type "<texte>"                      texte litteral (caracteres speciaux SendKeys echappes)
#   cu.ps1 key "<sequence>"                    sequence SendKeys brute : {ENTER} {TAB} {ESC} ^l %{LEFT}
# Options :
#   -img         x,y donnes dans le repere de la derniere capture (shot ou shotwin) : plus de calcul "x2" a la main
#   -n           simulation : affiche l'action et les coordonnees ecran, n'execute rien
#   -attendu T   refuse l'action si le titre de la fenetre au premier plan ne contient pas T
#   -agent N     nom de l'agent (repere de capture, journal, verrou). Defaut : $env:USINE_AGENT, sinon "defaut"
# Codes de sortie : 0 ok | 2 usage | 3 arret (STOP ou fenetre sensible) | 4 verrou ou fenetre inattendue | 5 introuvable
#
# Une action exige le verrou "bureau" detenu par cet agent : OUTILS\verrou.ps1 prendre bureau -agent <N>
# La garde "fenetre sensible" est un fil de detente, pas une garantie : l'agent reste tenu par GARDE-FOUS.md (G7).
param(
  [Parameter(Position=0)][string]$cmd,
  [Parameter(Position=1)][string]$a,
  [Parameter(Position=2)][string]$b,
  [Parameter(Position=3)][string]$c,
  [Parameter(Position=4)][string]$d,
  [switch]$img,
  [switch]$n,
  [string]$attendu,
  [string]$agent
)
$ErrorActionPreference = 'Stop'
if (-not $agent) { $agent = $env:USINE_AGENT }
if (-not $agent) { $agent = 'defaut' }
$racine = Split-Path -Parent $PSScriptRoot
$nomSur = $agent -replace '[^A-Za-z0-9_-]', '_'
$etatFichier = Join-Path $env:TEMP ("usine-cu-etat-$nomSur.json")
$utf8 = New-Object System.Text.UTF8Encoding($false)

# Titres de fenetre devant lesquels un agent s'arrete (G7). Le point remplace une lettre accentuee.
$sensible = 'captcha|v.rification|verification|two.?step|2.?step|\b2fa\b|deux ..?tapes|checkout|paiement|payment|buy robux|acheter des robux|\blog ?in\b|\bsign ?in\b|\bconnexion\b|se connecter|terms of use|conditions d.utilisation|consentement'

Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices; using System.Text;
public class UsineCu {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, int d, UIntPtr e);
  [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, uint f, UIntPtr e);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
}
"@
[UsineCu]::SetProcessDPIAware() | Out-Null

function Fin([int]$code, [string]$msg) { if ($msg) { Write-Output $msg }; exit $code }

function Journal([string]$texte) {
  try {
    $dos = Join-Path $racine 'JOURNAUX'
    if (-not (Test-Path $dos)) { New-Item -ItemType Directory -Force $dos | Out-Null }
    $ligne = "{0} | {1} | {2}" -f (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'), $agent, $texte
    [IO.File]::AppendAllText((Join-Path $dos ("cu-" + (Get-Date -Format 'yyyy-MM-dd') + ".log")), $ligne + "`r`n", $utf8)
  } catch { }
}

function PremierPlan {
  $h = [UsineCu]::GetForegroundWindow()
  $sb = New-Object System.Text.StringBuilder 512
  [UsineCu]::GetWindowText($h, $sb, 512) | Out-Null
  $idp = [uint32]0
  [UsineCu]::GetWindowThreadProcessId($h, [ref]$idp) | Out-Null
  $nom = ''
  try { $nom = (Get-Process -Id $idp).ProcessName } catch { }
  $r = New-Object UsineCu+RECT
  [UsineCu]::GetWindowRect($h, [ref]$r) | Out-Null
  [pscustomobject]@{ H = $h; Titre = $sb.ToString(); Idp = $idp; Processus = $nom; Rect = $r }
}

function Trouver([string]$titre) {
  Get-Process | Where-Object { $_.MainWindowTitle -and $_.MainWindowTitle -like "*$titre*" } | Select-Object -First 1
}

function Garde([bool]$verifierSensible) {
  if (Test-Path (Join-Path $racine 'STOP')) { Journal "REFUS STOP : $cmd"; Fin 3 'ARRET : fichier STOP present a la racine de l''usine.' }
  if ($n) { return }
  $verrou = Join-Path $racine 'VERROUS\bureau.lock'
  $tenu = $null
  if (Test-Path $verrou) { try { $tenu = ([IO.File]::ReadAllText($verrou, $utf8) | ConvertFrom-Json).agent } catch { } }
  if ($tenu -ne $agent) {
    Journal "REFUS VERROU : $cmd (detenteur : $tenu)"
    Fin 4 ("REFUS : le verrou 'bureau' n'est pas detenu par '$agent' (detenteur : " + $(if ($tenu) { $tenu } else { 'personne' }) + "). Lancer : OUTILS\verrou.ps1 prendre bureau -agent $agent")
  }
  $pp = PremierPlan
  if ($verifierSensible -and $pp.Titre -match $sensible) {
    Journal "REFUS SENSIBLE : $cmd sur '$($pp.Titre)'"
    Fin 3 ("ARRET-SENSIBLE : fenetre au premier plan '" + $pp.Titre + "'. Ne pas agir : OUTILS\alerte.ps1, puis passer a autre chose (G7).")
  }
  if ($attendu -and ($pp.Titre -notlike "*$attendu*")) {
    Journal "REFUS ATTENDU : $cmd attendu '$attendu' vu '$($pp.Titre)'"
    Fin 4 ("REFUS : fenetre au premier plan '" + $pp.Titre + "', attendu '" + $attendu + "'.")
  }
}

function Ecran([string]$sx, [string]$sy) {
  $x = 0; $y = 0
  if (-not ([int]::TryParse($sx, [ref]$x) -and [int]::TryParse($sy, [ref]$y))) { Fin 2 "USAGE : coordonnees entieres attendues, recu '$sx' '$sy'." }
  $src = 'ecran'
  if ($img) {
    if (-not (Test-Path $etatFichier)) { Fin 2 'USAGE : -img demande une capture prealable (shot ou shotwin) par le meme agent.' }
    $e = [IO.File]::ReadAllText($etatFichier, $utf8) | ConvertFrom-Json
    if ($x -lt 0 -or $y -lt 0 -or $x -ge $e.largeur -or $y -ge $e.hauteur) { Fin 2 "USAGE : ($x,$y) hors de la capture $($e.largeur)x$($e.hauteur)." }
    $src = "image ($x,$y) echelle $($e.echelle) origine ($($e.ox),$($e.oy))"
    $x = [int]($e.ox + $x * $e.echelle); $y = [int]($e.oy + $y * $e.echelle)
  }
  $v = [System.Windows.Forms.SystemInformation]::VirtualScreen
  if ($x -lt $v.X -or $y -lt $v.Y -or $x -ge ($v.X + $v.Width) -or $y -ge ($v.Y + $v.Height)) { Fin 2 "USAGE : ($x,$y) hors de l'ecran." }
  [pscustomobject]@{ X = $x; Y = $y; Source = $src }
}

function Capturer([int]$x, [int]$y, [int]$w, [int]$h, [string]$sortie, [bool]$plein, [string]$quoi) {
  if (-not $sortie) { Fin 2 'USAGE : chemin du fichier .png manquant.' }
  $sortie = [IO.Path]::GetFullPath($sortie)
  if (-not (Test-Path (Split-Path -Parent $sortie))) { Fin 5 "INTROUVABLE : dossier de sortie $(Split-Path -Parent $sortie)" }
  if ($w -le 0 -or $h -le 0) { Fin 5 'INTROUVABLE : rectangle de capture vide.' }
  $bmp = New-Object System.Drawing.Bitmap $w, $h
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($x, $y, 0, 0, $bmp.Size)
  $echelle = 1; $lw = $w; $lh = $h
  if ($plein) { $bmp.Save($sortie, [System.Drawing.Imaging.ImageFormat]::Png) }
  else {
    $echelle = 2; $lw = [int][math]::Floor($w / 2); $lh = [int][math]::Floor($h / 2)
    $petit = New-Object System.Drawing.Bitmap $lw, $lh
    $g2 = [System.Drawing.Graphics]::FromImage($petit)
    $g2.InterpolationMode = 'HighQualityBicubic'
    $g2.DrawImage($bmp, 0, 0, $lw, $lh)
    $petit.Save($sortie, [System.Drawing.Imaging.ImageFormat]::Png)
    $g2.Dispose(); $petit.Dispose()
  }
  $g.Dispose(); $bmp.Dispose()
  if ((Get-Item $sortie).Length -le 0) { Fin 5 "ECHEC : capture vide (disque plein ?) $sortie" }
  $etat = @{ fichier = $sortie; quoi = $quoi; ox = $x; oy = $y; echelle = $echelle; largeur = $lw; hauteur = $lh; date = (Get-Date).ToUniversalTime().ToString('o') } | ConvertTo-Json -Compress
  [IO.File]::WriteAllText($etatFichier, $etat, $utf8)
  Journal "capture $quoi -> $sortie"
  "capture $quoi : image ${lw}x${lh}, echelle $echelle, origine ecran ($x,$y) -> $sortie"
  "pour agir sur un point de cette image : ajouter -img (ex. cu.ps1 click <x> <y> -img)"
}

function Bouton([string]$quel) {
  switch ($quel) {
    'right'  { [UsineCu]::mouse_event(8, 0, 0, 0, [UIntPtr]::Zero); [UsineCu]::mouse_event(16, 0, 0, 0, [UIntPtr]::Zero) }
    'middle' { [UsineCu]::mouse_event(32, 0, 0, 0, [UIntPtr]::Zero); [UsineCu]::mouse_event(64, 0, 0, 0, [UIntPtr]::Zero) }
    default  { [UsineCu]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero); [UsineCu]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero) }
  }
}

switch ($cmd) {
  'shot' {
    $s = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    Capturer $s.X $s.Y $s.Width $s.Height $a ($b -eq 'full') 'ecran'
  }
  'shotwin' {
    $p = Trouver $a
    if (-not $p) { Fin 5 "INTROUVABLE : aucune fenetre dont le titre contient '$a'." }
    if ([UsineCu]::IsIconic($p.MainWindowHandle)) { Fin 5 "INTROUVABLE : la fenetre '$($p.MainWindowTitle)' est reduite ; la mettre au premier plan (focus) d'abord." }
    $r = New-Object UsineCu+RECT
    [UsineCu]::GetWindowRect($p.MainWindowHandle, [ref]$r) | Out-Null
    $v = [System.Windows.Forms.SystemInformation]::VirtualScreen
    $x1 = [math]::Max($r.L, $v.X); $y1 = [math]::Max($r.T, $v.Y)
    $x2 = [math]::Min($r.R, $v.X + $v.Width); $y2 = [math]::Min($r.B, $v.Y + $v.Height)
    if ((PremierPlan).H -ne $p.MainWindowHandle) { "attention : '$($p.MainWindowTitle)' n'est pas au premier plan ; la capture montre ce qui la recouvre." }
    Capturer $x1 $y1 ($x2 - $x1) ($y2 - $y1) $b ($c -eq 'full') "fenetre '$($p.MainWindowTitle)'"
  }
  'windows' {
    Get-Process | Where-Object { $_.MainWindowTitle } | ForEach-Object {
      $r = New-Object UsineCu+RECT
      [UsineCu]::GetWindowRect($_.MainWindowHandle, [ref]$r) | Out-Null
      "{0} | {1} | ({2},{3})-({4},{5}) | {6}" -f $_.Id, $_.ProcessName, $r.L, $r.T, $r.R, $r.B, $_.MainWindowTitle
    }
  }
  'fg' {
    $pp = PremierPlan
    "{0} | {1} | ({2},{3})-({4},{5}) | {6}" -f $pp.Idp, $pp.Processus, $pp.Rect.L, $pp.Rect.T, $pp.Rect.R, $pp.Rect.B, $pp.Titre
    if ($pp.Titre -match $sensible) { 'SENSIBLE : cette fenetre declenche l''arret des actions (G7).' }
  }
  'etat' {
    if (Test-Path $etatFichier) { [IO.File]::ReadAllText($etatFichier, $utf8) } else { 'aucune capture pour cet agent' }
  }
  'pause' {
    $min = 800; $max = 2500
    if ($a) { $min = [int]$a }
    if ($b) { $max = [int]$b }
    if ($max -le $min) { $max = $min + 1 }
    $ms = Get-Random -Minimum $min -Maximum $max
    if (-not $n) { Start-Sleep -Milliseconds $ms }
    "pause $ms ms"
  }
  'focus' {
    Garde $false
    $p = Trouver $a
    if (-not $p) { Fin 5 "INTROUVABLE : aucune fenetre dont le titre contient '$a'." }
    if ($n) { Fin 0 "SIMULATION focus '$($p.MainWindowTitle)'" }
    # Alt presse puis relache : autorise SetForegroundWindow depuis un processus d'arriere-plan.
    [UsineCu]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero); [UsineCu]::keybd_event(0x12, 0, 2, [UIntPtr]::Zero)
    if ([UsineCu]::IsIconic($p.MainWindowHandle)) { [UsineCu]::ShowWindow($p.MainWindowHandle, 9) | Out-Null }
    [UsineCu]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
    Start-Sleep -Milliseconds 250
    $pp = PremierPlan
    Journal "focus '$a' -> '$($pp.Titre)'"
    if ($pp.H -ne $p.MainWindowHandle) { Fin 4 "REFUS : focus demande sur '$($p.MainWindowTitle)', premier plan reste '$($pp.Titre)'." }
    "premier plan : $($pp.Titre)"
    if ($pp.Titre -match $sensible) { 'SENSIBLE : cette fenetre declenche l''arret des actions (G7).' }
  }
  'click' {
    Garde $true
    $pt = Ecran $a $b
    $quel = if ($c) { $c } else { 'left' }
    if ($quel -notin 'left', 'right', 'double', 'middle') { Fin 2 "USAGE : bouton '$quel' inconnu." }
    if ($n) { Fin 0 "SIMULATION click $quel ecran=($($pt.X),$($pt.Y)) depuis $($pt.Source)" }
    [UsineCu]::SetCursorPos($pt.X, $pt.Y) | Out-Null; Start-Sleep -Milliseconds 80
    if ($quel -eq 'double') { Bouton 'left'; Start-Sleep -Milliseconds 60; Bouton 'left' } else { Bouton $quel }
    Journal "click $quel ($($pt.X),$($pt.Y))"
    "click $quel ($($pt.X),$($pt.Y))"
  }
  'move' {
    Garde $true
    $pt = Ecran $a $b
    if ($n) { Fin 0 "SIMULATION move ecran=($($pt.X),$($pt.Y)) depuis $($pt.Source)" }
    [UsineCu]::SetCursorPos($pt.X, $pt.Y) | Out-Null
    "move ($($pt.X),$($pt.Y))"
  }
  'drag' {
    Garde $true
    $p1 = Ecran $a $b; $p2 = Ecran $c $d
    if ($n) { Fin 0 "SIMULATION drag ecran=($($p1.X),$($p1.Y)) -> ($($p2.X),$($p2.Y))" }
    [UsineCu]::SetCursorPos($p1.X, $p1.Y) | Out-Null; Start-Sleep -Milliseconds 80
    [UsineCu]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero)
    for ($i = 1; $i -le 10; $i++) {
      [UsineCu]::SetCursorPos([int]($p1.X + ($p2.X - $p1.X) * $i / 10), [int]($p1.Y + ($p2.Y - $p1.Y) * $i / 10)) | Out-Null
      Start-Sleep -Milliseconds 25
    }
    [UsineCu]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero)
    Journal "drag ($($p1.X),$($p1.Y)) -> ($($p2.X),$($p2.Y))"
    "drag ($($p1.X),$($p1.Y)) -> ($($p2.X),$($p2.Y))"
  }
  'scroll' {
    Garde $true
    $pt = Ecran $a $b
    if ($c -notin 'up', 'down') { Fin 2 'USAGE : scroll <x> <y> <up|down> [crans].' }
    $crans = 3
    if ($d -and (-not [int]::TryParse($d, [ref]$crans) -or $crans -lt 1)) { Fin 2 'USAGE : nombre de crans entier positif.' }
    if ($crans -gt 20) { Fin 2 'USAGE : 20 crans au plus par appel (rythme humain).' }
    if ($n) { Fin 0 "SIMULATION scroll $c $crans crans ecran=($($pt.X),$($pt.Y)) depuis $($pt.Source)" }
    [UsineCu]::SetCursorPos($pt.X, $pt.Y) | Out-Null; Start-Sleep -Milliseconds 80
    $pas = if ($c -eq 'up') { 120 } else { -120 }
    for ($i = 0; $i -lt $crans; $i++) { [UsineCu]::mouse_event(0x0800, 0, 0, $pas, [UIntPtr]::Zero); Start-Sleep -Milliseconds 40 }
    Journal "scroll $c $crans ($($pt.X),$($pt.Y))"
    "scroll $c $crans crans ($($pt.X),$($pt.Y))"
  }
  'type' {
    Garde $true
    if (-not $a) { Fin 2 'USAGE : type "<texte>".' }
    $echappe = [regex]::Replace($a, '[+^%~(){}\[\]]', '{$0}')
    if ($n) { Fin 0 "SIMULATION type $($a.Length) caracteres -> SendKeys '$echappe'" }
    [System.Windows.Forms.SendKeys]::SendWait($echappe)
    Journal "type $($a.Length) caracteres"
    "type $($a.Length) caracteres"
  }
  'key' {
    Garde $true
    if (-not $a) { Fin 2 'USAGE : key "<sequence SendKeys>".' }
    if ($n) { Fin 0 "SIMULATION key '$a'" }
    [System.Windows.Forms.SendKeys]::SendWait($a)
    Journal "key '$a'"
    "key '$a'"
  }
  default {
    Get-Content -LiteralPath $PSCommandPath -TotalCount 27 | ForEach-Object { $_ -replace '^# ?', '' }
    exit 2
  }
}
exit 0

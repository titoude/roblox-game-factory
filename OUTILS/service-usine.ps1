# Service utilisateur, ASCII volontaire pour PowerShell 5.1.
param(
  [Parameter(Position=0)][ValidateSet('etat','installer','retirer')][string]$Action = 'etat',
  [switch]$Confirmer
)
$ErrorActionPreference = 'Stop'
$nom = 'UsineRoblox-Battement'
$racine = Split-Path -Parent $PSScriptRoot
try {
  $tache = Get-ScheduledTask -TaskName $nom -ErrorAction SilentlyContinue
  if ($Action -eq 'etat') {
    if (-not $tache) { Write-Output "$nom : absente"; exit 0 }
    $info = Get-ScheduledTaskInfo -TaskName $nom
    Write-Output "$nom : $($tache.State)"
    Write-Output "Derniere execution : $($info.LastRunTime) ; resultat : $($info.LastTaskResult)"
    Write-Output "Prochaine execution : $($info.NextRunTime)"
    exit 0
  }
  if (-not $Confirmer) {
    if ($Action -eq 'retirer') { Write-Output "SIMULATION : suppression de $nom ; aucune modification." }
    else {
      Write-Output "SIMULATION : creation de $nom ; aucune modification."
      Write-Output "Commande : python OUTILS\battement.py --lancer"
      Write-Output "Dossier : $racine"
      Write-Output 'Frequence : toutes les heures ; utilisateur courant, session ouverte seulement.'
      Write-Output 'Aucun privilege administrateur, aucun mot de passe stocke ; quota de modeles consomme.'
      Write-Output 'Activation reservee au proprietaire : installer -Confirmer'
    }
    exit 0
  }
  if ($Action -eq 'retirer') {
    if ($tache) { Unregister-ScheduledTask -TaskName $nom -Confirm:$false }
    Write-Output "$nom : retiree (ou deja absente)"
    exit 0
  }
  if (Test-Path -LiteralPath (Join-Path $racine 'STOP')) { throw 'STOP present : installation refusee.' }
  if ($tache) { throw 'Tache deja presente ; retirer avant de reinstaller.' }
  $python = (Get-Command python -CommandType Application -ErrorAction Stop).Source
  $arguments = '"' + (Join-Path $racine 'OUTILS\battement.py') + '" --lancer'
  $execution = New-ScheduledTaskAction -Execute $python -Argument $arguments -WorkingDirectory $racine
  $declencheur = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Hours 1)
  $utilisateur = [Security.Principal.WindowsIdentity]::GetCurrent().Name
  $principal = New-ScheduledTaskPrincipal -UserId $utilisateur -LogonType Interactive -RunLevel Limited
  $reglages = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 1)
  Register-ScheduledTask -TaskName $nom -Action $execution -Trigger $declencheur -Principal $principal -Settings $reglages | Out-Null
  Write-Output "$nom : installee pour la session de l'utilisateur courant."
  exit 0
} catch {
  Write-Output 'ECHEC : consultation ou modification de la tache impossible.'
  exit 2
}

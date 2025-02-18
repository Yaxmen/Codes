# Criar um serviço de log de eventos do sistema
$logFile = "C:\Logs\SystemEvents.log"  # Arquivo de log
$eventTypes = @("Error", "Warning")    # Tipos de eventos a serem monitorados

# Criar pasta de logs se não existir
if (-not (Test-Path (Split-Path $logFile))) {
    New-Item -ItemType Directory -Path (Split-Path $logFile)
}

# Coletar eventos e salvar no arquivo de log
Get-WinEvent -LogName System | Where-Object { $_.LevelDisplayName -in $eventTypes } | ForEach-Object {
    $eventMessage = "$($_.TimeCreated) | $($_.LevelDisplayName) | $($_.Message)"
    Add-Content -Path $logFile -Value $eventMessage
}

Write-Host "Log de eventos salvo em: $logFile"
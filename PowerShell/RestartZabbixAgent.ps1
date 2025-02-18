$serviceName = "Zabbix Agent"
$maxAttempts = 5  # Número máximo de tentativas para verificar o serviço após o reinício
$restartService = $false
 
# Verifica o status do serviço
$service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
 
if ($service -eq $null) {
    Write-Host "O serviço '$serviceName' não foi encontrado."
} elseif ($service.Status -ne "Running") {
    Write-Host "O serviço '$serviceName' não está em execução. Reiniciando..."
    Restart-Service -Name $serviceName
    $restartService = $true
} else {
    Write-Host "O serviço '$serviceName' está em execução."
}
 
# Se o serviço foi reiniciado, aguardar até que esteja em execução:
if ($restartService) {
    $attempts = 0
    while ($attempts -lt $maxAttempts) {
        Start-Sleep -Seconds 10  # Aguarda 10 segundos entre as tentativas
        $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
        if ($service -ne $null -and $service.Status -eq "Running") {
            Write-Host "O serviço '$serviceName' está em execução após reinício."
            break
        }
        $attempts++
    }
 
    if ($attempts -eq $maxAttempts) {
        Write-Host "O serviço '$serviceName' não iniciou após reinício em $maxAttempts tentativas."
    }
}
 
# Registro do processamento em um arquivo de log
$logFilePath = "C:\Zabbix\script_log.txt"
$logMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Script executado - Serviço: $serviceName, Reinício: $restartService"
Add-Content -Path $logFilePath -Value $logMessage
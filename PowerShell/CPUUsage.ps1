# Monitorar uso de CPU e memória de um processo específico
$processName = "chrome"  # Nome do processo (sem .exe)

while ($true) {
    $process = Get-Process -Name $processName -ErrorAction SilentlyContinue

    if ($process) {
        $cpuUsage = ($process.CPU).ToString("N2")
        $memoryUsage = ($process.WorkingSet64 / 1MB).ToString("N2")
        Write-Host "Processo: $processName | CPU: $cpuUsage% | Memória: $memoryUsage MB"
    } else {
        Write-Host "Processo '$processName' não encontrado."
        break
    }

    Start-Sleep -Seconds 2  # Intervalo de 2 segundos
}
# Verificar e encerrar processos consumindo muita memória
$memoryThreshold = 1GB  # Limite de memória (1 GB)

# Listar processos que excedem o limite de memória
$processes = Get-Process | Where-Object { $_.WorkingSet64 -gt $memoryThreshold }

if ($processes) {
    Write-Host "Processos consumindo mais de $($memoryThreshold / 1MB) MB de memória:"
    $processes | ForEach-Object {
        Write-Host "Processo: $($_.ProcessName) | ID: $($_.Id) | Memória: $($_.WorkingSet64 / 1MB) MB"
    }

    # Perguntar ao usuário se deseja encerrar os processos
    $response = Read-Host "Deseja encerrar esses processos? (S/N)"
    if ($response -eq "S") {
        $processes | ForEach-Object {
            Stop-Process -Id $_.Id -Force
            Write-Host "Processo $($_.ProcessName) (ID: $($_.Id)) encerrado."
        }
    }
} else {
    Write-Host "Nenhum processo consumindo mais de $($memoryThreshold / 1MB) MB de memória."
}
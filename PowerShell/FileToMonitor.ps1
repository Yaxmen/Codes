# Monitorar alterações em um arquivo ou pasta
$folderToMonitor = "C:\Users\SeuUsuario\Documents"  # Pasta a ser monitorada
$fileToMonitor = "arquivo.txt"                     # Arquivo específico (opcional)

# Obter o hash inicial do arquivo/pasta
$initialHash = Get-ChildItem -Path $folderToMonitor -Recurse | Get-FileHash | Select-Object -ExpandProperty Hash

while ($true) {
    Start-Sleep -Seconds 5  # Intervalo de verificação

    # Obter o hash atual do arquivo/pasta
    $currentHash = Get-ChildItem -Path $folderToMonitor -Recurse | Get-FileHash | Select-Object -ExpandProperty Hash

    if ($currentHash -ne $initialHash) {
        Write-Host "Alteração detectada em: $folderToMonitor"
        $initialHash = $currentHash  # Atualizar o hash inicial
    }
}
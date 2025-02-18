# Backup automático de arquivos
$sourceFolder = "C:\Users\SeuUsuario\Documents"  # Pasta de origem
$backupFolder = "C:\Backups"                     # Pasta de backup
$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"   # Data e hora para o nome do backup

# Criar pasta de backup se não existir
if (-not (Test-Path $backupFolder)) {
    New-Item -ItemType Directory -Path $backupFolder
}

# Criar pasta de backup com a data atual
$backupPath = Join-Path -Path $backupFolder -ChildPath "Backup_$date"
New-Item -ItemType Directory -Path $backupPath

# Copiar arquivos
Copy-Item -Path "$sourceFolder\*" -Destination $backupPath -Recurse

Write-Host "Backup concluído em: $backupPath"
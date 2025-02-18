# Verificar espaço livre no disco
$disk = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'"

$freeSpaceGB = [math]::round($disk.FreeSpace / 1GB, 2)
$totalSpaceGB = [math]::round($disk.Size / 1GB, 2)

Write-Host "Espaço total: $totalSpaceGB GB"
Write-Host "Espaço livre: $freeSpaceGB GB"
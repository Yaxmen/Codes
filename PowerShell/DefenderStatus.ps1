# Verificar status do Windows Defender
$defenderStatus = Get-MpComputerStatus

if ($defenderStatus.AntivirusEnabled -and $defenderStatus.AntivirusSignatureLastUpdated) {
    Write-Host "O Windows Defender está ativo e as assinaturas estão atualizadas."
} else {
    Write-Host "O Windows Defender não está ativo ou as assinaturas não estão atualizadas."
}
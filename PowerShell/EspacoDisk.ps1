# Defina a porcentagem mínima de espaço livre desejada
$limiteEspacoLivre = 10

# Caminho para a pasta Temp
$caminhoTemp = [System.IO.Path]::GetTempPath()

# Caminho do arquivo de log
$caminhoArquivoLog = "C:\diretorio\diretorio\Log.txt"

# Obter informações sobre o disco C:
$discoC = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'"

# Calcular a porcentagem de espaço livre no disco C:
$porcentagemEspacoLivre = [math]::Round(($discoC.FreeSpace / $discoC.Size) * 100, 2)

# Informações sobre o espaço em disco
$espacoTotalGB = [math]::Round($discoC.Size / 1GB, 2)
$espacoLivreGB = [math]::Round($discoC.FreeSpace / 1GB, 2)
$espacoUsadoGB = $espacoTotalGB - $espacoLivreGB

# Mensagem de depuração
Write-Host "Espaço Total em Disco C: $($espacoTotalGB) GB"
Write-Host "Espaço Livre em Disco C: $($espacoLivreGB) GB"
Write-Host "Espaço Usado em Disco C: $($espacoUsadoGB) GB"
Write-Host "Porcentagem de Espaço Livre: $($porcentagemEspacoLivre)%"

# Verificar se o espaço livre é menor que o limite definido
if ($porcentagemEspacoLivre -lt $limiteEspacoLivre) {
    Write-Host "Espaço em disco C: abaixo do limite. Limpando a pasta Temp..."

    # Obter arquivos na pasta Temp
    $arquivosTemp = Get-ChildItem -Path $caminhoTemp

    # Mensagem de depuração
    Write-Host "Número de arquivos na pasta Temp: $($arquivosTemp.Count)"

    # Excluir arquivos na pasta Temp
    $arquivosTemp | Remove-Item -Force

    # Mensagem de depuração
    Write-Host "Arquivos excluídos da pasta Temp"

    # Gerar log
    $logMensagem = @"
Ação: Limpeza da pasta Temp
Data e Hora: $(Get-Date)
Espaço Total em Disco C: $($espacoTotalGB) GB
Espaço Livre em Disco C: $($espacoLivreGB) GB
Espaço Usado em Disco C: $($espacoUsadoGB) GB
Porcentagem de Espaço Livre: $($porcentagemEspacoLivre)%
"@
    Add-Content -Path $caminhoArquivoLog -Value $logMensagem

    # Mensagem de depuração
    Write-Host "Log atualizado com sucesso."

    Write-Host "Limpeza concluída. Consulte o log para mais informações."
} else {
    # Gerar log se o espaço estiver dentro do limite
    $logMensagem = @"
Ação: Verificação de Espaço em Disco
Data e Hora: $(Get-Date)
Espaço Total em Disco C: $($espacoTotalGB) GB
Espaço Livre em Disco C: $($espacoLivreGB) GB
Espaço Usado em Disco C: $($espacoUsadoGB) GB
Porcentagem de Espaço Livre: $($porcentagemEspacoLivre)%
Espaço em disco C: dentro do limite. Nenhuma ação necessária.
"@
    Add-Content -Path $caminhoArquivoLog -Value $logMensagem

    Write-Host "Espaço em disco C: dentro do limite. Nenhuma ação necessária."
}

# Define a hora de início da execução do script
$startTime = Get-Date

# Define o caminho base onde as pastas de log serão criadas
$logBasePath = "C:\diretorio\diretorio"

$localComputerName = $env:COMPUTERNAME

# Cria uma pasta com a data atual para armazenar os logs
$logFolderPath = Join-Path -Path $logBasePath -ChildPath (Get-Date -Format "Service_dd-MM-yyyy")
New-Item -ItemType Directory -Force -Path $logFolderPath

# Define o caminho do arquivo de log com a data, mês e hora de execução
$LogFileName = "$localComputerName.txt"
$LogFilePath = Join-Path -Path $logFolderPath -ChildPath $LogFileName

# Caminho do arquivo com a lista de serviços
$servicesFile = "C:\diretorio\diretorio\services.txt"

# Inicializa o log
$executionLog = @()

# Função para registrar mensagens no log
function LogMessage($message, $type) {
    $logEntry = "$type - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $message"
    Write-Output $logEntry
    $executionLog += $logEntry
}

LogMessage("Script iniciado.", "INFO")

# Lê o arquivo de texto com os nomes dos serviços
$services = Get-Content $servicesFile

# Loop através dos serviços
foreach ($service in $services) {
    LogMessage("Iniciando o serviço $service no computador localComputerName", "INFO")
    try {
        # Verifica se o serviço está definido como automático
        $serviceInfo = Get-WmiObject -Class Win32_Service -Filter "Name='$service'"
        if ($serviceInfo.StartMode -eq "Auto" -and $serviceInfo.State -eq "Stopped") {
            # Inicia o serviço
            Start-Service -Name $service
            LogMessage("O serviço $service foi iniciado no computador localComputerName.", "INFO")
        }
    } catch {
        LogMessage("Erro ao iniciar o serviço $service no computador localComputerName: $_", "ERROR")
    }
}

LogMessage("Script finalizado.", "INFO")

# Grava o log em um arquivo
$executionLog | Out-File -FilePath $LogFilePath -Append

# Calcula o tempo necessário para executar o script
$endTime = Get-Date
$executionTime = New-TimeSpan $startTime $endTime
LogMessage("Tempo de execução: $executionTime", "INFO")

# Enviar notificação por e-mail com status do sistema
$smtpServer = "smtp.seuservidor.com"  # Servidor SMTP
$smtpPort = 587                       # Porta SMTP
$emailFrom = "seuemail@dominio.com"   # E-mail do remetente
$emailTo = "destinatario@dominio.com" # E-mail do destinatário
$smtpUser = "seuemail@dominio.com"    # Usuário SMTP
$smtpPassword = "suasenha"           # Senha SMTP

# Coletar informações do sistema
$cpuUsage = (Get-WmiObject Win32_Processor).LoadPercentage
$memoryUsage = (Get-WmiObject Win32_OperatingSystem).FreePhysicalMemory / 1MB
$diskUsage = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'" | Select-Object Size, FreeSpace

# Criar corpo do e-mail
$body = @"
Status do Sistema:
- Uso de CPU: $cpuUsage%
- Memória livre: $memoryUsage GB
- Espaço livre no disco C:: $([math]::round($diskUsage.FreeSpace / 1GB, 2)) GB de $([math]::round($diskUsage.Size / 1GB, 2)) GB
"@

# Enviar e-mail
Send-MailMessage -From $emailFrom -To $emailTo -Subject "Status do Sistema" -Body $body -SmtpServer $smtpServer -Port $smtpPort -Credential (New-Object System.Management.Automation.PSCredential ($smtpUser, (ConvertTo-SecureString $smtpPassword -AsPlainText -Force)) -UseSsl
Write-Host "E-mail enviado com sucesso."
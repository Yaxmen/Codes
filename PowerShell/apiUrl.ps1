# Consultar IP público usando uma API
$apiUrl = "https://api.ipify.org?format=json"

try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method Get
    Write-Host "Seu IP público é: $($response.ip)"
} catch {
    Write-Host "Erro ao consultar o IP público: $_"
}
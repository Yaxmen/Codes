# Verificar tarefas agendadas
$tasks = Get-ScheduledTask | Where-Object { $_.State -eq "Ready" }

foreach ($task in $tasks) {
    $lastRun = $task.LastRunTime
    $lastResult = $task.LastTaskResult

    if ($lastRun) {
        Write-Host "Tarefa: $($task.TaskName) - Última execução: $lastRun - Resultado: $lastResult"
    } else {
        Write-Host "Tarefa: $($task.TaskName) - Nunca foi executada"
    }
}
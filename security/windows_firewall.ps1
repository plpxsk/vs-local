# Windows Firewall rules for on-device LLM
# Block all outbound traffic for Ollama/LM Studio except localhost
#
# Usage: Run as Administrator in PowerShell
#   .\windows_firewall.ps1

Write-Host "Applying on-device LLM firewall rules..." -ForegroundColor Cyan

# Find Ollama executable
$ollamaPath = (Get-Command ollama -ErrorAction SilentlyContinue).Source
if (-not $ollamaPath) {
    $ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
}

if (Test-Path $ollamaPath) {
    # Block Ollama outbound (except localhost is implicitly allowed)
    New-NetFirewallRule -DisplayName "Block Ollama Outbound" `
        -Direction Outbound `
        -Program $ollamaPath `
        -Action Block `
        -RemoteAddress "!127.0.0.1" `
        -Profile Any `
        -Description "Block Ollama from making external network calls"

    Write-Host "Blocked outbound for: $ollamaPath" -ForegroundColor Green
} else {
    Write-Host "Ollama not found at expected path. Update `$ollamaPath in this script." -ForegroundColor Yellow
}

# Find LM Studio executable
$lmStudioPaths = @(
    "$env:LOCALAPPDATA\Programs\LM Studio\LM Studio.exe",
    "$env:PROGRAMFILES\LM Studio\LM Studio.exe"
)

foreach ($path in $lmStudioPaths) {
    if (Test-Path $path) {
        New-NetFirewallRule -DisplayName "Block LM Studio Outbound" `
            -Direction Outbound `
            -Program $path `
            -Action Block `
            -RemoteAddress "!127.0.0.1" `
            -Profile Any `
            -Description "Block LM Studio from making external network calls"

        Write-Host "Blocked outbound for: $path" -ForegroundColor Green
        break
    }
}

Write-Host "`nFirewall rules applied. Use 'Get-NetFirewallRule | Where DisplayName -like '*LLM*'' to verify." -ForegroundColor Cyan

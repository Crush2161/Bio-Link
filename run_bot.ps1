# BioLink Protector Bot Setup and Starter
Write-Host "BioLink Protector Bot Setup and Starter" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Running setup script..." -ForegroundColor Yellow
python setup_env.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error: Python script failed to execute." -ForegroundColor Red
    Write-Host "Please make sure Python is installed and in your PATH." -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to exit"

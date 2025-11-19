# ============================================================================
# Document Upload Service - Windows Setup Script (PowerShell)
# ============================================================================
# This script sets up the environment for the document upload service
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  Document Upload Service - Setup" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[INFO] $pythonVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "        Please install Python 3.10+ and add it to PATH." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment if it doesn't exist
if (-Not (Test-Path "venvWindows")) {
    Write-Host "[1/3] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venvWindows
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "      ✓ Virtual environment created" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[INFO] Virtual environment already exists" -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "[2/3] Activating virtual environment..." -ForegroundColor Yellow
& "venvWindows\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to activate virtual environment!" -ForegroundColor Red
    Write-Host "        You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "      ✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "[3/3] Installing dependencies..." -ForegroundColor Yellow
Write-Host "      This may take a few minutes..." -ForegroundColor Gray
python -m pip install --upgrade pip --quiet
pip install -r windowsEnv_requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "      ✓ Dependencies installed successfully" -ForegroundColor Green
Write-Host ""

# Copy environment file if it doesn't exist
if (-Not (Test-Path ".env")) {
    Write-Host "[INFO] Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.windows" ".env"
    Write-Host "      ✓ Created .env file" -ForegroundColor Green
    Write-Host "      Please review and update the configuration in .env" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "[INFO] .env file already exists" -ForegroundColor Green
    Write-Host ""
}

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor White
Write-Host "  1. Review and update .env configuration" -ForegroundColor Gray
Write-Host "  2. Run test_upload.bat to test the service" -ForegroundColor Gray
Write-Host "  3. Use upload_document.bat to upload files" -ForegroundColor Gray
Write-Host ""
Write-Host "  Example usage:" -ForegroundColor White
Write-Host "  .\upload_document.bat my_file.cpp" -ForegroundColor Gray
Write-Host "  .\upload_document.bat document.pdf" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan

Read-Host "Press Enter to exit"

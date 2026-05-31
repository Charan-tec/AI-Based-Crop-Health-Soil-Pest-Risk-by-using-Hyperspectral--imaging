# ============================================================================
# AgriTech Pro - Automatic Dependency Fix Script (PowerShell)
# This script fixes NumPy/Pandas compatibility issues
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "  🌱 AgriTech Pro - Dependency Fix Script (PowerShell)" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 1: Checking for virtual environment..." -ForegroundColor Cyan
if (Test-Path "venv") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Step 2: Deactivating virtual environment..." -ForegroundColor Cyan
    & "venv\Scripts\Deactivate.ps1" 2>$null
    Write-Host "✅ Deactivated" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Step 3: Removing old virtual environment..." -ForegroundColor Cyan
    Remove-Item -Recurse -Force "venv" -ErrorAction SilentlyContinue
    Write-Host "✅ Removed old venv" -ForegroundColor Green
} else {
    Write-Host "ⓘ Virtual environment not found (will create new one)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 4: Creating fresh virtual environment..." -ForegroundColor Cyan
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Virtual environment created" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5: Activating virtual environment..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

Write-Host ""
Write-Host "Step 6: Clearing pip cache..." -ForegroundColor Cyan
python -m pip cache purge 2>$null
Write-Host "✅ Pip cache cleared" -ForegroundColor Green

Write-Host ""
Write-Host "Step 7: Upgrading pip, setuptools, and wheel..." -ForegroundColor Cyan
python -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to upgrade pip" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Pip upgraded" -ForegroundColor Green

Write-Host ""
Write-Host "Step 8: Installing compatible packages..." -ForegroundColor Cyan
Write-Host "  - numpy 1.26.3" -ForegroundColor Yellow
Write-Host "  - pandas 2.1.4" -ForegroundColor Yellow
Write-Host "  - Other dependencies..." -ForegroundColor Yellow
Write-Host ""
Write-Host "This may take 2-5 minutes..." -ForegroundColor Yellow
Write-Host ""

pip install --upgrade --force-reinstall numpy==1.26.3 pandas==2.1.4
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install numpy/pandas" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install requirements" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ All packages installed successfully" -ForegroundColor Green

Write-Host ""
Write-Host "Step 9: Verifying installation..." -ForegroundColor Cyan
python -c "import numpy; import pandas; import flask; print('✅ All imports successful!')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Verification failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "  ✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your system is ready to run AgriTech Pro!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Keep this terminal window open" -ForegroundColor White
Write-Host "  2. Run: python app.py" -ForegroundColor White
Write-Host "  3. Open: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter when ready to proceed"

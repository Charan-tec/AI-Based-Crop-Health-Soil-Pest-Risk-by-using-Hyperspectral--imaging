@echo off
REM ============================================================================
REM  AgriTech Pro - Automatic Dependency Fix Script (Windows)
REM  This script fixes NumPy/Pandas compatibility issues
REM ============================================================================

echo.
echo ============================================================================
echo  🌱 AgriTech Pro - Dependency Fix Script
echo ============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python found
python --version

echo.
echo Step 1: Checking for virtual environment...
if exist venv (
    echo ✅ Virtual environment found
    echo.
    echo Step 2: Deactivating virtual environment...
    call venv\Scripts\deactivate.bat 2>nul
    echo ✅ Deactivated
    
    echo.
    echo Step 3: Removing old virtual environment...
    rmdir /s /q venv
    echo ✅ Removed old venv
) else (
    echo ⓘ Virtual environment not found (will create new one)
)

echo.
echo Step 4: Creating fresh virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment created

echo.
echo Step 5: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated

echo.
echo Step 6: Clearing pip cache...
python -m pip cache purge >nul 2>&1
echo ✅ Pip cache cleared

echo.
echo Step 7: Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)
echo ✅ Pip upgraded

echo.
echo Step 8: Installing compatible packages...
echo   - numpy 1.26.3
echo   - pandas 2.1.4
echo   - Other dependencies...
echo.
echo This may take 2-5 minutes...
echo.

pip install --upgrade --force-reinstall numpy==1.26.3 pandas==2.1.4
if errorlevel 1 (
    echo ❌ Failed to install numpy/pandas
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)
echo ✅ All packages installed successfully

echo.
echo Step 9: Verifying installation...
python -c "import numpy; import pandas; import flask; print('✅ All imports successful!')"
if errorlevel 1 (
    echo ❌ Verification failed
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo  ✅ SETUP COMPLETE!
echo ============================================================================
echo.
echo Your system is ready to run AgriTech Pro!
echo.
echo Next steps:
echo   1. Keep this terminal window open
echo   2. Run: python app.py
echo   3. Open: http://localhost:5000
echo.
echo ============================================================================
echo.

pause

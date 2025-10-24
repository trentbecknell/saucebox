@echo off
REM SauceMax Installation Script for Windows
REM Installs SauceMax and integrates with Reaper

echo.
echo 🎛️ SauceMax Installation Script
echo =================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+ first.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python found
python --version

REM Check Python version
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [INFO] Python version: %PYTHON_VERSION%

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip not found. Installing pip...
    python -m ensurepip --upgrade
)

echo [INFO] pip found
pip --version

REM Ask about virtual environment
set /p CREATE_VENV="Create virtual environment? (recommended) [Y/n]: "
if /i "%CREATE_VENV%"=="n" goto skip_venv
if /i "%CREATE_VENV%"=="no" goto skip_venv

echo [INFO] Creating virtual environment...
python -m venv saucemax_env
call saucemax_env\Scripts\activate.bat
echo [SUCCESS] Virtual environment activated

:skip_venv

REM Upgrade pip
echo [INFO] Upgrading pip...
pip install --upgrade pip

REM Install SauceMax
echo [INFO] Installing SauceMax...
if exist setup.py (
    echo [INFO] Installing from local source...
    pip install -e .
) else (
    echo [INFO] Installing from PyPI...
    pip install saucemax
)

if %errorlevel% neq 0 (
    echo [ERROR] SauceMax installation failed
    pause
    exit /b 1
)

echo [SUCCESS] SauceMax installed successfully!

REM Find Reaper installation
echo [INFO] Looking for Reaper installation...

set REAPER_PATH=""
if exist "%APPDATA%\REAPER" (
    set REAPER_PATH=%APPDATA%\REAPER
    echo [SUCCESS] Found Reaper at: %REAPER_PATH%
) else if exist "C:\Program Files\REAPER" (
    set REAPER_PATH=C:\Program Files\REAPER
    echo [SUCCESS] Found Reaper at: %REAPER_PATH%
) else if exist "C:\Program Files (x86)\REAPER" (
    set REAPER_PATH=C:\Program Files (x86)\REAPER
    echo [SUCCESS] Found Reaper at: %REAPER_PATH%
) else (
    echo [WARNING] Reaper installation not found automatically
    set /p MANUAL_PATH="Enter Reaper installation path (or press Enter to skip): "
    if not "%MANUAL_PATH%"=="" (
        if exist "%MANUAL_PATH%" (
            set REAPER_PATH=%MANUAL_PATH%
            echo [SUCCESS] Using Reaper path: %REAPER_PATH%
        )
    )
)

REM Install Reaper integration
if not %REAPER_PATH%=="" (
    echo [INFO] Installing Reaper integration...
    
    REM Create Scripts directory
    if not exist "%REAPER_PATH%\Scripts" mkdir "%REAPER_PATH%\Scripts"
    
    REM Copy SauceMax.lua
    if exist "reaper\SauceMax.lua" (
        copy "reaper\SauceMax.lua" "%REAPER_PATH%\Scripts\"
        echo [SUCCESS] SauceMax.lua installed to Reaper Scripts
    ) else (
        echo [WARNING] SauceMax.lua not found in reaper\ directory
    )
    
    REM Create SauceMax data directory
    if not exist "%REAPER_PATH%\SauceMax" mkdir "%REAPER_PATH%\SauceMax"
    if not exist "%REAPER_PATH%\SauceMax\presets" mkdir "%REAPER_PATH%\SauceMax\presets"
    if not exist "%REAPER_PATH%\SauceMax\analysis" mkdir "%REAPER_PATH%\SauceMax\analysis"
    
    REM Copy Python scripts
    if exist "scripts" (
        xcopy "scripts\*" "%REAPER_PATH%\SauceMax\" /s /y
        echo [SUCCESS] Python analysis scripts installed
    )
    
    echo [SUCCESS] Reaper integration complete!
    echo.
    echo To use SauceMax in Reaper:
    echo 1. Open Reaper
    echo 2. Go to Actions → Load ReaScript...
    echo 3. Select SauceMax.lua from the Scripts folder
    echo 4. The SauceMax interface will open
)

REM Test installation
echo [INFO] Testing SauceMax installation...
python -c "import sauce_maximizer; print('✓ SauceMax import successful')" 2>nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Python package test passed
) else (
    echo [ERROR] Python package test failed
    pause
    exit /b 1
)

REM Test dependencies
echo [INFO] Testing dependencies...
python -c "import numpy; print('  ✓ numpy')" 2>nul
python -c "import librosa; print('  ✓ librosa')" 2>nul
python -c "import sklearn; print('  ✓ scikit-learn')" 2>nul
python -c "import scipy; print('  ✓ scipy')" 2>nul

echo.
echo [SUCCESS] 🎉 SauceMax installation complete!
echo.
echo Next steps:
echo 1. If you created a virtual environment, activate it with:
echo    saucemax_env\Scripts\activate.bat
echo 2. Test the command line tool: saucemax --help
echo 3. Open Reaper and load the SauceMax script
echo 4. Visit https://github.com/trentbecknell/saucemax for documentation
echo.
echo Happy mixing! 🎵
echo.
pause
@echo off
setlocal
title Aria Bot Launcher

echo ==================================================
echo             Aria Bot Launcher
echo ==================================================
echo.

cd /d "%~dp0"

:: Check for Docker
docker info >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Docker is running.
    set DOCKER_AVAILABLE=1
) else (
    echo [INFO] Docker is NOT running or not installed.
    set DOCKER_AVAILABLE=0
)

:: Check for Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Python is available.
    set PYTHON_AVAILABLE=1
) else (
    echo [INFO] Python is NOT available.
    set PYTHON_AVAILABLE=0
)

echo.
if "%DOCKER_AVAILABLE%"=="1" (
    echo Docker detected. Recommended way to run.
    set /p MODE="Run via [D]ocker or [L]ocal? (Default: D): "
    if /i "%MODE%"=="L" goto :RUN_LOCAL
    goto :RUN_DOCKER
) else (
    if "%PYTHON_AVAILABLE%"=="1" (
        echo Docker not available. Falling back to Local run.
        goto :RUN_LOCAL
    ) else (
        echo [ERROR] Neither Docker nor Python were found!
        echo Please install Docker Desktop OR Python 3.10+ to run Aria Bot.
        pause
        exit /b 1
    )
)

:RUN_DOCKER
echo.
echo [MODE] Docker
echo Pulling latest image...
docker pull agent0ai/agent-zero
if %errorlevel% neq 0 (
    echo [ERROR] Failed to pull image.
    pause
    exit /b 1
)

echo Starting Aria Bot container...
echo Access the UI at http://localhost:50001
start "" "http://localhost:50001"
:: Using interactive mode so user can see output
docker run -it -p 50001:80 -v "%cd%":/a0 agent0ai/agent-zero
pause
goto :EOF


:RUN_LOCAL
echo.
echo [MODE] Local

:: Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create venv.
        pause
        exit /b 1
    )
    echo Upgrading pip...
    venv\Scripts\python -m pip install --upgrade pip

    echo Installing dependencies (this may take a while)...
    venv\Scripts\pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment found.
)

:: Create Icon and Shortcut logic
:: 1. Generate .ico if missing
if not exist "aria.ico" (
    if exist "scripts\convert_icon.py" (
        echo Generating icon...
        venv\Scripts\python scripts\convert_icon.py
    )
)

:: 2. Create Desktop Shortcut if .ico exists
if exist "aria.ico" (
    if exist "scripts\create_shortcut.ps1" (
        echo Creating Desktop shortcut...
        powershell -ExecutionPolicy Bypass -File "scripts\create_shortcut.ps1" -TargetFile "%~f0" -IconFile "%~dp0aria.ico"
    )
)

echo Starting Aria Bot...
echo Access the UI at http://localhost:5000
start "" "http://localhost:5000"
venv\Scripts\python run_ui.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application crashed or failed to start.
    echo If you see 'ModuleNotFoundError', try deleting the 'venv' folder and running this script again.
    pause
)
goto :EOF

@echo off
REM ============================================================================
REM MkDocs on Steroids - Windows Startup Script
REM ============================================================================
REM Startet beide Server:
REM 1. Build Control Server (Port 8001) - für Browser Build-Pause Toggle
REM 2. MkDocs serve (Port 8005) - mit Live Edit Support
REM ============================================================================

echo.
echo ============================================================================
echo   MkDocs on Steroids - Startup
echo ============================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python ist nicht installiert oder nicht im PATH!
    echo         Bitte installiere Python 3.10+ und füge es zum PATH hinzu.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python Version: %PYTHON_VERSION%
echo.

REM Check if mkdocs is installed
python -m mkdocs --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] MkDocs ist nicht installiert!
    echo         Führe aus: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [INFO] Installierte MkDocs Version:
python -m mkdocs --version
echo.

REM Create a unique lock file to prevent multiple instances
set LOCK_FILE=.mkdocs-servers-running.lock
if exist %LOCK_FILE% (
    echo [WARNING] Server scheinen bereits zu laufen!
    echo           Lock-Datei gefunden: %LOCK_FILE%
    echo.
    choice /C YN /M "Trotzdem starten"
    if errorlevel 2 exit /b 0
    del %LOCK_FILE%
)

REM Create lock file
echo Running > %LOCK_FILE%

echo ============================================================================
echo   Server werden gestartet...
echo ============================================================================
echo.

REM Start Build Control Server in background
echo [1/2] Starte Build Control Server (Port 8001)...
start "MkDocs Build Control Server" /MIN python mkdocs_build_control.py
timeout /t 2 /nobreak >nul
echo       ✓ Build Control Server gestartet
echo         URL: http://localhost:8001
echo.

REM Start MkDocs serve with Live Edit support
echo [2/2] Starte MkDocs Server (Port 8005)...
echo       ✓ MkDocs Server wird gestartet
echo         URL: http://127.0.0.1:8005
echo         Live Edit: AKTIVIERT (WebSocket Port 9001)
echo.

echo ============================================================================
echo   Server erfolgreich gestartet!
echo ============================================================================
echo.
echo   Dokumentation:  http://127.0.0.1:8005
echo   Build Control:  http://localhost:8001
echo.
echo   Features:
echo   • Live Edit      - Bearbeite Seiten direkt im Browser
echo   • Build Control  - Klicke auf den 🔨 Button oben rechts
echo   • Auto-Reload    - Änderungen werden automatisch geladen
echo.
echo   Drücke Ctrl+C zum Beenden der Server
echo ============================================================================
echo.

REM Start MkDocs serve (blocking, in foreground)
python -m mkdocs serve -a 0.0.0.0:8005

REM Cleanup when mkdocs exits
echo.
echo [INFO] Server werden beendet...
del %LOCK_FILE% 2>nul
taskkill /FI "WindowTitle eq MkDocs Build Control Server*" /T /F >nul 2>&1
echo [INFO] Alle Server beendet.
pause

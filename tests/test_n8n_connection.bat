@echo off
REM ============================================================================
REM Test n8n Webhook Connection
REM ============================================================================

REM Check if virtual environment exists
if not exist "venvWindows\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo         Please run setup_document_uploader.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venvWindows\Scripts\activate.bat

REM Run connection test
python test_n8n_connection.py

pause

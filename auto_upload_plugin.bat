@echo off
REM ============================================================================
REM Auto-Document and Upload Plugin Files
REM ============================================================================
REM Automatically documents and uploads all source files from mkdocs-llm-autodoc
REM ============================================================================

echo.
echo ============================================================================
echo   Auto-Document and Upload: mkdocs-llm-autodoc Plugin
echo ============================================================================
echo.

REM Check if virtual environment exists
if not exist "venvWindows\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo         Please run setup_document_uploader.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venvWindows\Scripts\activate.bat

echo This script will:
echo   1. Read all Python files in the plugin
echo   2. Generate documentation for each file
echo   3. Upload the source files to RAG
echo   4. Upload the generated documentation to RAG
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause > nul

echo.
echo [*] Processing mkdocs-llm-autodoc plugin files...
echo.

python auto_document_and_upload.py "plugins\mkdocs-llm-autodoc" --multiple-patterns "**/*.py" "**/*.md"

if errorlevel 1 (
    echo.
    echo [ERROR] Some files failed to process!
    echo         Check the log above for details.
    goto :error
)

echo.
echo ============================================================================
echo   Upload Complete!
echo ============================================================================
echo.
echo   All plugin files and their documentation have been uploaded to RAG.
echo   You can now query the RAG system about the plugin!
echo.
echo ============================================================================
pause
exit /b 0

:error
echo.
echo ============================================================================
echo   Upload Failed!
echo ============================================================================
echo.
pause
exit /b 1

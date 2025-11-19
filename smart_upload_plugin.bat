@echo off
REM ============================================================================
REM Smart Auto-Upload Plugin (with code analysis)
REM ============================================================================
REM Analyzes Python code, generates detailed docs, and uploads everything
REM ============================================================================

echo.
echo ============================================================================
echo   Smart Auto-Upload: mkdocs-llm-autodoc Plugin
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

echo This will:
echo   - Analyze all Python files in the plugin
echo   - Extract classes, functions, and docstrings
echo   - Generate detailed documentation
echo   - Upload source files to RAG
echo   - Upload generated documentation to RAG
echo   - Upload existing markdown files
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause > nul

echo.
python smart_auto_upload.py "plugins\mkdocs-llm-autodoc"

if errorlevel 1 (
    echo.
    echo [WARNING] Some files encountered errors (see above)
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo   Upload Complete!
echo ============================================================================
echo.
echo   The RAG system now contains:
echo   - All Python source files from the plugin
echo   - Auto-generated documentation with code analysis
echo   - All existing markdown documentation
echo.
echo   You can now query about classes, functions, and implementation details!
echo.
echo ============================================================================
pause
exit /b 0

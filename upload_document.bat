@echo off
REM ============================================================================
REM Document Upload Service - Upload Script
REM ============================================================================
REM Usage: upload_document.bat <file_path> [chunk_size] [chunk_overlap]
REM ============================================================================

setlocal enabledelayedexpansion

if "%~1"=="" (
    echo.
    echo Usage: upload_document.bat ^<file_path^> [chunk_size] [chunk_overlap]
    echo.
    echo Examples:
    echo   upload_document.bat example.cpp
    echo   upload_document.bat document.pdf 1500 250
    echo   upload_document.bat README.md
    echo.
    echo Supported file types:
    echo   - Source code: .py .cpp .h .hpp .c .java .js .ts .go .rs etc.
    echo   - Documents: .md .txt .pdf .html .xml
    echo   - LaTeX: .tex .latex
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venvWindows\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo         Please run setup_document_uploader.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venvWindows\Scripts\activate.bat

REM Check if file exists
if not exist "%~1" (
    echo [ERROR] File not found: %~1
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo   Uploading Document
echo ============================================================================
echo   File: %~1
if not "%~2"=="" echo   Chunk Size: %~2
if not "%~3"=="" echo   Chunk Overlap: %~3
echo ============================================================================
echo.

REM Build command
set CMD=python document_uploader.py "%~1"
if not "%~2"=="" set CMD=!CMD! --chunk-size %~2
if not "%~3"=="" set CMD=!CMD! --chunk-overlap %~3

REM Execute upload
!CMD!

if errorlevel 1 (
    echo.
    echo [ERROR] Upload failed!
    pause
    exit /b 1
)

echo.
echo ============================================================================
pause

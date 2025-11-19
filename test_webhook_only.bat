@echo off
REM ============================================================================
REM Test Webhook Connection - Quick Test
REM ============================================================================
REM This script tests if the new webhook endpoint is working
REM ============================================================================

echo.
echo ============================================================================
echo   Testing New Webhook Endpoint
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

echo [1/2] Testing webhook connectivity...
echo.

REM Create a simple test using Python
python -c "import requests; import json; import os; from dotenv import load_dotenv; load_dotenv('.env.windows'); load_dotenv('.env'); url = os.getenv('N8N_WEBHOOK_URL'); print(f'Testing webhook: {url}'); payload = {'file_name': 'test.txt', 'file_path': 'test.txt', 'file_type': '.txt', 'total_chunks': 2, 'chunks': ['Test chunk 1 - Hello from Python uploader!', 'Test chunk 2 - This is a simple webhook test.'], 'metadata': {'test': True}}; response = requests.post(url, json=payload, timeout=10); print(f'Status: {response.status_code}'); print(f'Response: {response.text}'); exit(0 if response.status_code == 200 else 1)"

if errorlevel 1 (
    echo.
    echo [ERROR] Webhook test failed!
    echo.
    echo Possible issues:
    echo   1. n8n is not running at the configured URL
    echo   2. The new webhook is not activated in n8n
    echo   3. The webhook path is incorrect
    echo.
    echo Please check:
    echo   - Is n8n running? Check http://192.168.0.72:5678
    echo   - Did you import RAG_with_python_uploader.json?
    echo   - Is the workflow activated (toggle in top right)?
    echo.
    goto :error
)

echo.
echo       ✓ Webhook test successful!
echo.

echo [2/2] Checking if embeddings were generated...
echo       (Check your n8n execution log to verify embeddings)
echo.

echo ============================================================================
echo   Webhook Test Passed!
echo ============================================================================
echo.
echo   The webhook is responding correctly.
echo
echo   Next steps:
echo   1. Open n8n at http://192.168.0.72:5678
echo   2. Check the execution log for the RAG workflow
echo   3. Verify that:
echo      - Webhook received the data
echo      - Extract Chunks processed the array
echo      - Embeddings were generated
echo      - Documents were stored in Qdrant
echo.
echo   If everything looks good, run: test_upload.bat
echo.
echo ============================================================================
pause
exit /b 0

:error
echo.
echo ============================================================================
echo   Webhook Test Failed!
echo ============================================================================
echo.
pause
exit /b 1

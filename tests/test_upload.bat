@echo off
REM ============================================================================
REM Document Upload Service - Test Script
REM ============================================================================
REM Tests the document upload service with sample files
REM ============================================================================

echo.
echo ============================================================================
echo   Document Upload Service - Testing
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

REM Create test files directory
if not exist "test_documents" mkdir test_documents

echo [1/4] Creating test files...

REM Create a test C++ file
echo #include ^<iostream^> > test_documents\test.cpp
echo. >> test_documents\test.cpp
echo // Test C++ file for document upload service >> test_documents\test.cpp
echo. >> test_documents\test.cpp
echo class Example { >> test_documents\test.cpp
echo public: >> test_documents\test.cpp
echo     Example() {} >> test_documents\test.cpp
echo     void doSomething() { >> test_documents\test.cpp
echo         std::cout ^<^< "Hello from C++ test file!" ^<^< std::endl; >> test_documents\test.cpp
echo     } >> test_documents\test.cpp
echo }; >> test_documents\test.cpp
echo. >> test_documents\test.cpp
echo int main() { >> test_documents\test.cpp
echo     Example ex; >> test_documents\test.cpp
echo     ex.doSomething(); >> test_documents\test.cpp
echo     return 0; >> test_documents\test.cpp
echo } >> test_documents\test.cpp

REM Create a test Markdown file
echo # Test Markdown Document > test_documents\test.md
echo. >> test_documents\test.md
echo This is a test markdown file for the document upload service. >> test_documents\test.md
echo. >> test_documents\test.md
echo ## Features >> test_documents\test.md
echo. >> test_documents\test.md
echo - Automatic text splitting >> test_documents\test.md
echo - Language-aware processing >> test_documents\test.md
echo - Support for multiple file formats >> test_documents\test.md
echo. >> test_documents\test.md
echo ## Code Example >> test_documents\test.md
echo. >> test_documents\test.md
echo ```python >> test_documents\test.md
echo def hello_world(): >> test_documents\test.md
echo     print("Hello, World!") >> test_documents\test.md
echo ``` >> test_documents\test.md
echo. >> test_documents\test.md
echo This document will be split using the MarkdownTextSplitter. >> test_documents\test.md

REM Create a test Python file
echo # Test Python file for document upload service > test_documents\test.py
echo. >> test_documents\test.py
echo def fibonacci(n): >> test_documents\test.py
echo     """Calculate the nth Fibonacci number.""" >> test_documents\test.py
echo     if n ^<= 1: >> test_documents\test.py
echo         return n >> test_documents\test.py
echo     return fibonacci(n-1) + fibonacci(n-2) >> test_documents\test.py
echo. >> test_documents\test.py
echo class Calculator: >> test_documents\test.py
echo     """A simple calculator class.""" >> test_documents\test.py
echo     def add(self, a, b): >> test_documents\test.py
echo         return a + b >> test_documents\test.py
echo. >> test_documents\test.py
echo if __name__ == "__main__": >> test_documents\test.py
echo     print(fibonacci(10)) >> test_documents\test.py

echo       ✓ Test files created in test_documents\
echo.

echo [2/4] Testing C++ file upload...
python document_uploader.py test_documents\test.cpp
if errorlevel 1 (
    echo [ERROR] C++ file upload failed!
    goto :error
)
echo       ✓ C++ file upload successful
echo.

echo [3/4] Testing Markdown file upload...
python document_uploader.py test_documents\test.md
if errorlevel 1 (
    echo [ERROR] Markdown file upload failed!
    goto :error
)
echo       ✓ Markdown file upload successful
echo.

echo [4/4] Testing Python file upload...
python document_uploader.py test_documents\test.py
if errorlevel 1 (
    echo [ERROR] Python file upload failed!
    goto :error
)
echo       ✓ Python file upload successful
echo.

echo ============================================================================
echo   All Tests Passed!
echo ============================================================================
echo.
echo   Test files are located in: test_documents\
echo   You can now upload your own files using: upload_document.bat ^<file^>
echo.
echo ============================================================================
pause
exit /b 0

:error
echo.
echo ============================================================================
echo   Tests Failed!
echo ============================================================================
echo.
echo   Please check:
echo   1. Is the n8n service running at %N8N_WEBHOOK_URL%?
echo   2. Is the webhook URL correct in .env?
echo   3. Check the error messages above for details
echo.
echo ============================================================================
pause
exit /b 1

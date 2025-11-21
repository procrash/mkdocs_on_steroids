@echo off
REM Quick Start Script for MkDocs with Docker (Windows)

echo ========================================================================
echo      MkDocs with RAG ^& Docker - Quick Start
echo ========================================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo OK: Docker is running
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo OK: .env file created
    echo WARNING: Please edit .env and set SOURCE_CODE_PATH
    echo.
)

REM Start services
echo Starting Docker services...
echo.
docker-compose up -d

echo.
echo Waiting for services to be healthy...
timeout /t 5 /nobreak >nul

REM Check services
echo.
echo Service Status:
docker-compose ps

echo.
echo ========================================================================
echo  Services Started Successfully!
echo ========================================================================
echo.
echo Documentation:    http://localhost:8000
echo Chatbot API:      http://localhost:8765
echo Qdrant Dashboard: http://localhost:6333/dashboard
echo MinIO Console:    http://localhost:9001
echo     Login: admin / password123
echo.
echo View logs:
echo     docker-compose logs -f mkdocs
echo.
echo Stop services:
echo     docker-compose down
echo.
pause

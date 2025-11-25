#!/bin/bash
################################################################################
# MkDocs on Steroids - Linux/macOS Startup Script
################################################################################
# Startet beide Server:
# 1. Build Control Server (Port 8001) - für Browser Build-Pause Toggle
# 2. MkDocs serve (Port 8005) - mit Live Edit Support
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Lock file to prevent multiple instances
LOCK_FILE=".mkdocs-servers-running.lock"

# PID file for tracking background processes
BUILD_CONTROL_PID_FILE=".build-control-server.pid"

# Cleanup function
cleanup() {
    echo ""
    echo -e "${BLUE}============================================================================${NC}"
    echo -e "${YELLOW}[INFO] Server werden beendet...${NC}"
    echo -e "${BLUE}============================================================================${NC}"

    # Kill Build Control Server
    if [ -f "$BUILD_CONTROL_PID_FILE" ]; then
        BUILD_CONTROL_PID=$(cat "$BUILD_CONTROL_PID_FILE")
        if ps -p "$BUILD_CONTROL_PID" > /dev/null 2>&1; then
            echo -e "${YELLOW}[INFO] Beende Build Control Server (PID: $BUILD_CONTROL_PID)...${NC}"
            kill "$BUILD_CONTROL_PID" 2>/dev/null || true
        fi
        rm -f "$BUILD_CONTROL_PID_FILE"
    fi

    # Remove lock file
    rm -f "$LOCK_FILE"

    echo -e "${GREEN}[INFO] Alle Server beendet.${NC}"
    echo ""
    exit 0
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Print header
echo ""
echo -e "${BLUE}============================================================================${NC}"
echo -e "${BLUE}  MkDocs on Steroids - Startup${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}[ERROR] Python ist nicht installiert!${NC}"
    echo -e "${RED}        Bitte installiere Python 3.10+ und versuche es erneut.${NC}"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}[INFO] Python Version: $PYTHON_VERSION${NC}"
echo ""

# Check if mkdocs is installed
if ! $PYTHON_CMD -m mkdocs --version &> /dev/null; then
    echo -e "${RED}[ERROR] MkDocs ist nicht installiert!${NC}"
    echo -e "${RED}        Führe aus: pip install -r requirements.txt${NC}"
    exit 1
fi

# Display MkDocs version
echo -e "${GREEN}[INFO] Installierte MkDocs Version:${NC}"
$PYTHON_CMD -m mkdocs --version
echo ""

# Check for existing lock file
if [ -f "$LOCK_FILE" ]; then
    echo -e "${YELLOW}[WARNING] Server scheinen bereits zu laufen!${NC}"
    echo -e "${YELLOW}          Lock-Datei gefunden: $LOCK_FILE${NC}"
    echo ""
    read -p "Trotzdem starten? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
    rm -f "$LOCK_FILE"
fi

# Create lock file
echo "Running at $(date)" > "$LOCK_FILE"

echo -e "${BLUE}============================================================================${NC}"
echo -e "${BLUE}  Server werden gestartet...${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""

# Start Build Control Server in background
echo -e "${YELLOW}[1/2] Starte Build Control Server (Port 8001)...${NC}"
$PYTHON_CMD mkdocs_build_control.py > /dev/null 2>&1 &
BUILD_CONTROL_PID=$!
echo $BUILD_CONTROL_PID > "$BUILD_CONTROL_PID_FILE"

# Wait for Build Control Server to start
sleep 2

# Check if Build Control Server is still running
if ! ps -p "$BUILD_CONTROL_PID" > /dev/null 2>&1; then
    echo -e "${RED}[ERROR] Build Control Server konnte nicht gestartet werden!${NC}"
    cleanup
    exit 1
fi

echo -e "${GREEN}      ✓ Build Control Server gestartet (PID: $BUILD_CONTROL_PID)${NC}"
echo -e "${GREEN}        URL: http://localhost:8001${NC}"
echo ""

# Start MkDocs serve with Live Edit support
echo -e "${YELLOW}[2/2] Starte MkDocs Server (Port 8005)...${NC}"
echo -e "${GREEN}      ✓ MkDocs Server wird gestartet${NC}"
echo -e "${GREEN}        URL: http://127.0.0.1:8005${NC}"
echo -e "${GREEN}        Live Edit: AKTIVIERT (WebSocket Port 9001)${NC}"
echo ""

echo -e "${BLUE}============================================================================${NC}"
echo -e "${GREEN}  Server erfolgreich gestartet!${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""
echo -e "  ${BLUE}Dokumentation:${NC}  http://127.0.0.1:8005"
echo -e "  ${BLUE}Build Control:${NC}  http://localhost:8001"
echo ""
echo -e "  ${GREEN}Features:${NC}"
echo -e "  ${GREEN}•${NC} Live Edit      - Bearbeite Seiten direkt im Browser"
echo -e "  ${GREEN}•${NC} Build Control  - Klicke auf den 🔨 Button oben rechts"
echo -e "  ${GREEN}•${NC} Auto-Reload    - Änderungen werden automatisch geladen"
echo ""
echo -e "  ${YELLOW}Drücke Ctrl+C zum Beenden der Server${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""

# Start MkDocs serve (blocking, in foreground)
$PYTHON_CMD -m mkdocs serve -a 0.0.0.0:8005

# Cleanup will be called automatically via trap

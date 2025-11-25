#!/usr/bin/env python3
"""
MkDocs Build Control Server
============================
Kleiner HTTP-Server, der vom Browser aus gesteuert werden kann,
um den MkDocs HTML-Build zu pausieren/fortzusetzen.

Die LLM-Dokumentations-Generierung läuft weiter im Hintergrund,
aber die HTML-Dateien werden nicht neu gebaut, wenn pausiert.

Usage:
    python mkdocs_build_control.py

Der Server läuft auf http://localhost:8001
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from pathlib import Path
from datetime import datetime

# Flag-Datei, die anzeigt, ob der Build pausiert ist
BUILD_PAUSE_FLAG = Path('.mkdocs-build-paused')


class BuildControlHandler(BaseHTTPRequestHandler):
    """Handler für Build-Control-Requests"""

    def _set_headers(self, status=200):
        """Setze CORS-Headers für Browser-Zugriff"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self._set_headers()

    def do_GET(self):
        """GET /status - Gibt den aktuellen Build-Status zurück"""
        if self.path == '/status':
            is_paused = BUILD_PAUSE_FLAG.exists()
            response = {
                'paused': is_paused,
                'timestamp': datetime.now().isoformat()
            }
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_POST(self):
        """POST /pause oder /resume - Pausiert/Aktiviert den Build"""
        if self.path == '/pause':
            # Erstelle Flag-Datei
            BUILD_PAUSE_FLAG.touch()
            response = {
                'status': 'paused',
                'message': 'MkDocs HTML-Build pausiert. LLM-Generierung läuft weiter.',
                'timestamp': datetime.now().isoformat()
            }
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
            print(f"🟡 Build pausiert um {datetime.now().strftime('%H:%M:%S')}")

        elif self.path == '/resume':
            # Lösche Flag-Datei
            if BUILD_PAUSE_FLAG.exists():
                BUILD_PAUSE_FLAG.unlink()
            response = {
                'status': 'active',
                'message': 'MkDocs HTML-Build aktiviert',
                'timestamp': datetime.now().isoformat()
            }
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
            print(f"🟢 Build fortgesetzt um {datetime.now().strftime('%H:%M:%S')}")

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def log_message(self, format, *args):
        """Überschreibe Standard-Logging für sauberere Ausgabe"""
        pass  # Deaktiviere Standard-Request-Logs


def run_server(port=8001):
    """Starte den Control Server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, BuildControlHandler)

    print("=" * 60)
    print("🎛️  MkDocs Build Control Server")
    print("=" * 60)
    print(f"Server läuft auf: http://localhost:{port}")
    print(f"Status prüfen:    GET  http://localhost:{port}/status")
    print(f"Build pausieren:  POST http://localhost:{port}/pause")
    print(f"Build fortsetzen: POST http://localhost:{port}/resume")
    print("=" * 60)
    print("Drücke Ctrl+C zum Beenden")
    print()

    # Initiale Status-Ausgabe
    if BUILD_PAUSE_FLAG.exists():
        print("🟡 Status: Build ist PAUSIERT")
    else:
        print("🟢 Status: Build ist AKTIV")
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server wird beendet...")
        httpd.shutdown()
        print("✅ Server beendet")


if __name__ == '__main__':
    run_server()

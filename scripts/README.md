# Scripts

Dieses Verzeichnis enthält Hilfsskripte für die MkDocs-Dokumentation.

## Start-Skripte

| Skript | Plattform | Beschreibung |
|--------|-----------|--------------|
| `start.sh` | Linux/macOS | Startet den MkDocs-Server mit allen Abhängigkeiten |
| `start.bat` | Windows | Startet den MkDocs-Server mit allen Abhängigkeiten |
| `serve.bat` | Windows | Einfaches Serverskript |

## Setup-Skripte

| Skript | Beschreibung |
|--------|--------------|
| `setup_llm_autodoc.py` | Interaktives Setup für das LLM AutoDoc Plugin |

## Build-Hooks

| Skript | Beschreibung |
|--------|--------------|
| `build_control.py` | MkDocs Build-Hook für erweiterte Build-Kontrolle |
| `mkdocs_build_control.py` | Zusätzliche Build-Kontrolle |

## Utility-Skripte

| Skript | Beschreibung |
|--------|--------------|
| `fix_fstrings.py` | Korrigiert f-String-Syntax in Python-Dateien |
| `fix_detailed_agent.py` | Fixes für den Detailed-Agent |

## Verwendung

### Server starten

```bash
# Linux/macOS
./scripts/start.sh

# Windows
scripts\start.bat
```

### LLM AutoDoc einrichten

```bash
python scripts/setup_llm_autodoc.py
```

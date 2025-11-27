# Quick Start Guide

Starte die MkDocs-Dokumentation in 3 Schritten!

## 1. Python-Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

## 2. Development-Server starten

### Windows
```cmd
serve.bat
```

### Linux/macOS
```bash
mkdocs serve
```

## 3. Im Browser öffnen

Öffne http://127.0.0.1:8000 in deinem Browser.

## Theme wechseln

Bearbeite `mkdocs.yml` und kommentiere/dekommentiere die Theme-Sektion:

```yaml
# Material Theme (aktiv)
theme:
  name: material
  # ...

# ReadTheDocs Theme (inaktiv)
# theme:
#   name: readthedocs
```

Speichern und MkDocs lädt automatisch neu!

## Production Build erstellen

```bash
mkdocs build
```

Die fertige Website wird in `site/` erstellt.

## Mehr Infos

Siehe [README.md](README.md) für vollständige Dokumentation.

## Probleme?

- Stelle sicher, dass Python 3.8+ installiert ist
- Prüfe, ob alle Dependencies installiert sind: `pip list | grep mkdocs`
- Bei Port-Konflikten: `mkdocs serve --dev-addr 127.0.0.1:8001`

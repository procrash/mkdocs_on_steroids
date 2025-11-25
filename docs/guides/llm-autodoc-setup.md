# LLM AutoDoc Setup Script

Automatisiertes Setup-Script für die Konfiguration des MkDocs LLM AutoDoc Plugins.

## Verwendung

```bash
python setup_llm_autodoc.py
```

Das Script führt Sie interaktiv durch folgende Schritte:

### 1. LLM Provider auswählen

- **Anthropic Claude** - Beste Code-Verständnis, empfohlen (~$2-5 für typisches Projekt)
- **OpenAI GPT-4** - Gute Qualität (~$10-20 für typisches Projekt)
- **Ollama** - Kostenlos, läuft lokal
- **LM Studio** - Kostenlos, läuft lokal mit GUI

### 2. C++ Projekt-Pfad angeben

Geben Sie den Pfad zu Ihrem C++ Projekt an (relativ zum mkdocs Ordner):
- `../cpp-project` - Projekt im übergeordneten Ordner
- `./cpp-project` - Projekt im mkdocs Ordner
- Eigener Pfad

### 3. Dokumentationsebenen wählen

- **High-Level**: Projektübersicht & Architektur mit Mermaid-Diagrammen
- **Mid-Level**: Modul-Dokumentation mit Klassen und Dependencies
- **Detailed-Level**: Vollständige API-Referenz mit Beispielen

### 4. Code-Review aktivieren

Entscheiden Sie, ob automatische Code-Reviews und Verbesserungsvorschläge generiert werden sollen.

## Was macht das Script?

1. Stellt Ihnen interaktive Fragen zur Konfiguration
2. Zeigt eine Zusammenfassung Ihrer Auswahl
3. Aktualisiert automatisch Ihre `mkdocs.yml` Datei
4. Fügt die komplette Plugin-Konfiguration hinzu
5. Zeigt Ihnen die nächsten Schritte an

## Nach dem Setup

### Für Cloud-Provider (Anthropic/OpenAI):

```bash
# Setzen Sie Ihren API-Key
export ANTHROPIC_API_KEY='your-api-key'
# oder
export OPENAI_API_KEY='your-api-key'
```

### Für lokale Provider:

**Ollama:**
```bash
ollama serve
```

**LM Studio:**
1. LM Studio starten
2. Modell laden
3. Developer → Start Server

### Dokumentation generieren:

```bash
# Plugin installieren (falls noch nicht geschehen)
cd plugins/mkdocs-llm-autodoc
pip install -e .
cd ../..

# Dokumentation generieren
mkdocs build

# Dokumentation ansehen
mkdocs serve
```

Öffnen Sie dann http://localhost:8000

## Beispiel-Durchlauf

```
==================================================================
  MkDocs LLM AutoDoc Plugin - Automatisches Setup
==================================================================

Dieses Script hilft Ihnen bei der Konfiguration des LLM AutoDoc Plugins.
Es wird Ihre mkdocs.yml Datei automatisch aktualisieren.

==================================================================
  Schritt 1: LLM Provider
==================================================================

[1] Anthropic Claude
    Beste Code-Verständnis, empfohlen. Benötigt API-Key (~$2-5 für typisches Projekt)

[2] OpenAI GPT-4
    Gute Qualität. Benötigt API-Key (~$10-20 für typisches Projekt)

[3] Ollama
    Kostenlos, läuft lokal. Benötigt Ollama Installation

[4] LM Studio
    Kostenlos, läuft lokal mit GUI. Benötigt LM Studio Installation

Wählen Sie Ihren LLM Provider (1-4): 3
Modellname [llama3]: codellama
Server URL [http://localhost:11434/v1]:

... (weitere Schritte)

==================================================================
  Zusammenfassung Ihrer Konfiguration
==================================================================

LLM Provider:        ollama
LLM Modell:          codellama
LLM Server URL:      http://localhost:11434/v1
C++ Projekt-Pfad:    ./cpp-project
High-Level Docs:     ✓
Mid-Level Docs:      ✓
Detailed-Level Docs: ✓
Code-Review:         ✓

Möchten Sie mit dieser Konfiguration fortfahren? (j/n): j

... (Script aktualisiert mkdocs.yml)

✓ mkdocs.yml wurde erfolgreich aktualisiert!
```

## Erneute Konfiguration

Sie können das Script jederzeit erneut ausführen, um Ihre Konfiguration zu ändern.
Das Script erkennt bestehende Konfigurationen und fragt, ob Sie diese ersetzen möchten.

## Für andere Projekte verwenden

Kopieren Sie einfach das Script in ein anderes MkDocs-Projekt:

```bash
cp setup_llm_autodoc.py /pfad/zu/anderem/projekt/
cd /pfad/zu/anderem/projekt/
python setup_llm_autodoc.py
```

## Fehlerbehebung

### "mkdocs.yml nicht gefunden"
- Stellen Sie sicher, dass Sie das Script im mkdocs Hauptverzeichnis ausführen
- Das Verzeichnis sollte eine `mkdocs.yml` Datei enthalten

### "Plugin Position nicht gefunden"
- Das Script sucht nach `git-revision-date-localized` Plugin
- Stellen Sie sicher, dass Ihre `mkdocs.yml` eine standard Plugin-Sektion hat

### Script bricht ab
- Drücken Sie `Ctrl+C` um das Setup abzubrechen
- Ihre `mkdocs.yml` wird nicht verändert, wenn Sie abbrechen

## Manuelle Konfiguration

Falls Sie das Plugin manuell konfigurieren möchten, siehe:
- `plugins/mkdocs-llm-autodoc/README.md`
- `plugins/mkdocs-llm-autodoc/QUICKSTART.md`

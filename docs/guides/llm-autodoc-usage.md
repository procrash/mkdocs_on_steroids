# MkDocs LLM AutoDoc Plugin - Verwendung

## ✅ Status: Plugin erfolgreich konfiguriert!

Das LLM AutoDoc Plugin wurde erfolgreich installiert und konfiguriert.

## Aktuelle Konfiguration

Ihr Plugin ist konfiguriert für:
- **LLM Provider**: OpenAI-kompatibler Server
- **Server URL**: `http://localhost:11434/v1`
- **C++ Projekt**: `./cpp-project`
- **Dokumentationsebenen**: High-Level, Mid-Level, Detailed-Level (alle aktiviert)
- **Code-Review**: Aktiviert
- **Caching**: Aktiviert

## Vor der ersten Verwendung

### 1. LLM Server starten

Stellen Sie sicher, dass Ihr lokaler LLM-Server läuft:

**Für Ollama:**
```bash
ollama serve
```

**Für LM Studio:**
1. LM Studio öffnen
2. Ein Modell laden (z.B. CodeLlama, DeepSeek Coder, Mistral)
3. Server starten: Developer → Start Server (Port 11434)

**Für Ollama mit anderem Port:**
Falls Ihr Server auf einem anderen Port läuft, passen Sie die `llm_base_url` in `mkdocs.yml` an.

### 2. Modellname anpassen

Öffnen Sie `mkdocs.yml` und ändern Sie den Modellnamen:
```yaml
llm_model: 'local-model'  # Ändern Sie dies!
```

Zu Ihrem tatsächlichen Modellnamen, z.B.:
- `'llama3'`
- `'codellama'`
- `'deepseek-coder'`
- `'mistral'`
- Etc.

## Dokumentation generieren

### Erste Generation (vollständig)

```bash
mkdocs build
```

Das Plugin wird:
1. Ihr C++ Projekt analysieren (`./cpp-project/`)
2. Mit dem LLM-Server kommunizieren
3. Drei Ebenen von Dokumentation generieren:
   - `docs/generated/` - High-Level (Projektübersicht, Architektur)
   - `docs/generated/modules/` - Mid-Level (Module, Klassen)
   - `docs/generated/api/` - Detailed-Level (API-Referenz)
4. Code-Review Berichte erstellen

### Nur geänderte Dateien neu generieren

Das Plugin cached automatisch! Beim nächsten Build werden nur geänderte Dateien neu dokumentiert:

```bash
# C++ Datei ändern
echo "// Updated" >> cpp-project/src/myfile.cpp

# Nur die geänderte Datei wird neu dokumentiert
mkdocs build
```

### Alles neu generieren (Cache ignorieren)

```yaml
# In mkdocs.yml:
plugins:
  - llm-autodoc:
      force_regenerate: true  # Cache wird ignoriert
```

## Dokumentation ansehen

```bash
mkdocs serve
```

Öffnen Sie dann http://localhost:8000 in Ihrem Browser.

## Konfiguration anpassen

### Andere LLM-Provider verwenden

Sie können jederzeit das Setup-Script erneut ausführen:

```bash
python setup_llm_autodoc.py
```

Oder manuell in `mkdocs.yml` ändern:

**Anthropic Claude:**
```yaml
llm_provider: 'anthropic'
llm_model: 'claude-3-5-sonnet-20241022'
llm_api_key: !ENV ANTHROPIC_API_KEY
llm_base_url: null  # Nicht benötigt
```

**OpenAI GPT-4:**
```yaml
llm_provider: 'openai'
llm_model: 'gpt-4'
llm_api_key: !ENV OPENAI_API_KEY
llm_base_url: null  # Nicht benötigt
```

### Dokumentationsebenen selektiv aktivieren

Um Zeit und Kosten zu sparen, können Sie einzelne Ebenen deaktivieren:

```yaml
generate_high_level: true      # Projekt-Übersicht (schnell)
generate_mid_level: true       # Modul-Dokumentation (mittel)
generate_detailed_level: false # API-Referenz (langsam) - DEAKTIVIERT
```

### Bestimmte Dateien ausschließen

```yaml
exclude_patterns:
  - '**/build/**'
  - '**/third_party/**'
  - '**/test/**'
  - '**/examples/**'
  - '**/deprecated/**'
```

### Parallele LLM-Aufrufe anpassen

```yaml
max_concurrent_llm_calls: 3  # Standard
# Reduzieren bei Rate-Limits: 1
# Erhöhen für schnellere Builds: 5
```

## Generierte Dateien

Nach dem Build finden Sie:

```
docs/
├── generated/
│   ├── 00-getting-started.md     # Projekt-Übersicht
│   ├── 01-architecture.md        # Architektur & Diagramme
│   ├── modules/
│   │   ├── core.md              # Core-Modul Dokumentation
│   │   ├── utils.md             # Utils-Modul Dokumentation
│   │   └── ...
│   └── api/
│       ├── classes/
│       │   ├── myclass.md       # Detaillierte Klassen-Dokumentation
│       │   └── ...
│       └── functions/
│           ├── helpers.md       # Funktions-Dokumentation
│           └── ...
```

## Cache-Verwaltung

### Cache-Verzeichnis

Der Cache wird gespeichert in `.cache/llm-autodoc/`

### Cache löschen

```bash
rm -rf .cache/llm-autodoc
```

Oder in PowerShell:
```powershell
Remove-Item -Recurse -Force .cache\llm-autodoc
```

## Fehlerbehebung

### "No API key provided"

**Problem:** Das Plugin kann nicht mit dem LLM kommunizieren.

**Lösung:**
1. Für lokale Server (Ollama/LM Studio): Stellen Sie sicher, dass `llm_api_key: 'not-needed'` gesetzt ist
2. Für Cloud-Provider: Setzen Sie die Umgebungsvariable:
   ```bash
   export ANTHROPIC_API_KEY='your-key'
   # oder
   export OPENAI_API_KEY='your-key'
   ```

### "Failed to initialize LLM provider"

**Problem:** Der LLM-Server ist nicht erreichbar.

**Lösung:**
1. Prüfen Sie, ob der Server läuft:
   ```bash
   curl http://localhost:11434/v1/models
   ```
2. Prüfen Sie die `llm_base_url` in `mkdocs.yml`
3. Für Ollama: `ollama serve`
4. Für LM Studio: Server starten in der GUI

### "C++ project path not found"

**Problem:** Der Pfad zum C++ Projekt ist falsch.

**Lösung:**
1. Prüfen Sie `cpp_project_path` in `mkdocs.yml`
2. Der Pfad ist relativ zum mkdocs Hauptverzeichnis
3. Beispiel: Wenn Ihr Projekt in `Z:\mkdocs\cpp-project\` liegt, verwenden Sie `'./cpp-project'`

### Build dauert sehr lange

**Problem:** Das Plugin wartet auf LLM-Antworten.

**Lösungen:**
1. Reduzieren Sie `max_concurrent_llm_calls`
2. Deaktivieren Sie `generate_detailed_level` für schnellere Builds
3. Nutzen Sie Caching (`enable_cache: true`)
4. Schließen Sie Test-Dateien aus

### "Tree-sitter not available"

**Problem:** C++ Parser fehlt (nicht kritisch).

**Lösung:**
```bash
pip install tree-sitter tree-sitter-cpp
```

Das Plugin funktioniert auch mit dem Fallback-Parser, aber tree-sitter ist genauer.

## Performance-Tipps

### 1. Caching verwenden
```yaml
enable_cache: true  # Standard
force_regenerate: false  # Nur bei Bedarf auf true
```

### 2. Selektive Generation
```yaml
# Für schnelle Builds:
generate_high_level: true
generate_mid_level: true
generate_detailed_level: false  # Überspringen
```

### 3. Tests ausschließen
```yaml
exclude_patterns:
  - '**/test/**'
  - '**/tests/**'
  - '**/*_test.cpp'
```

### 4. Lokale Modelle nutzen
- Ollama und LM Studio sind kostenlos
- Keine API-Kosten
- Oft schneller als Cloud-APIs bei kleinen Projekten

## Kosten (bei Cloud-Providern)

### Typisches mittelgroßes C++ Projekt (50-100 Dateien):

**Anthropic Claude:**
- Erste vollständige Generation: ~$2-5
- Inkrementelle Updates: ~$0.10-0.50

**OpenAI GPT-4:**
- Erste vollständige Generation: ~$10-20
- Inkrementelle Updates: ~$0.50-2

**Ollama/LM Studio:**
- Kostenlos! 🎉

## Für andere Projekte verwenden

```bash
# 1. Script kopieren
cp setup_llm_autodoc.py /pfad/zu/anderem/projekt/

# 2. Im neuen Projekt ausführen
cd /pfad/zu/anderem/projekt/
python setup_llm_autodoc.py

# 3. Plugin installieren
cd plugins/mkdocs-llm-autodoc
pip install -e .

# 4. Dokumentation generieren
mkdocs build
```

## Weitere Informationen

- **Plugin-Dokumentation**: `plugins/mkdocs-llm-autodoc/README.md`
- **Quick Start**: `plugins/mkdocs-llm-autodoc/QUICKSTART.md`
- **Setup-Script**: `SETUP_README.md`

## Support

Bei Problemen:
1. Prüfen Sie diese Datei
2. Lesen Sie die Plugin-Dokumentation
3. Prüfen Sie die MkDocs Build-Logs (`mkdocs build --verbose`)
4. Testen Sie die LLM-Verbindung manuell

---

**Viel Erfolg mit Ihrer automatisch generierten C++ Dokumentation! 🚀**

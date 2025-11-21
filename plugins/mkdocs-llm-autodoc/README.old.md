# MkDocs LLM AutoDoc Plugin

Ein intelligentes MkDocs-Plugin, das automatisch mehrstufige C++-Dokumentation mithilfe von Large Language Models (LLMs) generiert.

## Features

- **Drei Dokumentationsebenen:**
  - **High-Level**: Projektübersicht, Architektur, Einstiegspunkte (300 Wörter mit Mermaid-Diagrammen)
  - **Mid-Level**: Modul-Dokumentation mit Klassen, Dependencies und Verwendungsszenarien
  - **Detailed-Level**: Vollständige API-Dokumentation mit Parametern, Beispielen und Fehlerbehandlung

- **Background-Generierung (NEU!):**
  - 🚀 Nicht-blockierende Dokumentationsgenerierung im Hintergrund
  - 📚 Bereits vorhandene Dokumentation ist sofort verfügbar
  - 📝 Neue Dokumentation erscheint automatisch live im Browser
  - ⚡ Schnellerer Start von `mkdocs serve`

- **Intelligente Code-Review:**
  - Automatische Identifikation von Schwachstellen (Security, Performance, Maintainability)
  - Konkrete Verbesserungsvorschläge mit Before/After-Code-Beispielen
  - Modern C++ Best Practices Analyse
  - Testing-Empfehlungen

- **Intelligentes Caching:**
  - SHA-256 File-Hash-Tracking
  - Inkrementelle Updates (nur geänderte Dateien werden neu dokumentiert)
  - Persistente Cache-Speicherung

- **Mehrere LLM-Provider:**
  - Anthropic Claude (empfohlen)
  - OpenAI GPT-4
  - Ollama (lokale Modelle)
  - LM Studio (lokale OpenAI-kompatible Modelle)

- **Cross-References:**
  - Automatische Links zwischen Dokumentationsebenen
  - Modul-zu-Klasse-Verlinkungen
  - Klassen-Beziehungen

- **C++ Code-Parsing:**
  - Tree-sitter-basiertes Parsing für höchste Genauigkeit
  - Regex-Fallback für Kompatibilität
  - Unterstützt Klassen, Funktionen, Templates

## Installation

```bash
cd plugins/mkdocs-llm-autodoc
pip install -e .
```

### Abhängigkeiten

```bash
pip install mkdocs>=1.4.0
pip install anthropic>=0.18.0  # Für Claude
pip install openai>=1.0.0      # Für OpenAI oder Ollama
pip install tree-sitter>=0.21.0
pip install tree-sitter-cpp>=0.21.0
```

## Konfiguration

Füge das Plugin zu deiner `mkdocs.yml` hinzu:

```yaml
plugins:
  - llm-autodoc:
      # Required
      enabled: true
      cpp_project_path: '../path/to/your/cpp/project'

      # LLM Configuration
      llm_provider: 'anthropic'  # oder 'openai', 'ollama', 'lmstudio'
      llm_api_key: !ENV ANTHROPIC_API_KEY  # oder direkt den Key
      llm_model: 'claude-3-5-sonnet-20241022'
      # llm_base_url: 'http://localhost:11434/v1'  # Für Ollama
      # llm_base_url: 'http://localhost:1234/v1'   # Für LM Studio

      # Documentation Levels
      generate_high_level: true
      generate_mid_level: true
      generate_detailed_level: true

      # Output Paths (relativ zu docs/)
      high_level_output: 'generated'
      mid_level_output: 'generated/modules'
      detailed_level_output: 'generated/api'

      # Caching
      enable_cache: true
      cache_dir: '.cache/llm-autodoc'
      force_regenerate: false

      # Quality Control
      enable_quality_check: true
      enable_cross_references: true
      enable_code_review: true        # Enable automated code review & improvement suggestions

      # File Patterns
      include_patterns:
        - '**/*.h'
        - '**/*.hpp'
        - '**/*.cpp'
      exclude_patterns:        # Recursively exclude paths matching these patterns
        - '**/build/**'        # Exclude build directories at any level
        - '**/third_party/**'  # Exclude third_party directories
        - '**/external/**'     # Exclude external dependencies
        - '**/.git/**'         # Exclude git directory
        - '**/__pycache__/**'  # Exclude Python cache
        - '**/*.pyc'           # Exclude Python compiled files
        - '**/.cache/**'       # Exclude cache directories
        - '**/node_modules/**' # Exclude Node.js modules

      # Advanced
      max_concurrent_llm_calls: 3
      retry_failed: true
      verbose: false

      # Background Processing (NEU!)
      background_generation: true      # Generierung läuft im Hintergrund
      show_generation_progress: true   # Fortschrittsbalken anzeigen
```

### Umgebungsvariablen

Statt API-Keys direkt in der Konfiguration anzugeben, verwende Umgebungsvariablen:

```bash
# Für Anthropic Claude
export ANTHROPIC_API_KEY="your-api-key"

# Für OpenAI
export OPENAI_API_KEY="your-api-key"
```

## Verwendung

### Live-Entwicklung mit `mkdocs serve`

Mit aktivierter Background-Generierung kannst du sofort mit der Entwicklung beginnen:

```bash
mkdocs serve
```

**Wie es funktioniert:**

1. **Sofortiger Start**: MkDocs startet sofort, ohne auf die Dokumentationsgenerierung zu warten
2. **Bereits vorhandene Docs**: Alle bereits generierten Dokumentationsdateien sind sofort verfügbar
3. **Live-Updates**: Neue Dokumentation erscheint automatisch im Browser, sobald sie generiert wurde
4. **Hintergrund-Prozess**: Die Generierung läuft parallel im Hintergrund

**Output-Beispiel:**
```
INFO    - Starting LLM-powered documentation generation...
INFO    - 📚 Found 42 existing documentation files - they will be available immediately
INFO    - 🚀 Starting background documentation generation...
INFO    - 📝 New documentation will appear automatically as it's generated
INFO    - [mkdocs] Serving on http://127.0.0.1:8000/
...
INFO    - ✓ Generated 3 high-level documentation files
INFO    - 📦 Generating Module Docs: 100%|████████| 5/5 [00:30<00:00]
INFO    - ✓ Generated 5 module documentation files
INFO    - 📄 Generating API Docs: 100%|████████| 23/23 [02:15<00:00]
INFO    - ✅ Documentation generation complete! Generated 31 files
```

**Vorteile:**
- ✅ Keine Wartezeit beim Start
- ✅ Bereits generierte Dokumentation ist sofort verfügbar
- ✅ Neue Teile erscheinen automatisch ohne Browser-Refresh (dank MkDocs Live-Reload)
- ✅ Produktiver arbeiten während die Dokumentation im Hintergrund generiert wird

### Vollständige Dokumentation generieren

```bash
mkdocs build
```

Das Plugin wird automatisch während des Build-Prozesses ausgeführt und generiert die Dokumentation.

### Nur bei Änderungen neu generieren

Standardmäßig generiert das Plugin nur Dokumentation für geänderte Dateien. Um alles neu zu generieren:

```yaml
plugins:
  - llm-autodoc:
      force_regenerate: true
```

### Cache löschen

```bash
rm -rf .cache/llm-autodoc
```

### Dateien einschließen/ausschließen

Das Plugin unterstützt flexible Glob-Patterns zum Ein- und Ausschließen von Dateien.

#### Include Patterns

Definiere, welche Dateien dokumentiert werden sollen:

```yaml
include_patterns:
  - '**/*.h'      # Alle .h Header-Dateien
  - '**/*.hpp'    # Alle .hpp Header-Dateien
  - '**/*.cpp'    # Alle .cpp Implementierungen
  - '**/*.cc'     # Alternative .cc Dateien
  - 'src/**/*'    # Nur Dateien im src-Verzeichnis
```

#### Exclude Patterns (Rekursiv)

Das Plugin unterstützt rekursive Ausschluss-Patterns, die auf alle Ebenen der Verzeichnisstruktur angewendet werden:

```yaml
exclude_patterns:
  # Verzeichnisse rekursiv ausschließen
  - '**/build/**'        # Alle build-Verzeichnisse und deren Inhalte
  - '**/third_party/**'  # Alle Drittanbieter-Bibliotheken
  - '**/external/**'     # Externe Dependencies
  - '**/vendor/**'       # Vendor-Verzeichnisse
  - '**/.git/**'         # Git-Verzeichnisse
  - '**/__pycache__/**'  # Python-Cache
  - '**/.cache/**'       # Cache-Verzeichnisse
  - '**/node_modules/**' # Node.js-Module
  - '**/test/**'         # Test-Verzeichnisse
  - '**/tests/**'        # Alternative Test-Verzeichnisse

  # Dateien nach Pattern ausschließen
  - '**/*.pyc'           # Python-Compiled-Dateien
  - '**/*.o'             # Object-Dateien
  - '**/*.a'             # Static Libraries
  - '**/*.so'            # Shared Libraries
  - '**/*_test.cpp'      # Test-Dateien mit bestimmtem Suffix
```

#### Wie Exclusion Patterns funktionieren

Die Exclude Patterns werden rekursiv auf alle Pfade angewendet:

- **`**/build/**`**: Schließt das `build`-Verzeichnis aus, egal wo es sich befindet
  - ✅ Schließt aus: `build/main.o`, `foo/build/lib.a`, `src/build/Debug/app.exe`

- **`**/*.pyc`**: Schließt alle `.pyc`-Dateien rekursiv aus
  - ✅ Schließt aus: `__pycache__/module.pyc`, `src/utils/cache.pyc`

- **`**/test/**`**: Schließt alle `test`-Verzeichnisse und deren Inhalte aus
  - ✅ Schließt aus: `test/unit.cpp`, `src/test/integration.cpp`

#### Beispielkonfiguration für große Projekte

```yaml
include_patterns:
  - 'src/**/*.h'
  - 'src/**/*.hpp'
  - 'src/**/*.cpp'
  - 'include/**/*.h'

exclude_patterns:
  # Build-Artefakte
  - '**/build/**'
  - '**/cmake-build-*/**'
  - '**/out/**'
  - '**/*.o'
  - '**/*.a'
  - '**/*.so'
  - '**/*.dll'

  # Tests
  - '**/test/**'
  - '**/tests/**'
  - '**/*_test.cpp'
  - '**/*_unittest.cpp'

  # Dependencies
  - '**/third_party/**'
  - '**/external/**'
  - '**/vendor/**'
  - '**/deps/**'

  # Version Control & System
  - '**/.git/**'
  - '**/.svn/**'
  - '**/.hg/**'

  # IDE & Editor
  - '**/.vscode/**'
  - '**/.idea/**'
  - '**/*.swp'

  # Cache & Temp
  - '**/.cache/**'
  - '**/tmp/**'
  - '**/temp/**'
```

## Generierte Struktur

```
docs/
├── generated/
│   ├── 00-getting-started.md     # High-Level: Projekt-Übersicht
│   ├── 01-architecture.md        # High-Level: Architektur
│   ├── modules/
│   │   ├── core.md              # Mid-Level: Core-Modul
│   │   ├── networking.md        # Mid-Level: Networking-Modul
│   │   └── utils.md             # Mid-Level: Utils-Modul
│   └── api/
│       ├── classes/             # Detailed-Level: Klassen
│       │   ├── parser.md
│       │   ├── lexer.md
│       │   └── executor.md
│       └── functions/           # Detailed-Level: Funktionen
│           ├── helpers.md
│           └── utilities.md
```

## Beispiele

### High-Level Dokumentation

Das Plugin erstellt eine umfassende Projekt-Übersicht:

```markdown
# Getting Started

## Project Overview
This C++ project implements a high-performance data processing pipeline...

## Core Architecture
- **Parser Module**: Handles input parsing and validation
- **Executor Module**: Executes data transformations
- **Output Module**: Manages result serialization

## Technology Stack
- C++17
- CMake build system
- Google Test framework

[Mermaid-Diagramm der Architektur]
```

### Mid-Level Dokumentation

Für jedes Modul:

```markdown
# Core Module

## Overview
The Core module provides fundamental data structures and algorithms...

## Main Classes
- **DataProcessor**: Central processing engine
- **Validator**: Input validation logic
- **Cache**: High-performance caching layer

## Dependencies
- Standard Library
- Boost 1.75+

[Mermaid-Diagramm der Klassen-Beziehungen]
```

### Detailed-Level Dokumentation

Für jede Klasse:

```markdown
# DataProcessor Class

## Overview
The DataProcessor class handles high-throughput data transformation...

## Constructor
**Signature**: `DataProcessor(const Config& config)`
**Parameters**:
- `config` (const Config&): Configuration object
**Example**:
```cpp
Config cfg;
cfg.maxThreads = 4;
DataProcessor processor(cfg);
```

## Methods

### process()
**Signature**: `Result process(const Data& input)`
**Description**: Processes input data and returns result
**Parameters**:
- `input` (const Data&): Input data to process
**Return Value**: Result object with processed data
**Exceptions**: May throw ProcessingError on invalid input
...

## Code Review & Improvement Suggestions

### Potential Issues

**Issue**: Missing bounds checking in array access
**Severity**: High
**Location**: `processData()` method
**Impact**: Could lead to buffer overflow and crash
**Recommendation**: Add bounds validation:
```cpp
if (index >= 0 && index < data.size()) {
    // Safe access
}
```

**Issue**: Unnecessary copy in loop
**Severity**: Medium
**Location**: `processItems()` method
**Impact**: Performance degradation with large containers
**Recommendation**: Use const reference:
```cpp
// Before
for (auto item : items) { ... }

// After
for (const auto& item : items) { ... }
```

### Improvement Suggestions

**Modern C++ Features:**
- Replace raw pointers with `std::unique_ptr` in `allocateBuffer()`
- Use `[[nodiscard]]` attribute for `validate()` method
- Add `noexcept` to move operations

**Performance Optimizations:**
- Reserve vector capacity in `loadData()`
- Use `string_view` for read-only string parameters
- Consider move semantics for `setConfiguration()`

### Testing Recommendations
- Test with empty input containers
- Test concurrent access from multiple threads
- Verify exception handling with invalid inputs
```

## LLM-Provider

### Anthropic Claude (Empfohlen)

```yaml
llm_provider: 'anthropic'
llm_model: 'claude-3-5-sonnet-20241022'
llm_api_key: !ENV ANTHROPIC_API_KEY
```

Vorteile:
- Ausgezeichnete Code-Verständnis
- Präzise technische Dokumentation
- Lange Kontextfenster

### OpenAI GPT-4

```yaml
llm_provider: 'openai'
llm_model: 'gpt-4'
llm_api_key: !ENV OPENAI_API_KEY
```

### Ollama (Lokal)

```yaml
llm_provider: 'ollama'
llm_model: 'llama3'
llm_base_url: 'http://localhost:11434/v1'
```

Vorteile:
- Keine API-Kosten
- Volle Datenkontrolle
- Offline-Nutzung

### LM Studio (Lokal)

```yaml
llm_provider: 'lmstudio'
llm_model: 'local-model'  # Der Name des geladenen Modells in LM Studio
llm_base_url: 'http://localhost:1234/v1'
```

Vorteile:
- Keine API-Kosten
- Benutzerfreundliche GUI
- Unterstützt viele Modellformate (GGUF, etc.)
- Volle Datenkontrolle
- Offline-Nutzung

**Installation:**
1. LM Studio von [lmstudio.ai](https://lmstudio.ai) herunterladen
2. Modell herunterladen (z.B. CodeLlama, DeepSeek Coder, Mistral)
3. Server starten (im LM Studio: Developer → Start Server)
4. Modellnamen aus LM Studio kopieren und in `llm_model` eintragen

## Background-Generierung (NEU!)

Die Background-Generierung ist eine neue Funktion, die es ermöglicht, die Dokumentationsgenerierung im Hintergrund auszuführen, während MkDocs bereits läuft.

### Aktivierung

```yaml
plugins:
  - llm-autodoc:
      background_generation: true      # Aktiviert Hintergrund-Generierung
      show_generation_progress: true   # Zeigt Fortschrittsbalken
```

### Funktionsweise

1. **Beim Start von `mkdocs serve` oder `mkdocs build`:**
   - Das Plugin prüft, ob bereits generierte Dokumentation existiert
   - Diese wird sofort verfügbar gemacht
   - Ein Background-Thread startet die Generierung neuer/geänderter Dateien

2. **Während der Generierung:**
   - Jede neu generierte Datei wird sofort auf die Festplatte geschrieben
   - MkDocs' Live-Reload erkennt die neue Datei automatisch
   - Der Browser aktualisiert sich automatisch und zeigt die neue Dokumentation

3. **Thread-Safety:**
   - Alle Schreiboperationen sind thread-safe
   - Der Background-Thread arbeitet unabhängig vom MkDocs-Prozess
   - Keine Blockierung des Build-Prozesses

### Synchrone Generierung (klassisch)

Wenn du die alte Funktionsweise bevorzugst (Build wartet auf Generierung):

```yaml
plugins:
  - llm-autodoc:
      background_generation: false  # Deaktiviert Hintergrund-Generierung
```

### Status-Informationen

Das Plugin gibt detaillierte Status-Meldungen aus:

- **📚** Gefundene existierende Dateien
- **🚀** Background-Generierung gestartet
- **📝** Live-Updates aktiviert
- **✓** Ebene abgeschlossen
- **📦** Modul-Generierung läuft
- **📄** API-Generierung läuft
- **✅** Generierung komplett abgeschlossen

## Performance-Optimierung

### Caching

Das Plugin cached generierte Dokumentation und regeneriert nur bei Dateiänderungen:

```python
# .cache/llm-autodoc/file_hashes.json
{
  "src/core/parser.cpp": "a1b2c3d4...",
  "src/core/executor.cpp": "e5f6g7h8..."
}
```

### Parallele LLM-Aufrufe

```yaml
max_concurrent_llm_calls: 3  # Anzahl paralleler LLM-Anfragen
```

### Selective Generation

Generiere nur bestimmte Ebenen:

```yaml
generate_high_level: true
generate_mid_level: true
generate_detailed_level: false  # Detaillierte API-Docs überspringen
```

## Troubleshooting

### Tree-sitter nicht verfügbar

Falls tree-sitter nicht funktioniert, fällt das Plugin automatisch auf Regex-Parsing zurück:

```
WARNING: Tree-sitter not available, using fallback regex parser
```

Installation von tree-sitter:

```bash
pip install tree-sitter tree-sitter-cpp
```

### LLM API-Fehler

Bei Rate-Limits oder API-Fehlern:

```yaml
retry_failed: true
max_concurrent_llm_calls: 1  # Reduzieren für Rate-Limits
```

### Cache-Probleme

Cache löschen und neu generieren:

```bash
rm -rf .cache/llm-autodoc
mkdocs build
```

## Entwicklung

### Lokale Installation für Entwicklung

```bash
cd plugins/mkdocs-llm-autodoc
pip install -e .[dev]
```

### Tests ausführen

```bash
pytest tests/
```

## Lizenz

MIT

## Credits

Entwickelt für intelligente C++-Dokumentation mit MkDocs und LLMs.

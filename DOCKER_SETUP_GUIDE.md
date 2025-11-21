# Docker Setup Guide - MkDocs mit RAG & Auto-Chunking

## 🚀 Quick Start

```bash
# 1. Clone/Setup project
cd /path/to/your/mkdocs/project

# 2. Configure environment
cp .env.example .env
# Edit .env: Set SOURCE_CODE_PATH to your C++ project

# 3. Start all services
docker-compose up -d

# 4. Access documentation
# → http://localhost:8000 (MkDocs)
# → http://localhost:9001 (MinIO Console)
# → http://localhost:6333/dashboard (Qdrant Dashboard)
```

---

## 📋 Inhaltsverzeichnis

1. [Voraussetzungen](#voraussetzungen)
2. [Installation](#installation)
3. [Konfiguration](#konfiguration)
4. [Services](#services)
5. [Automatisches RAG Upload](#automatisches-rag-upload)
6. [Exclusion Marker](#exclusion-marker)
7. [Troubleshooting](#troubleshooting)

---

## Voraussetzungen

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **LM Studio** (oder Anthropic/OpenAI API Key)
- **Source Code Verzeichnis** (dein C++ Projekt)

---

## Installation

### Schritt 1: Environment konfigurieren

```bash
# .env Datei erstellen
cp .env.example .env
```

**Wichtige Einstellungen in `.env`:**

```env
# Pfad zu deinem Quellcode
SOURCE_CODE_PATH=../your-cpp-project/src

# LLM Provider
LLM_PROVIDER=lmstudio
LLM_BASE_URL=http://host.docker.internal:1234/v1
```

### Schritt 2: Docker Services starten

```bash
# Alle Services im Hintergrund starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f

# Nur bestimmte Services anzeigen
docker-compose logs -f mkdocs
docker-compose logs -f qdrant
docker-compose logs -f minio
```

### Schritt 3: Health Check

```bash
# Alle Services überprüfen
docker-compose ps

# Sollte zeigen:
# mkdocs-builder    running
# mkdocs-qdrant     healthy
# mkdocs-minio      healthy
```

---

## Konfiguration

### Source Code Mount

Das Quellcode-Verzeichnis wird read-only gemountet:

```yaml
volumes:
  - ${SOURCE_CODE_PATH:-./src}:/workspace/source_code:ro
```

**Pfad ändern:**

1. In `.env` Datei:
   ```env
   SOURCE_CODE_PATH=/absolute/path/to/cpp/project
   ```

2. Oder direkt beim Start:
   ```bash
   SOURCE_CODE_PATH=../my-project docker-compose up -d
   ```

### LLM Provider konfigurieren

#### Option 1: LM Studio (Empfohlen für lokal)

1. **LM Studio starten** auf Host-Machine
2. **Modell laden** (z.B. Llama 3, Mistral)
3. **Server starten** auf Port 1234
4. In `.env`:
   ```env
   LLM_PROVIDER=lmstudio
   LLM_BASE_URL=http://host.docker.internal:1234/v1
   ```

#### Option 2: Anthropic Claude

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-api-key-here
```

#### Option 3: OpenAI

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key-here
```

---

## Services

### 1. MkDocs Builder (Port 8000)

**Funktion:** Dokumentations-Generator mit Chatbot

**URLs:**
- Documentation: http://localhost:8000
- Chatbot API: http://localhost:8765

**Volumes:**
- `/workspace` - Projekt-Root
- `/workspace/source_code` - Dein Quellcode (read-only)
- Pip Cache (persistent)
- Sentence Transformers Cache (persistent)

**Logs:**
```bash
docker-compose logs -f mkdocs
```

### 2. Qdrant (Port 6333)

**Funktion:** Vector Database für RAG

**URLs:**
- API: http://localhost:6333
- Dashboard: http://localhost:6333/dashboard

**Persistent:** Volume `qdrant_storage`

**Collection Info:**
```bash
# Collection Status anzeigen
curl http://localhost:6333/collections/mkdocs_documentation
```

### 3. MinIO (Port 9000, 9001)

**Funktion:** S3-kompatible Object Storage

**URLs:**
- API: http://localhost:9000
- Console: http://localhost:9001

**Login:**
- Username: `admin`
- Password: `password123`

**Buckets:**
- `mkdocs-documentation` - Generated docs
- `mkdocs-source` - Source files
- `mkdocs-generated` - Generated files

**Persistent:** Volume `minio_data`

---

## Automatisches RAG Upload

### Funktionsweise

Beim Build werden **automatisch** alle Dateien ins RAG hochgeladen:

1. **Source Code** - Alle `.cpp`, `.h`, `.py` Dateien
2. **Dokumentation** - Alle `.md` Dateien
3. **Generated Docs** - Generierte Dokumentation

### Intelligentes Chunking

**Python Code:**
```python
class Example:
    def method1(self):  # → Chunk 1
        pass

    def method2(self):  # → Chunk 2
        pass
```
↓
Jede Methode wird ein separater Chunk mit Metadata

**Markdown:**
```markdown
# Heading 1  # → Chunk 1 (mit allen Unterabschnitten)

## Heading 2  # → Chunk 2
```
↓
Nach Sections gechunked

**C++:**
```cpp
class MyClass {  // → Chunk 1 (ganze Klasse)
    void method1();
    void method2();
};

void globalFunc() {  // → Chunk 2 (separate Funktion)
}
```

### Chunk Metadata

Jeder Chunk enthält:
```json
{
  "content": "...",
  "metadata": {
    "file_path": "src/main.cpp",
    "file_name": "main.cpp",
    "file_type": "cpp",
    "chunk_index": 0,
    "total_chunks": 5,
    "type": "function",
    "name": "myFunction",
    "category": "source"
  }
}
```

---

## Exclusion Marker

### Verzeichnisse ausschließen

Erstelle `.exclude_from_docu` Datei in jedem Verzeichnis, das ausgeschlossen werden soll:

```bash
# Beispiel Projektstruktur
src/
├── main.cpp              # ✅ Wird dokumentiert
├── utils/
│   └── helper.cpp        # ✅ Wird dokumentiert
├── third_party/
│   ├── .exclude_from_docu  # ❌ Marker-Datei
│   └── library.cpp       # ❌ Wird ausgeschlossen
└── build/
    ├── .exclude_from_docu  # ❌ Marker-Datei
    └── output.o          # ❌ Wird ausgeschlossen
```

### Marker erstellen

**Manuell:**
```bash
cd src/third_party
echo "# Excluded from documentation" > .exclude_from_docu
```

**Automatisch (in Python):**
```python
from mkdocs_llm_autodoc.utils.exclusion_checker import ExclusionChecker

checker = ExclusionChecker(project_root)
checker.create_exclusion_marker(
    "src/third_party",
    reason="Third-party library, not our code"
)
```

### Marker entfernen

```bash
rm src/third_party/.exclude_from_docu
```

oder:

```python
checker.remove_exclusion_marker("src/third_party")
```

---

## mkdocs.yml Konfiguration

### Minimale Konfiguration

```yaml
plugins:
  - llm-autodoc:
      enabled: true
      cpp_project_path: /workspace/source_code
      llm_provider: lmstudio
      llm_base_url: http://host.docker.internal:1234/v1

      # RAG Upload aktivieren
      enable_rag_upload: true
      rag_webhook_url: http://qdrant:6333  # Oder custom endpoint

  - chatbot:
      enabled: true
      enable_rag: true
      rag_config:
        type: qdrant
        url: http://qdrant:6333
        collection_name: mkdocs_documentation
```

### Vollständige Konfiguration

Siehe `mkdocs_example_full_features.yaml`

---

## Troubleshooting

### Problem: MkDocs findet Quellcode nicht

**Lösung:**
```bash
# 1. Prüfe SOURCE_CODE_PATH in .env
cat .env | grep SOURCE_CODE_PATH

# 2. Prüfe Mount im Container
docker exec mkdocs-builder ls -la /workspace/source_code

# 3. Absolute Pfade verwenden
SOURCE_CODE_PATH=/absolute/path/to/src
```

### Problem: Qdrant nicht erreichbar

**Lösung:**
```bash
# 1. Service Status prüfen
docker-compose ps qdrant

# 2. Logs anzeigen
docker-compose logs qdrant

# 3. Health Check
curl http://localhost:6333/health

# 4. Neu starten
docker-compose restart qdrant
```

### Problem: MinIO Buckets nicht erstellt

**Lösung:**
```bash
# 1. Init Container Logs prüfen
docker-compose logs minio-init

# 2. Manuell erstellen
docker exec mkdocs-minio-init mc mb myminio/mkdocs-documentation

# 3. Buckets auflisten
docker exec mkdocs-minio mc ls myminio
```

### Problem: RAG Upload funktioniert nicht

**Lösung:**
```bash
# 1. Prüfe Qdrant Collection
curl http://localhost:6333/collections/mkdocs_documentation

# 2. Prüfe MkDocs Logs
docker-compose logs mkdocs | grep RAG

# 3. Manuell testen
docker exec -it mkdocs-builder python
>>> from mkdocs_chatbot.rag_manager import RAGManager
>>> rag = RAGManager({'type': 'qdrant', 'url': 'http://qdrant:6333'})
>>> rag.is_available()
```

### Problem: LM Studio nicht erreichbar von Docker

**Lösung:**
```bash
# 1. LM Studio läuft?
curl http://localhost:1234/v1/models

# 2. Docker Host erreichen?
docker exec mkdocs-builder curl http://host.docker.internal:1234/v1/models

# 3. Firewall?
# Windows: Firewall-Regel für LM Studio erlauben
# Linux: ufw allow 1234

# 4. Alternative: Host-Netzwerk (Linux only)
# In docker-compose.yml:
# network_mode: "host"
```

### Problem: Services zu langsam

**Lösung:**
```bash
# 1. Mehr RAM für Docker
# Docker Desktop → Settings → Resources → Memory: 8GB+

# 2. Caches löschen
docker-compose down -v  # Löscht auch Volumes!
docker-compose up -d

# 3. Weniger parallele LLM Calls
# In mkdocs.yml:
# max_concurrent_llm_calls: 1
```

---

## Nützliche Befehle

### Services verwalten

```bash
# Alle Services starten
docker-compose up -d

# Logs anzeigen (alle)
docker-compose logs -f

# Logs anzeigen (nur MkDocs)
docker-compose logs -f mkdocs

# Services neu starten
docker-compose restart

# Services stoppen
docker-compose stop

# Services stoppen und löschen
docker-compose down

# Services + Volumes löschen (ACHTUNG: Datenverlust!)
docker-compose down -v
```

### RAG Management

```bash
# Collection Info
curl http://localhost:6333/collections/mkdocs_documentation

# Alle Collections auflisten
curl http://localhost:6333/collections

# Collection löschen (neu indexieren)
curl -X DELETE http://localhost:6333/collections/mkdocs_documentation

# Collection neu erstellen (erfolgt automatisch beim nächsten Upload)
```

### MinIO Management

```bash
# Buckets auflisten
docker exec mkdocs-minio mc ls myminio

# Dateien auflisten
docker exec mkdocs-minio mc ls myminio/mkdocs-documentation

# Datei herunterladen
docker exec mkdocs-minio mc cp myminio/mkdocs-documentation/file.md ./
```

### Debugging

```bash
# In Container einsteigen
docker exec -it mkdocs-builder bash

# Python Shell im Container
docker exec -it mkdocs-builder python

# Ports prüfen
docker-compose ps

# Netzwerk prüfen
docker network inspect mkdocs-network
```

---

## Performance Optimierung

### 1. Build Cache nutzen

Die Docker Volumes cachen:
- Pip Packages
- Sentence Transformers Models

**Beim ersten Build:** Langsam (~5-10 Min Downloads)
**Nachfolgende Builds:** Schnell (~30 Sek)

### 2. Parallele Verarbeitung

```yaml
# mkdocs.yml
plugins:
  - llm-autodoc:
      max_concurrent_llm_calls: 5  # Mehr parallel
```

⚠️ **Achtung:** LM Studio kann überlastet werden!

### 3. Selektive Dokumentation

```yaml
# Nur wichtige Verzeichnisse
include_patterns:
  - 'src/core/**/*.cpp'
  - 'src/api/**/*.h'

exclude_patterns:
  - '**/test/**'
  - '**/third_party/**'
```

---

## Backup & Restore

### Qdrant Backup

```bash
# Backup erstellen
docker exec mkdocs-qdrant tar czf /tmp/qdrant-backup.tar.gz /qdrant/storage
docker cp mkdocs-qdrant:/tmp/qdrant-backup.tar.gz ./

# Restore
docker cp qdrant-backup.tar.gz mkdocs-qdrant:/tmp/
docker exec mkdocs-qdrant tar xzf /tmp/qdrant-backup.tar.gz -C /
docker-compose restart qdrant
```

### MinIO Backup

```bash
# Alle Buckets sichern
docker exec mkdocs-minio mc mirror myminio/mkdocs-documentation ./minio-backup/

# Restore
docker exec mkdocs-minio mc mirror ./minio-backup/ myminio/mkdocs-documentation
```

---

## Weiterführende Links

- **Qdrant Docs:** https://qdrant.tech/documentation/
- **MinIO Docs:** https://min.io/docs/minio/linux/index.html
- **Docker Compose:** https://docs.docker.com/compose/
- **LM Studio:** https://lmstudio.ai/

---

## Support

Bei Problemen:
1. Logs prüfen: `docker-compose logs`
2. Health Checks: `docker-compose ps`
3. Container neu starten: `docker-compose restart`
4. GitHub Issues: [Repository URL]

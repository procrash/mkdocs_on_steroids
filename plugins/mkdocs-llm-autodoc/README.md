# MkDocs LLM AutoDoc Plugin

**Intelligente, KI-gestützte Dokumentationsgenerierung für Codebases**

Automatisches Erstellen von mehrstufiger, thematischer Dokumentation mit LLM-Power. Von High-Level Architektur-Übersichten bis zu detaillierten API-Dokumentationen - alles automatisch, nachvollziehbar und immer aktuell.

---

## 🌟 Features im Überblick

### 📚 Multi-Level Dokumentation

1. **High-Level Thematic Overview** (40+ Topics)
   - Projekt-Übersicht, Getting Started, Architektur
   - CI/CD, Testing, Security, Performance
   - Threading, Memory Management, Error Handling
   - Und 30+ weitere Entwickler-relevante Themen

2. **Module Documentation**
   - Übersicht über einzelne Module
   - Klassen-Zusammenhänge
   - Design Patterns

3. **Detailed API Documentation**
   - Vollständige Klassen-Dokumentation
   - Method-Signaturen und Parameter
   - Code-Reviews und Verbesserungsvorschläge
   - Beispiele und Best Practices

### 🔗 Intelligente Features

4. **Hybrid-Analyse** (Source + Docs)
   - Analysiert SOWOHL Source Code ALS AUCH bereits generierte Docs
   - Kombiniert Implementation-Details mit strukturierten Insights
   - Maximale Informationsdichte

5. **Code-Referenzen** (Nachvollziehbarkeit)
   - Jede Aussage ist mit `[Code](file.cpp:123)` referenziert
   - Vollständige Traceability
   - Leicht wartbar

6. **Cross-Linking** (Automatische Verlinkung)
   - Erkennt thematische Ähnlichkeiten zwischen Docs
   - Fügt "See Also" Sektionen automatisch ein
   - Bidirektionale Links

7. **Auto-Navigation** (mkdocs.yml Update)
   - Aktualisiert mkdocs.yml automatisch
   - Intelligentes Merging mit bestehenden Einträgen
   - Hierarchische Strukturierung

8. **Dependency Analysis**
   - Include-Graphen und Circular Dependencies
   - Hub Files Identifikation
   - Mermaid Diagramme

9. **Resumable Generation** (State Management)
   - Kann jederzeit unterbrochen und fortgesetzt werden
   - Keine doppelte Arbeit
   - Change Detection

### 🚀 Workflow-Optimierung

10. **Parallel Processing**
    - Multi-threaded LLM calls
    - Konfigurierbare Worker-Anzahl
    - Schnelle Generation

11. **Smart Caching**
    - File-Hash basiertes Caching
    - Nur geänderte Files werden neu generiert
    - Kosteneinsparung

12. **RAG Integration**
    - Upload zu RAG-Systemen
    - Source Files + Dokumentation
    - Webhook-basiert

---

## 🎯 Der 7-Phasen Prozess

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: TOPIC EXTRACTION (Hybrid: Source + Docs)              │
│ Analysiert jede Datei für jeden der 40+ Topics                 │
│ Nutzt Source Code UND bereits generierte Markdown-Docs         │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: TOPIC SYNTHESIS                                        │
│ Kombiniert Extractions zu kohärenten Topic-Dokumenten          │
│ Mit Code-Referenzen für jede Aussage                           │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: TOPIC REFINEMENT                                       │
│ Strukturiert, entfernt Duplikate, verbessert Qualität          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: DEPENDENCY ANALYSIS                                    │
│ Include-Graphen, Circular Dependencies, Mermaid Diagramme      │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 5: INDEX GENERATION                                       │
│ Master-Index mit Navigation nach Priorität                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 6: CROSS-LINKING                                          │
│ Automatische "See Also" Links zwischen verwandten Docs         │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 7: NAVIGATION UPDATE                                      │
│ Aktualisiert mkdocs.yml automatisch mit generierten Docs       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

```bash
pip install -e plugins/mkdocs-llm-autodoc/
```

---

## ⚙️ Konfiguration

### Minimal-Konfiguration

```yaml
plugins:
  - llm-autodoc:
      enabled: true
      cpp_project_path: './cpp-project'

      # LLM Konfiguration
      llm_provider: 'anthropic'
      llm_api_key: '${ANTHROPIC_API_KEY}'

      # Alle Features aktivieren
      generate_overview: true
      generate_high_level: true
      generate_mid_level: true
      generate_detailed_level: true
```

Weitere Konfigurationsbeispiele siehe [CONFIG_EXAMPLE.yml](CONFIG_EXAMPLE.yml).

---

## 🚀 Verwendung

```bash
mkdocs build
```

Das war's! Das Plugin generiert automatisch:
- ✅ 40+ thematische Übersichts-Dokumente
- ✅ Modul-Dokumentationen
- ✅ API-Referenz-Dokumentationen
- ✅ Cross-Links zwischen verwandten Docs
- ✅ Aktualisierte mkdocs.yml Navigation

---

## 📂 Output-Struktur

```
docs/generated/
├── 00-overview-index.md          # Master Index
├── overview/                      # 40+ Thematische Topics
│   ├── project-overview.md
│   ├── getting-started.md
│   ├── architecture.md
│   ├── ci-cd.md                  # CI/CD Pipeline
│   ├── testing.md
│   ├── security.md
│   ├── performance.md
│   ├── threading.md
│   ├── dependencies-graph.md     # Dependency Analysis
│   └── ... (30+ weitere)
├── modules/                       # Module Docs
│   ├── core.md
│   └── ...
└── api/                           # API Docs
    ├── classes/
    │   └── threadpool.md
    └── functions/
        └── utils.md

mkdocs.yml  # Automatisch aktualisiert! ✅
```

---

## 💡 Key Features im Detail

### 1. Hybrid-Analyse (Source + Docs)

Das System analysiert **BEIDE**:
- **Source Code**: Implementation-Details, Patterns
- **Generierte Docs**: Strukturierte Insights, Code-Reviews

```
threading.cpp + threading.md → Comprehensive threading.md (Overview)
```

### 2. Code-Referenzen (Traceability)

**Jede Aussage ist nachvollziehbar:**

```markdown
"Thread pool is initialized in `[ThreadPool::init](threadpool.cpp:45-78)`"
```

### 3. Cross-Linking (Automatic)

**Automatische "See Also" Sektionen:**

```markdown
## See Also

Related documentation:
- **[Memory Management](memory-management.md)** - Related classes: ThreadPool
- **[Performance](performance.md)** - Thread pool tuning
```

### 4. Auto-Navigation

**mkdocs.yml wird automatisch aktualisiert:**

```yaml
nav:
  - Home: index.md
  - Generated Documentation:  # ← Automatisch!
      - Overview:
          - Project Overview: generated/overview/project-overview.md
          - CI/CD Pipeline: generated/overview/ci-cd.md
          - ...
```

---

## 🎓 Advanced Features

### Resumable Generation

```bash
# Unterbrechen mit Ctrl+C
mkdocs build
^C

# Später fortsetzen - keine doppelte Arbeit!
mkdocs build  # Setzt fort wo es aufgehört hat
```

### Smart Caching

```
Erste Ausführung: 150 Files → 45-60 min, ~$20
Zweite Ausführung: 3 geänderte Files → 5-10 min, ~$1
```

### Lokale LLMs (Kostenlos!)

```yaml
llm_provider: 'ollama'
llm_model: 'codellama'
```

---

## 📊 Performance & Kosten

| Metrik | Erste Ausführung | Inkrementell |
|--------|------------------|--------------|
| Zeit | 45-60 min | 5-10 min |
| LLM Calls | 6000-8000 | 120-200 |
| Kosten | $15-25 | $0.50-1.00 |

**Kostenoptimierung**: Siehe [CONFIG_EXAMPLE.yml](CONFIG_EXAMPLE.yml)

---

## 📚 Weitere Dokumentation

- **[OVERVIEW_FEATURE.md](OVERVIEW_FEATURE.md)** - High-Level Overview Details
- **[CROSS_LINKING_FEATURE.md](CROSS_LINKING_FEATURE.md)** - Cross-Linking Details
- **[CONFIG_EXAMPLE.yml](CONFIG_EXAMPLE.yml)** - Alle Konfigurations-Optionen
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technische Details

---

## 🆚 Vergleich

| Feature | Doxygen | Sphinx | **LLM AutoDoc** |
|---------|---------|--------|-----------------|
| Auto-Generation | ✅ | ✅ | ✅ |
| High-Level Docs | ❌ | ⚠️ Manual | ✅ Automatic |
| Thematische Docs | ❌ | ❌ | ✅ 40+ Topics |
| Code References | ⚠️ | ⚠️ | ✅ Comprehensive |
| Cross-Linking | ❌ | ⚠️ Manual | ✅ Automatic |
| Navigation Update | ❌ | ❌ | ✅ Automatic |
| Intelligence | ❌ Static | ❌ Static | ✅ LLM-Powered |

---

## 🚀 Quick Start

```bash
# 1. Installation
pip install -e plugins/mkdocs-llm-autodoc/

# 2. API Key
export ANTHROPIC_API_KEY=your-key

# 3. Konfiguration (mkdocs.yml)
plugins:
  - llm-autodoc:
      generate_overview: true
      llm_provider: 'anthropic'

# 4. Generieren
mkdocs build

# 5. Anschauen
mkdocs serve
```

**Fertig! 🎉**

---

## 🤝 Contributing

Contributions welcome! Siehe [GitHub](https://github.com/your-repo).

---

## 📄 Lizenz

Siehe [LICENSE](LICENSE).

---

*Generated with ❤️ by mkdocs-llm-autodoc*

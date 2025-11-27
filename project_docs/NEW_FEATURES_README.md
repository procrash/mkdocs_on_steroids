# MkDocs Advanced Features - Complete Guide

## Table of Contents

1. [Overview](#overview)
2. [New Features](#new-features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Features Deep Dive](#features-deep-dive)
6. [Usage Examples](#usage-examples)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This documentation system now includes powerful AI-driven features for generating and exploring C++ project documentation:

### Core Components

1. **LLM AutoDoc Plugin** - Automatically generates multi-level documentation
2. **Interactive ChatBot** - AI assistant with RAG integration
3. **Doxygen Importer** - Migrates legacy Doxygen documentation
4. **RAG Integration** - Vector search for relevant documentation
5. **MCP Tools** - Extensible tool system for custom integrations
6. **MinIO Storage** - Document and asset storage
7. **n8n Integration** - Workflow automation support

---

## New Features

### 1. RAG (Retrieval-Augmented Generation) Integration

The chatbot now uses vector search to find relevant documentation before answering questions.

**Supported Vector Databases:**
- ✅ **Qdrant** - Recommended for production
- ✅ **ChromaDB** - Easy local development
- ✅ **Pinecone** - Cloud-hosted solution
- ✅ **Weaviate** - Open-source with hybrid search
- ✅ **Custom** - Your own RAG endpoint

**Benefits:**
- More accurate answers based on actual documentation
- Source citations with relevance scores
- Handles large codebases efficiently

### 2. MCP Tools Integration

Extend the chatbot with custom tools via Model Context Protocol.

**Tool Types:**
- **HTTP** - Call external APIs
- **CLI** - Execute command-line tools
- **Python** - Run Python functions
- **MCP Server** - Connect to MCP-compatible servers

**Example Tools:**
- Search GitHub issues
- Run tests
- Analyze code complexity
- Query databases
- Execute workflows

### 3. Doxygen Legacy Import

Import existing Doxygen documentation with automatic freshness validation.

**Features:**
- Parse Doxygen XML output
- Validate against current codebase using LLM
- Merge into existing documentation
- Create new sections for unique content
- Freshness scores and warnings

### 4. MinIO Object Storage

Store and manage documentation assets in S3-compatible storage.

**Use Cases:**
- Store source files
- Archive generated documentation
- Manage attachments and images
- Generate presigned URLs for sharing

### 5. n8n Workflow Integration

Use n8n for complex LLM workflows instead of direct API calls.

**Benefits:**
- Visual workflow designer
- Multi-step processing
- Integration with 200+ services
- Custom business logic

---

## Installation

### Prerequisites

1. **Python 3.8+**
2. **LM Studio** (or Anthropic/OpenAI API)
3. **Docker** (for Qdrant, MinIO)

### Quick Start

```bash
# 1. Install Python dependencies
pip install -r REQUIREMENTS_FULL_FEATURES.txt

# 2. Start Qdrant (vector database)
docker run -p 6333:6333 qdrant/qdrant

# 3. Start MinIO (object storage)
docker run -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=password \
  minio/minio server /data --console-address ":9001"

# 4. Start LM Studio
# - Download from https://lmstudio.ai/
# - Load a model
# - Start local server on port 1234

# 5. Build documentation
mkdocs serve

# 6. Access at http://localhost:8000
```

### Using Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  mkdocs:
    image: python:3.11
    working_dir: /docs
    volumes:
      - .:/docs
    ports:
      - "8000:8000"
    command: >
      bash -c "pip install -r requirements.txt && mkdocs serve -a 0.0.0.0:8000"

  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"

  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: password
    command: server /data --console-address ":9001"

# Run with: docker-compose up
```

---

## Configuration

### Minimal Configuration

```yaml
# mkdocs.yml
plugins:
  - llm-autodoc:
      enabled: true
      cpp_project_path: ./src
      llm_provider: lmstudio
      llm_base_url: http://localhost:1234/v1

  - chatbot:
      enabled: true
      api_base_url: http://localhost:1234/v1
```

### Full Configuration

See `mkdocs_example_full_features.yaml` for complete configuration with all features enabled.

### Environment Variables

```bash
# .env file
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
GITHUB_TOKEN=your-token-here
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=password
N8N_API_KEY=your-key-here
```

---

## Features Deep Dive

### RAG Configuration

#### Qdrant (Recommended)

```yaml
enable_rag: true
rag_config:
  type: qdrant
  url: http://localhost:6333
  collection_name: mkdocs_documentation
  top_k: 5
  embedding_model: sentence-transformers/all-MiniLM-L6-v2
```

**Advantages:**
- Fast vector search
- Scales well
- Good documentation
- Cloud option available

#### ChromaDB (Easy Setup)

```yaml
enable_rag: true
rag_config:
  type: chromadb
  persist_directory: .cache/chromadb
  collection_name: mkdocs_documentation
  top_k: 5
```

**Advantages:**
- Zero configuration
- Perfect for local development
- No external dependencies

### MCP Tools Examples

#### HTTP Tool - GitHub Issues

```yaml
mcp_tools:
  - name: search_github_issues
    description: Search for related GitHub issues
    type: http
    endpoint: https://api.github.com/search/issues
    method: GET
    auth:
      type: bearer
      token: ${GITHUB_TOKEN}
    parameters:
      q:
        type: string
        description: Search query
        required: true
```

**Usage in Chat:**
> "Find GitHub issues related to memory leaks"

#### CLI Tool - Run Tests

```yaml
mcp_tools:
  - name: run_tests
    description: Run unit tests
    type: cli
    command: pytest tests/{module}_test.py -v
    parameters:
      module:
        type: string
        description: Module name
        required: true
```

**Usage in Chat:**
> "Run tests for the parser module"

#### Python Tool - Code Analysis

```yaml
mcp_tools:
  - name: analyze_complexity
    description: Analyze code complexity
    type: python
    module: radon.complexity
    function: cc_visit
    parameters:
      code:
        type: string
        description: Code to analyze
        required: true
```

**Usage in Chat:**
> "What's the complexity of the main.cpp file?"

### Doxygen Import Workflow

1. **Generate Doxygen XML**

```bash
# Ensure Doxyfile has:
# GENERATE_XML = YES
# XML_OUTPUT = xml

doxygen Doxyfile
```

2. **Configure Import**

```yaml
enable_doxygen_import: true
doxygen_xml_dir: ./doxygen/xml
doxygen_validate_freshness: true
doxygen_merge_strategy: auto
```

3. **Build Documentation**

```bash
mkdocs build
```

4. **Review Results**

The importer will:
- ✅ Parse Doxygen XML
- ✅ Validate against current code
- ✅ Merge or create sections
- ⚠️ Flag outdated content
- ❌ Skip removed entities

### MinIO Storage

#### Configuration

```yaml
enable_minio: true
minio_config:
  endpoint: localhost:9000
  access_key: admin
  secret_key: password
  bucket_name: mkdocs-documentation
  secure: false
```

#### Programmatic Usage

```python
from mkdocs_chatbot.minio_storage import MinioStorageManager

storage = MinioStorageManager(config)

# Upload file
storage.upload_file('README.md', 'docs/README.md')

# Download file
storage.download_file('docs/README.md', 'local_README.md')

# Generate presigned URL
url = storage.generate_presigned_url('docs/README.md', expires_seconds=3600)

# Sync directory
storage.sync_directory('./docs/', prefix='documentation/')
```

### n8n Integration

#### Setup n8n Workflow

1. **Create Webhook Node**
   - URL: `http://localhost:5678/webhook/chatbot`
   - Method: POST

2. **Add OpenAI Node**
   - Connect to webhook
   - Configure model and prompts

3. **Add Response Node**
   - Return JSON: `{"response": "..."}`

#### Configure MkDocs

```yaml
enable_n8n: true
n8n_webhook_url: http://localhost:5678/webhook/chatbot
n8n_api_key: ${N8N_API_KEY}
```

---

## Usage Examples

### Example 1: Basic Chatbot Query

**User:** "What does the Parser class do?"

**Chatbot:**
```
The Parser class handles C++ code parsing and AST generation.

📚 Sources (2):
1. **Parser Documentation** - The Parser class uses libclang to...
   Relevance: 95%

2. **Architecture Overview** - The parsing system consists of...
   Relevance: 87%
```

### Example 2: Using MCP Tools

**User:** "Run tests for the network module"

**Chatbot:**
```
I'll run the tests for the network module.

🔧 Executing: run_tests(module="network")

✅ Test Results:
- 15 tests passed
- 0 tests failed
- Duration: 2.3s

All tests passed successfully!
```

### Example 3: RAG-Enhanced Response

**User:** "How do I handle errors in the HTTP client?"

**Chatbot:**
```
Based on the documentation, here's how to handle errors:

1. **Exception Handling:**
   The HTTPClient throws `NetworkException` for connection errors.

2. **Error Codes:**
   Use `response.statusCode()` to check HTTP status.

3. **Retry Logic:**
   The client supports automatic retries via `setRetryPolicy()`.

📚 Sources:
- HTTP Client API Reference (Relevance: 92%)
- Error Handling Guide (Relevance: 88%)
- Network Module Overview (Relevance: 75%)
```

---

## Troubleshooting

### RAG Issues

**Problem:** "RAG not finding relevant documents"

**Solution:**
1. Check Qdrant is running: `curl http://localhost:6333`
2. Verify collection exists
3. Check embedding model is downloaded
4. Increase `top_k` value

**Problem:** "Slow RAG queries"

**Solution:**
1. Use Qdrant instead of ChromaDB
2. Reduce `top_k` to 3-5
3. Use smaller embedding model
4. Add query filters

### MCP Tools Issues

**Problem:** "Tool execution fails"

**Solution:**
1. Check tool configuration syntax
2. Verify endpoint URLs are accessible
3. Check API keys/tokens
4. Review tool logs in API server

### Doxygen Import Issues

**Problem:** "Doxygen content marked as outdated"

**Solution:**
1. Regenerate Doxygen XML
2. Check source file paths match
3. Review LLM validation prompts
4. Set `doxygen_validate_freshness: false` to skip

### MinIO Issues

**Problem:** "Cannot connect to MinIO"

**Solution:**
1. Verify MinIO is running: `curl http://localhost:9000`
2. Check access key/secret key
3. Verify bucket exists
4. Check network connectivity

### API Server Issues

**Problem:** "Backend API not responding"

**Solution:**
1. Check API server started: Look for "API server started on localhost:8765"
2. Verify port is not in use: `netstat -an | grep 8765`
3. Check firewall settings
4. Review Flask logs

---

## Performance Tips

### 1. RAG Optimization

```yaml
# Faster embedding model
embedding_model: sentence-transformers/all-MiniLM-L6-v2  # Fast, good quality

# vs slower but more accurate
# embedding_model: sentence-transformers/all-mpnet-base-v2
```

### 2. LLM Optimization

```yaml
# Use smaller, faster models for simple queries
# Use larger models for complex analysis
max_tokens: 500  # Reduce for faster responses
temperature: 0.3  # Lower for more consistent answers
```

### 3. Caching

```yaml
# Enable aggressive caching
enable_cache: true
cache_dir: .cache/llm-autodoc

# Disable for fresh generation
force_regenerate: false
```

### 4. Parallel Processing

```yaml
# Increase for faster generation
max_concurrent_llm_calls: 5  # Adjust based on API limits

# Reduce for rate-limited APIs
max_concurrent_llm_calls: 2
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        MkDocs Site                          │
│                                                             │
│  ┌──────────────┐    ┌────────────────┐   ┌─────────────┐ │
│  │   Generated  │    │    ChatBot     │   │   Search    │ │
│  │     Docs     │    │    Widget      │   │    Bar      │ │
│  └──────────────┘    └────────────────┘   └─────────────┘ │
└──────────────────┬──────────────┬──────────────────────────┘
                   │              │
        ┌──────────┴──────┐      │
        │  LLM AutoDoc    │      │
        │     Plugin      │      │
        └─────────────────┘      │
                │                │
      ┌─────────┼────────────────┼─────────────┐
      │         │                │             │
  ┌───▼────┐ ┌─▼──────┐  ┌──────▼────┐  ┌────▼────┐
  │Doxygen │ │  LLM   │  │  Backend  │  │   RAG   │
  │Import  │ │Provider│  │API Server │  │ Storage │
  └────────┘ └────────┘  └───────────┘  └─────────┘
                │              │              │
      ┌─────────┼──────────────┼──────────────┘
      │         │              │
  ┌───▼────┐ ┌──▼──────┐  ┌───▼──────┐
  │LM Studio│ │MCP Tools│  │ Qdrant  │
  │Anthropic│ │  n8n    │  │ChromaDB │
  │ OpenAI  │ │ MinIO   │  │ Pinecone│
  └─────────┘ └─────────┘  └─────────┘
```

---

## Additional Resources

- **LM Studio:** https://lmstudio.ai/
- **Qdrant:** https://qdrant.tech/documentation/
- **MinIO:** https://min.io/docs/minio/linux/index.html
- **n8n:** https://docs.n8n.io/
- **MCP Protocol:** https://modelcontextprotocol.io/
- **MkDocs Material:** https://squidfunk.github.io/mkdocs-material/

---

## Contributing

Found a bug or have a feature request? Please open an issue on GitHub.

## License

This project is licensed under the MIT License.

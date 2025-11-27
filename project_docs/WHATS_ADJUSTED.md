# What Has Been Adjusted for Windows Environment

## New Components Added

### 1. Document Upload System
A complete document processing and upload system has been created specifically for Windows to work with your n8n RAG service.

### 2. Files Created

#### Core Python Module
- **`document_uploader.py`** (line 1-384)
  - `DocumentProcessor` class: Handles intelligent document splitting
  - `N8NUploader` class: Manages webhook uploads to n8n
  - Language-aware splitters for 17+ programming languages
  - PDF extraction and processing
  - Automatic file type detection and appropriate splitter selection

#### Configuration Files
- **`windowsEnv_requirements.txt`** - Dependencies for document processing:
  - langchain & langchain-text-splitters
  - pypdf for PDF processing
  - requests for HTTP communication
  - python-dotenv for environment management
  - python-magic-bin (Windows-specific file type detection)

- **`.env.windows`** - Environment template with your n8n webhook:
  ```
  N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data
  DEFAULT_CHUNK_SIZE=1000
  DEFAULT_CHUNK_OVERLAP=200
  ```

#### Windows Batch Scripts
- **`setup_document_uploader.bat`** - Automated setup:
  - Creates venvWindows virtual environment
  - Installs all dependencies
  - Creates .env configuration

- **`upload_document.bat`** - Upload any document:
  ```batch
  upload_document.bat file.cpp
  upload_document.bat file.cpp 1500 250
  ```

- **`test_upload.bat`** - Test with sample files:
  - Creates test C++, Python, Markdown files
  - Uploads them to n8n
  - Verifies the service works

- **`quick_test.bat`** - Local test without upload:
  - Tests splitting functionality offline
  - No network connection required

#### PowerShell Alternative
- **`setup_document_uploader.ps1`** - PowerShell version of setup
  - Better error messages
  - Colored output
  - More Windows-friendly

#### Testing Scripts
- **`quick_test.py`** - Local testing without n8n:
  - Tests C++ splitting
  - Tests Markdown splitting
  - Shows chunk details
  - No upload required

#### Documentation
- **`DOCUMENT_UPLOADER_README.md`** - Complete guide (350+ lines):
  - Quick start instructions
  - Feature documentation
  - Usage examples
  - Troubleshooting guide
  - API documentation

- **`SETUP_SUMMARY.md`** - Quick reference:
  - Step-by-step setup
  - Testing checklist
  - Configuration options
  - Examples

## How It Works

### 1. Intelligent Document Splitting

The system uses LangChain's specialized text splitters:

```python
# C++ file example
processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
chunks = processor.process_file('example.cpp')
```

**For C++ files** (`.cpp`, `.h`, `.hpp`):
- Uses `RecursiveCharacterTextSplitter.from_language(Language.CPP)`
- Understands class/function boundaries
- Preserves code structure
- Splits at logical points (comments, functions, classes)

**For Python files** (`.py`):
- Uses Python-specific language splitter
- Maintains indentation context
- Respects function/class definitions

**For Markdown** (`.md`):
- Uses `MarkdownTextSplitter`
- Preserves header hierarchy
- Keeps code blocks intact
- Maintains document structure

**For PDFs** (`.pdf`):
- Extracts text page-by-page using pypdf
- Splits intelligently while noting page boundaries
- Handles multi-column layouts

### 2. Upload to n8n

```python
uploader = N8NUploader('http://192.168.0.72:5678/webhook/upload_data')
result = uploader.upload_chunks(file_path, chunks, metadata)
```

Sends POST request with:
```json
{
  "file_name": "example.cpp",
  "file_path": "Z:\\mkdocs\\example.cpp",
  "file_type": ".cpp",
  "total_chunks": 5,
  "chunks": ["chunk1", "chunk2", ...],
  "metadata": {}
}
```

## What Needs to Be Adjusted in Your Project

### 1. n8n Workflow Configuration

Your n8n workflow at `http://192.168.0.72:5678/webhook/upload_data` should:

**Accept POST requests** with this structure:
```json
{
  "file_name": string,
  "file_path": string,
  "file_type": string,
  "total_chunks": number,
  "chunks": array of strings,
  "metadata": object
}
```

**Example n8n webhook node:**
```
Method: POST
Path: /webhook/upload_data
Response Code: 200
Response Data: JSON
```

**Example workflow:**
1. Webhook Trigger (receives data)
2. Process chunks (loop through array)
3. Store in vector database (Pinecone/Qdrant/Weaviate)
4. Return success response

### 2. Environment Configuration

Edit `.env` file (created from `.env.windows`):

```env
# Verify this matches your n8n instance
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data

# Adjust based on your RAG requirements
DEFAULT_CHUNK_SIZE=1000        # Smaller chunks = more precise retrieval
DEFAULT_CHUNK_OVERLAP=200      # Overlap preserves context at boundaries

# Set to DEBUG to see detailed logs
LOG_LEVEL=INFO
```

### 3. Chunk Size Recommendations

**For Code (C++, Python, etc.):**
- Chunk size: 1000-1500 characters
- Overlap: 200-300 characters
- Rationale: Complete functions/classes in chunks

**For Documentation (Markdown, PDF):**
- Chunk size: 800-1200 characters
- Overlap: 150-250 characters
- Rationale: Complete paragraphs/sections

**For Large Context Models:**
- Chunk size: 2000-3000 characters
- Overlap: 300-500 characters
- Rationale: More context per chunk

### 4. Network/Firewall Settings

Ensure:
- Windows Firewall allows outbound connections to `192.168.0.72:5678`
- n8n service is running and accessible
- Network path between machines is working

Test connectivity:
```batch
curl -X POST http://192.168.0.72:5678/webhook/upload_data
```

## Integration with Existing Project

### Option 1: Standalone Usage

Use the document uploader independently:

```batch
cd Z:\mkdocs
upload_document.bat cpp-project\libtorrent\src\torrent.cpp
```

### Option 2: Integrate with MkDocs Build

Add to your MkDocs build process:

```python
# In mkdocs_build_control.py or similar
import os
from document_uploader import upload_document

def upload_docs_to_rag():
    """Upload all documentation to RAG system."""
    docs_dir = 'docs'
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(('.md', '.py', '.cpp', '.h')):
                file_path = os.path.join(root, file)
                upload_document(file_path)
```

### Option 3: Batch Process Existing Files

Create a custom batch script:

```batch
@echo off
REM upload_all_cpp.bat

echo Uploading all C++ files from cpp-project...

for /r cpp-project %%f in (*.cpp *.h *.hpp) do (
    echo Uploading %%f
    call upload_document.bat "%%f"
)

echo Done!
```

## Dependencies Added

### Python Packages (installed in venvWindows)

```
langchain>=0.1.0               # Text splitting framework
langchain-text-splitters        # Specialized splitters
pypdf>=3.17.0                  # PDF processing
requests>=2.31.0               # HTTP client
python-dotenv>=1.0.0           # Environment config
python-magic-bin (Windows)     # File type detection
```

### Why These Dependencies?

1. **langchain** - Provides intelligent text splitting that understands:
   - Programming language syntax
   - Document structure
   - Semantic boundaries

2. **pypdf** - Reliable PDF text extraction on Windows

3. **requests** - HTTP communication with n8n

4. **python-dotenv** - Secure configuration management

5. **python-magic-bin** - Windows file type detection (no native libmagic)

## File Encoding Handling

The system handles Windows-specific encoding issues:

```python
encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
for encoding in encodings:
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        break
    except UnicodeDecodeError:
        continue
```

This ensures files with:
- UTF-8 (most modern files)
- UTF-16 (some Windows apps)
- Latin-1 (legacy files)
- CP1252 (Windows default)

...are all handled correctly.

## Language Support

The system supports language-aware splitting for:

| Language | Extensions | Features |
|----------|-----------|----------|
| C/C++ | `.c`, `.cpp`, `.h`, `.hpp`, `.cc`, `.cxx` | Function/class boundaries |
| Python | `.py` | Indentation-aware |
| JavaScript | `.js` | Function/class detection |
| TypeScript | `.ts` | Type-aware splitting |
| Java | `.java` | Class/method boundaries |
| Go | `.go` | Package-aware |
| Rust | `.rs` | Module-aware |
| Ruby | `.rb` | Class/method detection |
| PHP | `.php` | Function/class boundaries |
| Scala | `.scala` | Object/trait awareness |
| Swift | `.swift` | Protocol-aware |
| Kotlin | `.kt` | Class/function detection |
| C# | `.cs` | Namespace-aware |
| Lua | `.lua` | Function detection |
| Perl | `.pl` | Subroutine detection |
| R | `.r` | Function detection |
| Solidity | `.sol` | Contract-aware |

## Testing the Setup

### Step-by-Step Test

1. **Setup** (5 minutes):
   ```batch
   setup_document_uploader.bat
   ```

2. **Local Test** (no n8n required):
   ```batch
   quick_test.bat
   ```
   Expected output: Shows chunk counts and previews

3. **n8n Connection Test**:
   ```batch
   test_upload.bat
   ```
   Expected output: 3 successful uploads (C++, Python, Markdown)

4. **Upload Real File**:
   ```batch
   upload_document.bat cpp-project\libtorrent\include\libtorrent\torrent.hpp
   ```

### Verify in n8n

Check your n8n workflow receives:
- Correct file name
- File type
- Array of text chunks
- Metadata

## No Changes to Existing Files

This is entirely additive - no existing files were modified:
- Your MkDocs configuration is unchanged
- Existing Python scripts untouched
- cpp-project remains as-is
- All new files are self-contained

## Summary

You now have a complete Windows-compatible document upload system that:

1. Automatically processes documents with language-aware splitting
2. Supports 17+ programming languages + PDFs
3. Uploads to your n8n RAG service at `http://192.168.0.72:5678/webhook/upload_data`
4. Includes comprehensive testing and documentation
5. Works standalone or can be integrated with your existing project

To start using it:
```batch
setup_document_uploader.bat
upload_document.bat yourfile.cpp
```

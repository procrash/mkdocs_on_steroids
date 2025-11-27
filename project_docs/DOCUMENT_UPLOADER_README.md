# Document Upload Service for Windows

Automatically process and upload documents to your n8n RAG service with intelligent text splitting using LangChain.

## Features

- **Smart Text Splitting**: Automatically selects the appropriate splitter based on file type
  - C/C++ files: Uses `RecursiveCharacterTextSplitter` with C/C++ syntax awareness
  - Python, JavaScript, TypeScript, Java, etc.: Language-specific splitting
  - Markdown: `MarkdownTextSplitter` preserving structure
  - LaTeX: `LatexTextSplitter` for .tex files
  - PDF: Extracts text and splits intelligently by pages
  - HTML/XML: Structure-aware splitting
  - Plain text: Smart recursive splitting

- **Supported File Types**:
  - Programming languages: `.py`, `.cpp`, `.h`, `.hpp`, `.c`, `.cc`, `.cxx`, `.java`, `.js`, `.ts`, `.go`, `.rs`, `.rb`, `.php`, `.scala`, `.swift`, `.kt`, `.cs`, `.lua`, `.pl`, `.r`, `.sol`
  - Documents: `.md`, `.markdown`, `.txt`, `.pdf`, `.rst`
  - Markup: `.html`, `.htm`, `.xml`
  - LaTeX: `.tex`, `.latex`

- **Configurable Chunking**: Customize chunk size and overlap
- **Windows-Optimized**: Batch scripts for easy setup and usage
- **n8n Integration**: Direct webhook upload to your RAG service

## Quick Start

### 1. Setup

Run the setup script to create a virtual environment and install dependencies:

```batch
setup_document_uploader.bat
```

This will:
- Create a Python virtual environment (`venvWindows`)
- Install all required dependencies
- Create a `.env` configuration file

### 2. Configure

Edit the `.env` file to configure your n8n webhook URL:

```env
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=200
```

### 3. Test

Run the test script to verify everything works:

```batch
test_upload.bat
```

This creates sample files (C++, Python, Markdown) and uploads them to your n8n service.

### 4. Upload Documents

Upload any supported document:

```batch
upload_document.bat path\to\your\file.cpp
upload_document.bat document.pdf
upload_document.bat README.md
```

With custom chunk settings:

```batch
upload_document.bat large_file.cpp 1500 250
```

## Usage

### Command Line

```batch
# Basic usage
python document_uploader.py path/to/file.cpp

# With custom chunk size and overlap
python document_uploader.py path/to/file.cpp --chunk-size 1500 --chunk-overlap 250

# With custom webhook URL
python document_uploader.py path/to/file.cpp --webhook-url http://custom-url/webhook
```

### Python API

```python
from document_uploader import upload_document

# Upload a file
result = upload_document('path/to/file.cpp')

# With custom settings
result = upload_document(
    'path/to/file.cpp',
    chunk_size=1500,
    chunk_overlap=250,
    metadata={'project': 'my_project', 'version': '1.0'}
)
```

### Advanced Usage

```python
from document_uploader import DocumentProcessor, N8NUploader

# Process a file
processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
chunks = processor.process_file('example.cpp')

# Upload chunks
uploader = N8NUploader('http://192.168.0.72:5678/webhook/upload_data')
result = uploader.upload_chunks(
    'example.cpp',
    chunks,
    metadata={'author': 'John Doe'}
)
```

## How It Works

### 1. File Type Detection

The system automatically detects the file type based on extension and selects the appropriate splitter:

```python
# C++ file -> Language-aware C++ splitter
upload_document.bat example.cpp

# Markdown -> MarkdownTextSplitter
upload_document.bat README.md

# PDF -> PDF text extraction + smart splitting
upload_document.bat document.pdf
```

### 2. Text Splitting

Each splitter is optimized for its file type:

- **C/C++ Splitter**: Understands class/function boundaries, preserves code structure
- **Python Splitter**: Respects function/class definitions, maintains indentation context
- **Markdown Splitter**: Splits on headers while preserving structure
- **PDF Splitter**: Extracts text per page, then splits intelligently

### 3. Upload to n8n

Chunks are sent as JSON to your n8n webhook:

```json
{
  "file_name": "example.cpp",
  "file_path": "Z:\\mkdocs\\example.cpp",
  "file_type": ".cpp",
  "total_chunks": 5,
  "chunks": [
    "chunk 1 content...",
    "chunk 2 content...",
    "..."
  ],
  "metadata": {}
}
```

## Configuration

### Environment Variables (`.env`)

```env
# Required: n8n webhook URL
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data

# Optional: Chunk settings
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=200

# Optional: Logging
LOG_LEVEL=INFO
```

### Chunk Size Guidelines

- **Small chunks (500-800)**: Better for precise retrieval, more chunks
- **Medium chunks (1000-1500)**: Balanced approach (recommended)
- **Large chunks (2000-3000)**: More context, fewer chunks

### Chunk Overlap

Overlap ensures context isn't lost at chunk boundaries:
- **Low overlap (100-150)**: Less redundancy
- **Medium overlap (200-300)**: Recommended for most cases
- **High overlap (400-500)**: Maximum context preservation

## Troubleshooting

### Connection Errors

If you see connection errors:

1. Verify n8n is running:
   ```batch
   curl http://192.168.0.72:5678/webhook/upload_data
   ```

2. Check firewall settings
3. Verify the webhook URL in `.env`

### Encoding Errors

The system tries multiple encodings (UTF-8, UTF-16, Latin-1, CP1252). If you still get errors:

```python
# Manually specify encoding in your code
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```

### PDF Extraction Issues

If PDF text extraction fails:

```batch
pip install --upgrade pypdf PyPDF2 pdfminer.six
```

## Dependencies

Core dependencies (installed automatically):

- `langchain` - Text splitting framework
- `langchain-text-splitters` - Specialized splitters
- `pypdf` / `PyPDF2` - PDF processing
- `requests` - HTTP client
- `python-dotenv` - Environment configuration
- `python-magic-bin` - File type detection (Windows)

## Examples

### Example 1: Upload C++ Project

```batch
REM Upload all C++ files in a directory
for /r cpp-project %%f in (*.cpp *.h *.hpp) do (
    upload_document.bat "%%f"
)
```

### Example 2: Batch Upload with Metadata

```python
import os
from pathlib import Path
from document_uploader import upload_document

# Upload all Python files with metadata
for file_path in Path('src').rglob('*.py'):
    upload_document(
        str(file_path),
        metadata={
            'project': 'my_project',
            'directory': str(file_path.parent),
            'size': os.path.getsize(file_path)
        }
    )
```

### Example 3: Custom Splitter Configuration

```python
from document_uploader import DocumentProcessor

# Create processor with custom settings
processor = DocumentProcessor(chunk_size=2000, chunk_overlap=400)

# Process file
chunks = processor.process_file('large_document.md')

print(f"Created {len(chunks)} chunks")
for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i+1}:")
    print(chunk[:200] + "...")
```

## n8n Webhook Configuration

Your n8n workflow should accept POST requests with this structure:

```json
{
  "file_name": "string",
  "file_path": "string",
  "file_type": "string",
  "total_chunks": "number",
  "chunks": ["array of strings"],
  "metadata": {"object"}
}
```

Example n8n webhook node configuration:
- Method: POST
- Response Code: 200
- Response Data: JSON

## License

This tool is designed to work with your existing n8n RAG service setup.

## Support

For issues or questions:
1. Check the logs (set `LOG_LEVEL=DEBUG` in `.env`)
2. Verify your n8n service is running
3. Test with the provided test files first
4. Check file permissions on Windows

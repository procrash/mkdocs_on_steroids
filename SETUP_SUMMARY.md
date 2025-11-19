# Document Upload Service - Setup Summary

## What Has Been Created

A complete Windows environment for uploading and processing documents to your n8n RAG service at `http://192.168.0.72:5678/webhook/upload_data`.

### Files Created

1. **`document_uploader.py`** - Main Python script with intelligent document processing
2. **`windowsEnv_requirements.txt`** - All required dependencies
3. **`.env.windows`** - Environment configuration template
4. **Setup Scripts:**
   - `setup_document_uploader.bat` - Automated Windows setup
   - `setup_document_uploader.ps1` - PowerShell setup script
5. **Usage Scripts:**
   - `upload_document.bat` - Upload any document
   - `test_upload.bat` - Test with sample files
   - `quick_test.bat` - Local test without uploading
6. **Helper Scripts:**
   - `quick_test.py` - Tests splitting locally
7. **Documentation:**
   - `DOCUMENT_UPLOADER_README.md` - Complete usage guide

## Quick Start Guide

### Step 1: Run Setup

```batch
setup_document_uploader.bat
```

This will:
- Create `venvWindows` virtual environment
- Install all dependencies
- Create `.env` configuration file

### Step 2: Configure n8n Endpoint

Edit `.env` file and verify the webhook URL:

```env
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data
```

### Step 3: Test Local Splitting (No Upload)

```batch
quick_test.bat
```

This tests the document splitting functionality locally without uploading to n8n.

### Step 4: Test Upload to n8n

```batch
test_upload.bat
```

This creates sample C++, Python, and Markdown files and uploads them to your n8n service.

### Step 5: Upload Your Documents

```batch
upload_document.bat path\to\your\file.cpp
upload_document.bat document.pdf
```

## Features

### Smart Document Splitting

The system automatically selects the best splitter for each file type:

| File Type | Splitter Used | Example Extensions |
|-----------|---------------|-------------------|
| C/C++ | Language-aware C++ splitter | `.cpp`, `.h`, `.hpp`, `.c`, `.cc` |
| Python | Python-specific splitter | `.py` |
| JavaScript/TypeScript | JS/TS splitter | `.js`, `.ts` |
| Java | Java splitter | `.java` |
| Go, Rust, Ruby, etc. | Language-specific splitters | `.go`, `.rs`, `.rb`, etc. |
| Markdown | MarkdownTextSplitter | `.md`, `.markdown` |
| LaTeX | LatexTextSplitter | `.tex`, `.latex` |
| PDF | PDF extraction + smart splitting | `.pdf` |
| HTML/XML | Structure-aware splitting | `.html`, `.xml` |
| Plain Text | RecursiveCharacterTextSplitter | `.txt` |

### Supported Programming Languages

The following languages have dedicated language-aware splitters:

- C/C++ (`.c`, `.cpp`, `.h`, `.hpp`, `.cc`, `.cxx`)
- Python (`.py`)
- JavaScript (`.js`)
- TypeScript (`.ts`)
- Java (`.java`)
- Go (`.go`)
- Rust (`.rs`)
- Ruby (`.rb`)
- PHP (`.php`)
- Scala (`.scala`)
- Swift (`.swift`)
- Kotlin (`.kt`)
- C# (`.cs`)
- Lua (`.lua`)
- Perl (`.pl`)
- R (`.r`)
- Solidity (`.sol`)

## Configuration Options

### Environment Variables (.env)

```env
# Required: n8n webhook URL
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data

# Optional: Chunk settings (defaults shown)
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=200

# Optional: Logging
LOG_LEVEL=INFO
```

### Custom Chunk Settings

```batch
# Default settings (chunk_size=1000, overlap=200)
upload_document.bat file.cpp

# Custom settings
upload_document.bat file.cpp 1500 250
```

## Usage Examples

### Example 1: Upload a C++ File

```batch
upload_document.bat cpp-project\src\main.cpp
```

The C++ file will be split using the language-aware C++ splitter that understands:
- Class and function boundaries
- Namespace structure
- Header/implementation separation
- Comment blocks

### Example 2: Upload a PDF

```batch
upload_document.bat documentation.pdf
```

PDF files are:
1. Text extracted page-by-page
2. Split intelligently while preserving page boundaries
3. Uploaded with page metadata

### Example 3: Upload Markdown Documentation

```batch
upload_document.bat README.md
```

Markdown files are split while preserving:
- Header hierarchy
- Code blocks
- Lists and structure

### Example 4: Batch Upload Directory

```batch
for /r src %%f in (*.cpp *.h) do upload_document.bat "%%f"
```

### Example 5: Python API Usage

```python
from document_uploader import upload_document

# Basic upload
upload_document('example.cpp')

# With metadata
upload_document(
    'example.cpp',
    chunk_size=1500,
    metadata={'project': 'my_project', 'author': 'John'}
)
```

## Data Sent to n8n

Each upload sends JSON data in this format:

```json
{
  "file_name": "example.cpp",
  "file_path": "Z:\\mkdocs\\example.cpp",
  "file_type": ".cpp",
  "total_chunks": 5,
  "chunks": [
    "// Chunk 1 content...",
    "// Chunk 2 content...",
    "..."
  ],
  "metadata": {}
}
```

Your n8n workflow receives this data via POST request.

## Adjustments Made for Windows

1. **Virtual Environment**: Creates `venvWindows` directory
2. **Batch Scripts**: Windows .bat files for easy execution
3. **PowerShell Scripts**: Alternative PowerShell versions
4. **File Type Detection**: Uses `python-magic-bin` (Windows-specific)
5. **Path Handling**: Windows path separators handled automatically
6. **Encoding**: Multiple encoding fallbacks (UTF-8, UTF-16, Latin-1, CP1252)

## Troubleshooting

### If Setup Fails

```batch
# Manually create virtual environment
python -m venv venvWindows

# Activate it
venvWindows\Scripts\activate.bat

# Install dependencies
pip install -r windowsEnv_requirements.txt
```

### If Upload Fails

1. Check n8n is running: Open `http://192.168.0.72:5678` in browser
2. Verify webhook URL in `.env`
3. Test connectivity: `curl -X POST http://192.168.0.72:5678/webhook/upload_data`
4. Check firewall settings
5. Enable debug logging: Set `LOG_LEVEL=DEBUG` in `.env`

### If Encoding Errors Occur

The system tries multiple encodings automatically. If you still get errors, the file might be binary or corrupted.

### If PDF Extraction Fails

```batch
venvWindows\Scripts\activate.bat
pip install --upgrade pypdf PyPDF2 pdfminer.six
```

## Next Steps

1. **Configure n8n workflow** to handle the incoming data
2. **Test with your documents** using `upload_document.bat`
3. **Customize chunk settings** based on your RAG requirements
4. **Batch process** multiple files as needed

## Testing Checklist

- [ ] Run `setup_document_uploader.bat`
- [ ] Verify `.env` configuration
- [ ] Run `quick_test.bat` (tests splitting locally)
- [ ] Ensure n8n service is running
- [ ] Run `test_upload.bat` (tests upload to n8n)
- [ ] Upload a real document with `upload_document.bat`
- [ ] Verify data received in n8n

## For More Information

See `DOCUMENT_UPLOADER_README.md` for:
- Detailed API documentation
- Advanced configuration options
- More code examples
- Complete feature list

## Support

If you encounter issues:
1. Check logs (set `LOG_LEVEL=DEBUG` in `.env`)
2. Verify n8n service is accessible
3. Test with provided sample files first
4. Check Windows firewall/antivirus settings

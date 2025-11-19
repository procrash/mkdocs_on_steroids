# Batch Files Guide

## Overview

This directory contains various batch files for different tasks. Here's what each one does:

---

## 📦 Setup & Installation

### `setup_document_uploader.bat`

**Purpose**: Initial setup for the document upload system

**What it does**:
1. Creates a Windows virtual environment (`venvWindows`)
2. Installs all Python dependencies (requests, langchain, pypdf, etc.)
3. Prepares the environment for document uploading

**When to use**:
- First time setup
- After fresh git clone
- If dependencies are broken/missing

**Command**:
```cmd
setup_document_uploader.bat
```

---

## 🧪 Testing Files

### `test_n8n_connection.bat`

**Purpose**: Test if n8n is reachable and webhook is working

**What it does**:
1. Activates virtual environment
2. Sends a simple test request to the n8n webhook
3. Verifies connection and reports success/failure

**When to use**:
- Before uploading documents
- After changing n8n configuration
- Troubleshooting connection issues

**Command**:
```cmd
test_n8n_connection.bat
```

---

### `test_webhook_only.bat`

**Purpose**: Quick test of the webhook endpoint with minimal data

**What it does**:
1. Activates virtual environment
2. Sends a small test payload (2 chunks) to webhook
3. Tests the webhook response without uploading real files

**When to use**:
- Quick webhook validation
- Testing new webhook configuration
- Before running full upload tests

**Command**:
```cmd
test_webhook_only.bat
```

**Test data sent**:
```json
{
  "file_name": "test.txt",
  "file_type": ".txt",
  "content": "Test content...",
  "metadata": {"test": true}
}
```

---

### `test_upload.bat`

**Purpose**: Full test of document upload with real files

**What it does**:
1. Creates test documents (C++, Markdown, Python)
2. Uploads each file to n8n
3. Tests the complete upload pipeline
4. Verifies all file types work correctly

**When to use**:
- After setup completion
- Testing new n8n workflow
- Verifying file type handling

**Command**:
```cmd
test_upload.bat
```

**Test files created**:
- `test_documents/test.cpp` - C++ code sample
- `test_documents/test.md` - Markdown sample
- `test_documents/test.py` - Python code sample

---

## 📤 Document Upload

### `upload_document.bat`

**Purpose**: Upload a single document to RAG system

**What it does**:
1. Accepts a file path as argument
2. Uploads that specific file to n8n
3. n8n processes and stores in Qdrant

**When to use**:
- Uploading individual files
- Manual document additions
- Selective file uploads

**Command**:
```cmd
upload_document.bat <file_path>
```

**Examples**:
```cmd
upload_document.bat "Z:\mkdocs\README.md"
upload_document.bat "C:\projects\mycode.cpp"
```

---

### `auto_upload_plugin.bat`

**Purpose**: Automatically upload mkdocs-llm-autodoc plugin files

**What it does**:
1. Activates virtual environment
2. Runs `auto_document_and_upload.py` on the plugin directory
3. Generates basic documentation for each file
4. Uploads source files AND generated docs to RAG

**When to use**:
- Uploading the entire plugin at once
- Basic documentation generation
- Quick plugin indexing

**Command**:
```cmd
auto_upload_plugin.bat
```

**Processes**:
- All `**/*.py` files in plugin
- All `**/*.md` files in plugin

---

### `smart_upload_plugin.bat` ⭐ **RECOMMENDED**

**Purpose**: Smart upload with Python code analysis

**What it does**:
1. Activates virtual environment
2. Runs `smart_auto_upload.py` with AST parsing
3. Analyzes Python code structure (classes, functions, imports)
4. Generates detailed documentation with extracted docstrings
5. Uploads source files AND smart-generated docs to RAG

**When to use**:
- Best option for uploading plugin code
- When you want detailed code documentation
- To make code queryable by class/function names

**Command**:
```cmd
smart_upload_plugin.bat
```

**Extracts**:
- Module docstrings
- Class definitions and docstrings
- Method names and descriptions
- Function signatures and docs
- Import dependencies

---

## 🌐 MkDocs Server

### `start.bat`

**Purpose**: Start MkDocs development server

**What it does**:
1. Checks if virtual environment exists
2. Installs dependencies if needed
3. Starts `mkdocs serve` on localhost

**When to use**:
- Viewing documentation locally
- Testing MkDocs configuration
- Previewing docs before deployment

**Command**:
```cmd
start.bat
```

**Opens**: `http://127.0.0.1:8000`

---

### `serve.bat`

**Purpose**: Alternative MkDocs server launcher

**What it does**:
- Similar to `start.bat`
- May have different port or configuration

**When to use**:
- Alternative to `start.bat`
- If `start.bat` has conflicts

**Command**:
```cmd
serve.bat
```

---

### `quick_test.bat`

**Purpose**: Quick validation test

**What it does**:
- Likely runs a fast test suite
- Validates basic functionality
- May check configurations

**When to use**:
- Quick sanity checks
- After making changes
- Before commits

**Command**:
```cmd
quick_test.bat
```

---

## 📊 Comparison Table

| Batch File | Category | Speed | Uploads Files | Generates Docs | Use Case |
|-----------|----------|-------|---------------|----------------|----------|
| `setup_document_uploader.bat` | Setup | Slow | ❌ | ❌ | First-time setup |
| `test_n8n_connection.bat` | Test | Fast | ❌ | ❌ | Connection check |
| `test_webhook_only.bat` | Test | Fast | ✅ | ❌ | Webhook validation |
| `test_upload.bat` | Test | Medium | ✅ | ❌ | Full pipeline test |
| `upload_document.bat` | Upload | Fast | ✅ | ❌ | Single file upload |
| `auto_upload_plugin.bat` | Upload | Medium | ✅ | ✅ (Basic) | Plugin batch upload |
| `smart_upload_plugin.bat` ⭐ | Upload | Medium | ✅ | ✅ (Smart) | Plugin smart upload |
| `start.bat` | Server | N/A | ❌ | ❌ | Run MkDocs server |
| `serve.bat` | Server | N/A | ❌ | ❌ | Alt MkDocs server |
| `quick_test.bat` | Test | Fast | ❌ | ❌ | Quick validation |

---

## 🎯 Common Workflows

### First Time Setup

```cmd
1. setup_document_uploader.bat     # Install dependencies
2. test_n8n_connection.bat         # Verify n8n is running
3. test_upload.bat                 # Test full pipeline
4. smart_upload_plugin.bat         # Upload plugin code
```

### Daily Usage

**Upload a single file**:
```cmd
upload_document.bat "path\to\myfile.py"
```

**Update plugin documentation**:
```cmd
smart_upload_plugin.bat
```

**View documentation locally**:
```cmd
start.bat
```

### Troubleshooting

**Connection issues**:
```cmd
test_n8n_connection.bat
```

**Webhook not responding**:
```cmd
test_webhook_only.bat
```

**Upload pipeline broken**:
```cmd
test_upload.bat
```

**Dependencies broken**:
```cmd
setup_document_uploader.bat
```

---

## 🔍 What Each Batch File Typically Contains

### Standard Structure

All batch files follow this pattern:

```batch
@echo off
REM ============================================================================
REM [Description]
REM ============================================================================

echo [Starting message]

REM Check if virtual environment exists
if not exist "venvWindows\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    pause
    exit /b 1
)

REM Activate virtual environment
call venvWindows\Scripts\activate.bat

REM Main commands
[python script or commands here]

if errorlevel 1 (
    echo [ERROR] Failed!
    goto :error
)

echo [Success message]
pause
exit /b 0

:error
echo [Error message]
pause
exit /b 1
```

---

## 🚨 Error Codes

All batch files use these exit codes:

- **0**: Success
- **1**: Error/Failure

Check error code with:
```cmd
echo %ERRORLEVEL%
```

---

## ⚙️ Configuration

Batch files read configuration from:
- `.env.windows` - Windows-specific settings
- `.env` - General settings (fallback)

Key variables:
```env
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data_raw
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=200
```

---

## 📝 Tips

### Running Silently

Remove `pause` commands for unattended runs:
```cmd
setup_document_uploader.bat
REM No pause = closes automatically
```

### Logging Output

Redirect output to file:
```cmd
smart_upload_plugin.bat > upload_log.txt 2>&1
```

### Running from Other Directories

Use full paths:
```cmd
Z:\mkdocs\smart_upload_plugin.bat
```

Or change directory first:
```cmd
cd Z:\mkdocs
smart_upload_plugin.bat
```

### Scheduled Tasks

Create Windows Task Scheduler entry:
- Action: Start a program
- Program: `Z:\mkdocs\smart_upload_plugin.bat`
- Start in: `Z:\mkdocs`

---

## 🆘 Common Issues

### "Virtual environment not found"

**Problem**: `venvWindows` doesn't exist

**Solution**:
```cmd
setup_document_uploader.bat
```

---

### "Cannot find python"

**Problem**: Python not in PATH

**Solution**:
1. Check Python installation
2. Add Python to PATH
3. Re-run setup

---

### "Connection refused"

**Problem**: n8n not running or wrong URL

**Solution**:
1. Start n8n: Check if running at `http://192.168.0.72:5678`
2. Check `.env.windows` webhook URL
3. Run `test_n8n_connection.bat`

---

### "Module not found"

**Problem**: Dependencies not installed

**Solution**:
```cmd
setup_document_uploader.bat
```

---

## 🔄 Maintenance

### Update Dependencies

```cmd
venvWindows\Scripts\activate.bat
pip install --upgrade -r requirements.txt
```

### Clean Virtual Environment

```cmd
rmdir /S /Q venvWindows
setup_document_uploader.bat
```

### Reset Everything

```cmd
rmdir /S /Q venvWindows
rmdir /S /Q test_documents
del /Q **\*_DOCS.md
setup_document_uploader.bat
```

---

## 📚 Related Files

- `document_uploader.py` - Core upload logic
- `auto_document_and_upload.py` - Basic auto-upload
- `smart_auto_upload.py` - Smart auto-upload with AST
- `.env.windows` - Configuration
- `requirements.txt` - Python dependencies

---

## 🎓 Learning Path

1. **Beginner**:
   - `setup_document_uploader.bat`
   - `test_upload.bat`
   - `upload_document.bat`

2. **Intermediate**:
   - `test_webhook_only.bat`
   - `auto_upload_plugin.bat`

3. **Advanced**:
   - `smart_upload_plugin.bat`
   - Custom modifications to scripts

---

## 🤔 FAQ

**Q: Which upload batch file should I use?**
A: Use `smart_upload_plugin.bat` for best results with code analysis.

**Q: Do I need to run setup every time?**
A: No, only once (or when dependencies change).

**Q: Can I upload files from other directories?**
A: Yes, use `upload_document.bat <full_path>`

**Q: How do I know if upload succeeded?**
A: Check the batch file output and n8n execution log.

**Q: What if I get errors?**
A: Run the test batch files to isolate the issue.

---

**Need more help?** Check:
- `AUTO_UPLOAD_README.md` - Auto-upload details
- `OPTION_B_SETUP.md` - n8n workflow setup
- `document_uploader.py` - Source code

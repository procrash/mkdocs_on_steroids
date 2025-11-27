# Automated Documentation and Upload Tools

## Overview

These tools automatically read source files, generate documentation, and upload everything to your RAG system.

## Tools Available

### 1. Basic Auto-Upload (`auto_document_and_upload.py`)

Simple tool that:
- Reads source files
- Generates basic documentation overview
- Uploads both source and docs to RAG

**Usage**:
```bash
python auto_document_and_upload.py <directory> --pattern "**/*.py"
```

**Example**:
```bash
python auto_document_and_upload.py plugins\mkdocs-llm-autodoc --multiple-patterns "**/*.py" "**/*.md"
```

### 2. Smart Auto-Upload (`smart_auto_upload.py`) ⭐ **Recommended**

Advanced tool with Python code analysis that:
- Parses Python AST to extract classes, functions, imports
- Extracts docstrings automatically
- Generates detailed documentation
- Uploads source and generated docs to RAG

**Usage**:
```bash
python smart_auto_upload.py <directory>
```

**Example**:
```bash
python smart_auto_upload.py plugins\mkdocs-llm-autodoc
```

**Options**:
- `--patterns "**/*.py" "**/*.cpp"` - Custom file patterns
- `--no-upload` - Generate docs only without uploading

## Batch Scripts

### For mkdocs-llm-autodoc Plugin

#### `auto_upload_plugin.bat`
Basic upload with simple documentation

#### `smart_upload_plugin.bat` ⭐ **Recommended**
Smart upload with code analysis and detailed docs

Just double-click to run!

## What Gets Uploaded

### Source Files
- Original source code (Python, C++, Markdown, etc.)
- Metadata: file type, project name, language
- Full content for RAG retrieval

### Generated Documentation
For Python files, the smart uploader extracts:
- Module docstring
- All imports/dependencies
- Classes with docstrings
- Class methods with docstrings
- Functions with arguments and docstrings

Example generated doc structure:
```markdown
# filename.py

## Module Overview
(module docstring)

## Dependencies
- import1
- import2

## Classes

### ClassName
(class docstring)

**Methods**:
- method1(): (docstring)
- method2(): (docstring)

## Functions

### function_name(arg1, arg2)
(function docstring)
```

## Example Workflow

### Upload the Plugin

1. Make sure n8n workflow is activated
2. Run the smart uploader:
   ```cmd
   smart_upload_plugin.bat
   ```

3. The script will:
   ```
   📦 Found 13 files to process

   📄 Processing: __init__.py
     [1/3] Uploading source file...
     ✓ Source uploaded
     [2/3] Analyzing Python code...
     ✓ Documentation generated
     [3/3] Uploading documentation...
     ✓ Documentation uploaded

   📄 Processing: plugin.py
     [1/3] Uploading source file...
     ...

   📊 SUMMARY
   ✓ Successfully processed: 13 files
   ```

### Query the RAG System

After upload, you can query about:
- "What classes are in the high_level_agent.py file?"
- "How does the cache manager work?"
- "Show me the cross reference implementation"
- "What functions are available in the llm_provider?"

## Customization

### Add More File Types

Edit the processor methods in `smart_auto_upload.py`:

```python
def process_cpp_file(self, file_path: Path) -> bool:
    """Process C++ files with custom logic."""
    # Your C++ analysis logic
    pass
```

### Custom Documentation Templates

Modify `generate_documentation()` method:

```python
@staticmethod
def generate_documentation(file_path: Path, analysis: Dict) -> str:
    doc = f"# Your Custom Template\n\n"
    # Add your sections
    return doc
```

### Different Upload Metadata

Customize metadata in the upload calls:

```python
upload_document(
    str(file_path),
    metadata={
        'type': 'source_code',
        'language': 'python',
        'project': self.source_dir.name,
        'author': 'your-name',
        'version': '1.0',
        'tags': ['plugin', 'mkdocs']
    }
)
```

## Output Files

Generated documentation files are saved alongside source files:

```
mkdocs_llm_autodoc/
├── plugin.py                    (original source)
├── plugin_DOCS.md               (auto-generated docs)
├── agents/
│   ├── high_level_agent.py     (original source)
│   └── high_level_agent_DOCS.md (auto-generated docs)
```

These are also uploaded to RAG automatically!

## Troubleshooting

### Import Error: No module named 'document_uploader'

**Solution**: Run from the mkdocs directory where `document_uploader.py` is located.

### Webhook Connection Error

**Solution**:
- Check n8n is running: `http://192.168.0.72:5678`
- Verify workflow is activated
- Check `.env` file has correct webhook URL

### AST Parse Error

**Solution**: Some Python files with syntax errors can't be parsed. The script will skip them and continue with others.

### File Already Exists

Generated `*_DOCS.md` files accumulate. This is intentional - they're kept for reference and also uploaded to RAG.

To clean up:
```bash
# Delete all generated docs
del /S *_DOCS.md
```

## Integration with Your Workflow

### Automatic Upload on File Change

Create a file watcher script:

```python
# watch_and_upload.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from smart_auto_upload import SmartAutoUploader

class UploadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            uploader = SmartAutoUploader('.')
            uploader.process_python_file(Path(event.src_path))

observer = Observer()
observer.schedule(UploadHandler(), 'plugins/mkdocs-llm-autodoc', recursive=True)
observer.start()
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python smart_auto_upload.py plugins/mkdocs-llm-autodoc --no-upload
git add **/*_DOCS.md
```

### CI/CD Integration

Add to your CI pipeline:

```yaml
# .github/workflows/upload-to-rag.yml
name: Upload to RAG
on: [push]
jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Upload to RAG
        run: |
          python smart_auto_upload.py plugins/mkdocs-llm-autodoc
```

## Advanced Usage

### Batch Process Multiple Projects

```bash
# Upload multiple projects
python smart_auto_upload.py project1
python smart_auto_upload.py project2
python smart_auto_upload.py project3
```

### Custom Patterns

```bash
# Only upload specific files
python smart_auto_upload.py . --patterns "**/agent*.py" "**/parser*.py"
```

### Generate Docs Without Upload

```bash
# Just generate documentation files
python smart_auto_upload.py plugins/mkdocs-llm-autodoc --no-upload
```

Then review the generated `*_DOCS.md` files before uploading.

## Performance

- **Small projects** (<50 files): ~1-2 minutes
- **Medium projects** (50-200 files): ~5-10 minutes
- **Large projects** (200+ files): ~15-30 minutes

Time depends on:
- File sizes
- Network speed to n8n
- n8n processing (splitting, embedding)
- Qdrant insertion speed

## Best Practices

1. **Start Small**: Test with a single file first
2. **Review Generated Docs**: Check `*_DOCS.md` files are correct
3. **Incremental Upload**: Upload in batches if you have many files
4. **Backup Qdrant**: Before large uploads, backup your Qdrant collection
5. **Monitor n8n**: Watch the execution log during uploads
6. **Clean Old Docs**: Periodically remove outdated `*_DOCS.md` files

## Future Enhancements

Potential additions:
- [ ] C++ code analysis with libclang
- [ ] JavaScript/TypeScript analysis
- [ ] Incremental upload (only changed files)
- [ ] Dependency graph generation
- [ ] Call graph analysis
- [ ] Test coverage integration
- [ ] Git blame integration
- [ ] Interactive selection UI

## Questions?

Check:
1. n8n execution logs
2. Python script output
3. Qdrant collection contents
4. Generated `*_DOCS.md` files

Still stuck? Review:
- `OPTION_B_SETUP.md` - n8n workflow setup
- `document_uploader.py` - Upload logic
- `.env.windows` - Configuration

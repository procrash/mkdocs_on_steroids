# Quick Start: RAG Integration with mkdocs-llm-autodoc

## TL;DR

Add 3 lines to your `mkdocs.yml` and **ALL your project files** (Python, C++, Markdown, etc.) + generated docs automatically upload to RAG during every build!

```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: true
      rag_webhook_url: "http://192.168.0.72:5678/webhook/upload_data_raw"
```

## 5-Minute Setup

### Step 1: Make sure n8n is running ✓

```bash
# Check n8n is accessible
curl http://192.168.0.72:5678/webhook/upload_data_raw
```

### Step 2: Edit mkdocs.yml ✓

```yaml
plugins:
  - llm-autodoc:
      # Your existing config...
      cpp_project_path: '../my-cpp-project'
      llm_provider: 'anthropic'
      # ... etc ...

      # ADD THESE 3 LINES:
      enable_rag_upload: true
      rag_webhook_url: "http://192.168.0.72:5678/webhook/upload_data_raw"
```

### Step 3: Build! ✓

```bash
mkdocs build
```

### Step 4: Watch the magic ✨

```
INFO - ✓ RAG upload enabled
INFO - Generating documentation...
INFO - 📤 Uploading to RAG...

=======================================================================
✅ DOCUMENTATION GENERATION COMPLETE!
   Total documentation files generated: 128

📤 RAG UPLOAD SUMMARY:
   Source files uploaded: 347  # All Python, C++, Markdown, YAML, etc.
   Documentation files uploaded: 128
   Total uploaded: 475
=======================================================================
```

### Step 5: Query your RAG! 🎯

Now you can ask about **any file** in your project:

```
"What does the ThreadPool class do?"
"Show me http_client.cpp implementation"
"Explain the Python setup script"
"What's in the mkdocs.yml configuration?"
"How does the RAG uploader work?"
```

## Done! 🎉

That's it! Every time you run `mkdocs build` or `mkdocs serve`, **ALL your project files** (source code, documentation, configs, scripts, etc.) are automatically uploaded to RAG. The n8n service intelligently handles each file type.

## What Gets Uploaded

### ALL project files get uploaded by default:
- ✅ **Source code**: `.cpp`, `.h`, `.hpp`, `.py`, `.js`, `.java`, etc.
- ✅ **Documentation**: `.md`, `.txt`, `.rst`
- ✅ **Configuration**: `.yml`, `.yaml`, `.json`, `.toml`
- ✅ **Any other text files** in your project
- ✅ Generated overview, module, and API documentation

### The n8n service decides what to do with each file type
The plugin uploads everything and lets your RAG system intelligently handle each file type based on its extension.

### Metadata included:
- File name and path
- File type/extension
- Content type (source_code or documentation)
- Project name
- Source file links (for docs)

## Common Configurations

### Upload only documentation (not source):

```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: true
      rag_upload_all_source: false    # Don't upload all project files
      rag_upload_source_files: false  # Don't upload processed source files
      rag_upload_generated_docs: true # Only upload generated .md
```

### Upload only C++ files (not Python, Markdown, etc.):

```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: true
      rag_upload_all_source: false    # Disable uploading all files
      rag_upload_source_files: true   # Upload only processed C++ files
      include_patterns: ['**/*.h', '**/*.hpp', '**/*.cpp']  # Only C++ files
```

### Use environment variable instead:

**Create `.env` file**:
```bash
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data_raw
```

**mkdocs.yml**:
```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: true
      # rag_webhook_url loaded from .env automatically!
```

### Disable RAG upload temporarily:

```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: false  # Just set to false
```

### Control which file types are uploaded:

Use `include_patterns` and `exclude_patterns` to control what gets uploaded:

```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: true
      rag_upload_all_source: true
      # Include only specific file types
      include_patterns:
        - '**/*.py'
        - '**/*.md'
        - '**/*.cpp'
        - '**/*.h'
      # Exclude build artifacts and dependencies
      exclude_patterns:
        - '**/build/**'
        - '**/node_modules/**'
        - '**/__pycache__/**'
        - '**/.git/**'
```

## Troubleshooting

### "RAG upload disabled: N8N_WEBHOOK_URL not configured"

**Fix**: Add webhook URL to mkdocs.yml or create `.env` file

---

### No files uploaded (count shows 0)

**Fix**:
- Check n8n is running
- Check webhook URL is correct
- Check n8n workflow is activated

---

### Build completes but RAG shows no new files

**Fix**:
- Check n8n execution log
- Verify n8n workflow matches Option B format
- Test webhook with curl

---

## Testing

Quick test without full build:

```bash
# Test webhook connectivity
curl -X POST http://192.168.0.72:5678/webhook/upload_data_raw \
  -H "Content-Type: application/json" \
  -d '{"file_name":"test.cpp","file_type":".cpp","content":"//test"}'
```

## FAQ

**Q: Does it really upload ALL file types?**
A: Yes! By default, it uploads Python, C++, Markdown, JSON, YAML, and any other text files in your project. The n8n service then decides how to handle each file type based on its extension.

**Q: What if I only want to upload C++ files like before?**
A: Set `rag_upload_all_source: false` and configure `include_patterns: ['**/*.cpp', '**/*.h', '**/*.hpp']`

**Q: Will this slow down my build?**
A: Minimal impact (<5-10% overhead depending on project size). Uploads happen after documentation generation.

**Q: What if n8n is down?**
A: Build continues normally. Failed uploads are logged but don't stop the build.

**Q: Can I see what was uploaded?**
A: Yes! Check the build output summary for upload statistics and n8n execution log for details.

**Q: Does this work with mkdocs serve?**
A: Yes! Every rebuild uploads automatically during development.

**Q: Can I exclude certain file types?**
A: Yes! Use `exclude_patterns` to exclude specific paths or file types.

**Q: Can I upload to multiple RAG systems?**
A: Not currently with a single config, but you can modify the code or run multiple builds.

## Next Steps

1. ✅ Enable RAG upload in mkdocs.yml
2. ✅ Run `mkdocs build`
3. ✅ Check upload statistics in output
4. ✅ Query your RAG system
5. 🎉 Enjoy automatic sync!

## Full Documentation

- `RAG_INTEGRATION.md` - Complete guide
- `RAG_PLUGIN_INTEGRATION_SUMMARY.md` - Implementation details
- `OPTION_B_SETUP.md` - n8n workflow setup

---

**That's it! You're now automatically syncing your code and docs to RAG.** 🚀

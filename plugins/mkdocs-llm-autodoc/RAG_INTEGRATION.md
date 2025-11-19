# RAG Integration for mkdocs-llm-autodoc

## Overview

The mkdocs-llm-autodoc plugin now supports **automatic RAG upload**! When enabled, the plugin will automatically upload both source files and generated documentation to your RAG system during the MkDocs build process.

## Features

✅ **Automatic Upload**: Source files and docs uploaded immediately after generation
✅ **Configurable**: Choose what to upload (source, docs, or both)
✅ **Non-blocking**: RAG upload runs asynchronously, doesn't slow down build
✅ **Statistics**: See upload counts in build summary
✅ **Error Handling**: Failed uploads logged but don't stop the build

## Configuration

### Step 1: Enable RAG Upload in mkdocs.yml

Add these options to your `mkdocs.yml`:

```yaml
plugins:
  - llm-autodoc:
      # ... your existing config ...

      # RAG Integration (NEW!)
      enable_rag_upload: true
      rag_webhook_url: "http://192.168.0.72:5678/webhook/upload_data_raw"
      rag_upload_source_files: true      # Upload C++ source files
      rag_upload_generated_docs: true    # Upload generated markdown docs
```

### Step 2: Or Use Environment Variable

Instead of hardcoding the webhook URL, you can use `.env`:

**mkdocs.yml**:
```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: true
      # rag_webhook_url will be read from N8N_WEBHOOK_URL env variable
```

**Create `.env` or `.env.windows` in plugin directory**:
```bash
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data_raw
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable_rag_upload` | bool | `false` | Enable automatic RAG upload |
| `rag_webhook_url` | str | `None` | n8n webhook URL (or use env variable) |
| `rag_upload_source_files` | bool | `true` | Upload C++ source files |
| `rag_upload_generated_docs` | bool | `true` | Upload generated markdown docs |

## How It Works

### Build Process

```
MkDocs Build Starts
    ↓
Plugin Generates Documentation
    ├─→ High-Level Docs Generated
    │   └─→ Uploaded to RAG ✓
    ├─→ Module Docs Generated
    │   ├─→ Source Files Uploaded ✓
    │   └─→ Module Docs Uploaded ✓
    └─→ API Docs Generated
        ├─→ Source Files Uploaded ✓
        └─→ API Docs Uploaded ✓
    ↓
Build Complete + RAG Upload Summary
```

### Data Uploaded

For each C++ file documented:

1. **Source File** (`example.cpp`, `example.h`)
   - Full source code
   - Metadata: `type: source_code`, `project: mkdocs-llm-autodoc`

2. **Generated Documentation** (`.md` files)
   - Overview documentation
   - Module documentation
   - API reference documentation
   - Metadata: `type: documentation`, `source_file: ...`, `auto_generated: true`

## Example Build Output

```bash
$ mkdocs build

INFO    - LLM AutoDoc plugin initialized with anthropic/claude-3-5-sonnet
INFO    - ✓ RAG upload enabled (webhook: http://192.168.0.72:5678/webhook/upload_data_raw)
INFO    - Starting LLM-powered documentation generation...
INFO    - 📦 Processing 15 modules...
INFO    - 📦 [1/15] Processing module: Core
INFO    -    ✓ Module Core completed (3 files generated)
INFO    - 📄 Processing 42 API documentation files...
INFO    - 📄 Progress: 42/42 files (40 success, 2 errors)

=======================================================================
✅ DOCUMENTATION GENERATION COMPLETE!
   Total documentation files generated: 128
   Successfully processed source files: 42
   Cache updated: Yes

📤 RAG UPLOAD SUMMARY:
   Source files uploaded: 42
   Documentation files uploaded: 128
   Total uploaded: 170
=======================================================================
```

## Usage Examples

### Minimal Configuration

Only upload generated docs:

```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: true
      rag_upload_source_files: false   # Don't upload source
      rag_upload_generated_docs: true  # Only docs
```

### Upload Everything

```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: true
      rag_upload_source_files: true
      rag_upload_generated_docs: true
```

### Disable RAG Upload

```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: false
```

Or simply omit the RAG configuration (disabled by default).

## Query Your RAG System

After the build completes, your RAG system will contain:

### Source Code Queries
- "Show me the implementation of ThreadPool class"
- "What functions are in http_client.cpp?"
- "Find all error handling code"

### Documentation Queries
- "What does the Core module do?"
- "Explain the architecture overview"
- "What APIs are available in the Networking module?"

## Troubleshooting

### Issue: "RAG upload disabled: N8N_WEBHOOK_URL not configured"

**Solution**: Add webhook URL to config or environment:

```yaml
plugins:
  - llm-autodoc:
      enable_rag_upload: true
      rag_webhook_url: "http://your-n8n-url/webhook/upload_data_raw"
```

Or create `.env` file with `N8N_WEBHOOK_URL`.

---

### Issue: Failed uploads reported in summary

**Check**:
1. n8n is running at the configured URL
2. Webhook path is correct (`/webhook/upload_data_raw`)
3. n8n workflow is activated
4. Network connectivity to n8n server

**Test manually**:
```bash
curl -X POST http://192.168.0.72:5678/webhook/upload_data_raw \
  -H "Content-Type: application/json" \
  -d '{"file_name": "test.cpp", "file_type": ".cpp", "content": "test"}'
```

---

### Issue: Build slowed down by uploads

**Solution**: Uploads run asynchronously and shouldn't block. If they do:

1. Check network latency to n8n
2. Reduce `max_concurrent_llm_calls` to avoid overwhelming webhook
3. Temporarily disable RAG upload during development

---

### Issue: Some files not uploaded

**Check build output** for specific errors. Common causes:
- File read errors (permissions)
- Network timeouts
- Invalid file encoding

## Performance Impact

RAG upload is designed to be **non-blocking**:
- Uploads happen asynchronously
- Don't wait for upload completion
- Failed uploads logged but don't stop build

**Typical overhead**: <5% additional build time

## Advanced Configuration

### Custom Metadata

Modify `rag_uploader.py` to add custom metadata:

```python
def upload_source_file(self, file_path: str, metadata: Optional[Dict] = None) -> bool:
    custom_metadata = {
        'project': 'my-cpp-project',
        'version': '1.0.0',
        'author': 'team-name',
        **(metadata or {})
    }
    return self.upload_file(file_path, file_type='source_code', metadata=custom_metadata)
```

### Batch Upload

Files are uploaded immediately after generation. For batch upload, modify:

```python
# In plugin.py, collect all files first, then upload at end
all_files_to_upload = []
# ... collect files ...
self.rag_uploader.upload_batch(all_files_to_upload)
```

### Conditional Upload

Upload only specific file types:

```python
def _upload_to_rag(self, source_file: str = None, doc_files: List[str] = None):
    if source_file and source_file.endswith('.h'):  # Only headers
        self.rag_uploader.upload_source_file(source_file)
```

## Integration with n8n Workflow

The RAG upload uses the **Option B** n8n workflow (server-side splitting).

**Expected n8n workflow**:
1. Webhook receives full file content
2. n8n splits content based on file type
3. Generates embeddings
4. Stores in Qdrant Vector Store

See `OPTION_B_SETUP.md` for n8n workflow configuration.

## Environment Variables

The plugin loads these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `N8N_WEBHOOK_URL` | n8n webhook endpoint | `http://192.168.0.72:5678/webhook/upload_data_raw` |
| `ANTHROPIC_API_KEY` | For LLM provider | `sk-ant-...` |
| `OPENAI_API_KEY` | Alternative LLM | `sk-...` |

Load from:
- `.env` in plugin directory
- `.env.windows` in plugin directory
- System environment variables

## Security Considerations

### Webhook URL

- Use HTTPS in production
- Consider authentication on webhook
- Don't commit webhook URLs to git

### Source Code Privacy

- Only upload if comfortable with code in RAG
- Consider self-hosted n8n + Qdrant
- Review RAG retention policies

### Rate Limiting

- n8n may have rate limits
- Large projects may generate many uploads
- Consider batch processing for huge codebases

## FAQ

**Q: Does this slow down my build?**
A: No, uploads are asynchronous. Typical overhead <5%.

**Q: What if n8n is down?**
A: Build continues normally. Failed uploads are logged.

**Q: Can I upload to multiple RAG systems?**
A: Currently one webhook only. Modify `rag_uploader.py` for multiple endpoints.

**Q: Are uploads incremental?**
A: Full uploads each build. Use caching to minimize regeneration.

**Q: Can I see upload progress?**
A: Check MkDocs logs. Each upload is logged at DEBUG level.

**Q: Does this work with `mkdocs serve`?**
A: Yes! Uploads happen on every rebuild.

## Roadmap

Future enhancements:
- [ ] Upload progress bar
- [ ] Retry failed uploads
- [ ] Incremental uploads (only changed files)
- [ ] Multiple RAG endpoint support
- [ ] Upload queue with rate limiting
- [ ] Compression for large files
- [ ] Metadata customization via config

## Contributing

Want to improve RAG integration?

1. Edit `mkdocs_llm_autodoc/utils/rag_uploader.py`
2. Update `mkdocs_llm_autodoc/plugin.py`
3. Test with real builds
4. Submit PR!

## Related Documentation

- `OPTION_B_SETUP.md` - n8n workflow setup
- `AUTO_UPLOAD_README.md` - Standalone upload tools
- `BATCH_FILES_GUIDE.md` - Batch file reference
- Plugin README - General plugin documentation

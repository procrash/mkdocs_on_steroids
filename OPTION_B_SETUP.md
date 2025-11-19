# Option B: Server-Side Language-Aware Splitting

## Overview

With Option B, Python sends the FULL file content to n8n, and n8n handles language-aware chunking based on file type.

## Benefits

- Centralized splitting logic in n8n
- No need to maintain Python splitting code
- Easy to adjust chunk sizes without code changes
- Language-specific splitting for better context preservation

## Architecture

```
Python Script
    ↓
Sends FULL file content + metadata
    ↓
n8n Webhook
    ↓
Extract Data (Code Node)
    ↓
Switch by File Type
    ├─→ .md files → Markdown Splitter → Qdrant
    ├─→ .cpp/.h files → C++ Splitter → Qdrant
    ├─→ .py files → Python Splitter → Qdrant
    ├─→ .js files → JavaScript Splitter → Qdrant
    ├─→ .html files → HTML Splitter → Qdrant
    └─→ Other files → Default Splitter → Qdrant
         ↑ (all use same Embeddings OpenAI)
```

## Workflow Structure

### Node Layout

1. **Webhook - Python Upload**: Receives file content
2. **Extract Data**: Prepares data for routing
3. **Switch by File Type**: Routes based on file extension
4. **6 parallel branches**, each with:
   - Language-specific Text Splitter
   - Data Loader (JSON mode)
   - Qdrant Vector Store node
5. **Embeddings OpenAI**: Shared across all branches

### Data Flow

```json
Python sends:
{
  "file_name": "example.cpp",
  "file_path": "Z:\\path\\to\\example.cpp",
  "file_type": ".cpp",
  "content": "#include <iostream>...",  // FULL content
  "metadata": {
    "chunk_size": 1000,
    "chunk_overlap": 200
  }
}

Extract Data outputs:
{
  "content": "#include <iostream>...",
  "file_name": "example.cpp",
  "file_path": "Z:\\path\\to\\example.cpp",
  "file_type": ".cpp",
  "chunk_size": 1000,
  "chunk_overlap": 200,
  "metadata": {...}
}

Switch routes to C++ branch based on file_type

C++ Splitter:
- Uses splitCode: "cpp"
- chunkSize: {{ $json.chunk_size }}
- chunkOverlap: {{ $json.chunk_overlap }}

Splits into language-aware chunks

Data Loader converts to LangChain Documents

Embeddings generates vectors

Qdrant stores in "test-collection"
```

## Changes Made

### 1. Python Script Changes

**File**: `document_uploader.py`

**Changed**:
- `upload_chunks()` → `upload_content()`
- Now sends `content` field instead of `chunks` array
- Chunk config passed in metadata for n8n to use

**Old format**:
```python
payload = {
    'chunks': ['chunk1', 'chunk2', ...],
    'total_chunks': 5,
    ...
}
```

**New format**:
```python
payload = {
    'content': 'full file content here...',
    'metadata': {
        'chunk_size': 1000,
        'chunk_overlap': 200
    },
    ...
}
```

### 2. n8n Workflow

**File**: `RAG_option_b_with_switch.json`

**Structure**:
- 1 Webhook node
- 1 Extract Data code node
- 1 Switch node (routes to 6 outputs)
- 6 Text Splitter nodes (one per file type)
- 6 Data Loader nodes
- 6 Qdrant Vector Store nodes
- 1 Embeddings OpenAI node (shared)

## Supported File Types

| Extension | Splitter Type | Description |
|-----------|---------------|-------------|
| .md, .markdown | Markdown | Preserves markdown structure |
| .cpp, .cc, .cxx, .h, .hpp | C++ | Language-aware C++ splitting |
| .py | Python | Language-aware Python splitting |
| .js, .jsx | JavaScript | Language-aware JS splitting |
| .html, .htm | HTML | HTML structure-aware |
| Others | Default | Generic recursive text splitter |

## Installation Steps

### Step 1: Update Python Script

The `document_uploader.py` has already been updated. No action needed.

### Step 2: Import n8n Workflow

1. Open n8n at `http://192.168.0.72:5678`
2. Create a new workflow or open existing RAG workflow
3. Import `RAG_option_b_with_switch.json`

**OR** manually create the nodes following the structure in the JSON.

### Step 3: Configure Qdrant Credentials

For each of the 6 Qdrant nodes:
- Click on the node
- Set Collection: `test-collection`
- Set Mode: `insert`
- Configure Qdrant credentials (should auto-fill if already set)

### Step 4: Configure OpenAI Credentials

For the Embeddings OpenAI node:
- Model: `text-embedding-qwen3-embedding-8b` (or your preferred model)
- Set OpenAI API credentials

### Step 5: Verify Connections

Ensure these connections exist:

**Main flow**:
1. Webhook → Extract Data (main)
2. Extract Data → Switch (main)
3. Switch → 6 Qdrant nodes (one per output: markdown, cpp, python, javascript, html, fallback)

**Sub-nodes for each branch** (example for Markdown):
- Splitter - Markdown → Data Loader - Markdown (ai_textSplitter)
- Data Loader - Markdown → Qdrant - Markdown (ai_document)
- Embeddings OpenAI → Qdrant - Markdown (ai_embedding)

Repeat for all 6 branches!

### Step 6: Activate Workflow

1. Save the workflow
2. Toggle to "Active" (top right)
3. Webhook URL will be: `http://192.168.0.72:5678/webhook/upload_data_raw`

## Testing

### Test 1: Quick Test

```cmd
test_webhook_only.bat
```

This will fail with the old test script because it's sending the old format. We need to update it.

### Test 2: Full Document Upload

```cmd
test_upload.bat
```

This should work correctly now, sending full file content.

### Test 3: Check n8n Execution Log

1. Go to n8n
2. Check execution log
3. You should see:
   - ✅ Webhook received data
   - ✅ Extract Data processed
   - ✅ Switch routed correctly (e.g., to "cpp" output for .cpp files)
   - ✅ Correct splitter was used
   - ✅ Data Loader created documents
   - ✅ Embeddings generated
   - ✅ Qdrant stored vectors

### Test 4: Verify in Qdrant

Check your Qdrant collection to see:
- Documents are chunked appropriately
- Metadata includes file_name, file_path, etc.
- All file types end up in "test-collection"

## Troubleshooting

### Issue: Switch doesn't route correctly

**Check**:
- Switch conditions are correct (case-sensitive!)
- File type includes the dot (e.g., ".cpp" not "cpp")
- Fallback output is enabled

### Issue: Splitter not using correct language

**Check**:
- Splitter node has `options.splitCode` set correctly
- Values: "markdown", "cpp", "python", "js", "html"
- Check n8n execution log to see which splitter was triggered

### Issue: Chunk size not being used

**Check**:
- Splitter nodes use: `={{ $json.chunk_size }}`
- Extract Data node outputs chunk_size field
- Python script sends chunk_size in metadata

### Issue: No embeddings generated

**Check**:
- Embeddings node is connected to ALL 6 Qdrant nodes
- Connection type is `ai_embedding` (not main)
- OpenAI credentials are configured

### Issue: Multiple Qdrant nodes confusing

**Explanation**:
- All 6 Qdrant nodes write to the SAME collection
- They're separate nodes because each needs its own Data Loader
- All data ends up in "test-collection"

## Adding More File Types

To add support for new file types:

### Step 1: Add to Switch Node

Add a new rule:
```json
{
  "conditions": {
    "conditions": [
      {
        "leftValue": "={{ $json.file_type }}",
        "rightValue": ".rs",  // Rust files
        "operator": {"type": "string", "operation": "equals"}
      }
    ]
  },
  "outputKey": "rust"
}
```

### Step 2: Add Splitter Node

Create new "Splitter - Rust":
- Type: Recursive Character Text Splitter
- chunkSize: `={{ $json.chunk_size }}`
- chunkOverlap: `={{ $json.chunk_overlap }}`
- options.splitCode: "rust"

### Step 3: Add Data Loader Node

Create new "Data Loader - Rust":
- Type: Default Data Loader
- dataType: "json"
- jsonProperty: "content"

### Step 4: Add Qdrant Node

Create new "Qdrant - Rust":
- Mode: insert
- Collection: test-collection

### Step 5: Connect Everything

- Switch → Qdrant - Rust (main, from "rust" output)
- Splitter - Rust → Data Loader - Rust (ai_textSplitter)
- Data Loader - Rust → Qdrant - Rust (ai_document)
- Embeddings OpenAI → Qdrant - Rust (ai_embedding)

## Available Split Codes in n8n

Based on LangChain's RecursiveCharacterTextSplitter:

- `cpp` - C++
- `go` - Go
- `java` - Java
- `js` - JavaScript
- `php` - PHP
- `proto` - Protocol Buffers
- `python` - Python
- `rst` - reStructuredText
- `ruby` - Ruby
- `rust` - Rust
- `scala` - Scala
- `swift` - Swift
- `markdown` - Markdown
- `latex` - LaTeX
- `html` - HTML
- `sol` - Solidity

Check n8n's text splitter node for the full list!

## Comparison: Option A vs Option B

| Feature | Option A (Python Splits) | Option B (n8n Splits) |
|---------|-------------------------|----------------------|
| Splitting logic | In Python | In n8n |
| Chunk size changes | Requires Python restart | Change in n8n UI |
| Language support | Hardcoded in Python | Configured in n8n |
| Network payload | Smaller (pre-split) | Larger (full content) |
| Debugging | Check Python logs | Check n8n execution log |
| Maintenance | Update Python code | Update n8n workflow |
| Flexibility | Less flexible | More flexible |

## Next Steps

1. Import `RAG_option_b_with_switch.json` into n8n
2. Configure all credentials
3. Verify all connections are correct
4. Activate the workflow
5. Run `test_upload.bat`
6. Check n8n execution log
7. Verify documents in Qdrant
8. Add more file types as needed!

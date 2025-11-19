# Python Document Uploader - n8n Integration Setup

## Problem Identified

Your current workflow has a broken connection:
- `Webhook1` (`/webhook/upload_data`) connects directly to Qdrant Vector Store
- **It skips both the Default Data Loader AND Embeddings OpenAI**
- This is why Python uploads only trigger the default data loader but not embeddings!

## Solution: New Dedicated Webhook

I've created a new workflow configuration that adds a proper Python upload webhook with the correct flow.

## New Workflow Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your n8n RAG Workflow                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [1] Form Upload (existing, working)                            │
│  ┌───────────────────────────────────────────────────┐          │
│  │ Form Trigger                                      │          │
│  │    ↓                                              │          │
│  │ [Default Data Loader] ──→ [Qdrant Vector Store]  │          │
│  │                              ↑                    │          │
│  │                              │                    │          │
│  │                        [Embeddings OpenAI]        │          │
│  └───────────────────────────────────────────────────┘          │
│                                                                  │
│  [2] Python Upload (NEW - properly connected)                   │
│  ┌───────────────────────────────────────────────────┐          │
│  │ Webhook: /webhook/upload_data_raw                 │          │
│  │    ↓                                              │          │
│  │ Code: Extract Chunks from Python                  │          │
│  │    ↓                                              │          │
│  │ Data Loader for Python Chunks ──→ [Qdrant]       │          │
│  │                                      ↑            │          │
│  │                                      │            │          │
│  │                              [Embeddings OpenAI]  │          │
│  └───────────────────────────────────────────────────┘          │
│                                                                  │
│  [3] Chat Interface (existing, for queries)                     │
│  ┌───────────────────────────────────────────────────┐          │
│  │ Chat Trigger → AI Agent ← [Qdrant Retrieval]     │          │
│  │                    ↑                              │          │
│  │              [OpenAI Chat Model]                  │          │
│  └───────────────────────────────────────────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## What Changed

### New Nodes Added:

1. **Webhook - Python Upload** (id: `new-webhook-python-upload`)
   - Path: `/webhook/upload_data_raw`
   - Method: POST
   - Accepts the Python script's JSON format

2. **Extract Chunks from Python** (Code node)
   - Parses the Python uploader payload
   - Extracts chunks array
   - Formats data for LangChain (uses `pageContent` field)
   - Preserves metadata (file_name, file_path, chunk_index, etc.)

3. **Data Loader for Python Chunks**
   - Type: Default Data Loader (JSON mode)
   - Reads from `pageContent` field
   - Converts chunks to LangChain Document format

### Connection Flow:

```
Python Script
    ↓
Webhook (/webhook/upload_data_raw)
    ↓
Extract Chunks (Code Node)
    ↓
Data Loader for Python Chunks
    ↓ (ai_document connection)
Qdrant Vector Store ← (ai_embedding) ← Embeddings OpenAI
```

## Installation Steps

### Step 1: Import the New Workflow

1. Open n8n at `http://192.168.0.72:5678`
2. Go to your RAG workflow
3. Click the "⋮" menu → "Import from File"
4. Select `RAG_with_python_uploader.json`
5. Or manually copy the workflow and paste in n8n

### Step 2: Update the Code Node

The "Extract Chunks from Python" node contains this JavaScript:

```javascript
// Extract chunks from Python uploader payload
const body = $input.first().json.body;

if (!body || !body.chunks || !Array.isArray(body.chunks)) {
  throw new Error('Invalid payload: chunks array required');
}

const chunks = body.chunks;
const fileName = body.file_name || 'unknown';
const filePath = body.file_path || '';
const fileType = body.file_type || '';
const totalChunks = body.total_chunks || chunks.length;
const metadata = body.metadata || {};

// Create one output item per chunk
const outputItems = chunks.map((chunkText, index) => ({
  json: {
    pageContent: chunkText,  // LangChain expects 'pageContent' field
    metadata: {
      file_name: fileName,
      file_path: filePath,
      file_type: fileType,
      chunk_index: index,
      total_chunks: totalChunks,
      source: filePath,
      ...metadata
    }
  }
}));

return outputItems;
```

### Step 3: Configure Data Loader Node

Settings for "Data Loader for Python Chunks":
- **Data Type**: `JSON` (not binary!)
- **JSON Property**: `pageContent`
- Leave other options as default

### Step 4: Verify Connections

Make sure these connections exist:
1. Webhook → Extract Chunks (main)
2. Extract Chunks → Data Loader (main)
3. Data Loader → Qdrant Vector Store (ai_document)
4. Embeddings OpenAI → Qdrant Vector Store (ai_embedding)

### Step 5: Activate Webhook

1. Save the workflow
2. Toggle the workflow to "Active" (top right)
3. The new webhook will be available at:
   ```
   http://192.168.0.72:5678/webhook/upload_data_raw
   ```

## Update Python Configuration

### Option 1: Update .env File

Edit `.env.windows` or `.env`:

```bash
# Python script upload endpoint (with embeddings)
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data_raw

# Old endpoint (broken - skips embeddings)
# N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data
```

### Option 2: Keep Both Endpoints

If you want to keep both:

```bash
# Form-based upload
N8N_WEBHOOK_URL_FORM=http://192.168.0.72:5678/webhook/upload_data

# Python script upload
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data_raw
```

## Testing

### Test 1: Simple cURL Test

```bash
curl -X POST http://192.168.0.72:5678/webhook/upload_data_raw \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "test.txt",
    "file_path": "test.txt",
    "file_type": ".txt",
    "total_chunks": 2,
    "chunks": [
      "This is the first chunk of text.",
      "This is the second chunk of text."
    ],
    "metadata": {
      "test": true
    }
  }'
```

### Test 2: Run test_upload.bat

```cmd
test_upload.bat
```

Watch the n8n execution log - you should see:
1. Webhook receives data ✓
2. Extract Chunks processes the array ✓
3. Data Loader converts to documents ✓
4. Embeddings OpenAI generates embeddings ✓
5. Qdrant stores the vectors ✓

### Test 3: Verify in Qdrant

Check your Qdrant collection to confirm:
- Documents are being stored
- Embeddings exist
- Metadata is preserved (file_name, chunk_index, etc.)

## Troubleshooting

### Issue: Webhook returns 404
**Solution**:
- Ensure workflow is activated (toggle in top right)
- Check webhook path is exactly `upload_data_raw`
- Restart n8n if needed

### Issue: "chunks array required" error
**Solution**:
- Check your Python script is sending the correct format
- Verify the payload has a `chunks` field that's an array
- Look at the webhook input in n8n execution log

### Issue: No embeddings generated
**Solution**:
- Verify OpenAI credentials are configured
- Check the connection from Embeddings node to Qdrant
- Ensure it's an `ai_embedding` type connection (not `main`)

### Issue: Data Loader fails
**Solution**:
- Ensure Data Loader is set to "JSON" mode (not "binary")
- Verify JSON Property is set to `pageContent`
- Check the Code node is outputting the correct format

### Issue: Documents stored but no metadata
**Solution**:
- Check the metadata mapping in Qdrant Vector Store node
- Ensure the Code node is including metadata in the output
- Verify Qdrant collection schema supports metadata

## Data Format Reference

### Python Script Sends:
```json
{
  "file_name": "document.cpp",
  "file_path": "Z:\\path\\to\\document.cpp",
  "file_type": ".cpp",
  "total_chunks": 5,
  "chunks": [
    "chunk text 1...",
    "chunk text 2...",
    "..."
  ],
  "metadata": {}
}
```

### After Extract Chunks Node:
```json
[
  {
    "pageContent": "chunk text 1...",
    "metadata": {
      "file_name": "document.cpp",
      "file_path": "Z:\\path\\to\\document.cpp",
      "file_type": ".cpp",
      "chunk_index": 0,
      "total_chunks": 5,
      "source": "Z:\\path\\to\\document.cpp"
    }
  },
  {
    "pageContent": "chunk text 2...",
    "metadata": {
      "file_name": "document.cpp",
      "chunk_index": 1,
      ...
    }
  }
]
```

### After Data Loader → Stored in Qdrant:
Each chunk becomes a vector with:
- **Vector**: Generated by Embeddings OpenAI
- **Payload**: Contains metadata + pageContent
- **ID**: Auto-generated by Qdrant

## Comparison: Old vs New

| Feature | Old Webhook | New Webhook |
|---------|-------------|-------------|
| Path | `/webhook/upload_data` | `/webhook/upload_data_raw` |
| Data Loader | ❌ Skipped | ✅ Included |
| Embeddings | ❌ Skipped | ✅ Included |
| Chunk Processing | ❌ None | ✅ Proper loop |
| Metadata | ❌ Lost | ✅ Preserved |
| Works with Python | ❌ Partially | ✅ Fully |

## Next Steps

1. Import the new workflow JSON
2. Update `.env.windows` with new URL
3. Test with `test_upload.bat`
4. Verify embeddings in Qdrant
5. Deactivate or delete the old broken webhook

## Questions?

If you encounter issues:
1. Check the n8n execution log for the workflow
2. Verify the webhook input data format
3. Check each node's output in the execution view
4. Ensure credentials are configured correctly

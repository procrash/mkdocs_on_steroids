# Manual n8n Workflow Setup - Python Upload Endpoint

Since the JSON import might not connect nodes properly, here are step-by-step manual instructions.

## Step 1: Open Your RAG Workflow in n8n

1. Go to `http://192.168.0.72:5678`
2. Open your existing "RAG" workflow
3. We'll add 3 new nodes to it

## Step 2: Add Webhook Node

1. Click "+" to add a new node
2. Search for "Webhook"
3. Configure:
   - **HTTP Method**: POST
   - **Path**: `upload_data_raw`
   - **Authentication**: None
   - **Response Mode**: "Last Node"
4. **Position it** on the left side of your canvas
5. **Name it**: "Webhook - Python Upload"

## Step 3: Add Code Node (Extract Chunks)

1. Click "+" after the webhook
2. Search for "Code"
3. Select "Code" node
4. Configure:
   - **Mode**: "Run Once for All Items"
   - **Language**: JavaScript
5. **Paste this code**:

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

6. **Name it**: "Extract Chunks from Python"

## Step 4: Add Default Data Loader Node

1. Click "+" after the Code node
2. Search for "Default Data Loader"
3. Select "@n8n/n8n-nodes-langchain.documentDefaultDataLoader"
4. Configure:
   - **Data Type**: JSON (NOT Binary!)
   - **JSON Property**: `pageContent`
   - Leave other options as default
5. **Name it**: "Data Loader for Python Chunks"

## Step 5: Connect to Existing Embeddings and Qdrant

Now connect your new nodes to the existing workflow:

### Connection 1: Webhook → Code
- Drag from "Webhook - Python Upload" output
- Connect to "Extract Chunks from Python" input
- This should be a **main** (gray) connection

### Connection 2: Code → Data Loader
- Drag from "Extract Chunks from Python" output
- Connect to "Data Loader for Python Chunks" input
- This should be a **main** (gray) connection

### Connection 3: Data Loader → Qdrant Vector Store
- Drag from "Data Loader for Python Chunks" output circle (right side)
- Connect to "Qdrant Vector Store" **ai_document** input (left side)
- This should be a **purple** connection (ai_document type)
- **IMPORTANT**: Connect to the same "Qdrant Vector Store" node that's used by the form upload

### Connection 4: Embeddings → Qdrant (should already exist)
- Your "Embeddings OpenAI" should already be connected to "Qdrant Vector Store"
- If not, connect "Embeddings OpenAI" → "Qdrant Vector Store" (ai_embedding connection, blue/purple)

## Step 6: Verify Connections

Your workflow should now look like this:

```
NEW Python Upload Path:
┌─────────────────────────────────────────────────────┐
│ Webhook - Python Upload                            │
│    ↓ (main)                                         │
│ Extract Chunks from Python                          │
│    ↓ (main)                                         │
│ Data Loader for Python Chunks                       │
│    ↓ (ai_document - purple)                         │
│    └──→ Qdrant Vector Store ←── (ai_embedding) ─┐  │
│                                                   │  │
│                            Embeddings OpenAI ─────┘  │
└─────────────────────────────────────────────────────┘

EXISTING Form Upload Path (unchanged):
┌─────────────────────────────────────────────────────┐
│ Upload your file here (Form Trigger)                │
│    ↓ (main)                                         │
│ Qdrant Vector Store                                 │
│    ↑ (ai_document)         ↑ (ai_embedding)         │
│    │                       │                        │
│ Default Data Loader    Embeddings OpenAI            │
└─────────────────────────────────────────────────────┘
```

## Step 7: Activate and Test

1. **Save** the workflow
2. **Activate** the workflow (toggle in top right)
3. Run the test:
   ```cmd
   test_webhook_only.bat
   ```

## Troubleshooting Connection Issues

### If connections aren't working:

**Check connection types:**
- Webhook → Code = **main** (gray line)
- Code → Data Loader = **main** (gray line)
- Data Loader → Qdrant = **ai_document** (purple line)
- Embeddings → Qdrant = **ai_embedding** (blue/purple line)

**To make an ai_document connection:**
1. Look for a small circle on the RIGHT side of "Data Loader for Python Chunks"
2. Drag from that circle to the LEFT side of "Qdrant Vector Store"
3. It should show as a purple/pink line labeled "ai_document"

**To make an ai_embedding connection:**
1. Look for a small circle on the RIGHT side of "Embeddings OpenAI"
2. Drag from that circle to the LEFT side of "Qdrant Vector Store"
3. It should show as a blue/purple line labeled "ai_embedding"

### Common Issues:

**Issue**: "Data Loader has no output"
- Make sure Data Type is set to "JSON" not "Binary"
- Verify JSON Property is exactly `pageContent`

**Issue**: "Qdrant doesn't receive documents"
- Check the connection type is "ai_document" (purple), not "main" (gray)
- Both the Data Loader AND Embeddings need to connect to Qdrant

**Issue**: "No embeddings generated"
- Verify "Embeddings OpenAI" is connected to "Qdrant Vector Store"
- Check OpenAI credentials are configured

## Visual Guide: Connection Types

```
main connection (gray):
[Node A] ──────> [Node B]

ai_document connection (purple):
[Data Loader] ━━━━━> [Qdrant]
              (purple)

ai_embedding connection (blue):
[Embeddings] ━━━━━> [Qdrant]
             (blue)
```

## Step 8: Verify in n8n Execution Log

After running `test_webhook_only.bat`, check the execution log:

1. Click on the workflow execution at the bottom
2. You should see:
   - ✅ Webhook - Python Upload (received data)
   - ✅ Extract Chunks from Python (2 items output)
   - ✅ Data Loader for Python Chunks (2 documents)
   - ✅ Embeddings OpenAI (2 embeddings generated)
   - ✅ Qdrant Vector Store (2 vectors stored)

If any step is missing or failed, check that node's configuration and connections.

# n8n Workflow Setup for Python Document Uploader

## Overview

This guide shows how to create a new n8n webhook endpoint specifically for the Python document uploader script, separate from the form-based upload.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     n8n Workflows                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Webhook 1: /webhook/upload_data (Form-based)               │
│  ┌────────────────────────────────────────────────┐         │
│  │ 1. Webhook Trigger                             │         │
│  │ 2. Extract form data                           │         │
│  │ 3. Download file from form                     │         │
│  │ 4. Split/Process file                          │         │
│  │ 5. Generate embeddings                         │         │
│  │ 6. Store in Qdrant Vector Store                │         │
│  └────────────────────────────────────────────────┘         │
│                                                              │
│  Webhook 2: /webhook/upload_data_raw (Python Script)        │
│  ┌────────────────────────────────────────────────┐         │
│  │ 1. Webhook Trigger                             │         │
│  │ 2. Extract chunks from payload                 │         │
│  │ 3. Loop through chunks                         │         │
│  │ 4. Generate embeddings for each chunk          │         │
│  │ 5. Store in Qdrant Vector Store                │         │
│  └────────────────────────────────────────────────┘         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Comparison

### Form-based Webhook (existing)
```json
Input:
[{
  "Upload your file(s)": [{
    "filename": "document.pdf",
    "mimetype": "application/pdf",
    "size": 147689
  }],
  "submittedAt": "2025-11-19T17:06:36.142+01:00",
  "formMode": "test"
}]

Process:
→ Download file
→ Split into chunks
→ Generate embeddings
→ Store in Qdrant
```

### Python Script Webhook (new)
```json
Input:
{
  "file_name": "test.cpp",
  "file_path": "Z:\\mkdocs\\test_documents\\test.cpp",
  "file_type": ".cpp",
  "total_chunks": 5,
  "chunks": [
    "#include <iostream>...",
    "class Example {...",
    "..."
  ],
  "metadata": {}
}

Process:
→ Extract chunks (already split)
→ Generate embeddings
→ Store in Qdrant
```

## Step-by-Step Setup in n8n

### Step 1: Create New Workflow

1. Open n8n at `http://192.168.0.72:5678`
2. Click "Add workflow" (+ button)
3. Name it: "Document Upload - Python Script"

### Step 2: Add Webhook Trigger

1. Click "+ Add first step"
2. Search for "Webhook"
3. Configure:
   - **Webhook Name**: `upload_data_raw`
   - **HTTP Method**: POST
   - **Path**: `upload_data_raw`
   - **Authentication**: None (or set if needed)
   - **Response Mode**: "Respond Immediately"
   - **Response Data**: "First Entry JSON"

Your webhook URL will be: `http://192.168.0.72:5678/webhook/upload_data_raw`

### Step 3: Add Code Node to Extract Chunks

1. Click "+" after webhook node
2. Search for "Code"
3. Name it: "Extract Chunks and Metadata"
4. Select JavaScript
5. Add this code:

```javascript
// Extract data from webhook payload
const data = $input.first().json.body;

// Prepare output items - one for each chunk
const chunks = data.chunks || [];
const outputItems = [];

for (let i = 0; i < chunks.length; i++) {
  outputItems.push({
    json: {
      chunk_index: i,
      chunk_text: chunks[i],
      file_name: data.file_name,
      file_path: data.file_path,
      file_type: data.file_type,
      total_chunks: data.total_chunks,
      metadata: data.metadata || {}
    }
  });
}

return outputItems;
```

### Step 4: Add Embeddings Node

1. Click "+" after Code node
2. Search for "Embeddings OpenAI" (or your embedding provider)
3. Configure:
   - **Input Field**: `chunk_text`
   - **Model**: `text-embedding-3-small` (or your preferred model)
   - **Add your OpenAI API credentials**

Alternative providers:
- Embeddings Cohere
- Embeddings HuggingFace
- Embeddings Azure OpenAI

### Step 5: Add Qdrant Vector Store Node

1. Click "+" after Embeddings node
2. Search for "Qdrant Vector Store"
3. Configure:
   - **Operation**: "Insert Documents"
   - **Qdrant Credentials**: (set up your Qdrant connection)
   - **Collection Name**: Your collection name (e.g., `documents`)
   - **Document Field**: `chunk_text`

4. Add metadata fields:
   - Click "Add Field"
   - Add: `file_name`, `file_path`, `file_type`, `chunk_index`, `total_chunks`

### Step 6: Add Response Node (Optional)

1. Click "+" after Qdrant node
2. Search for "Respond to Webhook"
3. Configure:
   - **Response Body**:
   ```json
   {
     "success": true,
     "message": "Successfully processed {{ $json.total_chunks }} chunks",
     "file_name": "{{ $json.file_name }}"
   }
   ```

### Step 7: Activate Workflow

1. Click the toggle in top right to activate
2. Save the workflow

## Alternative: Simplified JSON-based Configuration

If you prefer to import a workflow, here's a simplified n8n workflow JSON you can import:

### Minimal Workflow Structure

```json
{
  "name": "Document Upload - Python Script",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "upload_data_raw",
        "responseMode": "responseNode",
        "options": {}
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [240, 300]
    },
    {
      "parameters": {
        "jsCode": "// See code above in Step 3"
      },
      "name": "Extract Chunks",
      "type": "n8n-nodes-base.code",
      "position": [460, 300]
    },
    {
      "parameters": {
        "modelName": "text-embedding-3-small",
        "options": {}
      },
      "name": "OpenAI Embeddings",
      "type": "@langchain/openai.embeddings",
      "position": [680, 300]
    },
    {
      "parameters": {
        "mode": "insert",
        "collectionName": "documents"
      },
      "name": "Qdrant Vector Store",
      "type": "@langchain/community.vectorstore.qdrant",
      "position": [900, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{"node": "Extract Chunks", "type": "main", "index": 0}]]
    },
    "Extract Chunks": {
      "main": [[{"node": "OpenAI Embeddings", "type": "main", "index": 0}]]
    },
    "OpenAI Embeddings": {
      "main": [[{"node": "Qdrant Vector Store", "type": "main", "index": 0}]]
    }
  }
}
```

## Configuration Updates

### Update .env Files

After creating the new webhook, update your environment files:

**Option A: Keep existing for form, add new for Python script**
```bash
# .env.windows
# Form-based upload (keep existing)
N8N_WEBHOOK_URL_FORM=http://192.168.0.72:5678/webhook/upload_data

# Python script upload (new)
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data_raw
```

**Option B: Use new endpoint only**
```bash
# .env.windows
N8N_WEBHOOK_URL=http://192.168.0.72:5678/webhook/upload_data_raw
```

## Testing

### Test with test_upload.bat

1. Make sure the new webhook is activated in n8n
2. Run: `test_upload.bat`
3. Check n8n execution history to see the workflow run
4. Verify embeddings were created in Qdrant

### Test with curl

```bash
curl -X POST http://192.168.0.72:5678/webhook/upload_data_raw \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "test.cpp",
    "file_path": "test.cpp",
    "file_type": ".cpp",
    "total_chunks": 2,
    "chunks": [
      "#include <iostream>\nint main() { return 0; }",
      "// End of file"
    ],
    "metadata": {}
  }'
```

## Troubleshooting

### Issue: Webhook returns 404
- Check webhook is activated (toggle in top right)
- Verify path is exactly `upload_data_raw`
- Check n8n is running on port 5678

### Issue: No embeddings generated
- Check OpenAI credentials are configured
- Verify the `chunk_text` field is correctly mapped
- Check n8n execution log for errors

### Issue: Qdrant connection fails
- Verify Qdrant credentials in n8n
- Check collection exists
- Verify Qdrant is accessible from n8n server

### Issue: Chunks not processing
- Check the Code node JavaScript syntax
- Verify `data.chunks` is an array
- Look at webhook input data in execution log

## Next Steps

1. Set up the new webhook in n8n following steps above
2. Update `.env.windows` with the new URL
3. Test with `test_upload.bat`
4. Monitor n8n execution logs
5. Verify documents appear in Qdrant

## Comparison with Form Upload

| Feature | Form Upload | Python Script |
|---------|-------------|---------------|
| Endpoint | `/webhook/upload_data` | `/webhook/upload_data_raw` |
| Input | File upload | Pre-split chunks |
| Splitting | Done in n8n | Done in Python |
| Use Case | Manual uploads | Automated batch processing |
| File Size | Limited by form | Can handle large files |
| Preprocessing | Minimal | Full LangChain splitting |

# Correct n8n Setup for Python Upload

## The Key Insight

Looking at your working form upload, the flow is:
```
Form Trigger ──(main)──> Qdrant Vector Store
                           ↑ (ai_document sub-node)
                      Default Data Loader
                           ↑ (ai_embedding sub-node)
                      Embeddings OpenAI
```

The Default Data Loader and Embeddings are **SUB-NODES**, not in the main execution flow!

## The Problem with Our Approach

We can't just add another ai_document sub-node to Qdrant because **it only allows ONE**.

## The Solution: Use Insert Documents Mode Properly

Actually, looking more carefully, I think we need to use the Qdrant node differently. Let me check if the issue is that we're trying to use TWO different entry points into the same Qdrant node.

## Simplest Solution: Separate Qdrant Node for Python Upload

Since Qdrant Vector Store in "insert" mode only allows ONE ai_document input, we have two options:

### Option 1: Create a Second Qdrant Insert Node (Recommended)

Create a completely separate Qdrant Vector Store node just for Python uploads:

```
Python Upload Path:
  Webhook - Python Upload
      ↓ (main)
  Prepare Chunks for Qdrant (Code)
      ↓ (main)
  Qdrant Vector Store - Python Upload (NEW node!)
      ↑ (ai_embedding)
  Embeddings OpenAI (same one used by form)
```

This way:
- Form upload uses "Qdrant Vector Store" (existing)
- Python upload uses "Qdrant Vector Store - Python Upload" (new)
- Both write to the SAME collection ("test-collection")
- Both use the SAME embeddings node

### Option 2: Skip the Data Loader Pattern Entirely

Use Qdrant's ability to accept text directly via the main input:

```
Webhook - Python Upload
    ↓
Code Node (formats as: {text: "...", metadata: {...}})
    ↓
Insert into Qdrant via HTTP Request node or direct API
```

## Recommended Approach: Option 1

Let me create the correct workflow for Option 1...

## Step-by-Step Manual Setup

### Step 1: Add Webhook
- Type: Webhook
- Path: `upload_data_raw`
- Method: POST
- Name: "Webhook - Python Upload"

### Step 2: Add Code Node
- Name: "Prepare Chunks"
- Code:

```javascript
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

// Output one item per chunk
const outputItems = chunks.map((chunkText, index) => ({
  json: {
    pageContent: chunkText,
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

### Step 3: Add Data Loader
- Type: Default Data Loader
- Data Type: **JSON**
- JSON Property: `pageContent`
- Name: "Data Loader - Python"

### Step 4: Add NEW Qdrant Vector Store Node
- Type: Qdrant Vector Store
- Mode: **Insert**
- Collection: `test-collection` (same as your existing one!)
- Name: "Qdrant - Python Upload"
- Credentials: Same as existing Qdrant node

### Step 5: Make Connections

**Main flow:**
1. Webhook → Prepare Chunks (main)
2. Prepare Chunks → Qdrant - Python Upload (main)

**Sub-nodes (connect to Qdrant - Python Upload):**
3. Data Loader - Python → Qdrant - Python Upload (ai_document)
4. Embeddings OpenAI → Qdrant - Python Upload (ai_embedding)

### Final Flow Diagram:

```
Webhook - Python Upload
    ↓ (main)
Prepare Chunks
    ↓ (main)
Qdrant - Python Upload ←─── (ai_document) ──── Data Loader - Python
    ↑                                               ↑ (gets data from Prepare Chunks)
    │
    └──── (ai_embedding) ──── Embeddings OpenAI (existing node)
```

The key is that Data Loader - Python will automatically receive data from "Prepare Chunks" because it's connected as a sub-node to Qdrant, and Qdrant is in the main flow after Prepare Chunks.

## Why This Works

- Each Qdrant Vector Store node can have ONE ai_document input
- Both Qdrant nodes write to the SAME collection
- Both use the SAME Embeddings OpenAI node
- Form uploads go through one Qdrant node
- Python uploads go through a different Qdrant node
- But all data ends up in "test-collection"!

This is the correct n8n LangChain pattern!

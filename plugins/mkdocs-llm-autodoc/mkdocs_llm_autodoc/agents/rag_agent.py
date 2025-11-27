"""
RAG Agent with MCP Tool Support

Handles ingestion of documentation into ChromaDB and provides a
ReAct-style chatbot interface for querying the knowledge base.
"""

import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

import chromadb
from chromadb.utils import embedding_functions

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.rag')

class RAGAgent:
    """
    Agent for Retrieval-Augmented Generation (RAG) with Tool Use.
    """

    def __init__(self, llm_provider, collection_name: str = "llm_autodoc"):
        self.llm = llm_provider
        self.collection_name = collection_name
        
        # Initialize ChromaDB Client
        # If running in Docker with a separate service, use HttpClient
        chroma_host = os.environ.get("CHROMA_HOST", "localhost")
        chroma_port = os.environ.get("CHROMA_PORT", "8000")
        
        try:
            # Try connecting to HTTP server first (Docker setup)
            self.client = chromadb.HttpClient(host=chroma_host, port=int(chroma_port))
            logger.info(f"Connected to ChromaDB at {chroma_host}:{chroma_port}")
        except:
            # Fallback to local persistent client
            logger.info("ChromaDB server not found, falling back to local storage")
            self.client = chromadb.PersistentClient(path="./chroma_db")

        # Use OpenAI embeddings if key is present, otherwise default (all-MiniLM-L6-v2)
        openai_key = os.environ.get("OPENAI_API_KEY")
        openai_base = os.environ.get("OPENAI_API_BASE")
        
        if openai_key:
            self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                api_key=openai_key,
                api_base=openai_base, # Pass base_url if present
                model_name="text-embedding-ada-002"
            )
        else:
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn
        )

    def ingest_docs(self, docs_dir: str):
        """
        Ingest all Markdown files from the directory into ChromaDB.
        """
        docs_path = Path(docs_dir)
        files = list(docs_path.rglob("*.md"))
        
        logger.info(f"Ingesting {len(files)} files into RAG...")
        
        ids = []
        documents = []
        metadatas = []
        
        for file_path in files:
            try:
                content = file_path.read_text(encoding='utf-8')
                # Simple chunking by header could be done here.
                # For now, we ingest the whole file or large chunks.
                # Let's do a naive chunking of 1000 chars for simplicity in this MVP.
                chunks = [content[i:i+2000] for i in range(0, len(content), 1800)]
                
                for i, chunk in enumerate(chunks):
                    ids.append(f"{file_path.name}_{i}")
                    documents.append(chunk)
                    metadatas.append({
                        "source": str(file_path),
                        "filename": file_path.name,
                        "chunk_index": i
                    })
            except Exception as e:
                logger.error(f"Failed to read {file_path}: {e}")

        if documents:
            # Upsert (update or insert)
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_end = min(i + batch_size, len(documents))
                self.collection.upsert(
                    ids=ids[i:batch_end],
                    documents=documents[i:batch_end],
                    metadatas=metadatas[i:batch_end]
                )
            logger.info(f"Successfully ingested {len(documents)} chunks.")

    def chat(self, query: str) -> str:
        """
        ReAct Loop for answering questions.
        """
        # 1. Retrieve relevant context from RAG
        results = self.collection.query(
            query_texts=[query],
            n_results=3
        )
        
        context = ""
        if results['documents']:
            context = "\n\n".join(results['documents'][0])
            
        # 2. Construct Prompt with Tools
        prompt = f"""You are a helpful coding assistant with access to the project documentation and source code.

User Query: {query}

# Retrieved Documentation Context
{context}

# Available Tools
You can use the following tools if the documentation is not enough:
- `read_file(path)`: Read the content of a specific file.
- `search_code(term)`: Search for a term in the codebase.

# Instructions
- If the "Retrieved Documentation Context" contains the answer, answer directly.
- If you need to see the actual code to be sure, output a TOOL CALL in the format: `TOOL: read_file("path/to/file")`.
- I will execute the tool and give you the output.
- If you have enough info, just output the answer.

Current Query: {query}
"""
        
        # 3. LLM Generation (Single turn for MVP, loop for full ReAct)
        # For a true ReAct loop, we would loop here. 
        # For this implementation, we'll do a simple "Check if tool needed" pass.
        
        response = self.llm.generate(prompt)
        
        if response.startswith("TOOL:"):
            # Execute Tool (Mock implementation for now)
            tool_call = response.strip()
            logger.info(f"Agent requested tool: {tool_call}")
            
            # Parse tool
            if "read_file" in tool_call:
                # Extract path (naive parsing)
                import re
                match = re.search(r'read_file\("(.+?)"\)', tool_call)
                if match:
                    path = match.group(1)
                    try:
                        file_content = Path(path).read_text(encoding='utf-8')[:2000] # Limit size
                        tool_output = f"Content of {path}:\n{file_content}"
                    except Exception as e:
                        tool_output = f"Error reading file: {e}"
                else:
                    tool_output = "Invalid tool format"
            elif "search_code" in tool_call:
                 match = re.search(r'search_code\("(.+?)"\)', tool_call)
                 if match:
                     term = match.group(1)
                     # Mock search
                     tool_output = f"Found 3 matches for '{term}' in main.cpp..."
                 else:
                     tool_output = "Invalid tool format"
            else:
                tool_output = "Unknown tool"
                
            # Feed tool output back to LLM
            final_prompt = f"{prompt}\n\nTOOL OUTPUT:\n{tool_output}\n\nNow answer the user's question."
            return self.llm.generate(final_prompt)
            
        return response

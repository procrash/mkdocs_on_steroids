"""
RAG Store Manager for ChatBot Plugin

Manages vector database integration for retrieval-augmented generation.
Supports multiple RAG backends:
- ChromaDB (local)
- Pinecone (cloud)
- Weaviate (local/cloud)
- Custom RAG endpoints
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

logger = logging.getLogger('mkdocs.plugins.chatbot.rag')


class RAGManager:
    """
    Manages RAG store for documentation retrieval.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize RAG manager with configuration.

        Args:
            config: RAG configuration dictionary
                - type: 'chromadb', 'pinecone', 'weaviate', 'custom'
                - collection_name: Name of the collection/index
                - embedding_model: Model for embeddings
                - top_k: Number of results to retrieve
                - Additional backend-specific settings
        """
        self.config = config
        self.rag_type = config.get('type', 'chromadb')
        self.collection_name = config.get('collection_name', 'mkdocs_documentation')
        self.top_k = config.get('top_k', 5)
        self.embedding_model = config.get('embedding_model', 'sentence-transformers/all-MiniLM-L6-v2')

        self.client = None
        self.collection = None

        self._initialize_backend()

    def _initialize_backend(self):
        """Initialize the appropriate RAG backend."""
        try:
            if self.rag_type == 'chromadb':
                self._init_chromadb()
            elif self.rag_type == 'pinecone':
                self._init_pinecone()
            elif self.rag_type == 'weaviate':
                self._init_weaviate()
            elif self.rag_type == 'qdrant':
                self._init_qdrant()
            elif self.rag_type == 'custom':
                self._init_custom()
            else:
                logger.warning(f"Unknown RAG type: {self.rag_type}, RAG disabled")
        except Exception as e:
            logger.error(f"Failed to initialize RAG backend: {e}")
            self.client = None

    def _init_chromadb(self):
        """Initialize ChromaDB backend."""
        try:
            import chromadb
            from chromadb.config import Settings

            persist_directory = self.config.get('persist_directory', '.cache/chromadb')

            self.client = chromadb.Client(Settings(
                persist_directory=str(Path(persist_directory).absolute()),
                anonymized_telemetry=False
            ))

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "MkDocs documentation embeddings"}
            )

            logger.info(f"ChromaDB initialized with collection: {self.collection_name}")

        except ImportError:
            logger.error("ChromaDB not installed. Install with: pip install chromadb")
            self.client = None
        except Exception as e:
            logger.error(f"ChromaDB initialization failed: {e}")
            self.client = None

    def _init_pinecone(self):
        """Initialize Pinecone backend."""
        try:
            import pinecone

            api_key = self.config.get('api_key')
            environment = self.config.get('environment')

            if not api_key:
                raise ValueError("Pinecone API key not provided")

            pinecone.init(api_key=api_key, environment=environment)

            # Get index
            index_name = self.config.get('index_name', self.collection_name)
            if index_name not in pinecone.list_indexes():
                logger.warning(f"Pinecone index '{index_name}' not found")
                self.client = None
                return

            self.client = pinecone.Index(index_name)
            logger.info(f"Pinecone initialized with index: {index_name}")

        except ImportError:
            logger.error("Pinecone not installed. Install with: pip install pinecone-client")
            self.client = None
        except Exception as e:
            logger.error(f"Pinecone initialization failed: {e}")
            self.client = None

    def _init_weaviate(self):
        """Initialize Weaviate backend."""
        try:
            import weaviate

            url = self.config.get('url', 'http://localhost:8080')
            api_key = self.config.get('api_key')

            if api_key:
                auth_config = weaviate.AuthApiKey(api_key=api_key)
                self.client = weaviate.Client(url=url, auth_client_secret=auth_config)
            else:
                self.client = weaviate.Client(url=url)

            # Check if class exists
            schema = self.client.schema.get()
            class_names = [c['class'] for c in schema.get('classes', [])]

            if self.collection_name not in class_names:
                logger.warning(f"Weaviate class '{self.collection_name}' not found")
                self.client = None
                return

            logger.info(f"Weaviate initialized with class: {self.collection_name}")

        except ImportError:
            logger.error("Weaviate not installed. Install with: pip install weaviate-client")
            self.client = None
        except Exception as e:
            logger.error(f"Weaviate initialization failed: {e}")
            self.client = None

    def _init_qdrant(self):
        """Initialize Qdrant backend."""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams

            url = self.config.get('url', 'http://localhost:6333')
            api_key = self.config.get('api_key')

            # Initialize client
            if api_key:
                self.client = QdrantClient(url=url, api_key=api_key)
            else:
                self.client = QdrantClient(url=url)

            # Check if collection exists
            try:
                self.client.get_collection(self.collection_name)
                logger.info(f"Qdrant collection '{self.collection_name}' found")
            except Exception:
                logger.warning(f"Qdrant collection '{self.collection_name}' not found")
                # Collection will be created on first document add
                self.collection = None
                return

            self.collection = self.collection_name
            logger.info(f"Qdrant initialized with collection: {self.collection_name}")

        except ImportError:
            logger.error("Qdrant client not installed. Install with: pip install qdrant-client")
            self.client = None
        except Exception as e:
            logger.error(f"Qdrant initialization failed: {e}")
            self.client = None

    def _init_custom(self):
        """Initialize custom RAG endpoint."""
        endpoint = self.config.get('endpoint')
        if not endpoint:
            logger.error("Custom RAG endpoint not provided")
            self.client = None
            return

        self.client = {'type': 'custom', 'endpoint': endpoint}
        logger.info(f"Custom RAG endpoint initialized: {endpoint}")

    def query(self, query_text: str, page_context: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Query the RAG store for relevant documentation.

        Args:
            query_text: User's query
            page_context: Optional context about current page

        Returns:
            List of relevant document chunks with metadata
        """
        if not self.client:
            logger.warning("RAG not initialized, returning empty results")
            return []

        try:
            if self.rag_type == 'chromadb':
                return self._query_chromadb(query_text, page_context)
            elif self.rag_type == 'pinecone':
                return self._query_pinecone(query_text, page_context)
            elif self.rag_type == 'weaviate':
                return self._query_weaviate(query_text, page_context)
            elif self.rag_type == 'qdrant':
                return self._query_qdrant(query_text, page_context)
            elif self.rag_type == 'custom':
                return self._query_custom(query_text, page_context)
            else:
                return []
        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return []

    def _query_chromadb(self, query_text: str, page_context: Optional[Dict]) -> List[Dict[str, Any]]:
        """Query ChromaDB."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=self.top_k
        )

        documents = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results.get('metadatas') else {}
                distance = results['distances'][0][i] if results.get('distances') else None

                documents.append({
                    'content': doc,
                    'metadata': metadata,
                    'score': 1 - distance if distance is not None else 0.0
                })

        return documents

    def _query_pinecone(self, query_text: str, page_context: Optional[Dict]) -> List[Dict[str, Any]]:
        """Query Pinecone."""
        # Need to embed the query first
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(self.embedding_model)
        query_embedding = model.encode(query_text).tolist()

        results = self.client.query(
            vector=query_embedding,
            top_k=self.top_k,
            include_metadata=True
        )

        documents = []
        for match in results.get('matches', []):
            documents.append({
                'content': match.get('metadata', {}).get('text', ''),
                'metadata': match.get('metadata', {}),
                'score': match.get('score', 0.0)
            })

        return documents

    def _query_weaviate(self, query_text: str, page_context: Optional[Dict]) -> List[Dict[str, Any]]:
        """Query Weaviate."""
        result = (
            self.client.query
            .get(self.collection_name, ["content", "title", "url", "section"])
            .with_near_text({"concepts": [query_text]})
            .with_limit(self.top_k)
            .with_additional(["distance"])
            .do()
        )

        documents = []
        data = result.get('data', {}).get('Get', {}).get(self.collection_name, [])

        for item in data:
            documents.append({
                'content': item.get('content', ''),
                'metadata': {
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'section': item.get('section', '')
                },
                'score': 1 - item.get('_additional', {}).get('distance', 0.0)
            })

        return documents

    def _query_qdrant(self, query_text: str, page_context: Optional[Dict]) -> List[Dict[str, Any]]:
        """Query Qdrant."""
        from sentence_transformers import SentenceTransformer

        # Embed the query
        model = SentenceTransformer(self.embedding_model)
        query_embedding = model.encode(query_text).tolist()

        # Search in Qdrant
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=self.top_k
        )

        documents = []
        for hit in results:
            documents.append({
                'content': hit.payload.get('content', ''),
                'metadata': {k: v for k, v in hit.payload.items() if k != 'content'},
                'score': hit.score
            })

        return documents

    def _query_custom(self, query_text: str, page_context: Optional[Dict]) -> List[Dict[str, Any]]:
        """Query custom RAG endpoint."""
        import requests

        endpoint = self.client['endpoint']

        payload = {
            'query': query_text,
            'top_k': self.top_k,
            'page_context': page_context
        }

        headers = {}
        if api_key := self.config.get('api_key'):
            headers['Authorization'] = f"Bearer {api_key}"

        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()

        return response.json().get('results', [])

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Add documents to the RAG store.

        Args:
            documents: List of documents with 'content', 'metadata', and optional 'id'
        """
        if not self.client:
            logger.warning("RAG not initialized, cannot add documents")
            return

        try:
            if self.rag_type == 'chromadb':
                self._add_documents_chromadb(documents)
            elif self.rag_type == 'pinecone':
                self._add_documents_pinecone(documents)
            elif self.rag_type == 'weaviate':
                self._add_documents_weaviate(documents)
            elif self.rag_type == 'qdrant':
                self._add_documents_qdrant(documents)
            else:
                logger.warning(f"Adding documents not supported for {self.rag_type}")
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")

    def _add_documents_chromadb(self, documents: List[Dict[str, Any]]):
        """Add documents to ChromaDB."""
        ids = [doc.get('id', f"doc_{i}") for i, doc in enumerate(documents)]
        texts = [doc['content'] for doc in documents]
        metadatas = [doc.get('metadata', {}) for doc in documents]

        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )

        logger.info(f"Added {len(documents)} documents to ChromaDB")

    def _add_documents_pinecone(self, documents: List[Dict[str, Any]]):
        """Add documents to Pinecone."""
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(self.embedding_model)

        vectors = []
        for i, doc in enumerate(documents):
            embedding = model.encode(doc['content']).tolist()
            doc_id = doc.get('id', f"doc_{i}")
            metadata = doc.get('metadata', {})
            metadata['text'] = doc['content']  # Store text in metadata

            vectors.append((doc_id, embedding, metadata))

        self.client.upsert(vectors=vectors)
        logger.info(f"Added {len(documents)} documents to Pinecone")

    def _add_documents_weaviate(self, documents: List[Dict[str, Any]]):
        """Add documents to Weaviate."""
        with self.client.batch as batch:
            for doc in documents:
                properties = {
                    'content': doc['content'],
                    **doc.get('metadata', {})
                }
                batch.add_data_object(properties, self.collection_name)

        logger.info(f"Added {len(documents)} documents to Weaviate")

    def _add_documents_qdrant(self, documents: List[Dict[str, Any]]):
        """Add documents to Qdrant."""
        from sentence_transformers import SentenceTransformer
        from qdrant_client.models import PointStruct, Distance, VectorParams
        import uuid

        model = SentenceTransformer(self.embedding_model)

        # Create collection if it doesn't exist
        if not self.collection:
            # Determine vector size from first document
            sample_embedding = model.encode(documents[0]['content'])
            vector_size = len(sample_embedding)

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            self.collection = self.collection_name
            logger.info(f"Created Qdrant collection: {self.collection_name}")

        # Prepare points
        points = []
        for doc in documents:
            doc_id = doc.get('id', str(uuid.uuid4()))
            content = doc['content']
            metadata = doc.get('metadata', {})

            # Generate embedding
            embedding = model.encode(content).tolist()

            # Create payload
            payload = {'content': content, **metadata}

            points.append(PointStruct(
                id=doc_id,
                vector=embedding,
                payload=payload
            ))

        # Upload to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        logger.info(f"Added {len(documents)} documents to Qdrant")

    def is_available(self) -> bool:
        """Check if RAG is available and initialized."""
        return self.client is not None

"""
RAG Uploader Utility

Automatically uploads source files and generated documentation to RAG system.
"""

import os
import sys
import logging
import requests
from pathlib import Path
from typing import Optional, Dict, List
from dotenv import load_dotenv

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.rag_uploader')


class RAGUploader:
    """Uploads files to RAG system via n8n webhook."""

    def __init__(self, webhook_url: Optional[str] = None, enabled: bool = True):
        """
        Initialize RAG uploader.

        Args:
            webhook_url: n8n webhook URL (defaults to env variable)
            enabled: Whether uploads are enabled
        """
        self.enabled = enabled

        if not enabled:
            logger.info("RAG upload is disabled")
            return

        # Load environment variables
        load_dotenv('.env.windows')
        load_dotenv('.env')

        self.webhook_url = webhook_url or os.getenv('N8N_WEBHOOK_URL')

        if not self.webhook_url:
            logger.warning("RAG upload disabled: N8N_WEBHOOK_URL not configured")
            self.enabled = False
        else:
            logger.info(f"RAG uploader initialized: {self.webhook_url}")

    def upload_file(
        self,
        file_path: str,
        file_type: str = 'source_code',
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Upload a single file to RAG.

        Args:
            file_path: Path to file
            file_type: Type of file ('source_code' or 'documentation')
            metadata: Additional metadata

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False

        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"File not found: {file_path}")
                return False

            # Read file content
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(path, 'r', encoding='latin-1') as f:
                    content = f.read()

            # Prepare payload
            payload = {
                'file_name': path.name,
                'file_path': str(path.absolute()),
                'file_type': path.suffix.lower(),
                'content': content,
                'metadata': {
                    'type': file_type,
                    'project': 'mkdocs-llm-autodoc',
                    **(metadata or {})
                }
            }

            # Upload to n8n
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()

            logger.debug(f"✓ Uploaded to RAG: {path.name}")
            return True

        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to upload {file_path} to RAG: {e}")
            return False
        except Exception as e:
            logger.warning(f"Error uploading {file_path}: {e}")
            return False

    def upload_source_file(self, file_path: str, metadata: Optional[Dict] = None) -> bool:
        """Upload a source code file."""
        return self.upload_file(
            file_path,
            file_type='source_code',
            metadata=metadata
        )

    def upload_documentation(self, file_path: str, source_file: Optional[str] = None, metadata: Optional[Dict] = None) -> bool:
        """Upload generated documentation."""
        doc_metadata = metadata or {}
        if source_file:
            doc_metadata['source_file'] = source_file
            doc_metadata['auto_generated'] = True

        return self.upload_file(
            file_path,
            file_type='documentation',
            metadata=doc_metadata
        )

    def upload_batch(self, files: List[tuple]) -> Dict[str, int]:
        """
        Upload multiple files in batch.

        Args:
            files: List of tuples (file_path, file_type, metadata)

        Returns:
            Dictionary with success/failure counts
        """
        results = {'success': 0, 'failed': 0}

        for file_info in files:
            file_path = file_info[0]
            file_type = file_info[1] if len(file_info) > 1 else 'source_code'
            metadata = file_info[2] if len(file_info) > 2 else None

            if self.upload_file(file_path, file_type, metadata):
                results['success'] += 1
            else:
                results['failed'] += 1

        return results

"""
Document Upload Service for Windows
Automatically splits source code and documents using appropriate LangChain splitters
and uploads to n8n RAG service.
"""

import os
import sys
import mimetypes
import logging
from pathlib import Path
from typing import List, Optional, Tuple
from dotenv import load_dotenv
import requests

# LangChain imports
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language,
    MarkdownTextSplitter,
    LatexTextSplitter,
    HTMLHeaderTextSplitter,
)

# PDF processing
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

# Load environment variables
load_dotenv('.env.windows')
load_dotenv('.env')  # Fallback to .env if exists

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Processes documents and splits them using appropriate LangChain splitters."""

    # Map file extensions to LangChain Language enum
    # Only includes languages confirmed to exist in langchain_text_splitters.Language
    LANGUAGE_MAP = {
        '.cpp': Language.CPP,
        '.cc': Language.CPP,
        '.cxx': Language.CPP,
        '.c': Language.C,
        '.h': Language.CPP,
        '.hpp': Language.CPP,
        '.py': Language.PYTHON,
        '.js': Language.JS,
        '.ts': Language.TS,
        '.java': Language.JAVA,
        '.go': Language.GO,
        '.rs': Language.RUST,
        '.rb': Language.RUBY,
        '.php': Language.PHP,
        '.scala': Language.SCALA,
        '.swift': Language.SWIFT,
        '.kt': Language.KOTLIN,
        '.cs': Language.CSHARP,
        '.lua': Language.LUA,
        '.pl': Language.PERL,
        '.sol': Language.SOL,
        '.ps1': Language.POWERSHELL,
        '.vb': Language.VISUALBASIC6,
        '.vbs': Language.VISUALBASIC6,
        '.ex': Language.ELIXIR,
        '.exs': Language.ELIXIR,
        '.hs': Language.HASKELL,
        '.proto': Language.PROTO,
        '.cbl': Language.COBOL,
        '.cob': Language.COBOL,
    }

    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None
    ):
        """
        Initialize the document processor.

        Args:
            chunk_size: Size of text chunks (default from env or 1000)
            chunk_overlap: Overlap between chunks (default from env or 200)
        """
        self.chunk_size = chunk_size or int(os.getenv('DEFAULT_CHUNK_SIZE', 1000))
        self.chunk_overlap = chunk_overlap or int(os.getenv('DEFAULT_CHUNK_OVERLAP', 200))
        logger.info(f"Initialized DocumentProcessor (chunk_size={self.chunk_size}, overlap={self.chunk_overlap})")

    def get_splitter_for_file(self, file_path: str):
        """
        Get the appropriate text splitter based on file type.

        Args:
            file_path: Path to the file

        Returns:
            Appropriate LangChain text splitter
        """
        file_ext = Path(file_path).suffix.lower()

        # Markdown files
        if file_ext in ['.md', '.markdown']:
            logger.info(f"Using MarkdownTextSplitter for {file_path}")
            return MarkdownTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )

        # RST (reStructuredText) files
        if file_ext in ['.rst']:
            logger.info(f"Using RecursiveCharacterTextSplitter with RST for {file_path}")
            return RecursiveCharacterTextSplitter.from_language(
                language=Language.RST,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )

        # LaTeX files
        if file_ext in ['.tex', '.latex']:
            logger.info(f"Using LatexTextSplitter for {file_path}")
            return LatexTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )

        # HTML files (can also use Language.HTML)
        if file_ext in ['.html', '.htm']:
            logger.info(f"Using RecursiveCharacterTextSplitter with HTML for {file_path}")
            return RecursiveCharacterTextSplitter.from_language(
                language=Language.HTML,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )

        # XML files (generic approach)
        if file_ext in ['.xml']:
            logger.info(f"Using RecursiveCharacterTextSplitter for XML: {file_path}")
            return RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=["</", ">\n", "\n\n", "\n", " ", ""]
            )

        # Programming language files
        if file_ext in self.LANGUAGE_MAP:
            language = self.LANGUAGE_MAP[file_ext]
            logger.info(f"Using RecursiveCharacterTextSplitter with {language.value} for {file_path}")
            return RecursiveCharacterTextSplitter.from_language(
                language=language,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )

        # Default text splitter for other files
        logger.info(f"Using default RecursiveCharacterTextSplitter for {file_path}")
        return RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def read_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF file.

        Args:
            file_path: Path to PDF file

        Returns:
            Extracted text content
        """
        logger.info(f"Reading PDF: {file_path}")
        try:
            reader = PdfReader(file_path)
            text = ""
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num} ---\n{page_text}"
            logger.info(f"Extracted {len(text)} characters from {len(reader.pages)} pages")
            return text
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {e}")
            raise

    def read_file(self, file_path: str) -> str:
        """
        Read file content with encoding detection.

        Args:
            file_path: Path to file

        Returns:
            File content as string
        """
        encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                logger.info(f"Read {file_path} with {encoding} encoding ({len(content)} chars)")
                return content
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.error(f"Error reading {file_path}: {e}")
                raise

        raise ValueError(f"Could not decode {file_path} with any supported encoding")

    def process_file(self, file_path: str) -> List[str]:
        """
        Process a file and split it into chunks.

        Args:
            file_path: Path to the file

        Returns:
            List of text chunks
        """
        file_ext = Path(file_path).suffix.lower()

        # Handle PDF files specially
        if file_ext == '.pdf':
            content = self.read_pdf(file_path)
            # Use simple text splitter for PDFs
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=["\n--- Page ", "\n\n", "\n", ". ", " ", ""]
            )
        else:
            content = self.read_file(file_path)
            splitter = self.get_splitter_for_file(file_path)

        # Split the content
        chunks = splitter.split_text(content)
        logger.info(f"Split {file_path} into {len(chunks)} chunks")

        return chunks


class N8NUploader:
    """Handles uploading processed documents to n8n webhook."""

    def __init__(self, webhook_url: str = None):
        """
        Initialize the uploader.

        Args:
            webhook_url: n8n webhook URL (default from env)
        """
        self.webhook_url = webhook_url or os.getenv('N8N_WEBHOOK_URL')
        if not self.webhook_url:
            raise ValueError("N8N_WEBHOOK_URL not configured")
        logger.info(f"Initialized N8NUploader with URL: {self.webhook_url}")

    def upload_content(
        self,
        file_path: str,
        content: str,
        metadata: dict = None
    ) -> dict:
        """
        Upload full document content to n8n webhook for server-side splitting.

        Args:
            file_path: Original file path
            content: Full document content (not pre-split)
            metadata: Additional metadata to include

        Returns:
            Response from n8n webhook
        """
        file_name = Path(file_path).name
        file_ext = Path(file_path).suffix.lower()

        payload = {
            'file_name': file_name,
            'file_path': str(file_path),
            'file_type': file_ext,
            'content': content,  # Full content, not chunks
            'metadata': metadata or {}
        }

        try:
            logger.info(f"Uploading {len(content)} characters to {self.webhook_url}")
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()
            logger.info(f"Upload successful! Status: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Upload failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            raise


def upload_document(
    file_path: str,
    webhook_url: str = None,
    chunk_size: int = None,
    chunk_overlap: int = None,
    metadata: dict = None
) -> dict:
    """
    Main function to upload a document for server-side splitting.

    Args:
        file_path: Path to the document
        webhook_url: n8n webhook URL (optional)
        chunk_size: Custom chunk size (optional, passed in metadata)
        chunk_overlap: Custom chunk overlap (optional, passed in metadata)
        metadata: Additional metadata (optional)

    Returns:
        Response from n8n webhook
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read the file content
    processor = DocumentProcessor(chunk_size, chunk_overlap)
    file_ext = Path(file_path).suffix.lower()

    # Read full content without chunking
    if file_ext == '.pdf':
        content = processor.read_pdf(file_path)
    else:
        content = processor.read_file(file_path)

    logger.info(f"Read {len(content)} characters from {file_path}")

    # Add chunk config to metadata for n8n to use
    upload_metadata = metadata or {}
    upload_metadata['chunk_size'] = chunk_size or processor.chunk_size
    upload_metadata['chunk_overlap'] = chunk_overlap or processor.chunk_overlap

    # Upload to n8n for server-side splitting
    uploader = N8NUploader(webhook_url)
    result = uploader.upload_content(file_path, content, upload_metadata)

    return result


def main():
    """Command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Upload and process documents for RAG system'
    )
    parser.add_argument(
        'file_path',
        help='Path to the document to upload'
    )
    parser.add_argument(
        '--webhook-url',
        help='n8n webhook URL (default from .env)'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        help='Chunk size for splitting (default from .env or 1000)'
    )
    parser.add_argument(
        '--chunk-overlap',
        type=int,
        help='Chunk overlap (default from .env or 200)'
    )

    args = parser.parse_args()

    try:
        result = upload_document(
            args.file_path,
            args.webhook_url,
            args.chunk_size,
            args.chunk_overlap
        )
        print(f"\n✓ Upload successful!")
        print(f"Response: {result}")
        return 0
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        print(f"\n✗ Upload failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())

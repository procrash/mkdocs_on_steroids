"""
Automatic RAG Uploader

Automatically uploads and indexes:
- Source code files
- Generated documentation
- Markdown files
- All project files

With intelligent chunking based on file type.
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.auto-rag')


class AutoRAGUploader:
    """
    Automatically uploads documents to RAG store with intelligent chunking.
    """

    def __init__(self, rag_manager, document_chunker, max_workers: int = 4):
        """
        Initialize auto RAG uploader.

        Args:
            rag_manager: RAGManager instance
            document_chunker: DocumentChunker instance
            max_workers: Number of parallel upload workers
        """
        self.rag = rag_manager
        self.chunker = document_chunker
        self.max_workers = max_workers

    def upload_project(self,
                      project_path: str,
                      docs_path: Optional[str] = None,
                      generated_docs_path: Optional[str] = None,
                      include_patterns: Optional[List[str]] = None,
                      exclude_patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Upload entire project to RAG.

        Args:
            project_path: Path to source code
            docs_path: Path to documentation
            generated_docs_path: Path to generated docs
            include_patterns: File patterns to include
            exclude_patterns: File patterns to exclude

        Returns:
            Upload statistics
        """
        logger.info("Starting automatic RAG upload...")

        stats = {
            'source_files': 0,
            'doc_files': 0,
            'generated_files': 0,
            'total_chunks': 0,
            'errors': []
        }

        # Default patterns
        if not include_patterns:
            include_patterns = [
                '**/*.py',
                '**/*.cpp',
                '**/*.h',
                '**/*.hpp',
                '**/*.c',
                '**/*.cc',
                '**/*.md',
                '**/*.js',
                '**/*.ts',
                '**/*.java',
                '**/*.go',
                '**/*.rs',
                '**/*.txt'
            ]

        if not exclude_patterns:
            exclude_patterns = [
                '**/node_modules/**',
                '**/.git/**',
                '**/__pycache__/**',
                '**/*.pyc',
                '**/build/**',
                '**/dist/**',
                '**/.cache/**',
                '**/venv/**',
                '**/venvLinux/**',
                '**/venvWindows/**',
                '**/.pytest_cache/**',
                '**/test_*.py'
            ]

        # Upload source code
        if project_path:
            logger.info(f"Uploading source code from: {project_path}")
            source_stats = self._upload_directory(
                project_path,
                include_patterns,
                exclude_patterns,
                category='source'
            )
            stats['source_files'] = source_stats['files']
            stats['total_chunks'] += source_stats['chunks']
            stats['errors'].extend(source_stats['errors'])

        # Upload documentation
        if docs_path:
            logger.info(f"Uploading documentation from: {docs_path}")
            doc_stats = self._upload_directory(
                docs_path,
                ['**/*.md', '**/*.txt'],
                exclude_patterns,
                category='documentation'
            )
            stats['doc_files'] = doc_stats['files']
            stats['total_chunks'] += doc_stats['chunks']
            stats['errors'].extend(doc_stats['errors'])

        # Upload generated documentation
        if generated_docs_path:
            logger.info(f"Uploading generated docs from: {generated_docs_path}")
            gen_stats = self._upload_directory(
                generated_docs_path,
                ['**/*.md'],
                exclude_patterns,
                category='generated'
            )
            stats['generated_files'] = gen_stats['files']
            stats['total_chunks'] += gen_stats['chunks']
            stats['errors'].extend(gen_stats['errors'])

        logger.info(f"RAG upload complete: {stats['total_chunks']} chunks from "
                   f"{stats['source_files'] + stats['doc_files'] + stats['generated_files']} files")

        return stats

    def _upload_directory(self,
                         directory: str,
                         include_patterns: List[str],
                         exclude_patterns: List[str],
                         category: str) -> Dict[str, Any]:
        """Upload all files from a directory."""
        stats = {
            'files': 0,
            'chunks': 0,
            'errors': []
        }

        directory_path = Path(directory)
        if not directory_path.exists():
            logger.warning(f"Directory not found: {directory}")
            return stats

        # Collect all files
        files_to_process = []
        for pattern in include_patterns:
            for file_path in directory_path.glob(pattern):
                if file_path.is_file():
                    # Check exclusions
                    should_exclude = False
                    for exclude in exclude_patterns:
                        if file_path.match(exclude):
                            should_exclude = True
                            break

                    if not should_exclude:
                        files_to_process.append(file_path)

        logger.info(f"Found {len(files_to_process)} files to upload in {directory}")

        # Process files in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._process_and_upload_file, file_path, category): file_path
                for file_path in files_to_process
            }

            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    file_stats = future.result()
                    stats['files'] += 1
                    stats['chunks'] += file_stats['chunks']

                except Exception as e:
                    logger.error(f"Failed to upload {file_path}: {e}")
                    stats['errors'].append({
                        'file': str(file_path),
                        'error': str(e)
                    })

        return stats

    def _process_and_upload_file(self, file_path: Path, category: str) -> Dict[str, Any]:
        """Process a single file: chunk and upload."""
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Chunk document
            chunks = self.chunker.chunk_document(str(file_path), content)

            # Add category to metadata
            for chunk in chunks:
                chunk['metadata']['category'] = category
                chunk['metadata']['project'] = 'mkdocs'

            # Upload to RAG
            if self.rag and self.rag.is_available():
                self.rag.add_documents(chunks)

            logger.debug(f"Uploaded {len(chunks)} chunks from {file_path.name}")

            return {
                'chunks': len(chunks),
                'file': str(file_path)
            }

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            raise

    def upload_single_file(self,
                          file_path: str,
                          category: str = 'general',
                          metadata: Optional[Dict] = None) -> int:
        """
        Upload a single file to RAG.

        Args:
            file_path: Path to file
            category: File category
            metadata: Additional metadata

        Returns:
            Number of chunks uploaded
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            chunks = self.chunker.chunk_document(file_path, content)

            # Add metadata
            for chunk in chunks:
                chunk['metadata']['category'] = category
                chunk['metadata']['project'] = 'mkdocs'
                if metadata:
                    chunk['metadata'].update(metadata)

            # Upload
            if self.rag and self.rag.is_available():
                self.rag.add_documents(chunks)

            logger.info(f"Uploaded {len(chunks)} chunks from {Path(file_path).name}")

            return len(chunks)

        except Exception as e:
            logger.error(f"Failed to upload {file_path}: {e}")
            return 0

    def incremental_upload(self,
                          file_paths: List[str],
                          category: str = 'general') -> Dict[str, Any]:
        """
        Upload multiple files incrementally.

        Args:
            file_paths: List of file paths
            category: File category

        Returns:
            Upload statistics
        """
        stats = {
            'files': 0,
            'chunks': 0,
            'errors': []
        }

        for file_path in file_paths:
            try:
                chunks_uploaded = self.upload_single_file(file_path, category)
                stats['files'] += 1
                stats['chunks'] += chunks_uploaded

            except Exception as e:
                logger.error(f"Failed to upload {file_path}: {e}")
                stats['errors'].append({
                    'file': file_path,
                    'error': str(e)
                })

        return stats

    def reindex_all(self,
                   project_path: str,
                   docs_path: Optional[str] = None,
                   generated_docs_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Completely reindex the project (clear and upload).

        Args:
            project_path: Path to source code
            docs_path: Path to documentation
            generated_docs_path: Path to generated docs

        Returns:
            Upload statistics
        """
        logger.info("Starting full reindex...")

        # Note: RAG stores typically don't have a "clear all" API
        # Instead, we can use collection recreation
        # This is backend-specific, so we log a warning

        logger.warning("Full reindex: Consider manually clearing the collection first")

        # Upload everything
        return self.upload_project(
            project_path,
            docs_path,
            generated_docs_path
        )

    def get_upload_summary(self, stats: Dict[str, Any]) -> str:
        """Generate a human-readable upload summary."""
        summary = f"""
RAG Upload Summary:
─────────────────────────────────────────
Source Files:     {stats['source_files']}
Doc Files:        {stats['doc_files']}
Generated Files:  {stats['generated_files']}
─────────────────────────────────────────
Total Files:      {stats['source_files'] + stats['doc_files'] + stats['generated_files']}
Total Chunks:     {stats['total_chunks']}
Errors:           {len(stats['errors'])}
─────────────────────────────────────────
"""

        if stats['errors']:
            summary += "\nErrors:\n"
            for error in stats['errors'][:5]:  # Show first 5 errors
                summary += f"  • {error['file']}: {error['error']}\n"

            if len(stats['errors']) > 5:
                summary += f"  ... and {len(stats['errors']) - 5} more errors\n"

        return summary

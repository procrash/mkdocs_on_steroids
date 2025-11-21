"""
Document Chunker for RAG Integration

Intelligently chunks documents based on file type:
- Code files: By functions/classes
- Markdown: By sections
- Plain text: By semantic units
"""

import logging
import re
import subprocess
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.chunker')


class DocumentChunker:
    """
    Intelligently chunks documents for RAG storage.
    """

    def __init__(self,
                 max_chunk_size: int = 1000,
                 overlap: int = 100,
                 min_chunk_size: int = 100):
        """
        Initialize document chunker.

        Args:
            max_chunk_size: Maximum characters per chunk
            overlap: Character overlap between chunks
            min_chunk_size: Minimum chunk size (smaller chunks are merged)
        """
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        self.min_chunk_size = min_chunk_size

    def chunk_document(self,
                       file_path: str,
                       content: str,
                       file_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Chunk a document based on its type.

        Args:
            file_path: Path to the file
            content: File content
            file_type: Override file type detection

        Returns:
            List of chunks with metadata including:
            - content: The chunk text
            - id: Unique chunk identifier (MD5 hash)
            - metadata: Dict containing:
                - file_path: Full path to source file
                - file_name: Name of source file
                - file_type: Type of file (python, cpp, markdown, etc.)
                - chunk_index: Index of this chunk
                - total_chunks: Total number of chunks from this file
                - source_file_content: Full source file content for LLM reference
                - file_md5: MD5 hash of source file for versioning
                - git_commit: Git commit hash (short, 8 chars) if available
                - git_tag: Git tag for this commit if available
                - git_nearest_tag: Nearest Git tag if no exact tag
                - git_branch: Current Git branch if available
                - type: Chunk type (function, class, method, section, etc.)
                - name/class/header: Type-specific identifiers
        """
        if not file_type:
            file_type = self._detect_file_type(file_path)

        if file_type == 'code':
            chunks = self._chunk_code(content, file_path)
        elif file_type == 'markdown':
            chunks = self._chunk_markdown(content, file_path)
        elif file_type == 'python':
            chunks = self._chunk_python(content, file_path)
        elif file_type == 'cpp':
            chunks = self._chunk_cpp(content, file_path)
        else:
            chunks = self._chunk_text(content, file_path)

        # Post-process chunks
        chunks = self._merge_small_chunks(chunks)
        chunks = self._add_metadata(chunks, file_path, file_type, content)

        logger.info(f"Chunked {file_path}: {len(chunks)} chunks (type: {file_type})")

        return chunks

    def _detect_file_type(self, file_path: str) -> str:
        """Detect file type from extension."""
        ext = Path(file_path).suffix.lower()

        if ext in ['.py']:
            return 'python'
        elif ext in ['.cpp', '.cc', '.cxx', '.c', '.h', '.hpp', '.hxx']:
            return 'cpp'
        elif ext in ['.md', '.markdown']:
            return 'markdown'
        elif ext in ['.js', '.ts', '.java', '.cs', '.go', '.rs', '.rb']:
            return 'code'
        else:
            return 'text'

    def _chunk_python(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Chunk Python code by functions and classes."""
        chunks = []

        # Split by class definitions
        class_pattern = r'(^class\s+\w+.*?(?=^class\s|\Z))'
        classes = re.findall(class_pattern, content, re.MULTILINE | re.DOTALL)

        if classes:
            for class_code in classes:
                # Extract class name
                class_name_match = re.match(r'class\s+(\w+)', class_code)
                class_name = class_name_match.group(1) if class_name_match else 'Unknown'

                # Split class into methods
                method_pattern = r'(^\s{4}def\s+\w+.*?(?=^\s{4}def\s|^\s{0,3}\S|\Z))'
                methods = re.findall(method_pattern, class_code, re.MULTILINE | re.DOTALL)

                if methods:
                    for method in methods:
                        if len(method.strip()) >= self.min_chunk_size:
                            chunks.append({
                                'content': method.strip(),
                                'metadata': {
                                    'type': 'method',
                                    'class': class_name
                                }
                            })
                else:
                    # No methods found, chunk the whole class
                    if len(class_code.strip()) >= self.min_chunk_size:
                        chunks.append({
                            'content': class_code.strip(),
                            'metadata': {
                                'type': 'class',
                                'class': class_name
                            }
                        })

        # Split by top-level function definitions
        function_pattern = r'(^def\s+\w+.*?(?=^def\s|^class\s|\Z))'
        functions = re.findall(function_pattern, content, re.MULTILINE | re.DOTALL)

        for func in functions:
            if len(func.strip()) >= self.min_chunk_size:
                func_name_match = re.match(r'def\s+(\w+)', func)
                func_name = func_name_match.group(1) if func_name_match else 'Unknown'

                chunks.append({
                    'content': func.strip(),
                    'metadata': {
                        'type': 'function',
                        'name': func_name
                    }
                })

        # If no chunks found, fall back to text chunking
        if not chunks:
            return self._chunk_text(content, file_path)

        return chunks

    def _chunk_cpp(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Chunk C++ code by functions and classes."""
        chunks = []

        # Remove multi-line comments
        content_no_comments = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content_no_comments = re.sub(r'//.*?$', '', content_no_comments, flags=re.MULTILINE)

        # Split by class definitions
        class_pattern = r'(class\s+\w+\s*(?:\:\s*public\s+\w+\s*)?\{[^}]*\}[^;]*;)'
        classes = re.findall(class_pattern, content_no_comments, re.DOTALL)

        for class_code in classes:
            class_name_match = re.search(r'class\s+(\w+)', class_code)
            class_name = class_name_match.group(1) if class_name_match else 'Unknown'

            if len(class_code.strip()) >= self.min_chunk_size:
                chunks.append({
                    'content': class_code.strip(),
                    'metadata': {
                        'type': 'class',
                        'class': class_name
                    }
                })

        # Split by function definitions
        function_pattern = r'((?:[\w\s\*&:]+)\s+(\w+)\s*\([^)]*\)\s*(?:const)?\s*\{[^}]*\})'
        functions = re.findall(function_pattern, content_no_comments, re.DOTALL)

        for func_match in functions:
            func_code = func_match[0]
            func_name = func_match[1]

            if len(func_code.strip()) >= self.min_chunk_size:
                chunks.append({
                    'content': func_code.strip(),
                    'metadata': {
                        'type': 'function',
                        'name': func_name
                    }
                })

        # If no chunks found, fall back to text chunking
        if not chunks:
            return self._chunk_text(content, file_path)

        return chunks

    def _chunk_code(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Generic code chunking by blocks."""
        chunks = []

        # Split by function/method definitions (generic pattern)
        function_pattern = r'((?:function|def|func|fn|public|private|protected).*?\{[^}]*\})'
        functions = re.findall(function_pattern, content, re.DOTALL)

        for func in functions:
            if len(func.strip()) >= self.min_chunk_size:
                chunks.append({
                    'content': func.strip(),
                    'metadata': {'type': 'code_block'}
                })

        # If no functions found, chunk by lines
        if not chunks:
            return self._chunk_text(content, file_path)

        return chunks

    def _chunk_markdown(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Chunk Markdown by sections."""
        chunks = []

        # Split by headers (# ## ### etc.)
        sections = re.split(r'^(#{1,6}\s+.*?)$', content, flags=re.MULTILINE)

        current_section = ""
        current_header = None

        for i, part in enumerate(sections):
            # Check if this is a header
            header_match = re.match(r'^(#{1,6})\s+(.*?)$', part)

            if header_match:
                # Save previous section if exists
                if current_section.strip():
                    chunks.append({
                        'content': current_section.strip(),
                        'metadata': {
                            'type': 'section',
                            'header': current_header
                        }
                    })

                # Start new section
                current_header = header_match.group(2)
                current_section = part + "\n"
            else:
                current_section += part

        # Add last section
        if current_section.strip():
            chunks.append({
                'content': current_section.strip(),
                'metadata': {
                    'type': 'section',
                    'header': current_header
                }
            })

        # Split large sections
        final_chunks = []
        for chunk in chunks:
            if len(chunk['content']) > self.max_chunk_size:
                # Split large sections into smaller chunks
                sub_chunks = self._split_large_chunk(chunk['content'], chunk['metadata'])
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)

        return final_chunks

    def _chunk_text(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Chunk plain text by paragraphs and size."""
        chunks = []

        # Split by double newlines (paragraphs)
        paragraphs = re.split(r'\n\s*\n', content)

        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If adding this paragraph exceeds max size
            if len(current_chunk) + len(para) > self.max_chunk_size:
                if current_chunk:
                    chunks.append({
                        'content': current_chunk.strip(),
                        'metadata': {'type': 'text'}
                    })
                current_chunk = para
            else:
                current_chunk += "\n\n" + para if current_chunk else para

        # Add remaining chunk
        if current_chunk.strip():
            chunks.append({
                'content': current_chunk.strip(),
                'metadata': {'type': 'text'}
            })

        return chunks

    def _split_large_chunk(self, content: str, metadata: Dict) -> List[Dict[str, Any]]:
        """Split a large chunk into smaller pieces."""
        chunks = []
        words = content.split()

        current_chunk = []
        current_size = 0

        for word in words:
            word_size = len(word) + 1  # +1 for space

            if current_size + word_size > self.max_chunk_size:
                if current_chunk:
                    chunks.append({
                        'content': ' '.join(current_chunk),
                        'metadata': {**metadata, 'split': True}
                    })
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size

        if current_chunk:
            chunks.append({
                'content': ' '.join(current_chunk),
                'metadata': {**metadata, 'split': True}
            })

        return chunks

    def _merge_small_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge chunks that are too small."""
        if not chunks:
            return chunks

        merged = []
        current_chunk = None

        for chunk in chunks:
            if len(chunk['content']) < self.min_chunk_size:
                # Merge with previous
                if current_chunk:
                    current_chunk['content'] += "\n\n" + chunk['content']
                else:
                    current_chunk = chunk
            else:
                if current_chunk:
                    merged.append(current_chunk)
                current_chunk = chunk

        if current_chunk:
            merged.append(current_chunk)

        return merged

    def _add_metadata(self,
                     chunks: List[Dict[str, Any]],
                     file_path: str,
                     file_type: str,
                     source_content: str) -> List[Dict[str, Any]]:
        """Add common metadata to all chunks."""
        path = Path(file_path)

        # Calculate MD5 hash of source file
        file_md5 = hashlib.md5(source_content.encode('utf-8')).hexdigest()

        # Get Git information
        git_info = self._get_git_info(file_path)

        for i, chunk in enumerate(chunks):
            # Add file metadata
            chunk['metadata'].update({
                'file_path': str(path),
                'file_name': path.name,
                'file_type': file_type,
                'chunk_index': i,
                'total_chunks': len(chunks),
                'source_file_content': source_content,  # Full source file for LLM reference
                'file_md5': file_md5,  # MD5 hash for versioning
            })

            # Add Git information if available
            if git_info:
                chunk['metadata'].update(git_info)

            # Generate chunk ID
            chunk_id = hashlib.md5(
                f"{file_path}:{i}:{chunk['content'][:100]}".encode()
            ).hexdigest()
            chunk['id'] = chunk_id

        return chunks

    def _get_git_info(self, file_path: str) -> Dict[str, str]:
        """
        Get Git version information for a file.

        Returns:
            Dict with git_commit, git_tag, git_branch if available
        """
        git_info = {}

        try:
            path = Path(file_path)
            if not path.exists():
                return git_info

            # Get current commit hash
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%H', str(path)],
                cwd=path.parent if path.is_file() else path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                git_info['git_commit'] = result.stdout.strip()[:8]  # Short commit hash

            # Get tag for this commit (if any)
            result = subprocess.run(
                ['git', 'describe', '--tags', '--exact-match', 'HEAD'],
                cwd=path.parent if path.is_file() else path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                git_info['git_tag'] = result.stdout.strip()
            else:
                # Get nearest tag
                result = subprocess.run(
                    ['git', 'describe', '--tags', '--abbrev=0'],
                    cwd=path.parent if path.is_file() else path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and result.stdout.strip():
                    git_info['git_nearest_tag'] = result.stdout.strip()

            # Get current branch
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=path.parent if path.is_file() else path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                git_info['git_branch'] = result.stdout.strip()

        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            # Git not available or not a git repo - that's fine
            logger.debug(f"Could not get git info for {file_path}: {e}")

        return git_info

    def chunk_directory(self,
                       directory: str,
                       patterns: List[str] = None,
                       exclude_patterns: List[str] = None) -> List[Dict[str, Any]]:
        """
        Chunk all files in a directory.

        Args:
            directory: Directory path
            patterns: File patterns to include (e.g., ['*.py', '*.md'])
            exclude_patterns: Patterns to exclude

        Returns:
            List of all chunks with metadata
        """
        all_chunks = []
        directory_path = Path(directory)

        if not patterns:
            patterns = ['**/*']

        if not exclude_patterns:
            exclude_patterns = [
                '**/node_modules/**',
                '**/.git/**',
                '**/__pycache__/**',
                '**/*.pyc',
                '**/build/**',
                '**/.cache/**'
            ]

        for pattern in patterns:
            for file_path in directory_path.glob(pattern):
                if file_path.is_file():
                    # Check exclusions
                    should_exclude = False
                    for exclude in exclude_patterns:
                        if file_path.match(exclude):
                            should_exclude = True
                            break

                    if should_exclude:
                        continue

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        chunks = self.chunk_document(str(file_path), content)
                        all_chunks.extend(chunks)

                    except Exception as e:
                        logger.error(f"Failed to chunk {file_path}: {e}")

        logger.info(f"Chunked directory {directory}: {len(all_chunks)} total chunks")

        return all_chunks

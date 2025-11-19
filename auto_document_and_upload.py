"""
Automated Documentation Generator with RAG Upload

This script:
1. Reads source files from a directory
2. Generates documentation for them
3. Automatically uploads both the source AND documentation to the RAG system
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import logging
from dotenv import load_dotenv

# Import our document uploader
from document_uploader import upload_document

# Load environment
load_dotenv('.env.windows')
load_dotenv('.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AutoDocUploader:
    """Automatically documents and uploads files to RAG system."""

    def __init__(self, source_dir: str):
        """
        Initialize the auto-documenter.

        Args:
            source_dir: Directory containing source files to document
        """
        self.source_dir = Path(source_dir)
        self.uploaded_files = []
        self.failed_files = []

    def generate_simple_documentation(self, file_path: Path) -> str:
        """
        Generate simple documentation for a source file.

        Args:
            file_path: Path to the source file

        Returns:
            Generated documentation as markdown string
        """
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Generate basic documentation
            doc = f"""# Documentation for {file_path.name}

## File Information

- **File Path**: {file_path}
- **File Type**: {file_path.suffix}
- **Size**: {len(content)} characters
- **Lines**: {len(content.splitlines())} lines

## Purpose

This file is part of the {self.source_dir.name} project.

## Content Overview

{self._generate_content_overview(file_path, content)}

## File Content

The actual source code is stored separately in the RAG system for reference.

---
*This documentation was automatically generated and uploaded to the RAG system.*
"""
            return doc

        except Exception as e:
            logger.error(f"Error generating documentation for {file_path}: {e}")
            return None

    def _generate_content_overview(self, file_path: Path, content: str) -> str:
        """Generate a simple overview of the file content."""
        ext = file_path.suffix.lower()
        lines = content.splitlines()

        overview = []

        # Python files
        if ext == '.py':
            imports = [l for l in lines if l.strip().startswith('import ') or l.strip().startswith('from ')]
            classes = [l for l in lines if l.strip().startswith('class ')]
            functions = [l for l in lines if l.strip().startswith('def ')]

            if imports:
                overview.append(f"- {len(imports)} import statements")
            if classes:
                overview.append(f"- {len(classes)} class definitions")
                for cls in classes[:5]:  # First 5
                    overview.append(f"  - `{cls.strip()}`")
            if functions:
                overview.append(f"- {len(functions)} function definitions")
                for func in functions[:5]:  # First 5
                    overview.append(f"  - `{func.strip()}`")

        # C++ files
        elif ext in ['.cpp', '.cc', '.cxx', '.h', '.hpp']:
            includes = [l for l in lines if l.strip().startswith('#include')]
            classes = [l for l in lines if 'class ' in l and '{' in l]
            functions = [l for l in lines if '(' in l and ')' in l and '{' in l]

            if includes:
                overview.append(f"- {len(includes)} include directives")
            if classes:
                overview.append(f"- ~{len(classes)} class definitions")
            if functions:
                overview.append(f"- ~{len(functions)} function definitions")

        # Markdown files
        elif ext in ['.md', '.markdown']:
            headers = [l for l in lines if l.strip().startswith('#')]
            if headers:
                overview.append(f"- {len(headers)} headers/sections")
                for header in headers[:10]:
                    overview.append(f"  - {header.strip()}")

        # Default
        if not overview:
            overview.append("Source code file with no automatic analysis available.")

        return '\n'.join(overview)

    def process_file(self, file_path: Path) -> Dict:
        """
        Process a single file: read, document, and upload.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with processing results
        """
        result = {
            'file': str(file_path),
            'uploaded_source': False,
            'uploaded_docs': False,
            'error': None
        }

        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {file_path.name}")
        logger.info(f"{'='*60}")

        try:
            # Step 1: Upload the original source file
            logger.info(f"[1/3] Uploading source file...")
            upload_result = upload_document(
                str(file_path),
                metadata={
                    'type': 'source_code',
                    'project': self.source_dir.name
                }
            )
            result['uploaded_source'] = True
            logger.info(f"✓ Source file uploaded successfully")

            # Step 2: Generate documentation
            logger.info(f"[2/3] Generating documentation...")
            documentation = self.generate_simple_documentation(file_path)

            if documentation:
                # Save documentation to temp file
                doc_file = file_path.parent / f"{file_path.stem}_AUTO_DOC.md"
                with open(doc_file, 'w', encoding='utf-8') as f:
                    f.write(documentation)
                logger.info(f"✓ Documentation generated: {doc_file.name}")

                # Step 3: Upload the documentation
                logger.info(f"[3/3] Uploading documentation...")
                doc_result = upload_document(
                    str(doc_file),
                    metadata={
                        'type': 'documentation',
                        'source_file': str(file_path),
                        'project': self.source_dir.name,
                        'auto_generated': True
                    }
                )
                result['uploaded_docs'] = True
                logger.info(f"✓ Documentation uploaded successfully")

                # Clean up temp file (optional - keep for reference)
                # doc_file.unlink()
            else:
                logger.warning(f"⚠ Could not generate documentation")

            self.uploaded_files.append(file_path)
            return result

        except Exception as e:
            logger.error(f"✗ Error processing {file_path}: {e}")
            result['error'] = str(e)
            self.failed_files.append((file_path, str(e)))
            return result

    def process_directory(self, pattern: str = "**/*.py") -> List[Dict]:
        """
        Process all files matching pattern in the source directory.

        Args:
            pattern: Glob pattern for files to process

        Returns:
            List of processing results
        """
        files = list(self.source_dir.glob(pattern))
        logger.info(f"Found {len(files)} files matching pattern: {pattern}")

        results = []
        for file_path in files:
            # Skip __pycache__ and other unwanted directories
            if '__pycache__' in str(file_path) or '.egg-info' in str(file_path):
                continue

            result = self.process_file(file_path)
            results.append(result)

        return results

    def print_summary(self):
        """Print a summary of the processing."""
        logger.info(f"\n{'='*60}")
        logger.info(f"PROCESSING SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"✓ Successfully uploaded: {len(self.uploaded_files)} files")

        if self.failed_files:
            logger.info(f"✗ Failed: {len(self.failed_files)} files")
            for file_path, error in self.failed_files:
                logger.info(f"  - {file_path.name}: {error}")
        else:
            logger.info(f"✓ No failures!")

        logger.info(f"{'='*60}\n")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Automatically document and upload source files to RAG system'
    )
    parser.add_argument(
        'directory',
        help='Directory containing source files'
    )
    parser.add_argument(
        '--pattern',
        default='**/*.py',
        help='Glob pattern for files to process (default: **/*.py)'
    )
    parser.add_argument(
        '--multiple-patterns',
        nargs='+',
        help='Multiple patterns to process (e.g., "**/*.py" "**/*.cpp" "**/*.h")'
    )

    args = parser.parse_args()

    # Create uploader
    uploader = AutoDocUploader(args.directory)

    # Process files
    if args.multiple_patterns:
        logger.info(f"Processing multiple patterns: {args.multiple_patterns}")
        for pattern in args.multiple_patterns:
            logger.info(f"\n--- Processing pattern: {pattern} ---")
            uploader.process_directory(pattern)
    else:
        uploader.process_directory(args.pattern)

    # Print summary
    uploader.print_summary()

    return 0 if not uploader.failed_files else 1


if __name__ == '__main__':
    sys.exit(main())

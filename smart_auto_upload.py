"""
Smart Auto-Upload with Inline Documentation

This script reads source files, extracts meaningful information,
and uploads both source and generated docs automatically.
"""

import os
import sys
import ast
import re
from pathlib import Path
from typing import List, Dict, Optional
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
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class PythonAnalyzer:
    """Analyzes Python files and extracts documentation."""

    @staticmethod
    def analyze_file(file_path: Path) -> Dict:
        """Analyze a Python file and extract key information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            info = {
                'imports': [],
                'classes': [],
                'functions': [],
                'module_docstring': ast.get_docstring(tree) or "No module documentation available."
            }

            for node in ast.walk(tree):
                # Extract imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        info['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        info['imports'].append(f"{module}.{alias.name}")

                # Extract classes
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'docstring': ast.get_docstring(node) or "No documentation",
                        'methods': []
                    }
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info['methods'].append({
                                'name': item.name,
                                'docstring': ast.get_docstring(item) or "No documentation"
                            })
                    info['classes'].append(class_info)

                # Extract top-level functions
                elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                    func_info = {
                        'name': node.name,
                        'docstring': ast.get_docstring(node) or "No documentation",
                        'args': [arg.arg for arg in node.args.args]
                    }
                    info['functions'].append(func_info)

            return info

        except Exception as e:
            logger.warning(f"Could not parse {file_path}: {e}")
            return None

    @staticmethod
    def generate_documentation(file_path: Path, analysis: Dict) -> str:
        """Generate markdown documentation from analysis."""
        doc = f"""# {file_path.name}

## Module Overview

{analysis['module_docstring']}

**File**: `{file_path}`

---

"""

        # Imports
        if analysis['imports']:
            doc += "## Dependencies\n\n"
            unique_imports = sorted(set(analysis['imports']))
            for imp in unique_imports[:20]:  # Limit to 20
                doc += f"- `{imp}`\n"
            if len(unique_imports) > 20:
                doc += f"\n*...and {len(unique_imports) - 20} more*\n"
            doc += "\n"

        # Classes
        if analysis['classes']:
            doc += "## Classes\n\n"
            for cls in analysis['classes']:
                doc += f"### `{cls['name']}`\n\n"
                doc += f"{cls['docstring']}\n\n"

                if cls['methods']:
                    doc += "**Methods**:\n\n"
                    for method in cls['methods']:
                        doc += f"- `{method['name']}()`: {method['docstring']}\n"
                    doc += "\n"

        # Functions
        if analysis['functions']:
            doc += "## Functions\n\n"
            for func in analysis['functions']:
                args_str = ', '.join(func['args'])
                doc += f"### `{func['name']}({args_str})`\n\n"
                doc += f"{func['docstring']}\n\n"

        doc += """---

*This documentation was automatically generated from source code analysis.*
"""

        return doc


class SmartAutoUploader:
    """Smart auto-uploader with content analysis."""

    def __init__(self, source_dir: str, auto_upload: bool = True):
        """
        Initialize the smart uploader.

        Args:
            source_dir: Directory containing source files
            auto_upload: If True, uploads files immediately after processing
        """
        self.source_dir = Path(source_dir)
        self.auto_upload = auto_upload
        self.processed_files = []
        self.failed_files = []
        self.python_analyzer = PythonAnalyzer()

    def process_python_file(self, file_path: Path) -> bool:
        """Process a Python file: analyze, document, upload."""
        logger.info(f"\n📄 Processing: {file_path.relative_to(self.source_dir)}")

        try:
            # Step 1: Upload source file
            if self.auto_upload:
                logger.info("  [1/3] Uploading source file...")
                upload_document(
                    str(file_path),
                    metadata={
                        'type': 'source_code',
                        'language': 'python',
                        'project': self.source_dir.name,
                        'relative_path': str(file_path.relative_to(self.source_dir))
                    }
                )
                logger.info("  ✓ Source uploaded")

            # Step 2: Analyze and generate documentation
            logger.info("  [2/3] Analyzing Python code...")
            analysis = self.python_analyzer.analyze_file(file_path)

            if analysis:
                documentation = self.python_analyzer.generate_documentation(file_path, analysis)

                # Save documentation
                doc_file = file_path.parent / f"{file_path.stem}_DOCS.md"
                with open(doc_file, 'w', encoding='utf-8') as f:
                    f.write(documentation)
                logger.info(f"  ✓ Documentation generated")

                # Step 3: Upload documentation
                if self.auto_upload:
                    logger.info("  [3/3] Uploading documentation...")
                    upload_document(
                        str(doc_file),
                        metadata={
                            'type': 'documentation',
                            'source_file': str(file_path),
                            'language': 'markdown',
                            'project': self.source_dir.name,
                            'auto_generated': True
                        }
                    )
                    logger.info("  ✓ Documentation uploaded")
            else:
                logger.warning("  ⚠ Could not analyze file")

            self.processed_files.append(file_path)
            return True

        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
            self.failed_files.append((file_path, str(e)))
            return False

    def process_markdown_file(self, file_path: Path) -> bool:
        """Process a markdown file: just upload as-is."""
        logger.info(f"\n📄 Processing: {file_path.relative_to(self.source_dir)}")

        try:
            if self.auto_upload:
                logger.info("  [1/1] Uploading markdown file...")
                upload_document(
                    str(file_path),
                    metadata={
                        'type': 'documentation',
                        'language': 'markdown',
                        'project': self.source_dir.name,
                        'relative_path': str(file_path.relative_to(self.source_dir))
                    }
                )
                logger.info("  ✓ Uploaded")

            self.processed_files.append(file_path)
            return True

        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
            self.failed_files.append((file_path, str(e)))
            return False

    def process_directory(self, patterns: List[str] = None):
        """Process all files matching patterns."""
        if patterns is None:
            patterns = ['**/*.py', '**/*.md']

        all_files = []
        for pattern in patterns:
            files = list(self.source_dir.glob(pattern))
            all_files.extend(files)

        # Remove duplicates and filter
        all_files = [f for f in set(all_files)
                     if '__pycache__' not in str(f)
                     and '.egg-info' not in str(f)
                     and not f.name.endswith('_DOCS.md')]

        logger.info(f"\n{'='*70}")
        logger.info(f"📦 Found {len(all_files)} files to process")
        logger.info(f"{'='*70}\n")

        for file_path in all_files:
            ext = file_path.suffix.lower()

            if ext == '.py':
                self.process_python_file(file_path)
            elif ext in ['.md', '.markdown']:
                self.process_markdown_file(file_path)
            else:
                logger.info(f"\n📄 Skipping: {file_path.name} (unsupported type)")

    def print_summary(self):
        """Print processing summary."""
        logger.info(f"\n{'='*70}")
        logger.info(f"📊 SUMMARY")
        logger.info(f"{'='*70}")
        logger.info(f"✓ Successfully processed: {len(self.processed_files)} files")

        if self.failed_files:
            logger.info(f"✗ Failed: {len(self.failed_files)} files")
            for file_path, error in self.failed_files:
                logger.info(f"  - {file_path.name}: {error}")

        logger.info(f"{'='*70}\n")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Smart auto-document and upload tool with code analysis'
    )
    parser.add_argument(
        'directory',
        help='Directory containing source files'
    )
    parser.add_argument(
        '--patterns',
        nargs='+',
        default=['**/*.py', '**/*.md'],
        help='File patterns to process (default: **/*.py **/*.md)'
    )
    parser.add_argument(
        '--no-upload',
        action='store_true',
        help='Generate docs only, do not upload'
    )

    args = parser.parse_args()

    # Create uploader
    uploader = SmartAutoUploader(
        args.directory,
        auto_upload=not args.no_upload
    )

    # Process files
    uploader.process_directory(args.patterns)

    # Print summary
    uploader.print_summary()

    return 0 if not uploader.failed_files else 1


if __name__ == '__main__':
    sys.exit(main())

"""
C++ Parser using tree-sitter

Extracts structure information from C++ code:
- Project structure (directories, modules)
- Classes and their methods
- Functions
- Dependencies
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from glob import glob

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.parser')


class CppParser:
    """
    Parser for C++ code to extract structure and API information.

    Uses tree-sitter for accurate parsing, with fallback to regex-based parsing.
    """

    def __init__(self, include_patterns=None, exclude_patterns=None):
        self.include_patterns = include_patterns or ['**/*.h', '**/*.hpp', '**/*.cpp']
        self.exclude_patterns = exclude_patterns or ['**/build/**', '**/third_party/**']

        # Try to initialize tree-sitter
        self.tree_sitter_available = False
        try:
            import tree_sitter
            import tree_sitter_cpp
            self.tree_sitter = tree_sitter
            self.cpp_language = tree_sitter.Language(tree_sitter_cpp.language())
            self.parser = tree_sitter.Parser(self.cpp_language)
            self.tree_sitter_available = True
            logger.info("Tree-sitter C++ parser initialized")
        except ImportError:
            logger.warning("Tree-sitter not available, using fallback regex parser")

    def _is_excluded(self, file_path: Path, project_path: Path) -> bool:
        """
        Check if a file should be excluded based on exclude patterns.

        Supports glob patterns including:
        - **/build/** - Recursively excludes 'build' directories and their contents
        - **/*.pyc - Recursively excludes all .pyc files
        - **/node_modules/** - Recursively excludes 'node_modules' directories
        - .git/** - Excludes .git directory from project root

        Args:
            file_path: Absolute path to the file
            project_path: Root path of the project

        Returns:
            True if the file should be excluded, False otherwise
        """
        try:
            # Get relative path from project root for pattern matching
            relative_path = file_path.relative_to(project_path)
            relative_path_str = relative_path.as_posix()  # Use forward slashes for matching

            # Check each exclusion pattern
            for exclude_pattern in self.exclude_patterns:
                # Normalize pattern to use forward slashes
                pattern = exclude_pattern.replace('\\', '/')

                # Direct match using Path.match()
                if relative_path.match(pattern):
                    return True

                # Handle directory patterns like **/build/** or **/node_modules/**
                # These should match any file inside those directories
                if pattern.startswith('**/') and pattern.endswith('/**'):
                    # Extract directory name
                    dir_name = pattern[3:-3]  # Remove **/ and /**

                    # Check if the directory appears anywhere in the path
                    path_parts = relative_path.parts
                    if dir_name in path_parts:
                        return True

                # Handle patterns like **/.git/** that start with .
                elif pattern.startswith('**/') and '/**' in pattern:
                    # Extract directory name
                    dir_name = pattern[3:].rstrip('/**').rstrip('/*')

                    # Check if the directory appears anywhere in the path
                    path_parts = relative_path.parts
                    if dir_name in path_parts:
                        return True

        except ValueError:
            # file_path is not relative to project_path
            pass

        return False

    def parse_project_structure(self, project_path: str) -> Dict[str, Any]:
        """
        Parse entire C++ project structure.

        Args:
            project_path: Root path of the C++ project

        Returns:
            Dictionary containing:
            - all_files: List of all C++ files
            - modules: List of detected modules
            - directory_tree: Text representation of directory structure
            - dependencies: External dependencies
        """
        project_path = Path(project_path).resolve()

        logger.info(f"Parsing project structure: {project_path}")

        # Find all C++ files
        all_files = self._find_cpp_files(project_path)
        logger.info(f"Found {len(all_files)} C++ files")

        # Detect modules (directories with header files)
        modules = self._detect_modules(project_path, all_files)
        logger.info(f"Detected {len(modules)} modules")

        # Create directory tree
        directory_tree = self._create_directory_tree(project_path, all_files)

        # Detect dependencies (basic analysis)
        dependencies = self._detect_dependencies(all_files)

        return {
            'project_path': str(project_path),
            'all_files': all_files,
            'modules': modules,
            'directory_tree': directory_tree,
            'dependencies': dependencies,
        }

    def parse_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single C++ file.

        Args:
            file_path: Path to the C++ file

        Returns:
            Dictionary containing:
            - path: File path
            - classes: List of classes with methods
            - functions: List of standalone functions
            - includes: List of included files
        """
        file_path = Path(file_path)

        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None

        if self.tree_sitter_available:
            return self._parse_file_treesitter(file_path, content)
        else:
            return self._parse_file_regex(file_path, content)

    def find_all_source_files(self, project_path: Path) -> List[str]:
        """
        Find ALL source files matching include patterns (not just C++).
        This is useful for uploading all project files to RAG systems.
        """
        all_files = []

        for pattern in self.include_patterns:
            search_pattern = str(project_path / pattern)
            files = glob(search_pattern, recursive=True)
            all_files.extend(files)

        # Remove duplicates and excluded files
        all_files = list(set(all_files))
        filtered_files = []

        for file in all_files:
            # Skip directories
            if not Path(file).is_file():
                continue

            # Check if file should be excluded using proper glob pattern matching
            excluded = self._is_excluded(Path(file), project_path)

            if not excluded:
                filtered_files.append(file)

        return sorted(filtered_files)

    def _find_cpp_files(self, project_path: Path) -> List[str]:
        """Find all C++ files matching include patterns"""
        all_files = []

        for pattern in self.include_patterns:
            search_pattern = str(project_path / pattern)
            files = glob(search_pattern, recursive=True)
            all_files.extend(files)

        # Remove duplicates and excluded files
        all_files = list(set(all_files))
        filtered_files = []

        for file in all_files:
            # Check if file should be excluded using proper glob pattern matching
            excluded = self._is_excluded(Path(file), project_path)

            if not excluded:
                filtered_files.append(file)

        return sorted(filtered_files)

    def _detect_modules(self, project_path: Path, files: List[str]) -> List[Dict[str, Any]]:
        """
        Detect modules based on directory structure.

        A module is typically a directory containing header files.
        """
        modules = {}

        for file in files:
            file_path = Path(file)
            relative_path = file_path.relative_to(project_path)

            # Get the immediate subdirectory as module name
            parts = relative_path.parts
            if len(parts) > 1:
                module_name = parts[0]
            else:
                module_name = 'root'

            if module_name not in modules:
                modules[module_name] = {
                    'name': module_name,
                    'path': str(project_path / module_name) if module_name != 'root' else str(project_path),
                    'files': [],
                    'classes': [],
                    'dependencies': [],
                }

            modules[module_name]['files'].append(file)

        return list(modules.values())

    def _create_directory_tree(self, project_path: Path, files: List[str]) -> str:
        """Create a text representation of the directory tree"""
        tree_lines = []

        # Group files by directory
        dirs = {}
        for file in files[:50]:  # Limit to avoid huge output
            file_path = Path(file)
            try:
                relative = file_path.relative_to(project_path)
                dir_path = relative.parent
                file_name = relative.name

                if str(dir_path) not in dirs:
                    dirs[str(dir_path)] = []
                dirs[str(dir_path)].append(file_name)
            except ValueError:
                continue

        # Sort and format
        for dir_path in sorted(dirs.keys()):
            if dir_path == '.':
                tree_lines.append('.')
            else:
                tree_lines.append(f"{dir_path}/")

            for file_name in sorted(dirs[dir_path])[:5]:  # Limit files per dir
                tree_lines.append(f"  {file_name}")

            if len(dirs[dir_path]) > 5:
                tree_lines.append(f"  ... and {len(dirs[dir_path]) - 5} more files")

        if len(files) > 50:
            tree_lines.append(f"\n... and {len(files) - 50} more files not shown")

        return '\n'.join(tree_lines)

    def _detect_dependencies(self, files: List[str]) -> Dict[str, List[str]]:
        """Detect external dependencies from include statements"""
        system_includes = set()
        local_includes = set()

        for file in files[:100]:  # Sample files
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Find includes
                for match in re.finditer(r'#include\s*[<"]([^>"]+)[>"]', content):
                    include = match.group(1)
                    if match.group(0).find('<') != -1:
                        # System include
                        base = include.split('/')[0]
                        if base not in ['std', 'cstdlib', 'iostream', 'string', 'vector', 'map']:
                            system_includes.add(base)
                    else:
                        local_includes.add(include)

            except Exception:
                continue

        return {
            'system': sorted(list(system_includes)),
            'local': sorted(list(local_includes))[:20],  # Limit output
        }

    def _parse_file_treesitter(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Parse file using tree-sitter"""
        try:
            tree = self.parser.parse(bytes(content, 'utf8'))
            root_node = tree.root_node

            classes = []
            functions = []
            includes = []

            # Query for different constructs
            self._extract_classes_ts(root_node, content, classes)
            self._extract_functions_ts(root_node, content, functions)
            self._extract_includes_ts(root_node, content, includes)

            return {
                'path': str(file_path),
                'classes': classes,
                'functions': functions,
                'includes': includes,
            }
        except Exception as e:
            logger.warning(f"Tree-sitter parsing failed for {file_path}: {e}, falling back to regex")
            return self._parse_file_regex(file_path, content)

    def _extract_classes_ts(self, node, content: str, classes: List[Dict]):
        """Extract class information using tree-sitter"""
        if node.type == 'class_specifier':
            class_info = self._parse_class_node(node, content)
            if class_info:
                classes.append(class_info)

        for child in node.children:
            self._extract_classes_ts(child, content, classes)

    def _parse_class_node(self, node, content: str) -> Optional[Dict]:
        """Parse a class node"""
        class_name = None
        methods = []
        base_classes = []

        # Find class name
        for child in node.children:
            if child.type == 'type_identifier':
                class_name = content[child.start_byte:child.end_byte]
                break

        if not class_name:
            return None

        # Find methods in class body
        for child in node.children:
            if child.type == 'field_declaration_list':
                for item in child.children:
                    if item.type in ['function_definition', 'declaration']:
                        method = self._parse_method_node(item, content)
                        if method:
                            methods.append(method)

        header_code = content[node.start_byte:min(node.end_byte, node.start_byte + 500)]

        return {
            'name': class_name,
            'methods': methods,
            'base_classes': base_classes,
            'header_code': header_code,
        }

    def _parse_method_node(self, node, content: str) -> Optional[Dict]:
        """Parse a method/function node"""
        # This is simplified - full implementation would extract all details
        method_text = content[node.start_byte:node.end_byte]

        # Basic extraction
        name_match = re.search(r'\b(\w+)\s*\(', method_text)
        if not name_match:
            return None

        return {
            'name': name_match.group(1),
            'return_type': 'auto',  # Simplified
            'parameters': [],
            'visibility': 'public',  # Would need more complex logic
        }

    def _extract_functions_ts(self, node, content: str, functions: List[Dict]):
        """Extract function information using tree-sitter"""
        if node.type == 'function_definition':
            func_info = self._parse_function_node(node, content)
            if func_info:
                functions.append(func_info)

        for child in node.children:
            self._extract_functions_ts(child, content, functions)

    def _parse_function_node(self, node, content: str) -> Optional[Dict]:
        """Parse a function node"""
        func_text = content[node.start_byte:min(node.end_byte, node.start_byte + 300)]

        name_match = re.search(r'\b(\w+)\s*\(', func_text)
        if not name_match:
            return None

        return {
            'name': name_match.group(1),
            'return_type': 'auto',
            'parameters': [],
            'code': func_text,
        }

    def _extract_includes_ts(self, node, content: str, includes: List[str]):
        """Extract include statements using tree-sitter"""
        if node.type == 'preproc_include':
            include_text = content[node.start_byte:node.end_byte]
            match = re.search(r'#include\s*[<"]([^>"]+)[>"]', include_text)
            if match:
                includes.append(match.group(1))

        for child in node.children:
            self._extract_includes_ts(child, content, includes)

    def _parse_file_regex(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Fallback regex-based parser"""
        classes = []
        functions = []
        includes = []

        # Extract includes
        for match in re.finditer(r'#include\s*[<"]([^>"]+)[>"]', content):
            includes.append(match.group(1))

        # Extract classes (simplified)
        for match in re.finditer(r'class\s+(\w+)(?:\s*:\s*public\s+(\w+))?\s*\{', content):
            class_name = match.group(1)
            base_class = match.group(2)

            # Try to find methods (very simplified)
            class_start = match.end()
            class_end = content.find('};', class_start)
            if class_end != -1:
                class_body = content[class_start:class_end]
                methods = []

                for method_match in re.finditer(r'(\w+)\s+(\w+)\s*\([^)]*\)', class_body):
                    methods.append({
                        'name': method_match.group(2),
                        'return_type': method_match.group(1),
                        'parameters': [],
                        'visibility': 'public',
                    })

                header_code = content[match.start():min(match.end() + 500, class_end)]

                classes.append({
                    'name': class_name,
                    'methods': methods,
                    'base_classes': [base_class] if base_class else [],
                    'header_code': header_code,
                })

        # Extract standalone functions
        for match in re.finditer(r'^(\w+)\s+(\w+)\s*\([^)]*\)\s*\{', content, re.MULTILINE):
            return_type = match.group(1)
            func_name = match.group(2)

            # Skip if it looks like a method (inside a class)
            if not any(class_name in content[max(0, match.start()-100):match.start()] for class_name in [c['name'] for c in classes]):
                func_code = content[match.start():min(match.end() + 200, len(content))]

                functions.append({
                    'name': func_name,
                    'return_type': return_type,
                    'parameters': [],
                    'code': func_code,
                })

        return {
            'path': str(file_path),
            'classes': classes,
            'functions': functions,
            'includes': includes,
        }

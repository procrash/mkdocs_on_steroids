"""
High-Level Documentation Agent

Generates project overview and architecture documentation.
Creates 300-word introductions with architecture diagrams.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter

from ..utils.prompt_manager import get_prompt_manager

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.high-level')


class HighLevelAgent:
    """
    Agent for generating high-level project documentation.

    Creates:
    - Project overview (00-getting-started.md)
    - Architecture documentation (01-architecture.md)
    - Filesystem structure (02-filesystem-structure.md)
    - Technology stack overview
    - Entry points for new developers
    """

    def __init__(self, llm_provider, cache_manager):
        self.llm = llm_provider
        self.cache = cache_manager
        self.prompt_manager = get_prompt_manager()

    def generate(self, project_structure: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate high-level documentation files.

        Args:
            project_structure: Parsed C++ project structure
            output_dir: Directory to write documentation files

        Returns:
            List of generated file paths
        """
        generated_files = []
        output_path = Path(output_dir)

        # Generate Getting Started
        getting_started_file = output_path / '00-getting-started.md'
        content = self._generate_getting_started(project_structure)
        getting_started_file.write_text(content, encoding='utf-8')
        generated_files.append(str(getting_started_file))
        logger.info(f"Generated: {getting_started_file}")

        # Generate Architecture Documentation
        architecture_file = output_path / '01-architecture.md'
        content = self._generate_architecture(project_structure)
        architecture_file.write_text(content, encoding='utf-8')
        generated_files.append(str(architecture_file))
        logger.info(f"Generated: {architecture_file}")

        # Generate Filesystem Structure Documentation
        filesystem_file = output_path / '02-filesystem-structure.md'
        content = self._generate_filesystem_structure(project_structure)
        filesystem_file.write_text(content, encoding='utf-8')
        generated_files.append(str(filesystem_file))
        logger.info(f"Generated: {filesystem_file}")

        return generated_files

    def _generate_getting_started(self, project_structure: Dict[str, Any]) -> str:
        """Generate getting started documentation"""

        prompt = self._build_getting_started_prompt(project_structure)

        # Check cache
        cache_key = f"high_level_getting_started_{hash(str(project_structure))}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info("Using cached getting started documentation")
            return cached

        # Generate with LLM
        response = self.llm.generate(prompt)

        # Cache result
        self.cache.set(cache_key, response)

        return response

    def _generate_architecture(self, project_structure: Dict[str, Any]) -> str:
        """Generate architecture documentation"""

        prompt = self._build_architecture_prompt(project_structure)

        # Check cache
        cache_key = f"high_level_architecture_{hash(str(project_structure))}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info("Using cached architecture documentation")
            return cached

        # Generate with LLM
        response = self.llm.generate(prompt)

        # Cache result
        self.cache.set(cache_key, response)

        return response

    def _build_getting_started_prompt(self, project_structure: Dict[str, Any]) -> str:
        """Build prompt for getting started documentation"""

        structure_summary = self._summarize_structure(project_structure)
        entry_points = ', '.join(project_structure.get('entry_points', ['main.cpp']))

        # Use PromptManager to get template
        prompt = self.prompt_manager.get_prompt(
            'high_level', 'getting_started',
            project_structure=structure_summary,
            entry_points=entry_points
        )

        return prompt

    def _build_architecture_prompt(self, project_structure: Dict[str, Any]) -> str:
        """Build prompt for architecture documentation"""

        structure_summary = self._summarize_structure(project_structure)
        modules = project_structure.get('modules', [])
        modules_str = ', '.join([m.get('name', 'unknown') for m in modules[:10]])

        # Use PromptManager to get template
        prompt = self.prompt_manager.get_prompt(
            'high_level', 'architecture',
            project_structure=structure_summary,
            modules=modules_str
        )

        return prompt

    def _generate_filesystem_structure(self, project_structure: Dict[str, Any]) -> str:
        """Generate filesystem structure documentation"""

        prompt = self._build_filesystem_structure_prompt(project_structure)

        # Check cache
        cache_key = f"high_level_filesystem_{hash(str(project_structure))}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info("Using cached filesystem structure documentation")
            return cached

        # Generate with LLM
        response = self.llm.generate(prompt)

        # Cache result
        self.cache.set(cache_key, response)

        return response

    def _build_filesystem_structure_prompt(self, project_structure: Dict[str, Any]) -> str:
        """Build prompt for filesystem structure documentation"""

        all_files = project_structure.get('all_files', [])

        # Build directory tree
        directory_tree = self._build_directory_tree(all_files)

        # Calculate file statistics
        file_statistics = self._calculate_file_statistics(all_files)

        # Identify key directories
        key_directories = self._identify_key_directories(all_files)

        # Count unique directories
        unique_dirs = set()
        for file_path in all_files:
            unique_dirs.add(str(Path(file_path).parent))

        # Get project root
        project_root = project_structure.get('root_path', './')

        # Use PromptManager to get template
        prompt = self.prompt_manager.get_prompt(
            'high_level', 'filesystem_structure',
            project_root=project_root,
            total_files=len(all_files),
            total_directories=len(unique_dirs),
            directory_tree=directory_tree,
            file_statistics=file_statistics,
            key_directories=key_directories
        )

        return prompt

    def _build_directory_tree(self, all_files: List[str]) -> str:
        """Build ASCII directory tree from file list"""
        if not all_files:
            return "No files found"

        # Group files by directory
        dir_structure = {}
        for file_path in all_files:
            path = Path(file_path)
            parts = path.parts

            current = dir_structure
            for part in parts[:-1]:  # Directories
                if part not in current:
                    current[part] = {}
                current = current[part]

            # Add file
            if '__files__' not in current:
                current['__files__'] = []
            current['__files__'].append(parts[-1])

        # Build tree string
        def build_tree_recursive(structure: Dict, prefix: str = "", is_last: bool = True) -> List[str]:
            lines = []
            items = [(k, v) for k, v in structure.items() if k != '__files__']
            files = structure.get('__files__', [])

            # Process directories
            for idx, (name, subtree) in enumerate(items):
                is_last_item = (idx == len(items) - 1) and not files
                connector = "└── " if is_last_item else "├── "
                lines.append(f"{prefix}{connector}{name}/")

                extension = "    " if is_last_item else "│   "
                lines.extend(build_tree_recursive(subtree, prefix + extension, is_last_item))

            # Process files (show first 10)
            for idx, file_name in enumerate(files[:10]):
                is_last_file = idx == len(files[:10]) - 1
                connector = "└── " if is_last_file else "├── "
                lines.append(f"{prefix}{connector}{file_name}")

            if len(files) > 10:
                lines.append(f"{prefix}... ({len(files) - 10} more files)")

            return lines

        tree_lines = build_tree_recursive(dir_structure)
        return '\n'.join(tree_lines[:100])  # Limit to 100 lines

    def _calculate_file_statistics(self, all_files: List[str]) -> str:
        """Calculate file type statistics"""
        if not all_files:
            return "No files to analyze"

        # Count by extension
        extensions = Counter()
        for file_path in all_files:
            ext = Path(file_path).suffix
            if ext:
                extensions[ext] += 1
            else:
                extensions['(no extension)'] += 1

        # Build statistics table
        lines = ["| File Type | Count | Percentage |"]
        lines.append("|-----------|-------|------------|")

        total = len(all_files)
        for ext, count in extensions.most_common(10):
            percentage = (count / total) * 100
            lines.append(f"| `{ext}` | {count} | {percentage:.1f}% |")

        if len(extensions) > 10:
            lines.append(f"| _(others)_ | {sum(c for e, c in extensions.most_common()[10:])} | ... |")

        return '\n'.join(lines)

    def _identify_key_directories(self, all_files: List[str]) -> str:
        """Identify and describe key directories"""
        if not all_files:
            return "No directories to analyze"

        # Count files per directory
        dir_counts = Counter()
        for file_path in all_files:
            dir_path = str(Path(file_path).parent)
            dir_counts[dir_path] += 1

        # Build key directories table
        lines = ["| Directory | Files | Description |"]
        lines.append("|-----------|-------|-------------|")

        for dir_path, count in dir_counts.most_common(10):
            dir_name = Path(dir_path).name or "root"

            # Infer description from directory name
            description = self._infer_directory_purpose(dir_name)

            lines.append(f"| `{dir_name}/` | {count} | {description} |")

        return '\n'.join(lines)

    def _infer_directory_purpose(self, dir_name: str) -> str:
        """Infer directory purpose from name"""
        dir_lower = dir_name.lower()

        if dir_lower in ['src', 'source', 'sources']:
            return "Source code"
        elif dir_lower in ['include', 'includes', 'headers']:
            return "Header files"
        elif dir_lower in ['test', 'tests', 'testing']:
            return "Unit tests"
        elif dir_lower in ['doc', 'docs', 'documentation']:
            return "Documentation"
        elif dir_lower in ['build', 'bin', 'out', 'output']:
            return "Build output"
        elif dir_lower in ['lib', 'libs', 'library', 'libraries']:
            return "Libraries"
        elif dir_lower in ['tools', 'utils', 'utilities']:
            return "Utilities"
        elif dir_lower in ['examples', 'samples', 'demo']:
            return "Examples/demos"
        elif dir_lower in ['third_party', 'external', 'vendor']:
            return "Third-party code"
        elif dir_lower in ['cmake', 'config', 'conf']:
            return "Configuration"
        else:
            return "Project files"

    def _summarize_structure(self, project_structure: Dict[str, Any]) -> str:
        """Create a text summary of the project structure"""
        lines = []

        lines.append(f"**Total Files**: {len(project_structure.get('all_files', []))}")
        lines.append(f"**Modules**: {len(project_structure.get('modules', []))}")

        # File types
        headers = len([f for f in project_structure.get('all_files', []) if f.endswith(('.h', '.hpp'))])
        sources = len([f for f in project_structure.get('all_files', []) if f.endswith('.cpp')])
        lines.append(f"**Header Files**: {headers}")
        lines.append(f"**Source Files**: {sources}")

        # Directory structure
        if 'directory_tree' in project_structure:
            lines.append("\n**Directory Structure**:")
            lines.append("```")
            lines.append(project_structure['directory_tree'])
            lines.append("```")

        return '\n'.join(lines)

    def _format_modules(self, modules: List[Dict]) -> str:
        """Format modules for the prompt"""
        if not modules:
            return "No modules identified"

        lines = []
        for module in modules:
            lines.append(f"- **{module['name']}**: {len(module.get('files', []))} files")
            if module.get('path'):
                lines.append(f"  - Path: `{module['path']}`")

        return '\n'.join(lines)

    def _format_dependencies(self, dependencies: Dict) -> str:
        """Format dependencies for the prompt"""
        if not dependencies:
            return "No external dependencies identified"

        lines = []
        for dep_type, deps in dependencies.items():
            lines.append(f"**{dep_type}**: {', '.join(deps)}")

        return '\n'.join(lines)

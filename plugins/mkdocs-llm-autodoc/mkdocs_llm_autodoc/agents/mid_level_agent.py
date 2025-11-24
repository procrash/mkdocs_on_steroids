"""
Mid-Level Documentation Agent

Generates module-level documentation covering:
- Module overview
- Main classes and their responsibilities
- Interactions with other modules
- Typical usage scenarios
"""

import logging
from pathlib import Path
from typing import Dict, List, Any

from ..utils.prompt_manager import get_prompt_manager

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.mid-level')


class MidLevelAgent:
    """
    Agent for generating mid-level module documentation.

    Creates documentation for each module/component with:
    - 100-word overview
    - Class responsibilities
    - Module interactions
    - Usage scenarios
    """

    def __init__(self, llm_provider, cache_manager, cross_ref_manager):
        self.llm = llm_provider
        self.cache = cache_manager
        self.cross_ref = cross_ref_manager
        self.prompt_manager = get_prompt_manager()

    def generate(self, module: Dict[str, Any], project_structure: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate module documentation.

        Args:
            module: Module information (name, files, classes, etc.)
            project_structure: Full project structure for context
            output_dir: Directory to write documentation

        Returns:
            List of generated file paths
        """
        generated_files = []
        output_path = Path(output_dir)

        module_name = module['name']
        safe_name = self._sanitize_filename(module_name)

        module_file = output_path / f"{safe_name}.md"
        content = self._generate_module_doc(module, project_structure)
        module_file.write_text(content, encoding='utf-8')
        generated_files.append(str(module_file))

        logger.info(f"Generated module documentation: {module_file}")

        return generated_files

    def _generate_module_doc(self, module: Dict[str, Any], project_structure: Dict[str, Any]) -> str:
        """Generate documentation for a module"""

        prompt = self._build_module_prompt(module, project_structure)

        # Check cache
        cache_key = f"mid_level_{module['name']}_{hash(str(module))}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Using cached documentation for module: {module['name']}")
            return cached

        # Generate with LLM
        response = self.llm.generate(prompt)

        # Cache result
        self.cache.set(cache_key, response)

        # Register for cross-referencing
        self.cross_ref.register_module(module['name'], response)

        return response

    def _build_module_prompt(self, module: Dict[str, Any], project_structure: Dict[str, Any]) -> str:
        """Build prompt for module documentation"""

        module_name = module['name']
        module_files = module.get('files', [])
        module_files_str = ', '.join([str(Path(f).name) for f in module_files[:10]])
        if len(module_files) > 10:
            module_files_str += f" (and {len(module_files) - 10} more)"

        classes = module.get('classes', [])
        module_classes_str = ', '.join([c.get('name', 'unknown') for c in classes[:10]])
        if len(classes) > 10:
            module_classes_str += f" (and {len(classes) - 10} more)"

        # Use PromptManager to get template
        prompt = self.prompt_manager.get_prompt(
            'mid_level', 'module',
            module_name=module_name,
            module_files=module_files_str,
            module_classes=module_classes_str,
            project_structure=str(project_structure)
        )

        return prompt

    def _format_file_list(self, files: List[str]) -> str:
        """Format file list for prompt"""
        if not files:
            return "No files"

        lines = []
        for file in files[:20]:  # Limit to avoid huge prompts
            lines.append(f"- `{file}`")

        if len(files) > 20:
            lines.append(f"... and {len(files) - 20} more files")

        return '\n'.join(lines)

    def _format_class_list(self, classes: List[Dict]) -> str:
        """Format class list for prompt"""
        if not classes:
            return "No classes identified yet (will be parsed from code)"

        lines = []
        for cls in classes:
            name = cls.get('name', 'Unknown')
            methods = len(cls.get('methods', []))
            lines.append(f"- **{name}**: {methods} methods")

        return '\n'.join(lines)

    def _format_dependencies(self, dependencies: List[str]) -> str:
        """Format dependencies for prompt"""
        if not dependencies:
            return "No external dependencies identified"

        return '\n'.join(f"- {dep}" for dep in dependencies)

    def _format_project_context(self, project_structure: Dict[str, Any], current_module: str) -> str:
        """Provide context about other modules in the project"""
        modules = project_structure.get('modules', [])
        other_modules = [m for m in modules if m['name'] != current_module]

        if not other_modules:
            return "This is the only module in the project."

        lines = ["**Other modules in the project**:"]
        for module in other_modules[:10]:  # Limit context
            lines.append(f"- {module['name']}: {len(module.get('files', []))} files")

        return '\n'.join(lines)

    def _sanitize_filename(self, name: str) -> str:
        """Convert module name to safe filename"""
        # Replace spaces and special chars with hyphens
        safe = name.lower()
        safe = safe.replace(' ', '-')
        safe = safe.replace('_', '-')
        safe = ''.join(c for c in safe if c.isalnum() or c == '-')
        return safe

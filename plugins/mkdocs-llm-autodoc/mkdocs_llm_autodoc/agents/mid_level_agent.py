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

    def generate(self, module: Dict[str, Any], project_structure: Dict[str, Any], output_dir: str, detailed_docs_dir: str = None) -> List[str]:
        """
        Generate module documentation.

        Args:
            module: Module information (name, files, classes, etc.)
            project_structure: Full project structure for context
            output_dir: Directory to write documentation
            detailed_docs_dir: Directory containing detailed docs (optional)

        Returns:
            List of generated file paths
        """
        generated_files = []
        output_path = Path(output_dir)

        module_name = module['name']
        safe_name = self._sanitize_filename(module_name)

        module_file = output_path / f"{safe_name}.md"
        content = self._generate_module_doc(module, project_structure, detailed_docs_dir)
        module_file.write_text(content, encoding='utf-8')
        generated_files.append(str(module_file))

        logger.info(f"Generated module documentation: {module_file}")

        return generated_files

    def _generate_module_doc(self, module: Dict[str, Any], project_structure: Dict[str, Any], detailed_docs_dir: str = None) -> str:
        """Generate documentation for a module"""

        detailed_summaries = ""
        if detailed_docs_dir:
            detailed_summaries = self._collect_detailed_summaries(module, detailed_docs_dir)

        prompt = self._build_module_prompt(module, project_structure, detailed_summaries)

        # Check cache
        cache_key = f"mid_level_{module['name']}_{hash(str(module))}_{hash(detailed_summaries)}"
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

    def _collect_detailed_summaries(self, module: Dict[str, Any], detailed_docs_dir: str) -> str:
        """Collect summaries from detailed documentation"""
        summaries = []
        docs_path = Path(detailed_docs_dir)
        
        # Collect Class Summaries
        classes = module.get('classes', [])
        for cls in classes:
            class_name = cls.get('name')
            if not class_name:
                continue
            
            safe_name = self._sanitize_filename(class_name)
            class_doc_path = docs_path / 'classes' / f"{safe_name}.md"
            
            if class_doc_path.exists():
                content = class_doc_path.read_text(encoding='utf-8')
                # Extract first 500 chars or specific sections
                summary = f"## Class: {class_name}\n"
                # Simple extraction: Take lines until "## 2." or similar
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('## 2.') or line.startswith('## Visual'):
                        break
                    summary += line + "\n"
                summaries.append(summary)

        # Collect Function Summaries (per file)
        files = module.get('files', [])
        for file_path in files:
            file_name = Path(file_path).stem
            func_doc_path = docs_path / 'functions' / f"{file_name}.md"
            
            if func_doc_path.exists():
                content = func_doc_path.read_text(encoding='utf-8')
                summary = f"## Functions in: {file_name}\n"
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('## 2.') or line.startswith('## Code Quality'):
                        break
                    summary += line + "\n"
                summaries.append(summary)
                
        return "\n".join(summaries)

    def _build_module_prompt(self, module: Dict[str, Any], project_structure: Dict[str, Any], detailed_summaries: str = "") -> str:
        """Build prompt for module documentation"""

        module_name = module['name']
        module_files = module.get('files', [])
        module_files_str = ', '.join([str(Path(f).name) for f in module_files[:10]])
        
        prompt = f"""Act as a Lead Technical Writer. Synthesize a "Module Intelligence Report" for **{module_name}**.

# Module Information
**Name**: {module_name}
**Files**: {module_files_str}

# Atomic Intelligence Reports (from detailed analysis)
The following are summaries of the classes and files within this module:

{detailed_summaries}

# Project Context
{self._format_project_context(project_structure, module_name)}

# Your Task
Synthesize this information into a high-level Module Overview.
Do NOT just list the classes. Explain how they work TOGETHER.

## 1. Module Executive Summary
- **Purpose**: What problem does this module solve?
- **Key Capabilities**: High-level features.
- **Architecture**: How is it organized?

## 2. Component Interaction
- How do the classes identified above interact?
- **Mermaid Diagram**: Create a component diagram showing relationships.
```mermaid
classDiagram
    %% Add relationships based on the summaries
```

## 3. Key Workflows
Describe 1-2 primary workflows this module enables (e.g., "User Login Flow", "Data Processing Pipeline").

## 4. Dependencies & Integration
- What does this module need to work?
- How should other modules use this?

# Output Format
- Markdown with clear headings.
- **Embed Mermaid diagrams**.
- Focus on **Synthesis**, not repetition.
"""
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

"""
Detailed-Level Documentation Agent

Generates detailed API documentation for classes and functions:
- Parameter details
- Return values
- Example code
- Possible exceptions/errors
"""

import logging
from pathlib import Path
from typing import Dict, List, Any

from ..utils.prompt_manager import get_prompt_manager

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.detailed')


class DetailedLevelAgent:
    """
    Agent for generating detailed API documentation.

    Creates comprehensive documentation for each class and function:
    - Complete method signatures
    - Parameter documentation
    - Return value documentation
    - Usage examples
    - Error handling
    """

    def __init__(self, llm_provider, cache_manager, cross_ref_manager):
        self.llm = llm_provider
        self.cache = cache_manager
        self.cross_ref = cross_ref_manager
        self.prompt_manager = get_prompt_manager()

    def generate(self, file_info: Dict[str, Any], project_structure: Dict[str, Any], output_dir: str) -> List[str]:
        """
        Generate detailed API documentation for a file.

        Args:
            file_info: Parsed file information (classes, functions, etc.)
            project_structure: Full project structure for context
            output_dir: Directory to write documentation

        Returns:
            List of generated file paths
        """
        generated_files = []
        output_path = Path(output_dir)

        file_path = file_info.get('path', '')
        file_name = Path(file_path).stem

        # Generate documentation for classes
        classes = file_info.get('classes', [])
        for cls in classes:
            class_name = cls['name']
            safe_name = self._sanitize_filename(class_name)

            class_dir = output_path / 'classes'
            class_dir.mkdir(parents=True, exist_ok=True)

            class_file = class_dir / f"{safe_name}.md"
            content = self._generate_class_doc(cls, file_info, project_structure)
            class_file.write_text(content, encoding='utf-8')
            generated_files.append(str(class_file))

            logger.info(f"Generated class documentation: {class_file}")

        # Generate documentation for standalone functions
        functions = file_info.get('functions', [])
        if functions:
            func_dir = output_path / 'functions'
            func_dir.mkdir(parents=True, exist_ok=True)

            func_file = func_dir / f"{file_name}.md"
            content = self._generate_functions_doc(functions, file_info, project_structure)
            func_file.write_text(content, encoding='utf-8')
            generated_files.append(str(func_file))

            logger.info(f"Generated functions documentation: {func_file}")

        return generated_files

    def _generate_class_doc(self, cls: Dict[str, Any], file_info: Dict[str, Any], project_structure: Dict[str, Any]) -> str:
        """Generate detailed documentation for a class"""

        prompt = self._build_class_prompt(cls, file_info, project_structure)

        # Check cache
        cache_key = f"detailed_{cls['name']}_{hash(str(cls))}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Using cached documentation for class: {cls['name']}")
            return cached

        # Generate with LLM
        response = self.llm.generate(prompt)

        # Cache result
        self.cache.set(cache_key, response)

        # Register for cross-referencing
        self.cross_ref.register_class(cls['name'], response)

        return response

    def _generate_functions_doc(self, functions: List[Dict], file_info: Dict[str, Any], project_structure: Dict[str, Any]) -> str:
        """Generate detailed documentation for standalone functions"""

        prompt = self._build_functions_prompt(functions, file_info, project_structure)

        # Check cache
        cache_key = f"detailed_functions_{file_info.get('path')}_{hash(str(functions))}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Using cached documentation for functions in: {file_info.get('path')}")
            return cached

        # Generate with LLM
        response = self.llm.generate(prompt)

        # Cache result
        self.cache.set(cache_key, response)

        return response

    def _build_class_prompt(self, cls: Dict[str, Any], file_info: Dict[str, Any], project_structure: Dict[str, Any]) -> str:
        """Build prompt for class documentation"""

        class_name = cls['name']
        methods = cls.get('methods', [])
        base_classes = cls.get('base_classes', [])
        header_code = cls.get('header_code', '')
        file_path = file_info.get('path', 'N/A')

        prompt = f"""Act as a Senior Software Architect and QA Lead. Analyze this C++ class to create a "Deep Atomic Intelligence Report".

# Class Information
**Name**: {class_name}
**File**: {file_path}
**Base Classes**: {', '.join(base_classes) if base_classes else 'None'}
**Methods**: {len(methods)} methods

## Header Code
```cpp
{header_code}
```

## Methods
{self._format_methods(methods)}

# Your Task
Create a comprehensive developer-centric report. Do NOT just list methods. Analyze the code deeply.

## 1. Class Overview & Topics
- **High-Level Topic**: What broad category does this fit? (e.g., "Authentication", "Data Storage")
- **Low-Level Topics**: Specific implementation details (e.g., "AES Encryption", "File I/O")
- **Responsibility**: What is its SINGLE primary responsibility?
- **Relationships**: How does it fit into the larger system?

## 2. Visual Documentation (Mermaid)
Create a Mermaid diagram to visualize this class.
- **Class Diagram**: Show inheritance and key relationships.
```mermaid
classDiagram
    class {class_name} {{
        +publicMethod()
        -privateMember
    }}
    %% Add relationships here
```

## 3. Code Quality & Health Analysis
Analyze the code for potential issues. Be critical.
- **Complexity**: Identify "God Methods" or high cyclomatic complexity.
- **Dead Code**: Flag unused members or unreachable logic.
- **Design Patterns**: Identify patterns used (Singleton, Factory, Observer) or Anti-Patterns.
- **Maintainability**: Is it easy to extend? Tight coupling?

## 4. Tester's Intelligence Report
Crucial for QA and Unit Testing.
- **Test Scenarios**: List specific positive and negative test cases.
- **Edge Cases**: What happens with empty inputs, null pointers, max values?
- **Mocking Requirements**: What external dependencies need to be mocked to test this isolated?

## 5. Public Interface (Detailed)
For EACH public method:
### `methodName`
- **Signature**: `ReturnType methodName(...)`
- **Source Link**: `[View Source]({file_path})` (Note: Link to file)
- **Description**: Clear explanation.
- **Parameters**: Details with constraints.
- **Returns**: Meaning of values.
- **Complexity**: Time/Space estimate.
- **Example**:
```cpp
// Usage
obj.methodName(arg);
```

## 6. Cross-Referencing
- **Dependencies**: List what this class imports/uses and WHY.
- **See Also**: Links to related classes.

# Output Format
- Use Markdown with clear headings.
- **Embed Mermaid diagrams** directly.
- **Use Icons** for warnings/tips (e.g., ⚠️ for complexity, 💡 for tips).
- **Be concise but deep**. Focus on insights, not just restating code.
"""
        return prompt

    def _build_functions_prompt(self, functions: List[Dict], file_info: Dict[str, Any], project_structure: Dict[str, Any]) -> str:
        """Build prompt for functions documentation"""

        file_path = file_info.get('path', 'N/A')

        prompt = f"""Act as a Senior Software Architect and QA Lead. Analyze these C++ functions to create a "Deep Atomic Intelligence Report".

# File Information
**File**: {file_path}
**Functions**: {len(functions)} functions

## Functions
{self._format_functions_detailed(functions)}

# Your Task
Create a comprehensive developer-centric report. Do NOT just list functions. Analyze the code deeply.

## 1. File Overview & Topics
- **High-Level Topic**: What broad category does this file fit? (e.g., "Math Utilities", "String Processing")
- **Low-Level Topics**: Specific implementation details.
- **Responsibility**: What is the primary purpose of these functions?

## 2. Code Quality & Health Analysis
Analyze the code for potential issues. Be critical.
- **Complexity**: Identify "God Functions" or high cyclomatic complexity.
- **Dead Code**: Flag unused parameters or unreachable logic.
- **Efficiency**: Identify inefficient algorithms (e.g., O(n^2) on large data).
- **Maintainability**: Is the code readable? Magic numbers?

## 3. Visual Documentation (Mermaid)
If any function is complex (has multiple branches/loops), create a **Flowchart**.
```mermaid
graph TD
    Start --> CheckCondition
    CheckCondition -- Yes --> ProcessData
    CheckCondition -- No --> ReturnError
    ProcessData --> End
```
If functions are simple, you can omit this.

## 4. Tester's Intelligence Report
Crucial for QA and Unit Testing.
- **Test Scenarios**: List specific positive and negative test cases.
- **Edge Cases**: What happens with empty inputs, null pointers, max values?
- **Mocking Requirements**: Any external dependencies?

## 5. Functions (Detailed)
For EACH function:
### `functionName`
- **Signature**: `ReturnType functionName(...)`
- **Source Link**: `[View Source]({file_path})` (Note: Link to file)
- **Description**: Clear explanation.
- **Parameters**: Details with constraints.
- **Returns**: Meaning of values.
- **Complexity**: Time/Space estimate.
- **Example**:
```cpp
// Usage
auto result = functionName(arg);
```

# Output Format
- Use Markdown with clear headings.
- **Embed Mermaid diagrams** directly.
- **Use Icons** for warnings/tips.
- **Be concise but deep**.
"""
        return prompt

    def _format_methods(self, methods: List[Dict]) -> str:
        """Format methods for prompt"""
        if not methods:
            return "No methods found"

        lines = []
        for method in methods:
            name = method.get('name', 'unknown')
            return_type = method.get('return_type', 'void')
            params = method.get('parameters', [])
            visibility = method.get('visibility', 'public')

            param_str = ', '.join(f"{p.get('type', '')} {p.get('name', '')}" for p in params)
            lines.append(f"- **{name}** ({visibility})")
            lines.append(f"  - Signature: `{return_type} {name}({param_str})`")

            if method.get('is_const'):
                lines.append(f"  - Const method")
            if method.get('is_static'):
                lines.append(f"  - Static method")
            if method.get('is_virtual'):
                lines.append(f"  - Virtual method")

        return '\n'.join(lines)

    def _format_functions_detailed(self, functions: List[Dict]) -> str:
        """Format functions for prompt with full details"""
        if not functions:
            return "No functions found"

        lines = []
        for func in functions:
            name = func.get('name', 'unknown')
            return_type = func.get('return_type', 'void')
            params = func.get('parameters', [])

            param_str = ', '.join(f"{p.get('type', '')} {p.get('name', '')}" for p in params)
            lines.append(f"\n### {name}")
            lines.append(f"**Signature**: `{return_type} {name}({param_str})`")

            if params:
                lines.append("**Parameters**:")
                for p in params:
                    lines.append(f"- `{p.get('name', '')}` ({p.get('type', '')})")

            if func.get('code'):
                lines.append("**Code**:")
                lines.append("```cpp")
                lines.append(func.get('code', ''))
                lines.append("```")

        return '\n'.join(lines)

    def _sanitize_filename(self, name: str) -> str:
        """Convert class/function name to safe filename"""
        safe = name.lower()
        safe = safe.replace('::', '-')
        safe = safe.replace(' ', '-')
        safe = safe.replace('_', '-')
        safe = ''.join(c for c in safe if c.isalnum() or c == '-')
        return safe

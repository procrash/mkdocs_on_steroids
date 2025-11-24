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

        prompt = f"""Analyze this C++ class and create comprehensive API documentation.

# Class Information
**Name**: {class_name}
**File**: {file_info.get('path', 'N/A')}
**Base Classes**: {', '.join(base_classes) if base_classes else 'None'}
**Methods**: {len(methods)} methods

## Header Code
```cpp
{header_code}
```

## Methods
{self._format_methods(methods)}

# Your Task
Create detailed API documentation for this class with the following structure:

## 1. Class Overview
- Brief description (2-3 sentences)
- Purpose and responsibilities
- When to use this class
- Relationships to other classes

## 2. Constructor(s)
For each constructor:
- **Signature**: Full C++ signature
- **Parameters**: Detailed description of each parameter
  - Name, type, purpose
  - Valid values/ranges
  - Default values if any
- **Example**:
```cpp
// Example usage
MyClass obj(param1, param2);
```
- **Notes**: Thread safety, exceptions, special considerations

## 3. Public Methods
For EACH public method, provide:

### MethodName
- **Signature**: `ReturnType methodName(ParamType1 param1, ParamType2 param2)`
- **Description**: What does this method do? (2-3 sentences)
- **Parameters**:
  - `param1` (ParamType1): Description, valid values
  - `param2` (ParamType2): Description, valid values
- **Return Value**: What is returned? Meaning of return value? Possible values?
- **Exceptions/Errors**: What can go wrong? What exceptions might be thrown?
- **Example**:
```cpp
// Example usage
auto result = obj.methodName(value1, value2);
if (result) {{
    // Handle success
}}
```
- **See Also**: Links to related methods or classes
- **Thread Safety**: Is this method thread-safe?
- **Complexity**: Time and space complexity if relevant

## 4. Usage Examples
Provide 2-3 complete, realistic examples:

### Example 1: Basic Usage
```cpp
// Description of what this example demonstrates
MyClass obj;
obj.setup();
auto result = obj.process(data);
```

### Example 2: Advanced Usage
```cpp
// More complex scenario
MyClass obj(customConfig);
try {{
    obj.complexOperation();
}} catch (const std::exception& e) {{
    // Error handling
}}
```

## 5. Notes and Best Practices
- Common pitfalls to avoid
- Performance considerations
- Memory management considerations
- Thread safety guidelines

## 6. Code Review & Improvement Suggestions

Perform a thorough code review of this class and provide:

### 6.1 Potential Issues
Identify potential problems in the following categories:

**Security Issues:**
- Buffer overflows, memory leaks
- Unchecked user input
- Integer overflows
- Race conditions
- Use-after-free vulnerabilities

**Performance Issues:**
- Unnecessary copies or allocations
- Inefficient algorithms
- Missing const-correctness
- Suboptimal data structures
- Missing move semantics

**Maintainability Issues:**
- Overly complex methods (high cyclomatic complexity)
- Violation of Single Responsibility Principle
- Tight coupling with other classes
- Missing error handling
- Poor naming conventions

**Code Smells:**
- Long parameter lists
- God classes (too many responsibilities)
- Duplicate code
- Magic numbers
- Deep nesting

For each issue found, provide:
- **Issue**: Brief description
- **Severity**: Critical / High / Medium / Low
- **Location**: Which method/line (if identifiable)
- **Impact**: What problems could this cause?
- **Recommendation**: How to fix it

**Example:**
```markdown
**Issue**: Missing bounds checking in array access
**Severity**: High
**Location**: `processData()` method
**Impact**: Could lead to buffer overflow and crash
**Recommendation**: Add bounds validation before array access:
```cpp
if (index >= 0 && index < array.size()) {{
    // Safe access
}}
```

### 6.2 Improvement Suggestions

Provide concrete, actionable improvements:

**Refactoring Opportunities:**
- Extract methods to reduce complexity
- Introduce design patterns where beneficial
- Improve naming for clarity

**Modern C++ Features:**
- Use smart pointers instead of raw pointers
- Use std::optional for optional return values
- Use constexpr where applicable
- Use range-based for loops
- Use auto where appropriate

**Performance Optimizations:**
- Add [[nodiscard]] attributes
- Use string_view instead of const string&
- Reserve container capacity when size is known
- Use emplace instead of push_back

**Code Examples:**
For each significant suggestion, provide a before/after code example:

```cpp
// Before
void processItems(std::vector<Item> items) {{
    for (int i = 0; i < items.size(); i++) {{
        // Process item
    }}
}}

// After (improved)
void processItems(const std::vector<Item>& items) {{
    for (const auto& item : items) {{
        // Process item
    }}
}}
```

### 6.3 Best Practices Violations

Identify violations of C++ best practices:
- RAII violations
- Missing rule of five/zero
- Inconsistent const usage
- Missing noexcept specifications
- Improper exception handling

### 6.4 Testing Recommendations

Suggest what should be tested:
- Edge cases to cover
- Error conditions to verify
- Performance scenarios to benchmark

**Example:**
- Test with empty containers
- Test with maximum size inputs
- Test concurrent access if thread-safe
- Test exception scenarios

## 7. Related Classes
- Links to related classes (use `[ClassName](classname.md)` format)
- How this class interacts with others

# Output Format
Generate a complete Markdown document with:
- Clear hierarchical headings
- Code blocks with syntax highlighting
- Mermaid diagrams if helpful for understanding relationships
- Cross-references to other documentation
- **Comprehensive code review section with actionable insights**

Generate ONLY the markdown content, no additional commentary.
"""
        return prompt

    def _build_functions_prompt(self, functions: List[Dict], file_info: Dict[str, Any], project_structure: Dict[str, Any]) -> str:
        """Build prompt for functions documentation"""

        prompt = f"""Analyze these C++ functions and create comprehensive API documentation.

# File Information
**File**: {file_info.get('path', 'N/A')}
**Functions**: {len(functions)} functions

## Functions
{self._format_functions_detailed(functions)}

# Your Task
Create detailed API documentation for these functions.

For EACH function, provide:

## FunctionName

- **Signature**: `ReturnType functionName(ParamType1 param1, ParamType2 param2)`
- **Description**: Comprehensive description of what this function does
- **Parameters**:
  - `param1` (ParamType1): Detailed description, valid values, constraints
  - `param2` (ParamType2): Detailed description, valid values, constraints
- **Return Value**:
  - What is returned?
  - Meaning of different return values
  - Special values (nullptr, -1, etc.)
- **Exceptions/Errors**:
  - What can go wrong?
  - What exceptions might be thrown?
  - Error codes if applicable
- **Example**:
```cpp
// Practical example of using this function
auto result = functionName(arg1, arg2);
if (result != nullptr) {{
    // Use result
}}
```
- **Preconditions**: What must be true before calling this function?
- **Postconditions**: What is guaranteed after calling this function?
- **Thread Safety**: Is this function thread-safe?
- **Complexity**: Time and space complexity
- **See Also**: Related functions

# Additional Sections

## Usage Examples
Provide complete, realistic examples showing:
1. Basic usage
2. Error handling
3. Edge cases

## Best Practices
- How to use these functions effectively
- Common mistakes to avoid
- Performance tips

## Code Review & Improvement Suggestions

For each function, perform a thorough code review:

### Potential Issues
Analyze each function for:

**Security:**
- Input validation
- Buffer safety
- Integer overflow risks
- Resource leaks

**Performance:**
- Unnecessary allocations
- Inefficient algorithms (O(n²) when O(n log n) possible)
- Missing const-correctness
- Pass-by-value when pass-by-reference would be better

**Correctness:**
- Edge case handling
- Null pointer checks
- Error return values
- Exception safety

**Code Quality:**
- Function complexity (too long, too complex)
- Unclear naming
- Magic numbers
- Duplicate code

For each issue, provide:
- **Function**: Function name
- **Issue**: What's wrong
- **Severity**: Critical/High/Medium/Low
- **Impact**: Potential consequences
- **Fix**: How to resolve it (with code example)

**Example:**
```markdown
**Function**: `calculateSum()`
**Issue**: No overflow checking when summing large values
**Severity**: Medium
**Impact**: Could produce incorrect results with large inputs
**Fix**: Use checked arithmetic or larger data type:
```cpp
// Before
int calculateSum(const std::vector<int>& values) {{
    int sum = 0;
    for (int val : values) sum += val;
    return sum;
}}

// After
std::optional<int64_t> calculateSum(const std::vector<int>& values) {{
    int64_t sum = 0;
    for (int val : values) {{
        sum += val;
        // Could add overflow check here
    }}
    return sum;
}}
```

### Modernization Opportunities

Suggest modern C++ improvements:
- Use [[nodiscard]] for functions that return important values
- Use std::span for array parameters
- Use constexpr for compile-time evaluation
- Use concepts (C++20) for template constraints
- Use std::expected (C++23) for error handling

**Example:**
```cpp
// Before
bool processData(const char* data, size_t length);

// After (Modern C++)
[[nodiscard]] bool processData(std::span<const char> data);
```

### Refactoring Suggestions

Identify functions that should be:
- Split into smaller functions
- Combined with similar functions
- Made into class methods
- Moved to a utility namespace

### Performance Optimizations

Specific optimization opportunities:
- Use move semantics
- Return by value for RVO
- Use string_view for read-only strings
- Add noexcept where applicable

# Output Format
Generate a complete Markdown document with:
- Clear section headings
- Syntax-highlighted code blocks
- Cross-references to related functions/classes
- Practical, runnable examples

Generate ONLY the markdown content, no additional commentary.
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

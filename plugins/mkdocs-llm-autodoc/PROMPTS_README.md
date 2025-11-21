# LLM-AutoDoc Prompt Configuration System

This document explains how the prompt configuration system works and how to customize prompts.

## 📁 File Structure

```
mkdocs_llm_autodoc/
├── prompts.yml                    # Main prompt configuration file
├── utils/
│   └── prompt_manager.py          # PromptManager class
└── agents/
    ├── overview_agent.py          # Uses PromptManager
    ├── high_level_agent.py        # Uses PromptManager (TODO)
    ├── mid_level_agent.py         # Uses PromptManager (TODO)
    └── detailed_level_agent.py    # Uses PromptManager (TODO)
```

## 🎯 How It Works

### 1. Prompts are stored in `prompts.yml`

```yaml
overview:
  extraction: |
    Analyze this source file...
    {file_path}
    {content}
```

### 2. Agents use `PromptManager` to load prompts

```python
from ..utils.prompt_manager import get_prompt_manager

class HighLevelOverviewAgent:
    def __init__(self, ...):
        self.prompt_manager = get_prompt_manager()

    def _build_extraction_prompt(self, topic, file_path, content):
        prompt = self.prompt_manager.get_prompt(
            'overview', 'extraction',
            topic_name=topic.name,
            file_path=file_path,
            content=content
        )
        return prompt
```

### 3. Template variables are replaced automatically

```python
prompt = manager.get_prompt(
    'overview', 'extraction',
    topic_name='Threading',
    file_path='thread.cpp',
    content='...'
)
# Returns: "Analyze this source file...\nthread.cpp\n..."
```

## 📝 Customizing Prompts

### Option 1: Edit `prompts.yml` directly

```yaml
overview:
  extraction: |
    My custom prompt here...
    File: {file_path}
    Content: {content}
```

### Option 2: Environment Variable Override

```bash
export LLMAUTODOC_PROMPT_OVERVIEW_EXTRACTION="My custom prompt for {file_path}"
mkdocs serve
```

### Option 3: Custom prompts.yml path

```python
from mkdocs_llm_autodoc.utils.prompt_manager import PromptManager

manager = PromptManager(config_path='/path/to/my/prompts.yml')
```

## 🔧 Available Template Variables

### Overview Agent Prompts

**extraction / extraction_hybrid:**
- `{topic_name}` - Topic name (e.g., "Threading & Concurrency")
- `{topic_description}` - Topic description
- `{topic_questions}` - Formatted list of questions
- `{file_path}` - Source file path
- `{content}` - Source code content
- `{source_content}` - Source code (hybrid only)
- `{doc_content}` - Generated documentation (hybrid only)

**synthesis:**
- `{topic_name}` - Topic name
- `{topic_description}` - Topic description
- `{topic_questions}` - Formatted list of questions
- `{extractions_count}` - Number of files extracted from
- `{combined_info}` - Combined extraction results

**refinement:**
- `{content}` - Current documentation content
- `{file_path}` - Documentation file path

### High-Level Agent Prompts

**getting_started:**
- `{project_structure}` - Project structure as JSON
- `{entry_points}` - Main entry points

**architecture:**
- `{project_structure}` - Project structure as JSON
- `{modules}` - List of modules

### Mid-Level Agent Prompts

**module:**
- `{module_name}` - Module name
- `{module_files}` - List of files in module
- `{module_classes}` - List of classes in module
- `{project_structure}` - Full project structure

### Detailed-Level Agent Prompts

**class:**
- `{class_name}` - Class name
- `{file_path}` - File containing class
- `{namespace}` - Namespace
- `{class_code}` - Class source code
- `{members}` - Member variables
- `{methods}` - Methods
- `{project_structure}` - Project structure

**functions:**
- `{file_path}` - File path
- `{namespace}` - Namespace
- `{functions_list}` - List of functions
- `{project_structure}` - Project structure

### Cross-Linker Prompts

**linking:**
- `{doc_path}` - Current document path
- `{doc_content}` - Document content
- `{candidates}` - Candidate related documents

## 🧪 Testing Prompts

### Validate all prompts

```python
from mkdocs_llm_autodoc.utils.prompt_manager import get_prompt_manager

manager = get_prompt_manager()
is_valid = manager.validate_prompts()
print(f"Prompts valid: {is_valid}")
```

### List all available prompts

```python
prompts = manager.list_prompts()
print(prompts)
# Output: {
#   'overview': ['extraction', 'synthesis', 'refinement'],
#   'high_level': ['getting_started', 'architecture'],
#   ...
# }
```

### Test a specific prompt

```python
prompt = manager.get_prompt(
    'overview', 'extraction',
    topic_name='Testing',
    file_path='test.cpp',
    content='void test() {}'
)
print(prompt)
```

## 📊 Prompt Categories

### 1. **Overview** (Multi-Pass Analysis)
- `extraction` - Extract topic information from source
- `extraction_hybrid` - Extract from source + generated docs
- `synthesis` - Synthesize multiple extractions into document
- `refinement` - Refine and polish generated documentation

### 2. **High-Level** (Project Overview)
- `getting_started` - Generate Getting Started guide
- `architecture` - Generate Architecture documentation

### 3. **Mid-Level** (Module Documentation)
- `module` - Generate module documentation

### 4. **Detailed-Level** (API Reference)
- `class` - Generate class API documentation
- `functions` - Generate functions API documentation

### 5. **Cross-Linker** (Related Documents)
- `linking` - Analyze and suggest related documents

## 🎨 Prompt Writing Best Practices

### 1. Use Clear Instructions

```yaml
✅ Good:
  extraction: |
    Analyze this file and extract information about {topic_name}.

    File: {file_path}

    Output Format:
    - Use bullet points
    - Max 200 words
```

```yaml
❌ Bad:
  extraction: |
    Extract stuff from {file_path} about {topic_name}
```

### 2. Include Examples

```yaml
extraction: |
  Format: `[ClassName](file.cpp:123)`

  Example: "The build system uses CMake (see `[CMakeLists.txt](CMakeLists.txt:1)`)"
```

### 3. Specify Output Format

```yaml
synthesis: |
  # Output Format
  - Use Markdown
  - Include code blocks
  - Aim for 300-500 words
```

### 4. Use Template Variables

```yaml
✅ Good:
  module: |
    Document module: {module_name}
    Files: {module_files}

❌ Bad (hardcoded):
  module: |
    Document module: MyModule
    Files: file1.cpp, file2.cpp
```

## 🔄 Reloading Prompts

Prompts are loaded once at startup. To reload after making changes:

```python
manager = get_prompt_manager()
manager.reload_prompts()
```

Or restart mkdocs:
```bash
# Ctrl+C to stop
mkdocs serve
```

## 🐛 Troubleshooting

### Problem: Prompt not found

```
WARNING: Prompt 'overview.extraction' not found in config
```

**Solution:** Check `prompts.yml` has the correct structure:

```yaml
overview:           # Category
  extraction: |     # Prompt name
    Your prompt...
```

### Problem: Template variable missing

```
ERROR: Missing template variable in prompt 'overview.extraction': topic_name
```

**Solution:** Pass all required variables:

```python
prompt = manager.get_prompt(
    'overview', 'extraction',
    topic_name='...', # ← Missing this
    file_path='...',
    content='...'
)
```

### Problem: Prompt too short/suspicious

```
WARNING: Suspiciously short prompt: overview.extraction
```

**Solution:** Check if prompt content was accidentally deleted or malformed in YAML.

## 📚 Further Reading

- [YAML Syntax](https://yaml.org/spec/1.2/spec.html)
- [Python String Formatting](https://docs.python.org/3/library/string.html#formatstrings)
- [LLM Prompt Engineering](https://www.promptingguide.ai/)

## 🤝 Contributing

To add a new prompt:

1. **Add to `prompts.yml`:**
   ```yaml
   my_category:
     my_prompt: |
       Your prompt template...
       {variable1}
       {variable2}
   ```

2. **Update agent to use it:**
   ```python
   prompt = self.prompt_manager.get_prompt(
       'my_category', 'my_prompt',
       variable1='...',
       variable2='...'
   )
   ```

3. **Document template variables** in this README

4. **Test the prompt:**
   ```python
   manager.validate_prompts()
   ```

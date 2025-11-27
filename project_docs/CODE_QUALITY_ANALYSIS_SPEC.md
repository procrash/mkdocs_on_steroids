# Code Quality Analysis Feature

## Übersicht

Automatische Identifizierung von:
- **Toter Code** (dead code / unreachable code)
- **Schlecht wartbarer Code** (code smells)
- **Komplexitäts-Hotspots**
- **Verbesserungsvorschläge**

## Implementierung

### Option 1: Als Overview Topic

```yaml
# In utils/topic_definitions.py hinzufügen:

Topic(
    id='code-quality',
    name='Code Quality & Maintainability',
    priority=1,
    description='Analysis of code quality, dead code, and maintenance issues',
    questions=[
        'Which functions or classes are never used (dead code)?',
        'Which code has high cyclomatic complexity?',
        'Which code violates SOLID principles?',
        'Which code has poor naming conventions?',
        'Which code lacks error handling?',
        'Which code has too many responsibilities?',
        'Which code is difficult to test?',
        'Which code has duplicated logic?'
    ],
    keywords=[
        'unused', 'dead code', 'unreachable',
        'complexity', 'cyclomatic', 'maintainability',
        'code smell', 'anti-pattern', 'refactor',
        'SOLID', 'coupling', 'cohesion',
        'naming', 'convention', 'style',
        'duplicate', 'copy-paste', 'DRY'
    ]
)
```

### Option 2: Als separates Tool

```bash
llm-autodoc analyze-quality

Output:
┌───────────────────────────────────────────┐
│ Code Quality Report                       │
├───────────────────────────────────────────┤
│ Dead Code Found:                          │
│   - MyClass::unused_method() (file.cpp:45)│
│   - helper_function() (util.cpp:123)      │
│   - DEAD_CONSTANT (config.h:78)           │
│                                            │
│ High Complexity (>15):                    │
│   - parse_input() → CCN: 23 (parser.cpp)  │
│   - process_data() → CCN: 19 (main.cpp)   │
│                                            │
│ Code Smells:                               │
│   - God Class: Manager (500+ LOC)         │
│   - Long Parameter List: init() (8 params)│
│   - Magic Numbers: calculate() (calc.cpp) │
│                                            │
│ Improvement Suggestions: 12                │
└───────────────────────────────────────────┘
```

### Prompt für Code Quality

```yaml
# In prompts.yml hinzufügen:

overview:
  code_quality: |
    Analyze this code for quality issues and maintainability problems.

    # File: {file_path}
    ```cpp
    {content}
    ```

    # Your Task
    Identify the following issues:

    ## 1. Dead Code
    - Unused functions/methods (never called)
    - Unused variables/constants
    - Unreachable code (after return/break)
    - Commented-out code blocks

    ## 2. Complexity Issues
    - Functions with high cyclomatic complexity (>15)
    - Deep nesting (>4 levels)
    - Long functions (>100 LOC)
    - Long parameter lists (>5 parameters)

    ## 3. Code Smells
    - God Classes (>500 LOC, too many responsibilities)
    - Duplicated code
    - Magic numbers/strings
    - Poor naming (single letters, abbreviations)
    - Missing error handling
    - Global variables

    ## 4. SOLID Violations
    - Single Responsibility violations
    - Open/Closed violations
    - Liskov Substitution violations
    - Interface Segregation violations
    - Dependency Inversion violations

    # Output Format
    For EACH issue found, provide:
    - **Type**: Dead Code / Complexity / Code Smell / SOLID
    - **Location**: File:Line or Function name
    - **Description**: What is the problem?
    - **Impact**: Why is this bad? (Maintainability, Performance, etc.)
    - **Suggestion**: How to fix it?
    - **Priority**: High / Medium / Low

    Example:
    ```markdown
    ### Dead Code: `unused_helper()`
    - **Location**: `utils.cpp:145`
    - **Description**: Function is defined but never called
    - **Impact**: Confuses developers, increases codebase size
    - **Suggestion**: Remove function or document if kept for future use
    - **Priority**: Low
    ```

    Output as structured markdown with sections for each category.
```

### Technische Umsetzung

```python
# In overview_agent.py oder als separater CodeQualityAgent:

class CodeQualityAnalyzer:
    """Analyzes code for quality issues"""

    def __init__(self, llm_provider):
        self.llm = llm_provider
        self.prompt_manager = get_prompt_manager()

    def analyze_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze a single file for quality issues"""

        prompt = self.prompt_manager.get_prompt(
            'overview', 'code_quality',
            file_path=file_path,
            content=content
        )

        analysis = self.llm.generate(prompt)

        # Parse LLM response to structured format
        issues = self._parse_quality_issues(analysis)

        return {
            'file': file_path,
            'issues': issues,
            'total_issues': len(issues),
            'priority_breakdown': {
                'high': len([i for i in issues if i['priority'] == 'High']),
                'medium': len([i for i in issues if i['priority'] == 'Medium']),
                'low': len([i for i in issues if i['priority'] == 'Low'])
            }
        }

    def generate_report(self, all_analyses: List[Dict]) -> str:
        """Generate comprehensive quality report"""

        # Group by issue type
        dead_code = []
        complexity_issues = []
        code_smells = []
        solid_violations = []

        for analysis in all_analyses:
            for issue in analysis['issues']:
                if issue['type'] == 'Dead Code':
                    dead_code.append(issue)
                elif issue['type'] == 'Complexity':
                    complexity_issues.append(issue)
                elif issue['type'] == 'Code Smell':
                    code_smells.append(issue)
                elif issue['type'] == 'SOLID':
                    solid_violations.append(issue)

        # Generate markdown report
        report = self._format_quality_report(
            dead_code, complexity_issues, code_smells, solid_violations
        )

        return report
```

## Ausgabe-Datei

```markdown
# Code Quality & Maintainability Analysis

## Summary

- **Total Files Analyzed**: 150
- **Total Issues Found**: 47
- **High Priority**: 8
- **Medium Priority**: 23
- **Low Priority**: 16

## Dead Code (12 instances)

### 1. Unused Function: `legacy_parse()`
- **Location**: `[parser.cpp:234](parser.cpp:234)`
- **Description**: Function defined but never called in codebase
- **Impact**: Code bloat, confusion for new developers
- **Suggestion**: Remove or mark as deprecated with documentation
- **Priority**: Medium

### 2. Unreachable Code Block
- **Location**: `[main.cpp:456-460](main.cpp:456)`
- **Description**: Code after unconditional return statement
- **Impact**: Never executed, misleading
- **Suggestion**: Remove lines 456-460
- **Priority**: High

...

## High Complexity Functions (8 instances)

### 1. `process_request()` - CCN: 23
- **Location**: `[server.cpp:89](server.cpp:89)`
- **Description**: Function has 23 branches, very high complexity
- **Impact**: Hard to test, error-prone, difficult to maintain
- **Suggestion**:
  - Extract sub-functions for validation, processing, response
  - Use strategy pattern for different request types
  - Consider state machine for complex flow
- **Priority**: High

...

## Code Smells (15 instances)

### 1. God Class: `ApplicationManager`
- **Location**: `[manager.cpp:1](manager.cpp:1)`
- **Description**: Class has 687 lines, 45 methods, handles too many responsibilities
- **Impact**: Violates Single Responsibility, hard to test and maintain
- **Suggestion**: Split into:
  - `ConfigurationManager`
  - `ConnectionManager`
  - `WorkflowCoordinator`
- **Priority**: High

...

## SOLID Violations (12 instances)

...

## Recommendations

### Quick Wins (Can be fixed immediately)
1. Remove 12 instances of dead code
2. Extract magic numbers to constants
3. Rename 8 poorly named variables

### Refactoring Priorities
1. **High**: Split `ApplicationManager` god class
2. **High**: Reduce complexity of `process_request()`
3. **Medium**: Add error handling to 15 functions

### Long-term Improvements
1. Establish code review process
2. Set up static analysis tools (cppcheck, clang-tidy)
3. Define coding standards document
4. Add complexity metrics to CI/CD

## Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Avg. Cyclomatic Complexity | 8.5 | < 10 | ✅ OK |
| Max Cyclomatic Complexity | 23 | < 15 | ❌ High |
| Functions > 100 LOC | 12 | < 5 | ⚠️ Warning |
| Code Duplication | 8% | < 5% | ⚠️ Warning |
| Dead Code Instances | 12 | 0 | ❌ High |
```

## Integration in mkdocs.yml

```yaml
plugins:
  - llm-autodoc:
      # Enable code quality analysis
      enable_code_quality: true

      # Quality thresholds
      quality_thresholds:
        max_complexity: 15
        max_function_length: 100
        max_class_length: 500
        max_parameters: 5

      # Output location
      quality_report_output: "generated/code-quality.md"
```

## Nächste Schritte

1. Topic in `topic_definitions.py` hinzufügen
2. Prompt in `prompts.yml` hinzufügen
3. Analyzer implementieren
4. In Overview-Generation integrieren
5. Report-Template erstellen

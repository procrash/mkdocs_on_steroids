#!/usr/bin/env python3
"""
Fix f-string escaping issues in detailed_level_agent.py
Doubles all curly braces in C++ code examples within f-strings
"""

import re

def fix_fstring_braces(content):
    """
    Find all f-strings and ensure curly braces in code blocks are properly escaped.
    """
    # Find all multi-line f-strings (f""" ... """)
    # For now, we'll use a simpler approach: escape all { and } that aren't already escaped
    # and aren't part of f-string expressions

    # First pass: find lines with C++ code that need escaping
    lines = content.split('\n')
    fixed_lines = []
    in_fstring = False
    fstring_quote_type = None

    for i, line in enumerate(lines):
        # Detect f-string start
        if re.match(r'\s*prompt = f"""', line) or re.match(r'\s*.*= f"""', line):
            in_fstring = True
            fstring_quote_type = '"""'
            fixed_lines.append(line)
            continue

        # Detect f-string end
        if in_fstring and '"""' in line and not line.strip().startswith('#'):
            in_fstring = False
            fixed_lines.append(line)
            continue

        # If we're in an f-string, escape unescaped braces in C++ code
        if in_fstring:
            # Check if this line contains C++ code (heuristic: contains ; or :: or looks like C++)
            is_cpp_line = any(marker in line for marker in [';', '::', 'std::', 'int ', 'void ', 'auto ', 'for (', 'if (', 'try {', 'catch ('])

            # Also check if we're in a code block
            in_code_block = '```cpp' in '\n'.join(lines[max(0, i-10):i])

            if (is_cpp_line or in_code_block) and not line.strip().startswith('//'):
                # Escape single { and } but not already doubled ones
                # Replace { with {{ if not already {{
                fixed_line = re.sub(r'(?<!{){(?!{)', '{{', line)
                # Replace } with }} if not already }}
                fixed_line = re.sub(r'(?<!})}(?!})', '}}', fixed_line)
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)

# Read the file
with open('plugins/mkdocs-llm-autodoc/mkdocs_llm_autodoc/agents/detailed_level_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the content
fixed_content = fix_fstring_braces(content)

# Write back
with open('plugins/mkdocs-llm-autodoc/mkdocs_llm_autodoc/agents/detailed_level_agent.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Fixed f-string escaping issues!")

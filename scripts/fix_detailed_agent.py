#!/usr/bin/env python3
"""
Fix the detailed_level_agent.py by converting f-strings to .format() strings
to avoid escaping issues with C++ code examples.
"""

import re

def convert_fstring_to_format(content):
    """
    Convert f-strings containing C++ code to regular strings with .format()
    """
    # Find the _build_class_prompt method and replace its f-string

    # Pattern to match the entire prompt f-string
    pattern = r'(prompt = f""")(.*?)(""")'

    def replace_fstring(match):
        prefix = 'prompt = """'
        body = match.group(2)
        suffix = '"""'

        # Replace f-string placeholders with .format() placeholders
        # {class_name} -> {class_name}
        # {file_info.get('path', 'N/A')} -> {file_path}
        # etc.

        # Keep placeholders but remove expressions
        # We'll need to manually adjust the .format() call

        return prefix + body + suffix

    # Replace the f-string
    result = re.sub(pattern, replace_fstring, content, flags=re.DOTALL)

    return result

# Read the file
file_path = 'plugins/mkdocs-llm-autodoc/mkdocs_llm_autodoc/agents/detailed_level_agent.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the problematic f-string
output_lines = []
i = 0
while i < len(lines):
    line = lines[i]

    # Check if this is the start of a prompt f-string
    if 'prompt = f"""' in line:
        # Collect all lines until the closing """
        prompt_lines = [line.replace('f"""', '"""')]
        i += 1
        while i < len(lines) and '"""' not in lines[i]:
            prompt_lines.append(lines[i])
            i += 1
        if i < len(lines):
            prompt_lines.append(lines[i])  # Add the closing """ line
            i += 1

        # Now fix the prompt by escaping C++ code braces
        fixed_prompt = []
        in_cpp_block = False
        for pline in prompt_lines:
            if '```cpp' in pline:
                in_cpp_block = True
                fixed_prompt.append(pline)
            elif '```' in pline and in_cpp_block:
                in_cpp_block = False
                fixed_prompt.append(pline)
            elif in_cpp_block:
                # Escape braces in C++ code
                escaped = pline.replace('{', '{{').replace('}', '}}')
                fixed_prompt.append(escaped)
            else:
                fixed_prompt.append(pline)

        # Change back to f-string
        fixed_prompt[0] = fixed_prompt[0].replace('"""', 'f"""')

        output_lines.extend(fixed_prompt)
    else:
        output_lines.append(line)
        i += 1

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Fixed {file_path}!")

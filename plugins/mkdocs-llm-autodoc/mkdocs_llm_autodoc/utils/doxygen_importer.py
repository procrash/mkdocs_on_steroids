"""
Doxygen Legacy Documentation Importer

Imports existing Doxygen documentation and integrates it into MkDocs.
- Parses Doxygen XML output
- Validates content freshness against current codebase
- Merges content into existing documentation or creates new sections
"""

import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import hashlib
import re

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.doxygen')


class DoxygenImporter:
    """
    Imports and validates Doxygen legacy documentation.
    """

    def __init__(self, doxygen_xml_dir: str, llm_provider, source_files: Dict[str, str]):
        """
        Initialize Doxygen importer.

        Args:
            doxygen_xml_dir: Path to Doxygen XML output directory
            llm_provider: LLM provider for freshness validation
            source_files: Dict mapping file paths to their current content
        """
        self.doxygen_dir = Path(doxygen_xml_dir)
        self.llm = llm_provider
        self.source_files = source_files

        if not self.doxygen_dir.exists():
            logger.warning(f"Doxygen XML directory not found: {doxygen_xml_dir}")
            self.available = False
        else:
            self.available = True
            logger.info(f"Doxygen importer initialized with: {doxygen_xml_dir}")

    def import_documentation(self) -> Dict[str, Any]:
        """
        Import all Doxygen documentation.

        Returns:
            Dictionary with imported documentation organized by entity type
        """
        if not self.available:
            return {}

        documentation = {
            'classes': [],
            'functions': [],
            'files': [],
            'namespaces': [],
            'groups': []
        }

        try:
            # Find index.xml
            index_file = self.doxygen_dir / 'index.xml'
            if not index_file.exists():
                logger.error("Doxygen index.xml not found")
                return documentation

            # Parse index
            tree = ET.parse(index_file)
            root = tree.getroot()

            # Extract compounds (classes, files, namespaces, etc.)
            for compound in root.findall('.//compound'):
                refid = compound.get('refid')
                kind = compound.get('kind')
                name = compound.find('name').text if compound.find('name') is not None else ''

                logger.info(f"Processing {kind}: {name}")

                # Parse compound XML
                compound_data = self._parse_compound(refid, kind)

                if compound_data:
                    if kind == 'class' or kind == 'struct':
                        documentation['classes'].append(compound_data)
                    elif kind == 'file':
                        documentation['files'].append(compound_data)
                    elif kind == 'namespace':
                        documentation['namespaces'].append(compound_data)
                    elif kind == 'group':
                        documentation['groups'].append(compound_data)

            logger.info(f"Imported {len(documentation['classes'])} classes, "
                       f"{len(documentation['files'])} files, "
                       f"{len(documentation['namespaces'])} namespaces")

        except Exception as e:
            logger.error(f"Failed to import Doxygen documentation: {e}")

        return documentation

    def _parse_compound(self, refid: str, kind: str) -> Optional[Dict[str, Any]]:
        """Parse a compound XML file."""
        xml_file = self.doxygen_dir / f"{refid}.xml"

        if not xml_file.exists():
            logger.warning(f"Compound XML not found: {xml_file}")
            return None

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            compound_def = root.find('.//compounddef')
            if compound_def is None:
                return None

            name = compound_def.find('compoundname')
            name_text = name.text if name is not None else ''

            # Extract documentation
            briefdesc = self._extract_description(compound_def.find('briefdescription'))
            detaileddesc = self._extract_description(compound_def.find('detaileddescription'))

            # Extract location
            location = compound_def.find('location')
            file_path = location.get('file') if location is not None else ''

            # Extract members (functions, variables, etc.)
            members = []
            for memberdef in compound_def.findall('.//memberdef'):
                member_data = self._parse_member(memberdef)
                if member_data:
                    members.append(member_data)

            compound_data = {
                'refid': refid,
                'kind': kind,
                'name': name_text,
                'brief': briefdesc,
                'detailed': detaileddesc,
                'file': file_path,
                'members': members,
                'raw_xml': ET.tostring(compound_def, encoding='unicode')
            }

            return compound_data

        except Exception as e:
            logger.error(f"Failed to parse compound {refid}: {e}")
            return None

    def _parse_member(self, memberdef: ET.Element) -> Optional[Dict[str, Any]]:
        """Parse a member definition (function, variable, etc.)."""
        try:
            kind = memberdef.get('kind')
            name = memberdef.find('name')
            name_text = name.text if name is not None else ''

            # Extract type
            type_elem = memberdef.find('type')
            type_text = ''.join(type_elem.itertext()) if type_elem is not None else ''

            # Extract documentation
            briefdesc = self._extract_description(memberdef.find('briefdescription'))
            detaileddesc = self._extract_description(memberdef.find('detaileddescription'))

            # Extract parameters (for functions)
            params = []
            for param in memberdef.findall('.//param'):
                param_type = param.find('type')
                param_name = param.find('declname')

                params.append({
                    'type': ''.join(param_type.itertext()) if param_type is not None else '',
                    'name': param_name.text if param_name is not None else ''
                })

            # Extract return type and description
            return_desc = ''
            for simplesect in memberdef.findall('.//simplesect'):
                if simplesect.get('kind') == 'return':
                    return_desc = self._extract_description(simplesect)

            return {
                'kind': kind,
                'name': name_text,
                'type': type_text,
                'brief': briefdesc,
                'detailed': detaileddesc,
                'params': params,
                'return': return_desc
            }

        except Exception as e:
            logger.error(f"Failed to parse member: {e}")
            return None

    def _extract_description(self, desc_elem: Optional[ET.Element]) -> str:
        """Extract description text from XML element."""
        if desc_elem is None:
            return ''

        # Extract all text, handling special elements
        text_parts = []

        for elem in desc_elem.iter():
            if elem.text:
                text_parts.append(elem.text)
            if elem.tail:
                text_parts.append(elem.tail)

        return ' '.join(text_parts).strip()

    def validate_freshness(self, doxygen_entity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate if Doxygen documentation is still fresh/accurate.

        Args:
            doxygen_entity: Doxygen entity (class, function, etc.)

        Returns:
            Validation result with freshness score and issues
        """
        file_path = doxygen_entity.get('file', '')
        entity_name = doxygen_entity.get('name', '')
        entity_kind = doxygen_entity.get('kind', '')

        # Get current source code
        if file_path not in self.source_files:
            return {
                'fresh': False,
                'score': 0.0,
                'issues': [f'Source file not found: {file_path}'],
                'recommendation': 'remove'
            }

        current_source = self.source_files[file_path]

        # Check if entity still exists in source
        if entity_kind in ['class', 'struct']:
            pattern = rf'\b(class|struct)\s+{re.escape(entity_name)}\b'
        elif entity_kind == 'function':
            pattern = rf'\b{re.escape(entity_name)}\s*\('
        elif entity_kind == 'namespace':
            pattern = rf'\bnamespace\s+{re.escape(entity_name)}\b'
        else:
            pattern = rf'\b{re.escape(entity_name)}\b'

        entity_exists = bool(re.search(pattern, current_source))

        if not entity_exists:
            return {
                'fresh': False,
                'score': 0.0,
                'issues': [f'{entity_kind.capitalize()} "{entity_name}" not found in source code'],
                'recommendation': 'remove'
            }

        # Use LLM to validate documentation accuracy
        validation_prompt = self._build_validation_prompt(doxygen_entity, current_source)

        try:
            llm_response = self.llm.generate(validation_prompt)
            validation_result = self._parse_validation_response(llm_response)

            return validation_result

        except Exception as e:
            logger.error(f"LLM validation failed: {e}")
            return {
                'fresh': True,  # Assume fresh if validation fails
                'score': 0.5,
                'issues': ['Could not validate with LLM'],
                'recommendation': 'review'
            }

    def _build_validation_prompt(self, doxygen_entity: Dict[str, Any], current_source: str) -> str:
        """Build prompt for LLM validation."""
        entity_name = doxygen_entity.get('name', '')
        entity_kind = doxygen_entity.get('kind', '')
        brief = doxygen_entity.get('brief', '')
        detailed = doxygen_entity.get('detailed', '')

        # Truncate source for context
        source_excerpt = current_source[:5000]

        prompt = f"""Validate if this legacy Doxygen documentation is still accurate.

**Entity:** {entity_kind} `{entity_name}`

**Legacy Documentation:**
Brief: {brief}
Detailed: {detailed}

**Current Source Code Excerpt:**
```cpp
{source_excerpt}
```

**Your Task:**
1. Check if the entity still exists in the source code
2. Verify if the documentation accurately describes the current implementation
3. Identify any discrepancies or outdated information
4. Assign a freshness score (0.0 = completely outdated, 1.0 = fully accurate)
5. Provide a recommendation: 'keep', 'update', 'remove', or 'review'

**Output Format (JSON):**
```json
{{
  "fresh": true/false,
  "score": 0.0-1.0,
  "issues": ["list of issues found"],
  "recommendation": "keep/update/remove/review",
  "suggested_updates": "suggested corrections if needed"
}}
```"""

        return prompt

    def _parse_validation_response(self, llm_response: str) -> Dict[str, Any]:
        """Parse LLM validation response."""
        import json

        # Try to extract JSON from response
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', llm_response, re.DOTALL)

        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Fallback: parse manually
        score_match = re.search(r'"score":\s*([\d.]+)', llm_response)
        score = float(score_match.group(1)) if score_match else 0.5

        recommendation_match = re.search(r'"recommendation":\s*"(\w+)"', llm_response)
        recommendation = recommendation_match.group(1) if recommendation_match else 'review'

        return {
            'fresh': score >= 0.7,
            'score': score,
            'issues': [],
            'recommendation': recommendation,
            'suggested_updates': ''
        }

    def merge_into_documentation(
        self,
        doxygen_entity: Dict[str, Any],
        existing_docs: Dict[str, str],
        validation_result: Dict[str, Any]
    ) -> Tuple[str, str, str]:
        """
        Merge Doxygen documentation into existing documentation.

        Args:
            doxygen_entity: Doxygen entity data
            existing_docs: Existing MkDocs documentation (file path -> content)
            validation_result: Freshness validation result

        Returns:
            Tuple of (target_file, merge_strategy, merged_content)
            merge_strategy: 'integrate', 'new_section', 'skip'
        """
        entity_name = doxygen_entity.get('name', '')
        entity_kind = doxygen_entity.get('kind', '')

        # Skip if documentation is outdated
        if validation_result['recommendation'] == 'remove':
            return ('', 'skip', '')

        # Format Doxygen content as Markdown
        markdown_content = self._format_as_markdown(doxygen_entity, validation_result)

        # Find best matching existing document
        best_match = self._find_best_match(entity_name, entity_kind, existing_docs)

        if best_match:
            # Integrate into existing document
            target_file, existing_content = best_match
            merged_content = self._integrate_content(existing_content, markdown_content, entity_name)

            return (target_file, 'integrate', merged_content)
        else:
            # Create new section
            new_file = self._generate_filename(entity_name, entity_kind)

            return (new_file, 'new_section', markdown_content)

    def _format_as_markdown(self, doxygen_entity: Dict[str, Any], validation_result: Dict[str, Any]) -> str:
        """Format Doxygen entity as Markdown."""
        entity_name = doxygen_entity.get('name', '')
        entity_kind = doxygen_entity.get('kind', '')
        brief = doxygen_entity.get('brief', '')
        detailed = doxygen_entity.get('detailed', '')

        markdown = f"## {entity_kind.capitalize()}: `{entity_name}`\n\n"

        # Add freshness warning if needed
        if validation_result['score'] < 0.8:
            markdown += "!!! warning \"Legacy Documentation\"\n"
            markdown += f"    This documentation was imported from Doxygen (freshness: {validation_result['score']:.0%}).\n"
            if validation_result.get('suggested_updates'):
                markdown += f"    Suggested updates: {validation_result['suggested_updates']}\n"
            markdown += "\n"

        if brief:
            markdown += f"**Brief:** {brief}\n\n"

        if detailed:
            markdown += f"{detailed}\n\n"

        # Add members if it's a class
        members = doxygen_entity.get('members', [])
        if members:
            markdown += "### Members\n\n"
            for member in members:
                member_kind = member.get('kind', '')
                member_name = member.get('name', '')
                member_brief = member.get('brief', '')

                markdown += f"#### `{member_name}` ({member_kind})\n\n"
                if member_brief:
                    markdown += f"{member_brief}\n\n"

                # Add function signature
                if member_kind == 'function':
                    params = member.get('params', [])
                    param_str = ', '.join([f"{p['type']} {p['name']}" for p in params])
                    markdown += f"```cpp\n{member['type']} {member_name}({param_str})\n```\n\n"

        return markdown

    def _find_best_match(self, entity_name: str, entity_kind: str, existing_docs: Dict[str, str]) -> Optional[Tuple[str, str]]:
        """Find best matching existing documentation file."""
        # Search for entity name in existing docs
        for file_path, content in existing_docs.items():
            # Check if entity is mentioned
            if entity_name in content:
                return (file_path, content)

            # Check if file name is related
            if entity_name.lower() in Path(file_path).stem.lower():
                return (file_path, content)

        return None

    def _integrate_content(self, existing_content: str, new_content: str, entity_name: str) -> str:
        """Integrate new content into existing documentation."""
        # Find appropriate insertion point
        # Look for existing section about this entity
        section_pattern = rf'^##+ .*{re.escape(entity_name)}.*$'
        match = re.search(section_pattern, existing_content, re.MULTILINE)

        if match:
            # Replace existing section
            # Find end of section (next heading of same or higher level)
            start = match.start()
            heading_level = len(re.match(r'^(#+)', match.group()).group(1))
            end_pattern = rf'^#{{{1,{heading_level}}}} '

            end_match = re.search(end_pattern, existing_content[start + len(match.group()):], re.MULTILINE)

            if end_match:
                end = start + len(match.group()) + end_match.start()
            else:
                end = len(existing_content)

            # Insert new content with freshness note
            merged = existing_content[:start] + \
                    f"\n<!-- Merged from Doxygen -->\n{new_content}\n" + \
                    existing_content[end:]

            return merged
        else:
            # Append at end
            return existing_content + f"\n\n<!-- Added from Doxygen -->\n{new_content}"

    def _generate_filename(self, entity_name: str, entity_kind: str) -> str:
        """Generate filename for new documentation section."""
        # Convert CamelCase to kebab-case
        name = re.sub(r'(?<!^)(?=[A-Z])', '-', entity_name).lower()

        # Sanitize
        name = re.sub(r'[^a-z0-9-]', '', name)

        return f"doxygen-{entity_kind}-{name}.md"

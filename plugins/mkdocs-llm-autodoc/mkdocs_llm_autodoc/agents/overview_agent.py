"""
High-Level Overview Agent

Generates comprehensive high-level documentation by analyzing the codebase
across multiple thematic topics. Uses multi-pass analysis to extract,
synthesize, refine, and organize information.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..utils.topic_definitions import TopicRegistry, Topic
from ..utils.state_manager import StateManager, AnalysisPhase
from ..utils.dependency_analyzer import DependencyAnalyzer
from ..utils.cross_linker import CrossLinker
from ..utils.nav_updater import NavUpdater, SmartNavBuilder


logger = logging.getLogger('mkdocs.plugins.llm-autodoc.overview')


class HighLevelOverviewAgent:
    """
    Agent for generating high-level thematic documentation.

    Implements multi-pass analysis:
    1. Topic Extraction: Analyze each file for each topic
    2. Topic Synthesis: Combine findings into topic documents
    3. Topic Refinement: Clean up and structure the documents
    4. Dependency Analysis: Create relationship diagrams
    5. Index Generation: Create master navigation index
    """

    def __init__(self, llm_provider, cache_manager, state_manager: StateManager, mkdocs_yml_path: str = None, docs_dir: str = None):
        self.llm = llm_provider
        self.cache = cache_manager
        self.state = state_manager
        self.dependency_analyzer = DependencyAnalyzer()
        self.cross_linker = CrossLinker(llm_provider=llm_provider)
        self.nav_updater = NavUpdater(mkdocs_yml_path, docs_dir) if mkdocs_yml_path and docs_dir else None
        self.topics = TopicRegistry.get_all_topics()

    def generate(
        self,
        project_structure: Dict[str, Any],
        output_dir: str,
        generated_docs: List[str] = None,
        max_workers: int = 3,
        force_regenerate: bool = False
    ) -> List[str]:
        """
        Generate high-level overview documentation using BOTH source code AND generated markdown docs.

        This hybrid approach:
        1. Analyzes source code for implementation details and patterns
        2. Leverages already generated markdown documentation for structured insights
        3. Combines both sources for comprehensive topic documentation

        Args:
            project_structure: Parsed project structure
            output_dir: Directory to write documentation
            generated_docs: List of already generated markdown documentation files (optional)
            max_workers: Number of parallel workers
            force_regenerate: Force regeneration of all topics

        Returns:
            List of generated file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        all_files = project_structure.get('all_files', [])
        all_docs = generated_docs if generated_docs else []

        logger.info(f"📊 Overview generation sources:")
        logger.info(f"   - Source files: {len(all_files)}")
        logger.info(f"   - Generated docs: {len(all_docs)}")

        project_hash = self._calculate_project_hash(project_structure)

        # Initialize state
        if force_regenerate:
            self.state.reset()

        self.state.start_analysis(len(all_files), project_hash)

        generated_files = []

        # Phase 1: Topic Extraction (from both source and docs)
        logger.info("=" * 70)
        logger.info("PHASE 1: TOPIC EXTRACTION (Hybrid: Source + Docs)")
        logger.info("=" * 70)
        extraction_results = self._phase_1_topic_extraction(
            all_files, all_docs, project_structure, max_workers
        )

        # Phase 2: Topic Synthesis
        logger.info("=" * 70)
        logger.info("PHASE 2: TOPIC SYNTHESIS")
        logger.info("=" * 70)
        self.state.set_current_phase(AnalysisPhase.TOPIC_SYNTHESIS)
        synthesis_files = self._phase_2_topic_synthesis(
            extraction_results, project_structure, output_path, max_workers
        )
        generated_files.extend(synthesis_files)

        # Phase 3: Topic Refinement
        logger.info("=" * 70)
        logger.info("PHASE 3: TOPIC REFINEMENT")
        logger.info("=" * 70)
        self.state.set_current_phase(AnalysisPhase.TOPIC_REFINEMENT)
        self._phase_3_topic_refinement(synthesis_files, max_workers)

        # Phase 4: Dependency Analysis
        logger.info("=" * 70)
        logger.info("PHASE 4: DEPENDENCY ANALYSIS")
        logger.info("=" * 70)
        self.state.set_current_phase(AnalysisPhase.DEPENDENCY_ANALYSIS)
        dep_file = self._phase_4_dependency_analysis(
            project_structure, all_files, output_path
        )
        if dep_file:
            generated_files.append(dep_file)

        # Phase 5: Index Generation
        logger.info("=" * 70)
        logger.info("PHASE 5: INDEX GENERATION")
        logger.info("=" * 70)
        self.state.set_current_phase(AnalysisPhase.INDEX_GENERATION)
        index_file = self._phase_5_index_generation(
            synthesis_files, project_structure, output_path
        )
        if index_file:
            generated_files.append(index_file)

        # Phase 6: Cross-Linking
        logger.info("=" * 70)
        logger.info("PHASE 6: CROSS-LINKING")
        logger.info("=" * 70)
        all_doc_files = generated_files + ([index_file] if index_file else [])
        self._phase_6_cross_linking(all_doc_files)

        # Phase 7: Navigation Update (NEW!)
        logger.info("=" * 70)
        logger.info("PHASE 7: NAVIGATION UPDATE")
        logger.info("=" * 70)
        self._phase_7_navigation_update(all_doc_files)

        # Mark complete
        self.state.set_current_phase(AnalysisPhase.COMPLETED)

        logger.info("=" * 70)
        logger.info(f"✅ HIGH-LEVEL OVERVIEW GENERATION COMPLETE")
        logger.info(f"   Generated {len(generated_files)} documentation files")
        logger.info("=" * 70)

        return generated_files

    def _phase_1_topic_extraction(
        self,
        all_files: List[str],
        generated_docs: List[str],
        project_structure: Dict[str, Any],
        max_workers: int
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Phase 1: Extract relevant information from BOTH source files AND generated docs for each topic.

        This hybrid extraction:
        - Analyzes source code for patterns and implementation details
        - Reads generated markdown docs for structured insights and code reviews
        - Combines both for comprehensive topic coverage

        Args:
            all_files: List of source code files
            generated_docs: List of generated markdown documentation files
            project_structure: Project structure
            max_workers: Number of parallel workers

        Returns:
            Dictionary: topic_id -> list of extraction results
        """
        extraction_results = {topic.id: [] for topic in self.topics}

        # Build mapping from source file to its documentation
        doc_mapping = self._build_doc_mapping(all_files, generated_docs)

        # Process topics by priority
        for priority in [1, 2, 3, 4, 5]:
            priority_topics = TopicRegistry.get_topics_by_priority(priority)

            if not priority_topics:
                continue

            logger.info(f"📊 Processing Priority {priority} Topics ({len(priority_topics)} topics)")

            for topic in priority_topics:
                # Check if extraction is already complete
                if self.state.is_topic_extraction_complete(topic.id):
                    logger.info(f"  ⏭️  Topic '{topic.name}': extraction already complete (from cache)")
                    # Load from intermediate results
                    cached_results = self.state.get_intermediate_result(topic.id, 'extraction_results')
                    if cached_results:
                        extraction_results[topic.id] = cached_results
                    continue

                logger.info(f"  📝 Extracting: {topic.name}")

                # Get unprocessed files
                unprocessed_files = self.state.get_unprocessed_files_for_topic(topic.id, all_files)

                if not unprocessed_files:
                    logger.info(f"     ✓ All files already processed")
                    self.state.mark_topic_extraction_complete(topic.id)
                    continue

                logger.info(f"     Processing {len(unprocessed_files)} files...")

                # Process files in parallel (using BOTH source and docs)
                topic_results = []
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {
                        executor.submit(
                            self._extract_topic_from_file,
                            topic, file_path, doc_mapping.get(file_path), project_structure
                        ): file_path
                        for file_path in unprocessed_files
                    }

                    for future in as_completed(futures):
                        file_path = futures[future]
                        try:
                            result = future.result()
                            if result and result.get('has_relevant_info'):
                                topic_results.append(result)
                            self.state.mark_file_processed_for_topic(topic.id, file_path)
                        except Exception as e:
                            logger.error(f"     ✗ Error processing {file_path}: {e}")

                extraction_results[topic.id].extend(topic_results)

                # Save intermediate results
                self.state.store_intermediate_result(topic.id, 'extraction_results', extraction_results[topic.id])
                self.state.mark_topic_extraction_complete(topic.id)

                logger.info(f"     ✓ Extracted {len(topic_results)} relevant file insights")

        return extraction_results

    def _extract_topic_from_file(
        self,
        topic: Topic,
        file_path: str,
        doc_path: Optional[str],
        project_structure: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Extract information relevant to a specific topic from BOTH source file AND its documentation.

        Args:
            topic: The topic to extract information for
            file_path: Path to source file
            doc_path: Path to generated markdown documentation (if exists)
            project_structure: Project structure

        Returns:
            Dictionary with extraction results or None if not relevant
        """
        try:
            # Read source file
            source_content = ""
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    source_content = f.read()

            # Read generated documentation (if exists)
            doc_content = ""
            if doc_path and Path(doc_path).exists():
                with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    doc_content = f.read()

            # Build combined hash for caching
            combined_hash = hash(source_content + doc_content)
            cache_key = f"extract_{topic.id}_{file_path}_{combined_hash}"
            cached = self.cache.get(cache_key)
            if cached:
                return eval(cached)  # Convert string back to dict

            # Check if file is potentially relevant using keywords (check both sources)
            is_source_relevant = self._is_file_relevant_to_topic(source_content, topic)
            is_doc_relevant = self._is_file_relevant_to_topic(doc_content, topic)

            if not is_source_relevant and not is_doc_relevant:
                return None

            # Ask LLM to extract relevant information from BOTH sources
            prompt = self._build_extraction_prompt_hybrid(
                topic, file_path, source_content, doc_content
            )
            response = self.llm.generate(prompt)

            result = {
                'file': file_path,
                'topic_id': topic.id,
                'has_relevant_info': True,
                'extracted_info': response,
            }

            # Cache result
            self.cache.set(cache_key, str(result))

            return result

        except Exception as e:
            logger.error(f"Error extracting topic from {file_path}: {e}")
            return None

    def _build_doc_mapping(self, source_files: List[str], doc_files: List[str]) -> Dict[str, str]:
        """
        Build mapping from source file to its generated documentation file.

        Args:
            source_files: List of source code files
            doc_files: List of generated documentation files

        Returns:
            Dictionary mapping source_file_path -> doc_file_path
        """
        mapping = {}

        for source_file in source_files:
            source_name = Path(source_file).stem
            source_dir = Path(source_file).parent.name

            # Try to find corresponding doc file
            for doc_file in doc_files:
                doc_name = Path(doc_file).stem
                doc_content_indicator = Path(doc_file).parent.name

                # Match by filename
                if source_name.lower() in doc_name.lower():
                    mapping[source_file] = doc_file
                    break
                # Match by directory + name
                elif source_dir in doc_file and source_name in doc_file:
                    mapping[source_file] = doc_file
                    break

        logger.info(f"   Built doc mapping: {len(mapping)} source files have corresponding docs")
        return mapping

    def _is_file_relevant_to_topic(self, content: str, topic: Topic) -> bool:
        """Quick check if file might be relevant to topic using keywords"""
        if not content:
            return False

        content_lower = content.lower()

        # Check if any keyword appears in the file
        for keyword in topic.keywords:
            if keyword.lower() in content_lower:
                return True

        return False

    def _build_extraction_prompt_hybrid(
        self,
        topic: Topic,
        file_path: str,
        source_content: str,
        doc_content: str
    ) -> str:
        """Build prompt for extracting topic information from BOTH source and documentation"""

        # Limit content size for LLM
        max_chars = 6000
        if len(source_content) > max_chars:
            source_content = source_content[:max_chars] + "\n\n... (truncated)"
        if len(doc_content) > max_chars:
            doc_content = doc_content[:max_chars] + "\n\n... (truncated)"

        prompt = f"""Analyze both the source code AND its generated documentation to extract information relevant to: **{topic.name}**

# Topic Description
{topic.description}

# Specific Questions to Answer
{self._format_questions(topic.questions)}

# File Information
**Path**: {file_path}

# Source Code
```
{source_content if source_content else "No source code available"}
```

# Generated Documentation
```markdown
{doc_content if doc_content else "No documentation generated yet"}
```

# Your Task
Analyze BOTH the source code and its documentation to extract information relevant to the topic "{topic.name}".

**Prioritize information from the generated documentation** as it already contains:
- Structured explanations
- Code reviews and improvements
- Best practices
- Examples

**Supplement with source code** for:
- Implementation patterns not explained in docs
- Specific technical details
- Additional context

Answer these specific questions based on what you find:
{self._format_questions(topic.questions)}

# Output Format
Provide a concise summary (max 200 words) of what you found relevant to this topic.

**CRITICAL: Include Code References**:
- **ALWAYS** cite specific files, line numbers, classes, functions, or variables
- Format: `[ClassName](file.cpp:123)` or `[functionName](file.h:45-67)`
- For every claim, provide the source: "According to `[MyClass::init](main.cpp:34)`..."
- Example: "The build system uses CMake (see `[CMakeLists.txt](CMakeLists.txt:1)`)"
- Example: "Thread pool initialized in `[ThreadPool::start](threadpool.cpp:56-89)`"

**Format**:
- Use bullet points
- Be specific and reference code elements
- **Always include file:line references** for traceability
- Cite whether information comes from source code or documentation
- If nothing relevant found, respond with: "No relevant information found."

Generate ONLY the extracted information, no additional commentary.
"""
        return prompt

    def _build_extraction_prompt(self, topic: Topic, file_path: str, content: str) -> str:
        """Build prompt for extracting topic information from a file"""

        # Limit content size for LLM
        max_chars = 8000
        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n... (truncated)"

        prompt = f"""Analyze this source file and extract information relevant to the topic: **{topic.name}**

# Topic Description
{topic.description}

# Specific Questions to Answer
{self._format_questions(topic.questions)}

# File Information
**Path**: {file_path}
**Content**:
```
{content}
```

# Your Task
Analyze this file and extract ONLY information relevant to the topic "{topic.name}".

Answer these specific questions based on what you find in the code:
{self._format_questions(topic.questions)}

# Output Format
Provide a concise summary (max 200 words) of what you found relevant to this topic.

**Format**:
- Use bullet points
- Be specific and reference code elements (classes, functions, variables)
- Include file paths or line references where applicable
- If nothing relevant found, respond with: "No relevant information found."

Generate ONLY the extracted information, no additional commentary.
"""
        return prompt

    def _format_questions(self, questions: List[str]) -> str:
        """Format questions as numbered list"""
        return '\n'.join(f"{i+1}. {q}" for i, q in enumerate(questions))

    def _phase_2_topic_synthesis(
        self,
        extraction_results: Dict[str, List[Dict[str, Any]]],
        project_structure: Dict[str, Any],
        output_path: Path,
        max_workers: int
    ) -> List[str]:
        """
        Phase 2: Synthesize extracted information into cohesive topic documents.

        Returns:
            List of generated file paths
        """
        generated_files = []

        # Create overview directory
        overview_dir = output_path / 'overview'
        overview_dir.mkdir(parents=True, exist_ok=True)

        def synthesize_topic(topic: Topic) -> Optional[str]:
            # Check if already synthesized
            if self.state.is_topic_synthesis_complete(topic.id):
                existing_file = self.state.get_topic_output_file(topic.id)
                if existing_file and Path(existing_file).exists():
                    logger.info(f"  ⏭️  Topic '{topic.name}': already synthesized")
                    return existing_file

            extractions = extraction_results.get(topic.id, [])

            if not extractions:
                logger.info(f"  ⏭️  Topic '{topic.name}': no relevant information found")
                return None

            logger.info(f"  🔨 Synthesizing: {topic.name} ({len(extractions)} sources)")

            # Build synthesis prompt
            prompt = self._build_synthesis_prompt(topic, extractions, project_structure)
            response = self.llm.generate(prompt)

            # Write to file
            safe_name = topic.id.replace('_', '-')
            output_file = overview_dir / f"{safe_name}.md"
            output_file.write_text(response, encoding='utf-8')

            self.state.mark_topic_synthesis_complete(topic.id, str(output_file))

            logger.info(f"     ✓ Generated: {output_file.name}")
            return str(output_file)

        # Process topics in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(synthesize_topic, topic): topic for topic in self.topics}

            for future in as_completed(futures):
                topic = futures[future]
                try:
                    result = future.result()
                    if result:
                        generated_files.append(result)
                except Exception as e:
                    logger.error(f"  ✗ Error synthesizing topic '{topic.name}': {e}")

        logger.info(f"✅ Synthesized {len(generated_files)} topic documents")
        return generated_files

    def _build_synthesis_prompt(
        self,
        topic: Topic,
        extractions: List[Dict[str, Any]],
        project_structure: Dict[str, Any]
    ) -> str:
        """Build prompt for synthesizing topic document"""

        # Combine all extracted information
        combined_info = "\n\n".join([
            f"**From {e['file']}:**\n{e['extracted_info']}"
            for e in extractions
        ])

        prompt = f"""Create a comprehensive documentation section about: **{topic.name}**

# Topic Overview
{topic.description}

# Key Questions to Address
{self._format_questions(topic.questions)}

# Information Extracted from Codebase
The following information was extracted from {len(extractions)} files:

{combined_info}

# Your Task
Create a well-structured, comprehensive documentation section about "{topic.name}" for this project.

## Requirements
1. **Answer all key questions** listed above based on the extracted information
2. **Organize information logically** with clear headings and subheadings
3. **Be specific**: Reference actual files, classes, functions, and code elements
4. **Include examples**: Show code snippets where relevant
5. **Remove duplicates**: Consolidate repeated information
6. **Add context**: Explain why things are done this way
7. **Use Mermaid diagrams** where helpful (architecture, flow, etc.)
8. **CRITICAL: Always include code references** for traceability

## Code References (MANDATORY)
**Every statement must be traceable to source code:**
- Format: `[ClassName](file.cpp:123)` or `[functionName](file.h:45-67)` or `[file.cpp](file.cpp:1)`
- Examples:
  - "The application starts in `[main()](src/main.cpp:15)`"
  - "Build configuration is in `[CMakeLists.txt](CMakeLists.txt:1)`"
  - "Thread pool is initialized via `[ThreadPool::init](threadpool.cpp:45-78)`"
  - "Error handling uses exceptions (see `[ErrorHandler](errors.h:23)`)"
- **For every feature mentioned, cite the code location**
- **For every claim, provide evidence with file:line references**
- This ensures documentation is always verifiable and maintainable

## Structure
Use this general structure (adapt as needed):

# {topic.name}

## Overview
Brief introduction (2-3 sentences)

## [Relevant Section 1]
Content...

## [Relevant Section 2]
Content...

## Key Files
List of important files related to this topic

## Examples
Practical examples or code snippets

## Best Practices
Recommendations for developers

## See Also
Links to related topics (use format: `[Topic Name](topic-id.md)`)

# Output Format
- Use Markdown with proper headings
- Include code blocks with syntax highlighting
- Use Mermaid diagrams where appropriate
- Keep it practical and developer-focused
- Aim for 300-500 words per topic

Generate ONLY the markdown content, no additional commentary.
"""
        return prompt

    def _phase_3_topic_refinement(self, topic_files: List[str], max_workers: int):
        """
        Phase 3: Refine topic documents - remove duplicates, improve structure.
        """
        logger.info(f"Refining {len(topic_files)} topic documents...")

        def refine_topic(file_path: str):
            topic_id = Path(file_path).stem.replace('-', '_')

            if self.state.is_topic_refinement_complete(topic_id):
                logger.info(f"  ⏭️  {Path(file_path).name}: already refined")
                return

            try:
                # Read current content
                content = Path(file_path).read_text(encoding='utf-8')

                # Build refinement prompt
                prompt = self._build_refinement_prompt(content, file_path)
                refined = self.llm.generate(prompt)

                # Write refined version
                Path(file_path).write_text(refined, encoding='utf-8')

                self.state.mark_topic_refinement_complete(topic_id)
                logger.info(f"  ✨ Refined: {Path(file_path).name}")

            except Exception as e:
                logger.error(f"  ✗ Error refining {file_path}: {e}")

        # Process in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(refine_topic, f) for f in topic_files]
            for future in as_completed(futures):
                future.result()  # Wait for completion

        logger.info(f"✅ Refined all topic documents")

    def _build_refinement_prompt(self, content: str, file_path: str) -> str:
        """Build prompt for refining a topic document"""

        prompt = f"""Review and refine this documentation section.

# Current Content
```markdown
{content}
```

# Your Task
Refine this documentation by:

1. **Remove duplicates**: Eliminate repeated information
2. **Improve structure**: Ensure logical flow and clear hierarchy
3. **Fix formatting**: Ensure proper Markdown syntax
4. **Enhance clarity**: Make explanations clearer and more concise
5. **Add missing sections**: If key information is missing, note it
6. **Improve examples**: Make code examples more practical
7. **Cross-reference**: Add links to related topics where relevant

# Output Format
Return the refined version of the document in Markdown format.
Keep the same general structure but improve quality.

Generate ONLY the refined markdown content, no additional commentary.
"""
        return prompt

    def _phase_4_dependency_analysis(
        self,
        project_structure: Dict[str, Any],
        all_files: List[str],
        output_path: Path
    ) -> Optional[str]:
        """
        Phase 4: Analyze dependencies and create relationship documentation.
        """
        logger.info("Analyzing project dependencies...")

        try:
            # Perform dependency analysis
            dep_analysis = self.dependency_analyzer.analyze_project(project_structure, all_files)

            # Generate documentation
            dep_doc = self._generate_dependency_documentation(dep_analysis)

            # Write to file
            dep_file = output_path / 'overview' / 'dependencies-graph.md'
            dep_file.write_text(dep_doc, encoding='utf-8')

            logger.info(f"✅ Generated dependency documentation: {dep_file.name}")
            return str(dep_file)

        except Exception as e:
            logger.error(f"Error during dependency analysis: {e}")
            return None

    def _generate_dependency_documentation(self, analysis: Dict[str, Any]) -> str:
        """Generate markdown documentation from dependency analysis"""

        mermaid = self.dependency_analyzer.generate_mermaid_diagram()
        stats = self.dependency_analyzer.get_summary_stats()

        doc = f"""# Dependencies Between Components

## Overview

This document provides an analysis of how different components and files in the codebase depend on each other.

## Summary Statistics

- **Total Files Analyzed**: {stats['total_files_analyzed']}
- **Total Dependencies**: {stats['total_dependencies']}
- **Average Dependencies per File**: {stats['average_dependencies_per_file']}
- **Circular Dependencies**: {stats['circular_dependency_count']}
- **Hub Files** (highly depended upon): {stats['hub_file_count']}
- **Leaf Files** (no internal dependencies): {stats['leaf_file_count']}

## Dependency Graph

```mermaid
{mermaid}
```

## Hub Files

These files are heavily depended upon by other parts of the codebase:

"""
        # Add hub files
        for i, hub in enumerate(analysis.get('hub_files', [])[:10], 1):
            doc += f"\n### {i}. {Path(hub['file']).name}\n"
            doc += f"- **Depended upon by**: {hub['dependent_count']} files\n"
            if hub.get('classes'):
                doc += f"- **Key Classes**: {', '.join(hub['classes'][:5])}\n"

        # Add circular dependencies if any
        if analysis.get('circular_dependencies'):
            doc += "\n## ⚠️ Circular Dependencies\n\n"
            doc += "The following circular dependencies were detected:\n\n"
            for i, cycle in enumerate(analysis['circular_dependencies'][:5], 1):
                doc += f"{i}. {' → '.join(Path(f).name for f in cycle)}\n"

        # Add component groups
        if analysis.get('component_groups'):
            doc += "\n## Component Groups\n\n"
            doc += "Highly coupled groups of files:\n\n"
            for i, group in enumerate(analysis['component_groups'][:5], 1):
                doc += f"### Group {i} ({group['size']} files)\n"
                doc += f"- **Internal Dependencies**: {group['internal_dependencies']}\n"
                doc += "- **Files**: " + ", ".join(Path(f).name for f in group['files'][:10]) + "\n\n"

        return doc

    def _phase_5_index_generation(
        self,
        topic_files: List[str],
        project_structure: Dict[str, Any],
        output_path: Path
    ) -> Optional[str]:
        """
        Phase 5: Generate master index/navigation for all topics.
        """
        logger.info("Generating master index...")

        try:
            # Group topics by priority
            topics_by_priority = {}
            for topic in self.topics:
                if topic.priority not in topics_by_priority:
                    topics_by_priority[topic.priority] = []
                topics_by_priority[topic.priority].append(topic)

            # Build index content
            index_content = """# High-Level Code Overview

Welcome to the high-level documentation for this project. This section provides thematic documentation organized by common developer questions and concerns.

## 📚 Documentation Topics

"""

            priority_labels = {
                1: "🔥 Critical - Start Here",
                2: "⭐ Essential - Core Understanding",
                3: "💡 Important - Quality & Process",
                4: "🔧 Operational - Deployment & Monitoring",
                5: "📖 Reference - Additional Information"
            }

            for priority in sorted(topics_by_priority.keys()):
                topics = topics_by_priority[priority]
                label = priority_labels.get(priority, f"Priority {priority}")

                index_content += f"\n### {label}\n\n"

                for topic in topics:
                    # Check if topic file exists
                    topic_file = output_path / 'overview' / f"{topic.id.replace('_', '-')}.md"
                    if topic_file.exists():
                        index_content += f"- **[{topic.name}](overview/{topic.id.replace('_', '-')}.md)**: {topic.description}\n"

            # Add dependency graph link
            dep_file = output_path / 'overview' / 'dependencies-graph.md'
            if dep_file.exists():
                index_content += "\n### 🔗 Additional Resources\n\n"
                index_content += "- **[Dependencies & Component Relationships](overview/dependencies-graph.md)**: Detailed analysis of how components interact\n"

            # Add navigation tips
            index_content += """

## 💡 How to Use This Documentation

1. **New to the project?** Start with the "Critical" section topics
2. **Working on a specific area?** Use the search or topic index above
3. **Need to understand dependencies?** Check the Dependencies Graph
4. **Looking for specific code?** Use the detailed API documentation

## 📊 Documentation Statistics

"""
            index_content += f"- **Total Topics Covered**: {len(topic_files)}\n"
            index_content += f"- **Total Files Analyzed**: {len(project_structure.get('all_files', []))}\n"
            index_content += f"- **Modules Documented**: {len(project_structure.get('modules', []))}\n"

            # Write index file
            index_file = output_path / '00-overview-index.md'
            index_file.write_text(index_content, encoding='utf-8')

            logger.info(f"✅ Generated master index: {index_file.name}")
            return str(index_file)

        except Exception as e:
            logger.error(f"Error generating index: {e}")
            return None

    def _phase_6_cross_linking(self, all_generated_files: List[str]):
        """
        Phase 6: Create intelligent cross-links between documentation files.

        Analyzes content similarity and inserts "See Also" sections.
        """
        logger.info("Creating cross-links between documentation files...")

        try:
            # Analyze documents and build similarity graph
            self.cross_linker.analyze_documents(all_generated_files)

            # Generate cross-link recommendations
            recommendations = self.cross_linker.generate_cross_links(max_links_per_doc=5)

            # Insert links into files
            updated_count = self.cross_linker.insert_cross_links(recommendations)

            logger.info(f"✅ Cross-linking complete: {updated_count} files updated with related links")

        except Exception as e:
            logger.error(f"Error during cross-linking: {e}")

    def _phase_7_navigation_update(self, all_generated_files: List[str]):
        """
        Phase 7: Update mkdocs.yml navigation with generated documentation.

        Intelligently merges with existing navigation structure.
        """
        if not self.nav_updater:
            logger.warning("Navigation updater not configured - skipping nav update")
            return

        logger.info("Updating mkdocs.yml navigation...")

        try:
            # Preview changes
            preview = self.nav_updater.preview_changes(all_generated_files)
            logger.info(f"\n{preview}")

            # Update navigation
            success = self.nav_updater.update_navigation(all_generated_files)

            if success:
                logger.info(f"✅ Navigation update complete: mkdocs.yml updated")
            else:
                logger.error("❌ Failed to update navigation")

        except Exception as e:
            logger.error(f"Error during navigation update: {e}")

    def _calculate_project_hash(self, project_structure: Dict[str, Any]) -> str:
        """Calculate a hash of the project structure for change detection"""
        import hashlib
        structure_str = str(sorted(project_structure.get('all_files', [])))
        return hashlib.sha256(structure_str.encode()).hexdigest()[:16]

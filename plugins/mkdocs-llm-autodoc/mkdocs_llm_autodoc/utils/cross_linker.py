"""
Cross-Linker for Markdown Documentation

Analyzes all generated markdown files and creates intelligent cross-links
between related documents for better navigation.
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


logger = logging.getLogger('mkdocs.plugins.llm-autodoc.cross-linker')


class DocumentNode:
    """Represents a documentation file with metadata"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = ""
        self.title = ""
        self.headings = []
        self.keywords = set()
        self.mentioned_files = set()  # Files explicitly mentioned
        self.mentioned_classes = set()
        self.mentioned_functions = set()
        self.related_topics = set()
        self.existing_links = set()  # Links already in the document

    def load(self):
        """Load and parse the markdown file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()

            self._parse_metadata()
        except Exception as e:
            logger.error(f"Error loading {self.file_path}: {e}")

    def _parse_metadata(self):
        """Extract metadata from markdown content"""
        # Extract title (first # heading)
        title_match = re.search(r'^#\s+(.+)$', self.content, re.MULTILINE)
        if title_match:
            self.title = title_match.group(1)

        # Extract all headings
        self.headings = re.findall(r'^#{1,6}\s+(.+)$', self.content, re.MULTILINE)

        # Extract existing markdown links
        self.existing_links = set(re.findall(r'\[.+?\]\((.+?)\)', self.content))

        # Extract code references (file:line format)
        file_refs = re.findall(r'\[.+?\]\(([^)]+\.(?:cpp|h|hpp|py|md))(?::\d+)?\)', self.content)
        self.mentioned_files.update(file_refs)

        # Extract class/function mentions
        self.mentioned_classes = set(re.findall(r'`([A-Z][a-zA-Z0-9_]+)`', self.content))
        self.mentioned_functions = set(re.findall(r'`([a-z_][a-zA-Z0-9_]+)\(\)`', self.content))

        # Extract keywords (words in bold or code blocks)
        keywords = re.findall(r'\*\*([^*]+)\*\*', self.content)
        keywords.extend(re.findall(r'`([^`]+)`', self.content))
        self.keywords = set(w.lower() for w in keywords if len(w) > 3)


class CrossLinker:
    """
    Creates intelligent cross-links between documentation files.

    Features:
    - Thematic similarity detection
    - Automatic "See Also" section generation
    - Inline link suggestions
    - Bidirectional linking
    """

    def __init__(self, llm_provider=None):
        self.llm = llm_provider
        self.documents = {}  # file_path -> DocumentNode
        self.similarity_graph = defaultdict(list)  # file -> [(related_file, score), ...]

    def analyze_documents(self, doc_files: List[str]) -> Dict[str, List[Tuple[str, float]]]:
        """
        Analyze all documentation files and build similarity graph.

        Args:
            doc_files: List of markdown file paths

        Returns:
            Similarity graph: file -> [(related_file, similarity_score), ...]
        """
        logger.info(f"🔗 Analyzing {len(doc_files)} documents for cross-linking...")

        # Load all documents
        for file_path in doc_files:
            if file_path.endswith('.md'):
                doc = DocumentNode(file_path)
                doc.load()
                self.documents[file_path] = doc

        logger.info(f"   Loaded {len(self.documents)} markdown documents")

        # Build similarity graph
        self._build_similarity_graph()

        return self.similarity_graph

    def _build_similarity_graph(self):
        """Build graph of document similarities"""
        docs_list = list(self.documents.items())

        for i, (file_a, doc_a) in enumerate(docs_list):
            for file_b, doc_b in docs_list[i+1:]:
                if file_a == file_b:
                    continue

                # Calculate similarity score
                score = self._calculate_similarity(doc_a, doc_b)

                if score > 0.2:  # Threshold for relatedness
                    self.similarity_graph[file_a].append((file_b, score))
                    self.similarity_graph[file_b].append((file_a, score))

        # Sort by score
        for file_path in self.similarity_graph:
            self.similarity_graph[file_path].sort(key=lambda x: x[1], reverse=True)

        total_links = sum(len(links) for links in self.similarity_graph.values()) // 2
        logger.info(f"   Found {total_links} potential cross-link relationships")

    def _calculate_similarity(self, doc_a: DocumentNode, doc_b: DocumentNode) -> float:
        """
        Calculate similarity score between two documents.

        Uses multiple signals:
        - Shared keywords
        - Shared class/function mentions
        - Shared file references
        - Title similarity
        """
        score = 0.0

        # Keyword overlap (weighted heavily)
        if doc_a.keywords and doc_b.keywords:
            common_keywords = doc_a.keywords & doc_b.keywords
            keyword_score = len(common_keywords) / max(len(doc_a.keywords), len(doc_b.keywords))
            score += keyword_score * 0.4

        # Shared class mentions
        if doc_a.mentioned_classes and doc_b.mentioned_classes:
            common_classes = doc_a.mentioned_classes & doc_b.mentioned_classes
            class_score = len(common_classes) / max(len(doc_a.mentioned_classes), len(doc_b.mentioned_classes))
            score += class_score * 0.3

        # Shared function mentions
        if doc_a.mentioned_functions and doc_b.mentioned_functions:
            common_funcs = doc_a.mentioned_functions & doc_b.mentioned_functions
            func_score = len(common_funcs) / max(len(doc_a.mentioned_functions), len(doc_b.mentioned_functions))
            score += func_score * 0.2

        # Shared file references
        if doc_a.mentioned_files and doc_b.mentioned_files:
            common_files = doc_a.mentioned_files & doc_b.mentioned_files
            file_score = len(common_files) / max(len(doc_a.mentioned_files), len(doc_b.mentioned_files))
            score += file_score * 0.1

        return min(score, 1.0)

    def generate_cross_links(self, max_links_per_doc: int = 5) -> Dict[str, List[str]]:
        """
        Generate cross-link recommendations for each document.

        Args:
            max_links_per_doc: Maximum number of links to suggest per document

        Returns:
            Dictionary: file_path -> list of recommended links
        """
        recommendations = {}

        for file_path, related in self.similarity_graph.items():
            doc = self.documents[file_path]

            # Filter out already linked documents
            new_links = [
                (related_file, score)
                for related_file, score in related
                if not self._is_already_linked(doc, related_file)
            ]

            # Take top N
            top_links = new_links[:max_links_per_doc]
            recommendations[file_path] = [link[0] for link in top_links]

        total_recommendations = sum(len(links) for links in recommendations.values())
        logger.info(f"   Generated {total_recommendations} cross-link recommendations")

        return recommendations

    def _is_already_linked(self, doc: DocumentNode, target_file: str) -> bool:
        """Check if document already links to target"""
        target_filename = Path(target_file).name

        for existing_link in doc.existing_links:
            if target_filename in existing_link:
                return True

        return False

    def insert_cross_links(self, recommendations: Dict[str, List[str]]) -> int:
        """
        Insert cross-links into markdown files.

        Adds or updates "See Also" sections at the end of each document.

        Args:
            recommendations: Dictionary of file -> list of related files

        Returns:
            Number of files updated
        """
        updated_count = 0

        for file_path, related_files in recommendations.items():
            if not related_files:
                continue

            try:
                doc = self.documents[file_path]
                updated_content = self._add_see_also_section(doc, related_files)

                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)

                updated_count += 1

            except Exception as e:
                logger.error(f"Error updating {file_path}: {e}")

        logger.info(f"   Updated {updated_count} files with cross-links")
        return updated_count

    def _add_see_also_section(self, doc: DocumentNode, related_files: List[str]) -> str:
        """Add or update 'See Also' section in document"""
        content = doc.content

        # Build "See Also" section
        see_also_section = "\n\n## See Also\n\n"
        see_also_section += "Related documentation:\n\n"

        for related_file in related_files:
            related_doc = self.documents.get(related_file)
            if not related_doc:
                continue

            # Create relative path
            rel_path = self._get_relative_path(doc.file_path, related_file)

            # Get title
            title = related_doc.title if related_doc.title else Path(related_file).stem.replace('-', ' ').title()

            # Get snippet of what's related
            snippet = self._get_relationship_snippet(doc, related_doc)

            see_also_section += f"- **[{title}]({rel_path})** - {snippet}\n"

        # Check if "See Also" section already exists
        see_also_pattern = r'\n##\s+See Also\s*\n.*?(?=\n##|\Z)'

        if re.search(see_also_pattern, content, re.DOTALL):
            # Replace existing section
            content = re.sub(see_also_pattern, see_also_section, content, flags=re.DOTALL)
        else:
            # Append new section
            content = content.rstrip() + see_also_section

        return content

    def _get_relative_path(self, from_file: str, to_file: str) -> str:
        """Get relative path between two files"""
        from_path = Path(from_file).parent
        to_path = Path(to_file)

        try:
            rel_path = to_path.relative_to(from_path)
            return str(rel_path)
        except ValueError:
            # If can't make relative, try with common base
            from_parts = Path(from_file).parts
            to_parts = Path(to_file).parts

            # Find common base
            common = 0
            for i, (a, b) in enumerate(zip(from_parts, to_parts)):
                if a == b:
                    common = i + 1
                else:
                    break

            # Build relative path
            ups = len(from_parts) - common - 1
            rel = '../' * ups + '/'.join(to_parts[common:])
            return rel

    def _get_relationship_snippet(self, doc_a: DocumentNode, doc_b: DocumentNode) -> str:
        """Get a brief snippet explaining the relationship between documents"""

        # Find common elements
        common_classes = doc_a.mentioned_classes & doc_b.mentioned_classes
        common_keywords = doc_a.mentioned_keywords if hasattr(doc_a, 'mentioned_keywords') else set()

        if common_classes:
            classes_str = ', '.join(list(common_classes)[:2])
            return f"Related classes: {classes_str}"

        # Default generic message
        return "Related topic"

    def generate_llm_enhanced_links(self, file_path: str, max_links: int = 5) -> List[Tuple[str, str]]:
        """
        Use LLM to generate context-aware link suggestions.

        Args:
            file_path: Path to document
            max_links: Maximum number of suggestions

        Returns:
            List of (target_file, explanation) tuples
        """
        if not self.llm:
            return []

        doc = self.documents.get(file_path)
        if not doc:
            return []

        # Get top candidates from similarity graph
        candidates = self.similarity_graph.get(file_path, [])[:max_links * 2]

        if not candidates:
            return []

        # Build prompt for LLM
        prompt = self._build_linking_prompt(doc, candidates)

        try:
            response = self.llm.generate(prompt)
            # Parse response to extract links
            links = self._parse_linking_response(response, candidates)
            return links[:max_links]
        except Exception as e:
            logger.error(f"Error generating LLM links: {e}")
            return []

    def _build_linking_prompt(self, doc: DocumentNode, candidates: List[Tuple[str, float]]) -> str:
        """Build prompt for LLM-based link generation"""

        # Get candidate summaries
        candidate_info = []
        for candidate_file, score in candidates:
            candidate_doc = self.documents.get(candidate_file)
            if candidate_doc:
                candidate_info.append(f"- **{candidate_doc.title}** ({Path(candidate_file).name})")

        candidates_str = '\n'.join(candidate_info[:10])

        prompt = f"""Analyze this documentation and suggest relevant cross-links.

# Current Document
**Title**: {doc.title}
**File**: {Path(doc.file_path).name}

**Content Summary** (first 500 chars):
{doc.content[:500]}

# Candidate Related Documents
{candidates_str}

# Your Task
For the current document, suggest which of the candidate documents would be most valuable to link to, and explain WHY.

**Output Format**:
For each suggested link, provide:
```
LINK: filename.md
REASON: Brief explanation of why this link is valuable (1 sentence)
```

Only suggest links that provide clear value to readers. Maximum 5 suggestions.
"""
        return prompt

    def _parse_linking_response(self, response: str, candidates: List[Tuple[str, float]]) -> List[Tuple[str, str]]:
        """Parse LLM response to extract link suggestions"""
        links = []

        # Extract LINK and REASON pairs
        pattern = r'LINK:\s*([^\n]+)\s*\n\s*REASON:\s*([^\n]+)'
        matches = re.findall(pattern, response, re.MULTILINE)

        for filename, reason in matches:
            filename = filename.strip()
            reason = reason.strip()

            # Find matching candidate
            for candidate_file, _ in candidates:
                if Path(candidate_file).name in filename or filename in candidate_file:
                    links.append((candidate_file, reason))
                    break

        return links

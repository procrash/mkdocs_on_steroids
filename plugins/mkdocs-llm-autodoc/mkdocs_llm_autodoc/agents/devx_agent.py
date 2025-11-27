"""
DevX Documentation Agent

Generates task-oriented documentation for developers and testers.
- Smart Onboarding (Build/Run)
- Tester's Handbook (Aggregated Test Scenarios)
- Contribution Guidelines
"""

import logging
from pathlib import Path
from typing import Dict, List, Any

from ..utils.prompt_manager import get_prompt_manager

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.devx')


class DevXAgent:
    """
    Agent for generating Developer Experience (DevX) documentation.
    """

    def __init__(self, llm_provider, cache_manager):
        self.llm = llm_provider
        self.cache = cache_manager
        self.prompt_manager = get_prompt_manager()

    def generate(self, project_structure: Dict[str, Any], output_dir: str, detailed_docs_dir: str = None) -> List[str]:
        """
        Generate DevX documentation files.

        Args:
            project_structure: Parsed C++ project structure
            output_dir: Directory to write documentation files
            detailed_docs_dir: Directory containing detailed docs (for Tester's Handbook)

        Returns:
            List of generated file paths
        """
        generated_files = []
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 1. Smart Onboarding
        onboarding_file = output_path / '00-smart-onboarding.md'
        content = self._generate_onboarding(project_structure)
        onboarding_file.write_text(content, encoding='utf-8')
        generated_files.append(str(onboarding_file))
        logger.info(f"Generated: {onboarding_file}")

        # 2. Tester's Handbook
        if detailed_docs_dir:
            handbook_file = output_path / 'QA_HANDBOOK.md'
            content = self._generate_testers_handbook(project_structure, detailed_docs_dir)
            handbook_file.write_text(content, encoding='utf-8')
            generated_files.append(str(handbook_file))
            logger.info(f"Generated: {handbook_file}")

        return generated_files

    def _generate_onboarding(self, project_structure: Dict[str, Any]) -> str:
        """Generate smart onboarding guide"""
        
        # Identify build system files
        build_files = []
        all_files = project_structure.get('all_files', [])
        for f in all_files:
            name = Path(f).name.lower()
            if name in ['cmakelists.txt', 'makefile', 'build.gradle', 'pom.xml', 'package.json', 'requirements.txt']:
                build_files.append(f)
        
        # Read content of build files (limit to first 2k chars each to save context)
        build_context = ""
        for bf in build_files[:3]: # Limit to top 3 build files
            try:
                content = Path(bf).read_text(encoding='utf-8')[:2000]
                build_context += f"\n--- {Path(bf).name} ---\n{content}\n"
            except:
                pass

        prompt = self._build_onboarding_prompt(build_context)

        # Check cache
        cache_key = f"devx_onboarding_{hash(build_context)}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info("Using cached onboarding documentation")
            return cached

        # Generate with LLM
        response = self.llm.generate(prompt)

        # Cache result
        self.cache.set(cache_key, response)

        return response

    def _generate_testers_handbook(self, project_structure: Dict[str, Any], detailed_docs_dir: str) -> str:
        """Generate Tester's Handbook from atomic reports"""
        
        # Collect "Tester's Intelligence" sections
        tester_insights = []
        docs_path = Path(detailed_docs_dir)
        
        # Scan classes and functions
        for subdir in ['classes', 'functions']:
            search_path = docs_path / subdir
            if not search_path.exists():
                continue
                
            for doc_file in search_path.glob('*.md'):
                content = doc_file.read_text(encoding='utf-8')
                if "Tester's Intelligence" in content:
                    # Extract the section
                    lines = content.split('\n')
                    capture = False
                    insight = f"### From {doc_file.stem}\n"
                    has_content = False
                    for line in lines:
                        if "Tester's Intelligence" in line:
                            capture = True
                        elif line.startswith('## ') and "Tester's Intelligence" not in line:
                            capture = False
                        elif capture:
                            insight += line + "\n"
                            has_content = True
                    
                    if has_content:
                        tester_insights.append(insight)

        # Limit to top 20 insights to avoid context overflow, or summarize if needed
        # For now, we'll take a representative sample if too large
        aggregated_insights = "\n".join(tester_insights[:20])
        if len(tester_insights) > 20:
            aggregated_insights += f"\n\n... (and {len(tester_insights) - 20} more files with test scenarios)"

        prompt = self._build_tester_prompt(aggregated_insights)

        # Check cache
        cache_key = f"devx_tester_handbook_{hash(aggregated_insights)}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info("Using cached Tester's Handbook")
            return cached

        # Generate with LLM
        response = self.llm.generate(prompt)

        # Cache result
        self.cache.set(cache_key, response)

        return response

    def _build_onboarding_prompt(self, build_context: str) -> str:
        """Build prompt for onboarding"""
        return self.prompt_manager.get_prompt(
            "devx", "onboarding",
            build_context=build_context
        )

    def _build_tester_prompt(self, aggregated_insights: str) -> str:
        """Build prompt for Tester's Handbook"""
        return self.prompt_manager.get_prompt(
            "devx", "testing",
            aggregated_insights=aggregated_insights
        )

"""
Prompt Manager for LLM-AutoDoc

Loads and manages prompts from prompts.yml configuration file.
Supports template variables and environment variable overrides.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.prompts')


class PromptManager:
    """
    Manages prompts for LLM-AutoDoc plugin.

    Features:
    - Load prompts from YAML configuration
    - Template variable substitution
    - Environment variable overrides
    - Caching for performance
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the PromptManager.

        Args:
            config_path: Path to prompts.yml file. If None, uses default location.
        """
        if config_path is None:
            # Default: prompts.yml in the same directory as this file
            this_dir = Path(__file__).parent.parent
            config_path = this_dir / 'prompts.yml'

        self.config_path = Path(config_path)
        self.prompts = {}
        self._load_prompts()

    def _load_prompts(self):
        """Load prompts from YAML configuration file"""
        try:
            if not self.config_path.exists():
                logger.error(f"Prompts config file not found: {self.config_path}")
                logger.warning("Using default hardcoded prompts")
                return

            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.prompts = yaml.safe_load(f)

            logger.info(f"✓ Loaded prompts from {self.config_path}")

            # Count prompts
            prompt_count = self._count_prompts(self.prompts)
            logger.info(f"  Loaded {prompt_count} prompt templates")

        except Exception as e:
            logger.error(f"Error loading prompts config: {e}")
            logger.warning("Using default hardcoded prompts")
            self.prompts = {}

    def _count_prompts(self, data: Dict, count: int = 0) -> int:
        """Recursively count prompts in nested dict"""
        for key, value in data.items():
            if isinstance(value, dict):
                count = self._count_prompts(value, count)
            elif isinstance(value, str) and len(value) > 50:  # Likely a prompt
                count += 1
        return count

    def get_prompt(self, category: str, name: str, **kwargs) -> str:
        """
        Get a prompt with template variable substitution.

        Args:
            category: Prompt category (e.g., 'overview', 'high_level')
            name: Prompt name (e.g., 'extraction', 'synthesis')
            **kwargs: Template variables to substitute

        Returns:
            Formatted prompt string

        Example:
            prompt = manager.get_prompt(
                'overview', 'extraction',
                topic_name='Threading',
                file_path='thread.cpp',
                content='...'
            )
        """
        # Check for environment variable override
        env_var = f"LLMAUTODOC_PROMPT_{category.upper()}_{name.upper()}"
        if env_var in os.environ:
            logger.debug(f"Using prompt override from {env_var}")
            template = os.environ[env_var]
        else:
            # Load from config
            if category not in self.prompts:
                logger.warning(f"Prompt category '{category}' not found in config")
                return self._get_default_prompt(category, name)

            if name not in self.prompts[category]:
                logger.warning(f"Prompt '{category}.{name}' not found in config")
                return self._get_default_prompt(category, name)

            template = self.prompts[category][name]

        # Substitute template variables
        try:
            # Clean up None values
            clean_kwargs = {k: (v if v is not None else '') for k, v in kwargs.items()}

            # Format the template
            prompt = template.format(**clean_kwargs)
            return prompt

        except KeyError as e:
            logger.error(f"Missing template variable in prompt '{category}.{name}': {e}")
            logger.error(f"Available variables: {list(kwargs.keys())}")
            # Return template with missing variables highlighted
            return template
        except Exception as e:
            logger.error(f"Error formatting prompt '{category}.{name}': {e}")
            return template

    def _get_default_prompt(self, category: str, name: str) -> str:
        """
        Fallback default prompts if config file is missing or incomplete.

        These are minimal prompts to ensure the plugin doesn't crash.
        """
        defaults = {
            'overview': {
                'extraction': 'Analyze this code and extract information relevant to: {topic_name}\n\nFile: {file_path}\nContent: {content}',
                'synthesis': 'Create documentation about: {topic_name}\n\nInformation: {combined_info}',
                'refinement': 'Refine this documentation:\n\n{content}',
            },
            'high_level': {
                'getting_started': 'Create a Getting Started guide for this project:\n\n{project_structure}',
                'architecture': 'Document the architecture of this project:\n\n{project_structure}',
            },
            'mid_level': {
                'module': 'Document this module: {module_name}\n\nFiles: {module_files}',
            },
            'detailed_level': {
                'class': 'Document this class: {class_name}\n\nCode: {class_code}',
                'functions': 'Document these functions:\n\n{functions_list}',
            },
            'cross_linker': {
                'linking': 'Suggest related documents for:\n\n{doc_content}\n\nCandidates: {candidates}',
            }
        }

        if category in defaults and name in defaults[category]:
            logger.warning(f"Using default prompt for '{category}.{name}'")
            return defaults[category][name]

        logger.error(f"No default prompt available for '{category}.{name}'")
        return "Error: Prompt not found. Please check prompts.yml configuration."

    def reload_prompts(self):
        """Reload prompts from configuration file"""
        logger.info("Reloading prompts configuration...")
        self._load_prompts()

    def list_prompts(self) -> Dict[str, list]:
        """
        List all available prompts by category.

        Returns:
            Dictionary mapping category -> list of prompt names
        """
        result = {}
        for category, prompts in self.prompts.items():
            if isinstance(prompts, dict):
                result[category] = list(prompts.keys())
        return result

    def validate_prompts(self) -> bool:
        """
        Validate that all expected prompts are present.

        Returns:
            True if all prompts are valid, False otherwise
        """
        expected_prompts = {
            'overview': ['extraction', 'extraction_hybrid', 'synthesis', 'refinement'],
            'high_level': ['getting_started', 'architecture'],
            'mid_level': ['module'],
            'detailed_level': ['class', 'functions'],
            'cross_linker': ['linking'],
        }

        all_valid = True

        for category, names in expected_prompts.items():
            if category not in self.prompts:
                logger.error(f"Missing prompt category: {category}")
                all_valid = False
                continue

            for name in names:
                if name not in self.prompts[category]:
                    logger.error(f"Missing prompt: {category}.{name}")
                    all_valid = False
                elif not isinstance(self.prompts[category][name], str):
                    logger.error(f"Invalid prompt type: {category}.{name}")
                    all_valid = False
                elif len(self.prompts[category][name]) < 50:
                    logger.warning(f"Suspiciously short prompt: {category}.{name}")

        if all_valid:
            logger.info("✓ All prompts validated successfully")
        else:
            logger.error("✗ Prompt validation failed")

        return all_valid


# Global singleton instance
_prompt_manager = None


def get_prompt_manager(config_path: Optional[str] = None) -> PromptManager:
    """
    Get the global PromptManager instance.

    Args:
        config_path: Path to prompts.yml (only used on first call)

    Returns:
        PromptManager instance
    """
    global _prompt_manager

    if _prompt_manager is None:
        _prompt_manager = PromptManager(config_path)

    return _prompt_manager

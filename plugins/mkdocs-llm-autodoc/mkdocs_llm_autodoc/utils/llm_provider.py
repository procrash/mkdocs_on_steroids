"""
LLM Provider abstraction

Supports multiple LLM providers:
- Anthropic (Claude)
- OpenAI (GPT-4)
- Ollama (local models)
- LM Studio (local OpenAI-compatible models)
"""

import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

logger = logging.getLogger('mkdocs.plugins.llm-autodoc.llm')


class LLMProvider(ABC):
    """Base class for LLM providers"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        pass


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""

    def __init__(self, api_key: str, model: str = 'claude-3-5-sonnet-20241022', timeout: float = 600.0):
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key, timeout=timeout)
            self.model = model
            logger.info(f"Initialized Anthropic provider with model: {model}, timeout: {timeout}s")
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

    def generate(self, prompt: str, max_tokens: int = 4000, **kwargs) -> str:
        """Generate documentation using Claude"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Error generating with Anthropic: {e}")
            raise


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""

    def __init__(self, api_key: str, model: str = 'gpt-4', base_url: Optional[str] = None, timeout: float = 600.0):
        try:
            import openai
            self.client = openai.OpenAI(
                api_key=api_key,
                base_url=base_url,
                timeout=timeout
            )
            self.model = model
            logger.info(f"Initialized OpenAI provider with model: {model}, base_url: {base_url}, timeout: {timeout}s")
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def generate(self, prompt: str, max_tokens: int = 4000, **kwargs) -> str:
        """Generate documentation using GPT"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical documentation expert specializing in C++ code documentation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating with OpenAI: {e}")
            raise


class OllamaProvider(LLMProvider):
    """Ollama local model provider"""

    def __init__(self, model: str = 'llama3', base_url: Optional[str] = None, timeout: float = 600.0):
        try:
            import openai  # Ollama uses OpenAI-compatible API
            self.client = openai.OpenAI(
                base_url=base_url or "http://localhost:11434/v1",
                api_key="ollama",  # Ollama doesn't need a real API key
                timeout=timeout
            )
            self.model = model
            logger.info(f"Initialized Ollama provider with model: {model}, timeout: {timeout}s")
        except ImportError:
            raise ImportError("openai package needed for Ollama. Run: pip install openai")

    def generate(self, prompt: str, max_tokens: int = 4000, **kwargs) -> str:
        """Generate documentation using Ollama"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical documentation expert specializing in C++ code documentation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating with Ollama: {e}")
            raise


class LMStudioProvider(LLMProvider):
    """LM Studio local model provider (OpenAI-compatible)"""

    def __init__(self, model: str = 'local-model', base_url: Optional[str] = None, api_key: Optional[str] = None, timeout: float = 600.0):
        try:
            import openai  # LM Studio uses OpenAI-compatible API
            # Use provided API key from config, or default to "lm-studio" if not specified
            effective_api_key = api_key if api_key is not None else "lm-studio"
            self.client = openai.OpenAI(
                base_url=base_url or "http://localhost:1234/v1",
                api_key=effective_api_key,
                timeout=timeout
            )
            self.model = model
            logger.info(f"Initialized LM Studio provider with model: {model} at {base_url or 'http://localhost:1234/v1'}, timeout: {timeout}s")
        except ImportError:
            raise ImportError("openai package needed for LM Studio. Run: pip install openai")

    def generate(self, prompt: str, max_tokens: int = 4000, **kwargs) -> str:
        """Generate documentation using LM Studio"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical documentation expert specializing in C++ code documentation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating with LM Studio: {e}")
            raise


class LLMProviderFactory:
    """Factory for creating LLM providers"""

    @staticmethod
    def create(provider: str, api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None, timeout: float = 600.0) -> LLMProvider:
        """
        Create an LLM provider instance.

        Args:
            provider: Provider name ('anthropic', 'openai', 'ollama', 'lmstudio')
            api_key: API key (required for Anthropic/OpenAI, optional for LM Studio, not needed for Ollama)
            model: Model name
            base_url: Base URL (for Ollama, LM Studio, or custom endpoints)
            timeout: Timeout in seconds (default: 600.0 = 10 minutes)

        Returns:
            LLMProvider instance
        """
        provider = provider.lower()

        if provider == 'anthropic':
            if not api_key:
                raise ValueError("API key required for Anthropic")
            return AnthropicProvider(
                api_key=api_key,
                model=model or 'claude-3-5-sonnet-20241022',
                timeout=timeout
            )

        elif provider == 'openai':
            if not api_key:
                raise ValueError("API key required for OpenAI")
            return OpenAIProvider(
                api_key=api_key,
                model=model or 'gpt-4',
                base_url=base_url,
                timeout=timeout
            )

        elif provider == 'ollama':
            return OllamaProvider(
                model=model or 'llama3',
                base_url=base_url,
                timeout=timeout
            )

        elif provider == 'lmstudio':
            return LMStudioProvider(
                model=model or 'local-model',
                base_url=base_url,
                api_key=api_key,
                timeout=timeout
            )

        else:
            raise ValueError(f"Unknown provider: {provider}. Supported: anthropic, openai, ollama, lmstudio")

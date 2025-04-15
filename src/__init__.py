"""
SmolaAgents package.

Exports core functionality for easy imports.
"""

# Import providers
from src.config import ConfigProvider
from src.llm import LLMProvider
from src.tools import ToolsProvider
from src.prompts.prompt_loader import PromptProvider
from src.memory import MemoryProvider
from src.sandbox import SandboxProvider

# Import ServiceLoader singleton
from src.loader import loader

__all__ = [
    # Providers
    "ConfigProvider",
    "LLMProvider",
    "ToolsProvider",
    "PromptProvider",
    "MemoryProvider",
    "SandboxProvider",
    
    # ServiceLoader singleton
    "loader",
]

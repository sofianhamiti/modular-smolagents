"""
LLM loader for smolagents using LiteLLM gateway.

Provides a function to load and configure the LLM for smolagents.
"""

from smolagents.models import OpenAIServerModel
from src.core.config_loader import ConfigLoader


def load_llm():
    """
    Load the LLM for smolagents from configuration.

    Returns:
        Configured OpenAIServerModel instance for litellm or openrouter provider.
    """
    config = ConfigLoader().get_llm_config()
    provider = config.get("provider").lower()
    api_key = config.get("api_key")
    api_base = config.get("api_base")
    model = config.get("model")
    temperature = config.get("temperature", 0.7)
    max_tokens = config.get("max_tokens", 128000)

    if not api_key or not model:
        raise ValueError("Missing required LLM configuration (api_key, model)")

    if provider in ["litellm", "openrouter"]:
        if not api_base:
            raise ValueError(
                f"Missing required LLM configuration (api_base) for {provider} provider"
            )
        return OpenAIServerModel(
            model_id=model,
            api_base=api_base,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    else:
        raise ValueError(
            f"Unsupported provider '{provider}'. Only 'litellm' and 'openrouter' are supported."
        )

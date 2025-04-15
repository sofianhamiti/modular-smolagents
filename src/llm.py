"""
LLM implementation for smolagents.
Provides the core functionality for interacting with language models.
"""

class LLMProvider:
    """
    Provider class for language model functionality.
    Handles access to LLM instances.
    """
    
    @staticmethod
    def get_llm(config):
        """
        Get an LLM instance based on the provided configuration.

        Args:
            config: Dictionary containing LLM configuration parameters

        Returns:
            Configured OpenAIServerModel instance for litellm or openrouter provider.
        """
        from smolagents.models import OpenAIServerModel
        
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

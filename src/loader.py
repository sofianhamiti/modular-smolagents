"""
Centralized loader for all components.
Provides singleton access to config, LLM, tools, prompts, memory, and sandbox.
"""

# Singleton instances
_config_instance = None
_llm_instance = None
_tools_instance = None
_prompts_instance = None
_sandbox_instance = None

# Config
def get_config():
    """
    Get the singleton config instance.
    
    Returns:
        The loaded configuration dictionary
    """
    global _config_instance
    if _config_instance is None:
        from src.config import ConfigLoader
        _config_instance = ConfigLoader().config
    return _config_instance

def get_llm_config():
    """Get LLM configuration section"""
    return get_config().get('llm', {})

def get_docker_config():
    """Get Docker configuration section"""
    return get_config().get('docker', {})

# LLM
def get_llm():
    """
    Load the LLM for smolagents from configuration.

    Returns:
        Configured OpenAIServerModel instance for litellm or openrouter provider.
    """
    global _llm_instance
    if _llm_instance is None:
        from src.llm import LLMProvider
        config = get_llm_config()
        _llm_instance = LLMProvider.create_llm(config)
    return _llm_instance

# Tools
def get_tools():
    """
    Instantiate and return all available tool classes from smolagents.default_tools and src.tools.

    Returns:
        List of tool instances.
    """
    global _tools_instance
    if _tools_instance is None:
        from src.tools import ToolsProvider
        _tools_instance = ToolsProvider.create_tools()
    return _tools_instance

# Prompts
def get_prompts():
    """
    Get the prompts loader instance.
    
    Returns:
        PromptLoader instance
    """
    global _prompts_instance
    if _prompts_instance is None:
        from src.prompts.prompt_loader import PromptLoader
        _prompts_instance = PromptLoader()
    return _prompts_instance

def get_prompt_templates():
    """
    Returns the full prompt_templates dictionary, matching smolagents' expectations.
    """
    return get_prompts().get_prompt_templates()

def get_prompt(*keys, default=""):
    """
    Retrieve a specific prompt by nested keys, e.g. get_prompt('planning', 'initial_plan').
    Returns default if not found.
    """
    return get_prompts().get_prompt(*keys, default=default)

# Memory
def get_memory():
    """
    Get the memory instance.
    
    Returns:
        Memory instance
    """
    from src.memory import memory
    return memory

def memory_search(query, user_id="default_user", limit=3):
    """
    Retrieve relevant memories for a given query and user.
    Returns a list of memory dicts.
    """
    from src.memory import MemoryProvider
    return MemoryProvider.search(get_memory(), query, user_id, limit)

def memory_add(messages, user_id="default_user"):
    """
    Add a list of messages (dicts with 'role' and 'content') to memory for a user.
    """
    from src.memory import MemoryProvider
    return MemoryProvider.add(get_memory(), messages, user_id)

# Sandbox
def get_sandbox():
    """
    Get the Docker sandbox instance.
    
    Returns:
        DockerSandbox instance
    """
    global _sandbox_instance
    if _sandbox_instance is None:
        from src.sandbox import SandboxProvider
        docker_config = get_docker_config()
        _sandbox_instance = SandboxProvider.create_sandbox(docker_config)
    return _sandbox_instance

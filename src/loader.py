"""
Centralized loader for all components.
Provides singleton access to config, LLM, tools, prompts, memory, and sandbox.
"""

# Import providers
from src.config import ConfigProvider
from src.llm import LLMProvider
from src.tools import ToolsProvider
from src.prompts.prompt_loader import PromptProvider
from src.memory import MemoryProvider
from src.sandbox import SandboxProvider

# Import typing modules
from typing import Dict, List, Any, Optional

# Define type variables for better type hinting
ConfigType = Dict[str, Any]  
LLMType = Any  
ToolType = Any  
PromptLoaderType = Any  
MemoryType = Any  
SandboxType = Any  

class ServiceLoader:
    """
    Centralized loader providing singleton access to application components.
    Uses lazy initialization.
    """
    _instance: Optional['ServiceLoader'] = None
    
    def __new__(cls) -> 'ServiceLoader':
        """
        Ensure only one instance of ServiceLoader exists.
        
        Returns:
            The singleton ServiceLoader instance
        """
        if cls._instance is None:
            cls._instance = super(ServiceLoader, cls).__new__(cls)
            cls._instance._config: Optional[ConfigType] = None
            cls._instance._llm: Optional[LLMType] = None
            cls._instance._tools: Optional[List[ToolType]] = None
            cls._instance._prompts: Optional[PromptLoaderType] = None
            cls._instance._memory: Optional[MemoryType] = None
            cls._instance._sandbox: Optional[SandboxType] = None
        return cls._instance
    
    @property
    def config(self) -> ConfigType:
        """
        Get the singleton config instance.
        
        Returns:
            The loaded configuration dictionary
            
        Raises:
            RuntimeError: If configuration could not be loaded
        """
        if self._config is None:
            config_loader = ConfigProvider.get_config_loader()
            self._config = ConfigProvider.get_config(config_loader)
            if self._config is None:
                raise RuntimeError("Failed to load configuration")
        return self._config
    
    @property
    def llm(self) -> LLMType:
        """
        Get the LLM instance for smolagents from configuration.

        Returns:
            Configured OpenAIServerModel instance for litellm or openrouter provider.
            
        Raises:
            RuntimeError: If LLM could not be initialized
        """
        if self._llm is None:
            config = self.config.get('llm', {})
            self._llm = LLMProvider.get_llm(config)
            if self._llm is None:
                raise RuntimeError("Failed to initialize LLM")
        return self._llm
    
    @property
    def tools(self) -> List[ToolType]:
        """
        Get all available tool instances from smolagents.default_tools and src.tools.

        Returns:
            List of tool instances.
        """
        if self._tools is None:
            self._tools = ToolsProvider.get_tools()
            if self._tools is None:
                # For tools, an empty list might be valid, so we'll initialize it
                self._tools = []
        return self._tools
    
    @property
    def prompts(self) -> PromptLoaderType:
        """
        Get the prompts instance with access to prompt templates.
        
        Returns:
            PromptLoader instance
            
        Raises:
            RuntimeError: If prompts could not be initialized
        """
        if self._prompts is None:
            self._prompts = PromptProvider.get_prompts()
            if self._prompts is None:
                raise RuntimeError("Failed to initialize prompt loader")
        return self._prompts
    
    @property
    def memory(self) -> MemoryType:
        """
        Get the memory instance.
        
        Returns:
            Memory instance
            
        Raises:
            RuntimeError: If memory could not be initialized
        """
        if self._memory is None:
            self._memory = MemoryProvider.get_memory()
            if self._memory is None:
                raise RuntimeError("Failed to initialize memory")
        return self._memory
    
    @property
    def sandbox(self) -> SandboxType:
        """
        Get the Docker sandbox instance.
        
        Returns:
            DockerSandbox instance
            
        Raises:
            RuntimeError: If sandbox could not be initialized
        """
        if self._sandbox is None:
            docker_config = self.config.get('docker', {})
            self._sandbox = SandboxProvider.get_sandbox(docker_config)
            if self._sandbox is None:
                raise RuntimeError("Failed to initialize Docker sandbox")
        return self._sandbox

# Create a singleton instance for easy import
loader = ServiceLoader()

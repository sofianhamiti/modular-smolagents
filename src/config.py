import os
import yaml
import re
from typing import Dict, Any

class ConfigProvider:
    """
    Provider class for configuration functionality.
    Handles creation and access to configuration instances.
    """
    
    @staticmethod
    def create_config_loader(config_path: str = None):
        """
        Create a configuration loader instance.
        
        Args:
            config_path: Optional path to the config YAML file
            
        Returns:
            ConfigLoader instance
        """
        return ConfigLoader(config_path)
    
    @staticmethod
    def get_config(config_loader):
        """
        Get the configuration dictionary from a config loader.
        
        Args:
            config_loader: ConfigLoader instance
            
        Returns:
            Dictionary containing configuration
        """
        return config_loader.config


def resolve_env_vars(value):
    """
    If value is a string of the form '${ENV_VAR}', replace with the environment variable.
    Otherwise, return the value unchanged.
    """
    if isinstance(value, str):
        match = re.match(r"\$\{(\w+)\}", value)
        if match:
            return os.environ.get(match.group(1), "")
    return value

def resolve_env_in_dict(d):
    """
    Recursively resolve environment variables in a dictionary.
    """
    if isinstance(d, dict):
        return {k: resolve_env_in_dict(resolve_env_vars(v)) for k, v in d.items()}
    elif isinstance(d, list):
        return [resolve_env_in_dict(resolve_env_vars(i)) for i in d]
    else:
        return resolve_env_vars(d)

class ConfigLoader:
    """
    Configuration loader for the AI agent system.
    Loads configuration from a YAML file.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to the config file. Defaults to 'config/config.yaml'
        """
        if config_path is None:
            # Get the project root directory (assuming this file is in src/)
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(project_root, 'config', 'config.yaml')
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load the configuration from the YAML file.
        
        Returns:
            Dictionary containing configuration
        """
        try:
            with open(self.config_path, 'r') as file:
                raw_config = yaml.safe_load(file)
                return resolve_env_in_dict(raw_config)
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from {self.config_path}: {str(e)}")
    
    def get_llm_config(self) -> Dict[str, Any]:
        """
        Get the LLM configuration.
        
        Returns:
            Dictionary containing LLM configuration
        """
        return self.config.get('llm', {})
    
    def get_tools_config(self) -> Dict[str, Any]:
        """
        Get the tools configuration.
        
        Returns:
            Dictionary containing tools configuration
        """
        return self.config.get('tools', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get the logging configuration.
        
        Returns:
            Dictionary containing logging configuration
        """
        return self.config.get('logging', {})

import os
import yaml
from typing import Dict, Any, Optional


class PromptLoader:
    """
    Loads prompt templates from a YAML file for use with smolagents.
    """

    def __init__(self, prompts_path: Optional[str] = None):
        if prompts_path is None:
            # Get the project root directory (assuming this file is in src/core)
            project_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            prompts_path = os.path.join(project_root, "src", "prompts", "prompts.yaml")
        self.prompts_path = prompts_path
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, Any]:
        try:
            with open(self.prompts_path, "r") as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load prompts from {self.prompts_path}: {str(e)}"
            )

    def get_prompt_templates(self) -> Dict[str, Any]:
        """
        Returns the full prompt_templates dictionary, matching smolagents' expectations.
        """
        return self.prompts

    def get_prompt(self, *keys, default: str = "") -> str:
        """
        Retrieve a specific prompt by nested keys, e.g. get_prompt('planning', 'initial_plan').
        Returns default if not found.
        """
        d = self.prompts
        for key in keys:
            if isinstance(d, dict) and key in d:
                d = d[key]
            else:
                return default
        return d if isinstance(d, str) else default

"""
Prompt loading and management.
"""

import os
import yaml

_prompts_cache = None

def load_prompts():
    """Load prompts from YAML file"""
    global _prompts_cache
    if _prompts_cache is None:
        prompts_path = os.path.join(os.path.dirname(__file__), "prompts.yaml")
        with open(prompts_path, "r") as file:
            _prompts_cache = yaml.safe_load(file)
    return _prompts_cache

def get_prompt(*keys, default=""):
    """Get a specific prompt by nested keys"""
    d = load_prompts()
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d if isinstance(d, str) else default

__all__ = ["load_prompts", "get_prompt"]

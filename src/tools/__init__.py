"""
Tools package for agent use.

Exports all available tools for use by agents.
"""

from .file_tools import (
    ReadFileTool,
    SearchFilesTool,
    ListFilesTool,
    ReplaceInFileTool,
    WriteToFileTool,
)

__all__ = [
    "ReadFileTool",
    "SearchFilesTool",
    "ListFilesTool",
    "ReplaceInFileTool",
    "WriteToFileTool",
    "ToolsProvider",
]


class ToolsProvider:
    """
    Provider class for tools functionality.
    Handles creation and configuration of tool instances.
    """
    
    @staticmethod
    def create_tools():
        """
        Create and return all available tool instances.
        
        Returns:
            List of tool instances
        """
        from smolagents.default_tools import (
            PythonInterpreterTool,
            FinalAnswerTool,
            UserInputTool,
            DuckDuckGoSearchTool,
            VisitWebpageTool,
        )
        from .code_tools import ListCodeDefinitionNamesTool
        from .cli_tools import ExecuteCommandTool
        
        return [
            PythonInterpreterTool(),
            FinalAnswerTool(),
            UserInputTool(),
            DuckDuckGoSearchTool(),
            VisitWebpageTool(),
            ReadFileTool(),
            SearchFilesTool(),
            ListFilesTool(),
            ExecuteCommandTool(),
            ListCodeDefinitionNamesTool(),
        ]

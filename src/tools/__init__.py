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
from .agent_tools import (
    MemorySearchTool,
    MemoryAddTool,
    RunCodeAgentTool,
)


class ToolsProvider:
    """
    Provider class for tools functionality.
    Handles access and configuration of tool instances.
    """
    
    @staticmethod
    def get_tools():
        """
        Get all available tool instances.
        
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
        # from .agent_tools import MemorySearchTool, MemoryAddTool, RunCodeAgentTool
        
        return [
            PythonInterpreterTool(),
            FinalAnswerTool(),
            UserInputTool(),
            DuckDuckGoSearchTool(),
            VisitWebpageTool(),
            ReadFileTool(),
            SearchFilesTool(),
            ListFilesTool(),
            ReplaceInFileTool(),
            WriteToFileTool(),
            ExecuteCommandTool(),
            ListCodeDefinitionNamesTool(),
            # MemorySearchTool(),
            # MemoryAddTool(),
            # RunCodeAgentTool(),
        ]

"""
Tool loader for agent tools.

Provides a function to instantiate all available tools.
"""

from smolagents.default_tools import (
    PythonInterpreterTool,
    FinalAnswerTool,
    UserInputTool,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
)

from src.tools import (
    ReadFileTool,
    SearchFilesTool,
    ListFilesTool,
    ReplaceInFileTool,
    WriteToFileTool,
)
from src.tools.code_tools import ListCodeDefinitionNamesTool
from src.tools.cli_tools import ExecuteCommandTool


def load_tools():
    """
    Instantiate and return all available tool classes from smolagents.default_tools and src.tools.

    Returns:
        List of tool instances.
    """
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
        # WriteToFileTool(),
        # ExecuteCommandTool(),
        ListCodeDefinitionNamesTool(),
    ]

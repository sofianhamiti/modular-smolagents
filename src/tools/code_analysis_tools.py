from smolagents.default_tools import Tool
import os
import ast
from typing import List


class ListCodeDefinitionNamesTool(Tool):
    name = "list_code_definition_names"
    description = (
        "Lists all top-level function and class names in Python files at the given path. "
        "Input: path (string, required) - file or directory to analyze. "
        "Input: language (string, optional, default 'python') - programming language (only 'python' is supported). "
        "Output: list of strings, each describing a function or class (e.g., 'function: foo', 'class: Bar'), or an error message if the path is invalid or not a Python file. "
        "Edge cases: If the path is not a file or directory, or if no code definitions are found, returns an appropriate message. Only Python files (.py) are supported. "
        "Example: list_code_definition_names(path='src/') -> ['function: foo', 'class: Bar', ...]"
    )
    inputs = {
        "path": {
            "type": "string",
            "description": "Absolute or relative path to a Python file or directory to analyze. Must exist.",
        },
        "language": {
            "type": "string",
            "description": "Programming language (default: 'python'). Only 'python' is supported.",
            "nullable": True,
            "default": "python",
        },
    }
    output_type = "any"

    def forward(self, path: str, language: str = "python") -> List[str]:
        print(
            f"[ListCodeDefinitionNamesTool] Called with path={path}, language={language}"
        )
        if language != "python":
            error_msg = "Error: Only Python is supported currently."
            print(f"[ListCodeDefinitionNamesTool] {error_msg}")
            return [error_msg]
        def_names = []

        def extract_defs(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=file_path)
                for node in ast.iter_child_nodes(tree):
                    if isinstance(node, ast.FunctionDef):
                        def_names.append(f"function: {node.name}")
                    elif isinstance(node, ast.ClassDef):
                        def_names.append(f"class: {node.name}")
            except Exception as e:
                error_msg = f"{file_path}: Error parsing file: {str(e)}"
                print(f"[ListCodeDefinitionNamesTool] {error_msg}")
                def_names.append(error_msg)

        if os.path.isfile(path):
            if path.endswith(".py"):
                extract_defs(path)
            else:
                error_msg = f"Error: '{path}' is not a Python (.py) file."
                print(f"[ListCodeDefinitionNamesTool] {error_msg}")
                return [error_msg]
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        extract_defs(os.path.join(root, file))
        else:
            error_msg = f"Error: '{path}' is not a valid file or directory."
            print(f"[ListCodeDefinitionNamesTool] {error_msg}")
            return [error_msg]
        if def_names:
            print(
                f"[ListCodeDefinitionNamesTool] Found {len(def_names)} code definitions."
            )
            return def_names
        else:
            msg = "No code definitions found."
            print(f"[ListCodeDefinitionNamesTool] {msg}")
            return [msg]

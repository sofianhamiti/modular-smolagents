from smolagents.default_tools import Tool
import os
import fnmatch
import re
from typing import List


class ReadFileTool(Tool):
    name = "read_file"
    description = (
        "Reads the entire contents of a text file and returns it as a string. "
        "Input: file_path (string, required) - absolute or relative path to the file. "
        "Input: encoding (string, optional, default 'utf-8') - text encoding to use. "
        "Output: string containing the file's contents, or an error message if the file does not exist, is not readable, or cannot be decoded. "
        "Edge cases: If the file does not exist, returns an error message. If the file is binary or too large, may return unreadable output or fail. "
        "Example: read_file(file_path='notes.txt') -> 'Meeting notes: ...'"
    )
    inputs = {
        "file_path": {
            "type": "string",
            "description": "Absolute or relative path to the file to read. Must exist and be readable.",
        },
        "encoding": {
            "type": "string",
            "description": "Text encoding to use (e.g., 'utf-8', 'latin-1'). Default is 'utf-8'.",
            "nullable": True,
            "default": "utf-8",
        },
    }
    output_type = "string"

    def forward(self, file_path: str, encoding: str = "utf-8") -> str:
        print(f"[ReadFileTool] Called with file_path={file_path}, encoding={encoding}")
        try:
            if not os.path.exists(file_path):
                error_msg = f"Error: File '{file_path}' does not exist."
                print(f"[ReadFileTool] {error_msg}")
                return error_msg
            with open(file_path, "r", encoding=encoding) as f:
                content = f.read()
            print(f"[ReadFileTool] Successfully read file '{file_path}'")
            return content
        except PermissionError:
            error_msg = f"Error: Permission denied for '{file_path}'."
            print(f"[ReadFileTool] {error_msg}")
            return error_msg
        except UnicodeDecodeError:
            error_msg = (
                f"Error: Could not decode '{file_path}' with encoding '{encoding}'."
            )
            print(f"[ReadFileTool] {error_msg}")
            return error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"[ReadFileTool] {error_msg}")
            return error_msg


class WriteToFileTool(Tool):
    name = "write_to_file"
    description = (
        "Creates or overwrites a text file with the provided content. "
        "Input: file_path (string, required) - absolute or relative path to the file to write. "
        "Input: content (string, required) - content to write to the file. "
        "Input: encoding (string, optional, default 'utf-8') - text encoding to use. "
        "Output: string message indicating success or error. "
        "Edge cases: If the directory does not exist, it will be created. If the file cannot be written, returns an error message. "
        "Example: write_to_file(file_path='output.txt', content='Hello!') -> 'File output.txt written successfully.'"
    )
    inputs = {
        "file_path": {
            "type": "string",
            "description": "Absolute or relative path to the file to write. Parent directories will be created if needed.",
        },
        "content": {"type": "string", "description": "Content to write to the file."},
        "encoding": {
            "type": "string",
            "description": "Text encoding to use (e.g., 'utf-8', 'latin-1'). Default is 'utf-8'.",
            "nullable": True,
            "default": "utf-8",
        },
    }
    output_type = "string"

    def forward(self, file_path: str, content: str, encoding: str = "utf-8") -> str:
        print(
            f"[WriteToFileTool] Called with file_path={file_path}, encoding={encoding}"
        )
        try:
            os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
            with open(file_path, "w", encoding=encoding) as f:
                f.write(content)
            msg = f"File '{file_path}' written successfully."
            print(f"[WriteToFileTool] {msg}")
            return msg
        except Exception as e:
            error_msg = f"Error writing file: {str(e)}"
            print(f"[WriteToFileTool] {error_msg}")
            return error_msg


class ReplaceInFileTool(Tool):
    name = "replace_in_file"
    description = (
        "Replaces occurrences of a search string or regex pattern within a text file. "
        "Input: file_path (string, required) - path to the file to edit. "
        "Input: search (string, required) - text or regex pattern to search for. "
        "Input: replace (string, required) - replacement text. "
        "Input: count (integer, optional, default 1; -1 for all) - number of occurrences to replace. "
        "Input: use_regex (boolean, optional, default False) - interpret search as regex. "
        "Output: string message indicating how many replacements were made, or an error message. "
        "Edge cases: If no matches are found, returns a message. If the file does not exist or cannot be edited, returns an error. "
        "Example: replace_in_file(file_path='script.py', search='foo', replace='bar', count=-1) -> 'Replaced 3 occurrence(s) in script.py.'"
    )
    inputs = {
        "file_path": {
            "type": "string",
            "description": "Absolute or relative path to the file to edit. Must exist and be writable.",
        },
        "search": {
            "type": "string",
            "description": "Text or regex pattern to search for in the file.",
        },
        "replace": {"type": "string", "description": "Replacement text."},
        "count": {
            "type": "integer",
            "description": "Number of occurrences to replace (default: 1, -1 for all).",
            "nullable": True,
            "default": 1,
        },
        "use_regex": {
            "type": "boolean",
            "description": "Interpret search as regex (default: False).",
            "nullable": True,
            "default": False,
        },
    }
    output_type = "string"

    def forward(
        self,
        file_path: str,
        search: str,
        replace: str,
        count: int = 1,
        use_regex: bool = False,
    ) -> str:
        print(
            f"[ReplaceInFileTool] Called with file_path={file_path}, search={search}, replace={replace}, count={count}, use_regex={use_regex}"
        )
        if not os.path.exists(file_path):
            error_msg = f"Error: File '{file_path}' does not exist."
            print(f"[ReplaceInFileTool] {error_msg}")
            return error_msg
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if use_regex:
                new_content, n = re.subn(
                    search, replace, content, count=0 if count == -1 else count
                )
            else:
                n = (
                    content.count(search)
                    if count == -1
                    else min(content.count(search), count)
                )
                new_content = content.replace(
                    search, replace, count if count != -1 else content.count(search)
                )
            if n == 0:
                msg = "No matches found to replace."
                print(f"[ReplaceInFileTool] {msg}")
                return msg
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            msg = f"Replaced {n} occurrence(s) in '{file_path}'."
            print(f"[ReplaceInFileTool] {msg}")
            return msg
        except Exception as e:
            error_msg = f"Error editing file: {str(e)}"
            print(f"[ReplaceInFileTool] {error_msg}")
            return error_msg


class SearchFilesTool(Tool):
    name = "search_files"
    description = (
        "Searches for files in a directory whose names match a regex pattern. "
        "Input: directory (string, required) - directory to search in. "
        "Input: regex_pattern (string, required) - regex pattern to match filenames. "
        "Input: case_sensitive (boolean, optional, default False) - case-sensitive matching. "
        "Input: absolute_path (boolean, optional, default True) - return absolute paths. "
        "Output: list of matching file paths, or a message if no files matched or directory is invalid. "
        "Edge cases: If the directory does not exist, returns an error. If no files match, returns a message. "
        "Example: search_files(directory='src', regex_pattern='.*\\.py$') -> ['/project/src/a.py', ...]"
    )
    inputs = {
        "directory": {
            "type": "string",
            "description": "Absolute or relative path to the directory to search in. Must exist.",
        },
        "regex_pattern": {
            "type": "string",
            "description": "Regex pattern to match filenames (e.g., '.*\\.py$' for Python files).",
        },
        "case_sensitive": {
            "type": "boolean",
            "description": "Case-sensitive matching (default: False).",
            "nullable": True,
            "default": False,
        },
        "absolute_path": {
            "type": "boolean",
            "description": "Return absolute paths (default: True).",
            "nullable": True,
            "default": True,
        },
    }
    output_type = "any"

    def forward(
        self,
        directory: str,
        regex_pattern: str,
        case_sensitive: bool = False,
        absolute_path: bool = True,
    ) -> List[str]:
        print(
            f"[SearchFilesTool] Called with directory={directory}, regex_pattern={regex_pattern}, case_sensitive={case_sensitive}, absolute_path={absolute_path}"
        )
        if not os.path.isdir(directory):
            error_msg = f"Error: '{directory}' is not a valid directory."
            print(f"[SearchFilesTool] {error_msg}")
            return [error_msg]
        flags = re.IGNORECASE if not case_sensitive else 0
        pattern = re.compile(regex_pattern, flags)
        matches = []
        for root, _, files in os.walk(directory):
            for file in files:
                if pattern.match(file):
                    path = os.path.join(root, file)
                    matches.append(os.path.abspath(path) if absolute_path else path)
        if matches:
            print(f"[SearchFilesTool] Found {len(matches)} matching files.")
            return matches
        else:
            msg = "No files matched the pattern."
            print(f"[SearchFilesTool] {msg}")
            return [msg]


class ListFilesTool(Tool):
    name = "list_files"
    description = (
        "Lists all files and/or directories in the specified path. "
        "Input: directory (string, required) - path to list. "
        "Input: recursive (boolean, optional, default False) - list recursively. "
        "Input: exclude_dirs (boolean, optional, default False) - exclude directories from output. "
        "Output: list of file and/or directory names or paths, or an error message if the path does not exist. "
        "Edge cases: If the directory does not exist, returns an error. "
        "Example: list_files(directory='src', recursive=True) -> ['src/a.py', 'src/b.py', ...]"
    )
    inputs = {
        "directory": {
            "type": "string",
            "description": "Absolute or relative path to the directory to list. Must exist.",
        },
        "recursive": {
            "type": "boolean",
            "description": "List recursively (default: False).",
            "nullable": True,
            "default": False,
        },
        "exclude_dirs": {
            "type": "boolean",
            "description": "Exclude directories from output (default: False).",
            "nullable": True,
            "default": False,
        },
    }
    output_type = "any"

    def forward(
        self, directory: str, recursive: bool = False, exclude_dirs: bool = False
    ) -> List[str]:
        print(
            f"[ListFilesTool] Called with directory={directory}, recursive={recursive}, exclude_dirs={exclude_dirs}"
        )
        if not os.path.exists(directory):
            error_msg = f"Error: '{directory}' does not exist."
            print(f"[ListFilesTool] {error_msg}")
            return [error_msg]
        if not recursive:
            entries = os.listdir(directory)
            if exclude_dirs:
                result = [
                    entry
                    for entry in entries
                    if os.path.isfile(os.path.join(directory, entry))
                ]
                print(
                    f"[ListFilesTool] Found {len(result)} files (excluding directories)."
                )
                return result
            print(f"[ListFilesTool] Found {len(entries)} entries.")
            return entries
        else:
            file_list = []
            for root, dirs, files in os.walk(directory):
                if exclude_dirs:
                    file_list.extend([os.path.join(root, file) for file in files])
                else:
                    file_list.extend(
                        [os.path.join(root, entry) for entry in (dirs + files)]
                    )
            print(f"[ListFilesTool] Found {len(file_list)} entries (recursive).")
            return file_list

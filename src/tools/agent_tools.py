from smolagents.default_tools import Tool
from smolagents import CodeAgent
# from src.core.memory import memory_search, memory_add


class MemorySearchTool(Tool):
    name = "memory_search"
    description = (
        "Searches the agent's memory for relevant entries given a query. "
        "Inputs: query (string), user_id (string, optional), limit (int, optional). "
        "Returns a list of memory dicts."
    )
    inputs = {
        "query": {
            "type": "string",
            "description": "Query to search for relevant memories.",
        },
        "user_id": {
            "type": "string",
            "description": "User/session identifier.",
            "default": "default_user",
            "nullable": True,
        },
        "limit": {
            "type": "integer",
            "description": "Maximum number of memories to retrieve.",
            "default": 3,
            "nullable": True,
        },
    }
    output_type = "list"

    def forward(self, query, user_id="default_user", limit=3):
        return memory_search(query, user_id, limit)


class MemoryAddTool(Tool):
    name = "memory_add"
    description = (
        "Adds messages to the agent's memory. "
        "Inputs: messages (list of dicts with 'role' and 'content'), user_id (string, optional). "
        "Returns the result of the add operation."
    )
    inputs = {
        "messages": {
            "type": "array",
            "description": "List of messages (dicts with 'role' and 'content').",
        },
        "user_id": {
            "type": "string",
            "description": "User/session identifier.",
            "default": "default_user",
            "nullable": True,
        },
    }
    output_type = "any"

    def forward(self, messages, user_id="default_user"):
        return memory_add(messages, user_id)


class RunCodeAgentTool(Tool):
    name = "run_code_agent"
    description = (
        "Instantiates and runs a CodeAgent on a given task. "
        "Inputs: task (string), tools (list of Tool, optional), model (callable), plus any other CodeAgent config as kwargs. "
        "Returns the result of agent.run(task)."
    )
    inputs = {
        "task": {
            "type": "string",
            "description": "Task for the agent to solve.",
        },
        "tools": {
            "type": "array",
            "description": "List of Tool instances.",
            "nullable": True,
            "default": [],
        },
        "model": {
            "type": "callable",
            "description": "Callable model for the agent.",
        },
        # Additional kwargs can be passed for CodeAgent config
    }
    output_type = "any"

    def forward(self, task, tools=None, model=None, **kwargs):
        tools = tools or []
        agent = CodeAgent(tools=tools, model=model, **kwargs)
        return agent.run(task)

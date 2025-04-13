from smolagents.default_tools import Tool
from smolagents import CodeAgent


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
            "type": "list",
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

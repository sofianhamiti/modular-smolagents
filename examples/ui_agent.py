import sys
from smolagents import CodeAgent
from smolagents.gradio_ui import GradioUI
from src.core.llm_loader import load_llm
from src.tools.tool_loader import load_tools


def main():
    model = load_llm()
    tools = load_tools()

    agent = CodeAgent(
        tools=tools, model=model, executor_type="local", planning_interval=3
    )
    gradio_ui = GradioUI(agent)
    gradio_ui.launch()


if __name__ == "__main__":
    main()

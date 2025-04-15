import sys
from smolagents import CodeAgent
from smolagents.gradio_ui import GradioUI
from src import get_llm, get_tools, get_docker_config, get_prompt_templates


def main():
    model = get_llm()
    tools = get_tools()
    docker_config = get_docker_config()

    agent = CodeAgent(
        tools=tools,
        model=model,
        # prompt_templates=get_prompt_templates(),
        executor_type="local",
        planning_interval=3,
        max_steps=20,
        additional_authorized_imports=["*"],
    )

    gradio_ui = GradioUI(agent)
    gradio_ui.launch(
        server_name="0.0.0.0", server_port=docker_config.get("port"), share=False
    )


if __name__ == "__main__":
    main()

import sys
from smolagents import CodeAgent
from smolagents.gradio_ui import GradioUI
from src import loader


def main():
    model = loader.llm
    tools = loader.tools
    config = loader.config
    use_prompts_yaml = config["agent"]["use_prompts_yaml"]
    prompt_templates = None
    if use_prompts_yaml:
        prompt_templates = loader.prompts
    docker_config = config["docker"]

    agent = CodeAgent(
        tools=tools,
        model=model,
        # prompt_templates=None,  # Removed get_prompt_templates() call
        executor_type="local",
        planning_interval=3,
        max_steps=20,
        additional_authorized_imports=["*"],
    )

    gradio_ui = GradioUI(agent)
    gradio_ui.launch(
        server_name="0.0.0.0", server_port=docker_config["port"], share=False
    )


if __name__ == "__main__":
    main()

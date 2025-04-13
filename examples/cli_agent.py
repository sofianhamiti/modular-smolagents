from smolagents import CodeAgent
from src.core.llm_loader import load_llm
from src.tools.tool_loader import load_tools
from src.core.config_loader import ConfigLoader
from smolagents.monitoring import LogLevel


def main():
    model = load_llm()
    tools = load_tools()
    config_loader = ConfigLoader()
    use_prompts_yaml = config_loader.config.get("use_prompts_yaml", False)
    prompt_templates = None
    if use_prompts_yaml:
        from src.core.prompt_loader import PromptLoader

        prompt_loader = PromptLoader()
        prompt_templates = prompt_loader.get_prompt_templates()

    agent = CodeAgent(
        tools=tools,
        model=model,
        prompt_templates=prompt_templates,
        executor_type="local",
        planning_interval=6,
        max_steps=50,
        verbosity_level=LogLevel.INFO,
        additional_authorized_imports=["*"],
    )

    print("Type your message (or 'exit' to quit):")
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting agent session.")
            break
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Exiting agent session.")
            break
        result = agent.run(user_input)
        print("Agent result:", result)


if __name__ == "__main__":
    main()

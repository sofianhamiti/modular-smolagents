from smolagents import CodeAgent
from src import loader
from smolagents.monitoring import LogLevel


def main():
    model = loader.llm
    tools = loader.tools
    config = loader.config
    # use_prompts_yaml = config.get("use_prompts_yaml", False)
    # prompt_templates = None
    # if use_prompts_yaml:
    #     prompt_templates = loader.prompts

    agent = CodeAgent(
        tools=tools,
        model=model,
        # prompt_templates=prompt_templates,
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

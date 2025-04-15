from smolagents import CodeAgent
from src import loader
from smolagents.monitoring import LogLevel


def main():
    model = loader.llm
    tools = loader.tools
    config = loader.config
    # Get agent configuration with empty dict as fallback
    agent_config = config.get("agent", {})
    
    # Extract values with defaults
    use_prompts_yaml = agent_config.get("use_prompts_yaml", False)
    planning_interval = agent_config.get("planning_interval", 5)
    max_steps = agent_config.get("max_steps", 50)
    additional_authorized_imports = agent_config.get("additional_authorized_imports", ["*"])
    
    prompt_templates = None
    if use_prompts_yaml:
        prompt_templates = loader.prompts

    agent = CodeAgent(
        tools=tools,
        model=model,
        # prompt_templates=prompt_templates,
        executor_type="local",
        planning_interval=planning_interval,
        max_steps=max_steps,
        verbosity_level=LogLevel.INFO,
        additional_authorized_imports=additional_authorized_imports,
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

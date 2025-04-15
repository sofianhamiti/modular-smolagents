from smolagents import CodeAgent


class AugmentedCodeAgent(CodeAgent):
    def __init__(self, *args, memory_search_fn=None, memory_add_fn=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory_search_fn = memory_search_fn
        self.memory_add_fn = memory_add_fn

    def build_prompt(self, user_message, user_id="default_user"):
        # Retrieve relevant memories
        memories = []
        if self.memory_search_fn:
            memories = self.memory_search_fn(user_message, user_id)
        memories_str = "\n".join(f"- {entry['memory']}" for entry in memories)
        # Compose prompt with memories
        system_prompt = (
            "You are a helpful AI. Use the following user memories to inform your answer.\n"
            f"User Memories:\n{memories_str}\n"
        )
        # Compose the rest of the prompt as usual
        # This assumes the base class uses a similar prompt structure
        base_prompt = (
            super().build_prompt(user_message, user_id)
            if hasattr(super(), "build_prompt")
            else []
        )
        # Prepend the system prompt with memories
        if (
            base_prompt
            and isinstance(base_prompt, list)
            and base_prompt[0].get("role") == "system"
        ):
            base_prompt[0]["content"] = system_prompt + base_prompt[0]["content"]
            return base_prompt
        else:
            return [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ]

    def after_turn(self, user_message, assistant_response, user_id="default_user"):
        if self.memory_add_fn:
            messages = [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_response},
            ]
            self.memory_add_fn(messages, user_id)

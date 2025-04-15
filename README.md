# SmolaAgents Examples

A collection of examples and utilities for building AI agents with [smolagents](https://github.com/huggingface/smolagents). This project demonstrates how to create, configure, and deploy autonomous AI agents for various tasks.

---

## 🚀 Step-by-Step Tutorial

### 1. **Clone the Repository**

```bash
git clone https://github.com/sofianhamiti/modular-smolagents.git
cd modular-smolagents
```

### 2. **Set Up a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Configure the System**

- Copy the example config file and edit it:
  ```bash
  cp config/config.example.yaml config/config.yaml
  ```
- Edit `config/config.yaml` to set your LLM provider, API key, and other settings.
- Example LLM config:
  ```yaml
  llm:
    provider: "litellm"
    api_base: "http://localhost:4000"
    api_key: "${LITELLM_API_KEY}"
    model: "claude-3-5-sonnet-20241022-v2:0"
    temperature: 0.7
    max_tokens: 8000
  ```
- Example Docker config:
  ```yaml
  docker:
    image_name: "sandbox-image"
    dockerfile_path: "."
    port: 8888
    agent_script: "examples/cli_agent.py"
    force_rebuild: false
  ```

### 5. **Run the CLI Agent**

```bash
python examples/cli_agent.py
```

### 6. **Run the UI Agent**

```bash
python examples/ui_agent.py
```

### 7. **Run in Docker**

```bash
python main.py
```

---

## 🧩 Architecture Overview

The project uses a modular, flat architecture for easy maintenance and extension:

- **Centralized Loader System**: All components are accessed through getter functions in `src/loader.py`
- **Configuration**: Loaded from YAML files with environment variable support
- **Memory**: Vector-based memory for persistent agent knowledge
- **Tools**: Extensible tool system for agent capabilities
- **Sandbox**: Docker-based sandbox for secure agent execution
- **Prompts**: YAML-based prompt templates for agent behavior

```
src/
├── __init__.py      # Exports all loader functions
├── agents.py        # Agent implementations
├── config.py        # Configuration loading
├── loader.py        # Centralized component loader
├── memory.py        # Memory management
├── sandbox.py       # Docker sandbox
├── prompts/         # Prompt templates
└── tools/           # Tool implementations
```

---

## 🛠️ Adding or Customizing Tools

1. **Create your tool** in `src/tools/` as a class inheriting from the appropriate base tool class.
2. **Add your tool** to the `get_tools()` function in `src/loader.py`.
3. **Restart the app** to use your new tool.

Example:

```python
# In src/tools/my_custom_tool.py
from smolagents.tools import Tool

class MyCustomTool(Tool):
    name = "my_custom_tool"
    description = "Description of what my tool does"
    
    def _run(self, param1, param2):
        # Tool implementation
        return result

# In src/loader.py (add to get_tools function)
from src.tools.my_custom_tool import MyCustomTool

def get_tools():
    # ...existing code...
    _tools_instance = [
        # ...existing tools...
        MyCustomTool(),
    ]
    return _tools_instance
```

---

## 🐳 Docker Support

The project includes Docker support for running agents in an isolated environment:

```bash
# Run the default agent in Docker
python main.py

# Or build and run manually
docker build -t sandbox-image .
docker run -it --rm -v $(pwd):/app:ro -v $(pwd)/data:/data -p 8888:8888 -w /app sandbox-image python examples/cli_agent.py
```

---

## 📚 Example Session

```
Type your message (or 'exit' to quit):
> What are the latest advancements in quantum computing?

[Agent processes the query using enabled tools]

Agent result: [Comprehensive answer about quantum computing advancements]
```

---

## License

MIT License - see LICENSE file for details.

---

## Acknowledgments

- Built with [smolagents](https://github.com/huggingface/smolagents)
- Powered by your choice of LLM via LiteLLM or OpenRouter

# Agentic AI Project

A research assistant system built with [smolagents](https://github.com/huggingface/smolagents) that demonstrates autonomous AI agents working together to solve complex tasks. The system uses a supervisor-worker pattern where specialized agents collaborate to research topics and provide comprehensive answers to user queries.

---

## 🚀 Step-by-Step Tutorial

### 1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/agentic-ai-project.git
cd agentic-ai-project
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

### 4. **Configure Environment Variables**

- Copy the example environment file and edit it:
  ```bash
  cp .env.example .env
  ```
- Open `.env` and set your LiteLLM API key and any other secrets.

### 5. **Configure the System**

- Edit `config/config.yaml` to set your LiteLLM gateway URL, model, and enabled tools.
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
- Example tool config:
  ```yaml
  tools:
    enabled:
      - name: "DateTimeTool"
      - name: "WebSearchTool"
      - name: "PromptUserTool"
      - name: "AnalyzeQueryTool"
      - name: "RAGTool"
        params:
          faiss_index_path: "data/my_faiss_index"
  ```

### 6. **(Optional) Add a New Tool**

- Create a new file in `src/tools/`, e.g., `my_custom_tool.py`.
- Define your tool class, inheriting from `Tool`, and register it in `src/tools/__init__.py` (or use the registry pattern).
- Add your tool to the `tools.enabled` list in `config.yaml`.

### 7. **Run the Application**

```bash
python main.py
```

- The system will prompt you for a research query.
- You can provide additional context if needed.
- The agents will research your query using the enabled tools and present a comprehensive answer.
- You can ask follow-up questions in the same session.

---

## 🧩 Architecture Overview

- **smolagents**: Orchestrates agents and tools.
- **LiteLLM**: Any LLM endpoint supported by LiteLLM can be used.
- **Dynamic Tool Registry**: Tools are loaded at runtime based on config.
- **Supervisor/Researcher Agents**: Supervisor plans and synthesizes, researcher gathers information.

---

## 🛠️ Adding or Customizing Tools

1. **Create your tool** in `src/tools/` as a class inheriting from `Tool`.
2. **Register your tool** in the registry in `src/tools/__init__.py`.
3. **Add your tool** to the `tools.enabled` list in `config/config.yaml`, with any required parameters.
4. **Restart the app** to use your new tool.

---

## 🐳 Docker Support

```bash
docker build -t agentic-ai-project .
docker run -it --rm -e LITELLM_API_KEY=your_litellm_api_key agentic-ai-project
```

---

## 📚 Example Session

```
How can I help you today? 
> What are the latest advancements in quantum computing?

Would you like to provide any additional context or clarification? (yes/no)
> no

==== YOUR ANSWER ====
[Comprehensive, synthesized research answer from the agents]
```

---

## License

MIT License - see LICENSE file for details.

---

## Acknowledgments

- Built with [smolagents](https://github.com/huggingface/smolagents)
- Uses [LangChain](https://github.com/langchain-ai/langchain) for optional RAG tool
- Powered by your choice of LLM via LiteLLM

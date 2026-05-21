# Smart-Study-Agent

An AI-powered study assistant agent built in Python. The agent processes student questions and uses multiple tools to deliver helpful answers — including a calculator, file reader, knowledge base search, and text summarizer.

This project was built for the **DIP392 – System Implementation, Testing, and Deployment** practical task at Riga Technical University.

---

## Project Structure

```
ai-assistant-project/
├── main.py               # Entry point — run this to start the assistant
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── src/
│   ├── __init__.py
│   ├── agent.py          # StudyAssistantAgent — core agent logic
│   └── tools.py          # Tool functions: calculator, file_reader, search_tool, summarize_text
├── tests/
│   ├── test_tools.py     # Unit tests for each tool
│   └── test_agent.py     # Unit + integration tests for the agent
└── docs/
    └── architecture.md   # System architecture overview
```

---

## System Overview

The agent receives a user question, selects the appropriate tool(s) based on the content, runs them, and returns a formatted response.

**Tools used:**
| Tool | Purpose |
|------|---------|
| `calculator` | Evaluates math expressions |
| `file_reader` | Reads content from `.txt` files |
| `search_tool` | Searches an internal knowledge base |
| `summarize_text` | Produces a short extractive summary |

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Rupanth-dyno/ai-assistant-project.git
cd ai-assistant-project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> Python 3.10+ recommended. No external API keys required.

### 3. Start the assistant

```bash
python main.py
```

### Example interaction

```
You: What is machine learning?
Assistant:
Question: What is machine learning?

Tool Results:
[search_tool]: Machine learning (ML) is a branch of artificial intelligence...

Summary: Based on the tool results above, here is the information you requested.

You: Calculate 2^10
Assistant:
[calculator]: 1024.0
```

---

## Running Tests

```bash
pytest tests/ -v
```

All tests are located in the `tests/` folder and cover:
- Each tool individually (unit tests)
- Full agent pipeline (integration tests)
- Edge cases: empty input, division by zero, missing files, unknown topics

---

## Deployment

This system is a **local command-line application**. No server or cloud infrastructure is required.

To deploy on another machine:
1. Install Python 3.10+
2. Clone the repo
3. Run `pip install -r requirements.txt`
4. Run `python main.py`

No environment variables or API keys are needed for the default configuration.

---

## Author

**Rupanth Abhinav Pitta**  
DIP392 – Practical Task  
Riga Technical University, 2025/26

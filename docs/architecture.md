# System Architecture

## Overview

The AI Study Assistant is a single-agent system built in Python. It receives natural language input from a user, determines which tools are relevant, executes them, and returns a structured response.

---

## Component Diagram

```
User Input
    │
    ▼
┌─────────────────────────┐
│   StudyAssistantAgent   │  ← main agent logic (agent.py)
│                         │
│  1. Receive input        │
│  2. Select tools         │
│  3. Execute tools        │
│  4. Format response      │
└────────────┬────────────┘
             │ calls
   ┌─────────┼─────────────┐
   ▼         ▼             ▼
calculator  search_tool  file_reader
              ▼
         summarize_text
```

---

## Tool Details

### `calculator(expression: str) -> str`
- Accepts a math expression string.
- Sanitizes input to prevent code injection.
- Uses Python's `eval()` with a restricted namespace.
- Returns computed result or an error message.

### `file_reader(filepath: str) -> str`
- Accepts a relative path to a `.txt` file.
- Validates extension and file existence.
- Returns file contents or a descriptive error.

### `search_tool(query: str) -> str`
- Matches the query against a static knowledge base.
- Falls back to partial word matching.
- In production, this would call an external search API (e.g., Tavily, SerpAPI).

### `summarize_text(text: str, max_sentences: int) -> str`
- Splits input text into sentences using regex.
- Returns the first N sentences as an extractive summary.

---

## Data Flow

```
User types question
        │
        ▼
agent._select_tool(user_input)
        │ returns list of {tool, args}
        ▼
for each tool_call:
    tool_fn(**args) → result string
        │
        ▼
agent._format_response(question, all_results)
        │
        ▼
Printed to user / returned as string
```

---

## Deployment Strategy

The system uses **local/direct deployment**:
- No server, no cloud, no API keys.
- Runs on the user's machine via `python main.py`.
- For a production version, the architecture could be extended to:
  - A **web service** (Flask/FastAPI) for browser access.
  - A **staged release**: alpha → beta → production.
  - A **Dockerized container** for consistent cross-platform deployment.

---

## Versioning

Developed using Git with the following progression:
- Step 1: Project scaffolding, tool stubs
- Step 2: Full tool implementation, agent logic
- Step 3: Test suite, error handling
- Final: Documentation, README, deployment prep

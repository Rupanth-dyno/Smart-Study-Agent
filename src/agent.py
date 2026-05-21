"""
AI Study Assistant Agent
Processes user queries using multiple tools: calculator, file reader, and web search simulation.
"""

import json
from src.tools import calculator, file_reader, search_tool, summarize_text


SYSTEM_PROMPT = """You are a helpful AI study assistant. You help students understand topics,
solve problems, and find information. You have access to the following tools:

- calculator: evaluates math expressions
- file_reader: reads content from local text files
- search_tool: searches for information on a topic
- summarize_text: summarizes a given block of text

When the user asks something, decide which tool(s) to use and return a helpful answer.
Always explain your reasoning and cite tool results clearly.
"""


class StudyAssistantAgent:
    """Single intelligent agent that uses tools to assist students."""

    def __init__(self):
        self.tools = {
            "calculator": calculator,
            "file_reader": file_reader,
            "search_tool": search_tool,
            "summarize_text": summarize_text,
        }
        self.conversation_history = []

    def _select_tool(self, user_input: str) -> list[dict]:
        """
        Decide which tools to call based on the user's input.
        Returns a list of tool call dicts: [{"tool": name, "args": {...}}, ...]
        """
        lower = user_input.lower()
        calls = []

        # Math expressions
        math_keywords = ["+", "-", "*", "/", "^", "calculate", "what is", "how much is", "compute"]
        if any(k in lower for k in math_keywords):
            # Try to extract expression
            import re
            expr = re.findall(r"[\d\s\+\-\*\/\^\(\)\.]+", user_input)
            expr = "".join(expr).strip()
            if expr:
                calls.append({"tool": "calculator", "args": {"expression": expr}})

        # File reading
        if "read" in lower or "file" in lower or ".txt" in lower:
            import re
            filenames = re.findall(r"[\w\-]+\.txt", user_input)
            for fname in filenames:
                calls.append({"tool": "file_reader", "args": {"filepath": fname}})

        # Summarization
        if "summarize" in lower or "summary" in lower:
            calls.append({"tool": "summarize_text", "args": {"text": user_input}})

        # Default: search for information
        if not calls or "search" in lower or "find" in lower or "what" in lower or "explain" in lower:
            calls.append({"tool": "search_tool", "args": {"query": user_input}})

        return calls

    def run(self, user_input: str) -> str:
        """Process user input through the agent pipeline and return a response."""
        if not user_input.strip():
            return "Please provide a valid question or request."

        self.conversation_history.append({"role": "user", "content": user_input})

        tool_calls = self._select_tool(user_input)
        results = []

        for call in tool_calls:
            tool_name = call["tool"]
            args = call["args"]
            tool_fn = self.tools.get(tool_name)

            if tool_fn:
                try:
                    result = tool_fn(**args)
                    results.append(f"[{tool_name}]: {result}")
                except Exception as e:
                    results.append(f"[{tool_name}] Error: {str(e)}")

        tool_output = "\n".join(results) if results else "No tools were invoked."
        response = self._format_response(user_input, tool_output)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def _format_response(self, question: str, tool_output: str) -> str:
        """Format the final response combining question context and tool results."""
        return (
            f"Question: {question}\n\n"
            f"Tool Results:\n{tool_output}\n\n"
            f"Summary: Based on the tool results above, here is the information you requested."
        )

    def get_history(self) -> list[dict]:
        """Return the full conversation history."""
        return self.conversation_history

    def reset(self):
        """Clear conversation history."""
        self.conversation_history = []

"""
Tools available to the AI Study Assistant Agent.
Each tool is a standalone function the agent can call.
"""

import os
import math


def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression safely.

    Args:
        expression: A string containing a math expression, e.g. "2 + 2 * 5"

    Returns:
        The result as a string, or an error message.

    Example:
        >>> calculator("10 / 2 + 3")
        '8.0'
    """
    try:
        # Sanitize: allow only safe characters
        allowed = set("0123456789+-*/(). ^")
        cleaned = expression.replace("^", "**")  # Support caret exponentiation
        if not all(c in allowed or c.isspace() for c in expression):
            return "Error: Expression contains invalid characters."

        result = eval(cleaned, {"__builtins__": {}}, {"sqrt": math.sqrt, "pi": math.pi})
        return str(round(float(result), 6))
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


def file_reader(filepath: str) -> str:
    """
    Reads the contents of a local text file.

    Args:
        filepath: Path to the .txt file (relative to project root or absolute).

    Returns:
        File content as a string, or an error message.

    Example:
        >>> file_reader("data/notes.txt")
        'Contents of notes.txt...'
    """
    try:
        # Restrict to .txt files for safety
        if not filepath.endswith(".txt"):
            return "Error: Only .txt files are supported."

        # Resolve path relative to project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_dir, filepath)

        if not os.path.exists(full_path):
            return f"Error: File '{filepath}' not found."

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            return f"File '{filepath}' is empty."

        return content.strip()
    except PermissionError:
        return f"Error: Permission denied to read '{filepath}'."
    except Exception as e:
        return f"Error reading file: {str(e)}"


def search_tool(query: str) -> str:
    """
    Simulates a knowledge-base search for study topics.
    In a production system, this would call an external search API.

    Args:
        query: The topic or question to search for.

    Returns:
        A relevant summary string from the knowledge base.

    Example:
        >>> search_tool("What is machine learning?")
        'Machine learning is a subset of AI...'
    """
    if not query.strip():
        return "Error: Search query cannot be empty."

    # Simulated knowledge base
    knowledge_base = {
        "machine learning": (
            "Machine learning (ML) is a branch of artificial intelligence that enables systems "
            "to learn and improve from experience without being explicitly programmed. It focuses "
            "on developing programs that access data and use it to learn for themselves."
        ),
        "neural network": (
            "A neural network is a series of algorithms that mimic the operations of a human brain "
            "to recognize relationships between vast amounts of data. They are used in deep learning "
            "and consist of layers: input, hidden, and output layers."
        ),
        "algorithm": (
            "An algorithm is a step-by-step procedure or formula for solving a problem. In computer "
            "science, algorithms are sequences of instructions that a computer follows to complete a task."
        ),
        "python": (
            "Python is a high-level, interpreted programming language known for its clear syntax "
            "and readability. It supports multiple programming paradigms and is widely used in data "
            "science, AI, web development, and automation."
        ),
        "testing": (
            "Software testing is the process of evaluating and verifying that a software product does "
            "what it is supposed to do. Types include unit testing, integration testing, system testing, "
            "and acceptance testing."
        ),
        "deployment": (
            "Software deployment includes all activities that make a software system available for use. "
            "Strategies include direct deployment, parallel deployment, and phased deployment."
        ),
        "agent": (
            "An AI agent is a program that perceives its environment through inputs and produces actions "
            "to affect that environment. Agents can use tools, make decisions, and operate autonomously."
        ),
    }

    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value

    # Fuzzy fallback: match any keyword in the query
    words = query_lower.split()
    for word in words:
        for key, value in knowledge_base.items():
            if word in key:
                return f"(Partial match for '{key}'): {value}"

    return (
        f"No specific information found for: '{query}'. "
        "Please try a more specific topic such as 'machine learning', 'Python', 'testing', or 'deployment'."
    )


def summarize_text(text: str, max_sentences: int = 3) -> str:
    """
    Produces a short extractive summary of the given text.

    Args:
        text: The input text to summarize.
        max_sentences: Maximum number of sentences in the summary (default: 3).

    Returns:
        A short summary string.

    Example:
        >>> summarize_text("Python is great. It is used for AI. Many love it.", max_sentences=2)
        'Python is great. It is used for AI.'
    """
    if not text.strip():
        return "Error: Cannot summarize empty text."

    # Split into sentences (simple approach)
    import re
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return "No sentences found in the provided text."

    # Return first N sentences as the summary
    summary_sentences = sentences[:max_sentences]
    return " ".join(summary_sentences)

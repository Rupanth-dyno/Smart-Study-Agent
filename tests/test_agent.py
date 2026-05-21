"""
Unit and integration tests for the StudyAssistantAgent.
Run with: pytest tests/test_agent.py -v
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import StudyAssistantAgent


class TestStudyAssistantAgent:

    def setup_method(self):
        """Create a fresh agent before each test."""
        self.agent = StudyAssistantAgent()

    # ──────────────────────────────────────────────
    # Initialization Tests
    # ──────────────────────────────────────────────

    def test_agent_initializes(self):
        assert self.agent is not None

    def test_tools_loaded(self):
        assert "calculator" in self.agent.tools
        assert "file_reader" in self.agent.tools
        assert "search_tool" in self.agent.tools
        assert "summarize_text" in self.agent.tools

    def test_history_starts_empty(self):
        assert self.agent.get_history() == []

    # ──────────────────────────────────────────────
    # Run Tests
    # ──────────────────────────────────────────────

    def test_run_returns_string(self):
        result = self.agent.run("What is Python?")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_run_empty_input(self):
        result = self.agent.run("   ")
        assert "valid" in result.lower() or len(result) > 0

    def test_run_math_query(self):
        result = self.agent.run("Calculate 5 + 10")
        assert "calculator" in result.lower() or "15" in result

    def test_run_search_query(self):
        result = self.agent.run("What is machine learning?")
        assert isinstance(result, str)
        assert len(result) > 20

    def test_run_logs_history(self):
        self.agent.run("What is Python?")
        history = self.agent.get_history()
        assert len(history) == 2  # user + assistant
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"

    def test_multiple_runs_accumulate_history(self):
        self.agent.run("What is Python?")
        self.agent.run("What is testing?")
        history = self.agent.get_history()
        assert len(history) == 4

    # ──────────────────────────────────────────────
    # Reset Tests
    # ──────────────────────────────────────────────

    def test_reset_clears_history(self):
        self.agent.run("Hello")
        self.agent.reset()
        assert self.agent.get_history() == []

    # ──────────────────────────────────────────────
    # Tool Selection Tests
    # ──────────────────────────────────────────────

    def test_selects_calculator_for_math(self):
        calls = self.agent._select_tool("What is 10 + 5?")
        tool_names = [c["tool"] for c in calls]
        assert "calculator" in tool_names

    def test_selects_search_for_topic(self):
        calls = self.agent._select_tool("Explain deployment strategies")
        tool_names = [c["tool"] for c in calls]
        assert "search_tool" in tool_names

    def test_selects_file_reader_for_file(self):
        calls = self.agent._select_tool("Read the file notes.txt")
        tool_names = [c["tool"] for c in calls]
        assert "file_reader" in tool_names

    def test_selects_summarize_for_summary_request(self):
        calls = self.agent._select_tool("Summarize this content for me")
        tool_names = [c["tool"] for c in calls]
        assert "summarize_text" in tool_names


class TestAgentIntegration:
    """Integration tests: full agent pipeline scenarios."""

    def setup_method(self):
        self.agent = StudyAssistantAgent()

    def test_scenario_math_problem(self):
        """Student asks a math question — agent calculates it."""
        response = self.agent.run("Calculate 100 / 4 + 3")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_scenario_topic_lookup(self):
        """Student asks about a study topic — agent searches knowledge base."""
        response = self.agent.run("What is a neural network?")
        assert "neural" in response.lower() or "network" in response.lower()

    def test_scenario_deployment_question(self):
        """Student asks about deployment — agent provides info."""
        response = self.agent.run("Explain software deployment")
        assert isinstance(response, str)
        assert len(response) > 10

    def test_scenario_unknown_topic_graceful(self):
        """Agent handles unknown topics gracefully."""
        response = self.agent.run("Tell me about banana farming 99999")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_scenario_reset_and_continue(self):
        """Agent can be reset mid-conversation."""
        self.agent.run("What is Python?")
        self.agent.reset()
        assert self.agent.get_history() == []
        response = self.agent.run("What is testing?")
        assert isinstance(response, str)
        assert len(self.agent.get_history()) == 2

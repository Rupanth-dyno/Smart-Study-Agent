"""
AI Study Assistant - Main Entry Point
Run this file to start the interactive assistant.
"""

from src.agent import StudyAssistantAgent


def main():
    """Start the interactive AI Study Assistant."""
    print("=" * 60)
    print("   AI Study Assistant - Powered by Agent + Tools")
    print("=" * 60)
    print("Type your question or request and press Enter.")
    print("Commands: 'history' to see conversation, 'reset' to clear, 'quit' to exit.")
    print("-" * 60)

    agent = StudyAssistantAgent()

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        elif user_input.lower() == "history":
            history = agent.get_history()
            if not history:
                print("No conversation history yet.")
            else:
                for entry in history:
                    print(f"\n[{entry['role'].upper()}]: {entry['content']}")
            continue
        elif user_input.lower() == "reset":
            agent.reset()
            print("Conversation history cleared.")
            continue

        response = agent.run(user_input)
        print(f"\nAssistant:\n{response}")


if __name__ == "__main__":
    main()

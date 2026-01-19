#!/usr/bin/env python3
"""
Simple Claude API Client
Demonstrates how to use the Anthropic SDK to interact with Claude
"""

import os
import sys
from anthropic import Anthropic

def main():
    # Get API key from environment variable
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set your API key:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print("\nGet your API key from: https://console.anthropic.com/")
        sys.exit(1)

    # Initialize the Anthropic client
    client = Anthropic(api_key=api_key)

    print("Claude API Client")
    print("=" * 50)
    print("Type 'exit' or 'quit' to end the conversation")
    print("=" * 50)
    print()

    # Conversation loop
    conversation_history = []

    while True:
        # Get user input
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        # Add user message to conversation
        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        try:
            # Call Claude API
            response = client.messages.create(
                model="claude-sonnet-4-20250514",  # Latest Claude Sonnet
                max_tokens=4096,
                messages=conversation_history
            )

            # Extract Claude's response
            assistant_message = response.content[0].text

            # Add assistant's response to conversation
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            # Display response
            print(f"\nClaude: {assistant_message}\n")

        except Exception as e:
            print(f"\nError: {e}\n")
            # Remove the failed user message from history
            conversation_history.pop()

if __name__ == "__main__":
    main()

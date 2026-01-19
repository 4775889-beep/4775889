#!/usr/bin/env python3
"""
Advanced Claude API Client Examples
Demonstrates various features of the Anthropic SDK
"""

import os
import sys
from anthropic import Anthropic

def simple_chat(client):
    """Simple one-shot conversation"""
    print("\n=== Simple Chat ===")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "What is PyTorch AMP and why is it useful?"}
        ]
    )

    print(f"Claude: {message.content[0].text}\n")


def streaming_response(client):
    """Streaming response for real-time output"""
    print("\n=== Streaming Response ===")

    prompt = "Explain automatic mixed precision training in 3 short paragraphs."

    print(f"User: {prompt}")
    print("Claude: ", end="", flush=True)

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n")


def system_prompt_example(client):
    """Using system prompts to control Claude's behavior"""
    print("\n=== System Prompt Example ===")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="You are a Python expert who explains concepts using code examples. Always include working code.",
        messages=[
            {"role": "user", "content": "How do I use PyTorch's autocast?"}
        ]
    )

    print(f"Claude (as Python expert): {message.content[0].text}\n")


def multi_turn_conversation(client):
    """Multi-turn conversation with context"""
    print("\n=== Multi-turn Conversation ===")

    messages = []

    # Turn 1
    messages.append({"role": "user", "content": "What is gradient scaling?"})
    response1 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=messages
    )
    messages.append({"role": "assistant", "content": response1.content[0].text})
    print(f"User: What is gradient scaling?")
    print(f"Claude: {response1.content[0].text}\n")

    # Turn 2 (with context from Turn 1)
    messages.append({"role": "user", "content": "Can you show me a code example?"})
    response2 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=messages
    )
    print(f"User: Can you show me a code example?")
    print(f"Claude: {response2.content[0].text}\n")


def token_counting(client):
    """Count tokens in a message"""
    print("\n=== Token Counting ===")

    text = "This is a test message to count tokens."

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": text}]
    )

    print(f"Input text: {text}")
    print(f"Input tokens: {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")
    print(f"Total tokens: {response.usage.input_tokens + response.usage.output_tokens}\n")


def main():
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set your API key:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print("\nGet your API key from: https://console.anthropic.com/")
        sys.exit(1)

    # Initialize client
    client = Anthropic(api_key=api_key)

    print("Claude API Advanced Examples")
    print("=" * 50)

    try:
        # Run examples
        simple_chat(client)
        streaming_response(client)
        system_prompt_example(client)
        multi_turn_conversation(client)
        token_counting(client)

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

    print("=" * 50)
    print("All examples completed successfully!")


if __name__ == "__main__":
    main()

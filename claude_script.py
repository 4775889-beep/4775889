#!/usr/bin/env python3
"""
Claude API Batch Script
Reads prompts from a file and sends to Claude API
Usage: python claude_script.py <prompt_file>
"""

import anthropic
import sys
import os

def read_prompt(file_path):
    """Read prompt from file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    if len(sys.argv) < 2:
        print("Usage: python claude_script.py <prompt_file>")
        sys.exit(1)

    prompt_file = sys.argv[1]
    prompt = read_prompt(prompt_file)

    # Read API key from environment variable
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set your API key:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print("\nGet your API key from: https://console.anthropic.com/")
        sys.exit(1)

    # Create client and send request
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Print response
    print(response.content[0].text)

if __name__ == "__main__":
    main()

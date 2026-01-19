#!/usr/bin/env python3
"""
Claude Code Generator
Reads prompts from files and generates code, saving output to files
Usage: python my_claude_coder.py PROMPT.md
"""

import anthropic
import sys
import os
import re

def process_prompt_file(filename):
    """Process prompt file and generate code"""

    # Read prompt
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            prompt = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set your API key:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)

    # Call Claude API
    print(f"Processing prompt from: {filename}")
    print("Calling Claude API...")

    client = anthropic.Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        print(f"Error calling API: {e}")
        sys.exit(1)

    # Get response text
    response_text = response.content[0].text

    # Determine output filename
    if filename.endswith('.md'):
        output_file = "generated_" + filename.replace(".md", ".py")
    else:
        output_file = "generated_output.py"

    # Save response to file
    with open(output_file, 'w', encoding='utf-8') as f:
        # If response contains code blocks, extract them
        if '```python' in response_text:
            # Extract Python code from markdown code blocks
            code_blocks = re.findall(r'```python\n(.*?)```', response_text, re.DOTALL)
            if code_blocks:
                f.write('\n\n'.join(code_blocks))
            else:
                f.write(response_text)
        else:
            f.write(response_text)

    print(f"✓ Code generated successfully!")
    print(f"✓ Output saved to: {output_file}")

    # Print preview
    print("\n--- Preview (first 20 lines) ---")
    with open(output_file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:20], 1):
            print(f"{i:3}: {line}", end='')
        if len(lines) > 20:
            print(f"\n... ({len(lines) - 20} more lines)")
    print("--- End Preview ---\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python my_claude_coder.py PROMPT.md")
        print("\nExample:")
        print("  python my_claude_coder.py PROMPT.md")
        sys.exit(1)

    prompt_file = sys.argv[1]
    process_prompt_file(prompt_file)

if __name__ == "__main__":
    main()

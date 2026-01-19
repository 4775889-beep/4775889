#!/usr/bin/env python3
"""
Automatic Code Generation Loop with Error Correction
Generates code, runs it, and iterates with error feedback until success

Usage: python auto_code_loop.py PROMPT.md
"""

import anthropic
import sys
import os
import subprocess
import re

MAX_ITERATIONS = 5

def extract_code_from_response(response_text):
    """Extract Python code from markdown code blocks"""
    if '```python' in response_text:
        code_blocks = re.findall(r'```python\n(.*?)```', response_text, re.DOTALL)
        if code_blocks:
            return '\n\n'.join(code_blocks)
    return response_text

def run_generated_code(code_file):
    """Run generated Python code and capture output"""
    try:
        result = subprocess.run(
            ['python3', code_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Error: Code execution timeout (>10s)"
    except Exception as e:
        return -1, "", f"Error running code: {e}"

def call_claude(client, messages):
    """Call Claude API with messages"""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        messages=messages
    )
    return response.content[0].text

def auto_generate_loop(prompt_file):
    """Main loop: generate code, test, and iterate with error feedback"""

    # Read initial prompt
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            initial_prompt = f.read()
    except FileNotFoundError:
        print(f"Error: File '{prompt_file}' not found")
        sys.exit(1)

    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    messages = []
    output_file = "generated_code.py"

    print("=" * 60)
    print("Automatic Code Generation Loop")
    print("=" * 60)

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- Iteration {iteration}/{MAX_ITERATIONS} ---")

        # Prepare prompt for this iteration
        if iteration == 1:
            current_prompt = initial_prompt
        else:
            current_prompt = f"""The previous code had errors. Please fix them.

Error output:
{error_output}

Please provide corrected code."""

        messages.append({"role": "user", "content": current_prompt})

        # Call Claude API
        print("Calling Claude API...")
        try:
            response = call_claude(client, messages)
            messages.append({"role": "assistant", "content": response})
        except Exception as e:
            print(f"Error calling API: {e}")
            sys.exit(1)

        # Extract and save code
        code = extract_code_from_response(response)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)

        print(f"✓ Code generated and saved to: {output_file}")

        # Run the code
        print("Running generated code...")
        returncode, stdout, stderr = run_generated_code(output_file)

        # Check results
        if returncode == 0 and not stderr:
            print("✓ Code executed successfully!")
            if stdout:
                print("\n--- Output ---")
                print(stdout)
                print("--- End Output ---")
            print(f"\n{'=' * 60}")
            print("SUCCESS! Code is working correctly.")
            print(f"Final code saved to: {output_file}")
            print(f"{'=' * 60}")
            return True
        else:
            print("✗ Code execution failed")
            error_output = stderr if stderr else f"Exit code: {returncode}"
            print(f"\nError output:\n{error_output}\n")

            if iteration == MAX_ITERATIONS:
                print(f"\n{'=' * 60}")
                print(f"FAILED after {MAX_ITERATIONS} iterations")
                print(f"Last generated code saved to: {output_file}")
                print(f"{'=' * 60}")
                return False

            print("Retrying with error feedback...")

    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_code_loop.py PROMPT.md")
        print("\nExample:")
        print("  python auto_code_loop.py PROMPT.md")
        sys.exit(1)

    prompt_file = sys.argv[1]
    success = auto_generate_loop(prompt_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

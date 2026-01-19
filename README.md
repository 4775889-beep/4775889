# PyTorch AMP Test

This repository contains a test script for PyTorch Automatic Mixed Precision (AMP) training.

## Installation

### Quick Install

```bash
curl -fsSL https://raw.githubusercontent.com/4775889-beep/4775889/main/install.sh | bash
```

### Manual Install

```bash
git clone https://github.com/4775889-beep/4775889.git
cd 4775889
chmod +x install.sh
./install.sh
```

## Usage

After installation, run the test script:

```bash
python3 test-amp.py
```

If you used a virtual environment during installation:

```bash
source venv/bin/activate
python3 test-amp.py
```

## Requirements

- Python 3.8 or higher
- PyTorch (installed automatically by install.sh)
- NVIDIA GPU with CUDA support (optional, will use CPU if not available)

## What the Test Does

The `test-amp.py` script benchmarks PyTorch's Automatic Mixed Precision (AMP) training by:
- Creating a neural network with configurable layers
- Training on synthetic data
- Using mixed precision (float16) for faster computation
- Measuring execution time and memory usage

---

## Claude API Client Examples

This repository also includes Claude API client examples for building your own AI-powered tools.

### Setup

1. **Get your API key** from [Anthropic Console](https://console.anthropic.com/)

2. **Install the Anthropic SDK:**
   ```bash
   pip install anthropic
   ```

3. **Set your API key:**
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

### Available Scripts

#### 1. Interactive Chat Client (`claude_client.py`)
A simple interactive CLI chat with Claude:
```bash
python3 claude_client.py
```

Features:
- Multi-turn conversation with context
- Simple command-line interface
- Type 'exit' or 'quit' to end

#### 2. Batch Script (`claude_script.py`)
Process prompts from files:
```bash
python3 claude_script.py example_prompt.txt
```

Use cases:
- Batch processing of prompts
- Automation workflows
- Code generation from specifications

#### 3. Advanced Examples (`claude_advanced.py`)
Demonstrates various API features:
```bash
python3 claude_advanced.py
```

Includes:
- Simple one-shot conversations
- Streaming responses for real-time output
- System prompts for behavior control
- Multi-turn conversations with context
- Token usage counting

### Example Workflow

Create a prompt file and get Claude's response:
```bash
# Create a prompt
echo "Explain PyTorch gradient scaling" > my_prompt.txt

# Get response
python3 claude_script.py my_prompt.txt

# Or use interactive mode
python3 claude_client.py
```

### Building Your Own AI Tools

Use these scripts as templates to build:
- Code generators
- Documentation writers
- Automated code reviewers
- Custom AI assistants
- Batch processing pipelines

All scripts handle API key management, error handling, and demonstrate best practices for using the Anthropic SDK.

---

## Advanced: Code Generation Tools

### `my_claude_coder.py` - Smart Code Generator

Generates code from prompt files with intelligent code extraction:

```bash
python3 my_claude_coder.py PROMPT.md
```

Features:
- Automatically extracts Python code from markdown responses
- Saves generated code to files
- Shows preview of generated code
- Smart filename handling (PROMPT.md → generated_PROMPT.py)

**Example:**
```bash
# Edit your prompt
nano PROMPT.md

# Generate code
python3 my_claude_coder.py PROMPT.md

# Output: generated_PROMPT.py
```

### `auto_code_loop.py` - Auto-Fixing Code Generator

Automatically generates code, runs it, and fixes errors iteratively:

```bash
python3 auto_code_loop.py RUNNABLE_PROMPT.md
```

Features:
- Generates code from your prompt
- Runs the generated code
- If errors occur, sends them back to Claude for fixing
- Iterates up to 5 times until code works
- Perfect for rapid prototyping

**How it works:**
1. Reads your prompt from a file
2. Calls Claude API to generate code
3. Saves and executes the generated code
4. If errors occur, sends error messages back to Claude
5. Repeats until code runs successfully or max iterations reached

**Example workflow:**
```bash
# Create a prompt for runnable code
cat > my_task.md << 'EOF'
Write a Python script that:
1. Reads a CSV file
2. Calculates average of a column
3. Prints the result
EOF

# Auto-generate and fix until it works
python3 auto_code_loop.py my_task.md

# Result: working code in generated_code.py
```

### Sample Prompts Included

- `PROMPT.md` - Example for basic code generation
- `RUNNABLE_PROMPT.md` - Example for executable code generation
- `example_prompt.txt` - Example for Q&A

Try them out:
```bash
python3 my_claude_coder.py PROMPT.md
python3 auto_code_loop.py RUNNABLE_PROMPT.md
```
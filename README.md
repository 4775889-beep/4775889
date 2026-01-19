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
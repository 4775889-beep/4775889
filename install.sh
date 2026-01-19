#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}PyTorch AMP Test - Installation${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""

# Check if Python is installed
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}Installing pip...${NC}"
    python3 -m ensurepip --default-pip || {
        echo -e "${RED}Failed to install pip. Please install it manually.${NC}"
        exit 1
    }
fi

echo -e "${GREEN}✓ pip found${NC}"

# Detect CUDA availability
echo ""
echo -e "${YELLOW}Detecting CUDA...${NC}"
if command -v nvidia-smi &> /dev/null; then
    CUDA_AVAILABLE=true
    CUDA_VERSION=$(nvidia-smi | grep -oP 'CUDA Version: \K[0-9.]+' || echo "Unknown")
    echo -e "${GREEN}✓ NVIDIA GPU detected (CUDA ${CUDA_VERSION})${NC}"
    echo -e "${YELLOW}Installing PyTorch with CUDA support...${NC}"
    TORCH_INSTALL="torch torchvision torchaudio"
else
    CUDA_AVAILABLE=false
    echo -e "${YELLOW}No NVIDIA GPU detected. Installing CPU-only PyTorch...${NC}"
    TORCH_INSTALL="torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
fi

# Create virtual environment (optional but recommended)
echo ""
echo -e "${YELLOW}Do you want to create a virtual environment? (recommended) [y/N]${NC}"
read -r -n 1 USE_VENV
echo ""

if [[ $USE_VENV =~ ^[Yy]$ ]]; then
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    else
        echo -e "${YELLOW}Virtual environment already exists${NC}"
    fi

    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
fi

# Install PyTorch
echo ""
echo -e "${YELLOW}Installing PyTorch and dependencies...${NC}"
pip3 install --upgrade pip
pip3 install $TORCH_INSTALL

echo ""
echo -e "${GREEN}✓ Installation complete!${NC}"
echo ""

# Verify installation
echo -e "${YELLOW}Verifying PyTorch installation...${NC}"
python3 -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')" || {
    echo -e "${RED}Failed to verify PyTorch installation${NC}"
    exit 1
}

echo ""
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}Installation successful!${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""

if [[ $USE_VENV =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}To run the test script:${NC}"
    echo -e "  source venv/bin/activate"
    echo -e "  python3 test-amp.py"
else
    echo -e "${YELLOW}To run the test script:${NC}"
    echo -e "  python3 test-amp.py"
fi

echo ""

if [ "$CUDA_AVAILABLE" = false ]; then
    echo -e "${YELLOW}Note: No CUDA GPU detected. The script will run on CPU.${NC}"
    echo -e "${YELLOW}Performance will be significantly slower than GPU execution.${NC}"
fi

#!/bin/bash

# YT Short Clipper - macOS Runner Script
# This script ensures dependencies are installed and runs the app.

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}== YT Short Clipper for macOS ==${NC}"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is not installed. Please install it first.${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install/Update dependencies
echo -e "${GREEN}Checking dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Run the application
echo -e "${BLUE}Launching application...${NC}"
python3 app.py

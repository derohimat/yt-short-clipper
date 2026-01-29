#!/bin/bash

# YT Short Clipper - Mac Build Script
# This script handles the build process using a virtual environment to avoid 
# "externally-managed-environment" errors on macOS.

echo "🛠️  Starting build process for macOS..."

# 0. Check for tkinter/tcl-tk (Common issue on Homebrew Python)
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "❌ Error: tkinter not found in your Python installation."
    echo "💡 Please run: brew install python-tk@3.14"
    echo "   (Adjust version if you are not using Python 3.14)"
    exit 1
fi
if [ ! -d "venv_build" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv_build
fi

# 2. Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv_build/bin/activate

# 3. Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# 4. Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# 5. Install pyinstaller
echo "📥 Installing PyInstaller..."
pip install pyinstaller

# 6. Run the build
echo "🏗️  Building application bundle..."
pyinstaller --noconfirm macos_build.spec

echo "✨ Build completed! You can find the app in the 'dist' folder."
echo "💡 To run the app, type: open dist/AutoClipper.app"

# 7. Deactivate
deactivate
export PATH=$PATH

#!/bin/bash

# Build macOS app script for Alfred Pennyworth

# Ensure we're in the right directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=== Building Alfred Pennyworth macOS App ==="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi

# Generate the icon if it doesn't exist
if [ ! -f "static/alfred_icon.png" ] || [ ! -f "static/alfred_icon_menu.png" ]; then
    echo "Generating app icons..."
    python3 static/alfred_icon.py
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Build the app
echo "Building macOS app..."
python3 setup.py py2app

# Check if build was successful
if [ -d "dist/Alfred Pennyworth.app" ]; then
    echo "=== Build Successful! ==="
    echo "The app has been created at: $(pwd)/dist/Alfred Pennyworth.app"
    echo "You can run it by double-clicking on it in Finder or by running:"
    echo "open \"$(pwd)/dist/Alfred Pennyworth.app\""
else
    echo "=== Build Failed! ==="
    echo "Check the error messages above for details."
    exit 1
fi

# Make the app executable
chmod +x "dist/Alfred Pennyworth.app/Contents/MacOS/Alfred Pennyworth"

echo "Done!"
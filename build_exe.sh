#!/bin/bash
# Build script for Fallout 4 Resolution Updater
# Builds a Windows .exe from WSL

set -e

echo "Building Fallout 4 Resolution Updater..."
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Try to find Windows Python
WINDOWS_PYTHON=""
if [ -f "/mnt/c/Windows/System32/python.exe" ]; then
    WINDOWS_PYTHON="/mnt/c/Windows/System32/python.exe"
elif [ -f "/mnt/c/Program Files/Python*/python.exe" ]; then
    WINDOWS_PYTHON=$(ls -1 "/mnt/c/Program Files/Python"*"/python.exe" 2>/dev/null | head -n 1)
elif [ -f "/mnt/c/Users/$USER/AppData/Local/Programs/Python/Python*/python.exe" ]; then
    WINDOWS_PYTHON=$(ls -1 "/mnt/c/Users/$USER/AppData/Local/Programs/Python/Python"*"/python.exe" 2>/dev/null | head -n 1)
fi

# Try to use Windows Python if available
if [ -n "$WINDOWS_PYTHON" ] && [ -f "$WINDOWS_PYTHON" ]; then
    echo "Found Windows Python: $WINDOWS_PYTHON"
    PYTHON_CMD="$WINDOWS_PYTHON"
    PIP_CMD="${WINDOWS_PYTHON%python.exe}pip.exe"
    
    # Check if PyInstaller is installed
    if ! "$PYTHON_CMD" -m pip show pyinstaller >/dev/null 2>&1; then
        echo "Installing PyInstaller..."
        "$PYTHON_CMD" -m pip install pyinstaller
    fi
    
    echo ""
    echo "Building executable with Windows Python..."
    "$PYTHON_CMD" -m PyInstaller --onefile --name "UpdateFallout4Resolution" update_fallout4_resolution.py
    
    echo ""
    echo "Build complete! The executable is in the 'dist' folder."
    exit 0
fi

# Fallback: Try using Wine with Python
if command_exists wine; then
    echo "Windows Python not found. Attempting to use Wine..."
    echo "Note: This requires Python for Windows installed in Wine."
    echo ""
    
    # Check if pyinstaller is available via wine python
    if wine python --version >/dev/null 2>&1; then
        echo "Found Python in Wine"
        
        if ! wine python -m pip show pyinstaller >/dev/null 2>&1; then
            echo "Installing PyInstaller in Wine..."
            wine python -m pip install pyinstaller
        fi
        
        echo ""
        echo "Building executable with Wine Python..."
        wine python -m PyInstaller --onefile --name "UpdateFallout4Resolution" update_fallout4_resolution.py
        
        echo ""
        echo "Build complete! The executable is in the 'dist' folder."
        exit 0
    fi
fi

# Last resort: Use Linux Python (will create Linux executable, not Windows .exe)
if command_exists python3; then
    echo "Warning: Could not find Windows Python or Wine."
    echo "Using Linux Python will create a Linux executable, not a Windows .exe."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if ! python3 -m pip show pyinstaller >/dev/null 2>&1; then
            echo "Installing PyInstaller..."
            python3 -m pip install pyinstaller
        fi
        
        echo ""
        echo "Building executable..."
        python3 -m PyInstaller --onefile --name "UpdateFallout4Resolution" update_fallout4_resolution.py
        
        echo ""
        echo "Build complete! The executable is in the 'dist' folder."
        echo "Note: This is a Linux executable, not a Windows .exe"
        exit 0
    fi
fi

echo "ERROR: Could not find Python or Wine."
echo ""
echo "To build a Windows .exe from WSL, you need one of:"
echo "  1. Windows Python installed (will be auto-detected)"
echo "  2. Wine with Python for Windows installed"
echo ""
echo "Alternatively, you can use the build_exe.bat script from Windows."
exit 1

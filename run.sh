#!/bin/bash

# Detect Operating System (Linux or Windows)
OS=$(uname -s)

# On Linux
if [[ "$OS" == "Linux" ]]; then
    echo "Running on Linux..."
    # Check if the virtual environment exists
    if [ -d "Gemini Echo" ]; then
        # Activate the virtual environment
        source "Gemini Echo/bin/activate"
    else
        source ".venv/bin/activate"
    fi

elif [[ "$OS" == *"NT"* ]]; then
    echo "Running on Windows..."
    # On Windows (Git Bash), use the Scripts/activate.bat script
    source "Gemini Echo/Scripts/activate"
else
    echo "Unknown Operating System!"
    exit 1
fi

# Run the script
python app.py

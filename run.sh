#!/bin/bash

# Detect Operating System (Linux or Windows)
OS=$(uname -s)

# On Linux
if [[ "$OS" == "Linux" ]]; then
    echo "Running on Linux..."
    # Check if the virtual environment exists
    if [ ! -d "Gemini Echo" ]; then
        echo "Virtual environment not found. Creating it..."
        # Install virtualenv if it's not installed
        if ! command -v virtualenv &>/dev/null; then
            echo "virtualenv not found. Installing it..."
            pip install virtualenv
        fi
        # Create a new virtual environment
        virtualenv "Gemini Echo"
    fi

    # Activate the virtual environment
    source "Gemini Echo/bin/activate"

    # Install dependencies if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies from requirements.txt..."
        pip install -r requirements.txt
    else
        echo "requirements.txt not found. Skipping dependency installation."
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

# Check if python execution was successful
if [ $? -eq 0 ]; then
    exit 0 # Exit if python worked
elif python3 app.py; then
    exit 0 # Exit if python3 worked
elif pypy3 app.py; then
    exit 0 # Exit if pypy3 worked
elif pypy app.py; then
    exit 0 # Exit if pypy worked
else
    # All attempts failed, print failure message
    echo "Script failed to execute with all Python versions."
    exit 1
fi

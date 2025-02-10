import os
import json
from rich.console import Console

console = Console()  # Initialize Rich console for better output formatting

# Memory file path
MEMORY_FILE = os.path.join(os.getcwd(), "memory.json")


# Function to load memory from file
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            console.print("Memory file is corrupted. Resetting...", style="bold red")
    else:
        console.print("Memory file not found. Creating new...", style="bold yellow")

    # Initialize default memory structure
    memory = {}
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)
    return memory


# Function to save memory to file
def save_memory(data):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        console.print(f"❌ Error saving memory: {e}", style="bold red")

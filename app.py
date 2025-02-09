import os
import json
from google import genai
from rich.markdown import Markdown
from rich.console import Console
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Rich console for better output formatting
console = Console()
console.print(Markdown("- Hi, how can I assist you?\n"))

# Initialize the GenAI client
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

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


# Load stored memory
memory = load_memory()

# Main interaction loop
while True:
    prompt = input("\033[0m•\033[0m ")

    if prompt.lower() in ["exit", "quit", "bye", "bye bye", "goodbye", "good bye"]:
        console.print(Markdown("**See you again... Goodbye!** 👋"))
        break

    # Store memory for user-specific data
    if any(
        keyword in prompt.lower()
        for keyword in ["remember", "mind it", "note that", "save it"]
    ):
        for keyword in ["remember", "mind it", "note that", "save it"]:
            if keyword in prompt.lower():
                memory_text = prompt.lower().split(keyword, 1)[1].strip()
                if memory_text:
                    # Ask AI to reformat the memory as a clean key-value pair
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[
                            f"Convert this into a simple key-value format for AI memory. Just one simple key-value:\n'{memory_text}'"
                        ],
                    )
                    formatted_memory = response.text.strip()

                    if ":" in formatted_memory:
                        key, value = formatted_memory.split(":", 1)
                        memory[key.strip()] = value.strip()
                        save_memory(memory)
                        console.print("Memory updated!", style="i Cyan")
                        console.print(Markdown("**Got it! I'll remember that...**"))
                        break
        continue

    # Identify whether the question is about the AI or the user
    if any(
        keyword in prompt.lower()
        for keyword in ["who are you", "your name", "yourself", "your"]
    ):
        # AI-related response
        full_prompt = (
            "Describe yourself as an AI assistant shortly. Be dynamic and creative."
        )
    elif any(
        keyword in prompt.lower()
        for keyword in ["am i", "my", "mine", "myself", "me", "about me"]
    ):
        # User-related response
        memory_context = "\n".join(f"{k}: {v}" for k, v in memory.items())
        full_prompt = f"Contextual memory:\n{memory_context}\n\nUser: {prompt}"
    else:
        # General question without specific memory
        full_prompt = prompt

    # Generate AI response
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[full_prompt],
    )

    console.print("\n", Markdown(response.text), "\n")

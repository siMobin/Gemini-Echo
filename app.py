import os
import json
import pytz
from google import genai
from datetime import datetime
from google.genai import types
from rich.markdown import Markdown
from rich.console import Console
from dotenv import load_dotenv
from Functions.Files import *
from Functions.memory import *
from Functions.Data import chat_log, MK_File
from Functions.Input import multiline_input
from Functions.getResponse import process_prompt


# Load environment variables
load_dotenv()
# Initialize Rich console for better output formatting
console = Console()
# Initialize the GenAI client
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
# Get model
ai_model = os.getenv("GEMINI_MODEL_ID")
# Load memory (long-term/permanent memory)
memory = load_memory()
# Short-term memory for contextual responses
history = []

# Load instructions
keywords_path = "instructions/keywords.json"
commands_path = "instructions/commands.json"

with open(keywords_path, "r", encoding="utf-8") as f:
    keywords = json.load(f)

with open(commands_path, "r", encoding="utf-8") as f:
    commands = json.load(f)

# System instructions & configuration
sys_instruct = commands["system_instructions"]
log_file = MK_File()

if os.getenv("WARM_AT_STARTUP") == "true":
    startup = client.models.generate_content(
        model=ai_model,
        config=types.GenerateContentConfig(
            system_instruction=sys_instruct
            + f'Current date/time: {datetime.now(pytz.timezone("Asia/Dhaka")).isoformat(timespec="milliseconds")}',
            temperature=os.getenv("STARTUP_TEMPERATURE"),
        ),
        contents=commands["startup"],
    )
    console.print("\n", Markdown(startup.text), "\n")
    chat_log(log_file, "Startup", "@startup=True", startup.text)
    history.append(f"AI: {startup.text}")
else:
    console.print(Markdown("- Hay, What are you doing?"), style="bold Yellow")

# Main interaction loop
while True:
    prompt = multiline_input()

    process_prompt(prompt, log_file)

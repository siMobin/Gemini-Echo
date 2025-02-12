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
from Functions.Path import extract_path
from Functions.Data import chat_log, MK_File
from Functions.Input import multiline_input


# Load environment variables
load_dotenv()
# Initialize Rich console for better output formatting
console = Console()
console.print(Markdown("- Hi, how can I assist you?"), style="bold Green")
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
config = types.GenerateContentConfig(
    system_instruction=sys_instruct,
    temperature=0.7,
    tools=[
        types.Tool(
            google_search=types.GoogleSearchRetrieval(
                dynamic_retrieval_config=types.DynamicRetrievalConfig(
                    dynamic_threshold=0.6
                )
            )
        )
    ],
)
log_file = MK_File()


# Main interaction loop
while True:
    # prompt = input("\033[0m•\033[0m ")
    prompt = multiline_input()

    try:
        file_path = extract_path(prompt)
        if file_path:
            console.print(Markdown(f"**~File: {file_path}**"), style="i medium_orchid3")
            info = read_file(file_path)
            prompt = info + "\n" + prompt
    except:
        pass

    if prompt.lower() in keywords["farewells"]:
        console.print(Markdown("**See you again... Goodbye!** 👋"))
        break

    # Store memory for user-specific data
    if any(keyword in prompt.lower() for keyword in keywords["memorization"]):
        for keyword in keywords["memorization"]:
            if keyword in prompt.lower():
                memory_text = prompt.lower().split(keyword, 1)[1].strip()
                if memory_text:
                    # Ask AI to format the memory
                    response = client.models.generate_content(
                        model=ai_model,
                        contents=[f"{commands['create_memory']}\n'{memory_text}'"],
                    )
                    formatted_memory = response.text.strip()

                    if ":" in formatted_memory:
                        key, value = formatted_memory.split(":", 1)
                        memory[key.strip()] = value.strip()
                        save_memory(memory)
                        console.print("Memory updated!", style="i Cyan")
                        # console.print(Markdown("**Got it! I'll remember that...**"))
                        # Generate AI response to confirm memory update
                        response = client.models.generate_content(
                            model=ai_model,
                            config=config,
                            contents=[prompt],
                        )
                        console.print("\n", Markdown(response.text), "\n")
                        break
        continue

    # Maintain short-term memory (keep last 5 messages)
    history.append(f"User: {prompt}")
    if len(history) > 5:
        history.pop(0)

    # Build memory context
    memory_context = "\n".join(f"{k}: {v}" for k, v in memory.items())

    # Check if the user is asking about themselves (e.g., "Who the fuck I am?")
    user_related_question = any(
        keyword in prompt.lower() for keyword in keywords["define_user"]
    )

    if user_related_question or any(key in prompt.lower() for key in memory.keys()):
        full_prompt = f"Long-term Memory:\n{memory_context}\n\nShort-term Memory (recent conversation):\n{history}\n\nUser: {prompt}"
    else:
        full_prompt = (
            f"Short-term Memory (recent conversation):\n{history}\n\nUser: {prompt}"
        )

    # Generate AI response
    response = client.models.generate_content(
        model=ai_model,
        config=config,
        contents=[full_prompt],
    )

    # Store AI response in short-term memory
    history.append(f"AI: {response.text.strip()}")
    if len(history) > 5:  # Keep only the last 5 messages
        history.pop(0)
    time_stamp = datetime.now(pytz.timezone("Asia/Dhaka")).isoformat(
        timespec="milliseconds"
    )
    console.print("\n", Markdown(response.text))
    chat_log(log_file, time_stamp, prompt, response.text)

"""
Maintain only the last 5 messages.

This approach limits the conversational history to reduce token usage,
ensuring that the context remains concise and that the AI response generation is efficient.
"""

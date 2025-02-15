import os
import json
import PIL
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
log_file = MK_File()


# Main interaction loop
while True:
    prompt = multiline_input()

    # Check if the user is asking for code execution or Google search and set the appropriate tool for the appropriate response
    if "/>" in prompt:
        tools = [types.Tool(code_execution=types.ToolCodeExecution())]
    else:
        tools = [
            types.Tool(
                google_search=types.GoogleSearchRetrieval(
                    dynamic_retrieval_config=types.DynamicRetrievalConfig(
                        dynamic_threshold=0.6
                    )
                )
            )
        ]

    config = types.GenerateContentConfig(
        system_instruction=sys_instruct
        + f'Current date/time: {datetime.now(pytz.timezone("Asia/Dhaka")).isoformat(timespec="milliseconds")}',
        temperature=0.7,
        tools=tools,
    )

    image = None
    media_audio = None

    if "$>" in prompt:
        try:
            media_path = extract_path(prompt)
            if media_path and media_path.lower().endswith(tuple(keywords["images"])):
                image = PIL.Image.open(media_path)
                console.print(
                    Markdown(f"**~Image: {media_path}**"), style="i medium_orchid3"
                )
            elif media_path and media_path.lower().endswith(tuple(keywords["audios"])):
                media_audio = client.files.upload(file=media_path)
                console.print(
                    Markdown(f"**~Audio: {media_path}**"), style="i medium_orchid3"
                )
            else:
                pass
        except Exception as e:
            pass

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

    # Maintain short-term memory (keep last 20 messages)
    history.append(f"User: {prompt}")
    if len(history) > 20:
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

    if image:
        content = [[full_prompt], image]
    elif media_audio:
        content = [[full_prompt], media_audio]
    else:
        content = [full_prompt]
    # Generate AI response
    response = client.models.generate_content(
        model=ai_model,
        config=config,
        contents=content,
    )

    # Extract executable code
    generated_code = None

    # Check if candidates exist
    if hasattr(response, "candidates") and response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                for part in candidate.content.parts:
                    if hasattr(part, "executable_code") and part.executable_code:
                        generated_code = part.executable_code.code
                        break  # Exit loop once we find the code

    # Execute the extracted code
    if generated_code:
        output = "```python" + "\n" + generated_code + "```"
        exec(generated_code)  # Execute the code
    else:
        output = response.text

    # Store AI response in short-term memory
    history.append(f"AI: {output}")
    if len(history) > 20:  # Keep only the last 20 messages
        history.pop(0)
    time_stamp = datetime.now(pytz.timezone("Asia/Dhaka")).isoformat(
        timespec="milliseconds"
    )
    console.print("\n", Markdown(output))
    chat_log(log_file, time_stamp, prompt, output)

"""
Maintain only the last 20 messages.

This approach limits the conversational history to reduce token usage,
ensuring that the context remains concise and that the AI response generation is efficient.
"""

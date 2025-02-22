"""
MK_File()
---------
Creates a YAML file in the "Data" directory with a unique timestamp and a secure random hash.
This function performs the following:
    - Ensures that the "Data" directory exists.
    - Generates a filename by combining the current timestamp (formatted to milliseconds) and a random hex token.
    - Writes initial content to the file including:
            • A "start" key with the timestamp.
            • A "Hash" key with a secure random hex value.
    - Closes the file and returns the file path.
Returns:
        str: The path to the newly created YAML file.


chat_log(file_name, time_stamp, user_input, output)
-----------------------------------------------------
Appends a formatted chat log entry to an existing YAML file.
Parameters:
        file_name (str): The path of the file where the chat log should be appended.
        time_stamp (str): The timestamp associated with the chat entry.
        user_input (str): The input provided by the user. Newline characters will be indented.
        output (str): The output response corresponding to the user's input. Newline characters will be indented.
Behavior:
        - Opens the specified file in append mode.
        - Writes the timestamp, user input, and output into the file each in dedicated sections.
        - Closes the file automatically after writing.
Returns:
        None
"""

import os
import pytz
import secrets
from datetime import datetime

__tab__ = " " * 4
time = datetime.now(pytz.timezone("Asia/Dhaka"))


def MK_File():
    os.makedirs("Data", exist_ok=True)
    file_name = f"Data/{time.strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]}_{secrets.token_hex(16)}.yaml"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"Start: {time.isoformat(timespec="milliseconds")}\n")
        file.write(f"Hash: {secrets.token_hex(64)}\n\n\n")

    file.close()

    return file_name


def chat_log(file_name, time_stamp, user_input, output):
    # Open file in append mode
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(f"{time_stamp}:\n")
        file.write(
            f"{__tab__}Input:{__tab__}|\n{__tab__*2}{user_input.replace('\n', f'\n{__tab__*2}')}\n"
        )
        file.write(
            f"{__tab__}Output:{__tab__}|\n{__tab__*2}{output.replace('\n', f'\n{__tab__*2}')}\n\n\n"
        )

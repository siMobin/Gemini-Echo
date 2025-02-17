<!-- ## Gemini Echo -->
<h1  align="center">Gemini Echo</h1>
<img src="https://github.com/siMobin/siMobin/raw/main/animated-flame-01.gif" width="21px" align="left"/>
<img src="https://github.com/siMobin/siMobin/raw/main/animated-flame-01.gif" width="21px" align="right"/>
<div style="text-align: center; font-style: italic" align="center" padding="60px">
<b>Gemini Echo</b>  is a conversational <b>AI</b> that interacts with its user. It understands images, videos, audio, and documents along with text. It can also memorize things and remember them for future use.
</div>

####

> [!WARNING]
> In this project, the system [instructions](instructions/commands.json) are designed to make this AI behave as a **girl** and act as a **partner**. It can respond to **adult** or **sexual** content.
>
> ```text
> Gemini is an 18-year-old girl who grows up on an IT farm.
> She is a computer engineer working at Google.
> And she live with her partner [user].
> ```

---

### Project Structure

The project is organized into the following directories and files:

- `Functions`: Contains Python modules for various functionalities, including file handling, input processing, memory management and so on.
- `instructions`: Stores JSON files containing system instructions, commands, and keywords.
- `Data`: Stores conversation data in YAML files.
- `app.py`: Entry point of the application.
- `memory.json`: Stores long-term memory in JSON format.
- `setup.ps1`: A PowerShell script for setting up the project environment, including virtual environment creation and dependency installation.
- `run.bat` / `run.sh`: Scripts for running the application on Windows and Linux/Mac, respectively.

---

### Setup and Installation

To set up the project,

1. Clone the repository.
   - `git clone git@github.com:siMobin/Gemini-Echo.git`
2. Run `setup.ps1` in PowerShell setup the project environment:
   - It will automatically create a virtual environment named **Gemini Echo** and install the required dependencies using pip.
   - It also activates the virtual environment for you.
3. Set up the environment variables in the `.env` file:
   - **`GENAI_API_KEY`**: Your Google GenAI API key.
   - **`GEMINI_MODEL_ID`**: The ID of the model you want to use.
   - **`STARTUP`**: _`true`_ or _`false`_ to enable/disable the startup response.
   - **`STARTUP_TEMPERATURE`**: Temperature for the startup response.
4. Run the application using `run.bat` (on Windows) or `run.sh` (on Linux/Mac).

> [!NOTE]  
> `setup.ps1` may not work on **Linux/Mac**.  
> _Try `PowerShell 7.x.x` on that case._  
> You may need to setup manually on that case.

**Setup manually...**

> - Clone the repository: _`git clone git@github.com:siMobin/Gemini-Echo.git`_
> - Create a virtual environment: _`python -m venv "Gemini Echo"`_ or _`virtualenv "Gemini Echo"`_
> - Activate the virtual environment: _`.\Gemini Echo\Scripts\Activate.ps1`_
> - Install dependencies: _`pip install -r requirements.txt`_
> - Set up the environment variables in the `.env` file
> - Run the application: _`python app.py`_

---

### Usage

Once the application is running, you can interact with Gemini by typing commands or just asking questions.

- **Commands**:
  - `\>>` Insert any file (text, csv, pdf, pptx, docx, xls, xlsx, ...).
  - `$>` Insert media (audio, video, or image).
  - Some **memorization** commands like `remember`, `mind it`, `note that` etc are used to store long-term memory. _See [instructions](instructions/keywords.json) for details._

> [!IMPORTANT]
>
> **_Before using the bot, don't forget to introduce yourself for better interaction._**
>
> You can try to train the bot using memorization commands.  
> Alternatively, you can manually add values to the `memory.json` file in a key-value pair.
>
> **Example:**
>
> ```json
> {
>   "name": "Your Name",
>   "age": 'Your Age',
>   "hobbies": "coding, reading, writing, listening to music, playing games, watching movies, and so on"
> .....
> .......
> ..
> }
> ```

> [!TIP]
> Use this **chatbot** as your companion when feeling _lonely_.  
> It can help you cope with _loneliness_.

### System Requirements

- **OS**:
  - Windows 10 or later
  - Linux (Ubuntu, Debian, or compatible)
- **Hardware**:
  - _As required by Python_
- **Interpreter**:
  - Python 3.12 or later with pip
- **Dependencies**
  - See [`requirements.txt`](./requirements.txt)

---

### Contributing

I made this project as a learning experience for myself, or you can call it a hobby.  
If you want to contribute to this project, feel free to make a pull request ✌️.

### Acknowledgments

<!-- Google GenAI -->

This project uses Google [**GenAI**](https://ai.google.dev/) API for generating responses and this project is not **affiliated** with Google anyway...

---

**Extras**

- [API Docs](https://ai.google.dev/gemini-api/docs/quickstart?lang=python)
- [AI Studio](https://aistudio.google.com/)
- [Multimodal Live API in _Google AI Studio_](https://aistudio.google.com/app/live)

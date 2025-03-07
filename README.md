<!-- ## Gemini Echo -->
<h1  align="center"><a href="https://github.com/siMobin/Gemini-Echo">Gemini Echo</a></h1>
<img src="https://github.com/siMobin/siMobin/raw/main/animated-flame-01.gif" width="21px" align="left"/>
<img src="https://github.com/siMobin/siMobin/raw/main/animated-flame-01.gif" width="21px" align="right"/>
<div style="text-align: center; font-style: italic" align="center" padding="60px">
<b>Gemini Echo</b> is a conversational AI chatbot that interacts with its user as a <a href="#usage">♀</a> partner <code>(system_instructions)</code>. It can understand and analyze text, images, videos, audio, and documents. Additionally, it has memorization capabilities, allowing it to retain and recall information for the future.
</div>

####

> [!WARNING]
> In this project, the system [instructions](instructions/commands.json) are designed to make this AI behave as a **girl** and act as a **partner**. It can respond to **adult** or **sexually explicit** content.
>
> ```text
> Gemini is an 18-year-old girl who grows up on an IT farm.
> She is a computer engineer working at Google.
> And she live with her partner [user].
> ```

---

**Table of Contents**

- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [System Requirements](#system-requirements)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

### Project Structure

The project is organized into the following directories and files:

- `Functions`: Contains Python modules for various functionalities, including file handling, input processing, memory management and so on.
- `instructions`: Stores JSON files containing system instructions, commands, and keywords.
- `Data`: Stores conversation data in YAML files.
- `templates`: HTML templates for the web interface.
- `static`: Static files & storage for the web interface.
- `app.py`, `web.py`: Entry points for the command line interface and web interface.

---

### Setup and Installation

To set up the project,

1. Clone the repository.
   - `git clone git@github.com:siMobin/Gemini-Echo.git`
2. Run `setup.ps1` in PowerShell(Windows) to setup the project environment:
   - It will automatically create a virtual environment named **Gemini Echo** and install the required dependencies using pip.
   - It also activates the virtual environment for you.
3. Set up the environment variables in the `.env` file:
   - **`GENAI_API_KEY`**: Your Google [GenAI API](https://ai.google.dev/gemini-api/docs/quickstart?lang=python) key.
   - **`GEMINI_MODEL_ID`**: [Model](https://aistudio.google.com/) you want to use.
   - **`WARM_AT_STARTUP`**: _`true`_ or _`false`_ to enable/disable the startup response.
   - **`STARTUP_TEMPERATURE`, `TEMPERATURE`**: _`(float - 0.0 to 2.0)`_ Higher values give _AI_ more freedom.
   - & others...
4. Run the application using-
   - `python app.py` - to run the command line interface
   - `python web.py` - to run the web interface

> [!NOTE]
> You may need to use `git lfs` to pull files from git LFS.
> _Run `git lfs install` and `git lfs pull` to pull files from git LFS._

**Setup manually...**

> - Clone the repository: _`git clone git@github.com:siMobin/Gemini-Echo.git`_
>   - Pull files from git LFS
>     - _`cd Gemini-Echo`_
>     - _`git lfs install`_
>     - _`git lfs pull`_
> - Create a virtual environment: _`python -m venv "Gemini Echo"`_ or _`virtualenv "Gemini Echo"`_
> - Activate the virtual environment: _`.\Gemini Echo\Scripts\Activate.ps1`\_\_(windows)_, _`source "Gemini Echo/bin/activate"`\_\_(linux)_
> - Install dependencies: _`pip install -r requirements.txt`_
> - Set up the environment variables in the `.env` file
> - Run the application: _`python app.py`_ or _`python web.py`_

<br>

> [!TIP]
> You can use Google _[`Project IDX`](https://idx.google.com/)_ to run it in a virtual workspace.
>
> **IDX Config FIle:** _[.idx/dev.nix](.idx/dev.nix)_

---

### Usage

Once the application is running, you can interact with Gemini by typing commands or just asking questions.

- **Commands**:
  - `/>>` _or_ `$>` _(console)_ Insert any file _(path - relative or absolute)_ into the conversation.
  - Some **memorization** commands like `remember`, `mind it`, `note that` etc are used to store long-term memory. _See [instructions](instructions/keywords.json) for details._
  - Some **farewells** like `exit`, `quit`, `bye`, `good bye` etc are used to end the conversation.
  - `shift + down` _(console)_ or `shift + enter` _(web)_ used for line break.
  - `enter` submits the input.

> [!IMPORTANT]
>
> **_Before using the bot, don't forget to introduce yourself for better interaction._**
>
> You can try to train the bot using memorization commands.  
> Alternatively, you can manually add values to the `memory.json` file in a key-value pair.
>
> **Example:**
>
> ````json
> {
>   "```json\n{\n  \"name\"": "\"John Doe\"\n}\n```",
>   "```json\n{\n  \"age\"": "\"25\"\n}\n```",
>   "```json\n{\n  \"brother\"": "\"John Eoe\"\n}\n```",
>   "```json\n{\n  \"likes\"": "\"Cricket\"\n}\n```",
>   "```json\n{\n  \"hobbies\"": "\"Coding, Sleeping\"\n}\n```"
> }
> ````

> [!TIP]
> Use this **chatbot** as your companion when feeling _lonely_.  
> It can help you cope with _loneliness_.

---

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
- **Additional Components**
  - Git LFS

---

### Contributing

I made this project as a learning experience for myself, or you can call it a hobby.  
If you want to contribute to this project, feel free to make a pull request ✌️.

### Acknowledgments

<!-- Google GenAI -->

This project uses Google [**GenAI**](https://ai.google.dev/) API for generating responses and this project is not **affiliated** with Google anyway...

---

**Extras**

- [GitHub/Python-GenAI](https://github.com/googleapis/python-genai)
- [API Docs](https://ai.google.dev/gemini-api/docs/quickstart?lang=python)
- [AI Studio](https://aistudio.google.com/)
- [Multimodal Live API in _Google AI Studio_](https://aistudio.google.com/app/live)
- [Project IDX](https://idx.google.com/)

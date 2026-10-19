# Mini AI Agent

A small Python command-line experiment that sends a question to a Groq-hosted
chat model and lets the model request a local Python function. The currently
connected function reports the machine's CPU usage.

## What is in the project

- `main.py` loads the API key from `.env`, creates the Groq client, sends a
  question with the available tool schema, and dispatches a requested tool
  through `TOOL_MAP`.
- `tools.py` implements `get_cpu_usage()` with `psutil` and describes that
  function in the schema sent to the model.
- `toolcolor.py` is a separate color-change tool example. It is not imported by
  `main.py` and does not currently change a graphical interface; it only returns
  a text message.
- `.env` stores local configuration such as the Groq API key. It should remain
  private and is excluded from Git by `.gitignore`.
- `venv/` is the local Python virtual environment and is also excluded from Git.

## How the current flow works

1. `main.py` calls `load_dotenv()` to load variables from `.env`.
2. It reads `GROQ_API_KEY` and initializes the Groq client.
3. It starts a conversation with the hard-coded question, “Tell me my server
   CPU capacity?”
4. It sends that conversation, the `TOOLS_SCHEMA` from `tools.py`, and
   `tool_choice="auto"` to the `openai/gpt-oss-20b` model through Groq.
5. If the response requests `get_cpu_usage`, `main.py` looks up that function
   in `TOOL_MAP` and runs it locally. `psutil.cpu_percent(interval=1)` samples
   CPU usage over one second.
6. The script adds the assistant tool-call message and tool result to the
   conversation, then makes another model request and prints its response.

The model does not measure CPU usage itself: it requests the tool, and the
Python process reads the local machine's CPU usage.

## Requirements

- Python 3.12 (the checked-in local environment was created with Python 3.12)
- A Groq API key
- The Python packages `groq`, `python-dotenv`, and `psutil`

## Setup on Windows (PowerShell)

Run these commands from the project folder:

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install groq python-dotenv psutil
```

If PowerShell blocks virtual-environment activation, use the environment's
Python directly instead:

```powershell
.\venv\Scripts\python.exe -m pip install groq python-dotenv psutil
```

Create or edit `.env` in the project folder and add your own key:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not put quotes around the value unless they are part of the key. Do not share
or commit this file.

## Run

With the virtual environment activated:

```powershell
python main.py
```

Or without activating it:

```powershell
.\venv\Scripts\python.exe main.py
```

The program prints whether it found an API key, any requested function and its
result, and the model's response. If you see
`ModuleNotFoundError: No module named 'dotenv'`, install `python-dotenv` into
the same Python environment used to run the program. The import name is
`dotenv`, while the package name to install is `python-dotenv`.

## Current limitations

- The question in `main.py` is hard-coded; there is no interactive prompt or
  command-line argument handling yet.
- The tool-call loop currently does not update its working model message or
  exit after producing a final answer. As a result, it can repeat the initial
  tool request instead of completing a single clean request/response cycle.
- The no-tool response path still accesses tool-call variables that are only
  set when a tool call exists. A response without a tool call can therefore
  fail.
- Only one tool call is handled per model response, and tool arguments are not
  parsed or passed to the selected function.
- `toolcolor.py` is not included in the tool registry used by `main.py`.
- Exceptions from the Groq request or tool handling are printed as `Error: ...`;
  the script does not currently provide retries or structured logging.

These are current implementation limitations, not setup steps. The CPU tool
works without arguments, but the conversation loop needs improvement for
reliable completion and for model responses that do not request a tool.

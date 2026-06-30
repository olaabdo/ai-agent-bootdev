# 🧠 AI Coding Agent

A toy implementation of a coding AI agent, similar to **Claude Code** or **Cursor**, built as part of the "Build an AI Agent" course on [Boot.dev](https://www.boot.dev).

This agent uses Google's **Gemini 2.5 Flash** API to read, write, and execute Python code autonomously based on user prompts.

---

## ✨ Features

- 📂 **List Files**: Scan directories and view file metadata (size, type).
- 📖 **Read Files**: Safely read file contents (limited to 10,000 characters).
- ✍️ **Write Files**: Create or overwrite files within the permitted working directory.
- ⚡ **Run Python**: Execute Python scripts with optional arguments (timeout: 30s).
- 🔁 **Agent Loop**: Automatically plans and executes multiple tool calls in sequence to complete complex tasks (e.g., fixing bugs).
- 🛡️ **Secure Scoping**: All operations are restricted to a specific `working_directory` to prevent accidental system file access.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- `uv` (Package manager)
- Google Gemini API Key ([Get one here](https://aistudio.google.com/apikey))

### Installation
1.  **Clone the repository**
    ```bash
    git clone https://github.com/olaabdo/ai-agent-bootdev.git
    cd ai-agent-bootdev

2.  Set up the environment & dependencies

bash
uv venv
source .venv/bin/activate
uv sync

3. Configure API Key
Create a .env file in the root directory and add your Gemini API key:

env
GEMINI_API_KEY="your-api-key-here"


Usage
Run the agent by passing a task as a command-line argument:

bash

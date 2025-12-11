# 🤖 AI Coding Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Gemini API](https://img.shields.io/badge/Powered%20by-Google%20Gemini-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An autonomous AI Agent capable of **reasoning, coding, and executing Python scripts** within a secure sandbox environment. Powered by Google's Gemini models, this agent can autonomously solve problems by writing and testing its own code.

---

## 📸 See it in action

Below is an example of the agent running in **verbose mode**. You can observe the **Reasoning Loop** as the model analyzes the request, plans the necessary steps, and executes the Python code.

<img width="100%" alt="AI Agent Demo" src="[https://github.com/user-attachments/assets/980946e3-2b72-401d-baeb-9776114584fc](https://github.com/user-attachments/assets/980946e3-2b72-401d-baeb-9776114584fc)" />

*(In this example, the agent autonomously writes a script, executes it, and verifies the output)*

---

## 🚀 Features

* **🧠 Reasoning Loop:** Uses a "Thought → Plan → Action" cycle to break down complex tasks.
* **🛠️ Tool Use:** Can list files, read content, write code, and execute Python scripts.
* **🔒 Sandboxed Execution:** All code execution is restricted to the `./calculator` directory to prevent system-wide modifications.
* **⚡ Powered by `uv`:** Blazing fast dependency management.

## 📂 Project Structure

```text
AI-AGENT/
├── main.py              # The brain: Agent loop and API communication
├── prompts.py           # System instructions (Persona)
├── config.py            # Configuration settings
├── functions/           # Tool definitions
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/          # 🛡️ SANDBOX: The agent only works here
│   ├── main.py          # Custom Calculator Tool
│   ├── pkg/             # Helper packages
│   └── tests.py         # Unit tests
└── .env                 # API Keys (Not included in repo)
```

## 🛠️ Installation & Setup

This project is built using **[uv](https://github.com/astral-sh/uv)** for modern Python package management.

### 1. Clone the repository
```bash
git clone https://github.com/zagos09/ai-coding-agent.git
cd ai-coding-agent
```

### 2. Set up environment

**Using `uv` (Recommended):**
```bash
uv sync
```

**Using standard `pip` (Alternative):**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install google-genai python-dotenv
```

### 3. Configure API Key
Create a `.env` file in the root directory and add your Google Gemini API key:
```ini
GEMINI_API_KEY=your_api_key_here
```

## 💻 Usage

Run the agent by describing what you want it to do.

**Basic Example:**
```bash
python main.py "Create a Python script that calculates the Fibonacci sequence"
```

**Verbose Mode (See the thinking process):**
```bash
python main.py "Analyze the files in the pkg folder and tell me what they do" --verbose
```

## 🛡️ Security Note

This agent allows an AI model to **execute code** on your machine.
* **Sandbox:** Execution is limited to the `calculator/` directory by default.
* **Review:** Always review the code the agent writes if you are using this in a production environment.

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)

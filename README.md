# 🤖 AI Coding Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Gemini API](https://img.shields.io/badge/Powered%20by-Google%20Gemini-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An autonomous AI Agent capable of **reasoning, coding, and executing Python scripts** within a secure sandbox environment. Powered by Google's Gemini models, this agent can autonomously solve problems by writing and testing its own code.

---

## 📸 See it in action

Below is an example of the agent running in **verbose mode**. You can observe the **Reasoning Loop** as the model analyzes the request, plans the necessary steps, and executes the Python code.

![alt text](ai-agentt-1.png)

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
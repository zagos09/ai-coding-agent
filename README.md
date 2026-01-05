# AI Coding Agent

An intelligent, autonomous development assistant designed to bridge the gap between high-level logic and functional code execution. This agent leverages advanced LLMs to analyze requirements and generate structured code solutions efficiently.

## Motivation
Most AI assistants are confined to simple chat interfaces, requiring manual copy-pasting and context management. I built the **AI Coding Agent** because I wanted to create a tool that moves beyond conversation and focuses on autonomous task execution. By integrating AI reasoning directly with a Python-based execution engine, this project demonstrates how we can automate complex development workflows and reduce the time spent on repetitive coding tasks.

## Quick Start

### 1. Clone the repository
```bash
git clone [https://github.com/zagos09/ai-coding-agent.git](https://github.com/zagos09/ai-coding-agent.git)
cd ai-coding-agent
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up your API Key
Create a .env file in the root directory and add your key:
```bash
OPENAI_API_KEY=your_key_here
```

4. Run the Agent
```bash
python main.py
```

Usage
The AI Coding Agent can be customized to handle different development scenarios.

Basic Prompting: Run the script and describe the feature you want to build.

Verbose Mode: Use the --verbose flag to see the agent's internal reasoning and step-by-step logic.

Model Selection: Choose between different models (e.g., GPT-4o or GPT-3.5) by editing the configuration file.

Example:
```bash
python main.py --task "Create a Python script that scrapes weather data"
```

Contributing
Contributions are welcome to make this agent even more capable!

Fork the project.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

Note: Ensure all tests pass by running pytest before submitting a contribution.

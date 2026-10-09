# JARVIS Agent System

A JARVIS-inspired multi-agent task coordinator with 100 specialized agents, web dashboard, local session management, and production-ready deployment options.

## Features

✨ **100 Autonomous Agents** — Specialized in 15+ roles (planning, coding, testing, security, docs, research, monitoring, deployment, etc.)

🎯 **Intent-Based Routing** — Automatically selects the best agents for your command

📊 **Web Dashboard** — Real-time command center with agent monitoring and session tracking

💾 **Local Session Management** — All commands, executions, and agent assignments are logged and persisted

🔐 **Private Repository** — Keep your agent system and all data private

🚀 **Multiple Interfaces** — CLI, Python API, and Flask web dashboard

## Quick Start

### Option 1: CLI Mode

```bash
python3 main.py
```

Example commands:
- `analyze the repository`
- `write documentation for this project`
- `debug the login bug`
- `run the test suite`
- `plan a release`
- `monitor system health`
- `dashboard` (launch web UI)

### Option 2: Web Dashboard

```bash
pip install -r requirements.txt
python3 dashboard.py
```

Then open **http://localhost:5000** in your browser.

### Option 3: Python API

```python
from jarvis.coordinator import JARVISCoordinator
from jarvis.session import SessionManager

coordinator = JARVISCoordinator()
session = SessionManager()

result = coordinator.handle("debug the login bug")
session.log_command("debug the login bug", "debugging", ["JARVIS-001"], result)

print(result)
```

## Project Structure

```
jarvis-agent-system/
├── main.py                 # CLI entrypoint
├── dashboard.py            # Web dashboard entrypoint
├── jarvis/
│   ├── __init__.py        # Agent generation & definitions
│   ├── agents.py          # Agent class & role templates
│   ├── router.py          # Command parsing & routing
│   ├── coordinator.py     # Agent orchestration
│   ├── session.py         # Session management & persistence
│   └── dashboard.py       # Flask web application
├── .sessions/             # Local session storage (git-ignored)
├── requirements.txt       # Python dependencies
└── README.md
```

## Sessions

All sessions are stored in `.sessions/` directory (not tracked in git). Each session includes:

- Session ID (UUID)
- Created timestamp
- Command history with intents and agent assignments
- Status (active/completed)
- Agent participation log

View sessions in the CLI:
```bash
JARVIS> sessions
```

## Dashboard Features

- 📊 **Real-time stats** — Total sessions, active sessions, completed sessions, total commands
- 🤖 **Agent listing** — Browse all 100 agents with roles and specializations
- 📋 **Session management** — View active and completed sessions
- 📝 **Command history** — Track all executed commands
- 📡 **Live command execution** — Execute commands and see responses in real-time
- 🔄 **Auto-refresh** — Dashboard updates every 5 seconds

## Deployment

### Private GitHub Repository Setup

1. This repo is already created as private. To make it even more private:

```bash
# Clone locally
git clone https://github.com/lsamdancioglu-beep/jarvis-agent-system.git
cd jarvis-agent-system

# Create .env for sensitive data
echo "SECRET_KEY=your-secret-key" > .env

# Push to your private repo
git remote set-url origin https://github.com/YOUR-USERNAME/jarvis-agent-system.git
git push -u origin main
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "dashboard.py"]
```

```bash
docker build -t jarvis-agent-system .
docker run -p 5000:5000 -v jarvis-data:/app/.sessions jarvis-agent-system
```

### Kubernetes Deployment (Optional)

See `k8s/` directory for deployment manifests.

## Agent Categories

- **Planning** (Agents 001, 016, 031, ...) — Roadmaps, strategies, estimates
- **Coding** (Agents 002, 017, 032, ...) — Implementation, features, builds
- **Testing** (Agents 003, 018, 033, ...) — QA, validation, test automation
- **Security** (Agents 004, 019, 034, ...) — Scanning, audits, vulnerabilities
- **Documentation** (Agents 005, 020, 035, ...) — Writing, README, API docs
- **Research** (Agents 006, 021, 036, ...) — Investigation, exploration, analysis
- **Monitoring** (Agents 008, 023, 038, ...) — Health checks, alerts, observability
- **Deployment** (Agents 009, 024, 039, ...) — Releases, shipping, publishing
- And 7 more specialized roles...

## License

MIT

## Support

For issues, feature requests, or contributions:

1. Open an issue on the repo
2. Create a pull request with changes
3. Review session logs in `.sessions/` for debugging

---

**JARVIS Agent System** — Intelligent, distributed, autonomous. 🤖

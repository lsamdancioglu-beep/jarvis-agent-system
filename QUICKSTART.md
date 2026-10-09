# JARVIS Agent System - Quick Start Guide

## Installation

### 1. Clone or download the repository

```bash
git clone https://github.com/lsamdancioglu-beep/jarvis-agent-system.git
cd jarvis-agent-system
```

### 2. Run Setup (Automatic)

**On macOS/Linux:**
```bash
bash setup.sh
```

**On Windows:**
```bash
setup.bat
```

**Manual Setup (all platforms):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running JARVIS

### Option 1: Quick Start Menu

```bash
python3 quickstart.py
```

Then choose:
- **[1]** for CLI Mode
- **[2]** for Web Dashboard

### Option 2: CLI Mode (Interactive)

```bash
python3 main.py
```

**Example Commands:**
```
JARVIS> agents
JARVIS> sessions
JARVIS> analyze the repository
JARVIS> debug the login bug
JARVIS> run the test suite
JARVIS> write documentation for this project
JARVIS> plan a release
JARVIS> dashboard
JARVIS> exit
```

### Option 3: Web Dashboard

```bash
python3 dashboard.py
```

Then open your browser to: **http://localhost:5000**

**Dashboard Features:**
- 🔴 Real-time stats (100 active agents, commands executed, tasks completed)
- 🤖 Agent listing with performance metrics
- 📋 Session management (Active/Completed filters)
- 📝 Command history
- ⚡ Live command execution
- 🔄 Auto-refresh every 3 seconds

## System Architecture

```
JARVIS-agent-system/
├── main.py                    # CLI entry point
├── dashboard.py               # Web dashboard entry point
├── quickstart.py              # Quick start menu
├── jarvis/
│   ├── __init__.py           # Agent generator (100 agents)
│   ├── agents.py             # Agent class definitions
│   ├── router.py             # Command parsing & routing
│   ├── coordinator.py        # Agent orchestration & execution
│   ├── session.py            # Session management & persistence
│   └── dashboard.py          # Flask web application
├── .sessions/                # Local session storage (git-ignored)
├── requirements.txt          # Python dependencies
├── setup.sh / setup.bat      # Setup scripts
└── README.md
```

## Features Overview

### 100 Specialized Agents

Each agent has:
- **ID & Name**: Unique identifier (e.g., agent-001, JARVIS-001)
- **Role**: planning, coding, testing, security, documentation, research, monitoring, deployment, etc.
- **Specialization**: 20+ areas (backend, frontend, database, security scanning, API design, etc.)
- **Capabilities**: 4-6 skills per agent (analysis, testing, debugging, automation, etc.)
- **Performance**: Completed task count, success rate, priority level

### Intelligent Routing

When you run a command:
1. System detects intent (analyze, debug, code, test, deploy, etc.)
2. Extracts keywords from your command
3. Scores all 100 agents by:
   - Role match (strongest signal)
   - Capability match
   - Specialization relevance
   - Experience (completed tasks)
   - Success rate
4. Selects top 5 agents
5. Simulates execution and logs results

### Session Management

- Every interaction is logged to `.sessions/` directory
- Sessions track:
  - Timestamp
  - Commands executed
  - Agents assigned
  - Task completion counts
  - Session status (active/completed)

## Example Workflow

### CLI Example

```bash
$ python3 main.py

JARVIS Agent System ready.
Session ID: a1b2c3d4-e5f6-7890-1234-567890abcdef
Type 'exit' to quit, 'sessions' to list history, 'agents' to list all agents.

JARVIS> analyze the repository

🎯 Command: analyze the repository
📊 Intent Detected: analysis
🤖 Selected Agents: JARVIS-001, JARVIS-016, JARVIS-031, JARVIS-046, JARVIS-061
⚡ Combined Tasks Completed: 1250
⚡ Status: Command matched workflow and assigned optimal candidates.

[JARVIS-001] PLANNING / backend systems
Intent: analysis
Capabilities Active: analysis, planning, monitoring
Status: ACTIVE | Tasks Completed: 298
Success Rate: 97%
Execution: Running analysis, testing, debugging modules...
Result: ✓ SUCCESS (1.23s)
Action: Routing request through backend systems workflow for next phase.

[JARVIS-016] CODING / frontend experience
Intent: analysis
Capabilities Active: implementation, testing, debugging
Status: ACTIVE | Tasks Completed: 276
Success Rate: 94%
Execution: Checking agent frontend experience database...
Result: ✓ SUCCESS (0.87s)
Action: Routing request through frontend experience workflow for next phase.

... (3 more agents) ...

JARVIS> sessions

1 session(s) found:

  ● a1b2c3d4... | 2026-10-09T13:05:12.345678 | 1 commands | active

JARVIS> exit
Goodbye. Session saved.
```

### Web Dashboard Example

Open **http://localhost:5000** to see:

- **Stats Cards**: 100 Active Agents | Hundreds of Commands | Thousands of Tasks | 95%+ Success Rate
- **Command Interface**: Type a command and execute instantly
- **Agent List**: Browse all 100 agents with task counts and success rates
- **Sessions Panel**: View active and completed sessions with filters
- **Command History**: Track all executed commands with intents and agent assignments

## Troubleshooting

### Python 3 not found
```bash
# Install Python 3.8+
# On macOS: brew install python3
# On Windows: Download from python.org
# On Linux: sudo apt-get install python3
```

### Port 5000 already in use
```bash
# Edit dashboard.py and change the port
# Change: run_dashboard(host="0.0.0.0", port=5000, debug=True)
# To:     run_dashboard(host="0.0.0.0", port=5001, debug=True)
```

### Permission denied on setup.sh
```bash
chmod +x setup.sh
bash setup.sh
```

## Next Steps

Choose your next upgrade:

- **"smarter agents"** — Add memory, learning, adaptive behavior
- **"better dashboard"** — Add charts, agent graphs, live streaming
- **"deployment ready"** — Docker, Kubernetes, production configs
- **"real API + auth"** — Full REST API with authentication

## License

MIT

---

**JARVIS Agent System** — 100 autonomous agents at your command. 🚀

# JARVIS Agent System

A JARVIS-inspired multi-agent task coordinator with 100 specialized agents.

## Features

- 100 generated agents with distinct roles and specialties
- Intent-based command routing
- Agent selection for planning, coding, testing, docs, security, deployment, monitoring, and research
- CLI and Python API for interacting with the system
- Local simulation environment without external dependencies

## Quick start

```bash
python3 main.py
```

### Example commands

- `analyze the repository`
- `write documentation for this project`
- `debug the login bug`
- `run the test suite`
- `plan a release`
- `monitor system health`
- `create a security check`
- `summarize current work`

## Project structure

- `main.py` - CLI entrypoint
- `jarvis/agents.py` - agent generation and definitions
- `jarvis/router.py` - command parsing and routing logic
- `jarvis/coordinator.py` - agent orchestration and response assembly
- `agents.json` - export of generated agents

## Running a command programmatically

```python
from jarvis.coordinator import JARVISCoordinator

coordinator = JARVISCoordinator()
result = coordinator.handle("debug the login bug")
print(result)
```

## License

MIT

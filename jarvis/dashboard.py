from __future__ import annotations

from flask import Flask, render_template_string, jsonify, request
from pathlib import Path
import json

from jarvis.coordinator import JARVISCoordinator
from jarvis.session import SessionManager


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
coordinator = JARVISCoordinator()


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS Agent Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 20px;
        }
        h1 {
            font-size: 2.5rem;
            color: #00d4ff;
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
            margin-bottom: 10px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .stat-card {
            background: rgba(0, 212, 255, 0.1);
            border: 1px solid #00d4ff;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }
        .stat-value { font-size: 2rem; color: #00d4ff; font-weight: bold; }
        .stat-label { font-size: 0.9rem; color: #a0a0a0; margin-top: 5px; }
        .section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 30px 0;
        }
        .panel {
            background: rgba(48, 43, 99, 0.6);
            border: 1px solid #00d4ff;
            border-radius: 8px;
            padding: 20px;
        }
        .panel h2 {
            color: #00d4ff;
            margin-bottom: 20px;
            border-bottom: 1px solid #00d4ff;
            padding-bottom: 10px;
        }
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input[type="text"] {
            flex: 1;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid #00d4ff;
            color: #e0e0e0;
            padding: 10px;
            border-radius: 4px;
            font-size: 1rem;
        }
        button {
            background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
        }
        .agent-list, .session-list, .command-log {
            max-height: 400px;
            overflow-y: auto;
        }
        .agent-item, .session-item, .command-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 12px;
            margin-bottom: 10px;
            border-left: 3px solid #00d4ff;
            border-radius: 4px;
        }
        .agent-name { font-weight: bold; color: #00d4ff; }
        .agent-role { font-size: 0.9rem; color: #a0a0a0; }
        .session-status {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .status-active { background: rgba(0, 255, 0, 0.3); color: #00ff00; }
        .status-completed { background: rgba(0, 212, 255, 0.3); color: #00d4ff; }
        .response-box {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid #00d4ff;
            border-radius: 4px;
            padding: 15px;
            margin-top: 15px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 300px;
            overflow-y: auto;
        }
        .loading { color: #00d4ff; font-style: italic; }
        .error { color: #ff4444; }
        .success { color: #00ff00; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚙️ JARVIS Agent Command Center</h1>
            <p>100-Agent Coordinator System</p>
        </header>

        <div class="stats" id="stats"></div>

        <div class="section">
            <div class="panel">
                <h2>📡 Command Interface</h2>
                <div class="input-group">
                    <input type="text" id="commandInput" placeholder="Enter a command (e.g., 'analyze the repository')">
                    <button onclick="executeCommand()">Execute</button>
                </div>
                <div id="commandResponse" class="response-box" style="display:none;"></div>
            </div>

            <div class="panel">
                <h2>🤖 All Agents (100)</h2>
                <div class="agent-list" id="agentList"></div>
            </div>
        </div>

        <div class="section">
            <div class="panel">
                <h2>📋 Sessions</h2>
                <div class="session-list" id="sessionList"></div>
            </div>

            <div class="panel">
                <h2>📝 Command History</h2>
                <div class="command-log" id="commandLog"></div>
            </div>
        </div>
    </div>

    <script>
        async function loadStats() {
            const res = await fetch('/api/stats');
            const data = await res.json();
            const html = `
                <div class="stat-card">
                    <div class="stat-value">${data.total_sessions}</div>
                    <div class="stat-label">Total Sessions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.active_sessions}</div>
                    <div class="stat-label">Active Sessions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.completed_sessions}</div>
                    <div class="stat-label">Completed Sessions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.total_commands}</div>
                    <div class="stat-label">Total Commands</div>
                </div>
            `;
            document.getElementById('stats').innerHTML = html;
        }

        async function loadAgents() {
            const res = await fetch('/api/agents');
            const agents = await res.json();
            let html = '';
            agents.slice(0, 20).forEach(agent => {
                html += `
                    <div class="agent-item">
                        <div class="agent-name">${agent.name}</div>
                        <div class="agent-role">${agent.role} • ${agent.specialization}</div>
                    </div>
                `;
            });
            if (agents.length > 20) {
                html += `<div class="agent-item"><em>... and ${agents.length - 20} more agents</em></div>`;
            }
            document.getElementById('agentList').innerHTML = html;
        }

        async function loadSessions() {
            const res = await fetch('/api/sessions');
            const sessions = await res.json();
            let html = '';
            sessions.forEach(session => {
                const status = session.status === 'active' ? 'status-active' : 'status-completed';
                html += `
                    <div class="session-item">
                        <div>
                            <strong>${session.session_id.substring(0, 8)}...</strong>
                            <span class="session-status ${status}">${session.status.toUpperCase()}</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #a0a0a0; margin-top: 5px;">
                            ${session.command_count} commands • ${new Date(session.created_at).toLocaleString()}
                        </div>
                    </div>
                `;
            });
            if (sessions.length === 0) {
                html = '<div class="session-item"><em>No sessions yet</em></div>';
            }
            document.getElementById('sessionList').innerHTML = html;
        }

        async function loadCommandLog() {
            const res = await fetch('/api/sessions');
            const sessions = await res.json();
            let html = '';
            sessions.forEach(session => {
                session.commands.forEach(cmd => {
                    html += `
                        <div class="command-item">
                            <div><strong>${cmd.command}</strong></div>
                            <div style="font-size: 0.8rem; color: #a0a0a0;">
                                Intent: ${cmd.intent} • Agents: ${cmd.agents.length}
                            </div>
                        </div>
                    `;
                });
            });
            if (html === '') {
                html = '<div class="command-item"><em>No commands executed yet</em></div>';
            }
            document.getElementById('commandLog').innerHTML = html;
        }

        async function executeCommand() {
            const input = document.getElementById('commandInput');
            const command = input.value.trim();
            if (!command) return;

            const responseDiv = document.getElementById('commandResponse');
            responseDiv.textContent = 'Processing...';
            responseDiv.style.display = 'block';
            responseDiv.className = 'response-box loading';

            try {
                const res = await fetch('/api/command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command })
                });
                const data = await res.json();
                responseDiv.textContent = data.response;
                responseDiv.className = 'response-box success';
            } catch (error) {
                responseDiv.textContent = `Error: ${error.message}`;
                responseDiv.className = 'response-box error';
            }

            input.value = '';
            await Promise.all([
                loadSessions(),
                loadCommandLog(),
                loadStats()
            ]);
        }

        document.getElementById('commandInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') executeCommand();
        });

        // Initial load
        async function init() {
            await Promise.all([
                loadStats(),
                loadAgents(),
                loadSessions(),
                loadCommandLog()
            ]);
            setInterval(() => {
                loadStats();
                loadSessions();
                loadCommandLog();
            }, 5000);
        }

        init();
    </script>
</body>
</html>
"""


@app.route("/")
def dashboard():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/agents")
def api_agents():
    agents = coordinator.list_agents()
    return jsonify(agents)


@app.route("/api/sessions")
def api_sessions():
    sessions = SessionManager.list_sessions()
    return jsonify(sessions)


@app.route("/api/stats")
def api_stats():
    stats = SessionManager.get_stats()
    return jsonify(stats)


@app.route("/api/command", methods=["POST"])
def api_command():
    data = request.json
    command = data.get("command", "")
    if not command:
        return jsonify({"error": "No command provided"}), 400

    session = SessionManager()
    result = coordinator.handle(command)
    parsed = coordinator.router.parse_command(command)
    selected_agents = coordinator.router.route(command)
    agent_names = [agent.name for agent in selected_agents]
    session.log_command(command, parsed["intent"], agent_names, result)

    return jsonify({"response": result, "session_id": session.current_session_id})


def run_dashboard(host="127.0.0.1", port=5000, debug=True):
    print(f"🚀 JARVIS Dashboard running at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_dashboard()

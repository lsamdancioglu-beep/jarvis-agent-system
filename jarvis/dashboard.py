from __future__ import annotations

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
from pathlib import Path
import json

from jarvis.coordinator import JARVISCoordinator
from jarvis.session import SessionManager


app = Flask(__name__)
CORS(app)
app.config["JSON_SORT_KEYS"] = False
coordinator = JARVISCoordinator()


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS Agent Command Center</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1600px; margin: 0 auto; }
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
            border: 2px solid #00d4ff;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
        }
        .stat-card:hover {
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
            transform: translateY(-5px);
        }
        .stat-value { font-size: 2.5rem; color: #00ff00; font-weight: bold; }
        .stat-label { font-size: 0.9rem; color: #a0a0a0; margin-top: 5px; }
        .section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 30px 0;
        }
        @media (max-width: 1200px) {
            .section { grid-template-columns: 1fr; }
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
            font-size: 1.3rem;
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
            padding: 12px;
            border-radius: 4px;
            font-size: 1rem;
        }
        input[type="text"]:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        }
        button {
            background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
            color: #000;
            border: none;
            padding: 12px 24px;
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
            max-height: 450px;
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
        .agent-role { font-size: 0.85rem; color: #a0a0a0; margin-top: 3px; }
        .agent-stats { font-size: 0.8rem; color: #00ff00; margin-top: 5px; }
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
            font-size: 0.85rem;
            white-space: pre-wrap;
            word-wrap: break-word;
            max-height: 400px;
            overflow-y: auto;
        }
        .loading { color: #00d4ff; font-style: italic; }
        .error { color: #ff6666; }
        .success { color: #00ff00; }
        .filter-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .filter-btn {
            padding: 8px 16px;
            border: 1px solid #00d4ff;
            background: rgba(0, 212, 255, 0.2);
            color: #00d4ff;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .filter-btn.active {
            background: rgba(0, 212, 255, 0.5);
            color: #fff;
        }
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 212, 255, 0.1);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(0, 212, 255, 0.5);
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚙️ JARVIS Agent Command Center</h1>
            <p>100-Agent Coordinator | Real-Time Session Management</p>
        </header>

        <div class="stats" id="stats"></div>

        <div class="section">
            <div class="panel">
                <h2>📡 Command Interface</h2>
                <div class="input-group">
                    <input type="text" id="commandInput" placeholder="Enter a command (e.g., 'analyze the repository', 'debug the login bug')">
                    <button onclick="executeCommand()">Execute</button>
                </div>
                <div id="commandResponse" class="response-box" style="display:none;"></div>
            </div>

            <div class="panel">
                <h2>🤖 All Agents (100 Active)</h2>
                <div class="agent-list" id="agentList"></div>
            </div>
        </div>

        <div class="section">
            <div class="panel">
                <h2>📋 Sessions</h2>
                <div class="filter-buttons">
                    <button class="filter-btn active" onclick="filterSessions('all')">All</button>
                    <button class="filter-btn" onclick="filterSessions('active')">Active</button>
                    <button class="filter-btn" onclick="filterSessions('completed')">Completed</button>
                </div>
                <div class="session-list" id="sessionList"></div>
            </div>

            <div class="panel">
                <h2>📝 Command History</h2>
                <div class="command-log" id="commandLog"></div>
            </div>
        </div>
    </div>

    <script>
        let currentFilter = 'all';

        async function loadStats() {
            const res = await fetch('/api/stats');
            const data = await res.json();
            const agentStats = await fetch('/api/agent-stats').then(r => r.json());
            const html = `
                <div class="stat-card">
                    <div class="stat-value">100</div>
                    <div class="stat-label">Active Agents</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.total_commands}</div>
                    <div class="stat-label">Commands Executed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.total_tasks_executed}</div>
                    <div class="stat-label">Tasks Completed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.total_sessions}</div>
                    <div class="stat-label">Total Sessions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${agentStats.average_success_rate.toFixed(1)}%</div>
                    <div class="stat-label">Avg Success Rate</div>
                </div>
            `;
            document.getElementById('stats').innerHTML = html;
        }

        async function loadAgents() {
            const res = await fetch('/api/agents');
            const agents = await res.json();
            let html = '';
            agents.slice(0, 15).forEach(agent => {
                html += `
                    <div class="agent-item">
                        <div class="agent-name">${agent.name} [${agent.id}]</div>
                        <div class="agent-role">${agent.role} • ${agent.specialization}</div>
                        <div class="agent-stats">Tasks: ${agent.completed_tasks} | Success: ${(agent.success_rate * 100).toFixed(0)}%</div>
                    </div>
                `;
            });
            if (agents.length > 15) {
                html += `<div class="agent-item"><em style="color: #00d4ff;">... and ${agents.length - 15} more agents</em></div>`;
            }
            document.getElementById('agentList').innerHTML = html;
        }

        async function loadSessions(filter = 'all') {
            const res = await fetch('/api/sessions');
            const sessions = await res.json();
            let filtered = sessions;
            if (filter === 'active') {
                filtered = sessions.filter(s => s.status === 'active');
            } else if (filter === 'completed') {
                filtered = sessions.filter(s => s.status === 'completed');
            }
            let html = '';
            filtered.slice(0, 20).forEach(session => {
                const status = session.status === 'active' ? 'status-active' : 'status-completed';
                const icon = session.status === 'active' ? '●' : '○';
                html += `
                    <div class="session-item">
                        <div>
                            ${icon} <strong>${session.session_id.substring(0, 8)}...</strong>
                            <span class="session-status ${status}">${session.status.toUpperCase()}</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #a0a0a0; margin-top: 5px;">
                            ${session.command_count} commands • ${session.total_tasks_completed} tasks • ${new Date(session.created_at).toLocaleString()}
                        </div>
                    </div>
                `;
            });
            if (filtered.length === 0) {
                html = '<div class="session-item"><em>No sessions found</em></div>';
            }
            document.getElementById('sessionList').innerHTML = html;
        }

        async function loadCommandLog() {
            const res = await fetch('/api/sessions');
            const sessions = await res.json();
            let html = '';
            let cmdCount = 0;
            for (const session of sessions) {
                for (const cmd of session.commands) {
                    if (cmdCount >= 25) break;
                    html += `
                        <div class="command-item">
                            <div><strong>${cmd.command}</strong></div>
                            <div style="font-size: 0.8rem; color: #a0a0a0;">
                                Intent: <span style="color: #00d4ff;">${cmd.intent}</span> | Agents: ${cmd.agents.length} | ${new Date(cmd.timestamp).toLocaleTimeString()}
                            </div>
                        </div>
                    `;
                    cmdCount++;
                }
                if (cmdCount >= 25) break;
            }
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
            responseDiv.textContent = '📋 Processing your command...';
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
                responseDiv.textContent = `⚠ Error: ${error.message}`;
                responseDiv.className = 'response-box error';
            }

            input.value = '';
            await Promise.all([
                loadSessions(currentFilter),
                loadCommandLog(),
                loadStats()
            ]);
        }

        function filterSessions(filter) {
            currentFilter = filter;
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            loadSessions(filter);
        }

        document.getElementById('commandInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') executeCommand();
        });

        // Initial load
        async function init() {
            await Promise.all([
                loadStats(),
                loadAgents(),
                loadSessions(currentFilter),
                loadCommandLog()
            ]);
            setInterval(() => {
                loadStats();
                loadSessions(currentFilter);
                loadCommandLog();
            }, 3000);
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
    sessions = SessionManager.list_sessions(limit=100)
    return jsonify(sessions)


@app.route("/api/stats")
def api_stats():
    stats = SessionManager.get_stats()
    return jsonify(stats)


@app.route("/api/agent-stats")
def api_agent_stats():
    stats = coordinator.get_agent_stats()
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
    print(f"📊 100 Active Agents ready for deployment")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_dashboard()

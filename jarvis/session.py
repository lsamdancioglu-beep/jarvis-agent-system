from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


class SessionManager:
    """Manages JARVIS session logging and persistence."""

    def __init__(self, session_dir: str = ".sessions"):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        self.current_session_id = str(uuid.uuid4())
        self.session_file = self.session_dir / f"{self.current_session_id}.json"
        self.session_data: Dict[str, Any] = {
            "session_id": self.current_session_id,
            "created_at": datetime.utcnow().isoformat(),
            "commands": [],
            "agents_assigned": [],
            "status": "active",
            "command_count": 0,
        }
        self._save_session()

    def log_command(
        self,
        command: str,
        intent: str,
        selected_agents: List[str],
        response: str,
    ) -> None:
        """Log a command execution to the current session."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "command": command,
            "intent": intent,
            "agents": selected_agents,
            "response_summary": response[:200],
        }
        self.session_data["commands"].append(entry)
        self.session_data["command_count"] = len(self.session_data["commands"])
        if selected_agents:
            for agent in selected_agents:
                if agent not in self.session_data["agents_assigned"]:
                    self.session_data["agents_assigned"].append(agent)
        self._save_session()

    def _save_session(self) -> None:
        """Persist session data to disk."""
        with open(self.session_file, "w") as f:
            json.dump(self.session_data, f, indent=2)

    def close_session(self) -> None:
        """Mark session as completed."""
        self.session_data["status"] = "completed"
        self.session_data["closed_at"] = datetime.utcnow().isoformat()
        self._save_session()

    @staticmethod
    def list_sessions(status: str | None = None) -> List[Dict[str, Any]]:
        """List all saved sessions, optionally filtered by status."""
        session_dir = Path(".sessions")
        if not session_dir.exists():
            return []
        sessions = []
        for session_file in sorted(session_dir.glob("*.json"), reverse=True):
            with open(session_file) as f:
                session = json.load(f)
                if status is None or session.get("status") == status:
                    sessions.append(session)
        return sessions

    @staticmethod
    def get_session(session_id: str) -> Dict[str, Any] | None:
        """Retrieve a specific session."""
        session_file = Path(".sessions") / f"{session_id}.json"
        if not session_file.exists():
            return None
        with open(session_file) as f:
            return json.load(f)

    @staticmethod
    def get_stats() -> Dict[str, Any]:
        """Get session statistics."""
        all_sessions = SessionManager.list_sessions()
        active = [s for s in all_sessions if s["status"] == "active"]
        completed = [s for s in all_sessions if s["status"] == "completed"]
        total_commands = sum(s["command_count"] for s in all_sessions)
        
        return {
            "total_sessions": len(all_sessions),
            "active_sessions": len(active),
            "completed_sessions": len(completed),
            "total_commands": total_commands,
        }

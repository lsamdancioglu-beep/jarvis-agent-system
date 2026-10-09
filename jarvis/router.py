from __future__ import annotations

import json
from typing import List, Dict, Any

from jarvis.agents import Agent, generate_agents


class AgentRouter:
    """Routes incoming commands to the best matching agent(s)."""

    def __init__(self, agents: List[Agent] | None = None):
        self.agents = agents or generate_agents()

    def parse_command(self, command: str) -> Dict[str, Any]:
        text = command.strip().lower()
        intent = self._detect_intent(text)
        keywords = self._extract_keywords(text)
        return {"text": command.strip(), "intent": intent, "keywords": keywords}

    @staticmethod
    def _detect_intent(text: str) -> str:
        intents = {
            "analysis": ["analyze", "review", "inspect", "assess", "summarize"],
            "coding": ["code", "implement", "build", "develop", "feature"],
            "testing": ["test", "verify", "validate", "qa", "check"],
            "debugging": ["debug", "fix", "error", "issue", "crash"],
            "documentation": ["doc", "document", "readme", "writeup"],
            "security": ["security", "vuln", "scan", "risk", "audit"],
            "deployment": ["deploy", "release", "ship", "publish"],
            "monitoring": ["monitor", "health", "status", "watch", "alerts"],
            "research": ["research", "investigate", "explore", "find"],
            "planning": ["plan", "roadmap", "strategy", "estimate"],
            "operations": ["ops", "maintain", "manage", "infrastructure"],
        }

        for intent, phrases in intents.items():
            if any(phrase in text for phrase in phrases):
                return intent
        return "general"

    @staticmethod
    def _extract_keywords(text: str) -> List[str]:
        stopwords = {
            "the", "a", "an", "to", "for", "of", "and", "or", "in", "on", "with", "this", "that"
        }
        return [token for token in text.replace("?", " ").split() if token not in stopwords]

    def route(self, command: str) -> List[Agent]:
        parsed = self.parse_command(command)
        intent = parsed["intent"]
        keywords = parsed["keywords"]

        candidates = [agent for agent in self.agents if agent.role == intent or intent in agent.capabilities]
        if not candidates:
            candidates = sorted(self.agents, key=lambda agent: agent.priority)

        scored = []
        for agent in candidates:
            score = 0
            if agent.role == intent:
                score += 10
            if intent in agent.capabilities:
                score += 6
            for keyword in keywords:
                if keyword in agent.specialization or keyword in agent.capabilities:
                    score += 3
            score += agent.completed_tasks // 50  # Bonus for experienced agents
            score += int(agent.success_rate * 10)  # Bonus for high success rate
            scored.append((agent, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        ranked = [agent for agent, _ in scored[:5]]
        if not ranked:
            ranked = sorted(self.agents, key=lambda a: a.priority)[:3]
        return ranked

    def export_json(self) -> str:
        payload = {"agents": [agent.to_dict() for agent in self.agents]}
        return json.dumps(payload, indent=2)

from __future__ import annotations

from typing import List, Dict, Any

from jarvis.agents import Agent, get_agents
from jarvis.router import AgentRouter


class JARVISCoordinator:
    """Coordinates agent selection and response assembly."""

    def __init__(self, agents: List[Agent] | None = None):
        self.agents = agents or get_agents()
        self.router = AgentRouter(self.agents)

    def handle(self, command: str) -> str:
        parsed_command = self.router.parse_command(command)
        selected_agents = self.router.route(command)

        responses = [
            self._build_agent_response(agent, parsed_command)
            for agent in selected_agents
        ]
        summary = self._compose_summary(selected_agents, parsed_command)
        return "\n\n".join([summary, *responses])

    def _build_agent_response(self, agent: Agent, parsed: Dict[str, Any]) -> str:
        return (
            f"[{agent.name}] {agent.role} / {agent.specialization}\n"
            f"Intent: {parsed['intent']}\n"
            f"Focus: {', '.join(agent.capabilities[:3])}\n"
            f"Status: {agent.status}\n"
            f"Action: I am routing this request through the {agent.specialization} workflow and preparing the next operational step."
        )

    @staticmethod
    def _compose_summary(selected_agents: List[Agent], parsed: Dict[str, Any]) -> str:
        agent_names = ", ".join(agent.name for agent in selected_agents)
        return (
            f"Command: {parsed['text']}\n"
            f"Intent: {parsed['intent']}\n"
            f"Selected agents: {agent_names}\n"
            f"Routing: command matched the relevant workflow and assigned the best candidates for execution."
        )

    def list_agents(self) -> List[Dict[str, Any]]:
        return [agent.to_dict() for agent in self.agents]

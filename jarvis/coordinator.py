from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Any
import json
import random

from jarvis.agents import Agent, get_agents
from jarvis.router import AgentRouter


class JARVISCoordinator:
    """Coordinates agent selection and response assembly with execution simulation."""

    def __init__(self, agents: List[Agent] | None = None):
        self.agents = agents or get_agents()
        self.router = AgentRouter(self.agents)
        self.execution_log: List[Dict[str, Any]] = []

    def handle(self, command: str) -> str:
        parsed_command = self.router.parse_command(command)
        selected_agents = self.router.route(command)

        # Simulate agent execution
        execution_results = []
        for agent in selected_agents:
            result = self._simulate_agent_execution(agent, parsed_command)
            execution_results.append(result)
            agent.completed_tasks += 1

        summary = self._compose_summary(selected_agents, parsed_command)
        execution_details = "\n\n".join(execution_results)
        
        return f"{summary}\n\n{execution_details}"

    def _simulate_agent_execution(self, agent: Agent, parsed: Dict[str, Any]) -> str:
        """Simulate realistic agent execution."""
        execution_time = round(random.uniform(0.1, 2.5), 2)
        success = random.random() < agent.success_rate
        status = "✓ SUCCESS" if success else "⚠ PARTIAL"
        
        actions = [
            f"Analyzing {parsed['intent']} context...",
            f"Checking agent {agent.specialization} database...",
            f"Running {', '.join(agent.capabilities[:2])} modules...",
            f"Executing workflow for {agent.role} role...",
            f"Compiling results from {agent.name}...",
        ]
        
        return (
            f"[{agent.name}] {agent.role.upper()} / {agent.specialization}\n"
            f"Intent: {parsed['intent']}\n"
            f"Capabilities Active: {', '.join(agent.capabilities[:3])}\n"
            f"Status: {agent.status.upper()} | Tasks Completed: {agent.completed_tasks}\n"
            f"Success Rate: {agent.success_rate * 100:.0f}%\n"
            f"Execution: {random.choice(actions)}\n"
            f"Result: {status} ({execution_time}s)\n"
            f"Action: Routing request through {agent.specialization} workflow for next phase."
        )

    @staticmethod
    def _compose_summary(selected_agents: List[Agent], parsed: Dict[str, Any]) -> str:
        agent_names = ", ".join(agent.name for agent in selected_agents)
        total_tasks = sum(agent.completed_tasks for agent in selected_agents)
        return (
            f"🎯 Command: {parsed['text']}\n"
            f"📊 Intent Detected: {parsed['intent']}\n"
            f"🤖 Selected Agents: {agent_names}\n"
            f"📈 Combined Tasks Completed: {total_tasks}\n"
            f"⚡ Status: Command matched workflow and assigned optimal candidates."
        )

    def list_agents(self) -> List[Dict[str, Any]]:
        return [agent.to_dict() for agent in self.agents]

    def get_agent_stats(self) -> Dict[str, Any]:
        """Get comprehensive agent statistics."""
        total_tasks = sum(agent.completed_tasks for agent in self.agents)
        avg_success_rate = sum(agent.success_rate for agent in self.agents) / len(self.agents)
        active_agents = len([a for a in self.agents if a.status == "active"])
        
        return {
            "total_agents": len(self.agents),
            "active_agents": active_agents,
            "total_tasks_completed": total_tasks,
            "average_success_rate": round(avg_success_rate, 3),
            "agents_by_role": self._group_agents_by_role(),
        }

    def _group_agents_by_role(self) -> Dict[str, int]:
        """Group agents by their role."""
        roles = {}
        for agent in self.agents:
            roles[agent.role] = roles.get(agent.role, 0) + 1
        return roles

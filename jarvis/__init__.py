from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class Agent:
    id: str
    name: str
    role: str
    specialization: str
    capabilities: List[str]
    status: str = "active"
    priority: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


ROLE_TEMPLATES = [
    "planning",
    "coding",
    "testing",
    "security",
    "documentation",
    "research",
    "research",
    "monitoring",
    "deployment",
    "analysis",
    "operations",
    "communication",
    "support",
    "quality",
    "architecture",
]

SPECIALIZATION_POOL = [
    "backend systems",
    "frontend experience",
    "database reliability",
    "performance tuning",
    "container orchestration",
    "security scanning",
    "test automation",
    "API design",
    "observability",
    "incident response",
    "documentation quality",
    "feature planning",
    "release coordination",
    "data analysis",
    "customer support",
    "system architecture",
    "code review",
    "automation workflows",
    "dependency management",
    "platform operations",
]

CAPABILITY_POOL = [
    "analysis",
    "planning",
    "monitoring",
    "implementation",
    "testing",
    "reporting",
    "debugging",
    "automation",
    "communication",
    "documentation",
    "optimization",
    "security",
    "deployment",
    "research",
]


def generate_agents() -> List[Agent]:
    agents: List[Agent] = []
    for index in range(1, 101):
        role = ROLE_TEMPLATES[(index - 1) % len(ROLE_TEMPLATES)]
        specialization = SPECIALIZATION_POOL[(index - 1) % len(SPECIALIZATION_POOL)]
        capability_count = min(4 + (index % 3), len(CAPABILITY_POOL))
        capabilities = [
            CAPABILITY_POOL[(index + offset) % len(CAPABILITY_POOL)]
            for offset in range(capability_count)
        ]
        # ensure unique-ish capabilities
        seen = set()
        ordered = []
        for capability in capabilities:
            if capability not in seen:
                seen.add(capability)
                ordered.append(capability)
        id_value = f"agent-{index:03d}"
        agents.append(
            Agent(
                id=id_value,
                name=f"JARVIS-{index:03d}",
                role=role,
                specialization=specialization,
                capabilities=ordered,
                status="active",
                priority=(index % 5) + 1,
            )
        )
    return agents


AGENTS = generate_agents()


def get_agents() -> List[Agent]:
    return AGENTS


def export_agents_json() -> List[Dict[str, Any]]:
    return [agent.to_dict() for agent in AGENTS]

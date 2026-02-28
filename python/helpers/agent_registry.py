import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class AgentCapabilities:
    allowed_tools: List[str] = field(default_factory=list)
    max_delegation_depth: int = 1
    max_tokens: int = 10000
    max_tool_calls: int = 10
    refusal_rules: List[str] = field(default_factory=list)

@dataclass
class AgentDefinition:
    profile: str
    scope: str
    capabilities: AgentCapabilities
    completion_definition: str

class AgentRegistry:
    _instance = None

    def __init__(self):
        self.agents = {
            "default": AgentDefinition(
                profile="default",
                scope="General assistance and system orchestration",
                capabilities=AgentCapabilities(
                    allowed_tools=["*"],
                    max_delegation_depth=2,
                    max_tokens=50000,
                    max_tool_calls=20
                ),
                completion_definition="Final answer provided or task goal achieved"
            ),
            "researcher": AgentDefinition(
                profile="researcher",
                scope="Information gathering and synthesis",
                capabilities=AgentCapabilities(
                    allowed_tools=["search", "browser", "read_file"],
                    max_delegation_depth=0,
                    max_tokens=20000,
                    max_tool_calls=15
                ),
                completion_definition="Summary of research findings returned"
            ),
            "developer": AgentDefinition(
                profile="developer",
                scope="Coding and technical implementation",
                capabilities=AgentCapabilities(
                    allowed_tools=["code_exe", "read_file", "write_file"],
                    max_delegation_depth=0,
                    max_tokens=30000,
                    max_tool_calls=15
                ),
                completion_definition="Code implemented and verified"
            )
        }

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_agent_definition(self, profile: str) -> AgentDefinition:
        return self.agents.get(profile, self.agents["default"])

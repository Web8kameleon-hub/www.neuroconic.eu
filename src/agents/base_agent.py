"""
Base Agent - parent class for all agents
"""
import time
import hashlib
from typing import Any, Dict, Optional


class BaseAgent:
    """Base class for all agents in the system"""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.agent_id = hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:16]
        self.tasks_processed = 0
        self.active = False

    def start(self):
        """Start the agent"""
        self.active = True
        print(f"[AGENT] {self.name} ({self.role}) started")

    def stop(self):
        """Stop the agent"""
        self.active = False
        print(f"[AGENT] {self.name} stopped")

    def process(self, task: Any) -> Dict[str, Any]:
        """Process a task - must be implemented by subclasses"""
        raise RuntimeError(f"{self.__class__.__name__}.process must be overridden")

    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "active": self.active,
            "tasks_processed": self.tasks_processed,
        }

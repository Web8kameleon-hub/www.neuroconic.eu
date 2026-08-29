"""
Tide Engine - Controls system rhythm based on load
"""
import time
from typing import List, Dict


class TideEngine:
    """Tide Engine - Batica/Zbatica (high/low load)"""

    def __init__(self):
        self.state = "low"  # low, medium, high, critical
        self.level = 0.0  # 0.0 - 1.0
        self.history: List[Dict] = []

    def update(self, load: float):
        """Update tide level based on system load"""
        self.level = min(1.0, max(0.0, load / 100.0))

        # Determine state
        new_state = "low"
        if self.level >= 0.85:
            new_state = "critical"
        elif self.level >= 0.60:
            new_state = "high"
        elif self.level >= 0.30:
            new_state = "medium"

        if new_state != self.state:
            print(f"[TIDE] {self.state.upper()} -> {new_state.upper()} ({self.level * 100:.1f}%)")
            self.state = new_state

        # Record history
        self.history.append({
            "time": time.time(),
            "level": self.level,
            "state": self.state,
        })

        # Keep only last 1000 entries
        if len(self.history) > 1000:
            self.history = self.history[-1000:]

    def get_delay(self) -> float:
        """Get adaptive delay based on tide state"""
        delays = {
            "low": 0.001,
            "medium": 0.01,
            "high": 0.05,
            "critical": 0.1,
        }
        return delays.get(self.state, 0.01)

    def get_stats(self) -> Dict:
        """Get tide statistics"""
        return {
            "state": self.state,
            "level": self.level,
            "history_length": len(self.history),
        }

"""
Security Agent - detects threats and anomalies
"""
import time
from typing import Any, Dict
from .base_agent import BaseAgent


class SecurityAgent(BaseAgent):
    """Agent for security monitoring and threat detection"""

    def __init__(self):
        super().__init__("SecurityAgent", "Security")
        self.threats_detected = 0

    def process(self, task: Any) -> Dict[str, Any]:
        """Analyze event for security threats"""
        event = task if isinstance(task, dict) else {"data": str(task)}
        
        # Check for common attack patterns
        is_threat = False
        threat_type = "none"
        data_str = str(event).upper()
        
        if "DROP TABLE" in data_str or "DELETE FROM" in data_str:
            is_threat = True
            threat_type = "sql_injection"
        elif "../" in str(event):
            is_threat = True
            threat_type = "path_traversal"
        
        if is_threat:
            self.threats_detected += 1
        
        result = {
            "agent": self.name,
            "is_threat": is_threat,
            "threat_type": threat_type,
            "action": "blocked" if is_threat else "allowed",
            "timestamp": time.time(),
        }
        
        self.tasks_processed += 1
        return result

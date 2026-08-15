"""
Metrics Collector - system performance metrics
"""
import time
from typing import Dict, List


class MetricsCollector:
    """Collects and stores system metrics"""

    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.start_time = time.time()

    def record(self, name: str, value: float):
        """Record a metric"""
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append(value)
        
        # Keep only last 1000 values
        if len(self.metrics[name]) > 1000:
            self.metrics[name] = self.metrics[name][-1000:]

    def get_average(self, name: str, last_n: int = 10) -> float:
        """Get average of last N values"""
        if name not in self.metrics or not self.metrics[name]:
            return 0.0
        
        values = self.metrics[name][-last_n:]
        return sum(values) / len(values)

    def get_stats(self) -> Dict:
        """Get all metrics statistics"""
        return {
            "metrics_count": len(self.metrics),
            "uptime": time.time() - self.start_time,
            "averages": {k: self.get_average(k) for k in self.metrics},
        }

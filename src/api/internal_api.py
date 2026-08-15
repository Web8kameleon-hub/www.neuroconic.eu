"""
Internal API - for inter-module communication
"""
import time
from typing import Dict, Any, Callable


class InternalAPI:
    """Internal API for module communication"""

    def __init__(self):
        self.routes: Dict[str, Callable] = {}
        self.call_count = 0

    def register(self, path: str, handler: Callable):
        """Register a route"""
        self.routes[path] = handler
        print(f"[API] Registered route: {path}")

    def call(self, path: str, params: Dict = None) -> Dict[str, Any]:
        """Call an API route"""
        if params is None:
            params = {}

        self.call_count += 1

        if path in self.routes:
            try:
                result = self.routes[path](params)
                return {
                    "success": True,
                    "data": result,
                    "path": path,
                    "timestamp": time.time(),
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "path": path,
                    "timestamp": time.time(),
                }
        else:
            return {
                "success": False,
                "error": f"Route '{path}' not found",
                "path": path,
                "timestamp": time.time(),
            }

    def get_routes(self) -> list:
        """List all registered routes"""
        return list(self.routes.keys())

    def get_stats(self) -> Dict:
        """Get API statistics"""
        return {
            "total_routes": len(self.routes),
            "total_calls": self.call_count,
        }

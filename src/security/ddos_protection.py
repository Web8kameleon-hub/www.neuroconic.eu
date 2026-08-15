"""
DDoS Protection - Rate limiting and IP blacklist
"""
import time
from typing import Dict, List, Set


class DDoSProtection:
    """DDoS protection with rate limiting"""

    def __init__(self, rate_limit: int = 100):
        self.rate_limit = rate_limit  # requests per minute
        self.blacklist: Set[str] = set()
        self.request_log: Dict[str, List[float]] = {}

    def check_request(self, ip: str) -> bool:
        """Check if request from IP is allowed"""
        now = time.time()

        # Blocked IPs
        if ip in self.blacklist:
            return False

        # Initialize log for new IP
        if ip not in self.request_log:
            self.request_log[ip] = []

        # Clean old requests (older than 60 seconds)
        self.request_log[ip] = [t for t in self.request_log[ip] if now - t < 60]

        # Add current request
        self.request_log[ip].append(now)

        # Check rate limit
        if len(self.request_log[ip]) > self.rate_limit:
            self.blacklist.add(ip)
            print(f"[DDOS] IP {ip} blocked - {len(self.request_log[ip])} req/min")
            return False

        return True

    def whitelist_ip(self, ip: str):
        """Remove IP from blacklist"""
        if ip in self.blacklist:
            self.blacklist.remove(ip)

    def get_stats(self) -> Dict:
        """Get protection statistics"""
        return {
            "blacklist_size": len(self.blacklist),
            "active_ips": len(self.request_log),
            "total_requests": sum(len(v) for v in self.request_log.values()),
        }

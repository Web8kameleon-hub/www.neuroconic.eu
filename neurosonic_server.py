#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC HTTP SERVER - Zero Dependencies Version
Simple HTTP server using only Python stdlib (http.server)
Alternative to FastAPI backend
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Import core modules
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from neurosonic import NeurosonicKernel, Constitution


class NeurosonicHTTPHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for Neurosonic"""

    kernel = None  # Will be set when server starts

    def _send_json(self, data: dict, status: int = 200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path

        if path == "/" or path == "/api/health":
            self._send_json({
                "name": "Neurosonic Trinity+ASI",
                "version": "1.0.0",
                "status": "online",
                "timestamp": time.time(),
            })

        elif path == "/api/status":
            self._send_json(self.kernel.status())

        elif path == "/api/constitution":
            self._send_json({
                "laws": Constitution.get_all(),
                "total": len(Constitution.get_all()),
            })

        elif path == "/api/memory/stats":
            self._send_json(self.kernel.memory.stats())

        else:
            self._send_json({"error": "Not Found"}, 404)

    def do_POST(self):
        """Handle POST requests"""
        path = urlparse(self.path).path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, 400)
            return

        if path == "/api/memory/store":
            key = data.get("key")
            value = data.get("value")
            mem_type = data.get("type", "working")
            self.kernel.memory.store(key, value, mem_type)
            self._send_json({"success": True, "key": key})

        elif path == "/api/memory/recall":
            key = data.get("key")
            mem_type = data.get("type", "working")
            value = self.kernel.memory.recall(key, mem_type)
            self._send_json({"key": key, "value": value})

        elif path == "/api/auth/login":
            username = data.get("username")
            password = data.get("password")
            token = self.kernel.auth.login(username, password)
            if token:
                self._send_json({"success": True, "token": token})
            else:
                self._send_json({"error": "Invalid credentials"}, 401)

        else:
            self._send_json({"error": "Not Found"}, 404)

    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[HTTP] {self.address_string()} - {format % args}")


def run_server(host: str = "0.0.0.0", port: int = 8765):
    """Run the HTTP server"""
    
    print("=" * 60)
    print("  NEUROSONIC HTTP SERVER (Zero Dependencies)")
    print("  Using Python stdlib only - no FastAPI required")
    print("=" * 60)
    
    # Initialize kernel
    kernel = NeurosonicKernel()
    kernel.run()
    NeurosonicHTTPHandler.kernel = kernel
    
    # Start server
    server = HTTPServer((host, port), NeurosonicHTTPHandler)
    print(f"\n[SERVER] Listening on http://{host}:{port}")
    print(f"[SERVER] Endpoints:")
    print(f"  GET  /api/health - Health check")
    print(f"  GET  /api/status - System status")
    print(f"  GET  /api/constitution - Constitution laws")
    print(f"  GET  /api/memory/stats - Memory statistics")
    print(f"  POST /api/memory/store - Store in memory")
    print(f"  POST /api/memory/recall - Recall from memory")
    print(f"  POST /api/auth/login - Login")
    print(f"\n[SERVER] Press Ctrl+C to stop\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
        kernel.shutdown()
        server.shutdown()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Neurosonic HTTP Server (Zero Dependencies)")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind to")
    args = parser.parse_args()
    
    run_server(args.host, args.port)

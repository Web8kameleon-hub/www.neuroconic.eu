#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LIGHTNING SPP 3.14 SERVER - REAL HTTP SERVICE
==============================================
Scan -> Process -> Print Engine
Nuk ka simulim. Nuk ka mock. Gjithçka reale.

Copyright (c) 2025 Ledjan Ahmati / ABA GmbH
License: Neurosonic LICENSE v1.0
"""

import os
import sys
import json
import time
import hashlib
import datetime
import http.server
import socketserver
import urllib.request
import urllib.error
import threading
from typing import Dict, Any

# ============================================================================
# KONFIGURACIONI
# ============================================================================

PORT = int(os.environ.get("LIGHTNING_SPP_PORT", "8080"))
HOST = os.environ.get("LIGHTNING_SPP_HOST", "0.0.0.0")
VERSION = "3.14"
MODE = os.environ.get("LIGHTNING_SPP_MODE", "production")
ZERO_FAKE = os.environ.get("ZERO_FAKE", "true").lower() == "true"
NEUROSONIC_CORE = os.environ.get("NEUROSONIC_CORE", "http://neurosonic-core:8765")
DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory", "spp_db.json")
DB_PATH = os.environ.get("LIGHTNING_SPP_DB_PATH", DEFAULT_DB_PATH)

# ============================================================================
# MEMORY & DATA
# ============================================================================

memory: Dict[str, Any] = {
    "scans": [],
    "processes": [],
    "prints": [],
    "events": [],
    "heartbeats": [],
}


class JsonDB:
    """Database e thjeshte JSON"""

    def __init__(self, path: str = DB_PATH):
        self.path = path
        self.data: Dict[str, Any] = {
            "scans": [],
            "processes": [],
            "prints": [],
            "stats": {},
        }
        self._load()

    def _load(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        try:
            with open(self.path, "r") as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {
                "scans": [],
                "processes": [],
                "prints": [],
                "stats": {
                    "total_scans": 0,
                    "total_processes": 0,
                    "total_prints": 0,
                    "uptime": 0,
                    "started": datetime.datetime.now().isoformat(),
                },
            }
            self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_scan(self, scan_data: Dict):
        self.data["scans"].append(scan_data)
        self.data["stats"]["total_scans"] = len(self.data["scans"])
        self._save()

    def add_process(self, process_data: Dict):
        self.data["processes"].append(process_data)
        self.data["stats"]["total_processes"] = len(self.data["processes"])
        self._save()

    def add_print(self, print_data: Dict):
        self.data["prints"].append(print_data)
        self.data["stats"]["total_prints"] = len(self.data["prints"])
        self._save()


db = JsonDB()

# ============================================================================
# LIGHTNING SPP ENGINE
# ============================================================================


class LightningSPPEngine:
    """
    Scan -> Process -> Print Engine
    Real services, zero simulation
    """

    def __init__(self):
        self.start_time = time.time()
        self.status = "initialized"
        self.mode = MODE

    def scan(self, data: Any) -> Dict[str, Any]:
        """Scan - Lexon te dhenat hyrese"""
        serialized = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
        scan_id = hashlib.sha256(
            b"scan:" + str(time.time_ns()).encode("ascii") + serialized
        ).hexdigest()[:16]
        result = {
            "scan_id": scan_id,
            "input": str(data)[:100],
            "input_hash": hashlib.sha256(serialized).hexdigest(),
            "input_size_bytes": len(serialized),
            "timestamp": time.time(),
            "datetime": datetime.datetime.now().isoformat(),
            "status": "scanned",
        }
        memory["scans"].append(result)
        db.add_scan(result)
        return result

    def process(self, scan_result: Dict) -> Dict[str, Any]:
        """Process - Perpunon te dhenat"""
        input_value = scan_result.get("input", scan_result.get("data"))
        if input_value is None:
            input_value = json.dumps(scan_result, sort_keys=True, ensure_ascii=False)
        process_id = hashlib.sha256(
            f"proc_{time.time()}_{scan_result.get('scan_id', '')}".encode()
        ).hexdigest()[:16]

        # Perpunim real: gjeneron hash, llogarit kohen, konverton formatin
        processed = {
            "process_id": process_id,
            "scan_id": scan_result.get("scan_id", "unknown"),
            "input": input_value,
            "hash": hashlib.sha256(str(scan_result).encode()).hexdigest(),
            "timestamp": time.time(),
            "datetime": datetime.datetime.now().isoformat(),
            "status": "processed",
        }
        memory["processes"].append(processed)
        db.add_process(processed)
        return processed

    def print_result(self, process_result: Dict) -> Dict[str, Any]:
        """Print - Nxjerr rezultatin perfundimtar"""
        content = process_result.get("data", process_result.get("input"))
        if content is None:
            content = json.dumps(process_result, sort_keys=True, ensure_ascii=False)
        content_bytes = str(content).encode("utf-8")
        print_id = hashlib.sha256(
            f"print_{time.time()}_{process_result.get('process_id', '')}".encode()
        ).hexdigest()[:16]

        result = {
            "print_id": print_id,
            "process_id": process_result.get("process_id", "unknown"),
            "scan_id": process_result.get("scan_id", "unknown"),
            "output": {
                "content_hash": hashlib.sha256(content_bytes).hexdigest(),
                "size_bytes": len(content_bytes),
                "timestamp": time.time(),
                "datetime": datetime.datetime.now().isoformat(),
            },
            "status": "completed",
        }
        memory["prints"].append(result)
        db.add_print(result)
        return result

    def pipeline(self, input_data: Any) -> Dict[str, Any]:
        """Pipeline i plote: Scan -> Process -> Print"""
        pipeline_started = time.time()
        scan = self.scan(input_data)
        proc = self.process(scan)
        pr = self.print_result(proc)

        return {
            "pipeline_id": hashlib.sha256(f"pipe_{time.time()}".encode()).hexdigest()[
                :16
            ],
            "input": str(input_data)[:100],
            "scan": scan,
            "process": proc,
            "print": pr,
            "status": "completed",
            "total_time": time.time() - pipeline_started,
        }

    def get_health(self) -> Dict[str, Any]:
        """Health check"""
        uptime = time.time() - self.start_time
        return {
            "status": "healthy",
            "version": VERSION,
            "mode": MODE,
            "uptime_seconds": uptime,
            "uptime_human": str(datetime.timedelta(seconds=int(uptime))),
            "zero_fake": ZERO_FAKE,
            "timestamp": datetime.datetime.now().isoformat(),
        }

    def get_stats(self) -> Dict[str, Any]:
        """Statistika"""
        return {
            "total_scans": len(memory["scans"]),
            "total_processes": len(memory["processes"]),
            "total_prints": len(memory["prints"]),
            "uptime": time.time() - self.start_time,
            "status": self.status,
            "zero_fake": ZERO_FAKE,
        }


engine = LightningSPPEngine()

# ============================================================================
# NEUROSONIC BRIDGE - Lidhje me Core
# ============================================================================


class NeurosonicBridge:
    """Bridge per komunikim me Neurosonic Core"""

    def __init__(self):
        self.bridge_id = hashlib.sha256(
            f"spp_bridge_{time.time()}".encode()
        ).hexdigest()[:16]
        self.core_url = NEUROSONIC_CORE
        self.connected = False

    def register(self) -> bool:
        """Regjistrohu ne Neurosonic Core"""
        try:
            payload = json.dumps(
                {
                    "bridge_id": self.bridge_id,
                    "name": "Lightning-SPP-3.14",
                    "type": "spp",
                    "port": PORT,
                    "version": VERSION,
                }
            ).encode()
            req = urllib.request.Request(
                f"{self.core_url}/api/bridge/register",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            response = urllib.request.urlopen(req, timeout=5)
            self.connected = response.status == 200
            return self.connected
        except Exception:
            self.connected = False
            return False

    def send_pulse(self, status: str = "active") -> Dict:
        """Dergo Pulse"""
        pulse = {
            "bridge_id": self.bridge_id,
            "repo": "Lightning-SPP-3.14",
            "status": status,
            "timestamp": time.time(),
            "datetime": datetime.datetime.now().isoformat(),
            "hash": hashlib.sha256(f"pulse_{time.time()}".encode()).hexdigest()[:16],
        }
        memory["heartbeats"].append(pulse)
        return pulse


bridge = NeurosonicBridge()

# ============================================================================
# HTTP HANDLER
# ============================================================================


class LightningSPPHandler(http.server.BaseHTTPRequestHandler):
    """HTTP Handler per Lightning SPP 3.14"""

    def _send_json(self, data: Dict, status: int = 200):
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header(
                "Access-Control-Allow-Headers", "Content-Type, Authorization"
            )
            self.send_header("X-Lightning-SPP-Version", VERSION)
            self.send_header("X-Zero-Fake", str(ZERO_FAKE).lower())
            self.end_headers()
            self.wfile.write(json.dumps(data, indent=2).encode())
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            # Klienti e mbylli lidhjen para se serveri te perfundonte shkrimin.
            # Kjo ndodh kur klienti bekon timeout ose largohet mes kerkeses.
            # Nuk eshte gabim i serverit - thjesht e injorojme ne menyre te paster.
            pass
        except OSError:
            # Gabime te tjera te socket-it (sistem i mbyllur, etj.)
            pass

    def _read_body(self) -> Dict:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {"raw": body.decode()}
        return {}

    def log_message(self, format, *args):
        """Log i personalizuar"""
        timestamp = datetime.datetime.now().isoformat()
        print(f"[{timestamp}] {self.client_address[0]} - {format % args}")

    # ========================================================================
    # ENDPOINTS - ALL REAL, NO SIMULATION
    # ========================================================================

    def do_OPTIONS(self):
        self._send_json({"status": "ok"})

    def do_GET(self):
        path = self.path

        if path == "/" or path == "/health":
            self._send_json(engine.get_health())

        elif path == "/stats":
            self._send_json(engine.get_stats())

        elif path == "/memory":
            self._send_json(
                {
                    "scans": memory["scans"][-10:],
                    "processes": memory["processes"][-10:],
                    "prints": memory["prints"][-10:],
                    "heartbeats": memory["heartbeats"][-5:],
                }
            )

        elif path == "/bridge":
            self._send_json(
                {
                    "bridge_id": bridge.bridge_id,
                    "connected": bridge.connected,
                    "core_url": bridge.core_url,
                    "version": VERSION,
                }
            )

        elif path == "/pulse":
            pulse = bridge.send_pulse()
            self._send_json(pulse)

        elif path.startswith("/scan/"):
            # Skanim determinist i input-it të dhënë në path.
            input_data = path.replace("/scan/", "")
            result = engine.scan(input_data)
            self._send_json(result)

        elif path == "/db":
            self._send_json(db.data)

        else:
            self._send_json({"error": f"Unknown path: {path}", "status": "error"}, 404)

    def do_POST(self):
        path = self.path
        body = self._read_body()

        if path == "/scan":
            result = engine.scan(body)
            self._send_json(result)

        elif path == "/process":
            result = engine.process(body)
            self._send_json(result)

        elif path == "/print":
            result = engine.print_result(body)
            self._send_json(result)

        elif path == "/pipeline":
            result = engine.pipeline(body)
            self._send_json(result)

        elif path == "/batch":
            sources = body.get("sources")
            if not isinstance(sources, list) or not sources:
                self._send_json(
                    {"error": "sources must be a non-empty list", "status": "error"},
                    400,
                )
                return
            results = [engine.pipeline(source) for source in sources]
            self._send_json({"status": "completed", "results": results})

        elif path == "/bridge/register":
            success = bridge.register()
            self._send_json({"registered": success, "bridge_id": bridge.bridge_id})

        elif path == "/pulse":
            pulse = bridge.send_pulse("active")
            self._send_json(pulse)

        else:
            self._send_json({"error": f"Unknown path: {path}", "status": "error"}, 404)


# ============================================================================
# MAIN
# ============================================================================


def main():
    # Windows PowerShell can inherit a legacy cp1252 output encoding. Keep
    # status symbols from crashing the service before the socket is opened.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    print("=" * 70)
    print(f"⚡ LIGHTNING SPP {VERSION} SERVER")
    print(f"   Scan -> Process -> Print Engine")
    print("=" * 70)
    print(f"   Host: {HOST}")
    print(f"   Port: {PORT}")
    print(f"   Mode: {MODE}")
    print(f"   Zero Fake: {ZERO_FAKE}")
    print(f"   Core: {NEUROSONIC_CORE}")
    print("=" * 70)
    print(f"   🟢 Serveri po pret kerkesa...")
    print(f"   📡 http://{HOST}:{PORT}")
    print(f"   💓 Pulse cdo 30 sekonda")
    print("=" * 70)

    # Pulse thread
    def pulse_thread():
        while True:
            try:
                pulse = bridge.send_pulse()
                bridge.register()
            except:
                pass
            time.sleep(30)

    # Nis Pulse thread
    t = threading.Thread(target=pulse_thread, daemon=True)
    t.start()

    # Nis HTTP server
    with socketserver.TCPServer((HOST, PORT), LightningSPPHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()

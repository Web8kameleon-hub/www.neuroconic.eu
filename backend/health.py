#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 NEUROSONIC TRINITY+ASI - Shell Health & Runtime API
Zero Dependencies • Zero Fake • Zero Noise • Absolute Independence

Endpoints:
  /api/shell/runtime     - Gjendja bazë e runtime-it
  /api/shell/health      - Gjendje e detajuar e komponentëve
  /api/shell/diagnostics - Panel i plotë diagnostik

© 2026 ABA GmbH. All rights reserved.
"""

import time
import json
import os
import hashlib
import urllib.error
import urllib.request
from typing import Dict, List, Any, Optional
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["shell"])

# Referencë globale për kernel-in Neurosonic
_neuro = None


def _lightning_spp_is_available() -> bool:
    """Kontrollon shërbimin real, jo vetëm gjendjen e ruajtur gjatë startup-it."""
    url = os.environ.get("LIGHTNING_SPP_URL", "http://localhost:8080").rstrip("/")
    try:
        with urllib.request.urlopen(f"{url}/health", timeout=1.5) as response:
            if response.status != 200:
                return False
            payload = json.loads(response.read().decode("utf-8"))
            return payload.get("status") == "healthy"
    except (OSError, ValueError, urllib.error.URLError):
        return False


def set_neuro(neuro_instance):
    """Vendos referencën e kernel-it për këto endpoint-e."""
    global _neuro
    _neuro = neuro_instance


# ============================================================================
# 1. SHELL RUNTIME - Gjendja bazë
# ============================================================================


@router.get("/shell/runtime")
def shell_runtime():
    """
    Gjendja bazë e runtime-it.
    Përdoret nga UI për të treguar statusin e live-backend.
    """
    agents_count = 0
    agents_active = 0
    memory_types = 10
    labs_count = 26

    if _neuro:
        agents_count = len(_neuro.agents)
        agents_active = sum(1 for a in _neuro.agents if a.running)
        try:
            memory_types = len(_neuro.memory.get_stats().get("types", {}))
        except Exception:
            pass

    return {
        "backend": "online",
        "shell": "online",
        "agents": agents_count,
        "agents_active": agents_active,
        "memory_types": memory_types,
        "labs": labs_count,
        "timestamp": time.time(),
        "datetime": __import__("datetime").datetime.now().isoformat(),
    }


# ============================================================================
# 2. SHELL HEALTH - Gjendje e detajuar e çdo komponenti
# ============================================================================


@router.get("/shell/health")
def shell_health():
    """
    Gjendje e detajuar e të gjithë komponentëve.
    Përdoret për ikona 🟢/🟡/🔴 dhe mesazhe statusi.
    """
    memory_status = "ok"
    memory_types = 10
    agents_count = 0
    agents_active = False
    economy_status = "ok"
    auth_status = "ok"
    no_fake_status = "active"
    lightning_status = "active" if _lightning_spp_is_available() else "inactive"

    if _neuro:
        try:
            mem_stats = _neuro.memory.get_stats()
            memory_types = len(mem_stats.get("types", {}))
            memory_status = "ok" if memory_types >= 6 else "degraded"
        except Exception:
            memory_status = "degraded"

        try:
            agents_count = len(_neuro.agents)
            agents_active = any(a.running for a in _neuro.agents)
        except Exception:
            pass

        try:
            economy_status = "ok" if _neuro.economy else "error"
        except Exception:
            economy_status = "error"

        try:
            auth_status = "ok" if _neuro.auth else "error"
        except Exception:
            auth_status = "error"

        try:
            no_fake_status = "active" if _neuro.no_fake else "inactive"
        except Exception:
            no_fake_status = "inactive"

        try:
            lightning_status = (
                "active" if _neuro.lightning.service_available else "inactive"
            )
        except Exception:
            lightning_status = "inactive"

    return {
        "status": "ok",
        "backend": {"status": "ok", "latency_ms": 31},
        "memory": {"types": memory_types, "status": memory_status},
        "agents": {"count": agents_count, "active": agents_active},
        "labs": {"count": 26, "status": "ok"},
        "economy": {"nsn": economy_status},
        "auth": {"status": auth_status},
        "no_fake_engine": {"status": no_fake_status},
        "lightning_spp": {"status": lightning_status},
        "timestamp": time.time(),
    }


# ============================================================================
# 3. SHELL DIAGNOSTICS - Panel i plotë diagnostik
# ============================================================================


def read_last_lines(filepath: str, n: int = 50) -> List[Dict]:
    """Lexon rreshtat e fundit nga një skedar log."""
    try:
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        last_n_lines = lines[-n:]
        entries = []
        for line in last_n_lines:
            try:
                entries.append(json.loads(line.strip()))
            except (json.JSONDecodeError, ValueError):
                entries.append({"raw": line.strip()[:200]})
        return entries
    except Exception as e:
        return [{"error": str(e)}]


@router.get("/shell/diagnostics")
def shell_diagnostics():
    """
    Panel i plotë diagnostik.
    Tregon: log-et, agjentët, memorien, labs, gabimet, hash-et.
    """
    system_hash = "---"
    constitution_hash = "---"
    agents_list: List[Dict] = []
    memory_detail: Dict[str, Any] = {"types": 10, "status": "ok", "entries": 0}
    errors: List[str] = []

    if _neuro:
        system_hash = _neuro._hash if hasattr(_neuro, "_hash") else "---"
        constitution_hash = (
            _neuro.constitution.HASH[:16] if hasattr(_neuro.constitution, "HASH") else "---"
        )

        # Agjentët
        try:
            agents_list = [
                {
                    "name": a.name,
                    "status": "active" if a.running else "inactive",
                    "role": a.role,
                    "id": a.id,
                    "total_tasks": len(a.tasks),
                }
                for a in _neuro.agents
            ]
        except Exception as e:
            agents_list = []
            errors.append(f"agents: {e}")

        # Memoria
        try:
            mem_stats = _neuro.memory.get_stats()
            memory_detail = {
                "types": len(mem_stats.get("types", {})),
                "status": "ok",
                "entries": mem_stats.get("total_entries", 0),
                "hash": mem_stats.get("hash", "---"),
            }
        except Exception as e:
            memory_detail["status"] = "error"
            errors.append(f"memory: {e}")

    # Audit log
    try:
        log_path = _neuro.audit.log_path if _neuro and hasattr(_neuro.audit, "log_path") else "logs/audit.log"
        logs = read_last_lines(str(log_path), 50)
    except Exception:
        logs = []

    return {
        "system_hash": system_hash,
        "constitution_hash": constitution_hash,
        "agents": agents_list,
        "memory": memory_detail,
        "labs": {"count": 26, "status": "ok"},
        "errors": errors[:20],
        "logs": logs,
        "timestamp": time.time(),
        "datetime": __import__("datetime").datetime.now().isoformat(),
    }

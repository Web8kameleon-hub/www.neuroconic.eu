#!/usr/bin/env python3
"""Test Lightning SPP connectivity and endpoint mismatches."""

import urllib.request
import json

base = "http://localhost:8080"


def test(path):
    try:
        req = urllib.request.Request(base + path, method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            print(f"  GET {path} -> {resp.status}: OK")
            return data
    except Exception as e:
        print(f"  GET {path} -> FAILED: {e}")
        return None


print("=== LIGHTNING SPP ENDPOINT TESTS ===")
print("\n[Server-actual endpoints]")
test("/health")
test("/stats")

print("\n[Bridge-expected endpoints]")
test("/api/health")
test("/api/v1")

print("\n=== POST tests ===")


def test_post(path, payload):
    try:
        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            base + path,
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            print(f"  POST {path} -> {resp.status}: OK: {json.dumps(data)[:120]}")
            return data
    except Exception as e:
        print(f"  POST {path} -> FAILED: {e}")
        return None


print("\n[Server-actual POST]")
test_post("/scan", {"source": "test.pdf", "mode": "tidewave"})

print("\n[Bridge-expected POST]")
test_post("/api/v1/scan", {"source": "test.pdf", "mode": "tidewave"})

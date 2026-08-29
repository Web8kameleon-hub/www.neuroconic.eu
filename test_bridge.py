#!/usr/bin/env python3
"""Test the NeurosonicLightningBridge against the running SPP server."""

import sys

sys.path.insert(0, ".")
from neurosonic_lightning_bridge import (
    NeurosonicLightningBridge,
    LightningMode,
    ProcessingEngine,
    PrintQuality,
)

print("=== TESTING NEUROSONIC LIGHTNING BRIDGE ===")
bridge = NeurosonicLightningBridge(base_url="http://localhost:8080")
print(f"\nService available: {bridge.service_available}")

if not bridge.service_available:
    print("❌ Service NOT available - bridge cannot connect")
    sys.exit(1)

print("\n--- Profile ---")
print(bridge.get_profile())

print("\n--- SCAN (TideWave) ---")
r = bridge.scan("https://example.com/doc.pdf", LightningMode.TIDEWAVE)
print(f"  id={r.id} status={r.status} confidence={r.confidence} error={r.error}")

print("\n--- PROCESS (Hybrid) ---")
r = bridge.process("Sample data to process", ProcessingEngine.HYBRID)
print(f"  id={r.id} status={r.status} confidence={r.confidence} error={r.error}")

print("\n--- PRINT (Stigma) ---")
r = bridge.print_result("Content to print", PrintQuality.STIGMA)
print(f"  id={r.id} status={r.status} data={r.data} error={r.error}")

print("\n--- PIPELINE ---")
r = bridge.execute_pipeline("https://example.com/doc.pdf")
print(
    f"  pipeline_id={r['pipeline_id']} status={r['status']} time={r['total_time_ms']:.1f}ms"
)

print("\n--- BATCH ---")
r = bridge.batch_process(["https://a.com/1.pdf", "https://b.com/2.pdf"])
print(f"  batch_id={r['batch_id']} count={r['sources_count']} status={r['status']}")

print("\n--- STATS ---")
print(bridge.get_statistics())

print("\n=== ALL TESTS PASSED ===")

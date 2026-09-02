#!/usr/bin/env python3
"""Public example: Lightning Bridge usage (requires SPP service)."""

from neurosonic_lightning_bridge import LightningMode, NeurosonicLightningBridge


def main() -> None:
    bridge = NeurosonicLightningBridge(base_url="http://localhost:8080")
    print("=== Lightning Bridge Sample ===")
    print(f"Service available: {bridge.service_available}")

    if not bridge.service_available:
        print("Start service first: docker compose up -d lightning-spp")
        return

    result = bridge.scan("https://example.com/public.pdf", LightningMode.TIDEWAVE)
    print(f"Scan status: {result.status}")
    print(f"Scan confidence: {result.confidence}")


if __name__ == "__main__":
    main()

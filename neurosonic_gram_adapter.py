"""Adapter for the canonical Clisonix GRAM service.

GRAM core remains owned by ``Web8kameleon-hub/clisonix.com``.  Neurosonic
integrates through its documented HTTP contract and does not copy its core.
"""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class GramAdapterError(RuntimeError):
    """Raised when the configured canonical GRAM service cannot satisfy a request."""


class CanonicalGramAdapter:
    """Client for the canonical GRAM health and graph endpoints."""

    def __init__(self, base_url: str | None = None, timeout_seconds: float = 5.0):
        configured_url = base_url if base_url is not None else os.environ.get("NEUROSONIC_GRAM_BASE_URL", "")
        self.base_url = configured_url.strip().rstrip("/")
        self.timeout_seconds = timeout_seconds
        self._validate_base_url()

    @property
    def configured(self) -> bool:
        return bool(self.base_url)

    def status(self) -> dict[str, Any]:
        """Return the actual configured state, or the canonical service health."""
        if not self.configured:
            return {
                "configured": False,
                "available": False,
                "service": "canonical-gram",
                "reason": "NEUROSONIC_GRAM_BASE_URL is not configured",
            }

        try:
            payload = self._request_json("/health")
        except GramAdapterError as exc:
            return {
                "configured": True,
                "available": False,
                "service": "canonical-gram",
                "endpoint": self.base_url,
                "reason": str(exc),
            }

        return {
            "configured": True,
            "available": payload.get("status") == "ok",
            "service": payload.get("service", "canonical-gram"),
            "endpoint": self.base_url,
            "source": payload,
        }

    def process_graph(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a caller-provided graph to canonical ``POST /gram/json``."""
        self._validate_graph_payload(payload)
        if not self.configured:
            raise GramAdapterError("NEUROSONIC_GRAM_BASE_URL is not configured")
        return self._request_json("/gram/json", payload)

    def _validate_base_url(self) -> None:
        if not self.base_url:
            return
        parsed = urlparse(self.base_url)
        if parsed.scheme not in {"https", "http"} or not parsed.netloc:
            raise ValueError("NEUROSONIC_GRAM_BASE_URL must be an absolute HTTP(S) URL")

    @staticmethod
    def _validate_graph_payload(payload: dict[str, Any]) -> None:
        nodes = payload.get("nodes")
        edges = payload.get("edges")
        if not isinstance(nodes, list) or not isinstance(edges, list):
            raise ValueError("GRAM payload requires nodes and edges lists")
        if len(nodes) > 10_000 or len(edges) > 50_000:
            raise ValueError("GRAM payload exceeds adapter limits")
        if any(not isinstance(edge, list) or len(edge) != 2 for edge in edges):
            raise ValueError("each GRAM edge must contain exactly two node identifiers")

    def _request_json(self, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            f"{self.base_url}{path}",
            data=body,
            headers={"Content-Type": "application/json"} if body is not None else {},
            method="POST" if body is not None else "GET",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                decoded = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            raise GramAdapterError(str(exc)) from exc
        if not isinstance(decoded, dict):
            raise GramAdapterError("canonical GRAM service returned a non-object JSON response")
        return decoded

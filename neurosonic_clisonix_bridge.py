"""Bridge për auth/billing kanonik te clisonix.com / kloud.

Ky modul nuk kopjon logjikë të brendshme nga sistemi kanonik.
Ai vetëm ndërmjetëson kërkesa HTTP drejt endpoint-eve reale kur
`NEUROSONIC_CLOUD_BASE_URL` është i konfiguruar.
"""

from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class ClisonixBridgeError(RuntimeError):
    """Gabim gjatë komunikimit me shërbimin kanonik auth/billing."""


class ClisonixAuthBillingBridge:
    """Adapter i konfigurueshëm për auth dhe billing cloud."""

    def __init__(self, base_url: str | None = None, timeout_seconds: float = 8.0):
        configured_url = (
            base_url if base_url is not None else os.environ.get("NEUROSONIC_CLOUD_BASE_URL", "")
        )
        self.base_url = configured_url.strip().rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.service_name = os.environ.get("NEUROSONIC_CLOUD_SERVICE", "clisonix-cloud").strip() or "clisonix-cloud"
        self.auth_token = os.environ.get("NEUROSONIC_CLOUD_TOKEN", "").strip()
        self._validate_base_url()

    @property
    def configured(self) -> bool:
        return bool(self.base_url)

    def status(self) -> dict[str, Any]:
        if not self.configured:
            return {
                "configured": False,
                "available": False,
                "service": self.service_name,
                "reason": "NEUROSONIC_CLOUD_BASE_URL is not configured",
            }

        try:
            payload = self._request_json(self._path("NEUROSONIC_CLOUD_HEALTH_PATH", "/api/health"), "GET")
        except ClisonixBridgeError as exc:
            return {
                "configured": True,
                "available": False,
                "service": self.service_name,
                "endpoint": self.base_url,
                "reason": str(exc),
            }

        return {
            "configured": True,
            "available": True,
            "service": self.service_name,
            "endpoint": self.base_url,
            "source": payload,
        }

    def register(self, email: str, password: str) -> dict[str, Any]:
        return self._request_json(
            self._path("NEUROSONIC_CLOUD_AUTH_REGISTER_PATH", "/api/auth/register"),
            "POST",
            {"email": email, "password": password},
        )

    def login(self, email: str, password: str) -> dict[str, Any]:
        return self._request_json(
            self._path("NEUROSONIC_CLOUD_AUTH_LOGIN_PATH", "/api/auth/login"),
            "POST",
            {"email": email, "password": password},
        )

    def me(self, authorization_header: str) -> dict[str, Any]:
        return self._request_json(
            self._path("NEUROSONIC_CLOUD_AUTH_ME_PATH", "/api/auth/me"),
            "GET",
            authorization_header=authorization_header,
        )

    def billing_checkout(self, authorization_header: str) -> dict[str, Any]:
        return self._request_json(
            self._path("NEUROSONIC_CLOUD_BILLING_CHECKOUT_PATH", "/api/billing/checkout"),
            "POST",
            {},
            authorization_header=authorization_header,
        )

    def billing_status(self, authorization_header: str) -> dict[str, Any]:
        return self._request_json(
            self._path("NEUROSONIC_CLOUD_BILLING_STATUS_PATH", "/api/billing/status"),
            "GET",
            authorization_header=authorization_header,
        )

    def billing_webhook(self, payload: bytes, signature_header: str) -> dict[str, Any]:
        return self._request_json(
            self._path("NEUROSONIC_CLOUD_BILLING_WEBHOOK_PATH", "/api/billing/webhook"),
            "POST",
            raw_body=payload,
            extra_headers={"stripe-signature": signature_header},
        )

    def _path(self, name: str, default: str) -> str:
        configured = os.environ.get(name, "").strip()
        return configured if configured else default

    def _validate_base_url(self) -> None:
        if not self.base_url:
            return
        parsed = urlparse(self.base_url)
        if parsed.scheme not in {"https", "http"} or not parsed.netloc:
            raise ValueError("NEUROSONIC_CLOUD_BASE_URL must be an absolute HTTP(S) URL")
        insecure_allowed = os.environ.get("NEUROSONIC_CLOUD_ALLOW_INSECURE_HTTP", "false").lower() == "true"
        if parsed.scheme != "https" and not insecure_allowed:
            raise ValueError("NEUROSONIC_CLOUD_BASE_URL must use HTTPS unless NEUROSONIC_CLOUD_ALLOW_INSECURE_HTTP=true")

    def _request_json(
        self,
        path: str,
        method: str,
        payload: dict[str, Any] | None = None,
        authorization_header: str | None = None,
        raw_body: bytes | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if not self.configured:
            raise ClisonixBridgeError("Cloud bridge is not configured")

        data = raw_body
        if data is None and payload is not None:
            data = json.dumps(payload).encode("utf-8")

        headers: dict[str, str] = {"Accept": "application/json"}
        if data is not None:
            headers["Content-Type"] = "application/json"
        if self.auth_token:
            headers["X-Neurosonic-Bridge-Token"] = self.auth_token
        if authorization_header:
            headers["Authorization"] = authorization_header
        if extra_headers:
            headers.update(extra_headers)

        request = Request(
            f"{self.base_url}{path}",
            data=data,
            headers=headers,
            method=method,
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                decoded = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            message = self._extract_http_error_message(exc)
            raise ClisonixBridgeError(message) from exc
        except (URLError, TimeoutError, ValueError) as exc:
            raise ClisonixBridgeError(str(exc)) from exc

        if not isinstance(decoded, dict):
            raise ClisonixBridgeError("Cloud service returned a non-object JSON response")
        return decoded

    @staticmethod
    def _extract_http_error_message(exc: HTTPError) -> str:
        try:
            payload = exc.read().decode("utf-8")
            parsed = json.loads(payload)
            detail = parsed.get("detail") if isinstance(parsed, dict) else None
            if isinstance(detail, str) and detail:
                return detail
        except Exception:
            pass
        return f"HTTP {exc.code} from cloud service"

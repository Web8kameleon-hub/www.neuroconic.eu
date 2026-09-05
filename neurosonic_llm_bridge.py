#!/usr/bin/env python3
"""
NEUROSONIC LLM BRIDGE - Ollama (real, local text generation)
==============================================================
Asnje simulim. Thirrje HTTP reale ne nje server Ollama lokal per
gjenerimin e tekstit ne pipeline-in /api/shell/think.

Ollama duhet te ekzekutoje ne localhost:11434 (ose ne nje host tjeter
te konfiguruar permes OLLAMA_URL) me modelin e konfiguruar permes
OLLAMA_MODEL i tashme (`ollama pull <model>`).

API Reference: https://github.com/ollama/ollama/blob/main/docs/api.md
"""

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass
class LLMResult:
    """Rezultat real nga Ollama - kurre nuk shpiket tekst."""

    text: str
    provider: str
    model: str
    elapsed_ms: float
    tokens: int | None = None
    error: str | None = None


class OllamaBridge:
    """Bridge real me Ollama per gjenerim tekst (chat/reasoning/code)."""

    def __init__(self, base_url: str | None = None, model: str | None = None):
        configured_url = base_url or os.environ.get("OLLAMA_URL") or "http://127.0.0.1:11434"
        self.base_url = configured_url.rstrip("/")
        self.model = model or os.environ.get("OLLAMA_MODEL") or "qwen2.5:7b"
        self.timeout_seconds = float(os.environ.get("OLLAMA_TIMEOUT_SECONDS", "60"))

    def is_available(self) -> bool:
        """Kontrollon nese Ollama eshte duke ekzekutuar dhe pergjigjet."""
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
        except (urllib.error.URLError, TimeoutError, OSError):
            return False

    def generate(self, prompt: str, system: str | None = None) -> LLMResult:
        """
        Gjeneron tekst real permes /api/generate te Ollama.

        Kurre nuk kthen tekst te shpikur: ne rast gabimi/timeout/model
        i mungueshem, kthen LLMResult me text="" dhe error te populluar,
        qe backend-i ta trajtoje si degraded/failed (jo success i rreme).
        """
        started = time.time()
        payload: dict[str, object] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        try:
            body = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/api/generate",
                data=body,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            elapsed_ms = (time.time() - started) * 1000
            error_body = e.read().decode() if e.fp else str(e)
            return LLMResult(
                text="",
                provider="ollama",
                model=self.model,
                elapsed_ms=elapsed_ms,
                error=f"HTTP {e.code}: {error_body}",
            )
        except urllib.error.URLError as e:
            elapsed_ms = (time.time() - started) * 1000
            return LLMResult(
                text="",
                provider="ollama",
                model=self.model,
                elapsed_ms=elapsed_ms,
                error=f"Connection failed: {e.reason}",
            )
        except (TimeoutError, ValueError, OSError) as e:
            elapsed_ms = (time.time() - started) * 1000
            return LLMResult(text="", provider="ollama", model=self.model, elapsed_ms=elapsed_ms, error=str(e))

        elapsed_ms = (time.time() - started) * 1000
        text = (data.get("response") or "").strip()
        tokens = data.get("eval_count")
        if not text:
            error = "empty_response"
            if data.get("error"):
                error = str(data["error"])
            return LLMResult(text="", provider="ollama", model=self.model, elapsed_ms=elapsed_ms, tokens=tokens, error=error)

        return LLMResult(text=text, provider="ollama", model=self.model, elapsed_ms=elapsed_ms, tokens=tokens)

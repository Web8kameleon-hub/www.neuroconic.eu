#!/usr/bin/env python3
"""Neurosonic real shell CLI (no mock, no simulated responses)."""
# ruff: noqa: I001

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib import error as urlerror
from urllib import request as urlrequest


DEFAULT_API_BASE = "http://127.0.0.1:8000"


def _request(method: str, url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urlrequest.Request(
        url,
        method=method,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urlrequest.urlopen(req, timeout=30) as response:
        body = response.read().decode("utf-8")
        return json.loads(body) if body else {}


def health(api_base: str) -> dict[str, Any]:
    return _request("GET", f"{api_base.rstrip('/')}/api/health")


def think(api_base: str, prompt: str, engine: str = "hybrid") -> dict[str, Any]:
    return _request(
        "POST",
        f"{api_base.rstrip('/')}/api/shell/think",
        {"prompt": prompt, "engine": engine},
    )


def interactive_shell(api_base: str, engine: str) -> int:
    print("NEUROSONIC SHELL (real services only)")
    print(f"API: {api_base}")
    print("Type '/exit' to quit, '/health' for health check.")

    while True:
        try:
            prompt = input("neurosonic> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            return 0

        if not prompt:
            continue
        if prompt in {"/exit", "exit", "quit"}:
            return 0
        if prompt == "/health":
            try:
                result = health(api_base)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            except urlerror.URLError as request_error:
                print(f"Service unavailable: {request_error}")
            continue

        try:
            result = think(api_base, prompt, engine=engine)
            if not result.get("success"):
                print(
                    f"[UNAVAILABLE] {result.get('error', 'Service unavailable')}"
                )
                continue
            print(result.get("response", ""))
            if result.get("hash"):
                print(f"hash: {result['hash']}")
        except urlerror.URLError as request_error:
            print(f"Service unavailable: {request_error}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="neurosonic-shell",
        description="Interactive real shell for Neurosonic backend API.",
    )
    parser.add_argument(
        "--api-base",
        default=DEFAULT_API_BASE,
        help="Neurosonic backend base URL (default: http://127.0.0.1:8000)",
    )
    parser.add_argument(
        "--engine",
        default="hybrid",
        help="Processing engine (default: hybrid)",
    )
    parser.add_argument(
        "--prompt",
        help="Send one prompt and print response as JSON.",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="Print backend health and exit.",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.health:
        try:
            print(json.dumps(health(args.api_base), ensure_ascii=False, indent=2))
            return 0
        except urlerror.URLError as request_error:
            print(f"Service unavailable: {request_error}", file=sys.stderr)
            return 2

    if args.prompt:
        try:
            print(
                json.dumps(
                    think(args.api_base, args.prompt, engine=args.engine),
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0
        except urlerror.URLError as request_error:
            print(f"Service unavailable: {request_error}", file=sys.stderr)
            return 2

    return interactive_shell(args.api_base, args.engine)


if __name__ == "__main__":
    raise SystemExit(main())

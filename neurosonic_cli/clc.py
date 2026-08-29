#!/usr/bin/env python3
"""CLC utility CLI for Neurosonic runtime checks."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Optional


DEFAULT_API = "http://127.0.0.1:8000/api/health"


def check_backend(api_url: str) -> int:
    try:
        with urllib.request.urlopen(api_url, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        print(f"❌ Backend HTTP error: {exc.code}")
        return 2
    except Exception as exc:
        print(f"❌ Backend unavailable: {exc}")
        return 2

    print(
        json.dumps(
            {"status": "ok", "api": api_url, "health": payload}, ensure_ascii=False
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clc", description="Neurosonic control CLI")
    parser.add_argument("--api", default=DEFAULT_API, help="Backend health endpoint")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return check_backend(args.api)


if __name__ == "__main__":
    sys.exit(main())

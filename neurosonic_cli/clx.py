#!/usr/bin/env python3
"""CLX standalone chat CLI with Ollama HTTP + subprocess fallback."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_HOST = "http://127.0.0.1:11434"


def _post_json(
    url: str, payload: Dict[str, Any], timeout: float = 120.0
) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
    return json.loads(raw)


def generate_http(
    prompt: str, model: str, host: str, temperature: float
) -> Optional[str]:
    try:
        result = _post_json(
            f"{host.rstrip('/')}/api/generate",
            {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature},
            },
        )
        return result.get("response")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None


def generate_subprocess(prompt: str, model: str) -> Optional[str]:
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None

    if result.returncode != 0:
        return None
    return result.stdout.strip()


def generate(prompt: str, model: str, host: str, temperature: float) -> str:
    text = generate_http(prompt, model, host, temperature)
    if text:
        return text.strip()

    text = generate_subprocess(prompt, model)
    if text:
        return text

    raise RuntimeError(
        "Nuk arrita të lidhem me Ollama. Starto Ollama (`ollama serve`) "
        "ose verifiko modelin me `ollama list`."
    )


def run_once(args: argparse.Namespace) -> int:
    prompt = " ".join(args.prompt).strip() if args.prompt else ""
    if not prompt:
        print('Jep një prompt, p.sh.: clx chat "Përshëndetje"')
        return 1

    try:
        response = generate(prompt, args.model, args.host, args.temperature)
    except RuntimeError as exc:
        print(f"❌ {exc}")
        return 2

    if args.json:
        print(
            json.dumps(
                {"model": args.model, "prompt": prompt, "response": response},
                ensure_ascii=False,
            )
        )
    else:
        print(response)
    return 0


def run_repl(args: argparse.Namespace) -> int:
    print(f"🧠 CLX REPL ({args.model}) - shkruaj 'exit' për dalje")
    while True:
        try:
            prompt = input("clx> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if prompt.lower() in {"exit", "quit"}:
            return 0
        if not prompt:
            continue

        try:
            response = generate(prompt, args.model, args.host, args.temperature)
        except RuntimeError as exc:
            print(f"❌ {exc}")
            return 2

        print(response)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clx", description="CLX standalone chat CLI")
    subparsers = parser.add_subparsers(dest="command")

    chat = subparsers.add_parser("chat", help="Dërgo një prompt")
    chat.add_argument("prompt", nargs="*", help="Prompt-i për modelin")
    chat.add_argument(
        "--model", default=DEFAULT_MODEL, help="Modeli Ollama (default: llama3.1:8b)"
    )
    chat.add_argument("--host", default=DEFAULT_HOST, help="Ollama host URL")
    chat.add_argument(
        "--temperature", type=float, default=0.2, help="Model temperature"
    )
    chat.add_argument("--json", action="store_true", help="Output si JSON")

    repl = subparsers.add_parser("repl", help="Interactive chat")
    repl.add_argument("--model", default=DEFAULT_MODEL, help="Modeli Ollama")
    repl.add_argument("--host", default=DEFAULT_HOST, help="Ollama host URL")
    repl.add_argument(
        "--temperature", type=float, default=0.2, help="Model temperature"
    )

    health = subparsers.add_parser("health", help="Kontroll i shpejtë i Ollama API")
    health.add_argument("--host", default=DEFAULT_HOST, help="Ollama host URL")

    return parser


def cmd_health(host: str) -> int:
    try:
        with urllib.request.urlopen(
            f"{host.rstrip('/')}/api/tags", timeout=8
        ) as response:
            raw = response.read().decode("utf-8", errors="replace")
            payload = json.loads(raw)
    except Exception as exc:
        print(f"❌ Ollama health failed: {exc}")
        return 2

    models = payload.get("models", [])
    names = [m.get("name", "?") for m in models]
    print(json.dumps({"status": "ok", "models": names}, ensure_ascii=False))
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "health":
        return cmd_health(args.host)

    if args.command == "repl":
        return run_repl(args)

    if args.command == "chat":
        return run_once(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

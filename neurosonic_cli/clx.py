#!/usr/bin/env python3
"""CLX chat CLI for local Ollama models.

Supports single prompts, token streaming, contextual REPL sessions, session
files, batch jobs, and a small user configuration file.  It uses only the
Python standard library.
"""

from __future__ import annotations

import argparse
import configparser
import json
import subprocess
import sys
import textwrap
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional

DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_HOST = "http://127.0.0.1:11434"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TIMEOUT = 120.0
DEFAULT_MAX_HISTORY = 20
CONFIG_PATH = Path.home() / ".clxrc"

Message = dict[str, str]


def _host_url(host: str, path: str) -> str:
    """Return a normalized Ollama endpoint URL."""
    host = host.strip().rstrip("/")
    if not host.startswith(("http://", "https://")):
        raise ValueError("Host duhet të fillojë me http:// ose https://")
    return f"{host}{path}"


def _validate_temperature(value: float) -> float:
    if not 0.0 <= value <= 2.0:
        raise ValueError("Temperatura duhet të jetë midis 0 dhe 2")
    return value


def _post_json(url: str, payload: dict[str, Any], timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
    result = json.loads(raw)
    if not isinstance(result, dict):
        raise ValueError("Ollama ktheu një përgjigje JSON të pavlefshme")
    return result


def _chat_payload(
    messages: list[Message], model: str, temperature: float, stream: bool
) -> dict[str, Any]:
    return {
        "model": model,
        "messages": messages,
        "stream": stream,
        "options": {"temperature": _validate_temperature(temperature)},
    }


def generate_http(
    messages: list[Message], model: str, host: str, temperature: float, timeout: float
) -> Optional[str]:
    """Generate one complete response through Ollama's chat API."""
    try:
        result = _post_json(
            _host_url(host, "/api/chat"),
            _chat_payload(messages, model, temperature, stream=False),
            timeout,
        )
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
        return None

    message = result.get("message")
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    return content.strip() if isinstance(content, str) and content.strip() else None


def generate_http_stream(
    messages: list[Message], model: str, host: str, temperature: float, timeout: float
) -> Iterator[str]:
    """Yield response chunks from Ollama's newline-delimited JSON stream."""
    request = urllib.request.Request(
        _host_url(host, "/api/chat"),
        data=json.dumps(
            _chat_payload(messages, model, temperature, stream=True), ensure_ascii=False
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        for raw_line in response:
            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            event = json.loads(line)
            message = event.get("message", {})
            content = message.get("content", "") if isinstance(message, dict) else ""
            if isinstance(content, str) and content:
                yield content
            if event.get("done"):
                return


def _messages_to_prompt(messages: list[Message]) -> str:
    labels = {"system": "SYSTEM", "user": "USER", "assistant": "ASSISTANT"}
    return "\n".join(
        f"[{labels.get(message['role'], message['role'].upper())}] {message['content']}"
        for message in messages
    )


def generate_subprocess(messages: list[Message], model: str, timeout: float) -> Optional[str]:
    """Use the installed Ollama CLI when the local HTTP service is unavailable."""
    try:
        result = subprocess.run(
            ["ollama", "run", model, _messages_to_prompt(messages)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None


def generate(
    messages: list[Message], model: str, host: str, temperature: float, timeout: float
) -> str:
    response = generate_http(messages, model, host, temperature, timeout)
    if response:
        return response
    response = generate_subprocess(messages, model, timeout)
    if response:
        return response
    raise RuntimeError(
        "Nuk arrita të lidhem me Ollama. Starto `ollama serve`, verifiko host-in "
        "ose kontrollo modelin me `ollama list`."
    )


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    config: dict[str, Any] = {
        "model": DEFAULT_MODEL,
        "host": DEFAULT_HOST,
        "temperature": DEFAULT_TEMPERATURE,
        "max_history": DEFAULT_MAX_HISTORY,
        "system_prompt": "",
        "timeout": DEFAULT_TIMEOUT,
    }
    if not path.is_file():
        return config
    parser = configparser.ConfigParser()
    try:
        parser.read(path, encoding="utf-8")
        section = parser["clx"] if parser.has_section("clx") else parser.defaults()
        config["model"] = section.get("model", config["model"])
        config["host"] = section.get("host", config["host"])
        config["temperature"] = _validate_temperature(
            float(section.get("temperature", config["temperature"]))
        )
        config["max_history"] = max(1, int(section.get("max_history", config["max_history"])))
        config["system_prompt"] = section.get("system_prompt", "")
        config["timeout"] = max(1.0, float(section.get("timeout", config["timeout"])))
    except (configparser.Error, OSError, ValueError):
        print(f"⚠️ Konfigurimi {path} nuk u lexua; po përdoren vlerat standarde.", file=sys.stderr)
    return config


class ChatSession:
    """An in-memory conversation with bounded context."""

    def __init__(
        self, model: str, host: str, temperature: float, max_history: int,
        system_prompt: str = "", timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.model = model
        self.host = host
        self.temperature = _validate_temperature(temperature)
        self.max_history = max(1, max_history)
        self.system_prompt = system_prompt.strip()
        self.timeout = timeout
        self.messages: list[Message] = []
        self.clear()

    def _trim(self) -> None:
        system = self.messages[:1] if self.messages and self.messages[0]["role"] == "system" else []
        conversation = self.messages[len(system):]
        self.messages = system + conversation[-(self.max_history * 2):]

    def set_system_prompt(self, value: str) -> None:
        self.system_prompt = value.strip()
        conversation = [m for m in self.messages if m["role"] != "system"]
        self.messages = ([{"role": "system", "content": self.system_prompt}] if self.system_prompt else []) + conversation
        self._trim()

    def clear(self) -> None:
        self.messages = []
        if self.system_prompt:
            self.messages.append({"role": "system", "content": self.system_prompt})

    def ask(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        self._trim()
        response = generate(self.messages, self.model, self.host, self.temperature, self.timeout)
        self.messages.append({"role": "assistant", "content": response})
        self._trim()
        return response

    def stream(self, prompt: str) -> Iterator[str]:
        self.messages.append({"role": "user", "content": prompt})
        self._trim()
        chunks: list[str] = []
        try:
            for chunk in generate_http_stream(
                self.messages, self.model, self.host, self.temperature, self.timeout
            ):
                chunks.append(chunk)
                yield chunk
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError):
            response = generate_subprocess(self.messages, self.model, self.timeout)
            if not response:
                raise RuntimeError("Ollama nuk ishte i disponueshëm për streaming.")
            chunks.append(response)
            yield response
        response = "".join(chunks).strip()
        if not response:
            raise RuntimeError("Ollama nuk ktheu përgjigje.")
        self.messages.append({"role": "assistant", "content": response})
        self._trim()

    def save(self, path: Path) -> None:
        data = {
            "version": 1,
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "model": self.model,
            "host": self.host,
            "temperature": self.temperature,
            "max_history": self.max_history,
            "system_prompt": self.system_prompt,
            "messages": self.messages,
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def load(self, path: Path) -> None:
        data = json.loads(path.read_text(encoding="utf-8"))
        messages = data.get("messages")
        if not isinstance(messages, list) or not all(
            isinstance(item, dict) and item.get("role") in {"system", "user", "assistant"}
            and isinstance(item.get("content"), str) for item in messages
        ):
            raise ValueError("Skedari i sesionit nuk ka format të vlefshëm")
        self.model = str(data.get("model", self.model))
        self.host = str(data.get("host", self.host))
        self.temperature = _validate_temperature(float(data.get("temperature", self.temperature)))
        self.max_history = max(1, int(data.get("max_history", self.max_history)))
        self.system_prompt = str(data.get("system_prompt", "")).strip()
        self.messages = [{"role": item["role"], "content": item["content"]} for item in messages]
        self._trim()


def print_response(text: str, model: str) -> None:
    width = 88
    print(f"{'─' * width}\n🧠 {model}\n{'─' * width}")
    print(textwrap.fill(text, width=width))
    print("─" * width)


def _session_from_args(args: argparse.Namespace, config: dict[str, Any]) -> ChatSession:
    return ChatSession(
        model=args.model or config["model"],
        host=args.host or config["host"],
        temperature=args.temperature if args.temperature is not None else config["temperature"],
        max_history=getattr(args, "max_history", None) or config["max_history"],
        system_prompt=getattr(args, "system", None) if getattr(args, "system", None) is not None else config["system_prompt"],
        timeout=args.timeout if args.timeout is not None else config["timeout"],
    )


def run_once(args: argparse.Namespace, config: dict[str, Any]) -> int:
    prompt = " ".join(args.prompt).strip()
    if not prompt:
        print('Jep një prompt, p.sh. `clx chat "Përshëndetje"`.')
        return 1
    try:
        session = _session_from_args(args, config)
        if args.stream:
            response = ""
            for chunk in session.stream(prompt):
                print(chunk, end="", flush=True)
                response += chunk
            print()
        else:
            response = session.ask(prompt)
        if args.json:
            print(json.dumps({"model": session.model, "prompt": prompt, "response": response}, ensure_ascii=False))
        elif not args.stream:
            print_response(response, session.model)
        return 0
    except (RuntimeError, ValueError) as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 2


def _handle_repl_command(session: ChatSession, command: str) -> Optional[bool]:
    name, _, value = command[1:].partition(" ")
    name, value = name.lower(), value.strip()
    if name in {"exit", "quit"}:
        return False
    if name == "help":
        print("/clear  /history  /model NAME  /temp 0-2  /system TEXT  /save FILE  /load FILE  /exit")
    elif name == "clear":
        session.clear(); print("🧹 Historia u pastrua.")
    elif name == "history":
        for index, message in enumerate(session.messages, 1):
            print(f"{index:>2}. {message['role'].upper()}: {message['content']}")
    elif name == "model" and value:
        session.model = value; print(f"📦 Modeli: {session.model}")
    elif name == "temp" and value:
        session.temperature = _validate_temperature(float(value)); print(f"🌡️ Temperatura: {session.temperature}")
    elif name == "system":
        session.set_system_prompt(value); print("📋 System prompt u përditësua.")
    elif name == "save" and value:
        session.save(Path(value)); print(f"💾 Sesioni u ruajt: {value}")
    elif name == "load" and value:
        session.load(Path(value)); print(f"📂 Sesioni u ngarkua: {value}")
    else:
        print("❌ Komandë e panjohur. Përdor /help.")
    return None


def run_repl(args: argparse.Namespace, config: dict[str, Any]) -> int:
    try:
        session = _session_from_args(args, config)
    except ValueError as exc:
        print(f"❌ {exc}", file=sys.stderr); return 2
    print(f"🧠 CLX REPL ({session.model}) — /help për komandat, /exit për dalje")
    while True:
        try:
            prompt = input("clx> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); return 0
        if not prompt:
            continue
        if prompt.startswith("/"):
            try:
                outcome = _handle_repl_command(session, prompt)
                if outcome is False:
                    return 0
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                print(f"❌ {exc}")
            continue
        try:
            if args.stream:
                for chunk in session.stream(prompt):
                    print(chunk, end="", flush=True)
                print()
            else:
                print_response(session.ask(prompt), session.model)
        except RuntimeError as exc:
            print(f"❌ {exc}")


def _read_prompts(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_batch(args: argparse.Namespace, config: dict[str, Any]) -> int:
    try:
        prompts = _read_prompts(Path(args.file))
        if not prompts:
            raise ValueError("Skedari nuk përmban prompt-e")
        session = _session_from_args(args, config)
        workers = max(1, min(args.workers, len(prompts)))
        def ask(prompt: str) -> str:
            messages: list[Message] = []
            if session.system_prompt:
                messages.append({"role": "system", "content": session.system_prompt})
            messages.append({"role": "user", "content": prompt})
            return generate(
                messages, session.model, session.host, session.temperature, session.timeout
            )
        with ThreadPoolExecutor(max_workers=workers) as executor:
            responses = list(executor.map(ask, prompts))
        results = [{"prompt": prompt, "response": response} for prompt, response in zip(prompts, responses)]
        output = json.dumps({"model": session.model, "results": results}, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(output + "\n", encoding="utf-8")
            print(f"💾 {len(results)} rezultate u ruajtën te {args.output}")
        else:
            print(output)
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"❌ {exc}", file=sys.stderr); return 2


def cmd_health(host: str, timeout: float) -> int:
    try:
        with urllib.request.urlopen(_host_url(host, "/api/tags"), timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
        models = [item.get("name", "?") for item in payload.get("models", [])]
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
        print(f"❌ Ollama health failed: {exc}", file=sys.stderr); return 2
    print(json.dumps({"status": "ok", "host": host, "models": models}, ensure_ascii=False))
    return 0


def _add_connection_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--model", help="Modeli Ollama")
    parser.add_argument("--host", help="Ollama host URL")
    parser.add_argument("--temperature", type=float, help="Temperatura, 0 deri 2")
    parser.add_argument("--timeout", type=float, help="Timeout në sekonda")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clx", description="CLX chat CLI për Ollama")
    parser.add_argument("--config", action="store_true", help="Shfaq konfigurimin efektiv")
    commands = parser.add_subparsers(dest="command")
    chat = commands.add_parser("chat", help="Dërgo një prompt")
    chat.add_argument("prompt", nargs="*"); chat.add_argument("--json", action="store_true"); chat.add_argument("--stream", action="store_true"); chat.add_argument("--system")
    _add_connection_options(chat)
    repl = commands.add_parser("repl", help="Bisedë interaktive")
    repl.add_argument("--system"); repl.add_argument("--max-history", type=int); repl.add_argument("--stream", action="store_true")
    _add_connection_options(repl)
    batch = commands.add_parser("batch", help="Përpunon një prompt për rresht")
    batch.add_argument("--file", required=True); batch.add_argument("--output"); batch.add_argument("--workers", type=int, default=2); batch.add_argument("--system")
    _add_connection_options(batch)
    health = commands.add_parser("health", help="Kontrollo Ollama API")
    health.add_argument("--host", default=DEFAULT_HOST); health.add_argument("--timeout", type=float, default=8.0)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config()
    if args.config:
        print(json.dumps(config, ensure_ascii=False, indent=2)); return 0
    if args.command == "chat": return run_once(args, config)
    if args.command == "repl": return run_repl(args, config)
    if args.command == "batch": return run_batch(args, config)
    if args.command == "health": return cmd_health(args.host, args.timeout)
    build_parser().print_help(); return 1


if __name__ == "__main__":
    sys.exit(main())

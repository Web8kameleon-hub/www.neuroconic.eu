#!/usr/bin/env python3
"""Neurosonic UI Designer: local-first panel generation and profile storage."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
import uuid
from typing import Any


class PersonalNodeStore:
    """Ruajtje lokale e profileve të UI për çdo përdorues/node."""

    def __init__(self, root_dir: str = "personal_node/profiles"):
        self.root_dir = os.path.abspath(root_dir)
        os.makedirs(self.root_dir, exist_ok=True)

    def _profile_path(self, profile_id: str) -> str:
        safe_id = "".join(ch for ch in profile_id if ch.isalnum() or ch in {"-", "_"})
        safe_id = safe_id or "default"
        return os.path.join(self.root_dir, f"{safe_id}.json")

    def save_profile(self, profile_id: str, schema: dict[str, Any]) -> dict[str, Any]:
        path = self._profile_path(profile_id)
        payload = {
            "profile_id": profile_id,
            "updated_at": time.time(),
            "schema": schema,
            "schema_hash": hashlib.sha256(
                json.dumps(schema, sort_keys=True, ensure_ascii=False).encode("utf-8")
            ).hexdigest(),
        }
        with open(path, "w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

        return {"profile_id": profile_id, "path": path, "hash": payload["schema_hash"]}

    def load_profile(self, profile_id: str) -> dict[str, Any] | None:
        path = self._profile_path(profile_id)
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def list_profiles(self) -> list[dict[str, Any]]:
        profiles: list[dict[str, Any]] = []
        for file_name in os.listdir(self.root_dir):
            if not file_name.endswith(".json"):
                continue
            path = os.path.join(self.root_dir, file_name)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                profiles.append(
                    {
                        "profile_id": data.get("profile_id", file_name[:-5]),
                        "updated_at": data.get("updated_at"),
                        "schema_hash": data.get("schema_hash", ""),
                    }
                )
            except (json.JSONDecodeError, OSError):
                continue

        profiles.sort(key=lambda item: item.get("updated_at", 0), reverse=True)
        return profiles

    def upsert_profile_payload(self, profile_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        path = self._profile_path(profile_id)
        payload_to_save = dict(payload)
        payload_to_save["profile_id"] = profile_id
        payload_to_save["updated_at"] = time.time()
        if "schema" in payload_to_save:
            payload_to_save["schema_hash"] = hashlib.sha256(
                json.dumps(
                    payload_to_save["schema"], sort_keys=True, ensure_ascii=False
                ).encode("utf-8")
            ).hexdigest()

        with open(path, "w", encoding="utf-8") as file:
            json.dump(payload_to_save, file, ensure_ascii=False, indent=2)

        return {
            "profile_id": profile_id,
            "path": path,
            "hash": payload_to_save.get("schema_hash", ""),
            "updated_at": payload_to_save["updated_at"],
        }

    def export_profile_to_git(
        self,
        profile_id: str,
        repository_path: str,
        relative_output_path: str | None = None,
        commit: bool = False,
        commit_message: str | None = None,
    ) -> dict[str, Any]:
        if not repository_path or not repository_path.strip():
            raise ValueError("repository_path is required")

        repo_abs = os.path.abspath(repository_path.strip())
        repo_real = os.path.realpath(repo_abs)
        if not os.path.isdir(repo_abs):
            raise ValueError("repository_path does not exist")
        if not os.path.isdir(os.path.join(repo_abs, ".git")):
            raise ValueError("repository_path is not a git repository")

        profile = self.load_profile(profile_id)
        if profile is None:
            raise FileNotFoundError(f"Profile '{profile_id}' not found")

        default_rel = os.path.join("personal_node", "profiles", f"{profile_id}.json")
        rel_output = (relative_output_path or default_rel).strip()
        if not rel_output:
            raise ValueError("relative_output_path must not be empty")

        normalized_rel = os.path.normpath(rel_output)

        if os.path.isabs(normalized_rel):
            raise ValueError("relative_output_path must be relative")
        if os.path.splitdrive(normalized_rel)[0]:
            raise ValueError("relative_output_path must not contain a drive prefix")
        if normalized_rel in {".", ".."} or normalized_rel.startswith(f"..{os.sep}"):
            raise ValueError("relative_output_path escapes repository root")
        normalized_rel_unix = normalized_rel.replace("\\", "/")
        if normalized_rel_unix == ".git" or normalized_rel_unix.startswith(".git/"):
            raise ValueError("writing inside .git directory is not allowed")

        target_abs = os.path.abspath(os.path.join(repo_abs, normalized_rel))
        target_real = os.path.realpath(target_abs)
        repo_prefix = repo_real + os.sep
        if target_real != repo_real and not target_real.startswith(repo_prefix):
            raise ValueError("relative_output_path escapes repository root")

        os.makedirs(os.path.dirname(target_abs), exist_ok=True)
        with open(target_abs, "w", encoding="utf-8") as file:
            json.dump(profile, file, ensure_ascii=False, indent=2)

        git_rel = os.path.relpath(target_real, repo_real).replace("\\", "/")
        self._run_git_command(["git", "add", "--", git_rel], cwd=repo_abs)

        commit_attempted = bool(commit)
        commit_created = False
        commit_note = "Staged file with git add."
        resolved_message = (commit_message or "").strip() or f"Save Neurosonic profile {profile_id}"

        if commit:
            diff_result = self._run_git_command(
                ["git", "diff", "--cached", "--quiet", "--", git_rel],
                cwd=repo_abs,
                check=False,
            )
            if diff_result.returncode == 0:
                commit_note = "No staged changes detected for commit."
            else:
                self._run_git_command(
                    ["git", "commit", "-m", resolved_message, "--", git_rel],
                    cwd=repo_abs,
                )
                commit_created = True
                commit_note = "Commit created in user repository."

        return {
            "profile_id": profile_id,
            "repository_path": repo_real,
            "file_path": target_real,
            "relative_path": git_rel,
            "commit_attempted": commit_attempted,
            "commit_created": commit_created,
            "commit_message": resolved_message if commit else None,
            "notice": "User owns repository, credentials, subscriptions, and third-party contracts.",
            "status": commit_note,
            "updated_at": time.time(),
        }

    def _run_git_command(
        self,
        command: list[str],
        cwd: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        command_to_run = list(command)
        if command_to_run and command_to_run[0] == "git":
            null_hooks_path = "NUL" if os.name == "nt" else "/dev/null"
            command_to_run = [
                "git",
                "-c",
                f"core.hooksPath={null_hooks_path}",
                *command_to_run[1:],
            ]

        try:
            result = subprocess.run(
                command_to_run,
                cwd=cwd,
                text=True,
                capture_output=True,
                check=check,
            )
            return result
        except FileNotFoundError as exc:
            raise RuntimeError("git executable not found on system") from exc
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip() or (exc.stdout or "").strip()
            raise RuntimeError(f"git command failed: {stderr}") from exc


class UIDesignEngine:
    """Gjeneron një panel dinamik nga prompt-i i përdoruesit."""

    def generate_schema(
        self,
        prompt: str,
        preferences: dict[str, Any] | None = None,
        owner_id: str = "local-user",
    ) -> dict[str, Any]:
        preferences = preferences or {}
        detected_mode = self._detect_mode(prompt)
        theme = self._build_theme(preferences)
        widgets = self._build_widgets(prompt, detected_mode, preferences)

        return {
            "schema_version": "1.0",
            "owner_id": owner_id,
            "title": preferences.get("title", "My Neurosonic Panel"),
            "description": prompt.strip() or "Generated by Neurosonic UI Designer",
            "mode": detected_mode,
            "dna_contract": {
                "immutable": True,
                "message": "Backend DNA is immutable and never user-editable.",
            },
            "theme": theme,
            "layout": {
                "type": preferences.get("layout_type", "grid"),
                "columns": int(preferences.get("columns", 12)),
                "gap": int(preferences.get("gap", 16)),
            },
            "widgets": widgets,
            "integrations": {
                "plugins": [],
                "nodedb_fluid": {
                    "enabled": bool(preferences.get("nodedb_enabled", True)),
                    "storage": "local-device",
                },
                "tide": {
                    "enabled": bool(preferences.get("tide_enabled", True)),
                    "mode": preferences.get("tide_mode", "batica-zbatica"),
                },
                "llm_runtime": {
                    "target": preferences.get("llm_target", "local"),
                    "engine": preferences.get("llm_engine", "llama"),
                    "device_hint": preferences.get("llm_device_hint", "server-or-smartphone"),
                },
            },
            "compliance_notice": {
                "third_party_billing_responsibility": "user",
                "provider_contract_responsibility": "user",
                "service_role": "neurosonic-provides-api-support-only",
            },
            "actions": [
                {"id": "refresh", "label": "Refresh", "type": "api_call"},
                {"id": "save_layout", "label": "Save Layout", "type": "local_save"},
            ],
            "generated_at": time.time(),
        }

    def normalize_plugin(
        self,
        address: str,
        name: str | None = None,
        plugin_type: str = "auto",
        connector_scope: str = "general",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raw_address = (address or "").strip()
        resolved_type = self._classify_address(raw_address, plugin_type)
        plugin_name = name.strip() if isinstance(name, str) and name.strip() else raw_address
        plugin_id = f"plugin_{uuid.uuid4().hex[:10]}"
        now = time.time()
        normalized_scope = (connector_scope or "general").strip().lower()

        return {
            "id": plugin_id,
            "name": plugin_name,
            "address": raw_address,
            "address_type": resolved_type,
            "connector_scope": normalized_scope,
            "status": "active",
            "service_role": "api-support-only",
            "liability_model": "user-responsible-third-party-contracts",
            "metadata": metadata or {},
            "created_at": now,
            "updated_at": now,
        }

    def attach_plugin_to_schema(
        self,
        schema: dict[str, Any],
        plugin: dict[str, Any],
    ) -> dict[str, Any]:
        integrations = schema.setdefault("integrations", {})
        plugins = integrations.setdefault("plugins", [])

        existing_index = None
        for index, current in enumerate(plugins):
            if str(current.get("address", "")).strip().lower() == str(
                plugin.get("address", "")
            ).strip().lower():
                existing_index = index
                break

        if existing_index is None:
            plugins.append(plugin)
        else:
            plugin["id"] = plugins[existing_index].get("id", plugin.get("id"))
            plugin["created_at"] = plugins[existing_index].get(
                "created_at", plugin.get("created_at")
            )
            plugin["updated_at"] = time.time()
            plugins[existing_index] = plugin

        schema["updated_at"] = time.time()
        return schema

    def extract_plugins(self, schema: dict[str, Any]) -> list[dict[str, Any]]:
        integrations = schema.get("integrations", {}) if isinstance(schema, dict) else {}
        plugins = integrations.get("plugins", [])
        if not isinstance(plugins, list):
            return []
        return plugins

    def _detect_mode(self, prompt: str) -> str:
        text = prompt.lower()
        if any(token in text for token in ["image", "vision", "ocr", "scan", "foto"]):
            return "vision"
        if any(token in text for token in ["governance", "audit", "policy", "compliance"]):
            return "reasoning"
        if any(token in text for token in ["code", "debug", "developer", "api"]):
            return "code"
        return "text"

    def _classify_address(self, address: str, plugin_type: str) -> str:
        if plugin_type and plugin_type != "auto":
            return plugin_type

        text = address.strip().lower()
        if not text:
            return "unknown"
        if "@" in text and "://" not in text:
            return "email"
        if text.startswith(("bank://", "swift://", "iban://")):
            return "banking"
        if any(token in text for token in ["bank", "iban", "swift", "bic"]):
            return "banking"
        if text.startswith(("http://", "https://")):
            return "website"
        if text.startswith(("localhost", "127.0.0.1")):
            return "local-service"
        if text.startswith("/"):
            return "internal-api"
        if "://" in text:
            return "app-endpoint"
        if any(token in text for token in [".com", ".net", ".org", ".eu"]):
            return "website"
        return "generic-endpoint"

    def _build_theme(self, preferences: dict[str, Any]) -> dict[str, Any]:
        palette = preferences.get("palette", "neon-night")
        density = preferences.get("density", "comfortable")
        return {
            "palette": palette,
            "density": density,
            "font": preferences.get("font", "Inter"),
            "radius": preferences.get("radius", 12),
        }

    def _build_widgets(
        self, prompt: str, mode: str, preferences: dict[str, Any]
    ) -> list[dict[str, Any]]:
        widgets: list[dict[str, Any]] = [
            {
                "id": "welcome",
                "type": "hero",
                "title": preferences.get("hero_title", "Welcome Creator"),
                "subtitle": "Design your personal UI node",
                "span": {"col": 12, "row": 1},
            },
            {
                "id": "activity",
                "type": "timeline",
                "title": "Activity",
                "source": "/api/lightning/stats",
                "span": {"col": 6, "row": 2},
            },
            {
                "id": "health",
                "type": "status",
                "title": "System Health",
                "source": "/api/health",
                "span": {"col": 6, "row": 2},
            },
        ]

        if mode == "vision":
            widgets.append(
                {
                    "id": "vision_input",
                    "type": "image-dropzone",
                    "title": "Vision Input",
                    "action": "/api/lightning/scan",
                    "span": {"col": 12, "row": 2},
                }
            )
        elif mode == "reasoning":
            widgets.append(
                {
                    "id": "policy_matrix",
                    "type": "policy-grid",
                    "title": "Governance Matrix",
                    "source": "/api/dna",
                    "span": {"col": 12, "row": 2},
                }
            )
        elif mode == "code":
            widgets.append(
                {
                    "id": "api_console",
                    "type": "console",
                    "title": "API Console",
                    "action": "/api/shell/think",
                    "span": {"col": 12, "row": 2},
                }
            )
        else:
            widgets.append(
                {
                    "id": "notes",
                    "type": "markdown",
                    "title": "Personal Notes",
                    "content": prompt[:500],
                    "span": {"col": 12, "row": 2},
                }
            )

        return widgets

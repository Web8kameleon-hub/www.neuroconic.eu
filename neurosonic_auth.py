#!/usr/bin/env python3
"""Neurosonic Auth: regjistrim, login dhe verifikim token — zero varësi.

Përdor vetëm stdlib (hashlib, hmac, secrets) në përputhje me filozofinë
"Zero Dependencies" të bërthamës Neurosonic. Ruajtja bëhet lokalisht si
JSON, njësoj si `PersonalNodeStore` (neurosonic_ui_designer.py).

Fjalëkalimet hashohen me PBKDF2-HMAC-SHA256 (i disponueshëm në
`hashlib.pbkdf2_hmac`, pa varësi si bcrypt/argon2). Tokenat janë JWT
minimal (HS256) të nënshkruar me HMAC-SHA256, të kompatibël me
standardin JWT por të gjeneruar/verifikuar pa librari të jashtme.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import time
from typing import Any

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PBKDF2_ITERATIONS = 260_000
_TOKEN_TTL_SECONDS = 60 * 60 * 24 * 7  # 7 ditë default për sesionin e login-it


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _get_secret_key() -> bytes:
    """Çelësi i nënshkrimit të JWT. Në prodhim duhet vendosur NEUROSONIC_AUTH_SECRET."""
    secret = os.environ.get("NEUROSONIC_AUTH_SECRET")
    if not secret:
        # Fallback vetëm për zhvillim lokal — çdo restart e ndryshon,
        # duke pavlefshmëruar tokenat ekzistues. Në prodhim CAKTO env var.
        secret = "dev-insecure-secret-change-me"
    return secret.encode("utf-8")


class AuthError(Exception):
    """Gabim gjatë regjistrimit, login-it ose verifikimit të tokenit."""


class NeurosonicAuth:
    """Menaxhon përdoruesit dhe tokenat JWT, e ruajtur lokalisht si JSON."""

    def __init__(self, root_dir: str = "personal_node/auth"):
        self.root_dir = os.path.abspath(root_dir)
        os.makedirs(self.root_dir, exist_ok=True)
        self._users_path = os.path.join(self.root_dir, "users.json")

    # ------------------------------------------------------------------
    # Ruajtja e përdoruesve
    # ------------------------------------------------------------------

    def _load_users(self) -> dict[str, dict[str, Any]]:
        if not os.path.exists(self._users_path):
            return {}
        with open(self._users_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_users(self, users: dict[str, dict[str, Any]]) -> None:
        tmp_path = self._users_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as file:
            json.dump(users, file, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self._users_path)

    # ------------------------------------------------------------------
    # Hash fjalëkalimi (PBKDF2-HMAC-SHA256, pa varësi të jashtme)
    # ------------------------------------------------------------------

    @staticmethod
    def _hash_password(password: str, salt: bytes | None = None) -> str:
        salt = salt or secrets.token_bytes(16)
        derived = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS
        )
        return f"pbkdf2_sha256${_PBKDF2_ITERATIONS}${salt.hex()}${derived.hex()}"

    @staticmethod
    def _verify_password(password: str, encoded: str) -> bool:
        try:
            algo, iterations_str, salt_hex, hash_hex = encoded.split("$")
            if algo != "pbkdf2_sha256":
                return False
            iterations = int(iterations_str)
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(hash_hex)
        except (ValueError, AttributeError):
            return False

        derived = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, iterations
        )
        return hmac.compare_digest(derived, expected)

    # ------------------------------------------------------------------
    # JWT minimal (HS256), pa varësi të jashtme
    # ------------------------------------------------------------------

    def _issue_token(self, user_id: str, email: str, ttl_seconds: int = _TOKEN_TTL_SECONDS) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        now = int(time.time())
        payload = {
            "sub": user_id,
            "email": email,
            "iat": now,
            "exp": now + ttl_seconds,
        }
        header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
        signature = hmac.new(_get_secret_key(), signing_input, hashlib.sha256).digest()
        signature_b64 = _b64url_encode(signature)
        return f"{header_b64}.{payload_b64}.{signature_b64}"

    def verify_token(self, token: str) -> dict[str, Any]:
        """Verifikon nënshkrimin dhe skadimin e tokenit. Hedh AuthError nëse i pavlefshëm."""
        try:
            header_b64, payload_b64, signature_b64 = token.split(".")
        except ValueError as exc:
            raise AuthError("Token i keqformuar") from exc

        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
        expected_signature = hmac.new(_get_secret_key(), signing_input, hashlib.sha256).digest()
        try:
            actual_signature = _b64url_decode(signature_b64)
        except Exception as exc:
            raise AuthError("Nënshkrim i pavlefshëm") from exc

        if not hmac.compare_digest(expected_signature, actual_signature):
            raise AuthError("Nënshkrim i pavlefshëm")

        try:
            payload = json.loads(_b64url_decode(payload_b64))
        except Exception as exc:
            raise AuthError("Payload i pavlefshëm") from exc

        if payload.get("exp", 0) < int(time.time()):
            raise AuthError("Token i skaduar")

        return payload

    # ------------------------------------------------------------------
    # API publike: regjistrim / login / profil
    # ------------------------------------------------------------------

    def register(self, email: str, password: str) -> dict[str, Any]:
        email = (email or "").strip().lower()
        if not _EMAIL_RE.match(email):
            raise AuthError("Email i pavlefshëm")
        if not password or len(password) < 8:
            raise AuthError("Fjalëkalimi duhet të ketë të paktën 8 karaktere")

        users = self._load_users()
        if email in users:
            raise AuthError("Ky email është regjistruar tashmë")

        user_id = secrets.token_hex(16)
        users[email] = {
            "user_id": user_id,
            "email": email,
            "password_hash": self._hash_password(password),
            "created_at": time.time(),
            "entitlement": None,  # plotësohet nga Stripe pas pagesës
        }
        self._save_users(users)

        token = self._issue_token(user_id, email)
        return {"user_id": user_id, "email": email, "token": token}

    def login(self, email: str, password: str) -> dict[str, Any]:
        email = (email or "").strip().lower()
        users = self._load_users()
        user = users.get(email)
        if not user or not self._verify_password(password, user["password_hash"]):
            raise AuthError("Email ose fjalëkalim i gabuar")

        token = self._issue_token(user["user_id"], email)
        return {"user_id": user["user_id"], "email": email, "token": token}

    def get_user_by_email(self, email: str) -> dict[str, Any] | None:
        users = self._load_users()
        user = users.get((email or "").strip().lower())
        if not user:
            return None
        return {k: v for k, v in user.items() if k != "password_hash"}

    def set_entitlement(self, email: str, entitlement: dict[str, Any] | None) -> None:
        """Përditëson entitlement-in e përdoruesit (thirret nga Stripe webhook)."""
        email = (email or "").strip().lower()
        users = self._load_users()
        if email not in users:
            raise AuthError(f"Përdoruesi {email} nuk ekziston")
        users[email]["entitlement"] = entitlement
        self._save_users(users)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auth.py – Optional SSH session protection (research / defensive use)

This module demonstrates:
- secure password hashing (PBKDF2)
- timing-safe verification
- basic anti-bruteforce backoff
- environment-based feature toggling

⚠️ Disabled by default for GitHub / open-source usage.
"""

import os
import sys
import time
import json
import getpass
import hashlib
import hmac
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def _cfg_path() -> Path:
    return Path(os.getenv("GVA_CONFIG", "config.json"))

def _load_cfg() -> dict:
    p = _cfg_path()
    if p.is_file():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

# ---------------------------------------------------------------------------
# Password hashing / verification (demonstration-grade)
# ---------------------------------------------------------------------------

def _hash_password(password: str, iterations: int = 200_000) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256.
    Returns a portable string representation.
    """
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"

def _verify_password(password: str, stored: str) -> bool:
    """
    Verify a PBKDF2-HMAC-SHA256 password hash.
    """
    try:
        algo, it_s, salt_hex, dk_hex = stored.split("$", 3)
        if algo != "pbkdf2_sha256":
            return False
        iterations = int(it_s)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(dk_hex)
        candidate = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt, iterations
        )
        return hmac.compare_digest(candidate, expected)
    except Exception:
        return False

# ---------------------------------------------------------------------------
# SSH detection
# ---------------------------------------------------------------------------

def is_ssh_session() -> bool:
    """
    Detect whether the current process runs inside an SSH session.

    Disabled entirely when:
      GVA_DISABLE_SSH_GATE=1
    """
    if os.getenv("GVA_DISABLE_SSH_GATE"):
        return False
    return bool(os.getenv("SSH_CONNECTION") or os.getenv("SSH_TTY"))

# ---------------------------------------------------------------------------
# Interactive password gate (opt-in)
# ---------------------------------------------------------------------------

def _prompt_password(prompt: str = "🔐 SSH detected – enter password: ") -> str:
    try:
        return getpass.getpass(prompt)
    except Exception:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return sys.stdin.readline().rstrip("\n")

def require_password(
    expected_hash: Optional[str],
    max_attempts: int = 3,
) -> bool:
    """
    Require a password in SSH sessions.

    - Disabled by default (expected_hash must be provided)
    - Intended for research / demonstration only
    - No persistence or device binding
    """
    if not expected_hash:
        # Feature not configured → skip gate
        return True

    attempts = 0
    fails = 0

    while attempts < max_attempts:
        pwd = _prompt_password()
        if _verify_password(pwd, expected_hash):
            return True

        attempts += 1
        fails += 1
        remaining = max_attempts - attempts
        print(f"[❌] Invalid password. Remaining attempts: {remaining}")

        if remaining > 0:
            backoff = min(2 ** fails, 10)
            print(f"[⏳] Backoff active ({backoff}s)...")
            try:
                time.sleep(backoff)
            except KeyboardInterrupt:
                pass

    print("[❌] Access denied for this session.")
    return False


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reverse_shell.py – Controlled outbound connectivity demonstration

IMPORTANT:
This module intentionally does NOT implement a real reverse shell.

Purpose:
- demonstrate low-level socket handling
- show outbound connectivity patterns
- provide a safe, opt-in networking example for research and education

No shell, no command execution, no persistence.
"""

from __future__ import annotations

import os
import socket
from typing import Optional


def _get_demo_target() -> Optional[tuple[str, int]]:
    """
    Read demo target from environment variables.

    Required:
      GVA_DEMO_HOST
      GVA_DEMO_PORT
    """
    host = os.getenv("GVA_DEMO_HOST")
    port = os.getenv("GVA_DEMO_PORT")

    if not host or not port:
        return None

    try:
        return host, int(port)
    except ValueError:
        return None


def attempt_reverse_shell() -> bool:
    """
    Demonstrate an outbound TCP connection in a controlled, non-invasive way.

    Returns
    -------
    bool
        True if a connection could be established, False otherwise.
    """
    target = _get_demo_target()
    if not target:
        # Explicit opt-in required
        return False

    host, port = target

    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            # Send a harmless identification banner
            message = b"GhostVenumAI connectivity demo\n"
            sock.sendall(message)
        return True

    except OSError:
        return False


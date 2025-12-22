#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scanner.py – Nmap execution helper (defensive / research use)

This module provides a robust wrapper around nmap with:
- safe argument handling
- controlled privilege fallback (-sS → -sT)
- consistent text output for downstream analysis
- predictable behavior in restricted environments

Intended for:
- defensive security analysis
- network research
- automated reporting pipelines
"""

from __future__ import annotations

import shlex
import shutil
import subprocess
from typing import List, Tuple

# ---------------------------------------------------------------------------
# Binary discovery
# ---------------------------------------------------------------------------

NMAP_BIN: str = shutil.which("nmap") or "/usr/bin/nmap"

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _run(cmd: List[str], timeout: int = 900) -> Tuple[int, str]:
    """
    Execute a command and return (return_code, combined_output).

    Timeout default (900s) is chosen to support slow or large scans
    while still preventing indefinite hangs.
    """
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout or ""
    except subprocess.TimeoutExpired as e:
        return 124, f"[!] nmap timeout after {timeout}s\n{e.stdout or ''}"
    except FileNotFoundError:
        return 127, f"[!] nmap binary not found at: {NMAP_BIN}"
    except Exception as exc:
        return 1, f"[!] unexpected execution error: {exc}"


def _parse_args(args_str: str) -> List[str]:
    """
    Safely split an argument string into a list.
    Example: '-sS -T4 -v -sV' → ['-sS', '-T4', '-v', '-sV']
    """
    return shlex.split(args_str or "")


def _uses_syn_scan(args: List[str]) -> bool:
    """Return True if SYN scan (-sS) is requested."""
    return "-sS" in args

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_nmap_scan(target: str, args_str: str) -> str:
    """
    Execute an nmap scan and ALWAYS return the full textual output.

    Strategy:
    - If SYN scan (-sS) is requested:
        1) Try 'sudo -n' (non-interactive, if sudoers allows)
        2) Try without sudo (for setcap-enabled binaries)
        3) If root privileges are required → fallback to -sT
    - Without -sS: run directly without privilege escalation

    This function never raises and always returns a string
    suitable for logging, reporting, or AI-based analysis.
    """
    if not target:
        return "[!] No target specified."

    args = _parse_args(args_str)
    base_cmd = [NMAP_BIN] + args + [target]

    # ------------------------------------------------------------------
    # SYN scan handling with graceful fallback
    # ------------------------------------------------------------------
    if _uses_syn_scan(args):
        # 1) Try sudo -n (fast path, no prompt)
        rc, out = _run(["sudo", "-n"] + base_cmd)
        if rc == 0:
            return out

        # 2) Try without sudo (setcap scenario)
        rc2, out2 = _run(base_cmd)
        if rc2 == 0:
            return out2

        # 3) Root required → fallback to TCP connect scan (-sT)
        lower_out = out2.lower()
        if "requires root" in lower_out or "quitting!" in lower_out:
            fallback_args = [a for a in args if a != "-sS"]
            fallback_cmd = [NMAP_BIN] + fallback_args + [target]
            rc3, out3 = _run(fallback_cmd)
            header = (
                "[i] Privileged SYN scan unavailable. "
                "Falling back to TCP connect scan (-sT).\n"
            )
            return header + out3

        return out2

    # ------------------------------------------------------------------
    # Non-privileged scan path
    # ------------------------------------------------------------------
    _, out = _run(base_cmd)
    return out


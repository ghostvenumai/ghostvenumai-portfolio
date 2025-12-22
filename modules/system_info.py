#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
system_info.py – Local system information collection

This module gathers basic, non-invasive system metadata for
diagnostics and reporting purposes.

Design goals:
- no external services
- cross-platform best effort
- defensive and privacy-aware
"""

from __future__ import annotations

import socket
import platform
import uuid
from typing import Dict, Optional

try:
    import netifaces as ni  # optional dependency
except ImportError:
    ni = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _detect_primary_ip() -> Optional[str]:
    """
    Attempt to determine the primary local IPv4 address.

    Strategy:
    1) Prefer active non-loopback interfaces via netifaces (if available)
    2) Fallback to UDP socket trick without sending traffic

    Returns
    -------
    Optional[str]
        Detected IPv4 address or None if unavailable.
    """
    if ni:
        try:
            for iface in ni.interfaces():
                if iface.startswith(("lo", "docker", "veth")):
                    continue
                addrs = ni.ifaddresses(iface).get(ni.AF_INET, [])
                for entry in addrs:
                    ip = entry.get("addr")
                    if ip and not ip.startswith("127."):
                        return ip
        except Exception:
            pass  # silent fallback

    # Fallback: UDP socket trick (no packets sent)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except Exception:
        return None
    finally:
        sock.close()


def _format_mac_address() -> str:
    """
    Format the local MAC address in human-readable form.
    """
    mac = uuid.getnode()
    return ":".join(
        f"{(mac >> ele) & 0xff:02x}"
        for ele in range(0, 8 * 6, 8)
    )[::-1]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def collect_system_info() -> Dict[str, str]:
    """
    Collect basic system metadata.

    Returns
    -------
    Dict[str, str]
        Dictionary containing hostname, IP address, platform details,
        architecture, and MAC address.
    """
    return {
        "hostname": socket.gethostname(),
        "ip_address": _detect_primary_ip() or "unknown",
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "mac_address": _format_mac_address(),
    }


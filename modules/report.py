#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report.py – Lightweight text report generation for Nmap scan results

This module:
- parses a subset of Nmap output conservatively
- extracts basic port/service information
- generates a human-readable text report

Intended use:
- defensive security analysis
- research and education
- automated reporting pipelines
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

PortEntry = Dict[str, object]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_PORT_LINE_RE = re.compile(
    r"^\s*(\d+)\/(tcp|udp)\s+(\w+)\s+([^\s]+)(.*)$"
)

def _ensure_parent(path: Path) -> None:
    """Ensure that the parent directory of a file path exists."""
    path.parent.mkdir(parents=True, exist_ok=True)

def _parse_ports(nmap_text: str) -> List[PortEntry]:
    """
    Conservatively parse open port information from Nmap output.

    Only lines that closely match typical Nmap port table rows
    are considered. This avoids false positives.
    """
    ports: List[PortEntry] = []

    for line in nmap_text.splitlines():
        m = _PORT_LINE_RE.match(line)
        if not m:
            continue

        port, proto, state, service, extra = m.groups()
        ports.append(
            {
                "port": int(port),
                "protocol": proto,
                "state": state,
                "service": service,
                "details": extra.strip(),
            }
        )

    return ports

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_report(
    nmap_text: str,
    out_path: Optional[str] = None,
) -> Path:
    """
    Create a plain-text report from raw Nmap output.

    Parameters
    ----------
    nmap_text : str
        Raw textual output produced by Nmap.
    out_path : str, optional
        Output file path. Defaults to './report.txt'.

    Returns
    -------
    Path
        Path to the written report file.
    """
    if not nmap_text:
        nmap_text = ""

    output = Path(out_path or "report.txt")
    _ensure_parent(output)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    ports = _parse_ports(nmap_text)

    lines: List[str] = []

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------
    lines.append(f"GhostVenumAI Report")
    lines.append(f"Generated: {timestamp}")
    lines.append("=" * 72)
    lines.append("")

    # ------------------------------------------------------------------
    # Nmap preview
    # ------------------------------------------------------------------
    lines.append("Nmap Output Preview (first 30 lines)")
    lines.append("-" * 72)
    for line in nmap_text.splitlines()[:30]:
        lines.append(line)
    lines.append("")

    # ------------------------------------------------------------------
    # Parsed ports
    # ------------------------------------------------------------------
    lines.append("Detected Open Ports (conservative parser)")
    lines.append("-" * 72)

    if ports:
        for p in ports:
            lines.append(
                f"{p['port']}/{p['protocol']}  "
                f"{p['state']}  "
                f"{p['service']}  "
                f"{p['details']}"
            )
    else:
        lines.append("No ports matched the conservative parser rules.")

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


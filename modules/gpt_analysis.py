#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gpt_analysis.py – AI-assisted interpretation of Nmap scan results

This module demonstrates:
- structured prompt engineering
- safe OpenAI SDK (>=1.0) usage
- environment-based secret handling
- deterministic, review-friendly output

Intended use:
- defensive security analysis
- research and education
- automated reporting pipelines
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

# OpenAI SDK (>= 1.0)
try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_MODEL = os.getenv("GVA_OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_OUT_DIR = Path(os.getenv("GVA_OUTPUT_DIR", "output"))

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_output_dir() -> None:
    DEFAULT_OUT_DIR.mkdir(parents=True, exist_ok=True)

def _load_openai_key() -> Optional[str]:
    """
    Load OpenAI API key from environment.

    Supported variables:
      - OPENAI_API_KEY
      - GVA_OPENAI_KEY
    """
    return os.getenv("OPENAI_API_KEY") or os.getenv("GVA_OPENAI_KEY")

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_scan_with_gpt(nmap_output: str) -> Path:
    """
    Analyze textual Nmap output using an LLM and store the result as a text file.

    Parameters
    ----------
    nmap_output : str
        Raw Nmap scan output.

    Returns
    -------
    Path
        Path to the generated analysis file.

    Raises
    ------
    RuntimeError
        If the OpenAI SDK or API key is unavailable.
    ValueError
        If no scan output is provided.
    """
    if not nmap_output or not nmap_output.strip():
        raise ValueError("No Nmap output provided for analysis.")

    if OpenAI is None:
        raise RuntimeError(
            "OpenAI SDK not installed. "
            "Install with: pip install openai>=1.0.0"
        )

    api_key = _load_openai_key()
    if not api_key:
        raise RuntimeError(
            "OpenAI API key not found. "
            "Set OPENAI_API_KEY or GVA_OPENAI_KEY."
        )

    _ensure_output_dir()

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are a defensive security analyst.\n\n"
        "Analyze the following Nmap scan output and provide a concise, "
        "structured assessment:\n"
        "1) Target overview and high-level summary\n"
        "2) Open ports with detected services/versions (short list)\n"
        "3) Potential security risks or misconfigurations (qualitative)\n"
        "4) Overall risk level (Low / Medium / High) with reasoning\n"
        "5) Recommended defensive next steps\n\n"
        "Be precise and technical. Avoid speculation and unnecessary verbosity."
    )

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": nmap_output},
        ],
    )

    content = response.choices[0].message.content or ""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    out_file = DEFAULT_OUT_DIR / f"gpt_analysis_{timestamp}.txt"

    out_file.write_text(content, encoding="utf-8")

    return out_file


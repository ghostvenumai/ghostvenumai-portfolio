#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI API-Key Verwaltung:
- ensure_openai_key(cfg_path): fragt nur, wenn leer; speichert in config.json
- CLI:
    python3 -m modules.api_key --set sk-...   # Key setzen/ändern
    python3 -m modules.api_key --clear        # Key löschen
    python3 -m modules.api_key --path config.json
ENV-Override (nur Laufzeit, ohne Speichern):
    GVA_OPENAI_KEY=sk-... python3 main.py
"""
from __future__ import annotations
import os, json, sys, getpass
from pathlib import Path

try:
    from modules.i18n_quick import _
except Exception:
    def _(k, **kw): return kw.get("fallback", k)

def _load_cfg(p: Path) -> dict:
    if p.is_file():
        try: return json.loads(p.read_text(encoding="utf-8"))
        except Exception: pass
    return {}

def _save_cfg(p: Path, d: dict):
    tmp = Path(str(p)+".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    tmp.replace(p)

def get_openai_key(cfg_path: str | Path = "config.json") -> str:
    env = os.getenv("GVA_OPENAI_KEY", "").strip()
    if env: return env
    d = _load_cfg(Path(cfg_path))
    return str(d.get("openai_key","") or "").strip()

def ensure_openai_key(cfg_path: str | Path = "config.json", prompt_if_missing=True) -> str:
    key = get_openai_key(cfg_path)
    if key: return key
    if not prompt_if_missing: return ""
    print("\n" + _("apikey.prompt", fallback="🔑 Please enter your OpenAI API key (stored locally in config.json)."))
    print(_("apikey.hint", fallback="Format usually starts with 'sk-' or 'sk-proj-'. You can paste it here."))
    try: entered = getpass.getpass("API key: ").strip()
    except Exception: entered = input("API key: ").strip()
    if not entered:
        print(_("apikey.missing", fallback="⚠️ No API key entered. GPT features will be skipped."))
        return ""
    p = Path(cfg_path); d = _load_cfg(p); d["openai_key"] = entered; _save_cfg(p, d)
    print(_("apikey.saved", fallback="✅ API key saved to config.json."))
    return entered

def _cli():
    cfg = "config.json"; args = sys.argv[1:]
    if "--path" in args:
        i = args.index("--path")
        if i+1 < len(args): cfg = args[i+1]
    if "--clear" in args:
        p=Path(cfg); d=_load_cfg(p); d.pop("openai_key", None); _save_cfg(p,d)
        print(_("apikey.cleared", fallback="✅ API key removed from config.json.")); return
    if "--set" in args:
        j = args.index("--set")
        if j+1 < len(args):
            key = args[j+1].strip()
            p=Path(cfg); d=_load_cfg(p); d["openai_key"]=key; _save_cfg(p,d)
            print(_("apikey.saved", fallback="✅ API key saved to config.json.")); return
    ensure_openai_key(cfg, prompt_if_missing=True)

if __name__ == "__main__":
    _cli()

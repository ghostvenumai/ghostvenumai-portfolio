#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GhostVenumAI – Quick i18n (de/en/es) in EINER Datei
- Erststart: 1/2/3 Sprachwahl, Speicherung in config.json
- Später ändern:  python3 -m modules.i18n_quick --set de|en|es
- Nutzung im Code: from modules.i18n_quick import _, ensure_language_once
"""
from __future__ import annotations
import json, sys
from pathlib import Path

TR = {
    "de": {
        "app.name": "GhostVenumAI",
        "app.banner": "GhostVenumAI — Sicherheit von Anfang an",
        "status.ready": "Bereit.",
        "status.error": "Fehler: {message}",
        "config.load_error": "Fehler beim Laden der config.json: {message}",
        "app.start": "[GhostVenumAI V3] 🚀 Starte Sicherheitstool...",
        "label.target_ip": "Ziel-IP",
        "label.nmap_args": "Nmap-Parameter",
        "action.start_nmap": "Starte Nmap-Scan...",
        "nmap.preview": "Nmap-Output (erste Zeilen):",
        "nmap.no_result": "Kein Scan-Ergebnis erhalten.",
        "gpt.start": "Starte GPT-Auswertung...",
        "gpt.saved": "GPT-Analyse gespeichert unter: {path}",
        "gpt.failed": "GPT-Analyse fehlgeschlagen: {error}",
        "gpt.skip_no_data": "Überspringe GPT-Analyse – keine Scan-Daten.",
        "report.create": "Erzeuge Sicherheitsreport...",
        "report.saved_fixed": "Report gespeichert unter: report.txt",
        "report.error": "Fehler beim Erstellen des Reports: {error}",
        "sysinfo.collect": "Systeminformationen sammeln...",
        "sysinfo.error": "Fehler beim Sammeln der Systeminformationen: {error}",
        "shell.try": "Versuche Reverse Shell...",
        "shell.failed": "Reverse shell fehlgeschlagen: {error}",
        "app.done": "GhostVenumAI V3 abgeschlossen.",
        "settings.language": "Sprache",
        "settings.saved": "Einstellungen gespeichert.",
        "lang.prompt.title": "=== Sprache wählen / Choose language / Elige idioma ===",
        "lang.prompt.options": "[1] Deutsch    [2] English    [3] Español",
        "lang.prompt.hint": "(1/2/3, Enter = {default}) ",
        "lang.set.to": "Sprache gesetzt auf: {human} ({code})"
    },
    "en": {
        "app.name": "GhostVenumAI",
        "app.banner": "GhostVenumAI — secure by design",
        "status.ready": "Ready.",
        "status.error": "Error: {message}",
        "config.load_error": "Error loading config.json: {message}",
        "app.start": "[GhostVenumAI V3] 🚀 Starting security tool...",
        "label.target_ip": "Target IP",
        "label.nmap_args": "Nmap params",
        "action.start_nmap": "Starting Nmap scan...",
        "nmap.preview": "Nmap output (first lines):",
        "nmap.no_result": "No scan result received.",
        "gpt.start": "Starting GPT analysis...",
        "gpt.saved": "GPT analysis saved to: {path}",
        "gpt.failed": "GPT analysis failed: {error}",
        "gpt.skip_no_data": "Skipping GPT analysis – no scan data.",
        "report.create": "Creating security report...",
        "report.saved_fixed": "Report saved at: report.txt",
        "report.error": "Error creating report: {error}",
        "sysinfo.collect": "Collecting system information...",
        "sysinfo.error": "Error collecting system information: {error}",
        "shell.try": "Trying reverse shell...",
        "shell.failed": "Reverse shell failed: {error}",
        "app.done": "GhostVenumAI V3 finished.",
        "settings.language": "Language",
        "settings.saved": "Settings saved.",
        "lang.prompt.title": "=== Sprache wählen / Choose language / Elige idioma ===",
        "lang.prompt.options": "[1] Deutsch    [2] English    [3] Español",
        "lang.prompt.hint": "(1/2/3, Enter = {default}) ",
        "lang.set.to": "Language set to: {human} ({code})"
    },
    "es": {
        "app.name": "GhostVenumAI",
        "app.banner": "GhostVenumAI — seguridad desde el diseño",
        "status.ready": "Listo.",
        "status.error": "Error: {message}",
        "config.load_error": "Error al cargar config.json: {message}",
        "app.start": "[GhostVenumAI V3] 🚀 Iniciando herramienta de seguridad...",
        "label.target_ip": "IP de destino",
        "label.nmap_args": "Parámetros de Nmap",
        "action.start_nmap": "Iniciando escaneo Nmap...",
        "nmap.preview": "Salida de Nmap (primeras líneas):",
        "nmap.no_result": "No se recibió resultado del escaneo.",
        "gpt.start": "Iniciando análisis con GPT...",
        "gpt.saved": "Análisis GPT guardado en: {path}",
        "gpt.failed": "Error en el análisis GPT: {error}",
        "gpt.skip_no_data": "Se omite el análisis con GPT: no hay datos de escaneo.",
        "report.create": "Creando informe de seguridad...",
        "report.saved_fixed": "Informe guardado en: report.txt",
        "report.error": "Error al crear el informe: {error}",
        "sysinfo.collect": "Recopilando información del sistema...",
        "sysinfo.error": "Error al recopilar información del sistema: {error}",
        "shell.try": "Intentando reverse shell...",
        "shell.failed": "Falló la reverse shell: {error}",
        "app.done": "GhostVenumAI V3 finalizado.",
        "settings.language": "Idioma",
        "settings.saved": "Ajustes guardados.",
        "lang.prompt.title": "=== Sprache wählen / Choose language / Elige idioma ===",
        "lang.prompt.options": "[1] Deutsch    [2] English    [3] Español",
        "lang.prompt.hint": "(1/2/3, Enter = {default}) ",
        "lang.set.to": "Idioma configurado a: {human} ({code})"
    }
}
_VALID = {"de","en","es"}
_HUMAN = {"de":"Deutsch","en":"English","es":"Español"}
_LANG = "de"

def _fmt(txt: str, kw: dict) -> str:
    if not kw: return txt
    try:
        class _D(dict):
            def __missing__(self, k): return "{"+k+"}"
        return txt.format_map(_D(**kw))
    except Exception:
        return txt

def set_language(code: str) -> str:
    global _LANG
    _LANG = code if code in _VALID else "de"
    return _LANG

def get_language() -> str:
    return _LANG

def _(key: str, **kw) -> str:
    return _fmt(TR.get(_LANG, {}).get(key) or TR["en"].get(key) or key, kw)

def _load_cfg(p: Path) -> dict:
    if p.is_file():
        try: return json.loads(p.read_text(encoding="utf-8"))
        except Exception: pass
    return {}

def _save_cfg(p: Path, d: dict):
    tmp = Path(str(p)+".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    tmp.replace(p)

def ensure_language_once(cfg_path: str | Path = "config.json", default="de") -> str:
    p = Path(cfg_path)
    d = _load_cfg(p)
    code = str(d.get("language","")).strip().lower()
    if code in _VALID:
        set_language(code); return code
    print(); print(_("lang.prompt.title")); print(_("lang.prompt.options"))
    print(_(
        "lang.prompt.hint",
        default=default
    ), end="", flush=True)
    choice = (input().strip() or "")
    code = {"1":"de","2":"en","3":"es"}.get(choice, default)
    set_language(code)
    d["language"] = code
    try:
        _save_cfg(p, d)
        print(_("lang.set.to", human=_HUMAN[code], code=code))
        print(_("settings.saved"))
    except Exception as e:
        print(_("status.error", message=str(e)))
    return code

def _cli():
    cfg = "config.json"
    args = sys.argv[1:]
    if "--path" in args:
        i = args.index("--path")
        if i+1 < len(args): cfg = args[i+1]
    if "--set" in args:
        j = args.index("--set")
        if j+1 < len(args):
            code = args[j+1].strip().lower()
            if code not in _VALID:
                print("Use --set de|en|es"); sys.exit(2)
            p = Path(cfg); d = _load_cfg(p)
            d["language"] = code; _save_cfg(p, d); set_language(code)
            print(_("lang.set.to", human=_HUMAN[code], code=code))
            print(_("settings.saved")); return
    ensure_language_once(cfg, default="de")

if __name__ == "__main__":
    _cli()


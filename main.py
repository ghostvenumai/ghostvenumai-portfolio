import os
import sys
import json
import time

# === Sprache (einmalig fragen & setzen) ======================================
from modules.i18n_quick import _, ensure_language_once
CFG_PATH = os.getenv("GVA_CONFIG", "config.json")
ensure_language_once(CFG_PATH, default="de")
# ============================================================================

# === OpenAI API-Key sicherstellen (nur fragen, wenn leer) ====================
from modules.api_key import ensure_openai_key, get_openai_key
OPENAI_KEY = ensure_openai_key(CFG_PATH, prompt_if_missing=True)
# ============================================================================

# ---- Defaults (verhindert NameError) ----
TARGET_IP = ""
NMAP_ARGS = "-sS -T4 -v -sV"

# ---- Config laden (überschreibt Defaults) ----
try:
    with open("config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)
        TARGET_IP = cfg.get("target", TARGET_IP)
        NMAP_ARGS = cfg.get("nmap_args", NMAP_ARGS)
except Exception as e:
    print("❌ " + _("config.load_error", message=str(e)))

# ---- SSH-Gate (Passwort nur bei SSH) ----
from modules.auth import is_ssh_session, require_password
if is_ssh_session():
    if not require_password():
        print("❌ " + _("status.error", message="Zugriff verweigert (SSH-Passwort falsch/abgebrochen)."))
        sys.exit(1)

# ---- Restliche Module erst nach Gate laden ----
from modules.scanner import run_nmap_scan
from modules.report import create_report
from modules.system_info import collect_system_info
from modules.reverse_shell import attempt_reverse_shell
from modules.gpt_analysis import analyze_scan_with_gpt

# ---- Hilfsfunktionen ----
def detect_gateway():
    try:
        route_info = os.popen("ip route | grep default").read()
        return route_info.split()[2]
    except Exception:
        return None

def detect_laptop_ip():
    try:
        arp_output = os.popen("arp -a").read()
        for line in arp_output.splitlines():
            if "wlan0" in line or "eth0" in line or "b8:" in line or "dc:" in line:
                return line.split("(")[1].split(")")[0]
    except Exception:
        return None

print(f"\n{_('app.start')}\n")

# Ziel-IP bestimmen
if not TARGET_IP:
    TARGET_IP = detect_laptop_ip() or detect_gateway() or "192.168.0.1"

print(f"🌐 {_('label.target_ip')}: {TARGET_IP}")
print(f"⚙️ {_('label.nmap_args')}: {NMAP_ARGS}")
print(f"🔎 {_('action.start_nmap')}\n")

# Nmap (liefert IMMER String)
scan_text = run_nmap_scan(TARGET_IP, NMAP_ARGS)

if scan_text:
    preview = "\n".join(scan_text.splitlines()[:10])
    print("🛠️  " + _("nmap.preview") + "\n" + preview)
else:
    print("⚠️ " + _("nmap.no_result"))

# GPT-Auswertung (nur wenn API-Key vorhanden)
if OPENAI_KEY and scan_text and scan_text.strip():
    try:
        print("\n🤖 " + _("gpt.start"))
        out_path = analyze_scan_with_gpt(scan_text)
        print("📄 " + _("gpt.saved", path=out_path))
    except Exception as e:
        print("❌ " + _("gpt.failed", error=str(e)))
else:
    if not OPENAI_KEY:
        print("⚠️ Skipping GPT analysis – no API key set.")
    else:
        print("⚠️ " + _("gpt.skip_no_data"))

# Report
print("\n📄 " + _("report.create"))
try:
    create_report(scan_text)  # erwartet String
    print("📁 " + _("report.saved_fixed"))
except Exception as e:
    print("❌ " + _("report.error", error=str(e)))

# Systeminfos
print("\n📊 " + _("sysinfo.collect"))
try:
    info = collect_system_info()
    print(info)
except Exception as e:
    print("❌ " + _("sysinfo.error", error=str(e)))

# Reverse Shell
print("\n🔁 " + _("shell.try"))
try:
    attempt_reverse_shell()
except Exception as e:
    print("[!] " + _("shell.failed", error=str(e)))

print("\n🎯 " + _("app.done"))

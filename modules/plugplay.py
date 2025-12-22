# modules/plugplay.py
import os
import time
import ipaddress
import subprocess
from datetime import datetime

from modules.scanner import run_nmap_scan
from modules.gpt_analysis import analyze_scan_with_gpt
from modules.report import create_report

LOGDIR = "logs"

# Doppelstarts dämpfen (wenn Dispatcher mehrfach feuert)
LOCK = "/tmp/ghostvenum_plugplay.lock"
COOLDOWN_SEC = 120  # 2 Minuten

def _ensure_dirs():
    os.makedirs(LOGDIR, exist_ok=True)

def _acquire_lock():
    try:
        if os.path.exists(LOCK):
            if (time.time() - os.path.getmtime(LOCK)) < COOLDOWN_SEC:
                print("[Plug&Play] Cooldown aktiv – Scan übersprungen.")
                return False
        with open(LOCK, "w") as f:
            f.write(str(os.getpid()))
        return True
    except Exception:
        return True

def _release_lock():
    try:
        if os.path.exists(LOCK):
            os.remove(LOCK)
    except Exception:
        pass

def _sh(cmd: str) -> str:
    return subprocess.check_output(["sh", "-lc", cmd], text=True).strip()

def _gateway_for_iface(iface: str) -> str | None:
    """
    Versucht das Gateway/Peer für ein Interface zu finden.
    1) 'ip route show dev IFACE' → default via x.x.x.x
    2) 'ip neigh show dev IFACE' → erstes erreichbares Nachbar-IP
    3) Heuristik: .1 im lokalen Netz pingen und zurückgeben, falls erreichbar
    """
    # 1) Default-Gateway auf diesem IF
    try:
        out = _sh(f"ip -4 route show dev {iface} | awk '$1==\"default\" {{print $3; exit}}'")
        if out:
            return out
    except Exception:
        pass

    # 2) Nachbarn (ARP/NDP)
    try:
        # Beispielzeile: "192.168.178.1 dev eth0 lladdr xx:xx:xx:xx:xx:xx REACHABLE"
        neigh = _sh(f"ip -4 neigh show dev {iface} | awk '($NF==\"REACHABLE\"||$NF==\"STALE\"||$NF==\"DELAY\"||$NF==\"PROBE\"){{print $1; exit}}'")
        if neigh:
            return neigh
    except Exception:
        pass

    return None

def _cidr_from_ip_mask(ip_str: str, mask_str: str) -> str | None:
    try:
        return str(ipaddress.IPv4Network((ip_str, mask_str), strict=False))
    except Exception:
        return None

def _guess_dot1(cidr: str) -> str | None:
    try:
        net = ipaddress.ip_network(cidr, strict=False)
        # erstes Host im Netz (typisch .1)
        first = str(list(net.hosts())[0]) if net.num_addresses >= 4 else None
        return first
    except Exception:
        return None

def run_plug_and_play(interface: str, ip_address: str, subnet: str, nmap_args: str = "-sS -T4 -v -sV"):
    """
    Wird vom Dispatcher-Runner aufgerufen.
    Scannt NUR das Gegenüber (Gateway/Peer) statt das ganze Subnetz.
    """
    _ensure_dirs()
    if not _acquire_lock():
        return

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    try:
        # Peer/Gateway ermitteln
        peer = _gateway_for_iface(interface)
        if not peer:
            cidr = _cidr_from_ip_mask(ip_address, subnet)
            if cidr:
                peer = _guess_dot1(cidr)

        if not peer:
            print(f"[Plug&Play] Kein Peer/Gateway gefunden (IF={interface}). Abbruch.")
            return

        print(f"[Plug&Play] IF={interface} IP={ip_address} → Peer={peer}")
        scan_text = run_nmap_scan(peer, nmap_args)

        base = os.path.join(LOGDIR, f"{interface}_{ts}")
        with open(base + "_nmap.txt", "w", encoding="utf-8") as f:
            f.write(scan_text or "")

        if scan_text and scan_text.strip():
            try:
                gpt_path = analyze_scan_with_gpt(scan_text)
                print(f"[Plug&Play] GPT-Analyse: {gpt_path}")
            except Exception as e:
                print(f"[Plug&Play] GPT fehlgeschlagen: {e}")

        try:
            create_report(scan_text)
            print(f"[Plug&Play] Report aktualisiert: report.txt")
        except Exception as e:
            print(f"[Plug&Play] Report-Fehler: {e}")

    finally:
        _release_lock()

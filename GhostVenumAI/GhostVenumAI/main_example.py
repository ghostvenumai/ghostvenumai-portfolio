"""
GhostVenumAI - Minimal Demo Entry Point

This is NOT the full project.
It only shows how I structure code and connect modules.
"""

from analysis_module_example import analyze_scan_result


def simulate_scan():
    """
    In the real project, this would be real nmap output.
    Here we just return a small simulated scan list.
    """
    return [
        {"ip": "192.168.0.10", "port": 22, "service": "ssh"},
        {"ip": "192.168.0.10", "port": 80, "service": "http"},
        {"ip": "192.168.0.10", "port": 3389, "service": "rdp"},
    ]


def main():
    print("=== GhostVenumAI Demo ===")
    scan_results = simulate_scan()

    for entry in scan_results:
        ip = entry["ip"]
        port = entry["port"]
        service = entry["service"]
        print(f"\n[+] Analysing {ip}:{port} ({service})")
        ai_summary = analyze_scan_result(entry)
        print("AI Summary:", ai_summary)


if __name__ == "__main__":
    main()

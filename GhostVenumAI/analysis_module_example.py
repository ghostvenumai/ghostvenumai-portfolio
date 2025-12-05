"""
GhostVenumAI - Simplified Analysis Module

In the real project, this logic is much more complex and uses GPT models.
Here we show a small rule-based example to illustrate the concept.
"""


def analyze_scan_result(entry: dict) -> str:
    port = entry.get("port")
    service = entry.get("service", "").lower()

    # Very simplified rule-based logic (for demo only)
    if port == 22 or "ssh" in service:
        return (
            "SSH service detected. "
            "Check for key-based authentication only, disable password login, "
            "and limit access to trusted IP ranges."
        )

    if port == 3389 or "rdp" in service:
        return (
            "RDP service detected. "
            "Consider VPN-only access, strong credentials and account lockout policies."
        )

    if port in (80, 443) or "http" in service:
        return (
            "Web service detected. "
            "Check for HTTPS, security headers, up-to-date software and hardened configs."
        )

    return (
        "No specific issues detected in this simple demo. "
        "The real GhostVenumAI uses AI for deeper context-aware analysis."
    )

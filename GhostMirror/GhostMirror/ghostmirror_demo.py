"""
GhostMirror - Minimal Demo

Simulates network "events" and shows how they could be sent
to an AI model for explanation (here we just emulate the AI response).
"""

from typing import Dict, List


def get_simulated_events() -> List[Dict]:
    return [
        {
            "src_ip": "10.0.0.5",
            "dst_ip": "8.8.8.8",
            "dst_port": 53,
            "protocol": "udp",
        },
        {
            "src_ip": "10.0.0.5",
            "dst_ip": "91.198.174.192",
            "dst_port": 80,
            "protocol": "tcp",
        },
        {
            "src_ip": "10.0.0.5",
            "dst_ip": "203.0.113.50",
            "dst_port": 4444,
            "protocol": "tcp",
        },
    ]


def fake_ai_explain(event: Dict) -> str:
    """
    In the real project this would call the OpenAI API.
    Here we just return a static explanation based on simple rules.
    """
    port = event["dst_port"]

    if port == 53:
        return "This looks like normal DNS traffic resolving domain names."
    if port == 80:
        return "HTTP traffic, probably a normal web request."
    if port >= 1024 and port not in (80, 443):
        return (
            "Unusual high port. Could be a custom service, tunnel, or reverse shell. "
            "Should be reviewed in more detail."
        )

    return "No clear conclusion in this demo."


def main():
    print("=== GhostMirror Demo ===")
    events = get_simulated_events()

    for ev in events:
        print(
            f"\n[EVENT] {ev['src_ip']} -> {ev['dst_ip']}:{ev['dst_port']} "
            f"({ev['protocol']})"
        )
        explanation = fake_ai_explain(ev)
        print("AI-style explanation:", explanation)


if __name__ == "__main__":
    main()

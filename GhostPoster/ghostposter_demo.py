"""
GhostPoster - Minimal Demo

Builds simple "post" objects and simulates AI-generated content.
No real API calls in this public demo.
"""


def build_post(topic: str, platform: str) -> dict:
    # In the real project, GPT would generate the text and tone.
    text = f"Short demo post about '{topic}' for {platform}."
    return {
        "platform": platform,
        "topic": topic,
        "text": text,
        "hashtags": ["#demo", "#ai", "#ghostposter"],
    }


def main():
    print("=== GhostPoster Demo ===")

    topics = ["AI security", "network visibility", "automation"]
    platforms = ["Twitter", "Reddit"]

    for t in topics:
        for p in platforms:
            post = build_post(t, p)
            print(f"\n[POST for {p}]")
            print("Topic:", post["topic"])
            print("Text:", post["text"])
            print("Hashtags:", " ".join(post["hashtags"]))


if __name__ == "__main__":
    main()

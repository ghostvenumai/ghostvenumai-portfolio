"""
GhostShield - Minimal Demo

Takes simulated "file metadata" and assigns rough risk levels.
In the real project, AI models would help to explain and classify behaviour.
"""


def classify_file(file_info: dict) -> str:
    name = file_info.get("name", "").lower()
    signed = file_info.get("signed", False)
    from_internet = file_info.get("from_internet", False)

    if not signed and from_internet and name.endswith(".exe"):
        return "High risk: unsigned executable downloaded from the internet."
    if name.endswith(".dll") and not signed:
        return "Medium risk: unsigned library (DLL). Further review recommended."
    return "Low risk in this simple demo."


def main():
    print("=== GhostShield Demo ===")

    samples = [
        {"name": "setup.exe", "signed": False, "from_internet": True},
        {"name": "system.dll", "signed": False, "from_internet": False},
        {"name": "document.pdf", "signed": True, "from_internet": True},
    ]

    for s in samples:
        print(f"\n[FILE] {s}")
        result = classify_file(s)
        print("Classification:", result)


if __name__ == "__main__":
    main()

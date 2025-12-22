# GhostVenumAI

GhostVenumAI is a local-first Python project that combines robust network scanning with optional AI-assisted interpretation of scan results.

The project is intentionally designed as a **portfolio-grade engineering system**, focusing on:
- clean modular architecture
- responsible security tooling
- reproducible execution
- structured AI integration

Website: https://www.ghostvenumai.de

---

## Key Features

- **Robust Nmap Scan Orchestration**
  - Safe argument handling
  - Graceful privilege fallback (SYN scan → TCP connect scan)
  - Deterministic text output for further processing

- **Optional AI-Assisted Analysis**
  - Uses OpenAI via environment-based API key handling
  - Generates structured, human-readable analysis output

- **Report Generation**
  - Conservative parsing of scan results
  - Produces a clean text report without assumptions or exploitation logic

- **Local System Metadata Collection**
  - Hostname, IP, platform, architecture
  - No external services required

- **Controlled Connectivity Demonstration**
  - Opt-in outbound TCP connection example
  - No shell, no command execution, no persistence

---

## Safety & Responsibility

This repository is intended for **defensive security analysis, research, and education**.

- No exploit code
- No automated attack logic
- No plug-and-play deployment
- No persistence mechanisms

You must have **explicit authorization** before scanning any network or system.

---

## Project Structure

```text
ghostvenumai/
├── main.py
├── modules/
│   ├── api_key.py
│   ├── auth.py
│   ├── scanner.py
│   ├── gpt_analysis.py
│   ├── report.py
│   ├── system_info.py
│   ├── reverse_shell.py
│   └── i18n_quick.py
├── config.example.json
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## Requirements

- Python 3.10+ recommended
- Nmap installed and available in PATH

### Install Nmap (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install -y nmap
```

---

## Installation

```bash
git clone https://github.com/ghostvenumai/ghostvenumai-portfolio.git
cd ghostvenumai-portfolio

cp config.example.json config.json

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

```bash
python3 main.py
```

### Optional: enable AI-assisted analysis

```bash
export OPENAI_API_KEY="YOUR_API_KEY_HERE"
python3 main.py
```

---

## License

MIT License.  
See `LICENSE` file for details.

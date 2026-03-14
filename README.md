# GhostVenumAI

<p align="center">
  <img src="assets/materna-badge-master.jpg" alt="Master Badge" width="180" />
</p>

<h1 align="center">GhostVenumAI</h1>

<p align="center">
  <strong>AI-Powered Cybersecurity Platform — Defensive Network Analysis & Automated Reporting</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
  <img src="https://img.shields.io/badge/AI-OpenAI%20GPT-blueviolet?logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/security-Nmap-orange?logo=linux&logoColor=white" />
  <img src="https://img.shields.io/badge/status-active-brightgreen" />
</p>

<p align="center">
  🌐 <a href="https://www.ghostvenumai.de">www.ghostvenumai.de</a>
</p>

---

## 🏆 Award & Recognition

<table>
  <tr>
    <td width="80" align="center">🥇</td>
    <td>
      <strong>Malt — Freelancers Got AI Talent Award</strong><br/>
      GhostVenumAI was submitted to the <em>Freelancers Got AI Talent Award</em> organized by <a href="https://www.malt.com">Malt</a>, a Europe-wide competition showcasing leading AI freelancers and innovative AI projects.<br/><br/>
      The project was <strong>reviewed by the Malt jury</strong> and <strong>selected for inclusion in Malt's internal AI project library</strong>, where enterprise clients can explore innovative AI applications developed by freelancers.
    </td>
  </tr>
</table>

---

## About the Project

GhostVenumAI is a local-first Python platform that combines robust network scanning with AI-assisted interpretation of scan results. It automates network reconnaissance, vulnerability analysis, and security reporting — built for cybersecurity professionals, researchers, and defensive analysts.

This project is engineered as a **portfolio-grade system**, demonstrating:

- Clean, modular Python architecture
- Responsible and ethical security tooling
- Reproducible, deterministic execution
- Structured AI/LLM integration for real-world use

---

## Key Features

### 🔍 Nmap Scan Orchestration
- Safe argument handling via `shlex`
- Graceful privilege fallback (SYN scan → TCP connect scan)
- Timeout management and error recovery
- Deterministic text output for downstream analysis

### 🤖 AI-Assisted Security Analysis
- OpenAI GPT integration for structured scan interpretation
- Prompt-engineered for defensive security context
- Environment-based API key handling (no hardcoded secrets)
- Generates human-readable, time-stamped analysis reports

### 📄 Automated Report Generation
- Conservative parsing of Nmap output (regex-based port extraction)
- Clean, structured text reports
- Designed for audit trails and documentation

### 🖥️ Local System Metadata
- Hostname, IP, platform, architecture, MAC address
- Cross-platform support (Linux, macOS, Windows)
- No external services required

### 🔐 Optional SSH Access Control
- PBKDF2-HMAC-SHA256 password hashing
- Timing-safe verification to prevent side-channel attacks
- Anti-bruteforce backoff mechanism
- Fully opt-in — disabled by default

### 🌍 Multi-Language Support (i18n)
- German, English, Spanish
- Persistent language selection stored in config
- CLI-based language switching

---

## Tech Stack

| Category | Technologies |
|---|---|
| **Language** | Python 3.10+ |
| **AI / LLM** | OpenAI GPT (via SDK ≥ 1.0) |
| **Security** | Nmap, PBKDF2, HMAC |
| **Architecture** | Modular, local-first, CLI-driven |
| **DevOps** | Git, venv, MIT License |

---

## Project Structure

```text
ghostvenumai/
├── main.py                  # Entry point & orchestration
├── modules/
│   ├── api_key.py           # OpenAI API key management (CLI + interactive)
│   ├── auth.py              # SSH session protection (PBKDF2, opt-in)
│   ├── scanner.py           # Nmap execution with privilege fallback
│   ├── gpt_analysis.py      # AI-powered scan interpretation
│   ├── report.py            # Text report generation
│   ├── system_info.py       # Local system metadata collector
│   └── i18n_quick.py        # Multi-language support (de/en/es)
├── config.example.json
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.10+ recommended
- Nmap installed and available in PATH

```bash
# Install Nmap (Ubuntu / Debian)
sudo apt update && sudo apt install -y nmap
```

### Setup

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

### Enable AI-Assisted Analysis

```bash
export OPENAI_API_KEY="YOUR_API_KEY_HERE"
python3 main.py
```

Or enter the key interactively when prompted — it will be stored locally in `config.json`.

---

## Safety & Responsibility

This repository is intended for **defensive security analysis, research, and education**.

- ✅ No exploit code
- ✅ No automated attack logic
- ✅ No plug-and-play deployment against third parties
- ✅ No persistence mechanisms

> ⚠️ **You must have explicit authorization before scanning any network or system.**

---

## About the Developer

**Serkan Iazurlo** — Freelance Software Developer & AI Engineer

Focused on building intelligent tools at the intersection of **artificial intelligence**, **cybersecurity**, and **automation**. GhostVenumAI represents a hands-on approach to combining modern AI capabilities with practical security engineering.

**Core competencies demonstrated in this project:**
- Python development & software architecture
- AI/LLM integration & prompt engineering
- Cybersecurity automation & network analysis
- Security tool development
- Clean code practices & open-source engineering

---

## License

MIT License — see [`LICENSE`](LICENSE) for details.

© 2025 Serkan Iazurlo

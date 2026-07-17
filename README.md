<div align="center">

# 🛡️ SecOps-Arsenal

### A Professional Collection of Cybersecurity Tools for Education, Research & Defense

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](http://makeapullrequest.com)
[![CI](https://img.shields.io/github/actions/workflow/status/Aakash02A/SecOps-Arsenal/ci.yml?style=for-the-badge&label=CI)](../../actions/workflows/ci.yml)
[![CodeQL](https://img.shields.io/github/actions/workflow/status/Aakash02A/SecOps-Arsenal/codeql.yml?style=for-the-badge&label=CodeQL)](../../actions/workflows/codeql.yml)
![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

---

**SecOps-Arsenal** is a curated collection of 20+ hands-on cybersecurity tools, scripts, and services designed for education, research, defensive engineering, and authorized security testing. Each tool is a standalone project that teaches essential security concepts through real, runnable implementations.

[Getting Started](#-quick-start) · [Tool Catalog](#-tool-catalog) · [Contributing](CONTRIBUTING.md) · [Security Policy](SECURITY.md)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Repository Scope](#-repository-scope)
- [Tool Catalog](#-tool-catalog)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Supported Platforms](#-supported-platforms)
- [Security Notice](#-security-notice)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [FAQ](#-faq)
- [License](#-license)
- [Maintainers](#-maintainers)
- [Acknowledgements](#-acknowledgements)

---

## 🔍 Overview

SecOps-Arsenal provides **practical, code-driven cybersecurity education** organized in a progressive learning path from Beginner to Expert. Unlike theoretical resources, every tool in this repository is a working implementation that you can run, modify, extend, and integrate into your own security lab.

### What You'll Get

- 🔧 **Learn by building** — each tool implements a real cybersecurity concept
- 🧠 **Understand internals** — see how detection engines, SOAR platforms, and offensive tools actually work
- 💻 **Portfolio-ready projects** — polished, documented tools you can showcase
- 📁 **Progressive difficulty** — structured path from DNS lookups to SOAR orchestration
- 🛡️ **Defensive-first mindset** — offensive tools exist to improve your defenses

---

## 🎯 Repository Scope

This repository is intended for:

- **Cybersecurity Education** — learning security concepts through implementation
- **Defensive Engineering** — building detection, monitoring, and response tools
- **Research** — experimenting with security techniques in controlled environments
- **Laboratory Environments** — testing tools in isolated security labs
- **Authorized Security Assessments** — supporting legitimate penetration testing engagements

---

## 🧰 Tool Catalog

### 🟢 Beginner

| # | Tool | Description |
|:---:|---|---|
| 1 | [`basic-recon/`](basic-recon/) | DNS lookup, IP geolocation, WHOIS queries, Nmap wrapper |
| 2 | [`credential-check/`](credential-check/) | Password complexity tester + Have I Been Pwned breach lookup |
| 3 | [`file-integrity/`](file-integrity/) | SHA-256 file hashing + integrity monitoring (FIM) |
| 4 | [`url-scanner/`](url-scanner/) | URL safety checker with regex analysis + VirusTotal API |

### 🟡 Intermediate

| # | Tool | Description |
|:---:|---|---|
| 5 | [`log-parser/`](log-parser/) | Apache/Nginx log parser + Streamlit visualization dashboard |
| 6 | [`packet-sniffer/`](packet-sniffer/) | Live network capture via Scapy with protocol inspection |
| 7 | [`siem-ingest/`](siem-ingest/) | ELK stack ingestion scripts + Docker Compose setup |
| 8 | [`alerts/`](alerts/) | YAML rule-based alert engine (IDS/IPS logic) |
| 9 | [`windows-monitor/`](windows-monitor/) | Real-time Windows Event ID monitoring (PowerShell) |

### 🔵 Advanced

| # | Tool | Description |
|:---:|---|---|
| 10 | [`automations/`](automations/) | Security playbooks: IP blocking, account locking, email alerts |
| 11 | [`forensics/`](forensics/) | Metadata extractor + forensic timeline builder |
| 12 | [`red-team/`](red-team/) | SMB enumeration + phishing template generator (educational) |
| 13 | [`threat-intel/`](threat-intel/) | IOC enrichment via AbuseIPDB + AlienVault OTX |
| 14 | [`web-scanner/`](web-scanner/) | HTTP header audit, TLS inspection, common exposure checks |
| 15 | [`api-security/`](api-security/) | Automated OWASP API Top 10 security tests |

### 🔴 Expert

| # | Tool | Description |
|:---:|---|---|
| 16 | [`blue-team/`](blue-team/) | Host hardening auditor for Windows & Linux baselines |
| 17 | [`correlation-engine/`](correlation-engine/) | Multi-source log correlation for brute-force + exfiltration detection |
| 18 | [`incident-response/`](incident-response/) | Automated live-response evidence collector + IR report generator |
| 19 | [`recon-framework/`](recon-framework/) | Multi-threaded subdomain enumeration + directory brute-forcing |
| 20 | [`orchestration/`](orchestration/) | Dockerized SOAR-lite engine with YAML playbooks |

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Aakash02A/SecOps-Arsenal.git
cd SecOps-Arsenal

# Create a virtual environment
python -m venv venv
source venv/bin/activate    # Linux/macOS
.\venv\Scripts\activate     # Windows

# Install all dependencies
pip install -r requirements.txt

# Run a tool — for example, check a password
python credential-check/credential_checker.py "MyP@ssw0rd!"

# Or build a file integrity baseline
python file-integrity/fim.py build ./some-directory
```

---

## 📦 Installation

### Prerequisites

- **Python 3.11+**
- **pip** (Python package manager)
- **Git**

### Optional Prerequisites

| Tool | Required For |
|---|---|
| [Nmap](https://nmap.org) | `basic-recon/nmap_scanner.py` |
| [Npcap](https://npcap.com) (Windows) | `packet-sniffer/sniffer.py` |
| [Docker](https://docker.com) | `orchestration/`, `siem-ingest/` |

### Install All Dependencies

```bash
pip install -r requirements.txt
```

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
pre-commit install
```

Each tool's `README.md` lists its specific dependencies if you prefer to install only what you need.

---

## 🏗 Architecture

```
SecOps-Arsenal/
├── .github/                    # GitHub Actions, templates, Dependabot
│   ├── workflows/              # CI and CodeQL pipelines
│   ├── ISSUE_TEMPLATE/         # Bug report, feature request, tool request
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── dependabot.yml
│   └── FUNDING.yml
├── tests/                      # Unit tests (pytest)
├── alerts/                     # 🟡 Rule-based alert engine
├── api-security/               # 🔵 API security tester
├── automations/                # 🔵 Security playbooks
├── basic-recon/                # 🟢 DNS, WHOIS, IP info, Nmap
├── blue-team/                  # 🔴 Host hardening auditor
├── correlation-engine/         # 🔴 Log correlation engine
├── credential-check/           # 🟢 Password checker
├── file-integrity/             # 🟢 File integrity monitor
├── forensics/                  # 🔵 Metadata & timeline tools
├── incident-response/          # 🔴 IR evidence collector
├── log-parser/                 # 🟡 Log parser & dashboard
├── orchestration/              # 🔴 SOAR-lite engine (Docker)
├── packet-sniffer/             # 🟡 Network packet sniffer
├── recon-framework/            # 🔴 Subdomain & directory enum
├── red-team/                   # 🔵 SMB enum & phishing (educational)
├── siem-ingest/                # 🟡 ELK stack ingestion
├── threat-intel/               # 🔵 IOC enrichment
├── url-scanner/                # 🟢 URL safety scanner
├── web-scanner/                # 🔵 Web vulnerability scanner
├── windows-monitor/            # 🟡 Windows event monitor (PS1)
├── requirements.txt            # Global Python dependencies
├── requirements-dev.txt        # Development dependencies
├── pyproject.toml              # Ruff & pytest configuration
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── SUPPORT.md
├── CHANGELOG.md
└── LICENSE                     # MIT License
```

---

## ⚙️ Technologies

| Category | Technologies |
|---|---|
| **Languages** | Python 3.11+ (primary), PowerShell, Bash |
| **Core Libraries** | `requests`, `scapy`, `pyyaml`, `dnspython`, `python-nmap` |
| **Visualization** | Streamlit, Plotly, Pandas |
| **Infrastructure** | Docker, Docker Compose, ELK Stack |
| **CI/CD** | GitHub Actions, CodeQL, Dependabot |
| **Quality** | Ruff (lint + format), pytest, pre-commit, pip-audit |

---

## 💻 Supported Platforms

| Platform | Status | Notes |
|---|:---:|---|
| **Windows 10/11** | ✅ | Full support. PowerShell tools are Windows-native. |
| **Ubuntu / Debian** | ✅ | Full support. Tested on Ubuntu 22.04+. |
| **macOS** | ⚠️ | Most tools work. Some system-level scripts (firewall, account management) are Windows/Linux only. |
| **Docker** | ✅ | Containerized tools available for `orchestration/` and `siem-ingest/`. |

---

## 🔒 Security Notice

> **⚠️ IMPORTANT: Responsible Use**
>
> The tools in this repository are provided for **educational purposes, authorized security research, and legitimate penetration testing** only. By using these tools, you agree to:
>
> - **Only use tools against systems you own or have explicit written authorization to test**
> - **Comply with all applicable laws** in your jurisdiction
> - **Not use these tools for unauthorized access**, data theft, or any malicious purpose
> - **Report vulnerabilities responsibly** following our [Security Policy](SECURITY.md)
>
> The maintainers are not responsible for misuse of any tool in this repository.

For security vulnerability reports, see [SECURITY.md](SECURITY.md).

---

## 🤝 Contributing

We welcome contributions! Whether you're fixing a bug, adding a new tool, or improving documentation, your help is appreciated.

1. Read the [Contributing Guidelines](CONTRIBUTING.md)
2. Review the [Code of Conduct](CODE_OF_CONDUCT.md)
3. Check [open issues](../../issues) for tasks labeled `good first issue`
4. Fork, branch, code, test, and submit a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for full development environment setup and coding standards.

---

## 🗺 Roadmap

### Near-term
- [ ] Expand test coverage to all 20 tools
- [ ] Add Malware Analysis toolkit (static analysis, YARA rules)
- [ ] Add Cloud Security module (AWS/GCP misconfiguration scanner)
- [ ] Add Network Security module (port knocking, ARP spoofing detection)

### Medium-term
- [ ] Interactive web dashboard consolidating all tools
- [ ] Plugin architecture for community tool extensions
- [ ] Integration with MITRE ATT&CK framework
- [ ] Pre-built Docker lab environments with intentionally vulnerable targets

### Long-term
- [ ] AI-assisted threat detection module
- [ ] Full CTF challenge platform using the tools
- [ ] Certification-aligned learning paths (Security+, CEH, OSCP)

---

## ❓ FAQ

<details>
<summary><strong>Is this repository safe to use?</strong></summary>

Yes. All tools are designed for educational use and authorized testing. Offensive tools include prominent disclaimers. No tool contains malware, backdoors, or destructive payloads.
</details>

<details>
<summary><strong>Do I need all the dependencies?</strong></summary>

No. Each tool's `README.md` lists its specific requirements. The root `requirements.txt` installs everything for convenience, but you can install selectively.
</details>

<details>
<summary><strong>Can I use these tools in production?</strong></summary>

These tools are educational and not hardened for production use. They are excellent for learning, prototyping, and lab environments, but production security infrastructure should use battle-tested solutions.
</details>

<details>
<summary><strong>What Python version do I need?</strong></summary>

Python 3.11 or higher is recommended. The CI pipeline tests against Python 3.11 and 3.12.
</details>

<details>
<summary><strong>How do I report a security vulnerability?</strong></summary>

Do NOT open a public issue. Follow our <a href="SECURITY.md">Security Policy</a> for responsible disclosure.
</details>

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Maintainers

| | |
|---|---|
| **Aakash** | [![GitHub](https://img.shields.io/badge/GitHub-Aakash02A-181717?style=flat-square&logo=github)](https://github.com/Aakash02A) |

---

## 🙏 Acknowledgements

- [OWASP](https://owasp.org/) — API Security Top 10 and web security standards
- [Have I Been Pwned](https://haveibeenpwned.com/) — Breached password API
- [AbuseIPDB](https://www.abuseipdb.com/) & [AlienVault OTX](https://otx.alienvault.com/) — Threat intelligence APIs
- [VirusTotal](https://www.virustotal.com/) — URL reputation API
- [Elastic](https://www.elastic.co/) — ELK Stack
- [Contributor Covenant](https://www.contributor-covenant.org/) — Code of Conduct
- The open-source cybersecurity community

---

<div align="center">

**Built with ❤️ for the cybersecurity community**

[⬆ Back to Top](#️-secops-arsenal)

</div>
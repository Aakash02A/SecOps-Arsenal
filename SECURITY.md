# Security Policy

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in any tool within this repository, please report it responsibly.

### How to Report

1. **Do NOT open a public issue** — this could expose the vulnerability to others before a fix is ready.
2. **Email the maintainers** at [aakash02a@outlook.com](mailto:aakash02a@outlook.com) with the subject line: `[SECURITY] SecOps-Arsenal Vulnerability Report`.
3. Include as much detail as possible:
   - Description of the vulnerability
   - Affected tool(s) and file(s)
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment** within 48 hours of your report.
- **Assessment** within 7 days — we will confirm whether the report is valid and estimate a timeline for a fix.
- **Fix & Disclosure** — once a fix is ready, we will publish a security advisory and credit the reporter (unless anonymity is requested).

## Supported Versions

| Version | Supported |
|---------|-----------|
| `main` branch (latest) | ✅ |
| Older commits / tags | ❌ |

## Scope

This repository contains **educational cybersecurity tools** intended for authorized security testing and learning. The security policy applies to:

- Vulnerabilities in the tool code itself (e.g., command injection, unsafe deserialization)
- Credential exposure or secrets accidentally committed
- Dependency vulnerabilities in pinned packages

The following are **out of scope**:

- Vulnerabilities in third-party services or APIs the tools interact with
- Security issues arising from intentional misuse of offensive tools against unauthorized targets
- Issues that require physical access or social engineering to exploit

## Responsible Disclosure

We follow responsible disclosure practices. We ask that reporters:

- Allow us reasonable time to investigate and address the vulnerability
- Avoid accessing or modifying other users' data
- Act in good faith to avoid privacy violations, data destruction, and service disruption

Thank you for helping keep SecOps-Arsenal secure.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Global `requirements.txt` and `requirements-dev.txt` for dependency management
- `SECURITY.md` — responsible disclosure policy
- `SUPPORT.md` — support and help guide
- `CHANGELOG.md` — this file
- `.gitignore` — comprehensive exclusion rules
- `pyproject.toml` — Ruff linting and formatting configuration
- GitHub Actions CI pipeline (`ci.yml`)
- CodeQL security analysis workflow (`codeql.yml`)
- Dependabot configuration for automated dependency updates
- Unit tests for core tools (`credential-check`, `alerts`, `log-parser`, `correlation-engine`, `url-scanner`, `file-integrity`)
- CLI entry points for `dns_lookup.py`, `ip_info.py`, and `whois_lookup.py`
- Security tool request issue template
- `FUNDING.yml` for GitHub Sponsors

### Changed
- **SECURITY FIX**: Replaced `shell=True` with argument lists in `block_ip.py`, `lock_account.py`, and `soar_engine.py` to prevent command injection
- **SECURITY FIX**: Added input sanitization to SOAR engine template variables
- **BUG FIX**: Fixed `whois_lookup.py` executing network call on import (moved to `__main__` guard)
- **BUG FIX**: Replaced bare `except:` clauses in `ip_info.py` with specific exception types
- **BUG FIX**: Fixed `auditor.py` crash on Windows due to `os.geteuid()` (Linux-only API)
- **BUG FIX**: Replaced deprecated `datetime.utcnow()` in `web-scanner/scanner.py`
- Added IP address validation to `block_ip.py`
- Added username validation to `lock_account.py`
- Added `--dry-run` and `--yes` flags to destructive automation scripts
- Added structured logging to SOAR engine
- Updated Dockerfile base image from Python 3.9 to 3.11
- Enhanced `CONTRIBUTING.md` with development setup, licensing guidance, and AI policy
- Enhanced PR template with security review checklist
- Completed truncated `CODE_OF_CONDUCT.md` (full Contributor Covenant v2.1)
- Professionally rewritten root `README.md`

### Security
- Fixed command injection vulnerabilities in 3 files
- Added educational disclaimers and watermarks to offensive tool outputs
- All API keys and credentials handled via environment variables (verified — no hardcoded secrets)

## [0.1.0] — 2025-01-01

### Added
- Initial release with 20 cybersecurity tools across Beginner, Intermediate, Advanced, and Expert tiers

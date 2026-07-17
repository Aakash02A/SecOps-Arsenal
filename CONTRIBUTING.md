# Contributing to SecOps-Arsenal

First off, thank you for considering contributing to **SecOps-Arsenal**! It's people like you that make this toolset a great learning resource for the cybersecurity community.

## 📝 Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to the project maintainers.

## 🛠 Development Environment Setup

### Prerequisites

- **Python 3.11+**
- **Git**
- **Docker** (optional — only needed for `orchestration/` and `siem-ingest/`)

### Getting Started

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/SecOps-Arsenal.git
cd SecOps-Arsenal

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate    # Linux/macOS
# or: .\venv\Scripts\activate    # Windows

# 3. Install development dependencies
pip install -r requirements-dev.txt

# 4. Install pre-commit hooks
pre-commit install

# 5. Run the test suite to verify your setup
pytest
```

## 🚀 How Can I Contribute?

### Reporting Bugs

- Ensure the bug was not already reported by searching on GitHub under [Issues](../../issues).
- If you're unable to find an open issue addressing the problem, open a new one using the **Bug Report** template.
- Include: affected tool/folder, steps to reproduce, expected vs. actual behavior, and your environment (OS, Python version).

### Suggesting Enhancements

- Open a new [Issue](../../issues) using the **Feature Request** or **Security Tool Request** template.
- Provide a clear and detailed explanation of the feature and why it's important for the security community.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes (`pytest`).
5. Ensure your code passes linting (`ruff check .` and `ruff format --check .`).
6. Issue your pull request!

## 💻 Coding Standards

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) — enforced via **Ruff**.
- Use **type hints** where practical.
- Write clear, concise **docstrings** for all major functions and classes.
- Include a **shebang line** (`#!/usr/bin/env python3`) at the top of every script.
- Add a **module-level docstring** explaining what the tool does.
- Wrap all executable code in `if __name__ == "__main__":` guards.
- Ensure tools meant for educational purposes emphasize safety and explicit authorization.

### CLI Conventions

Tools should follow a consistent CLI pattern:

- `--help` (provided by argparse)
- `--verbose` / `--quiet` (where applicable)
- `--output` / `-o` for output file specification
- `--json` for JSON output (where applicable)
- Consistent exit codes: `0` for success, `1` for error

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Limit the first line to 72 characters or less.
- Reference issue numbers where applicable (e.g., "Fix #42").

### Dependencies

- Provide `requirements.txt` if you introduce new external dependencies.
- Use **compatible release specifiers** (`~=`) in version pins.
- Do not introduce unnecessary heavy dependencies.

## 🛠 Adding a New Project

If you are adding a completely new project to the arsenal:

1. Determine the appropriate difficulty tier (🟢 Beginner, 🟡 Intermediate, 🔵 Advanced, 🔴 Expert).
2. Create a dedicated folder for your tool using **kebab-case** naming (e.g., `my-new-tool/`).
3. Include a `README.md` inside your folder explaining:
   - What the tool does
   - Prerequisites and installation
   - Usage examples
   - Safety disclaimers (especially for offensive tools)
4. Add unit tests in `tests/test_<tool_name>.py`.
5. Update the main project table in the root `README.md` to list your tool.
6. Add any new dependencies to the root `requirements.txt`.

## 📜 Licensing & Legal

- By contributing, you certify that you own the submitted code or have the right to submit it under the MIT License.
- Third-party code must retain its original license and be clearly attributed.
- Do not submit copyrighted datasets, proprietary detection signatures, or materials you do not have the right to distribute.
- AI-generated contributions are welcome but must be reviewed for correctness, security, and licensing compliance before submission.

## 🔒 Security

- **Never hardcode** API keys, credentials, or secrets in source code. Use environment variables.
- **Never commit** `.env` files, API keys, or tokens.
- If you discover a security vulnerability, **do NOT open a public issue**. Follow our [Security Policy](SECURITY.md).

Thank you for contributing!

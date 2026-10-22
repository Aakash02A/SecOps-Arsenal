"""Security-focused tests for the SOAR orchestration engine.

Explicitly exercises the injection-sanitization boundary and command
construction, per the requirement to test the SOAR engine against
maliciously crafted inputs.
"""

import os
import sys
from unittest import mock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "orchestration"))

from soar_engine import execute_action, sanitize_value

SAFE_VALUES = [
    "10.0.0.1",
    "user@example.com",
    "/var/log/sys.log",
    "ab-cd_ef.1",
    "2001:db8::1",  # IPv6 with colons
    "5",  # non-string values are coerced
]

UNSAFE_VALUES = [
    "10.0.0.1; rm -rf /",  # command separator
    "$(whoami)",  # command substitution
    "a|b",  # pipe
    "a&&b",  # logical AND
    "a`b`",  # backtick substitution
    "hello\nworld",  # newline injection
    ">out.txt",  # redirection
    "127.0.0.1 && calc.exe",  # chained command
]


class TestSanitizeValue:
    @pytest.mark.parametrize("value", SAFE_VALUES)
    def test_allows_safe_values(self, value):
        assert sanitize_value(value) == str(value)

    @pytest.mark.parametrize("value", UNSAFE_VALUES)
    def test_rejects_injection_payloads(self, value):
        with pytest.raises(ValueError):
            sanitize_value(value)


class TestExecuteAction:
    def test_dry_run_does_not_invoke_subprocess(self):
        action = {"command": "echo {msg}"}
        with mock.patch("soar_engine.subprocess.run") as run:
            execute_action(action, {"msg": "hello"}, dry_run=True)
        run.assert_not_called()

    def test_malicious_value_is_blocked_before_execution(self):
        action = {"command": "block {ip}"}
        with mock.patch("soar_engine.subprocess.run") as run:
            execute_action(action, {"ip": "1.2.3.4; rm -rf /"}, dry_run=False)
        run.assert_not_called()

    def test_safe_value_runs_as_argument_list_without_shell(self):
        action = {"command": "firewall block {ip}"}
        with mock.patch("soar_engine.subprocess.run") as run:
            run.return_value.returncode = 0
            run.return_value.stderr = ""
            execute_action(action, {"ip": "1.2.3.4"}, dry_run=False)
        run.assert_called_once()
        # Command is split into a list (no shell string execution)
        assert run.call_args[0][0] == ["firewall", "block", "1.2.3.4"]

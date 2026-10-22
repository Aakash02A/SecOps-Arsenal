"""Tests for the incident-response evidence collector.

Verifies the security-relevant contract that commands are executed with
``shell=False`` using argument lists (never shell string interpolation),
and that the report generator produces the expected artifact.
"""

import os
import subprocess
import sys
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "incident-response"))

import ir_collector


class TestRunCmd:
    def test_list_command_uses_shell_false(self):
        with mock.patch("ir_collector.subprocess.run") as run:
            run.return_value.returncode = 0
            run.return_value.stdout = "output data"
            run.return_value.stderr = ""
            result = ir_collector.run_cmd(["netstat", "-ano"])
        assert result == "output data"
        assert run.call_args[0][0] == ["netstat", "-ano"]
        assert run.call_args[1]["shell"] is False

    def test_string_command_is_split_safely(self):
        with mock.patch("ir_collector.subprocess.run") as run:
            run.return_value.returncode = 0
            run.return_value.stdout = "x"
            run.return_value.stderr = ""
            ir_collector.run_cmd("ps aux")
        assert run.call_args[0][0] == ["ps", "aux"]

    def test_timeout_is_handled(self):
        with mock.patch(
            "ir_collector.subprocess.run",
            side_effect=subprocess.TimeoutExpired("cmd", 15),
        ):
            result = ir_collector.run_cmd(["sleep", "1"])
        assert result.startswith("[-]")

    def test_command_not_found_is_handled(self):
        with mock.patch(
            "ir_collector.subprocess.run",
            side_effect=FileNotFoundError(),
        ):
            result = ir_collector.run_cmd(["definitely-not-a-real-command"])
        assert "not found" in result


class TestGenerateReport:
    def test_report_written_with_expected_content(self, tmp_path):
        out_dir = str(tmp_path)
        files = ["network_connections.txt", "running_processes.txt"]
        ir_collector.generate_report(out_dir, files, "TestOS")

        report = tmp_path / "IR_Report.md"
        assert report.exists()
        text = report.read_text(encoding="utf-8")
        assert "Incident Response Triage Report" in text
        assert "TestOS" in text
        assert "network_connections.txt" in text
        assert "running_processes.txt" in text

"""Tests for the log parser regex and analysis logic."""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "log-parser"))

from log_parser import parse_log_file, analyze_logs, LOG_PATTERN


SAMPLE_LOG_LINE = (
    '192.168.1.1 - frank [10/Oct/2000:13:55:36 -0700] '
    '"GET /apache_pb.gif HTTP/1.0" 200 2326 '
    '"http://www.example.com/start.html" "Mozilla/4.08"'
)

SAMPLE_LOG_LINE_404 = (
    '10.0.0.5 - - [10/Oct/2000:14:00:00 -0700] '
    '"POST /login HTTP/1.1" 404 0 '
    '"-" "curl/7.68.0"'
)


class TestLogPattern:
    """Test the regex pattern matches correctly."""

    def test_valid_combined_log(self):
        match = LOG_PATTERN.match(SAMPLE_LOG_LINE)
        assert match is not None
        data = match.groupdict()
        assert data["ip"] == "192.168.1.1"
        assert data["method"] == "GET"
        assert data["path"] == "/apache_pb.gif"
        assert data["status"] == "200"
        assert data["bytes"] == "2326"

    def test_post_request(self):
        match = LOG_PATTERN.match(SAMPLE_LOG_LINE_404)
        assert match is not None
        data = match.groupdict()
        assert data["method"] == "POST"
        assert data["status"] == "404"

    def test_invalid_line(self):
        match = LOG_PATTERN.match("this is not a log line")
        assert match is None


class TestParseLogFile:
    """Test the file parsing function."""

    def test_parse_valid_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False, encoding="utf-8") as f:
            f.write(SAMPLE_LOG_LINE + "\n")
            f.write(SAMPLE_LOG_LINE_404 + "\n")
            f.write("bad line\n")
            tmp_path = f.name

        try:
            logs = parse_log_file(tmp_path)
            assert len(logs) == 2
            assert logs[0]["ip"] == "192.168.1.1"
            assert logs[1]["status"] == "404"
            # Bytes '-' should be cleaned to 0
            assert logs[1]["bytes"] == 0
        finally:
            os.unlink(tmp_path)

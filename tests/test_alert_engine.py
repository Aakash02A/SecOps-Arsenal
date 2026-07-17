"""Tests for the alert engine rule evaluation logic."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "alerts"))

from alert_engine import AlertEngine


class TestAlertEngineEvaluation:
    """Unit tests for AlertEngine.evaluate()."""

    def setup_method(self):
        """Create a minimal engine with inline rules."""
        # We'll monkeypatch the rules directly instead of loading from YAML
        self.engine = AlertEngine.__new__(AlertEngine)
        self.engine.rules = [
            {
                "id": 1001,
                "name": "SQL Injection",
                "severity": "High",
                "conditions": {
                    "field": "path",
                    "operator": "regex",
                    "value": "(?i)(union.*select|select.*from)",
                },
            },
            {
                "id": 1002,
                "name": "Path Traversal",
                "severity": "High",
                "conditions": {
                    "field": "path",
                    "operator": "contains",
                    "value": "/etc/passwd",
                },
            },
            {
                "id": 1003,
                "name": "Status 500",
                "severity": "Low",
                "conditions": {
                    "field": "status",
                    "operator": "equals",
                    "value": 500,
                },
            },
        ]

    def test_regex_match(self):
        log = {"path": "/search?q=1 UNION SELECT * FROM users", "ip": "10.0.0.1"}
        alerts = self.engine.evaluate(log)
        assert len(alerts) == 1
        assert alerts[0]["rule_id"] == 1001

    def test_regex_no_match(self):
        log = {"path": "/about", "ip": "10.0.0.2"}
        alerts = self.engine.evaluate(log)
        assert len(alerts) == 0

    def test_contains_match(self):
        log = {"path": "/../../etc/passwd", "ip": "10.0.0.3"}
        alerts = self.engine.evaluate(log)
        assert len(alerts) == 1
        assert alerts[0]["rule_id"] == 1002

    def test_equals_match(self):
        log = {"status": 500, "ip": "10.0.0.4"}
        alerts = self.engine.evaluate(log)
        assert len(alerts) == 1
        assert alerts[0]["rule_id"] == 1003

    def test_equals_no_match(self):
        log = {"status": 200, "ip": "10.0.0.5"}
        alerts = self.engine.evaluate(log)
        assert len(alerts) == 0

    def test_missing_field_skips_rule(self):
        log = {"user_agent": "Mozilla/5.0", "ip": "10.0.0.6"}
        alerts = self.engine.evaluate(log)
        assert len(alerts) == 0

    def test_multiple_matches(self):
        log = {
            "path": "/../../etc/passwd?q=UNION SELECT * FROM users",
            "status": 500,
            "ip": "10.0.0.7",
        }
        alerts = self.engine.evaluate(log)
        assert len(alerts) == 3

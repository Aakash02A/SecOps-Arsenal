"""Tests for the correlation engine brute-force and exfiltration detection."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "correlation-engine"))

from correlator import correlate_events


class TestCorrelationEngine:
    """Unit tests for the correlate_events logic."""

    def test_critical_alert_brute_force_plus_exfiltration(self):
        auth = [
            {"ip": "10.0.0.1", "action": "failed_login"},
            {"ip": "10.0.0.1", "action": "failed_login"},
            {"ip": "10.0.0.1", "action": "failed_login"},
            {"ip": "10.0.0.1", "action": "success_login"},
        ]
        net = [
            {"src_ip": "10.0.0.1", "bytes_sent": 52428800},  # 50MB
        ]
        alerts = correlate_events(auth, net)
        assert len(alerts) == 1
        assert alerts[0]["severity"] == "CRITICAL"

    def test_high_alert_brute_force_low_traffic(self):
        auth = [
            {"ip": "10.0.0.2", "action": "failed_login"},
            {"ip": "10.0.0.2", "action": "failed_login"},
            {"ip": "10.0.0.2", "action": "failed_login"},
            {"ip": "10.0.0.2", "action": "success_login"},
        ]
        net = [
            {"src_ip": "10.0.0.2", "bytes_sent": 1024},  # 1KB — normal
        ]
        alerts = correlate_events(auth, net)
        assert len(alerts) == 1
        assert alerts[0]["severity"] == "HIGH"

    def test_no_alert_only_failed_logins(self):
        auth = [
            {"ip": "10.0.0.3", "action": "failed_login"},
            {"ip": "10.0.0.3", "action": "failed_login"},
            {"ip": "10.0.0.3", "action": "failed_login"},
        ]
        net = [
            {"src_ip": "10.0.0.3", "bytes_sent": 52428800},
        ]
        alerts = correlate_events(auth, net)
        assert len(alerts) == 0  # No successful login → no brute force alert

    def test_no_alert_normal_login(self):
        auth = [
            {"ip": "10.0.0.4", "action": "success_login"},
        ]
        net = [
            {"src_ip": "10.0.0.4", "bytes_sent": 5000},
        ]
        alerts = correlate_events(auth, net)
        assert len(alerts) == 0  # No failed logins → no brute force

    def test_no_alert_below_threshold(self):
        auth = [
            {"ip": "10.0.0.5", "action": "failed_login"},
            {"ip": "10.0.0.5", "action": "failed_login"},  # Only 2 fails
            {"ip": "10.0.0.5", "action": "success_login"},
        ]
        net = [
            {"src_ip": "10.0.0.5", "bytes_sent": 52428800},
        ]
        alerts = correlate_events(auth, net)
        assert len(alerts) == 0  # Under the 3-fail threshold

    def test_empty_logs(self):
        alerts = correlate_events([], [])
        assert len(alerts) == 0

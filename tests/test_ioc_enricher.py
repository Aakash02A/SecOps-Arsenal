"""Tests for the threat-intelligence IOC enricher (network fully mocked)."""

import os
import sys
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "threat-intel"))

import ioc_enricher as ioc


class _FakeResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload


class TestAbuseIPDB:
    def test_success(self):
        resp = _FakeResponse(
            200,
            {"data": {"abuseConfidenceScore": 80, "totalReports": 12, "countryCode": "US"}},
        )
        with mock.patch("ioc_enricher.requests.get", return_value=resp):
            result = ioc.check_abuseipdb("8.8.8.8", "KEY")
        assert result["source"] == "AbuseIPDB"
        assert result["abuseConfidenceScore"] == "80%"
        assert result["totalReports"] == 12

    def test_http_error(self):
        with mock.patch("ioc_enricher.requests.get", return_value=_FakeResponse(403)):
            result = ioc.check_abuseipdb("1.1.1.1", "KEY")
        assert "error" in result

    def test_network_exception_is_captured(self):
        with mock.patch("ioc_enricher.requests.get", side_effect=Exception("boom")):
            result = ioc.check_abuseipdb("1.1.1.1", "KEY")
        assert result["error"] == "boom"


class TestAlienVaultOTX:
    def test_success_extracts_pulses_and_tags(self):
        payload = {
            "pulse_info": {
                "count": 3,
                "pulses": [
                    {"tags": ["malware", "c2"]},
                    {"tags": ["phish"]},
                ],
            }
        }
        with mock.patch("ioc_enricher.requests.get", return_value=_FakeResponse(200, payload)):
            result = ioc.check_alienvault_otx("8.8.8.8", "ip", "KEY")
        assert result["source"] == "AlienVault OTX"
        assert result["pulseCount"] == 3
        assert set(result["topTags"]).issubset({"malware", "c2", "phish"})

    def test_missing_keys_handled_gracefully(self):
        # Malformed/unexpected response shape must not raise.
        with mock.patch("ioc_enricher.requests.get", return_value=_FakeResponse(200, {})):
            result = ioc.check_alienvault_otx("example.com", "domain", "KEY")
        assert result["pulseCount"] == 0

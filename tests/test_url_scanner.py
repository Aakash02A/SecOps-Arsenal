"""Tests for the URL scanner static pattern detection."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "url-scanner"))

from url_scanner import check_regex_patterns


class TestURLPatternDetection:
    """Unit tests for the regex-based URL pattern checker."""

    def test_http_url_flagged(self):
        findings = check_regex_patterns("http://example.com")
        assert any("HTTP" in f and "HTTPS" in f for f in findings)

    def test_https_url_clean(self):
        findings = check_regex_patterns("https://example.com")
        assert not any("HTTP" in f and "HTTPS" in f for f in findings)

    def test_ip_address_url_flagged(self):
        findings = check_regex_patterns("http://192.168.1.1/login")
        assert any("IP address" in f for f in findings)

    def test_domain_url_not_flagged_for_ip(self):
        findings = check_regex_patterns("https://example.com/login")
        assert not any("IP address" in f for f in findings)

    def test_excessive_subdomains_flagged(self):
        findings = check_regex_patterns("https://a.b.c.d.example.com/page")
        assert any("subdomain" in f.lower() for f in findings)

    def test_normal_subdomains_not_flagged(self):
        findings = check_regex_patterns("https://www.example.com/page")
        assert not any("subdomain" in f.lower() for f in findings)

    def test_long_url_flagged(self):
        long_url = "https://example.com/" + "a" * 80
        findings = check_regex_patterns(long_url)
        assert any("long" in f.lower() for f in findings)

    def test_at_sign_in_domain_flagged(self):
        findings = check_regex_patterns("https://admin@evil.com/login")
        assert any("@" in f for f in findings)

    def test_clean_url(self):
        findings = check_regex_patterns("https://google.com")
        assert len(findings) == 0

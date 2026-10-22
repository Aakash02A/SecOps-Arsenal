"""Tests for the recon framework (DNS and HTTP fully mocked)."""

import os
import socket
import sys
from unittest import mock

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "recon-framework"))

import recon


class _FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code


class TestSubdomainEnum:
    def test_resolves(self):
        with mock.patch("recon.socket.gethostbyname", return_value="93.184.216.34"):
            result = recon.check_subdomain("example.com", "www")
        assert result == "www.example.com -> 93.184.216.34"

    def test_non_resolving_returns_none(self):
        with mock.patch("recon.socket.gethostbyname", side_effect=socket.gaierror):
            assert recon.check_subdomain("example.com", "nope") is None


class TestDirectoryEnum:
    def test_existing_path_reported(self):
        with mock.patch("recon.requests.get", return_value=_FakeResponse(200)):
            result = recon.check_directory("https://example.com", "admin")
        assert result is not None
        assert "admin" in result and "200" in result

    def test_404_is_ignored(self):
        with mock.patch("recon.requests.get", return_value=_FakeResponse(404)):
            assert recon.check_directory("https://example.com", "missing") is None

    def test_request_exception_is_swallowed(self):
        with mock.patch("recon.requests.get", side_effect=requests.exceptions.RequestException("timeout")):
            assert recon.check_directory("https://example.com", "slow") is None

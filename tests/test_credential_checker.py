"""Tests for the credential checker password complexity logic."""

import sys
import os

# Add the project root so we can import from tool directories
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "credential-check"))

from credential_checker import check_password_complexity


class TestPasswordComplexity:
    """Unit tests for the password complexity checker."""

    def test_strong_password(self):
        score, feedback = check_password_complexity("Str0ng!Pass")
        assert score == 5
        assert feedback == []

    def test_short_password(self):
        score, feedback = check_password_complexity("Ab1!")
        assert score == 4  # Has upper, lower, digit, special — just too short
        assert any("short" in f.lower() for f in feedback)

    def test_missing_uppercase(self):
        score, feedback = check_password_complexity("lowercase1!")
        assert score == 4
        assert any("uppercase" in f.lower() for f in feedback)

    def test_missing_lowercase(self):
        score, feedback = check_password_complexity("UPPERCASE1!")
        assert score == 4
        assert any("lowercase" in f.lower() for f in feedback)

    def test_missing_number(self):
        score, feedback = check_password_complexity("NoNumbers!!")
        assert score == 4
        assert any("number" in f.lower() for f in feedback)

    def test_missing_special_char(self):
        score, feedback = check_password_complexity("NoSpecial123")
        assert score == 4
        assert any("special" in f.lower() for f in feedback)

    def test_worst_password(self):
        score, feedback = check_password_complexity("abc")
        assert score == 1  # Only lowercase
        assert len(feedback) == 4  # short + no upper + no digit + no special

    def test_empty_password(self):
        score, feedback = check_password_complexity("")
        assert score == 0
        assert len(feedback) == 5

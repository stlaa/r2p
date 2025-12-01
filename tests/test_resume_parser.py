"""Tests for resume parser module."""
import pytest
from utils.resume_parser import ResumeParser


class TestResumeParserFilters:
    """Test resume parser filtering methods."""

    def test_filter_personal_data_removes_phone_numbers(self):
        """Test that phone numbers are filtered."""
        text = "Contact me at 555-123-4567"
        filtered = ResumeParser.filter_personal_data(text)
        assert "555-123-4567" not in filtered

    def test_filter_personal_data_removes_addresses(self):
        """Test that addresses are filtered."""
        text = "I live at 123 Main Street"
        filtered = ResumeParser.filter_personal_data(text)
        assert "123 Main Street" not in filtered

    def test_filter_personal_data_removes_zip_codes(self):
        """Test that zip codes are filtered."""
        text = "My zip code is 12345"
        filtered = ResumeParser.filter_personal_data(text)
        assert "12345" not in filtered

    def test_filter_personal_data_preserves_non_personal(self):
        """Test that non-personal data is preserved."""
        text = "I have 5 years of experience"
        filtered = ResumeParser.filter_personal_data(text)
        assert "experience" in filtered

    def test_filter_personal_data_empty_string(self):
        """Test filtering empty string."""
        text = ""
        filtered = ResumeParser.filter_personal_data(text)
        assert filtered == ""

    def test_filter_personal_data_returns_string(self):
        """Test that filtered result is a string."""
        text = "Some resume text"
        filtered = ResumeParser.filter_personal_data(text)
        assert isinstance(filtered, str)

"""Tests for configuration module."""
import os
import tempfile
import pytest
from config import Config


class TestConfigInitialization:
    """Test configuration initialization."""

    def test_config_secret_key_exists(self):
        """Verify SECRET_KEY is configured."""
        assert Config.SECRET_KEY is not None
        assert isinstance(Config.SECRET_KEY, str)

    def test_config_upload_folder_configured(self):
        """Verify upload folder is configured."""
        assert Config.UPLOAD_FOLDER is not None
        assert isinstance(Config.UPLOAD_FOLDER, str)

    def test_config_generated_folder_configured(self):
        """Verify generated folder is configured."""
        assert Config.GENERATED_FOLDER is not None
        assert isinstance(Config.GENERATED_FOLDER, str)

    def test_config_allowed_extensions(self):
        """Verify allowed file extensions are configured."""
        assert Config.ALLOWED_EXTENSIONS == {'pdf', 'doc', 'docx'}

    def test_config_max_content_length(self):
        """Verify max content length is set correctly."""
        assert Config.MAX_CONTENT_LENGTH == 16 * 1024 * 1024


class TestConfigMethods:
    """Test configuration methods."""

    def test_allowed_file_with_valid_extension(self):
        """Test allowed_file method with valid extensions."""
        assert Config.allowed_file('resume.pdf') is True
        assert Config.allowed_file('resume.doc') is True
        assert Config.allowed_file('resume.docx') is True

    def test_allowed_file_with_invalid_extension(self):
        """Test allowed_file method with invalid extensions."""
        assert Config.allowed_file('resume.txt') is False
        assert Config.allowed_file('resume.exe') is False
        assert Config.allowed_file('resume') is False

    def test_allowed_file_case_insensitive(self):
        """Test allowed_file method is case insensitive."""
        assert Config.allowed_file('resume.PDF') is True
        assert Config.allowed_file('resume.DOC') is True
        assert Config.allowed_file('resume.DOCX') is True


class TestColorThemes:
    """Test color theme configuration."""

    def test_color_themes_exist(self):
        """Verify color themes are configured."""
        assert Config.COLOR_THEMES is not None
        assert len(Config.COLOR_THEMES) > 0

    def test_color_themes_have_required_keys(self):
        """Verify color themes have required color keys."""
        required_keys = {'primary', 'secondary', 'accent', 'background', 'text'}
        for theme_name, theme_colors in Config.COLOR_THEMES.items():
            assert set(theme_colors.keys()) == required_keys, \
                f"Theme '{theme_name}' missing required color keys"

    def test_professional_blue_theme_exists(self):
        """Verify professional-blue theme is configured."""
        assert 'professional-blue' in Config.COLOR_THEMES
        theme = Config.COLOR_THEMES['professional-blue']
        assert theme['primary'] == '#2C3E50'

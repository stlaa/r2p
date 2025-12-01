"""Tests for portfolio generator module."""
import pytest
from utils.portfolio_generator import PortfolioGenerator


class TestPortfolioGeneratorInitialization:
    """Test portfolio generator initialization."""

    def test_portfolio_generator_init(self):
        """Test PortfolioGenerator initialization."""
        api_key = "test_key"
        api_url = "https://api.example.com"
        model = "test_model"

        generator = PortfolioGenerator(api_key, api_url, model)

        assert generator.api_key == api_key
        assert generator.api_url == api_url
        assert generator.model == model

    def test_portfolio_generator_attributes_not_none(self):
        """Test that all generator attributes are not None."""
        generator = PortfolioGenerator("key", "url", "model")

        assert generator.api_key is not None
        assert generator.api_url is not None
        assert generator.model is not None

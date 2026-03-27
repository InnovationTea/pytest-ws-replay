"""
Tests for URL matcher.
"""
import pytest
from vcr_code.matcher import Matcher


class TestMatcher:
    """Test Matcher class."""

    def test_matcher_init_default(self):
        """Test Matcher initialization with default fuzzy match."""
        matcher = Matcher()
        assert matcher.enable_fuzzy_match is True

    def test_matcher_init_no_fuzzy(self):
        """Test Matcher initialization without fuzzy match."""
        matcher = Matcher(enable_fuzz_match=False)
        assert matcher.enable_fuzzy_match is False

    def test_matcher_exact_url_match(self):
        """Test exact URL matching."""
        matcher = Matcher()
        data = {
            "ws://example.com/chat": []
        }
        result = matcher.find_best_match("ws://example.com/chat", data)
        assert result == "ws://example.com/chat"

    def test_matcher_no_match_returns_none(self):
        """Test None is returned when no match found."""
        matcher = Matcher(enable_fuzz_match=False)
        data = {
            "ws://example.com/chat": []
        }
        result = matcher.find_best_match("ws://other.com/test", data)
        assert result is None

    def test_matcher_fuzzy_match_by_path(self):
        """Test fuzzy matching by URL path."""
        matcher = Matcher(enable_fuzz_match=True)
        data = {
            "ws://example.com/chat?token=abc": []
        }
        result = matcher.find_best_match("ws://example.com/chat", data)
        assert result == "ws://example.com/chat?token=abc"

    def test_matcher_fuzzy_match_with_query_params(self):
        """Test fuzzy matching ignores query parameters."""
        matcher = Matcher(enable_fuzz_match=True)
        data = {
            "ws://example.com/chat": []
        }
        result = matcher.find_best_match("ws://example.com/chat?token=123", data)
        assert result == "ws://example.com/chat"

    def test_matcher_fuzzy_match_disabled(self):
        """Test fuzzy match returns None when disabled."""
        matcher = Matcher(enable_fuzz_match=False)
        data = {
            "ws://example.com/chat?token=abc": []
        }
        result = matcher.find_best_match("ws://example.com/chat", data)
        assert result is None

    def test_matcher_extract_path(self):
        """Test path extraction from URL."""
        matcher = Matcher()
        path = matcher._extract_path("ws://example.com/chat")
        assert path == "/chat"

    def test_matcher_extract_path_with_query(self):
        """Test path extraction ignores query parameters."""
        matcher = Matcher()
        path = matcher._extract_path("ws://example.com/chat?token=abc&id=123")
        assert path == "/chat"

    def test_matcher_extract_path_with_fragment(self):
        """Test path extraction ignores fragment."""
        matcher = Matcher()
        path = matcher._extract_path("ws://example.com/chat#section")
        assert path == "/chat"

    def test_matcher_find_best_url_alias(self):
        """Test find_best_url is alias for find_best_match."""
        matcher = Matcher()
        data = {
            "ws://example.com/chat": []
        }
        result = matcher.find_best_url("ws://example.com/chat", data)
        assert result == "ws://example.com/chat"

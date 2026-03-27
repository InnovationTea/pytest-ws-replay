"""
Tests for configuration classes.
"""
import pytest
from pathlib import Path
from model.config import RecordMode, VCRConfig, MatcherConfig


class TestRecordMode:
    """Test RecordMode enum."""

    def test_record_mode_enum_values(self):
        """Test all record mode enum values."""
        assert RecordMode.ONCE.value == "once"
        assert RecordMode.REWRITE.value == "rewrite"
        assert RecordMode.ALL.value == "all"
        assert RecordMode.NONE.value == "none"
        assert RecordMode.NEW_EPISODES.value == "new_episodes"


class TestVCRConfig:
    """Test VCRConfig dataclass."""

    def test_vcr_config_defaults(self):
        """Test VCRConfig default values."""
        config = VCRConfig()
        assert config.record_mode == RecordMode.ONCE
        assert config.cassette_dir == "cassette/websocket_recording"
        assert config.enable_fuzzy_match is True
        assert config.project_root is None
        assert config.stable_cassette_dir == "cassette/stable"
        assert config.daily_cassette_dir == "{date}"
        assert config.max_message_size == 10 * 1024 * 1024
        assert config.encoding == "utf-8"

    def test_vcr_config_cassette_path_without_project_root(self):
        """Test cassette_path without project_root."""
        config = VCRConfig()
        path = config.cassette_path
        assert isinstance(path, Path)
        assert str(path).endswith("cassette\websocket_recording")

    def test_vcr_config_cassette_path_with_project_root(self):
        """Test cassette_path with custom project_root."""
        config = VCRConfig(project_root="\custom\path")
        path = config.cassette_path
        assert isinstance(path, Path)
        assert str(path).startswith("\custom\path")
        assert str(path).endswith("cassette\websocket_recording")


class TestMatcherConfig:
    """Test MatcherConfig dataclass."""

    def test_matcher_config_defaults(self):
        """Test MatcherConfig default values."""
        config = MatcherConfig()
        assert config.enable_fuzzy_match is True
        assert config.match_path_only is True
        assert config.strict_host is False
        assert config.ignore_query_params is True
        assert config.ignore_fragment is True

    def test_matcher_config_custom_values(self):
        """Test MatcherConfig with custom values."""
        config = MatcherConfig(
            enable_fuzzy_match=False,
            strict_host=True,
            ignore_query_params=False
        )
        assert config.enable_fuzzy_match is False
        assert config.strict_host is True
        assert config.ignore_query_params is False

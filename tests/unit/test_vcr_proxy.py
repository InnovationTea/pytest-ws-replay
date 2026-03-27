"""
Tests for VCRProxy class.
"""
import pytest
from vcr_code.vcr_proxy import VCRProxy
from storage.storage import CassetteStorage
from unittest.mock import AsyncMock, MagicMock


class TestVCRProxy:
    """Test VCRProxy main class."""

    def test_vcr_proxy_init_idle_mode(self):
        """Test VCRProxy initializes in idle mode."""
        proxy = VCRProxy()
        assert proxy.mode == 'idle'
        assert proxy.storage is None
        assert proxy.query is None
        assert proxy.recorder is None
        assert proxy.player is None
        assert proxy.matcher is None
        assert proxy.playback_interaction_indices == {}

    def test_vcr_proxy_set_record_mode(self, storage_instance):
        """Test switching to record mode."""
        proxy = VCRProxy()
        proxy.set_record_mode("test_query", storage_instance)

        assert proxy.mode == 'record'
        assert proxy.query == "test_query"
        assert proxy.storage == storage_instance
        assert proxy.recorder is not None
        assert proxy.player is None

    def test_vcr_proxy_set_playback_mode(self, storage_instance):
        """Test switching to playback mode."""
        proxy = VCRProxy()
        data = {"ws://example.com": []}
        proxy.set_playback_mode("test_query", storage_instance, data)

        assert proxy.mode == 'playback'
        assert proxy.query == "test_query"
        assert proxy.storage == storage_instance
        assert proxy.player is not None
        assert proxy.recorder is None

    def test_vcr_proxy_has_requirements_true(self, storage_instance):
        """Test _has_requirements returns True when all set."""
        proxy = VCRProxy()
        proxy.set_record_mode("test_query", storage_instance)

        assert proxy._has_requirements() is True

    def test_vcr_proxy_has_requirements_false_mode(self, storage_instance):
        """Test _has_requirements returns False when mode wrong."""
        proxy = VCRProxy()
        proxy.mode = 'idle'
        proxy.recorder = MagicMock()
        proxy.query = "test"
        proxy.storage = storage_instance

        assert proxy._has_requirements() is False

    def test_vcr_proxy_has_requirements_false_no_recorder(self, storage_instance):
        """Test _has_requirements returns False when no recorder."""
        proxy = VCRProxy()
        proxy.mode = 'record'
        proxy.recorder = None
        proxy.query = "test"
        proxy.storage = storage_instance

        assert proxy._has_requirements() is False

    def test_vcr_proxy_cleanup(self, storage_instance):
        """Test cleanup clears state."""
        proxy = VCRProxy()
        proxy.set_record_mode("test_query", storage_instance)
        proxy.playback_interaction_indices["test_url"] = 5

        proxy.cleanup()

        assert proxy.mode == 'idle'
        assert proxy.playback_interaction_indices == {}


    def test_vcr_proxy_save_recording(self, storage_instance):
        """Test save_recording calls recorder.save_recording."""
        proxy = VCRProxy()
        proxy.set_record_mode("test_query", storage_instance)

        proxy.recorder.save_recording = MagicMock()

        proxy.save_recording()
        proxy.recorder.save_recording.assert_called_once_with("test_query", storage_instance)

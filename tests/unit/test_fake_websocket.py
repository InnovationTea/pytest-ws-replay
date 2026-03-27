"""
Tests for FakeWebSocket class.
"""
import pytest
import asyncio
from vcr_code.fake_websocket import FakeWebSocket
from unittest.mock import Mock


class TestFakeWebSocket:
    """Test FakeWebSocket class."""

    def test_fake_websocket_init(self, sample_interactions):
        """Test FakeWebSocket initialization."""
        mock_parent_vcr = Mock()
        fake_ws = FakeWebSocket(
            interactions=sample_interactions,
            target_url="ws://example.com/test",
            parent_vcr= mock_parent_vcr
        )
        assert fake_ws.interactions == sample_interactions
        assert fake_ws.target_url == "ws://example.com/test"
        assert fake_ws.closed is False
        assert fake_ws.state == "OPEN"

    @pytest.mark.asyncio
    async def test_fake_websocket_send_no_op(self, sample_interactions):
        """Test send is no-op in playback mode."""
        mock_parent_vcr = Mock()
        mock_parent_vcr.playback_interaction_indices = {"ws://example.com/test": 0}
        fake_ws = FakeWebSocket(
            interactions=sample_interactions,
            target_url="ws://example.com/test",
            parent_vcr=mock_parent_vcr
        )
        # Should not raise
        await fake_ws.send("Test message")
        assert fake_ws.current_response == ["Response 1", "Response 2"]
        assert fake_ws.parent_vcr.playback_interaction_indices.get("ws://example.com/test") == 1

    @pytest.mark.asyncio
    async def test_fake_websocket_recv_single_response(self, sample_interactions):
        """Test recv returns single response."""
        mock_parent_vcr=Mock()
        mock_parent_vcr.playback_interaction_indices = {"ws://example.com/test": 0}
        fake_ws = FakeWebSocket(
            interactions=sample_interactions,
            target_url="ws://example.com/test",
            parent_vcr= mock_parent_vcr
        )

        await fake_ws.send("Test message")

        result = await fake_ws.recv()
        assert result == "Response 1"


    @pytest.mark.asyncio
    async def test_fake_websocket_close(self, sample_interactions):
        """Test close method."""
        fake_ws = FakeWebSocket(
            interactions=sample_interactions,
            target_url="ws://example.com/test",
            parent_vcr= Mock()
        )
        await fake_ws.close()

        assert fake_ws.closed is True
        assert fake_ws.state == "CLOSED"

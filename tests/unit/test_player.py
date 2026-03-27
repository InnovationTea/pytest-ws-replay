"""
Tests for Player class.
"""
import pytest
from unittest.mock import MagicMock
from vcr_code.vcr_proxy import Player


class TestPlayer:
    """Test Player class."""

    def test_player_init(self):
        """Test Player initialization."""
        proxy = MagicMock()
        player = Player(proxy)

        assert player.vcr_proxy == proxy
        assert player.playback_data == {}
        assert player.playback_indices == {}

    def test_player_load_playback_data(self):
        """Test load_playback_data sets data and clears indices."""
        proxy = MagicMock()
        player = Player(proxy)

        data = {
            "ws://example.com/chat": [],
            "ws://example.com/updates": []
        }
        player.load_playback_data(data)

        assert player.playback_data == data
        assert player.playback_indices == {}

    def test_player_create_fake_websocket_with_data(self):
        """Test create_fake_websocket with matching data."""
        from unittest.mock import patch

        proxy = MagicMock()
        player = Player(proxy)

        data = {
            "ws://example.com/chat": [
                {"type": "interaction", 
                "request": None, 
                "response": ["msg"]}
            ]
        }
        player.load_playback_data(data)

        with patch("vcr_code.vcr_proxy.FakeWebSocket") as mock_fake_ws:
            fake_ws_instance = MagicMock()
            mock_fake_ws.return_value = fake_ws_instance

            matcher = MagicMock()
            result = player.create_fake_websocket("ws://example.com/chat", matcher)

            assert result == fake_ws_instance

    def test_player_create_fake_websocket_no_data(self):
        """Test create_fake_websocket with no matching data."""
        from unittest.mock import patch

        proxy = MagicMock()
        player = Player(proxy)

        data = {}
        player.load_playback_data(data)

        with patch("vcr_code.vcr_proxy.FakeWebSocket") as mock_fake_ws:
            fake_ws_instance = MagicMock()
            mock_fake_ws.return_value = fake_ws_instance

            matcher = MagicMock()
            result = player.create_fake_websocket("ws://example.com/chat", matcher)

            # Should still return FakeWebSocket, but with empty data
            assert result == fake_ws_instance

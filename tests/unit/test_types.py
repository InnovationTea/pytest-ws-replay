"""
Tests for data model types.
"""
import pytest
from model.types import WebsocketMessage, Interaction, CassetteData, PlaybackState


class TestWebsocketMessage:
    """Test WebsocketMessage dataclass."""

    def test_websocket_message_creation(self):
        """Test creating a WebsocketMessage."""
        msg = WebsocketMessage(
            content="Hello",
            timestamp=1234567890.123,
            direction="send",
            message_type="text"
        )
        assert msg.content == "Hello"
        assert msg.timestamp == 1234567890.123
        assert msg.direction == "send"
        assert msg.message_type == "text"

    def test_websocket_message_default_type(self):
        """Test default message_type is 'text'."""
        msg = WebsocketMessage(
            content="Test",
            timestamp=1234567890.123,
            direction="recv"
        )
        assert msg.message_type == "text"

    def test_websocket_message_is_control_true(self):
        """Test is_control returns True for control messages."""
        msg = WebsocketMessage(
            content="ping",
            timestamp=1234567890.123,
            direction="send",
            message_type="control"
        )
        assert msg.is_control is True

    def test_websocket_message_is_control_false(self):
        """Test is_control returns False for non-control messages."""
        msg = WebsocketMessage(
            content="Hello",
            timestamp=1234567890.123,
            direction="recv",
            message_type="text"
        )
        assert msg.is_control is False


class TestInteraction:
    """Test Interaction TypedDict."""

    def test_interaction_dict_structure(self):
        """Test Interaction has correct structure."""
        interaction: Interaction = {
            "type": "interaction",
            "request": "Hello",
            "response": ["Hello back"],
            "timestamp": 1234567890.123,
            "metadata": {}
        }
        assert interaction["type"] == "interaction"
        assert interaction["request"] == "Hello"
        assert interaction["response"] == ["Hello back"]
        assert interaction["timestamp"] == 1234567890.123
        assert interaction["metadata"] == {}

    def test_interaction_with_null_request(self):
        """Test Interaction with null request (server-initiated)."""
        interaction: Interaction = {
            "type": "interaction",
            "request": None,
            "response": ["Server push"],
            "timestamp": 1234567890.123,
            "metadata": {}
        }
        assert interaction["request"] is None
        assert interaction["response"] == ["Server push"]


class TestCassetteData:
    """Test CassetteData TypedDict."""

    def test_cassette_data_dict_structure(self):
        """Test CassetteData has correct structure."""
        cassette: CassetteData = {
            "url": "ws://example.com/test",
            "interactions": [],
            "created_at": "2026-03-25T10:30:00Z",
            "session_info": {}
        }
        assert cassette["url"] == "ws://example.com/test"
        assert cassette["interactions"] == []
        assert cassette["created_at"] == "2026-03-25T10:30:00Z"
        assert cassette["session_info"] == {}


class TestPlaybackState:
    """Test PlaybackState dataclass."""

    def test_playback_state_init(self):
        """Test PlaybackState initialization."""
        state = PlaybackState(url="ws://example.com/test")
        assert state.url == "ws://example.com/test"
        assert state.interaction_index == 0
        assert state.response_index == 0
        assert state.is_complete is False

    def test_playback_state_advance(self):
        """Test PlaybackState advance method."""
        state = PlaybackState(url="ws://example.com/test")
        state.advance()
        assert state.interaction_index == 1
        assert state.response_index == 0

    def test_playback_state_multiple_advances(self):
        """Test multiple advances."""
        state = PlaybackState(url="ws://example.com/test")
        for i in range(5):
            state.advance()
        assert state.interaction_index == 5

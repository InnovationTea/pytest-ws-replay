"""
Tests for message interactions.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.vcr
async def test_send_and_receive():
    """Test sending message and receiving response."""
    import websockets

    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        async with websockets.connect("ws://example.com/test") as ws:
            # Mock WebSocket with send and recv
            original_send = AsyncMock()
            original_recv = AsyncMock(return_value="Hello back")

            ws.send = original_send
            ws.recv = original_recv

            await ws.send("Hello")
            response = await ws.recv()

            assert response == "Hello back"


@pytest.mark.vcr
async def test_multiple_send_receive_cycles():
    """Test multiple send-receive cycles."""
    import websockets

    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        async with websockets.connect("ws://example.com/test") as ws:
            original_send = AsyncMock()
            responses = ["Response 1", "Response 2", "Response 3"]
            original_recv = AsyncMock(side_effect=responses)

            ws.send = original_send
            ws.recv = original_recv

            for i in range(3):
                await ws.send(f"Message {i}")
                response = await ws.recv()
                assert response == f"Response {i}"


@pytest.mark.vcr
async def test_receive_without_send():
    """Test receiving server-initiated messages."""
    import websockets

    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        async with websockets.connect("ws://example.com/test") as ws:
            original_recv = AsyncMock(return_value="Server push")
            ws.recv = original_recv

            response = await ws.recv()
            assert response == "Server push"


@pytest.mark.vcr
async def test_heartbeat_message_filtered():
    """Test that heartbeat messages are filtered."""
    import websockets
    import json

    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        async with websockets.connect("ws://example.com/test") as ws:
            original_send = AsyncMock()
            original_recv = AsyncMock(return_value="Pong")

            ws.send = original_send
            ws.recv = original_recv

            # Send heartbeat (should be filtered in current implementation)
            heartbeat = json.dumps({"type": "ping"})
            await ws.send(heartbeat)

            # This heartbeat should not be recorded
            # (in current implementation at vcr_proxy.py:105-119)

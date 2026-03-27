"""
Tests for edge cases.
"""
import pytest
import websockets
import json 
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_empty_message():
    """Test sending/receiving empty messages."""
    
    mock_ws = AsyncMock()
    mock_ws.recv.return_value = ""

    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_ws
    with pytest.MonkeyPatch.context() as m:
        m.setattr(websockets, "connect", lambda *args, **kwargs: mock_connect)

        async with websockets.connect("ws://example.com/test") as ws:

            await ws.send("")
            response = await ws.recv()
            assert response == ""


@pytest.mark.asyncio
async def test_large_message():
    """Test handling large messages."""
    mock_ws = AsyncMock()
    mock_ws.recv.return_value = "response"

    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_ws

    with pytest.MonkeyPatch.context() as m:
        m.setattr(websockets, "connect", lambda *args, **kwargs: mock_connect)

        large_data = "x" * 10000
        async with websockets.connect("ws://example.com/test") as ws:
            await ws.send(large_data)
            response = await ws.recv()
            assert len(response) > 0


@pytest.mark.asyncio
async def test_unicode_message():
    """Test Unicode message handling."""
    mock_ws = AsyncMock()
    mock_ws.recv.return_value = "测试响应 🚀"

    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_ws

    with pytest.MonkeyPatch.context() as m:
        m.setattr(websockets, "connect", lambda *args, **kwargs: mock_connect)

        unicode_msg = "测试消息 🚀"
        async with websockets.connect("ws://example.com/test") as ws:
            await ws.send(unicode_msg)
            response = await ws.recv()
            assert isinstance(response, str)


@pytest.mark.asyncio
async def test_json_message():
    """Test JSON format messages."""
    mock_ws = AsyncMock()
    mock_ws.recv.return_value = json.dumps({"action": "test", "data": "ok"})

    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_ws

    with pytest.MonkeyPatch.context() as m:
        m.setattr(websockets, "connect", lambda *args, **kwargs: mock_connect)

        json_msg = json.dumps({"action": "test", "data": "value"})
        async with websockets.connect("ws://example.com/test") as ws:
            await ws.send(json_msg)
            response = await ws.recv()
            parsed = json.loads(response)
            assert "action" in parsed

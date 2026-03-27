"""
Tests for multiple WebSocket connections.
"""
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
@pytest.mark.vcr
async def test_concurrent_connections():
    """Test multiple concurrent WebSocket connections."""
    import websockets

    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        # Create multiple connections concurrently
        async with websockets.connect("ws://example.com/chat") as ws1:
            async with websockets.connect("ws://example.com/updates") as ws2:
                assert ws1 is not None
                assert ws2 is not None

@pytest.mark.asyncio
@pytest.mark.vcr
async def test_sequential_connections():
    """Test sequentially establishing multiple connections."""
    import websockets

    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        connections = []
        for url in ["ws://example.com/chat", "ws://example.com/updates"]:
            async with websockets.connect(url) as ws:
                connections.append(ws)

        assert len(connections) == 2
        assert all(c is not None for c in connections)

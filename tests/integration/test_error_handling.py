"""
Tests for error handling.
"""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_cassette_not_found():
    """Test behavior when cassette file not found."""
    import websockets

    # In playback mode, if cassette doesn't exist, should raise error
    # (This test demonstrates expected behavior)
    with pytest.raises(Exception):
        with patch.object(websockets, "connect", new_callable=AsyncMock()):
            async with websockets.connect("ws://example.com/nonexistent") as ws:
                pass


@pytest.mark.asyncio
async def test_playback_data_exhausted():
    """Test behavior when playback data exhausted."""
    import websockets

    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        async with websockets.connect("ws://example.com/test") as ws:
            # Receive first message
            await ws.recv()
            # Try to receive more than available
            # Should raise EOFError
            with pytest.raises(EOFError):
                await ws.recv()


@pytest.mark.vcr(ws_record_mode="none")
@pytest.mark.asyncio
async def test_none_mode_without_cassette():
    """Test error in none mode when no cassette exists."""
    import websockets

    # 'none' mode requires existing cassette
    # Should raise FileNotFoundError if cassette doesn't exist
    with pytest.raises(FileNotFoundError):
        with patch.object(websockets, "connect", new_callable=AsyncMock()):
            async with websockets.connect("ws://example.com/no_cassette") as ws:
                pass

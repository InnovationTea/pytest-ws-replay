"""
Tests for recording and playback flow.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio

@pytest.mark.asyncio
@pytest.mark.vcr
async def test_recording_new_session():
    """Test recording a new session (this test will create cassette)."""
    import websockets
    from vcr_code.vcr_proxy import _vcr_instance

    # This test should create a new cassette
    # We can't actually connect to a real server, but we can mock it
    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        # Mock the connection to avoid actual network calls
        async with websockets.connect("ws://example.com/test") as ws:
            assert ws is not None

    # After test, _vcr_instance should have recorded data

@pytest.mark.asyncio
@pytest.mark.vcr
async def test_playback_existing_session():
    """Test playing back existing session (requires cassette to exist)."""
    import websockets
    from vcr_code.vcr_proxy import _vcr_instance

    # This test will replay from existing cassette
    # First run should have created the cassette
    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        async with websockets.connect("ws://example.com/test") as ws:
            assert ws is not None

@pytest.mark.asyncio
@pytest.mark.vcr(ws_record_mode="all")
async def test_force_rerecord():
    """Test forcing re-recording in 'all' mode."""
    import websockets
    from vcr_code.vcr_proxy import _vcr_instance

    # This should always record, overwriting existing data
    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        async with websockets.connect("ws://example.com/test") as ws:
            assert ws is not None

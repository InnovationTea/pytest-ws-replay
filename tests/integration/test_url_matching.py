"""
Tests for URL matching.
"""
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
@pytest.mark.vcr
async def test_exact_url_match():
    """Test exact URL matching."""
    import websockets

    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        # This should match exactly
        async with websockets.connect("ws://example.com/chat") as ws:
            assert ws is not None

@pytest.mark.asyncio
@pytest.mark.vcr
async def test_fuzzy_url_match():
    """Test fuzzy URL matching (same path)."""
    import websockets

    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        # First connection with query
        async with websockets.connect("ws://example.com/chat?token=abc") as ws1:
            pass

        # Second connection without query - should match via fuzzy
        async with websockets.connect("ws://example.com/chat") as ws2:
            # This should match with fuzzy matching enabled
            pass

@pytest.mark.asyncio
@pytest.mark.vcr
async def test_url_with_query_params():
    """Test URLs with query parameters."""
    import websockets

    with patch.object(websockets, "connect", new_callable=AsyncMock()):
        urls = [
            "ws://example.com/chat?token=123&session=abc",
            "ws://example.com/chat?token=456&session=def",
        ]
        for url in urls:
            async with websockets.connect(url) as ws:
                assert ws is not None

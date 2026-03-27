"""
Shared pytest fixtures for websocket-recording tests.

This conftest.py provides common fixtures used across unit and integration tests.
"""
import sys
from pathlib import Path
import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from vcr_code.vcr_proxy import VCRProxy
from storage.storage import CassetteStorage


@pytest.fixture(scope="session")
def shared_test_data():
    """Load and share test cassette data across tests."""
    import json

    fixtures_dir = Path(__file__).parent / "fixtures" / "cassettes"
    test_data = {}

    for cassette_file in fixtures_dir.glob("*.json"):
        with open(cassette_file, "r", encoding="utf-8") as f:
            test_data[cassette_file.stem] = json.load(f)

    return test_data


@pytest.fixture
def temp_storage_dir(tmp_path):
    """Create a temporary storage directory for testing."""
    storage_dir = tmp_path / "cassette"/"websocket_recording"
    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir


@pytest.fixture
def vcr_instance():
    """Provide a fresh VCRProxy instance for each test."""
    instance = VCRProxy()
    yield instance
    instance.cleanup()


@pytest.fixture
def storage_instance(tmp_path):
    """Provide a CassetteStorage instance with temp directory."""
    return CassetteStorage(project_root = tmp_path)


@pytest.fixture
def sample_cassette_data():
    """Provide sample cassette data for testing."""
    return {
        "url": "ws://example.com/test",
        "interactions": [
            {
                "type": "interaction",
                "request": "Hello",
                "response": ["Hello back"]
            },
            {
                "type": "interaction",
                "request": None,
                "response": ["Server message"]
            }
        ]
    }


@pytest.fixture
def multi_url_cassette_data():
    """Provide cassette data with multiple URLs."""
    return {
        "ws://example.com/chat": [
            {
                "type": "interaction",
                "request": "chat message",
                "response": ["chat response"]
            }
        ],
        "ws://example.com/updates": [
            {
                "type": "interaction",
                "request": "subscribe",
                "response": ["update 1", "update 2"]
            }
        ]
    }


@pytest.fixture
def sample_interactions():
    """Provide sample interactions for FakeWebSocket testing."""
    return [
        {
            "type": "interaction",
            "request": "Test message",
            "response": ["Response 1", "Response 2"]
        },
        {
            "type": "interaction",
            "request": None,
            "response": ["Server push"]
        }
    ]

"""
Cassette fixtures for testing.

This module provides functions to load test cassette data.
"""
import json
from pathlib import Path


def load_sample_cassette():
    """Load simple chat cassette."""
    fixtures_dir = Path(__file__).parent / "cassettes"
    with open(fixtures_dir / "simple_chat.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_multi_url_cassette():
    """Load multi-url cassette."""
    fixtures_dir = Path(__file__).parent / "cassettes"
    with open(fixtures_dir / "multi_url.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_empty_cassette():
    """Load empty cassette."""
    fixtures_dir = Path(__file__).parent / "cassettes"
    with open(fixtures_dir / "empty.json", "r", encoding="utf-8") as f:
        return json.load(f)

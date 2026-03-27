"""
Tests for CassetteStorage class.
"""
import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from storage.storage import CassetteStorage


class TestCassetteStorage:
    """Test CassetteStorage class."""

    def test_storage_init_with_project_root(self):
        """Test CassetteStorage with custom project root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_root = Path(tmpdir)/ "custom"
            storage = CassetteStorage(
                base_dir="custom_cassettes",
                project_root=str(custom_root)
            )
            assert str(storage.base_dir).startswith(str(custom_root))
            assert str(storage.base_dir).endswith("custom_cassettes")

    def test_sanitize_filename_basic(self):
        """Test basic filename sanitization."""
        storage = CassetteStorage(project_root="test")
        result = storage._sanitize_filename("test_name")
        assert result == "test_name"

    def test_sanitize_filename_with_special_chars(self):
        """Test sanitization removes special characters."""
        storage = CassetteStorage(project_root="test")
        result = storage._sanitize_filename("test<>:\"/\\|?*name")
        assert all(c not in result for c in '<>:"/\\|?*')

    def test_sanitize_filename_unicode(self):
        """Test sanitization handles unicode."""
        storage = CassetteStorage(project_root="test")
        result = storage._sanitize_filename("测试名称")
        assert result == "测试名称"

    def test_find_cassette_in_stable_dir(self, temp_storage_dir, tmp_path):
        """Test finding cassette in stable directory."""
        stable_dir = temp_storage_dir / "stable"
        stable_dir.mkdir()
        cassette_file = stable_dir / "ws_test.json" 
        cassette_file.touch()

        storage = CassetteStorage(project_root = tmp_path)
        result = storage.find_cassette("test")
        assert result == cassette_file


    def test_find_cassette_not_found(self, tmp_path):
        """Test None returned when cassette not found."""
        storage = CassetteStorage(project_root = tmp_path)
        result = storage.find_cassette("nonexistent")
        assert result is None


    def test_get_save_path_creates_dated_dir(self, tmp_path):
        """Test save path creates dated directory."""
        from unittest.mock import patch
        from datetime import datetime, timezone

        with patch('datetime.datetime') as mock_datetime:
            # Mock to consistent date
            mock_now = datetime(2026, 3, 26, 10, 30, tzinfo=timezone.utc)
            mock_datetime.now.return_value = mock_now

            storage = CassetteStorage(project_root = tmp_path)
            path = storage.get_save_path("test")

            assert path.exists() is False 
            assert path.parent.exists() 
            assert path.parent.name.startswith("2026-")  

    def test_save_and_load_cassette(self, tmp_path):
        """Test saving and loading cassette data."""
        storage = CassetteStorage(project_root = tmp_path)
        data = {
            "url": "ws://example.com/test",
            "interactions": [],
            "created_at": "2026-03-26T10:30:00Z",
            "session_info": {}
        }

        storage.save("test", data)

        path = storage.get_save_path("test")
        loaded = storage.load(path)
        assert loaded["url"] == data["url"]
        assert loaded["interactions"] == data["interactions"]
    

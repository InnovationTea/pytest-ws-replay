from enum import Enum
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


class RecordMode(Enum):
    """Enumeration of available recording modes."""
    ONCE = 'once'
    REWRITE = 'rewrite'
    ALL = 'all'
    NONE = 'none'
    NEW_EPISODES = 'new_episodes'


@dataclass
class VCRConfig:  
    """Configuration for VCR behavior."""
    record_mode: RecordMode = RecordMode.ONCE
    cassette_dir: str = 'cassette/websocket_recording'
    enable_fuzzy_match: bool = True
    project_root: Optional[str] = None
    stable_cassette_dir: str = 'cassette/stable'
    daily_cassette_dir: str = '{date}'
    max_message_size: int = 10 * 1024 * 1024  # 10MB
    encoding: str = 'utf-8'

    @property
    def cassette_path(self) -> Path:
        """Get the base path for cassette storage."""
        if self.project_root:
            return Path(self.project_root) / self.cassette_dir
        return Path(self.cassette_dir)


@dataclass
class MatcherConfig:
    """Configuration for URL matching."""
    enable_fuzzy_match: bool = True
    match_path_only: bool = True
    strict_host: bool = False
    ignore_query_params: bool = True
    ignore_fragment: bool = True

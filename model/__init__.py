"""
VCR Model Definitions

This module contains data structures and types used throughout the WebSocket VCR package.
"""

from .types import Interaction, CassetteData, WebsocketMessage, PlaybackState
from .config import RecordMode, VCRConfig, MatcherConfig
from .exceptations import VCRError, CassetteError, PlaybackError

__all__ = [
    "Interaction",
    "CassetteData",
    "WebsocketMessage",
    "PlaybackState",
    "RecordMode",
    "VCRConfig",
    "MatcherConfig",
    "VCRError",
    "CassetteError",
    "PlaybackError"
]
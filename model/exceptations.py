"""
VCR Exceptions

This module defines custom exceptions used throughout the WebSocket VCR package.
"""


class VCRError(Exception):
    """Base exception for VCR-related errors."""
    pass


class CassetteError(VCRError):
    """Exception raised when there are issues with cassette files."""
    pass


class PlaybackError(VCRError):
    """Exception raised during playback of recorded interactions."""
    pass


class RecordingError(VCRError):
    """Exception raised during recording of WebSocket interactions."""
    pass


class ConfigurationError(VCRError):
    """Exception raised for configuration-related issues."""
    pass
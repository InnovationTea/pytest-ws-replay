"""
WebSocket VCR - A pytest plugin for recording and replaying WebSocket interactions.

This package provides a VCR (Video Cassette Recorder) pattern for WebSocket connections,
allowing you to record WebSocket interactions during tests and replay them later.
"""

from .vcr_code.vcr_proxy import _vcr_instance

__version__ = "0.1.0"
__all__ = ["_vcr_instance"]
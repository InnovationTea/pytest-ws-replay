"""
VCR Plugin Module

This module provides pytest fixtures and utilities for WebSocket VCR integration.
"""

from .plugin import vcr_context, mock_websockets

__all__ = ["vcr_context", "mock_websockets"]
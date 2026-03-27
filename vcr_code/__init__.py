"""
VCR Core Module

This module contains the core VCR proxy and related classes.
"""

from .vcr_proxy import VCRProxy, Recorder, Player, _vcr_instance
from .fake_websocket import FakeWebSocket
from .matcher import Matcher

__all__ = ["VCRProxy", "Recorder", "Player", "FakeWebSocket", "Matcher", "_vcr_instance"]
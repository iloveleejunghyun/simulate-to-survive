"""
Simulate to Survive - A text-based survival simulation game with emotional storytelling
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core.game import Game
from .core.scene_manager import SceneManager
from .core.audio_manager import AudioManager
from .core.emotion_system import EmotionSystem

__all__ = [
    "Game",
    "SceneManager", 
    "AudioManager",
    "EmotionSystem",
]

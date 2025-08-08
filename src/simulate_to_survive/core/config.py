"""
Configuration system for Simulate to Survive
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class AudioConfig:
    """Audio configuration settings"""
    master_volume: float = 1.0
    music_volume: float = 0.8
    sfx_volume: float = 0.9
    voice_volume: float = 1.0
    ambient_volume: float = 0.7
    
    # Audio file paths
    audio_path: str = "assets/audio"
    sfx_path: str = "assets/audio/sfx"
    music_path: str = "assets/audio/music"
    voice_path: str = "assets/audio/voice"
    
    # Audio format settings
    sample_rate: int = 44100
    bit_depth: int = 16
    channels: int = 2


@dataclass
class DisplayConfig:
    """Display and UI configuration"""
    window_width: int = 1280
    window_height: int = 720
    fullscreen: bool = False
    vsync: bool = True
    fps: int = 60
    
    # Font settings
    font_path: str = "assets/fonts"
    default_font: str = "NotoSansSC-Regular.ttf"
    font_size: int = 24
    line_spacing: float = 1.2
    
    # Text animation settings
    text_speed: float = 1.0  # 1.0 = normal, 0.5 = slow, 2.0 = fast
    auto_advance: bool = False
    auto_advance_delay: float = 3.0  # seconds


@dataclass
class GameConfig:
    """Game-specific configuration"""
    language: str = "zh_CN"
    save_path: str = "saves"
    auto_save: bool = True
    auto_save_interval: int = 5  # minutes
    
    # Emotion system settings
    emotion_decay_rate: float = 0.1  # per minute
    max_emotion_value: int = 100
    min_emotion_value: int = 0
    
    # Simulation system settings
    simulation_time_scale: float = 1.0  # 1 day = 1 minute
    max_simulation_days: int = 1095  # 3 years


@dataclass
class Config:
    """Main configuration class"""
    audio: AudioConfig = field(default_factory=AudioConfig)
    display: DisplayConfig = field(default_factory=DisplayConfig)
    game: GameConfig = field(default_factory=GameConfig)
    
    def __post_init__(self):
        """Initialize configuration after creation"""
        self.config_path = Path("config")
        self.config_file = self.config_path / "game_config.yaml"
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    self._update_from_dict(data)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
                self.create_default_config()
        else:
            self.create_default_config()
    
    def save_config(self) -> None:
        """Save configuration to file"""
        self.config_path.mkdir(exist_ok=True)
        
        config_data = {
            'audio': self._dataclass_to_dict(self.audio),
            'display': self._dataclass_to_dict(self.display),
            'game': self._dataclass_to_dict(self.game)
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")
    
    def create_default_config(self) -> None:
        """Create default configuration file"""
        self.save_config()
    
    def _update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update configuration from dictionary"""
        if 'audio' in data:
            for key, value in data['audio'].items():
                if hasattr(self.audio, key):
                    setattr(self.audio, key, value)
        
        if 'display' in data:
            for key, value in data['display'].items():
                if hasattr(self.display, key):
                    setattr(self.display, key, value)
        
        if 'game' in data:
            for key, value in data['game'].items():
                if hasattr(self.game, key):
                    setattr(self.game, key, value)
    
    def _dataclass_to_dict(self, obj) -> Dict[str, Any]:
        """Convert dataclass to dictionary"""
        return {key: getattr(obj, key) for key in obj.__dataclass_fields__}
    
    def get_audio_file_path(self, category: str, filename: str) -> Path:
        """Get full path to audio file"""
        base_path = Path(self.audio.audio_path)
        if category == "sfx":
            return base_path / "sfx" / filename
        elif category == "music":
            return base_path / "music" / filename
        elif category == "voice":
            return base_path / "voice" / filename
        else:
            return base_path / filename
    
    def get_font_path(self, font_name: str) -> Path:
        """Get full path to font file"""
        return Path(self.display.font_path) / font_name
    
    def get_save_path(self) -> Path:
        """Get save directory path"""
        return Path(self.game.save_path)

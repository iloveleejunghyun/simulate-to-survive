"""
Audio manager for Simulate to Survive
Handles all audio playback including environment sounds, foley effects, and UI sounds
"""

import pygame
import os
from pathlib import Path
from typing import Dict, Optional, List, Any
from enum import Enum
import threading
import time


class AudioType(Enum):
    """Audio types"""
    AMBIENT = "ambient"      # 环境音效
    FOLEY = "foley"         # 拟音效果
    UI = "ui"               # 界面音效
    VOICE = "voice"         # 语音
    MUSIC = "music"         # 音乐


class AudioChannel:
    """Individual audio channel"""
    
    def __init__(self, channel_id: int, audio_type: AudioType):
        self.channel_id = channel_id
        self.audio_type = audio_type
        self.current_sound: Optional[pygame.mixer.Sound] = None
        self.volume = 1.0
        self.looping = False
        self.fade_out_time = 0
        
    def play(self, sound: pygame.mixer.Sound, volume: float = 1.0, loop: bool = False) -> bool:
        """Play sound on this channel"""
        try:
            channel = pygame.mixer.Channel(self.channel_id)
            if channel:
                channel.set_volume(volume * self.volume)
                channel.play(sound, loops=-1 if loop else 0)
                self.current_sound = sound
                self.looping = loop
                return True
        except Exception as e:
            print(f"Error playing sound on channel {self.channel_id}: {e}")
        return False
    
    def stop(self, fade_out: int = 0) -> None:
        """Stop current sound"""
        try:
            channel = pygame.mixer.Channel(self.channel_id)
            if channel:
                if fade_out > 0:
                    channel.fadeout(fade_out)
                else:
                    channel.stop()
                self.current_sound = None
                self.looping = False
        except Exception as e:
            print(f"Error stopping sound on channel {self.channel_id}: {e}")
    
    def set_volume(self, volume: float) -> None:
        """Set channel volume"""
        self.volume = max(0.0, min(1.0, volume))
        try:
            channel = pygame.mixer.Channel(self.channel_id)
            if channel:
                channel.set_volume(self.volume)
        except Exception as e:
            print(f"Error setting volume on channel {self.channel_id}: {e}")
    
    def is_playing(self) -> bool:
        """Check if channel is playing"""
        try:
            channel = pygame.mixer.Channel(self.channel_id)
            return channel and channel.get_busy()
        except:
            return False


class AudioManager:
    """Main audio manager class"""
    
    def __init__(self, config):
        self.config = config
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.channels: Dict[AudioType, AudioChannel] = {}
        self.ambient_sounds: List[str] = []
        self.current_ambient: Optional[str] = None
        
        # Initialize pygame mixer
        pygame.mixer.init(
            frequency=self.config.audio.sample_rate,
            size=-self.config.audio.bit_depth,
            channels=self.config.audio.channels,
            buffer=1024
        )
        
        # Set number of channels
        pygame.mixer.set_num_channels(16)
        
        # Initialize audio channels
        self._init_channels()
        
        # Load audio files
        self._load_audio_files()
    
    def _init_channels(self) -> None:
        """Initialize audio channels"""
        channel_id = 0
        for audio_type in AudioType:
            self.channels[audio_type] = AudioChannel(channel_id, audio_type)
            channel_id += 1
    
    def _load_audio_files(self) -> None:
        """Load all audio files"""
        audio_path = Path(self.config.audio.audio_path)
        
        # Load SFX files
        sfx_path = audio_path / "sfx"
        if sfx_path.exists():
            for category in ["environment", "foley", "ui"]:
                category_path = sfx_path / category
                if category_path.exists():
                    for audio_file in category_path.glob("*.wav"):
                        self._load_sound(audio_file, f"{category}_{audio_file.stem}")
        
        # Load music files
        music_path = audio_path / "music"
        if music_path.exists():
            # Load from main music directory
            for audio_file in music_path.glob("*.wav"):
                self._load_sound(audio_file, f"music_{audio_file.stem}")
            
            # Load from subdirectories (background, ambient, etc.)
            for subdir in music_path.iterdir():
                if subdir.is_dir():
                    for audio_file in subdir.glob("*.wav"):
                        # Use subdirectory name as prefix
                        self._load_sound(audio_file, f"{subdir.name}_{audio_file.stem}")
        
        # Load voice files
        voice_path = audio_path / "voice"
        if voice_path.exists():
            for audio_file in voice_path.glob("*.wav"):
                self._load_sound(audio_file, f"voice_{audio_file.stem}")
    
    def _load_sound(self, file_path: Path, sound_id: str) -> None:
        """Load individual sound file"""
        try:
            sound = pygame.mixer.Sound(str(file_path))
            self.sounds[sound_id] = sound
            print(f"Loaded audio: {sound_id}")
        except Exception as e:
            print(f"Error loading audio {file_path}: {e}")
    
    def play_sound(self, sound_id: str, audio_type: AudioType, volume: float = 1.0, loop: bool = False) -> bool:
        """Play sound by ID"""
        if sound_id not in self.sounds:
            print(f"Sound not found: {sound_id}")
            return False
        
        channel = self.channels.get(audio_type)
        if not channel:
            print(f"Audio channel not found: {audio_type}")
            return False
        
        # Apply volume based on audio type
        final_volume = volume * self._get_type_volume(audio_type)
        
        return channel.play(self.sounds[sound_id], final_volume, loop)
    
    def play_ambient(self, ambient_id: str, fade_in: int = 1000) -> bool:
        """Play ambient sound with fade in"""
        if self.current_ambient == ambient_id:
            return True
        
        # Stop current ambient
        self.stop_ambient()
        
        # Play new ambient
        success = self.play_sound(ambient_id, AudioType.AMBIENT, loop=True)
        if success:
            self.current_ambient = ambient_id
            # Apply fade in effect
            if fade_in > 0:
                self._fade_in_ambient(fade_in)
        
        return success
    
    def stop_ambient(self, fade_out: int = 1000) -> None:
        """Stop current ambient sound"""
        if self.current_ambient:
            channel = self.channels[AudioType.AMBIENT]
            channel.stop(fade_out)
            self.current_ambient = None
    
    def play_foley(self, foley_id: str, volume: float = 1.0) -> bool:
        """Play foley sound effect"""
        return self.play_sound(foley_id, AudioType.FOLEY, volume)
    
    def play_ui(self, ui_id: str, volume: float = 1.0) -> bool:
        """Play UI sound effect"""
        return self.play_sound(ui_id, AudioType.UI, volume)
    
    def play_voice(self, voice_id: str, volume: float = 1.0) -> bool:
        """Play voice audio"""
        return self.play_sound(voice_id, AudioType.VOICE, volume)
    
    def play_music(self, music_id: str, volume: float = 1.0, loop: bool = True) -> bool:
        """Play background music"""
        return self.play_sound(music_id, AudioType.MUSIC, volume, loop)
    
    def stop_music(self, fade_out: int = 1000) -> None:
        """Stop background music"""
        channel = self.channels[AudioType.MUSIC]
        channel.stop(fade_out)
    
    def set_master_volume(self, volume: float) -> None:
        """Set master volume"""
        self.config.audio.master_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()
    
    def set_type_volume(self, audio_type: AudioType, volume: float) -> None:
        """Set volume for specific audio type"""
        if audio_type == AudioType.AMBIENT:
            self.config.audio.ambient_volume = volume
        elif audio_type == AudioType.FOLEY:
            self.config.audio.sfx_volume = volume
        elif audio_type == AudioType.VOICE:
            self.config.audio.voice_volume = volume
        elif audio_type == AudioType.MUSIC:
            self.config.audio.music_volume = volume
        
        self._update_all_volumes()
    
    def _get_type_volume(self, audio_type: AudioType) -> float:
        """Get volume for specific audio type"""
        base_volume = self.config.audio.master_volume
        
        if audio_type == AudioType.AMBIENT:
            return base_volume * self.config.audio.ambient_volume
        elif audio_type == AudioType.FOLEY:
            return base_volume * self.config.audio.sfx_volume
        elif audio_type == AudioType.VOICE:
            return base_volume * self.config.audio.voice_volume
        elif audio_type == AudioType.MUSIC:
            return base_volume * self.config.audio.music_volume
        elif audio_type == AudioType.UI:
            return base_volume * self.config.audio.sfx_volume
        
        return base_volume
    
    def _update_all_volumes(self) -> None:
        """Update volumes for all channels"""
        for audio_type, channel in self.channels.items():
            channel.set_volume(self._get_type_volume(audio_type))
    
    def _fade_in_ambient(self, fade_time: int) -> None:
        """Fade in ambient sound"""
        def fade_in_thread():
            channel = self.channels[AudioType.AMBIENT]
            steps = fade_time // 50  # 50ms steps
            volume_step = self._get_type_volume(AudioType.AMBIENT) / steps
            
            for i in range(steps):
                if not channel.is_playing():
                    break
                channel.set_volume(volume_step * (i + 1))
                time.sleep(0.05)
        
        threading.Thread(target=fade_in_thread, daemon=True).start()
    
    def pause_all(self) -> None:
        """Pause all audio"""
        pygame.mixer.pause()
    
    def unpause_all(self) -> None:
        """Unpause all audio"""
        pygame.mixer.unpause()
    
    def stop_all(self) -> None:
        """Stop all audio"""
        for channel in self.channels.values():
            channel.stop()
    
    def get_loaded_sounds(self) -> List[str]:
        """Get list of loaded sound IDs"""
        return list(self.sounds.keys())
    
    def cleanup(self) -> None:
        """Cleanup audio resources"""
        self.stop_all()
        pygame.mixer.quit()

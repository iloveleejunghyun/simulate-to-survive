#!/usr/bin/env python3
"""
Audio Generator for Simulate to Survive
Generates basic audio files for the game
"""

import os
import numpy as np
from pathlib import Path
import wave
import struct

def create_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a sine wave"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def generate_white_noise(duration, sample_rate=44100, amplitude=0.1):
    """Generate white noise"""
    samples = int(sample_rate * duration)
    noise = amplitude * np.random.normal(0, 1, samples)
    return noise

def generate_rain_sound(duration, sample_rate=44100):
    """Generate rain sound effect"""
    # Base rain sound (low frequency noise)
    base_rain = generate_white_noise(duration, sample_rate, 0.05)
    
    # Add some variation
    for i in range(5):
        drop_freq = np.random.uniform(200, 800)
        drop_duration = np.random.uniform(0.1, 0.3)
        drop_start = np.random.uniform(0, duration - drop_duration)
        
        drop = generate_sine_wave(drop_freq, drop_duration, sample_rate, 0.02)
        start_sample = int(drop_start * sample_rate)
        end_sample = start_sample + len(drop)
        
        if end_sample <= len(base_rain):
            base_rain[start_sample:end_sample] += drop
    
    return base_rain

def generate_ambient_music(duration, sample_rate=44100):
    """Generate ambient background music"""
    # Create a simple ambient loop
    base_freq = 220  # A3
    harmonics = [1, 2, 3, 5, 8]  # Harmonic series
    
    music = np.zeros(int(sample_rate * duration))
    
    for i, harmonic in enumerate(harmonics):
        freq = base_freq * harmonic
        amplitude = 0.1 / harmonic  # Decreasing amplitude for higher harmonics
        wave = generate_sine_wave(freq, duration, sample_rate, amplitude)
        music += wave
    
    # Add some slow modulation
    t = np.linspace(0, duration, len(music))
    modulation = 0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t)  # Slow modulation
    music *= modulation
    
    return music

def generate_ui_sound(frequency=800, duration=0.1, sample_rate=44100):
    """Generate UI click sound"""
    wave = generate_sine_wave(frequency, duration, sample_rate, 0.2)
    # Add fade out
    fade_samples = int(0.05 * sample_rate)
    fade_out = np.linspace(1, 0, fade_samples)
    wave[-fade_samples:] *= fade_out
    return wave

def save_wav_file(filename, audio_data, sample_rate=44100):
    """Save audio data as WAV file"""
    # Ensure audio data is in the correct range
    audio_data = np.clip(audio_data, -1, 1)
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(str(filename), 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def main():
    """Generate all required audio files"""
    print("开始生成音频文件...")
    
    # Create audio directories
    base_path = Path("assets/audio")
    create_directory(base_path / "sfx" / "environment")
    create_directory(base_path / "sfx" / "ui")
    create_directory(base_path / "music" / "background")
    create_directory(base_path / "music" / "ambient")
    
    # Generate environment sounds
    print("生成环境音效...")
    
    # Gentle rain
    gentle_rain = generate_rain_sound(10.0)  # 10 seconds
    save_wav_file(base_path / "sfx" / "environment" / "gentle-rain.wav", gentle_rain)
    print("✓ gentle-rain.wav")
    
    # Heavy rain
    heavy_rain = generate_rain_sound(10.0)
    heavy_rain *= 1.5  # Make it louder
    save_wav_file(base_path / "sfx" / "environment" / "heavy-rain.wav", heavy_rain)
    print("✓ heavy-rain.wav")
    
    # Generate UI sounds
    print("生成UI音效...")
    
    # Click sound
    click_sound = generate_ui_sound(800, 0.1)
    save_wav_file(base_path / "sfx" / "ui" / "click.wav", click_sound)
    print("✓ click.wav")
    
    # Hover sound
    hover_sound = generate_ui_sound(600, 0.05)
    save_wav_file(base_path / "sfx" / "ui" / "hover.wav", hover_sound)
    print("✓ hover.wav")
    
    # Generate music
    print("生成背景音乐...")
    
    # Main theme
    main_theme = generate_ambient_music(30.0)  # 30 seconds loop
    save_wav_file(base_path / "music" / "background" / "main_theme.wav", main_theme)
    print("✓ main_theme.wav")
    
    # Ambient music
    ambient_music = generate_ambient_music(20.0)
    ambient_music *= 0.7  # Quieter ambient
    save_wav_file(base_path / "music" / "ambient" / "forest_ambient.wav", ambient_music)
    print("✓ forest_ambient.wav")
    
    print("\n音频文件生成完成！")
    print(f"生成的文件位置: {base_path.absolute()}")

if __name__ == "__main__":
    main()

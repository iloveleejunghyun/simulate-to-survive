#!/usr/bin/env python3
"""
Debug script to check audio manager
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from simulate_to_survive.core.config import Config
from simulate_to_survive.core.audio_manager import AudioManager, AudioType

def main():
    print("🔍 调试音频管理器...")
    
    config = Config()
    audio_manager = AudioManager(config)
    
    print("\n📋 已加载的音频文件:")
    for sound_id in audio_manager.sounds.keys():
        print(f"   ✓ {sound_id}")
    
    print(f"\n📊 总共加载了 {len(audio_manager.sounds)} 个音频文件")
    
    # Test specific sound
    test_sound = "environment_gentle-rain"
    if test_sound in audio_manager.sounds:
        print(f"✅ {test_sound} 已加载")
    else:
        print(f"❌ {test_sound} 未找到")
        print("可用的环境音频:")
        for sound_id in audio_manager.sounds.keys():
            if sound_id.startswith("environment_"):
                print(f"   - {sound_id}")
    
    print("\n🎵 音频通道:")
    for audio_type, channel in audio_manager.channels.items():
        print(f"   {audio_type.value}: 通道 {channel.channel_id}")
    
    # Test playing sound
    print(f"\n🎵 测试播放 {test_sound}:")
    success = audio_manager.play_sound(test_sound, AudioType.AMBIENT, volume=0.5)
    if success:
        print("✅ 播放成功")
    else:
        print("❌ 播放失败")

if __name__ == "__main__":
    main()

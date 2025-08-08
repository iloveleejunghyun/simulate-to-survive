#!/usr/bin/env python3
"""
Quick test script for Simulate to Survive
Tests basic functionality without manual waiting
"""

import sys
import os
import time
import threading
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import pygame
from simulate_to_survive.core.config import Config
from simulate_to_survive.core.game import Game

def test_game_initialization():
    """Test if game can be initialized"""
    print("🧪 测试游戏初始化...")
    
    try:
        config = Config()
        game = Game(config)
        print("✅ 游戏初始化成功")
        return game
    except Exception as e:
        print(f"❌ 游戏初始化失败: {e}")
        return None

def test_scene_loading(game):
    """Test scene loading"""
    print("🧪 测试场景加载...")
    
    try:
        # Test loading different scenes
        scenes_to_test = ["main_menu", "CH0_PHASE_01", "CH1_PHASE_01"]
        
        for scene_id in scenes_to_test:
            game.scene_manager.load_scene(scene_id)
            current_scene = game.scene_manager.current_scene
            if current_scene and current_scene.scene_id == scene_id:
                print(f"✅ 场景 {scene_id} 加载成功")
            else:
                print(f"❌ 场景 {scene_id} 加载失败")
                
    except Exception as e:
        print(f"❌ 场景加载测试失败: {e}")

def test_audio_system(game):
    """Test audio system"""
    print("🧪 测试音频系统...")
    
    try:
        # Test playing different audio types
        audio_tests = [
            ("environment_gentle-rain", "ambient"),
            ("ui_click", "sfx"),
            ("main_theme", "music")
        ]
        
        for audio_id, audio_type in audio_tests:
            success = game.audio_manager.play_sound(audio_id, audio_type)
            if success:
                print(f"✅ 音频 {audio_id} 播放成功")
            else:
                print(f"⚠️ 音频 {audio_id} 播放失败")
                
    except Exception as e:
        print(f"❌ 音频系统测试失败: {e}")

def test_emotion_system(game):
    """Test emotion system"""
    print("🧪 测试情感系统...")
    
    try:
        # Test emotion updates
        initial_emotions = game.get_emotion_summary()
        print(f"初始情感状态: {initial_emotions}")
        
        # Update emotions
        game.update_emotion("happiness", 10)
        game.update_emotion("sadness", -5)
        
        updated_emotions = game.get_emotion_summary()
        print(f"更新后情感状态: {updated_emotions}")
        
        print("✅ 情感系统测试成功")
        
    except Exception as e:
        print(f"❌ 情感系统测试失败: {e}")

def test_game_loop(game, duration=1):
    """Test game loop for a short duration"""
    print(f"🧪 测试游戏主循环 ({duration}秒)...")
    
    try:
        # Test a few frames without threading (avoid macOS SDL issues)
        for i in range(60):  # 60 frames at 60fps = 1 second
            game._handle_events()
            game._update()
            game._render()
            game.clock.tick(60)
        print("✅ 游戏主循环测试成功")
    except Exception as e:
        print(f"❌ 游戏主循环测试失败: {e}")

def test_save_load(game):
    """Test save/load functionality"""
    print("🧪 测试存档系统...")
    
    try:
        # Test save
        game.save_game()
        print("✅ 存档功能测试成功")
        
        # Test load
        game.load_game()
        print("✅ 读档功能测试成功")
        
    except Exception as e:
        print(f"❌ 存档系统测试失败: {e}")

def main():
    """Run all tests"""
    print("🎮 开始测试 Simulate to Survive")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    
    # Test game initialization
    game = test_game_initialization()
    if not game:
        print("❌ 游戏初始化失败，停止测试")
        return
    
    print()
    
    # Test individual systems
    test_scene_loading(game)
    print()
    
    test_audio_system(game)
    print()
    
    test_emotion_system(game)
    print()
    
    test_save_load(game)
    print()
    
    # Test game loop
    test_game_loop(game, 2)  # 2 seconds
    print()
    
    # Cleanup
    try:
        pygame.quit()
    except:
        pass
    
    print("=" * 50)
    print("🎉 测试完成！")
    print("\n如果所有测试都通过，游戏应该可以正常运行。")
    print("你可以运行 'python src/simulate_to_survive/main.py' 来启动完整游戏。")

if __name__ == "__main__":
    main()

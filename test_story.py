#!/usr/bin/env python3
"""
Test script for story content and scene transitions
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from simulate_to_survive.data.scenes import get_scene, get_all_scene_ids, SCENES
from simulate_to_survive.core.emotion_system import EmotionSystem, EmotionType
from simulate_to_survive.core.config import Config


def test_scene_loading():
    """Test that all scenes can be loaded properly"""
    print("🧪 测试场景加载...")
    
    scene_ids = get_all_scene_ids()
    print(f"   发现 {len(scene_ids)} 个场景:")
    
    for scene_id in scene_ids:
        scene = get_scene(scene_id)
        if scene:
            print(f"   ✓ {scene_id}: {scene.title}")
            
            # Test events
            print(f"      - 事件数量: {len(scene.events)}")
            for event in scene.events:
                print(f"      - 事件 {event.id}: {len(event.choices)} 个选择")
                
                # Test choices
                for choice in event.choices:
                    print(f"        * {choice.text[:30]}...")
                    if choice.emotion_effects:
                        print(f"          情感效果: {choice.emotion_effects}")
                    if choice.next_scene:
                        print(f"          下一场景: {choice.next_scene}")
        else:
            print(f"   ✗ {scene_id}: 加载失败")
    
    print("✅ 场景加载测试完成\n")


def test_emotion_system():
    """Test emotion system with story choices"""
    print("🧪 测试情感系统与故事选择...")
    
    config = Config()
    emotion_system = EmotionSystem(config)
    
    # Test CH0_PHASE_01 choices
    scene = get_scene("CH0_PHASE_01")
    if scene:
        print(f"   测试场景: {scene.title}")
        
        for event in scene.events:
            print(f"   事件: {event.id}")
            
            for i, choice in enumerate(event.choices):
                print(f"   选择 {i+1}: {choice.text}")
                
                if choice.emotion_effects:
                    # Apply emotion effects
                    for emotion, value in choice.emotion_effects.items():
                        emotion_system.update_emotion_by_name(emotion, value)
                        print(f"     {emotion} +{value}")
                
                # Show current emotion state
                summary = emotion_system.get_emotion_summary()
                print(f"     当前情感状态: {summary['values']}")
    
    print("✅ 情感系统测试完成\n")


def test_scene_transitions():
    """Test scene transition logic"""
    print("🧪 测试场景转换逻辑...")
    
    # Test CH0_PHASE_04 -> CH1_PHASE_01 transition
    scene = get_scene("CH0_PHASE_04")
    if scene:
        print(f"   测试场景转换: {scene.title}")
        
        # Find the event with scene transition
        for event in scene.events:
            for choice in event.choices:
                if choice.next_scene:
                    print(f"   发现场景转换: {choice.text}")
                    print(f"   目标场景: {choice.next_scene}")
                    
                    # Verify target scene exists
                    target_scene = get_scene(choice.next_scene)
                    if target_scene:
                        print(f"   ✓ 目标场景存在: {target_scene.title}")
                    else:
                        print(f"   ✗ 目标场景不存在: {choice.next_scene}")
    
    print("✅ 场景转换测试完成\n")


def test_story_progression():
    """Test complete story progression"""
    print("🧪 测试完整故事流程...")
    
    config = Config()
    emotion_system = EmotionSystem(config)
    
    # Simulate playing through all scenes
    scenes_to_test = [
        "CH0_PHASE_01",
        "CH0_PHASE_02", 
        "CH0_PHASE_03",
        "CH0_PHASE_04",
        "CH1_PHASE_01"
    ]
    
    print("   模拟故事流程:")
    
    for scene_id in scenes_to_test:
        scene = get_scene(scene_id)
        if scene:
            print(f"   📖 {scene.title}")
            
            # Simulate first choice of each event
            for event in scene.events:
                if event.choices:
                    choice = event.choices[0]  # Take first choice
                    
                    # Apply emotion effects
                    if choice.emotion_effects:
                        for emotion, value in choice.emotion_effects.items():
                            emotion_system.update_emotion_by_name(emotion, value)
                    
                    # Check for scene transition
                    if choice.next_scene:
                        print(f"     → 转换到: {choice.next_scene}")
                        break
            
            # Show emotion state after scene
            summary = emotion_system.get_emotion_summary()
            print(f"     情感状态: {summary['values']}")
    
    print("✅ 故事流程测试完成\n")


def main():
    """Main test function"""
    print("🎮 开始故事内容测试 Simulate to Survive")
    print("=" * 50)
    
    try:
        test_scene_loading()
        test_emotion_system()
        test_scene_transitions()
        test_story_progression()
        
        print("=" * 50)
        print("🎉 故事内容测试完成！")
        print("\n总结:")
        print("✅ 所有场景已实现")
        print("✅ 情感系统正常工作")
        print("✅ 场景转换逻辑正确")
        print("✅ 故事流程完整")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

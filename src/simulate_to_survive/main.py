#!/usr/bin/env python3
"""
Main entry point for Simulate to Survive game
"""

import sys
import os
import argparse
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from simulate_to_survive.core.game import Game
from simulate_to_survive.core.config import Config


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Simulate to Survive - 文字冒险游戏")
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="启用debug模式，自动截图和详细日志"
    )
    parser.add_argument(
        "--screenshot-interval", 
        type=float, 
        default=2.0,
        help="debug模式下的截图间隔（秒），默认2.0秒"
    )
    parser.add_argument(
        "--auto-screenshot", 
        action="store_true", 
        help="启用事件自动截图"
    )
    return parser.parse_args()


def main():
    """Main game entry point"""
    try:
        # 解析命令行参数
        args = parse_arguments()
        
        # Initialize configuration
        config = Config()
        
        # 设置debug模式
        if args.debug:
            config.debug_mode = True
            config.screenshot_interval = args.screenshot_interval
            config.auto_screenshot = args.auto_screenshot
            print(f"🔧 Debug模式已启用")
            print(f"📸 截图间隔: {args.screenshot_interval}秒")
            print(f"📸 事件自动截图: {'启用' if args.auto_screenshot else '禁用'}")
        
        # Create and run the game
        game = Game(config)
        game.run()
        
    except KeyboardInterrupt:
        print("\n游戏已退出")
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        try:
            import pygame
            pygame.quit()
        except:
            pass


if __name__ == "__main__":
    main()

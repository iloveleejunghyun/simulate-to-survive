#!/usr/bin/env python3
"""
Main entry point for Simulate to Survive game
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from simulate_to_survive.core.game import Game
from simulate_to_survive.core.config import Config


def main():
    """Main game entry point"""
    try:
        # Initialize configuration
        config = Config()
        
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
            pygame.quit()
        except:
            pass


if __name__ == "__main__":
    main()

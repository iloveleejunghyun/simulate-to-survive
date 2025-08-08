"""
Main game class for Simulate to Survive
Coordinates all systems and manages the game loop
"""

import pygame
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from .config import Config
from .emotion_system import EmotionSystem, EmotionType
from .audio_manager import AudioManager, AudioType
from .scene_manager import SceneManager


class Game:
    """Main game class"""
    
    def __init__(self, config: Config):
        self.config = config
        self.running = False
        self.clock = pygame.time.Clock()
        
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Simulate to Survive")
        
        # Create display
        self.screen = pygame.display.set_mode(
            (config.display.window_width, config.display.window_height),
            pygame.FULLSCREEN if config.display.fullscreen else 0
        )
        
        # Initialize systems
        self.emotion_system = EmotionSystem(config)
        self.audio_manager = AudioManager(config)
        self.scene_manager = SceneManager(config, self)
        
        # Game state
        self.current_scene = "CH0_PHASE_01"  # Start with first phase of chapter 0
        self.game_data = {}
        
        print("游戏初始化完成")
    
    def run(self) -> None:
        """Main game loop"""
        self.running = True
        
        # Load initial scene (this will also set up ambient sound)
        self.scene_manager.load_scene(self.current_scene)
        
        print("开始游戏循环")
        
        while self.running:
            # Handle events
            self._handle_events()
            
            # Update game state
            self._update()
            
            # Render
            self._render()
            
            # Cap frame rate
            self.clock.tick(self.config.display.fps)
        
        self._cleanup()
    
    def _handle_events(self) -> None:
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)
            
            # Pass events to current scene
            self.scene_manager.handle_event(event)
    
    def _handle_keydown(self, event) -> None:
        """Handle key press events"""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_F11:
            self._toggle_fullscreen()
        elif event.key == pygame.K_F1:
            self._show_debug_info()
    
    def _handle_mouse_click(self, event) -> None:
        """Handle mouse click events"""
        # Pass to scene manager for UI handling
        self.scene_manager.handle_mouse_click(event.pos)
    
    def _update(self) -> None:
        """Update game state"""
        # Update current scene
        self.scene_manager.update()
        
        # Update emotion system
        self._update_emotions()
        
        # Check for scene transitions
        self._check_scene_transitions()
    
    def _render(self) -> None:
        """Render current frame"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Render current scene
        self.scene_manager.render(self.screen)
        
        # Render UI overlays
        self._render_ui_overlays()
        
        # Update display
        pygame.display.flip()
    
    def _update_emotions(self) -> None:
        """Update emotion values with time decay"""
        # This is handled automatically by the emotion system
        # when update_emotion() is called
        pass
    
    def _check_scene_transitions(self) -> None:
        """Check if scene should transition"""
        next_scene = self.scene_manager.get_next_scene()
        if next_scene and next_scene != self.current_scene:
            self._transition_to_scene(next_scene)
    
    def _transition_to_scene(self, scene_id: str) -> None:
        """Transition to a new scene"""
        print(f"场景转换: {self.current_scene} -> {scene_id}")
        
        # Save current scene state
        self.scene_manager.save_scene_state()
        
        # Update current scene
        self.current_scene = scene_id
        
        # Load new scene
        self.scene_manager.load_scene(scene_id)
        
        # Update ambient sound based on scene
        self._update_ambient_sound(scene_id)
    
    def _update_ambient_sound(self, scene_id: str) -> None:
        """Update ambient sound based on scene"""
        ambient_map = {
            "CH0_PHASE_01": "environment_gentle_rain",  # 细雨声
            "CH0_PHASE_02": "environment_gentle_rain",  # 细雨声
            "CH0_PHASE_03": "environment_gentle_rain",  # 细雨声
            "CH0_PHASE_04": "environment_heavy_rain",   # 暴雨声
            "CH1_PHASE_01": "ui_system",                # 系统音效
        }
        
        ambient_id = ambient_map.get(scene_id)
        if ambient_id:
            self.audio_manager.play_ambient(ambient_id, fade_in=1000)
    
    def _render_ui_overlays(self) -> None:
        """Render UI overlays (emotion bars, etc.)"""
        # Render emotion bars
        self._render_emotion_bars()
        
        # Render debug info if enabled
        if hasattr(self, 'debug_mode') and self.debug_mode:
            self._render_debug_info()
    
    def _render_emotion_bars(self) -> None:
        """Render emotion value bars"""
        emotion_summary = self.emotion_system.get_emotion_summary()
        values = emotion_summary['values']
        
        # Render emotion bars at top of screen
        bar_height = 20
        bar_width = 200
        bar_spacing = 10
        start_x = 10
        start_y = 10
        
        for i, (emotion_name, value) in enumerate(values.items()):
            x = start_x
            y = start_y + i * (bar_height + bar_spacing)
            
            # Background bar
            pygame.draw.rect(self.screen, (50, 50, 50), 
                           (x, y, bar_width, bar_height))
            
            # Value bar
            percentage = value / 100.0
            fill_width = int(bar_width * percentage)
            color = self._get_emotion_color(emotion_name, percentage)
            pygame.draw.rect(self.screen, color, 
                           (x, y, fill_width, bar_height))
            
            # Border
            pygame.draw.rect(self.screen, (200, 200, 200), 
                           (x, y, bar_width, bar_height), 1)
            
            # Text
            font = pygame.font.Font(None, 16)
            text = font.render(f"{emotion_name}: {value}", True, (255, 255, 255))
            self.screen.blit(text, (x + bar_width + 10, y + 2))
    
    def _get_emotion_color(self, emotion_name: str, percentage: float) -> tuple:
        """Get color for emotion bar based on value"""
        if emotion_name == "执念":
            return (255, 100, 100)  # Red
        elif emotion_name == "愤怒":
            return (255, 150, 0)    # Orange
        elif emotion_name == "压抑":
            return (100, 100, 255)  # Blue
        elif emotion_name == "情感":
            return (255, 100, 255)  # Pink
        elif emotion_name == "决心":
            return (100, 255, 100)  # Green
        else:
            return (200, 200, 200)  # Gray
    
    def _render_debug_info(self) -> None:
        """Render debug information"""
        font = pygame.font.Font(None, 20)
        debug_info = [
            f"FPS: {self.clock.get_fps():.1f}",
            f"Scene: {self.current_scene}",
            f"Loaded Sounds: {len(self.audio_manager.get_loaded_sounds())}",
        ]
        
        for i, info in enumerate(debug_info):
            text = font.render(info, True, (255, 255, 255))
            self.screen.blit(text, (10, self.config.display.window_height - 60 + i * 20))
    
    def _toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode"""
        self.config.display.fullscreen = not self.config.display.fullscreen
        pygame.display.set_mode(
            (self.config.display.window_width, self.config.display.window_height),
            pygame.FULLSCREEN if self.config.display.fullscreen else 0
        )
    
    def _show_debug_info(self) -> None:
        """Toggle debug mode"""
        if not hasattr(self, 'debug_mode'):
            self.debug_mode = False
        self.debug_mode = not self.debug_mode
        print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
    
    def update_emotion(self, emotion_type: EmotionType, delta: int) -> None:
        """Update emotion value"""
        self.emotion_system.update_emotion(emotion_type, delta)
    
    def update_emotion_by_name(self, emotion_name: str, delta: int) -> None:
        """Update emotion value by Chinese name"""
        self.emotion_system.update_emotion_by_name(emotion_name, delta)
    
    def play_sound(self, sound_id: str, audio_type: AudioType, volume: float = 1.0) -> bool:
        """Play sound effect"""
        return self.audio_manager.play_sound(sound_id, audio_type, volume)
    
    def get_emotion_summary(self) -> Dict[str, Any]:
        """Get emotion system summary"""
        return self.emotion_system.get_emotion_summary()
    
    def save_game(self) -> None:
        """Save game state"""
        save_data = {
            'current_scene': self.current_scene,
            'game_data': self.game_data,
            'emotions': self.emotion_system.save_emotions(),
            'scene_state': self.scene_manager.get_scene_state()
        }
        
        save_path = self.config.get_save_path()
        save_path.mkdir(exist_ok=True)
        
        import json
        with open(save_path / "save_game.json", 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print("游戏已保存")
    
    def load_game(self) -> None:
        """Load game state"""
        save_file = self.config.get_save_path() / "save_game.json"
        if not save_file.exists():
            print("没有找到存档文件")
            return
        
        import json
        with open(save_file, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        self.current_scene = save_data.get('current_scene', self.current_scene)
        self.game_data = save_data.get('game_data', {})
        self.emotion_system.load_emotions(save_data.get('emotions', {}))
        self.scene_manager.set_scene_state(save_data.get('scene_state', {}))
        
        # Load the saved scene
        self.scene_manager.load_scene(self.current_scene)
        
        print("游戏已加载")
    
    def _cleanup(self) -> None:
        """Cleanup resources"""
        print("清理游戏资源...")
        self.audio_manager.cleanup()
        pygame.quit()
        print("游戏已退出")

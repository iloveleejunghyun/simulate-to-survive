"""
Scene Manager for Simulate to Survive
Manages game scenes, transitions, and scene-specific logic
"""

import pygame
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod

from .config import Config


class Scene(ABC):
    """Abstract base class for all game scenes"""
    
    def __init__(self, config: Config, game):
        self.config = config
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        # Scene state
        self.is_active = False
        self.next_scene = None
        self.scene_data = {}
        
        # UI elements
        self.ui_elements = []
        self.buttons = []
        
        # Text rendering
        self.text_speed = 30  # characters per second
        self.current_text = ""
        self.full_text = ""
        self.text_progress = 0
        self.text_complete = False
        
    def activate(self):
        """Called when scene becomes active"""
        self.is_active = True
        self.on_activate()
    
    def deactivate(self):
        """Called when scene becomes inactive"""
        self.is_active = False
        self.on_deactivate()
    
    @abstractmethod
    def on_activate(self):
        """Override to handle scene activation"""
        pass
    
    @abstractmethod
    def on_deactivate(self):
        """Override to handle scene deactivation"""
        pass
    
    @abstractmethod
    def update(self):
        """Update scene logic"""
        pass
    
    @abstractmethod
    def render(self, screen):
        """Render scene"""
        pass
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos)
    
    def handle_keydown(self, event):
        """Handle key press events"""
        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
            self.advance_text()
    
    def handle_mouse_click(self, pos):
        """Handle mouse click events"""
        # Check button clicks
        for button in self.buttons:
            if button.collidepoint(pos):
                self.on_button_click(button)
    
    def advance_text(self):
        """Advance text display (for typewriter effect)"""
        if not self.text_complete:
            self.text_complete = True
            self.current_text = self.full_text
        else:
            # Text is complete, move to next
            self.on_text_complete()
    
    def set_text(self, text: str):
        """Set text for typewriter effect"""
        self.full_text = text
        self.current_text = ""
        self.text_progress = 0
        self.text_complete = False
    
    def update_text(self, dt):
        """Update text animation"""
        if not self.text_complete and self.text_progress < len(self.full_text):
            chars_to_add = int(self.text_speed * dt / 1000)
            self.text_progress = min(self.text_progress + chars_to_add, len(self.full_text))
            self.current_text = self.full_text[:self.text_progress]
            if self.text_progress >= len(self.full_text):
                self.text_complete = True
    
    def on_text_complete(self):
        """Called when text display is complete"""
        pass
    
    def on_button_click(self, button):
        """Called when a button is clicked"""
        pass
    
    def transition_to(self, scene_id: str):
        """Request transition to another scene"""
        self.next_scene = scene_id


class MainMenuScene(Scene):
    """Main menu scene"""
    
    def __init__(self, config: Config, game):
        super().__init__(config, game)
        self.scene_id = "main_menu"  # Add scene_id
    
    def on_activate(self):
        self.set_text("模拟生存 - Simulate to Survive")
        # Start background music
        self.game.audio_manager.play_music("background_main_theme", loop=True)
    
    def on_deactivate(self):
        self.game.audio_manager.stop_music()
    
    def update(self):
        # Update text animation
        dt = self.game.clock.get_time()
        self.update_text(dt)
    
    def render(self, screen):
        # Clear screen
        screen.fill((20, 20, 40))
        
        # Render title
        if self.current_text:
            title_surface = self.large_font.render(self.current_text, True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(self.config.display.window_width // 2, 200))
            screen.blit(title_surface, title_rect)
        
        # Render menu options
        if self.text_complete:
            options = ["开始游戏", "设置", "退出"]
            for i, option in enumerate(options):
                color = (200, 200, 200) if i == 0 else (150, 150, 150)
                option_surface = self.font.render(option, True, color)
                option_rect = option_surface.get_rect(
                    center=(self.config.display.window_width // 2, 350 + i * 50)
                )
                screen.blit(option_surface, option_rect)
    
    def handle_keydown(self, event):
        super().handle_keydown(event)
        if self.text_complete:
            if event.key == pygame.K_1 or event.key == pygame.K_RETURN:
                self.transition_to("CH0_PHASE_01")
            elif event.key == pygame.K_2:
                self.transition_to("settings")
            elif event.key == pygame.K_3 or event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


class GameScene(Scene):
    """Base class for game play scenes"""
    
    def __init__(self, config: Config, game, scene_id: str):
        super().__init__(config, game)
        self.scene_id = scene_id
        self.background_color = (30, 30, 50)
        
        # Scene data
        self.scene_data = None
        self.current_event_index = 0
        self.current_event = None
        
    def on_activate(self):
        # Load scene-specific data
        self.load_scene_data()
        
    def on_deactivate(self):
        # Save scene state
        self.save_scene_state()
    
    def load_scene_data(self):
        """Load scene-specific data from files"""
        try:
            from simulate_to_survive.data.scenes import get_scene
            self.scene_data = get_scene(self.scene_id)
            
            if self.scene_data and self.scene_data.events:
                self.current_event_index = 0
                self.current_event = self.scene_data.events[0]
                self.set_text(self.current_event.text)
            else:
                # Fallback data
                self.scene_data = {
                    "text": "这是一个游戏场景...",
                    "choices": ["选择1", "选择2", "选择3"],
                    "background": "forest"
                }
                self.set_text(self.scene_data["text"])
                
        except ImportError:
            # Fallback if scene data not available
            self.scene_data = {
                "text": "这是一个游戏场景...",
                "choices": ["选择1", "选择2", "选择3"],
                "background": "forest"
            }
            self.set_text(self.scene_data["text"])
    
    def save_scene_state(self):
        """Save current scene state"""
        pass
    
    def update(self):
        dt = self.game.clock.get_time()
        self.update_text(dt)
    
    def render(self, screen):
        # Clear screen
        screen.fill(self.background_color)
        
        # Render scene title
        if self.scene_data:
            title_font = pygame.font.Font(None, 36)
            title_surface = title_font.render(self.scene_data.title, True, (255, 255, 255))
            title_rect = title_surface.get_rect(
                center=(self.config.display.window_width // 2, 50)
            )
            screen.blit(title_surface, title_rect)
        
        # Render text with fade-in effect
        if self.current_text:
            # Split text into lines for better display
            lines = self.wrap_text(self.current_text, 70)
            
            # Calculate text position
            text_start_y = 150
            line_height = 35
            
            for i, line in enumerate(lines):
                # Apply fade-in effect based on text progress
                alpha = min(255, int(255 * (self.text_progress / len(self.current_text)) * 2))
                if alpha > 0:
                    text_surface = self.font.render(line, True, (255, 255, 255))
                    text_surface.set_alpha(alpha)
                    text_rect = text_surface.get_rect(
                        center=(self.config.display.window_width // 2, text_start_y + i * line_height)
                    )
                    screen.blit(text_surface, text_rect)
        
        # Render progress indicator
        if self.scene_data and self.scene_data.events:
            progress_text = f"事件 {self.current_event_index + 1} / {len(self.scene_data.events)}"
            progress_font = pygame.font.Font(None, 20)
            progress_surface = progress_font.render(progress_text, True, (150, 150, 150))
            progress_rect = progress_surface.get_rect(
                bottomright=(self.config.display.window_width - 20, self.config.display.window_height - 20)
            )
            screen.blit(progress_surface, progress_rect)
        
        # Render choices if text is complete
        if self.text_complete and self.current_event and self.current_event.choices:
            choice_start_y = 400
            choice_height = 60
            
            for i, choice in enumerate(self.current_event.choices):
                # Check if mouse is hovering over choice
                mouse_pos = pygame.mouse.get_pos()
                choice_rect = pygame.Rect(
                    self.config.display.window_width // 2 - 300,
                    choice_start_y + i * choice_height,
                    600,
                    50
                )
                
                # Choose color based on hover state
                if choice_rect.collidepoint(mouse_pos):
                    bg_color = (100, 100, 150)
                    text_color = (255, 255, 255)
                    border_color = (200, 200, 255)
                else:
                    bg_color = (50, 50, 80)
                    text_color = (200, 200, 200)
                    border_color = (100, 100, 150)
                
                # Draw choice background with rounded corners effect
                pygame.draw.rect(screen, bg_color, choice_rect)
                pygame.draw.rect(screen, border_color, choice_rect, 2)
                
                # Draw choice text
                choice_surface = self.font.render(f"{i+1}. {choice.text}", True, text_color)
                choice_text_rect = choice_surface.get_rect(
                    center=choice_rect.center
                )
                screen.blit(choice_surface, choice_text_rect)
        
        # Render instruction text
        if self.text_complete and self.current_event and self.current_event.choices:
            instruction_text = "点击选择或按数字键 1-3"
            instruction_font = pygame.font.Font(None, 18)
            instruction_surface = instruction_font.render(instruction_text, True, (100, 100, 100))
            instruction_rect = instruction_surface.get_rect(
                center=(self.config.display.window_width // 2, self.config.display.window_height - 50)
            )
            screen.blit(instruction_surface, instruction_rect)
    
    def wrap_text(self, text: str, max_width: int) -> List[str]:
        """Wrap text to fit screen width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def on_text_complete(self):
        """Handle text completion"""
        pass
    
    def handle_keydown(self, event):
        super().handle_keydown(event)
        if self.text_complete and self.current_event and self.current_event.choices:
            if event.key == pygame.K_1:
                self.on_choice_selected(0)
            elif event.key == pygame.K_2:
                self.on_choice_selected(1)
            elif event.key == pygame.K_3:
                self.on_choice_selected(2)
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks for choice selection"""
        super().handle_mouse_click(pos)
        
        # Handle choice selection with mouse
        if self.text_complete and self.current_event and self.current_event.choices:
            choice_start_y = 400
            choice_height = 60
            
            for i, choice in enumerate(self.current_event.choices):
                choice_rect = pygame.Rect(
                    self.config.display.window_width // 2 - 300,
                    choice_start_y + i * choice_height,
                    600,
                    50
                )
                
                if choice_rect.collidepoint(pos):
                    self.on_choice_selected(i)
                    break
    
    def on_choice_selected(self, choice_index: int):
        """Handle choice selection"""
        if not self.current_event or choice_index >= len(self.current_event.choices):
            return
            
        choice = self.current_event.choices[choice_index]
        print(f"选择: {choice.text}")
        
        # Apply emotion effects
        if choice.emotion_effects:
            for emotion, value in choice.emotion_effects.items():
                self.game.update_emotion_by_name(emotion, value)
                print(f"情感值更新: {emotion} +{value}")
        
        # Check for scene transition
        if choice.next_scene:
            print(f"场景转换: {self.scene_id} -> {choice.next_scene}")
            self.transition_to(choice.next_scene)
        else:
            # Move to next event in same scene
            self.move_to_next_event()
    
    def move_to_next_event(self):
        """Move to next event in the scene"""
        if not self.scene_data or not self.scene_data.events:
            return
            
        self.current_event_index += 1
        
        if self.current_event_index < len(self.scene_data.events):
            # Move to next event in same scene
            self.current_event = self.scene_data.events[self.current_event_index]
            self.set_text(self.current_event.text)
            print(f"进入事件: {self.current_event.id}")
        else:
            # Scene completed, move to next scene
            print("场景完成，准备进入下一场景")
            # For now, just restart the scene
            self.current_event_index = 0
            self.current_event = self.scene_data.events[0]
            self.set_text(self.current_event.text)


class SceneManager:
    """Manages all game scenes and transitions"""
    
    def __init__(self, config: Config, game):
        self.config = config
        self.game = game
        
        # Scene registry
        self.scenes = {}
        self.current_scene = None
        self.scene_states = {}
        
        # Initialize scenes
        self._initialize_scenes()
    
    def _initialize_scenes(self):
        """Initialize all game scenes"""
        # Main menu
        self.scenes["main_menu"] = MainMenuScene(self.config, self.game)
        
        # Game scenes - Chapter 0
        self.scenes["CH0_PHASE_01"] = GameScene(self.config, self.game, "CH0_PHASE_01")
        self.scenes["CH0_PHASE_02"] = GameScene(self.config, self.game, "CH0_PHASE_02")
        self.scenes["CH0_PHASE_03"] = GameScene(self.config, self.game, "CH0_PHASE_03")
        self.scenes["CH0_PHASE_04"] = GameScene(self.config, self.game, "CH0_PHASE_04")
        
        # Game scenes - Chapter 1
        self.scenes["CH1_PHASE_01"] = GameScene(self.config, self.game, "CH1_PHASE_01")
        
        # Settings scene (placeholder)
        self.scenes["settings"] = MainMenuScene(self.config, self.game)  # Temporary
    
    def load_scene(self, scene_id: str):
        """Load and activate a scene"""
        if scene_id not in self.scenes:
            print(f"Warning: Scene '{scene_id}' not found, using main menu")
            scene_id = "main_menu"
        
        # Deactivate current scene
        if self.current_scene:
            self.current_scene.deactivate()
        
        # Activate new scene
        self.current_scene = self.scenes[scene_id]
        self.current_scene.activate()
        
        print(f"Loaded scene: {scene_id}")
    
    def update(self):
        """Update current scene"""
        if self.current_scene:
            self.current_scene.update()
            
            # Check for scene transitions
            if self.current_scene.next_scene:
                next_scene = self.current_scene.next_scene
                self.current_scene.next_scene = None
                self.load_scene(next_scene)
    
    def render(self, screen):
        """Render current scene"""
        if self.current_scene:
            self.current_scene.render(screen)
    
    def handle_event(self, event):
        """Handle events for current scene"""
        if self.current_scene:
            self.current_scene.handle_event(event)
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks for current scene"""
        if self.current_scene:
            self.current_scene.handle_mouse_click(pos)
    
    def get_next_scene(self) -> Optional[str]:
        """Get the next scene ID if a transition is requested"""
        if self.current_scene and self.current_scene.next_scene:
            return self.current_scene.next_scene
        return None
    
    def save_scene_state(self):
        """Save current scene state"""
        if self.current_scene:
            self.scene_states[self.current_scene.scene_id] = self.current_scene.scene_data
    
    def get_scene_state(self) -> Dict[str, Any]:
        """Get all scene states"""
        return self.scene_states.copy()
    
    def set_scene_state(self, states: Dict[str, Any]):
        """Set scene states from saved data"""
        self.scene_states = states.copy()

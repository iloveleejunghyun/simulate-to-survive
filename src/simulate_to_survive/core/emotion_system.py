"""
Emotion system for Simulate to Survive
Manages five emotion values and their effects on gameplay
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import time


class EmotionType(Enum):
    """Emotion types"""
    OBSESSION = "执念"      # 执念值
    ANGER = "愤怒"          # 愤怒值
    DEPRESSION = "压抑"     # 压抑值
    AFFECTION = "情感"      # 情感值
    DETERMINATION = "决心"  # 决心值


@dataclass
class EmotionValue:
    """Individual emotion value with metadata"""
    value: int = 0
    max_value: int = 100
    min_value: int = 0
    decay_rate: float = 0.1  # per minute
    last_update: float = field(default_factory=time.time)
    
    def update(self, delta: int, current_time: float = None) -> None:
        """Update emotion value with decay"""
        if current_time is None:
            current_time = time.time()
        
        # Apply decay
        time_diff = (current_time - self.last_update) / 60.0  # minutes
        decay_amount = self.decay_rate * time_diff
        
        # Update value
        self.value = max(self.min_value, min(self.max_value, self.value + delta - decay_amount))
        self.last_update = current_time
    
    def set_value(self, value: int) -> None:
        """Set emotion value directly"""
        self.value = max(self.min_value, min(self.max_value, value))
        self.last_update = time.time()
    
    def get_percentage(self) -> float:
        """Get emotion value as percentage"""
        return (self.value - self.min_value) / (self.max_value - self.min_value)


class EmotionSystem:
    """Main emotion system class"""
    
    def __init__(self, config):
        self.config = config
        self.emotions: Dict[EmotionType, EmotionValue] = {}
        self.emotion_history: List[Dict[str, Any]] = []
        
        # Initialize all emotion values
        for emotion_type in EmotionType:
            self.emotions[emotion_type] = EmotionValue(
                decay_rate=config.game.emotion_decay_rate
            )
    
    def update_emotion(self, emotion_type: EmotionType, delta: int) -> None:
        """Update specific emotion value"""
        if emotion_type in self.emotions:
            current_time = time.time()
            old_value = self.emotions[emotion_type].value
            self.emotions[emotion_type].update(delta, current_time)
            new_value = self.emotions[emotion_type].value
            
            # Record change in history
            self.emotion_history.append({
                'emotion': emotion_type.value,
                'old_value': old_value,
                'new_value': new_value,
                'delta': delta,
                'timestamp': current_time
            })
    
    def set_emotion(self, emotion_type: EmotionType, value: int) -> None:
        """Set emotion value directly"""
        if emotion_type in self.emotions:
            old_value = self.emotions[emotion_type].value
            self.emotions[emotion_type].set_value(value)
            
            # Record change in history
            self.emotion_history.append({
                'emotion': emotion_type.value,
                'old_value': old_value,
                'new_value': value,
                'delta': value - old_value,
                'timestamp': time.time()
            })
    
    def get_emotion(self, emotion_type: EmotionType) -> int:
        """Get current emotion value"""
        return self.emotions.get(emotion_type, EmotionValue()).value
    
    def get_emotion_percentage(self, emotion_type: EmotionType) -> float:
        """Get emotion value as percentage"""
        return self.emotions.get(emotion_type, EmotionValue()).get_percentage()
    
    def get_all_emotions(self) -> Dict[str, int]:
        """Get all emotion values as dictionary"""
        return {emotion.value: self.get_emotion(emotion) for emotion in EmotionType}
    
    def get_emotion_summary(self) -> Dict[str, Any]:
        """Get comprehensive emotion summary"""
        summary = {
            'values': self.get_all_emotions(),
            'percentages': {emotion.value: self.get_emotion_percentage(emotion) 
                          for emotion in EmotionType},
            'total_value': sum(self.get_emotion(emotion) for emotion in EmotionType),
            'dominant_emotion': self.get_dominant_emotion(),
            'emotion_stability': self.get_emotion_stability()
        }
        return summary
    
    def get_dominant_emotion(self) -> Optional[str]:
        """Get the emotion with the highest value"""
        if not self.emotions:
            return None
        
        dominant = max(self.emotions.items(), key=lambda x: x[1].value)
        return dominant[0].value if dominant[1].value > 0 else None
    
    def get_emotion_stability(self) -> float:
        """Calculate emotion stability (0-1, higher = more stable)"""
        if not self.emotion_history:
            return 1.0
        
        # Calculate variance of recent emotion changes
        recent_changes = [entry['delta'] for entry in self.emotion_history[-10:]]
        if not recent_changes:
            return 1.0
        
        mean_change = sum(recent_changes) / len(recent_changes)
        variance = sum((change - mean_change) ** 2 for change in recent_changes) / len(recent_changes)
        
        # Convert to stability score (0-1)
        stability = max(0.0, 1.0 - (variance / 100.0))
        return stability
    
    def check_emotion_threshold(self, emotion_type: EmotionType, threshold: int) -> bool:
        """Check if emotion value meets threshold"""
        return self.get_emotion(emotion_type) >= threshold
    
    def get_emotion_effects(self) -> Dict[str, Any]:
        """Get effects of current emotion values on gameplay"""
        effects = {
            'system_activation': self.check_emotion_threshold(EmotionType.OBSESSION, 80),
            'combat_bonus': self.get_emotion_percentage(EmotionType.ANGER) * 0.2,
            'recovery_penalty': self.get_emotion_percentage(EmotionType.DEPRESSION) * 0.3,
            'relationship_bonus': self.get_emotion_percentage(EmotionType.AFFECTION) * 0.15,
            'growth_bonus': self.get_emotion_percentage(EmotionType.DETERMINATION) * 0.25
        }
        return effects
    
    def reset_emotions(self) -> None:
        """Reset all emotion values to 0"""
        for emotion in self.emotions.values():
            emotion.set_value(0)
    
    def save_emotions(self) -> Dict[str, Any]:
        """Save emotion state for persistence"""
        return {
            'emotions': {emotion.value: {
                'value': emotion_data.value,
                'last_update': emotion_data.last_update
            } for emotion, emotion_data in self.emotions.items()},
            'history': self.emotion_history[-100:]  # Keep last 100 entries
        }
    
    def load_emotions(self, data: Dict[str, Any]) -> None:
        """Load emotion state from saved data"""
        if 'emotions' in data:
            for emotion_name, emotion_data in data['emotions'].items():
                for emotion_type in EmotionType:
                    if emotion_type.value == emotion_name:
                        self.emotions[emotion_type].value = emotion_data['value']
                        self.emotions[emotion_type].last_update = emotion_data['last_update']
                        break
        
        if 'history' in data:
            self.emotion_history = data['history']

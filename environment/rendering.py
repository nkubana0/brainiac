"""
Pygame Visualization for Adaptive E-Learning AAC Platform

This module provides a graphical user interface using Pygame to visualize:
1. AAC communication panel with symbol buttons
2. Lesson content display
3. Student performance metrics
4. Agent's adaptation decisions
5. Accessibility features (large buttons, high contrast)
"""

import pygame
import numpy as np
from typing import Optional, Tuple, Dict, Any
import sys


class ELearningVisualizer:
    """
    Pygame-based visualization for the adaptive e-learning environment
    """
    
    # Color scheme (high contrast for accessibility)
    COLORS = {
        'background': (30, 30, 40),
        'panel': (50, 50, 60),
        'button': (70, 130, 180),
        'button_hover': (100, 160, 210),
        'button_active': (50, 200, 100),
        'text': (255, 255, 255),
        'text_secondary': (200, 200, 200),
        'accent': (255, 165, 0),
        'success': (76, 175, 80),
        'warning': (255, 193, 7),
        'error': (244, 67, 54),
        'engagement_high': (76, 175, 80),
        'engagement_med': (255, 193, 7),
        'engagement_low': (244, 67, 54)
    }
    
    def __init__(self, width: int = 1200, height: int = 800):
        """Initialize the visualizer"""
        pygame.init()
        pygame.font.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Adaptive E-Learning & AAC Platform")
        
        # Fonts (large for accessibility)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
        self.font_tiny = pygame.font.Font(None, 20)
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.fps = 4
        
        # AAC Symbols
        self.aac_symbols = [
            "I want", "Help", "Yes", 
            "No", "More", "Stop"
        ]
        
        # Button positions (will be dynamically adjusted)
        self.button_positions = self._initialize_button_positions()
        
        # Animation state
        self.frame_count = 0
        self.last_action = None
        self.action_display_timer = 0
        
    def _initialize_button_positions(self) -> list:
        """Initialize AAC button positions"""
        positions = []
        button_width = 180
        button_height = 120
        margin = 20
        start_x = 50
        start_y = 500
        
        for i in range(6):
            row = i // 3
            col = i % 3
            x = start_x + col * (button_width + margin)
            y = start_y + row * (button_height + margin)
            positions.append((x, y, button_width, button_height))
        
        return positions
    
    def render(
        self, 
        env_state: Dict[str, Any], 
        action: Optional[int] = None,
        reward: Optional[float] = None,
        episode: Optional[int] = None,
        total_reward: Optional[float] = None
    ):
        """
        Render the current state of the environment
        
        Args:
            env_state: Dictionary with environment state information
            action: Last action taken by agent
            reward: Last reward received
            episode: Current episode number
            total_reward: Cumulative reward for episode
        """
        self.screen.fill(self.COLORS['background'])
        
        # Update action display
        if action is not None:
            self.last_action = action
            self.action_display_timer = 2 * self.fps  # Display for 2 seconds
        
        if self.action_display_timer > 0:
            self.action_display_timer -= 1
        
        # Draw main panels
        self._draw_lesson_panel(env_state)
        self._draw_aac_panel(env_state)
        self._draw_metrics_panel(env_state, reward, total_reward)
        self._draw_agent_info_panel(self.last_action if self.action_display_timer > 0 else None, episode)
        
        # Draw header
        self._draw_header()
        
        # Update display
        pygame.display.flip()
        self.clock.tick(self.fps)
        self.frame_count += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return False
        
        return True
    
    def _draw_header(self):
        """Draw the header with title"""
        header_rect = pygame.Rect(0, 0, self.width, 80)
        pygame.draw.rect(self.screen, self.COLORS['panel'], header_rect)
        
        # Title
        title = self.font_large.render(
            "Adaptive E-Learning & AAC Platform", True, self.COLORS['accent']
        )
        title_rect = title.get_rect(center=(self.width // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_small.render(
            "For Children with Physical Disabilities", True, self.COLORS['text_secondary']
        )
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 60))
        self.screen.blit(subtitle, subtitle_rect)
    
    def _draw_lesson_panel(self, env_state: Dict[str, Any]):
        """Draw the lesson content panel"""
        panel_rect = pygame.Rect(50, 100, 600, 350)
        pygame.draw.rect(self.screen, self.COLORS['panel'], panel_rect, border_radius=10)
        
        # Panel title
        title = self.font_medium.render("Current Lesson", True, self.COLORS['accent'])
        self.screen.blit(title, (70, 120))
        
        # Difficulty indicator
        difficulty = env_state.get('lesson_difficulty', 0.5)
        diff_text = "Easy" if difficulty < 0.4 else "Medium" if difficulty < 0.7 else "Hard"
        diff_color = self.COLORS['success'] if 0.4 <= difficulty <= 0.7 else self.COLORS['warning']
        
        difficulty_label = self.font_small.render(
            f"Difficulty: {diff_text} ({difficulty:.2f})", True, diff_color
        )
        self.screen.blit(difficulty_label, (70, 160))
        
        # Lesson content (simulated)
        lesson_items = [
            "Topic: Colors and Shapes",
            "Activity: Match the shape",
            "Progress: 60% Complete"
        ]
        
        y_offset = 200
        for item in lesson_items:
            text = self.font_small.render(item, True, self.COLORS['text'])
            self.screen.blit(text, (90, y_offset))
            y_offset += 40
        
        # Hint indicator
        hints = env_state.get('hints_requested', 0)
        hint_text = self.font_small.render(
            f"Hints Used: {hints}", True, self.COLORS['text_secondary']
        )
        self.screen.blit(hint_text, (70, 380))
        
        # Time on lesson
        time_lesson = env_state.get('time_on_lesson', 0)
        time_text = self.font_small.render(
            f"Time: {time_lesson} steps", True, self.COLORS['text_secondary']
        )
        self.screen.blit(time_text, (350, 380))
    
    def _draw_aac_panel(self, env_state: Dict[str, Any]):
        """Draw the AAC communication panel"""
        panel_rect = pygame.Rect(50, 470, 600, 280)
        pygame.draw.rect(self.screen, self.COLORS['panel'], panel_rect, border_radius=10)
        
        # Panel title
        title = self.font_medium.render("AAC Communication", True, self.COLORS['accent'])
        self.screen.blit(title, (70, 485))
        
        # AAC buttons
        button_usage = env_state.get('aac_button_usage', np.array([0.17] * 6))
        
        for i, (symbol, usage) in enumerate(zip(self.aac_symbols, button_usage)):
            x, y, w, h = self.button_positions[i]
            
            # Adjust button appearance based on usage frequency
            # More frequently used buttons are highlighted
            if usage > 0.25:
                button_color = self.COLORS['button_active']
            elif usage > 0.15:
                button_color = self.COLORS['button_hover']
            else:
                button_color = self.COLORS['button']
            
            # Draw button
            button_rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=8)
            pygame.draw.rect(self.screen, self.COLORS['text'], button_rect, 2, border_radius=8)
            
            # Draw symbol text
            symbol_text = self.font_medium.render(symbol, True, self.COLORS['text'])
            text_rect = symbol_text.get_rect(center=(x + w//2, y + h//2 - 10))
            self.screen.blit(symbol_text, text_rect)
            
            # Draw usage percentage
            usage_text = self.font_tiny.render(
                f"{usage*100:.1f}%", True, self.COLORS['text_secondary']
            )
            usage_rect = usage_text.get_rect(center=(x + w//2, y + h - 20))
            self.screen.blit(usage_text, usage_rect)
    
    def _draw_metrics_panel(
        self, 
        env_state: Dict[str, Any],
        reward: Optional[float],
        total_reward: Optional[float]
    ):
        """Draw performance metrics panel"""
        panel_rect = pygame.Rect(680, 100, 470, 350)
        pygame.draw.rect(self.screen, self.COLORS['panel'], panel_rect, border_radius=10)
        
        # Panel title
        title = self.font_medium.render("Performance Metrics", True, self.COLORS['accent'])
        self.screen.blit(title, (700, 120))
        
        # Student accuracy
        accuracy = env_state.get('student_accuracy', 0.7)
        self._draw_metric_bar(
            "Student Accuracy", accuracy, 700, 170, 
            400, 30, self.COLORS['success']
        )
        
        # Engagement level
        engagement = env_state.get('engagement_level', 0.8)
        engagement_color = (
            self.COLORS['engagement_high'] if engagement > 0.7
            else self.COLORS['engagement_med'] if engagement > 0.4
            else self.COLORS['engagement_low']
        )
        self._draw_metric_bar(
            "Engagement", engagement, 700, 220,
            400, 30, engagement_color
        )
        
        # Interface efficiency
        interface_eff = env_state.get('interface_efficiency', 0.5)
        self._draw_metric_bar(
            "Interface Efficiency", interface_eff, 700, 270,
            400, 30, self.COLORS['button']
        )
        
        # Reward information
        if reward is not None:
            reward_text = self.font_small.render(
                f"Last Reward: {reward:+.1f}", True, 
                self.COLORS['success'] if reward > 0 else self.COLORS['error']
            )
            self.screen.blit(reward_text, (700, 330))
        
        if total_reward is not None:
            total_text = self.font_small.render(
                f"Episode Reward: {total_reward:.1f}", True, self.COLORS['text']
            )
            self.screen.blit(total_text, (700, 370))
        
        # Current step
        step = env_state.get('step', 0)
        step_text = self.font_small.render(
            f"Step: {step}/200", True, self.COLORS['text_secondary']
        )
        self.screen.blit(step_text, (700, 410))
    
    def _draw_agent_info_panel(
        self, 
        action: Optional[int],
        episode: Optional[int]
    ):
        """Draw agent action information panel"""
        panel_rect = pygame.Rect(680, 470, 470, 280)
        pygame.draw.rect(self.screen, self.COLORS['panel'], panel_rect, border_radius=10)
        
        # Panel title
        title = self.font_medium.render("Agent Actions", True, self.COLORS['accent'])
        self.screen.blit(title, (700, 485))
        
        # Episode number
        if episode is not None:
            ep_text = self.font_small.render(
                f"Episode: {episode}", True, self.COLORS['text_secondary']
            )
            self.screen.blit(ep_text, (700, 530))
        
        # Action descriptions
        action_names = [
            "Keep current layout",
            "Optimize AAC buttons",
            "Increase difficulty",
            "Decrease difficulty",
            "Provide hint",
            "Predict next word",
            "Adjust button sizes"
        ]
        
        if action is not None and 0 <= action < len(action_names):
            # Highlight current action
            action_rect = pygame.Rect(700, 570, 420, 80)
            pygame.draw.rect(self.screen, self.COLORS['button'], action_rect, border_radius=5)
            
            action_label = self.font_small.render("Current Action:", True, self.COLORS['accent'])
            self.screen.blit(action_label, (720, 585))
            
            action_text = self.font_medium.render(
                action_names[action], True, self.COLORS['text']
            )
            text_rect = action_text.get_rect(center=(910, 620))
            self.screen.blit(action_text, text_rect)
        else:
            # Show all possible actions
            info_text = self.font_small.render(
                "Waiting for agent action...", True, self.COLORS['text_secondary']
            )
            self.screen.blit(info_text, (720, 585))
        
        # Controls hint
        controls_text = self.font_tiny.render(
            "Press ESC or Q to quit", True, self.COLORS['text_secondary']
        )
        self.screen.blit(controls_text, (700, 710))
    
    def _draw_metric_bar(
        self, 
        label: str, 
        value: float, 
        x: int, 
        y: int, 
        width: int, 
        height: int,
        color: Tuple[int, int, int]
    ):
        """Draw a horizontal metric bar"""
        # Label
        label_text = self.font_small.render(label, True, self.COLORS['text'])
        self.screen.blit(label_text, (x, y - 25))
        
        # Background bar
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (60, 60, 70), bg_rect, border_radius=5)
        
        # Filled bar
        filled_width = int(width * value)
        filled_rect = pygame.Rect(x, y, filled_width, height)
        pygame.draw.rect(self.screen, color, filled_rect, border_radius=5)
        
        # Border
        pygame.draw.rect(self.screen, self.COLORS['text'], bg_rect, 2, border_radius=5)
        
        # Value text
        value_text = self.font_small.render(f"{value*100:.1f}%", True, self.COLORS['text'])
        value_rect = value_text.get_rect(center=(x + width + 40, y + height // 2))
        self.screen.blit(value_text, value_rect)
    
    def close(self):
        """Clean up and close the visualizer"""
        pygame.quit()


# Test the visualizer
if __name__ == "__main__":
    print("Testing E-Learning Visualizer...")
    
    visualizer = ELearningVisualizer()
    
    # Simulate some environment states
    test_states = [
        {
            'lesson_difficulty': 0.5,
            'student_accuracy': 0.7,
            'engagement_level': 0.8,
            'hints_requested': 2,
            'time_on_lesson': 15,
            'interface_efficiency': 0.6,
            'aac_button_usage': np.array([0.25, 0.15, 0.20, 0.10, 0.20, 0.10]),
            'step': 15
        },
        {
            'lesson_difficulty': 0.6,
            'student_accuracy': 0.75,
            'engagement_level': 0.85,
            'hints_requested': 2,
            'time_on_lesson': 20,
            'interface_efficiency': 0.7,
            'aac_button_usage': np.array([0.30, 0.15, 0.15, 0.10, 0.20, 0.10]),
            'step': 20
        }
    ]
    
    episode = 1
    total_reward = 0
    
    for i, state in enumerate(test_states):
        action = i % 7
        reward = np.random.uniform(-5, 10)
        total_reward += reward
        
        running = visualizer.render(
            state, action, reward, episode, total_reward
        )
        
        if not running:
            break
        
        pygame.time.wait(2000)  # Wait 2 seconds
    
    visualizer.close()
    print("Visualizer test completed!")
"""
Class TransitionText: A graphical component for displaying scrolling text.
"""
import pyxel
from ui.primitives import draw_large_text # Import the revised function

class TransitionText:
    """Manages the animation of horizontally scrolling text that pauses in the middle."""
    def __init__(self, y_pos, speed=40, screen_width=256, pause_duration=10):
        self.y = y_pos
        self.speed = speed
        self.screen_width = screen_width
        self.pause_duration = pause_duration
        
        self.text = ""
        self.x = 0
        self.is_active = False
        self.state = 'inactive'
        self.center_x = 0
        self.pause_timer = 0

    def start(self, text):
        """
        Begins the transition with the given text.
        """
        self.text = text
        # Adjust width calculation for the new "blocky" text.
        # Each character is effectively (FONT_WIDTH + 1) wide.
        text_width = len(text) * (pyxel.FONT_WIDTH) + 1
        self.center_x = (self.screen_width - text_width) / 2
        self.x = self.screen_width
        self.state = 'entering'
        self.is_active = True

    def update(self):
        """Updates the position and state of the text."""
        if self.state == 'inactive':
            return

        if self.state == 'entering':
            self.x -= self.speed
            if self.x <= self.center_x:
                self.x = self.center_x
                self.state = 'paused'
                self.pause_timer = self.pause_duration
        
        elif self.state == 'paused':
            self.pause_timer -= 1
            if self.pause_timer <= 0:
                self.state = 'exiting'
        
        elif self.state == 'exiting':
            self.x -= self.speed
            text_width = len(self.text) * (pyxel.FONT_WIDTH) + 1
            if self.x < -text_width:
                self.state = 'inactive'
                self.is_active = False

    def draw(self):
        """Draws the large text to the screen if the transition is active."""
        if not self.is_active:
            return
        
        # Use the new function to draw the shadow and the text
        draw_large_text(self.x + 1, self.y + 1, self.text, 0)
        draw_large_text(self.x, self.y, self.text, 7)
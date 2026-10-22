"""
Class MainMenu: Title screen with the animated "chaos" logo
"""
import pyxel
from ui.primitives import drawGameLogo
from ui.button import Button


class MainMenu:
    """Title screen. Pyxel must already be initialized (see DuelGUI)."""
    def __init__(self):
        self.started = False
        self.button = Button(
            rect=(106, 180, 44, 10),
            color=0,
            colorBorder=7,
            colorText=7,
            text="Start Game",
            func=self.start
        )

    def start(self):
        """Called when the "Start Game" button is clicked."""
        self.started = True

    def run(self):
        """Shows the title screen until the player clicks "Start Game"."""
        self.started = False
        while not self.started:
            self.update()
            self.draw()
            pyxel.flip()
        # Swallow the click so it doesn't also land on the board.
        pyxel.flip()

    def update(self):
        self.button.update()

    def draw(self):
        pyxel.cls(0)
        drawGameLogo(65, 10, 16)
        self.button.draw()
        pyxel.text(70, 240, "Esc: quit at any time", 5)

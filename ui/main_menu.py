import pyxel
from ui.primitives import drawGameLogo
from ui.button import Button


class MainMenu:
    def __init__(self):
        pyxel.init(256, 256, fps=60)
        pyxel.mouse(True)
        self.button = Button(
            rect=(110, 180, 44, 10),
            color=0,
            colorBorder=7,
            colorText=7,
            text="Start Game",
            func=lambda: print("Button Click")
        )
        pyxel.run(self.update, self.draw)

    def update(self):
        self.button.update()

    def draw(self):
        pyxel.cls(0)
        drawGameLogo(70, 10, 16)
        self.button.draw()

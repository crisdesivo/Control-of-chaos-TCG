import pyxel
from ui.primitives import inRect


class Button:
    def __init__(self,
                 rect=(),
                 color=0,
                 colorBorder=7,
                 colorText=7,
                 text="",
                 func=lambda: None):
        self.rect = rect
        self.text = text
        self.function = func
        self.color = color
        self.colorBorder = colorBorder
        self.colorText = colorText

    def update(self):
        if (inRect(self.rect, pyxel.mouse_x, pyxel.mouse_y)
                and pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)):
            self.function()

    def draw(self):
        pyxel.rect(*self.rect, self.color)
        pyxel.rectb(*self.rect, self.colorBorder)
        pyxel.text(self.rect[0] + 2,
                   self.rect[1] + 2,
                   self.text,
                   self.colorText)

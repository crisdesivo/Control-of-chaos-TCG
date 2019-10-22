"""
Class Button: A button that activates a given function when clicked
"""
import pyxel
from ui.primitives import mouseInRect


class Button:
    def __init__(self,
                 rect=(),
                 color=0,
                 colorBorder=7,
                 colorBorderActive=11,
                 colorText=7,
                 text="",
                 func=lambda: None):
        """A button that activates a given function when clicked

        Keyword arguments:
        rect -- Rectangle coordinates that defines the range of the button
        color -- Filling color
        colorBorder -- Color of the border if mouse is not inside the button
        colorBorderActive -- Color of the border if mouse is inside the button
        text -- Texto to be displayed inside the button
        func -- Function that is activated when the mouse is clicked
        """
        self.rect = rect
        self.text = text
        self.function = func
        self.color = color
        self.colorBorder = colorBorder
        self.colorBorderActive = colorBorderActive
        self.colorText = colorText

    def update(self):
        """
        Check if a click occurs inside the button and activates function
        """
        if (mouseInRect(self.rect)
                and pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)):
            self.function()

    def draw(self):
        """
        Draws the button
        """
        pyxel.rect(*self.rect, self.color)
        if mouseInRect(self.rect):
            pyxel.rectb(*self.rect, self.colorBorderActive)
        else:
            pyxel.rectb(*self.rect, self.colorBorder)
        pyxel.text(self.rect[0] + 2,
                   self.rect[1] + 2,
                   self.text,
                   self.colorText)

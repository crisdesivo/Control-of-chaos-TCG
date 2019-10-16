import pyxel
from ui.constants import CARD_DRAW_HEiGHT, CARD_DRAW_WIDTH
from ui.primitives import centeredRect, drawCard


class CardDisplay:
    card = None
    playable = False
    usable = False
    opened = False

    def draw(self):
        if self.card is not None:
            rect = centeredRect(
                int(pyxel.width/2),
                int(pyxel.height/2),
                128,
                156)
            leftSidePosition = rect[0]
            topSidePosition = rect[1]
            width = rect[2]
            height = rect[3]
            pyxel.rect(
                leftSidePosition,
                topSidePosition,
                width,
                height,
                0)
            drawCard(
                self.card,
                int(pyxel.width/2-CARD_DRAW_WIDTH/2),
                int(pyxel.height/2-CARD_DRAW_HEiGHT/2))

    def open(self, card=None, playable=False, usable=False):
        self.card = card
        self.playable = playable
        self.usable = usable
        self.opened = True

    def rectangle(self):
        return centeredRect(
                int(pyxel.width/2),
                int(pyxel.height/2),
                128,
                156)

    def mouseInside(self):
        rect = self.rectangle()
        x = pyxel.mouse_x
        y = pyxel.mouse_y
        mouseXInside = x > rect[0] and x < rect[0] + rect[2]
        mouseYInside = y > rect[1] and y < rect[1] + rect[3]
        return mouseXInside and mouseYInside

    def update(self):
        if not self.mouseInside and pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON):
            self.close()

    def close(self):
        self.opened = False

import pyxel
import time
from ui.constants import CARD_DRAW_HEIGHT, CARD_DRAW_WIDTH
from ui.primitives import centeredRect, drawCard, updateWrapper
from ui.button import Button


class CardDisplay:
    def __init__(self, parent):
        self.parent = parent
        self.card = None
        self.playable = False
        self.usable = False

        self.frozen = True
        self.hidden = True
        self.freeze = False
        self.hide = False
        self.unfreeze = False
        self.unhide = False

    def draw(self):
        if self.card is not None and not self.hidden:
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
                leftSidePosition,
                topSidePosition)
            self.drawDescription()
            self.drawTechniques()

            if self.playable:
                self.playButton.draw()

    def drawDescription(self):
        rect = self.rectangle()
        pyxel.text(
            rect[0],
            rect[1] + CARD_DRAW_HEIGHT,
            self.card.description,
            7)

    def drawTechniques(self):
        rect = self.rectangle()
        if self.playable:
            yStart = rect[1] + CARD_DRAW_HEIGHT + 10 + 20
        else:
            yStart = rect[1] + CARD_DRAW_HEIGHT + 10

        for i, technique in enumerate(self.card.techniques):
            y = yStart + i*20
            pyxel.rectb(rect[0], y, rect[2], 20, 7)
            pyxel.text(rect[0] + 2, y + 2, technique.name, 7)
            pyxel.text(rect[0] + 2, y + 10, technique.description, 7)

    def open(self, card=None, playable=False, usable=False):
        print("open")
        self.card = card
        self.playable = playable
        self.usable = usable
        self.frozen = False
        self.hidden = False
        rect = self.rectangle()

        if self.playable:
            self.playButton = Button(
                rect=(rect[0],
                      rect[1] + CARD_DRAW_HEIGHT + 10,
                      rect[2],
                      20
                      ),
                text="Play card",
                func=self.playCard
            )

    def playCard(self):
        self.close()
        print("Closed display")
        self.card.play(self.parent.duel)

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

    def mouseClick(self):
        return pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON, 0, 0)

    @updateWrapper
    def update(self):
        if self.playable:
            self.playButton.update()

        if not self.mouseInside() and self.mouseClick():
            self.close()

    def close(self):
        print("close")
        # print(self.parent.components.updateSet)
        self.frozen = True
        self.hidden = True
        # self.parent.update()
        # self.parent.draw()
        self.parent.unfreezeForeground()

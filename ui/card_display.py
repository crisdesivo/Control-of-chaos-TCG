import pyxel
import time
from ui.constants import CARD_DRAW_HEIGHT, CARD_DRAW_WIDTH
from ui.primitives import centeredRect, drawCard
from ui.button import Button


class CardDisplay:
    card = None
    playable = False
    usable = False

    def __init__(self, parent):
        self.parent = parent

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
                leftSidePosition,
                topSidePosition)
            self.drawDescription()

        if self.playable:
            self.playButton.draw()

    def drawDescription(self):
        rect = self.rectangle()
        pyxel.text(
            rect[0],
            rect[1] + CARD_DRAW_HEIGHT,
            self.card.description,
            7)

    def open(self, card=None, playable=False, usable=False):
        print("open")
        self.card = card
        self.playable = playable
        self.usable = usable
        self.opened = True
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
        self.card.play(self.parent.duel)
        self.close()

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

    def update(self):
        if self.playable:
            self.playButton.update()

        if not self.mouseInside() and self.mouseClick():
            self.close()

    def close(self):
        print("close")
        #print(self.parent.components.updateSet)
        self.parent.components.pause(self)
        self.parent.update()
        self.parent.draw()
        self.parent.components.resume(self.parent.handGUI)

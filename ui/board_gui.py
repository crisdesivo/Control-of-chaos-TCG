import pyxel
from ui.constants import CARD_DRAW_HEIGHT, CARD_DRAW_WIDTH
from ui.primitives import drawCard, updateWrapper


class BoardGUI:
    def __init__(self, parent):
        self.parent = parent
        self.board = parent.duel.board
        self.highlight = []

        self.frozen = False
        self.hidden = False
        self.freeze = False
        self.hide = False
        self.unfreeze = False
        self.unhide = False

        self.targetSelected = None
        self.findTarget = False

    @property
    def currrentPlayer(self):
        return self.parent.duel.turn.player

    def drawSlot(self, slot):
        x, y = self.slotPosition(slot)
        color = pyxel.frame_count % 16 if slot in self.highlight else 0
        pyxel.rectb(
            x - 1,
            y - 1,
            CARD_DRAW_WIDTH + 2,
            CARD_DRAW_HEIGHT + 2,
            color)

    def slotPosition(self, slot):
        if slot.player == self.currrentPlayer:
            return (3 + slot.location*(CARD_DRAW_WIDTH + 3),
                    197 - CARD_DRAW_HEIGHT)
        else:
            return (3 + slot.location*(CARD_DRAW_WIDTH + 3),
                    CARD_DRAW_HEIGHT/2 + 3)

    def mouseInSlot(self, slot):
        leftPosition, topPosition = self.slotPosition(slot)
        leftPosition -= 1
        topPosition -= 1
        rightPosition = leftPosition + CARD_DRAW_WIDTH + 2
        bottomPosition = topPosition + CARD_DRAW_HEIGHT + 2
        inXCoordinate = (pyxel.mouse_x > leftPosition
                         and pyxel.mouse_x < rightPosition)
        inYCoordinate = (pyxel.mouse_y > topPosition
                         and pyxel.mouse_y < bottomPosition)
        return inXCoordinate and inYCoordinate

    def drawUnits(self):
        for slot in self.board.units[self.currrentPlayer]:
            x, y = self.slotPosition(slot)
            self.drawSlot(slot)
            if slot.occupant is not None:
                drawCard(slot.occupant, x, y)

        for slot in self.board.units[1 - self.currrentPlayer]:
            x, y = self.slotPosition(slot)
            self.drawSlot(slot)
            if slot.occupant is not None:
                drawCard(slot.occupant, x, y)

    def draw(self):
        if not self.hidden:
            self.drawUnits()

    @updateWrapper
    def update(self):
        if self.mouseInside() and pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            for slots in self.board.units:
                for slot in slots:
                    if slot.occupant is not None:
                        if self.mouseInSlot(slot):
                            self.parent.checkBoardCard(slot.occupant)

    def updateSelection(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            for slot in self.highlight:
                if self.mouseInSlot(slot):
                    print(slot)
                    self.targetSelected = slot
                    break

    def mouseInside(self):
        return (pyxel.mouse_y > CARD_DRAW_HEIGHT/2
                and pyxel.mouse_y < 200)

    def selectTarget(self, possibleTargets):
        self.findTarget = True
        pyxel.flip()
        pyxel.flip()

        self.highlight = possibleTargets
        self.targetSelected = None
        while self.targetSelected is None:
            pyxel.cls(4)
            self.updateSelection()
            self.draw()
            pyxel.flip()
        self.highlight = []
        return self.targetSelected

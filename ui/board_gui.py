"""
Class BoardGUI: Draws and handles choices in the board on the user interface
"""
import pyxel
from ui.constants import CARD_DRAW_HEIGHT, CARD_DRAW_WIDTH
from ui.primitives import (drawCard,
                           updateWrapper,
                           mouseInRect,
                           drawEnergyAmount)


class BoardGUI:
    """Draws and handles choices in the board on the user interface
    """
    def __init__(self, parent):
        """
        Draws and handles choices in the board on the user interface
        
        Keyword arguments:
        parents -- Location of the board
        """
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

        self.divisionPosition = 100

    @property
    def currrentPlayer(self):
        """Returns current player integer"""
        return self.parent.duel.turn.player

    def drawSlot(self, slot):
        """Draws the slot in its position

        Keyword arguments:
        slot -- Slot to draw
        """
        x, y, w, h = self.slotRectangle(slot)
        color = pyxel.frame_count % 16 if slot in self.highlight else 0
        if mouseInRect((x-1, y-1, w, h)):
            color = 11
        pyxel.rectb(
            x - 1,
            y - 1,
            w,
            h,
            color)

    def slotRectangle(self, slot):
        """Returns the rectangle coordinates of the slot

        Keyword arguments:
        slot -- Slot object
        """
        if slot.location in range(5):
            startPosition = (pyxel.width - 5*(CARD_DRAW_WIDTH + 3))/2
            if slot.player == self.currrentPlayer:
                return (startPosition + slot.location*(CARD_DRAW_WIDTH + 3),
                        self.divisionPosition + 1,
                        CARD_DRAW_WIDTH + 2,
                        CARD_DRAW_HEIGHT + 2)
            else:
                return (startPosition + slot.location*(CARD_DRAW_WIDTH + 3),
                        self.divisionPosition - 1 - CARD_DRAW_HEIGHT,
                        CARD_DRAW_WIDTH + 2,
                        CARD_DRAW_HEIGHT + 2)
        elif slot.location == 5:
            x, y, w, h = self.informationRect()
            return (x + 1, y + 8, w/2, 8)

    def informationRect(self):
        """Returns the rectangle coordinates of the information section"""
        return (
            (pyxel.width - 5*(CARD_DRAW_WIDTH + 3))/2 - 1,
            self.divisionPosition + CARD_DRAW_HEIGHT + 3,
            (5*(CARD_DRAW_WIDTH + 3) - 1),
            200 - 1 - (self.divisionPosition + CARD_DRAW_HEIGHT + 3)
        )

    def nextTurnRect(self):
        """Returns the rectangle coordinates of the next turn section"""
        x, y, w, h = self.informationRect()
        return (x, y + 15, w/2, 8)

    def drawNextTurn(self):
        """Draws next turn section"""
        x, y, w, h = self.nextTurnRect()
        pyxel.rect(x, y, w, h, 7)
        if mouseInRect(self.nextTurnRect()):
            pyxel.rectb(x, y, w, h, 11)
        else:
            pyxel.rectb(x, y, w, h, 0)
        pyxel.text(x + 3, y + 1, "Next Turn", 0)

    def drawInformation(self):
        """Draws information section"""
        x, y, w, h = self.informationRect()
        pyxel.rect(x, y, w/2, h, 7)
        pyxel.rectb(x, y, w/2, h, 0)
        text = f"Cards in hand: {len(self.board.players[self.currrentPlayer].hand.cards)}"
        pyxel.text(x + 3, y + 2, text, 0)
        self.drawEnergyDeposit()
        self.drawNextTurn()

    def drawEnergyDeposit(self):
        """Draws the energies amounts in the energy deposit"""
        slot = self.board.energies[self.currrentPlayer]
        energyDeposit = slot.occupant
        rect = self.slotRectangle(slot)
        pyxel.rect(rect[0], rect[1], rect[2] - 1, rect[3], 0)
        pyxel.text(rect[0] + 1, rect[1] + 1, "Field Energies", 7)
        drawEnergyAmount(rect[0] + 62, rect[1], energyDeposit.energyCount)
        if slot in self.highlight:
            pyxel.rectb(rect[0],
                        rect[1],
                        rect[2] - 1,
                        rect[3] - 1,
                        pyxel.frame_count % 16)

        if mouseInRect(rect):
            pyxel.rectb(rect[0], rect[1], rect[2] - 1, rect[3] - 1, 11)

    def mouseInSlot(self, slot):
        """Returns True if the mouse cursor is inside the rectangle of the slot

        Keyword arguments:
        slot -- Slot
        """
        leftPosition, topPosition, width, height = self.slotRectangle(slot)
        leftPosition -= 2
        topPosition -= 1
        rightPosition = leftPosition + width
        bottomPosition = topPosition + height
        inXCoordinate = (pyxel.mouse_x > leftPosition
                         and pyxel.mouse_x < rightPosition)
        inYCoordinate = (pyxel.mouse_y > topPosition
                         and pyxel.mouse_y < bottomPosition)
        return inXCoordinate and inYCoordinate

    def drawUnits(self):
        """
        Draws the units in the board
        """
        for slot in self.board.units[self.currrentPlayer]:
            x, y, w, h = self.slotRectangle(slot)
            self.drawSlot(slot)

        for slot in self.board.units[1 - self.currrentPlayer]:
            x, y, w, h = self.slotRectangle(slot)
            self.drawSlot(slot)

        for slot in self.board.units[self.currrentPlayer]:
            x, y, w, h = self.slotRectangle(slot)
            if slot.occupant is not None:
                drawCard(slot.occupant, x, y, showEnergies=True)

        for slot in self.board.units[1 - self.currrentPlayer]:
            x, y, w, h = self.slotRectangle(slot)
            if slot.occupant is not None:
                drawCard(slot.occupant, x, y, showEnergies=True)

    def draw(self):
        """
        Draws the entire board
        """
        if not self.hidden:
            self.drawUnits()
            self.drawInformation()

    @updateWrapper
    def update(self):
        """
        Updates the board
        """
        if self.mouseInside() and pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            slots = self.board.units[self.currrentPlayer]
            for slot in slots:
                if slot.occupant is not None:
                    if self.mouseInSlot(slot):
                        self.parent.checkBoardCard(slot.occupant, True)
            slots = self.board.units[1-self.currrentPlayer]
            for slot in slots:
                if slot.occupant is not None:
                    if self.mouseInSlot(slot):
                        self.parent.checkBoardCard(slot.occupant, False)
            if mouseInRect(self.nextTurnRect()):
                self.parent.endTurn = True

    def updateSelection(self):
        """
        Handles mouse click on the board
        """
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            for slot in self.highlight:
                if self.mouseInSlot(slot):
                    self.targetSelected = slot
                    break

    def mouseInside(self):
        """
        Returns True if the mouse cursor is inside the board
        """
        return (pyxel.mouse_y > CARD_DRAW_HEIGHT/2
                and pyxel.mouse_y < 200)

    def selectTarget(self, possibleTargets):
        """
        Highlights the possible targets to let the user choose one

        Keyword arguments:
        possibleTargets -- List of available targets to choose
        """
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

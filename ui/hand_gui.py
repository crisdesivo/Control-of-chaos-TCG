"""
Class HandGUI: Draws and handles choices in the hand on the user interface
"""

import pyxel
from ui.constants import CARD_DRAW_HEIGHT, CARD_DRAW_WIDTH
from ui.primitives import drawCard, updateWrapper
import time


class HandGUI:
    """Draws and handles choices in the hand on the user interface
    """
    def __init__(self, hand):
        """Draws and handles choices in the hand on the user interface

        Keyword arguments:
        hand -- Hand object
        """
        self.hand = hand
        self.topIndex = 0
        self.checkCard = None
        self.hide = False
        self.freeze = False
        self.unfreeze = False
        self.unhide = False
        self.frozen = False
        self.hidden = False

    def initGUI(self):
        """Initializes the hand gui"""
        self.hand.GUI = self

    def draw(self):
        """Draws the hand"""
        if not self.hidden:
            cards = self.hand.cards
            if len(cards) > 0:
                separation = self.cardSeparation()
                startingPosition = (
                    pyxel.width
                    - CARD_DRAW_WIDTH
                    - (len(cards)-1)*separation
                )/2
                enumeratedCards = list(enumerate(cards))
                if separation < int(CARD_DRAW_WIDTH)+1:
                    behindCards = enumeratedCards[self.topIndex+1:]
                    onTopCards = enumeratedCards[:self.topIndex+1]

                    behindCards.reverse()
                    for i, card in behindCards:
                        drawCard(card, startingPosition+i*separation, 200)

                    for i, card in onTopCards[:-1]:
                        drawCard(card, startingPosition+i*separation, 200)

                    if self.mouseInside():
                        i, card = onTopCards[-1]
                        drawCard(card, startingPosition+i*separation, 205)
                    else:
                        i, card = onTopCards[-1]
                        drawCard(card, startingPosition+i*separation, 200)
                else:
                    for i, card in enumeratedCards:
                        if i != self.topIndex:
                            drawCard(card, startingPosition+i*separation, 200)
                    if self.mouseInside():
                        i = self.topIndex
                        card = self.hand.cards[i]
                        drawCard(card, startingPosition+i*separation, 205)
                    else:
                        i = self.topIndex
                        if i < len(self.hand.cards):
                            card = self.hand.cards[i]
                            drawCard(card, startingPosition+i*separation, 200)

    def mouseInside(self):
        """Returns True if the mouse cursor is inside the interface"""
        sep = self.cardSeparation()
        startingPosition = (
            pyxel.width
            - CARD_DRAW_WIDTH
            - (len(self.hand.cards)-1)*sep
        )/2
        return (pyxel.mouse_y > 200
                and pyxel.mouse_x > startingPosition
                and pyxel.mouse_x <
                int(startingPosition
                    + CARD_DRAW_WIDTH
                    - sep
                    + sep*len(self.hand.cards)))

    def cardSeparation(self):
        """
        Returns an Integer: How many pixels apart each card is drawn from
        the next one.
        """
        return min(int(180/len(self.hand.cards)),
                   int(CARD_DRAW_WIDTH) + 1)

    def updateTopIndex(self):
        """
        Checks which card is under the mouse cursor and updates it
        """
        separation = self.cardSeparation()
        startingPosition = (
            pyxel.width
            - CARD_DRAW_WIDTH
            - (len(self.hand.cards)-1)*separation
        )/2

        if separation <= int(CARD_DRAW_WIDTH) + 1:
            mouseOnTopCards = (pyxel.mouse_x
                               < startingPosition
                               + self.topIndex*separation
                               + CARD_DRAW_WIDTH)

            if mouseOnTopCards:
                if pyxel.mouse_x < (startingPosition
                                    + self.topIndex*separation):
                    self.topIndex = int((pyxel.mouse_x - startingPosition)
                                        / separation)
            else:
                self.topIndex = int(
                    (pyxel.mouse_x
                     - startingPosition
                     - (CARD_DRAW_WIDTH - separation)) / separation)
        else:
            self.topIndex = int((pyxel.mouse_x - startingPosition)
                                / separation)

    @updateWrapper
    def update(self):
        """
        Handles updates on the hand interface
        """
        if len(self.hand.cards) > 0 and self.mouseInside():
            self.updateTopIndex()

            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                if pyxel.mouse_y <= 205 + CARD_DRAW_HEIGHT:
                    self.checkCard(self.hand.cards[self.topIndex])

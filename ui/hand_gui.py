import pyxel
from ui.constants import CARD_DRAW_HEiGHT, CARD_DRAW_WIDTH

class HandGUI:
    def __init__(self, hand):
        self.hand = hand
        self.topIndex = -1
        self.checkCard = None

    def initGUI(self):
        self.hand.GUI = self

    def draw(self):
        cards = self.hand.cards
        if len(cards) > 0:
            if self.topIndex == -1:
                self.topIndex = len(cards) - 1
            separation = self.cardSeparation()

            enumeratedCards = list(enumerate(cards))
            if separation < int(CARD_DRAW_WIDTH)+1:
                behindCards = enumeratedCards[self.topIndex+1:]
                onTopCards = enumeratedCards[:self.topIndex+1]

                slideDistance = 0

                behindCards.reverse()
                for i, card in behindCards:
                    self.drawCard(card,
                                  25+slideDistance/2+i*separation,
                                  200)

                for i, card in onTopCards:
                    self.drawCard(card, 25-slideDistance/2+i*separation, 200)
            else:
                for i, card in enumeratedCards:
                    self.drawCard(card, 25+i*separation, 200)

    def mouseInside(self):
        return pyxel.mouse_y > 200 and pyxel.mouse_x > 25

    def cardSeparation(self):
        return min(int(180/len(self.hand.cards)), int(CARD_DRAW_WIDTH) + 1)

    def updateTopIndex(self):
        separation = self.cardSeparation()
        slideDistance = 0

        if separation < int(CARD_DRAW_WIDTH) + 1:
            mouseOnTopCards = (pyxel.mouse_x
                               < 25
                               - slideDistance/2
                               + self.topIndex*separation
                               + 40)

            if mouseOnTopCards:
                if pyxel.mouse_x < 25 - slideDistance/2 + self.topIndex*separation:
                    self.topIndex = int((pyxel.mouse_x - 25 + slideDistance/2) 
                                        / separation)
            else:
                self.topIndex = int(
                    (pyxel.mouse_x
                     - 25.
                     # - slideDistance/2
                     - CARD_DRAW_WIDTH/2) / separation)
        else:
            self.topIndex = int((pyxel.mouse_x - 25) / separation)

    def update(self):
        if len(self.hand.cards) > 0 and self.mouseInside():
            self.updateTopIndex()

            if pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON):
                self.checkCard(self.hand.cards[self.topIndex])

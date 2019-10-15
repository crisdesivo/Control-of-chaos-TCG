import pyxel


class HandGUI:
    def __init__(self, hand):
        self.hand = hand
        self.topIndex = -1

    def initGUI(self):
        self.hand.GUI = self

    def draw(self):
        cards = self.hand.cards
        if self.topIndex == -1:
            self.topIndex = len(cards) - 1
        separation = int(180/len(cards))
        enumeratedCards = list(enumerate(cards))
        behindCards = enumeratedCards[self.topIndex+1:]
        onTopCards = enumeratedCards[:self.topIndex+1]

        for i, card in onTopCards:
            self.drawCard(card, 25+i*separation, 200)

        for i, card in behindCards:
            self.drawCard(card, 55+i*separation, 200)

    def update(self):
        if pyxel.mouse_y > 200 and pyxel.mouse_x > 25:
            separation = int(180/len(self.hand.cards))
            mouseOnTopCards = (pyxel.mouse_x
                               < 25
                               + self.topIndex*separation
                               + 40)

            if mouseOnTopCards:
                if pyxel.mouse_x < 25 + self.topIndex*separation:
                    self.topIndex = int((pyxel.mouse_x - 25) / separation)
            else:
                self.topIndex = int((pyxel.mouse_x - 55) / separation)

from scr.hand import Hand


class Player:
    def __init__(self, deck=None):
        self.deck = deck
        self.hand = Hand()

    def drawCard(self):
        drawnCard = self.deck.drawCard()
        print(drawnCard.name)
        self.hand.addCard(drawnCard)

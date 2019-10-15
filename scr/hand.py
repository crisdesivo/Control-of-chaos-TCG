class Hand:
    def __init__(self):
        self.cards = []

    def addCard(self, card):
        self.cards.append(card)
        card.location = self

    def removeCard(self, card):
        self.cards.remove(card)

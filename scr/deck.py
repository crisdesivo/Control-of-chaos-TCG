"""
Class Deck: Handles the logic of a deck of cards
"""


class Deck:
    """Handles the logic of a deck of cards"""
    def __init__(self):
        """Handles the logic of a deck of cards"""
        self.cards = []

    def drawCard(self):
        """Pops out a card"""
        if len(self.cards) > 0:
            return self.cards.pop(-1)

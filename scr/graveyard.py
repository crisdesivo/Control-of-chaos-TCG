"""
Class Graveyard: Handles the logic of a graveyard in a duel
"""


class Graveyard:
    """
    Handles the logic of a graveyard in a duel
    """
    def __init__(self):
        """
        Handles the logic of a graveyard in a duel
        """
        self.cards = []

    def addCard(self, card):
        """Adds a card to the graveyard."""
        self.cards.append(card)
        card.parent = self
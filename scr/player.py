"""
Class Player: Handles the logic of a player
"""
from scr.hand import Hand


class Player:
    """
    Handles the logic of a player
    """
    def __init__(self, deck=None):
        """
        Handles the logic of a player

        Keywords arguments:
        deck -- Deck of the player (default None)
        """
        self.deck = deck
        self.hand = Hand()

    def drawCard(self):
        """Draws a card"""
        drawnCard = self.deck.drawCard()
        if drawnCard is not None:
            self.hand.addCard(drawnCard)

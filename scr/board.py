"""
Class Board: Handles the logic of boards in a card duel
"""


from scr.slot import Slot
from scr.energy_deposit import EnergyDeposit
from scr.graveyard import Graveyard
from scr.hand import Hand
import copy


class Board:
    """
    Handles the logic of boards in a card duel
    """
    def __init__(self, player1, player2):
        """
        Handles the logic of boards in a card duel

        Keyword arguments:
        player1: Player 1 in the card duel
        player2: Player 2 in the card duel
        """
        self.players = [player1, player2]
        self.fullDecks = [copy.deepcopy(player1.deck.cards),
                          copy.deepcopy(player2.deck.cards)]
        self.units = [[Slot(self, location=i, player=0) for i in range(5)],
                      [Slot(self, location=i, player=1) for i in range(5)]]
        energiesSlot1 = Slot(self, location=5, player=0)
        energiesSlot1.place(EnergyDeposit(None))
        energiesSlot2 = Slot(self, location=5, player=1)
        energiesSlot2.place(EnergyDeposit(None))

        graveyardSlot1 = Slot(self, location=6, player=0)
        graveyardSlot2 = Slot(self, location=6, player=1)
        self.energies = [energiesSlot1, energiesSlot2]
        self.graveyards = [graveyardSlot1, graveyardSlot2]

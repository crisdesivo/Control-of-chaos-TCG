from scr.slot import Slot
from scr.energy_deposit import EnergyDeposit
from scr.graveyard import Graveyard
from scr.hand import Hand
import copy


class Board:
    def __init__(self, player1, player2):
        # assert that deck.cards is a copy and not a reference
        self.players = [player1, player2]
        self.fullDecks = [copy.deepcopy(player1.deck.cards),
                          copy.deepcopy(player2.deck.cards)]
        self.units = [[Slot(location=i, player=0) for i in range(5)],
                      [Slot(location=i, player=1) for i in range(5)]]
        energiesSlot1 = Slot(location=5, player=0)
        energiesSlot2 = Slot(location=5, player=1)

        graveyardSlot1 = Slot(location=6, player=0)
        graveyardSlot2 = Slot(location=6, player=1)
        self.energies = [energiesSlot1, energiesSlot2]
        self.graveyards = [graveyardSlot1, graveyardSlot2]

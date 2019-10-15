from ui.gui import UserInterface
from scr.deck import Deck
from scr.card import Card, Unit, Energy
from scr.player import Player
from scr.game_match import GameMatch
import pyxel

# energies1 = [Energy(0) for _ in range(20)]
# energies2 = [Energy(0) for _ in range(20)]
# unit1 = Unit(primaryType=0,
#              secondaryType=1,
#              techniques=[],
#              hp=1,
#              name='Unidad 1')
# unit2 = Unit(primaryType=0,
#              secondaryType=1,
#              techniques=[],
#              hp=1,
#              name='Unidad 2')
# deck1 = Deck()
# deck1.cards = energies1
# deck1.cards.append(unit1)
# deck2 = Deck()
# deck2.cards = energies2
# deck2.cards.append(unit2)

# player1 = Player(deck1)
# player2 = Player(deck2)
from scr.hand import Hand
from ui.hand_gui import HandGUI
import random

hand = Hand()

for i in range(20):
    card = Energy(random.randint(0, 4))
    hand.cards.append(card)

handGUI = HandGUI(hand)

ui = UserInterface(handGUI)

from ui.duel_gui import DuelGUI
from ui.main_menu import MainMenu
from scr.deck import Deck
from scr.card import Card, Unit, Energy
from scr.player import Player
from scr.duel import Duel
import pyxel
import random


energies1 = [Energy(random.randint(0, 4)) for _ in range(20)]
energies2 = [Energy(random.randint(0, 4)) for _ in range(20)]
unit1 = Unit(primaryType=0,
             secondaryType=1,
             techniques=[],
             hp=1,
             name='Unidad 1')
unit2 = Unit(primaryType=0,
             secondaryType=1,
             techniques=[],
             hp=1,
             name='Unidad 2')
deck1 = Deck()
deck1.cards = energies1
deck1.cards.append(unit1)
deck2 = Deck()
deck2.cards = energies2
deck2.cards.append(unit2)

player1 = Player(deck1)
player2 = Player(deck2)

# menu = MainMenu()

gui = DuelGUI()
duel = Duel(player1, player2, gui)

duel.begin()

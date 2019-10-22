import pyxel
import random
from ui.duel_gui import DuelGUI
from ui.main_menu import MainMenu
from scr.deck import Deck
from scr.card import Card, Unit, Energy
from scr.player import Player
from scr.duel import Duel
from scr.technique import Technique
from scr.effect import Effect


deck1 = Deck()
deck2 = Deck()
energies1 = [Energy(deck1, random.randint(0, 4)) for _ in range(20)]
energies2 = [Energy(deck2, random.randint(0, 4)) for _ in range(20)]


def paralyze(duel, target):
    if target is not None:
        target.paralyzed = True


def poison(duel, target):
    if target is not None:
        target.poisoned = True


paralyzeEffect = Effect(paralyze, timing=1)
poisonEffect = Effect(poison, timing=1)

technique = Technique(name='Technique 1',
                      description="Is a technique",
                      cost=[0, 0, 0, 0, 2])
# technique.effects.append(paralyzeEffect)
technique.effects.append(poisonEffect)

unit1 = Unit(deck1,
             primaryType=0,
             secondaryType=1,
             techniques=[technique],
             hp=3,
             name='Unidad 1')
unit2 = Unit(deck1,
             primaryType=0,
             secondaryType=1,
             techniques=[technique],
             hp=6,
             name='Unidad 2')

deck1.cards = energies1
deck1.cards.append(unit1)
deck2.cards = energies2
deck2.cards.append(unit2)

player1 = Player(deck1)
player2 = Player(deck2)

# menu = MainMenu()

gui = DuelGUI()
duel = Duel(player1, player2, gui)

duel.begin()

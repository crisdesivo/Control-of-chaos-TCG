from scr.user_interface import UserInterface
from scr.deck import Deck
from scr.card import Card, Unit, Energy
from scr.player import Player
from scr.game_match import GameMatch

energies1 = [Energy(0) for _ in range(20)]
energies2 = [Energy(0) for _ in range(20)]
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

ui = UserInterface()
match = GameMatch(player1=player1, player2=player2, ui=ui)

match.run()

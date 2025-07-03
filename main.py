import pyxel
import random
from ui.duel_gui import DuelGUI
from scr.deck import Deck
from scr.player import Player
from scr.duel import Duel
from scr.card_factory import CardFactory

# Define decks using card IDs from cards.json
deck1_ids = ["U01"] * 2 + ["IGN"]*4 + ["GEL"]*4 + ["AER"]*4 + ["ORD"]*4 + ["CHA"]*4
deck2_ids = ["U02"] * 2 + ["IGN"]*4 + ["GEL"]*4 + ["AER"]*4 + ["ORD"]*4 + ["CHA"]*4

# Create deck objects
deck1 = Deck()
deck2 = Deck()

# Instantiate the factory
factory = CardFactory('data/cards.json')

# Populate decks with new card instances
for card_id in deck1_ids:
    deck1.cards.append(factory.create_card(card_id, deck1))

for card_id in deck2_ids:
    deck2.cards.append(factory.create_card(card_id, deck2))

# Shuffle the decks
random.shuffle(deck1.cards)
random.shuffle(deck2.cards)

# Setup players and duel
player1 = Player(deck1)
player2 = Player(deck2)

gui = DuelGUI()
duel = Duel(player1, player2, ui=gui, ai_player_index=1)

duel.begin()
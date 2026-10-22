"""
Helpers to build decks and duels from the card database (data/cards.json).

Shared by the game (main.py), the headless simulator (simulate.py) and the
tests, so every entry point plays with exactly the same rules and decks.
"""
import random
from pathlib import Path

from scr.card_factory import CardFactory
from scr.deck import Deck
from scr.duel import Duel
from scr.player import Player

CARDS_PATH = Path(__file__).resolve().parent.parent / "data" / "cards.json"

ENERGY_IDS = ["IGN", "GEL", "AER", "ORD", "CHA"]

# Starter decks: 2 copies of a unit + 4 copies of each of the five energies.
DECK1_IDS = ["U01"] * 2 + [eid for eid in ENERGY_IDS for _ in range(4)]
DECK2_IDS = ["U02"] * 2 + [eid for eid in ENERGY_IDS for _ in range(4)]


def build_deck(card_ids, factory, rng=None):
    """Creates a Deck with a fresh card instance for every ID.

    Keyword arguments:
    card_ids -- List of card IDs from cards.json
    factory -- CardFactory used to instantiate the cards
    rng -- random.Random used to shuffle the deck (None: keep the order)
    """
    deck = Deck()
    for card_id in card_ids:
        deck.cards.append(factory.create_card(card_id, deck))
    if rng is not None:
        rng.shuffle(deck.cards)
    return deck


def new_duel(ui=None, ai_player_index=1, seed=None, max_turns=None,
             deck_ids=(DECK1_IDS, DECK2_IDS), factory=None):
    """Builds a ready-to-begin Duel with shuffled starter decks.

    Keyword arguments:
    ui -- Human user interface (DuelGUI). None runs AI vs AI, headless.
    ai_player_index -- Which player the AI controls when there is a ui.
    seed -- Seed for the shuffles and the first-player coin flip.
    max_turns -- Optional turn limit (see Duel).
    deck_ids -- Pair of card ID lists, one per player.
    factory -- CardFactory to reuse (loaded from CARDS_PATH if None).
    """
    rng = random.Random(seed)
    factory = factory or CardFactory(CARDS_PATH)
    player1 = Player(build_deck(deck_ids[0], factory, rng))
    player2 = Player(build_deck(deck_ids[1], factory, rng))
    return Duel(player1, player2, ui=ui, ai_player_index=ai_player_index,
                rng=rng, max_turns=max_turns)

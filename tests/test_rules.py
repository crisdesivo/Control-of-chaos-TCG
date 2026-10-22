"""Tests for the rules engine (no window needed: Pyxel is never imported)."""
import pytest

from scr.card import Energy, Unit
from scr.card_factory import CardFactory
from scr.game_setup import CARDS_PATH, new_duel
from scr.turn import Turn

CHAO = 4


class FirstChoiceUI:
    """Stand-in for the GUI: always picks the first option (or cancels)."""
    def __init__(self, cancel=False):
        self.cancel = cancel

    def selectTarget(self, options):
        return None if self.cancel else options[0]

    selectSlot = selectTarget


@pytest.fixture
def factory():
    return CardFactory(CARDS_PATH)


@pytest.fixture
def duel():
    """A duel paused at the start of player 1's turn, with empty hands."""
    duel = new_duel(seed=0)
    duel.turn = Turn(player=0, duel=duel)
    duel.ui = FirstChoiceUI()
    return duel


def give(duel, factory, player, card_id):
    """Puts a fresh card in a player's hand and returns it."""
    card = factory.create_card(card_id, None)
    duel.players[player].hand.addCard(card)
    return card


def deploy(duel, factory, player, card_id, energies=()):
    """Puts a unit on the board for `player`, with energies attached."""
    previous = duel.turn
    duel.turn = Turn(player=player, duel=duel)
    unit = give(duel, factory, player, card_id)
    assert unit.play(duel)
    for energy_id in energies:
        unit.attach(factory.create_card(energy_id, None))
    duel.turn = previous
    return unit


def test_factory_builds_cards_from_json(factory):
    unit = factory.create_card("U02", None)
    assert isinstance(unit, Unit)
    assert (unit.name, unit.hp, unit.maxHP) == ("Unidad 2", 6, 6)
    assert unit.techniques[0].name == "Poison Sting"
    assert unit.techniques[0].cost == [0, 0, 0, 0, 2]
    energy = factory.create_card("CHA", None)
    assert isinstance(energy, Energy) and energy.energyType == CHAO
    with pytest.raises(ValueError):
        factory.create_card("NOPE", None)


def test_only_one_energy_per_turn(duel, factory):
    first = give(duel, factory, 0, "IGN")
    second = give(duel, factory, 0, "GEL")
    assert first.playable(duel)
    assert first.play(duel)
    assert duel.board.energies[0].occupant.energyCount == [1, 0, 0, 0, 0]
    assert not second.playable(duel)


def test_only_one_unit_per_turn(duel, factory):
    first = give(duel, factory, 0, "U01")
    second = give(duel, factory, 0, "U01")
    assert first.play(duel)
    assert duel.board.units[0][0].occupant is first
    assert not second.playable(duel)


def test_cancelling_a_selection_keeps_the_card_in_hand(duel, factory):
    duel.ui = FirstChoiceUI(cancel=True)
    unit = give(duel, factory, 0, "U01")
    assert not unit.play(duel)
    assert unit in duel.players[0].hand.cards
    assert unit.playable(duel)  # still playable this turn


def test_technique_cost_counts_attached_and_field_energies(duel, factory):
    unit = deploy(duel, factory, 0, "U01", energies=["CHA"])
    sting = unit.techniques[0]
    assert not sting.hasEnoughEnergies(unit, duel)
    duel.board.energies[0].occupant.attach(factory.create_card("CHA", None))
    assert sting.hasEnoughEnergies(unit, duel)


def test_poison_sting_damages_and_poisons(duel, factory):
    attacker = deploy(duel, factory, 0, "U01", energies=["CHA", "CHA"])
    defender = deploy(duel, factory, 1, "U02")
    assert attacker.techniques[0].play(duel, attacker)
    assert defender.hp == 5 and defender.poisoned
    assert not attacker.canAttack
    # Poison ticks at the beginning and at the end of its owner's turn
    defender.turnBeginUpdate()
    defender.turnEndUpdate()
    assert defender.hp == 3


def test_dead_units_go_to_the_graveyard_with_their_energies(duel, factory):
    attacker = deploy(duel, factory, 0, "U01", energies=["CHA", "CHA"])
    defender = deploy(duel, factory, 1, "U01", energies=["IGN"])
    defender.hp = 1
    attacker.techniques[0].play(duel, attacker)
    graveyard = duel.board.graveyards[1].occupant.cards
    assert duel.board.units[1][0].occupant is None
    assert defender in graveyard and len(graveyard) == 2


def test_attacking_an_empty_board_hits_the_player_and_can_win(duel, factory):
    attacker = deploy(duel, factory, 0, "U01", energies=["CHA", "CHA"])
    duel.players[1].hp = 1
    attacker.techniques[0].play(duel, attacker)
    assert duel.players[1].hp == 0
    assert duel.endGame and duel.winner == 0


def test_headless_duels_are_reproducible():
    results = []
    for _ in range(2):
        duel = new_duel(seed=42, max_turns=500)
        results.append((duel.begin(), duel.turnNumber,
                        [p.hp for p in duel.players]))
    assert results[0] == results[1]


def test_ai_vs_ai_duels_always_terminate():
    for seed in range(50):
        duel = new_duel(seed=seed, max_turns=500)
        winner = duel.begin()
        assert duel.endGame
        assert winner in (0, 1, None)
        if winner is not None:
            assert duel.players[1 - winner].hp <= 0

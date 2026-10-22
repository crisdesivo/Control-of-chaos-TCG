"""
Class Duel: Handles the logic of a card duel
"""
import random

from scr.ai_user_interface import AI_UserInterface
from scr.board import Board
from scr.turn import Turn


class Duel:
    """Handles the logic of a card duel.

    The duel never talks to Pyxel directly. Every decision is delegated to a
    "user interface" object that implements ``selectTarget``, ``selectSlot``
    and ``runTurn`` (the human GUI or the AI), so the same rules engine runs
    with a window, with an AI opponent, or fully headless (AI vs AI).

    Keyword arguments:
    player1 -- The player 1, Player object
    player2 -- The player 2, Player object
    ui      -- The user interface for the human player(s). If None, the duel
               runs headless and both players are controlled by the AI.
    ai_player_index -- The index of the AI player (0 or 1, default None)
    rng     -- random.Random used to decide who goes first (default: module
               level random)
    max_turns -- Optional turn limit. When reached the duel ends without a
                 winner (used by the headless simulator).
    """
    def __init__(self, player1=None, player2=None, ui=None,
                 ai_player_index=None, rng=None, max_turns=None):
        self.players = [player1, player2]
        self.players[0].duel = self
        self.players[1].duel = self
        self.board = Board(self.players[0], self.players[1])
        self.human_ui = ui
        if ui is None:
            self.ai_players = {0, 1}
        elif ai_player_index is not None:
            self.ai_players = {ai_player_index}
        else:
            self.ai_players = set()
        self.ai_player_index = ai_player_index
        self.ai_ui = AI_UserInterface(self) if self.ai_players else None
        self.ui = None  # This will be set each turn
        self.rng = rng if rng is not None else random
        self.max_turns = max_turns
        self.endGame = False
        self.winner = None
        self.firstPlayer = None
        self.turnNumber = 0
        self.turn = None

    @property
    def humanPlayers(self):
        """Indexes of the players controlled by a human."""
        return [i for i in (0, 1) if i not in self.ai_players]

    def viewpoint(self, currentPlayer=None):
        """Index of the player whose side of the table the GUI shows.

        Against the AI this is always the human. In a hot-seat game (two
        humans) the view follows the player whose turn it is.
        """
        humans = self.humanPlayers
        if len(humans) == 1:
            return humans[0]
        if currentPlayer is None:
            currentPlayer = self.turn.player if self.turn else 0
        return currentPlayer

    def notify(self, text):
        """Announces an event (attack, end of turn...) on the GUI, if any."""
        if self.human_ui is not None:
            self.human_ui.show_transition(text)

    def emptyUnitSlots(self):
        """Returns a list of the current player's empty unit slots."""
        slots = self.board.units[self.turn.player]
        availableSlots = [s for s in slots if s.occupant is None and s.isPlayable]
        return availableSlots

    def playerUnits(self):
        """Returns a list of the current player's units."""
        slots = self.board.units[self.turn.player]
        return [s for s in slots if s.occupant is not None]

    def oponentUnits(self):
        """Returns a list of the current oponent player's units."""
        slots = self.board.units[1 - self.turn.player]
        return [s for s in slots if s.occupant is not None]

    def selectTarget(self, possibleTargets):
        """Gives the player the ability to choose a target from a list."""
        if not possibleTargets:
            return None
        return self.ui.selectTarget(possibleTargets)

    def selectSlot(self, possibleTargets):
        """Gives the player the ability to choose a slot from a list."""
        if not possibleTargets:
            return None
        return self.ui.selectSlot(possibleTargets)

    def decideFirstPlayer(self):
        """Decide which player plays the first turn"""
        return self.rng.randint(0, 1)

    def begin(self):
        """Runs the duel until the game ends.

        Returns the index of the winner (0 or 1), or None for a draw
        (stalemate, or ``max_turns`` reached).
        """
        firstPlayer = self.decideFirstPlayer()
        self.firstPlayer = firstPlayer
        if self.human_ui is not None:
            self.human_ui.initComponents(self, self.viewpoint(firstPlayer))
        currentPlayer = firstPlayer
        while not self.endGame:
            if self.max_turns is not None and self.turnNumber >= self.max_turns:
                self.endGame = True
                break
            currentPlayer = self.runTurn(currentPlayer)
        return self.winner

    def checkWinCondition(self):
        """Checks if a player's HP is 0 or less, ending the game."""
        if self.players[0].hp <= 0:
            self.endGame = True
            self.winner = 1
        elif self.players[1].hp <= 0:
            self.endGame = True
            self.winner = 0

    def checkStalemate(self):
        """Ends the duel as a draw when nobody can ever attack again: no unit
        is on the board and no unit card is left in any hand or deck."""
        for index, player in enumerate(self.players):
            if any(s.occupant is not None for s in self.board.units[index]):
                return
            cards = player.hand.cards + player.deck.cards
            if any(card.cardType == 1 for card in cards):
                return
        self.endGame = True
        self.winner = None

    def runTurn(self, currentPlayer):
        """Runs the turn of the current player."""
        isAI = currentPlayer in self.ai_players
        # Set the correct UI for the current player
        if isAI:
            self.ui = self.ai_ui
        else:
            self.ui = self.human_ui
            # Re-init human GUI components if it's their turn
            self.human_ui.initComponents(self, currentPlayer)

        for slot in self.board.units[currentPlayer]:
            if slot.occupant is not None:
                slot.occupant.turnBeginUpdate()

        self.turn = Turn(player=currentPlayer, duel=self)

        # Initial draw phase
        if self.turnNumber < 2:
            for _ in range(9):
                self.players[self.turn.player].drawCard()
        else:
            self.players[self.turn.player].drawCard()

        # Execute turn
        if isAI:
            self.ai_ui.runTurn()
        else:
            self.human_ui.runTurn()

        for slot in self.board.units[currentPlayer]:
            if slot.occupant is not None:
                slot.occupant.turnEndUpdate()

        self.checkStalemate()
        if not self.endGame:
            self.notify(f"Player {currentPlayer + 1}'s Turn Ends")
        self.turnNumber += 1
        return 1 - currentPlayer

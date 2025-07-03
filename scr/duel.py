"""
Class Duel: Handles the logic of a card duel
"""
from scr.board import Board
from scr.turn import Turn
from scr.ai_user_interface import AI_UserInterface
import random


class Duel:
    """Handles the logic of a card duel.

    Keyword arguments:
    player1 -- The player 1, Player object (default None)
    player2 -- The player 2, Player object (default None)
    ui      -- The user interface for the human player (default None)
    ai_player_index -- The index of the AI player (0 or 1, default None)
    """
    def __init__(self, player1=None, player2=None, ui=None, ai_player_index=None):
        self.players = [player1, player2]
        self.players[0].duel = self
        self.players[1].duel = self
        self.board = Board(self.players[0], self.players[1])
        self.human_ui = ui
        self.ai_player_index = ai_player_index
        self.ai_ui = AI_UserInterface(self) if ai_player_index is not None else None
        self.ui = None  # This will be set each turn
        self.endGame = False
        self.turnNumber = 0
        self.turn = None

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
        return random.randint(0, 1)

    def begin(self):
        """Runs the duel until the game ends."""
        firstPlayer = self.decideFirstPlayer()
        self.human_ui.initComponents(self, firstPlayer)
        currentPlayer = firstPlayer
        while not self.endGame:
            currentPlayer = self.runTurn(currentPlayer)

    def checkWinCondition(self):
        """Checks if a player's HP is 0 or less, ending the game."""
        if self.players[0].hp <= 0:
            self.endGame = True
            print("Player 2 Wins!")
        elif self.players[1].hp <= 0:
            self.endGame = True
            print("Player 1 Wins!")

    def runTurn(self, currentPlayer):
        """Runs the turn of the current player."""
        # Set the correct UI for the current player
        if currentPlayer == self.ai_player_index:
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
        if currentPlayer == self.ai_player_index:
            self.ai_ui.runTurn()
        else:
            self.human_ui.runTurn()

        for slot in self.board.units[currentPlayer]:
            if slot.occupant is not None:
                slot.occupant.turnEndUpdate()

        if not self.endGame:
            self.human_ui.show_transition(f"Player {currentPlayer + 1}'s Turn Ends")
        self.turnNumber += 1
        return 1 - currentPlayer
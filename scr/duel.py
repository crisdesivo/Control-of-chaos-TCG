"""
Class Duel: Handles the logic of a card duel
"""
from scr.board import Board
from scr.turn import Turn
import random


class Duel:
    """Handles the logic of a card duel.

    Keyword arguments:
    player1 -- The player 1, Player object (default None)
    player2 -- The player 2, Player object (default None)
    ui      -- The user interface (default None)
    """
    def __init__(self, player1=None, player2=None, ui=None):
        """Handles the logic of a card duel.

        Keyword arguments:
        player1 -- The player 1, Player object (default None)
        player2 -- The player 2, Player object (default None)
        ui      -- The user interface (default None)
        """
        self.players = [player1, player2]
        self.board = Board(self.players[0], self.players[1])
        self.ui = ui
        self.endGame = False
        self.turnNumber = 0
        self.turn = None

    def emptyUnitSlots(self):
        """Returns a list of the current player's empty unit slots."""
        print("Getting empty slots")
        slots = self.board.units[self.turn.player]
        availableSlots = []
        for slot in slots:
            if slot.occupant is None and slot.isPlayable:
                availableSlots.append(slot)
        return availableSlots

    def playerUnits(self):
        """Returns a list of the current player's units."""
        slots = self.board.units[self.turn.player]
        units = []
        for slot in slots:
            if slot.occupant is not None:
                units.append(slot)
        return units

    def oponentUnits(self):
        """Returns a list of the current oponent player's units."""
        slots = self.board.units[1 - self.turn.player]
        units = []
        for slot in slots:
            if slot.occupant is not None:
                units.append(slot)
        return units

    def selectTarget(self, possibleTargets):
        """Gives the player the ability to choose a target from a list
        and returns the choice.

        Keyword arguments:
        possibleTargets -- List of possible targets to choose from
        """
        if len(possibleTargets) == 0:
            return None
        else:
            return self.ui.selectTarget(possibleTargets)

    def selectTechnique(self, unit):
        """Gives the player the ability to choose a technique from a unit
        and returns the choice.

        ONLY USED IN TEXT UI.

        Keyword arguments:
        unit -- Unit to select technique from
        """
        return self.ui.selectTechnique(unit)

    def selectSlot(self, possibleTargets):
        """Gives the player the ability to choose a slot from a list of slots
        and returns the choice.

        Keyword arguments:
        possibleTargets -- List of possible targets to choose from
        """
        if len(possibleTargets) == 0:
            return None
        else:
            return self.ui.selectSlot(possibleTargets)

    def selectPlay(self, player):
        """Gives the player the ability to choose an action in his own turn
        and returns True when done.

        ONLY USED IN TEXT UI.

        Keyword arguments:
        player -- Integer index of current player
        """
        return self.ui.selectPlay(player)

    def decideFirstPlayer(self):
        """Decide which player plays the first turn"""
        return random.randint(0, 1)

    def begin(self):
        """Runs the duel until the game ends."""
        print("Decide first player")
        firstPlayer = self.decideFirstPlayer()
        print("Initializing gui components")
        self.ui.initComponents(self, firstPlayer)
        currentPlayer = firstPlayer
        while not self.endGame:
            print("begin turn")
            currentPlayer = self.runTurn(currentPlayer)

    def runTurn(self, currentPlayer):
        """Runs the turn of the current player.

        Keyword arguments:
        currentPlayer -- Integer index of current player
        """
        for slot in self.board.units[currentPlayer]:
            if slot.occupant is not None:
                slot.occupant.turnBeginUpdate()
        self.turn = Turn(player=currentPlayer, duel=self)
        self.ui.initComponents(self, currentPlayer)
        if self.turnNumber < 2:
            for _ in range(9):
                self.players[self.turn.player].drawCard()
        else:
            self.players[self.turn.player].drawCard()

        self.ui.runTurn()

        for slot in self.board.units[currentPlayer]:
            if slot.occupant is not None:
                slot.occupant.turnEndUpdate()
        print("end turn")
        self.turnNumber += 1
        currentPlayer = 1 - currentPlayer
        return currentPlayer

from scr.board import Board
from scr.turn import Turn
import random


class Duel:
    def __init__(self, player1=None, player2=None, ui=None):
        self.players = [player1, player2]
        self.board = Board(self.players[0], self.players[1])
        self.ui = ui
        self.endGame = False
        self.turnNumber = 0
        self.turn = None

    def emptyUnitSlots(self):
        print("Getting empty slots")
        slots = self.board.units[self.turn.player]
        availableSlots = []
        for slot in slots:
            if slot.occupant is None and slot.isPlayable:
                availableSlots.append(slot)
        return availableSlots

    def playerUnits(self):
        slots = self.board.units[self.turn.player]
        units = [slot for slot in slots if slot.occupant is not None]
        return units

    def oponentUnits(self):
        slots = self.board.units[1 - self.turn.player]
        units = []
        for slot in slots:
            if slot.occupant is not None:
                units.append(slot)
        return units

    def selectTarget(self, possibleTargets):
        return self.ui.selectTarget(possibleTargets)

    def selectTechnique(self, unit):
        return self.ui.selectTechnique(unit)

    def selectSlot(self, possibleTargets):
        return self.ui.selectSlot(possibleTargets)

    def selectPlay(self, player):
        return self.ui.selectPlay(player)

    def decideFirstPlayer(self):
        return random.randint(0, 1)

    def begin(self):
        print("Decide first player")
        firstPlayer = self.decideFirstPlayer()
        print("Initializing gui components")
        self.ui.initComponents(self, firstPlayer)
        currentPlayer = firstPlayer
        while not self.endGame:
            currentPlayer = self.runTurn(currentPlayer)

    def runTurn(self, currentPlayer):
        print("A new turn")
        self.turn = Turn(player=currentPlayer, match=self)
        self.turn.run()
        self.turnNumber += 1
        currentPlayer = 1 - currentPlayer
        self.ui.swapPlayers()
        return currentPlayer

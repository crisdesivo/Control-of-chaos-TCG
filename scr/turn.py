"""
Class Turn: Handles the logic of a turn in a card duel.
"""


class Turn:
    """Handles the logic of a turn in a card duel."""
    def __init__(self, player=None, duel=None):
        """Handles the logic of a turn in a card duel."""
        self.player = player
        self.energyPlayed = None
        self.unitPlayed = None
        self.techniquesPlayed = []
        self.duel = duel
        self.endTurn = False

    def selectTarget(self, possibleTargets):
        """Gives the player the ability to choose a target from a list
        and returns the choice.

        Keyword arguments:
        possibleTargets -- List of possible targets to choose from
        """
        return self.duel.selectTarget(possibleTargets)

    def addAttack(self, technique, attacker, effects):
        """Handles an attack from a unit.

        Keyword arguments:
        technique -- Technique that is used to attack
        attacker -- Unit that declares que attack
        effects -- List of Effects that will be applied during the attack
        """
        possibleTargets = self.duel.oponentUnits()
        target = self.duel.selectTarget(possibleTargets)
        if target is not None:
            target.occupant.receiveAttack(attacker, technique)
            for effect in effects:
                effect.activate(self.duel, target.occupant)
        self.endTurn = True

    def run(self):
        """Runs one turn until conclusion. ONLY USED IN TEXT UI."""
        if self.duel.turnNumber < 2:
            for _ in range(15):
                self.duel.players[self.player].drawCard()
        else:
            self.duel.players[self.player].drawCard()
        while not self.endTurn:
            endTurn = self.duel.selectPlay(self.player)
            if endTurn:
                self.endTurn = True

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

    def addAttack(self, technique, attacker, effects=()):
        """Handles an attack from a unit. If no opposing units, attacks player.

        Returns True if the attack happened, False if the player cancelled
        the target selection.
        """
        possibleTargets = self.duel.oponentUnits()

        if not possibleTargets:
            self.duel.notify(f"{attacker.name} uses {technique.name}!")
            opponent = self.duel.players[1 - self.player]
            opponent.receiveDamage(technique.damage)
            self.techniquesPlayed.append(technique)
            return True

        target = self.duel.selectTarget(possibleTargets)
        if target is None:
            return False
        self.duel.notify(f"{attacker.name} uses {technique.name}!")
        target.occupant.receiveAttack(attacker, technique)
        for effect in effects:
            effect.activate(self.duel, target.occupant)
        self.techniquesPlayed.append(technique)
        return True

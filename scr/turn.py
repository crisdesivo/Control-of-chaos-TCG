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
        """Handles an attack from a unit. If no opposing units, attacks player."""
        possibleTargets = self.duel.oponentUnits()
        
        if not possibleTargets:
            # Explicitly close the unit menu before the transition.
            self.duel.human_ui.cardDisplay.close()
            self.duel.human_ui.show_transition(f"{attacker.name} uses {technique.name}!")
            opponent = self.duel.players[1 - self.player]
            opponent.receiveDamage(technique.damage)
        else:
            target = self.duel.selectTarget(possibleTargets)
            if target is not None:
                # Explicitly close the unit menu before the transition.
                self.duel.human_ui.cardDisplay.close()
                self.duel.human_ui.show_transition(f"{attacker.name} uses {technique.name}!")
                target.occupant.receiveAttack(attacker, technique)
                for effect in effects:
                    effect.activate(self.duel, target.occupant)

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
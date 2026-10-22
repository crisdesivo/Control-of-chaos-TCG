"""
Class Technique: Handles the logic of techniques (attacks used by units)
"""


class Technique:
    """Handles the logic of techniques
    """
    def __init__(
            self,
            effects=None,
            damage=1,
            name="",
            description="",
            cost=None):
        """Handles the logic of techniques

        Keywords arguments:
        effects -- List of Effects the technique produces (default [])
        damage -- Integer, amount of damage the technique does (default 1)
        name -- String, name of the technique (default "")
        description -- String, description of the card (default "")
        cost -- List of 5 Integers, the cost of each type of energy
        (default [0,0,0,0,0])
        """
        self.effects = list(effects) if effects is not None else []
        self.damage = damage
        self.name = name
        self.description = description
        self.cost = list(cost) if cost is not None else [0, 0, 0, 0, 0]

    def play(self, duel, user):
        """Executes the technique. Returns True if it was used.

        Keyword arguments:
        duel -- Current Duel
        user -- Unit that performs the technique
        """
        if not self.hasEnoughEnergies(user, duel):
            return False

        duringAttackEffects = []
        for effect in self.effects:
            if effect.timing == 0:
                # "Before attack" effects fire before a target is chosen.
                effect.activate(duel, None)
            elif effect.timing == 1:
                duringAttackEffects.append(effect)
        if self.damage > 0:
            if not duel.turn.addAttack(self, user, duringAttackEffects):
                return False
        user.canAttack = False
        return True

    def hasEnoughEnergies(self, user, duel):
        """Checks if the energies attached to the unit plus the energies in
        its player's field cover the cost of the technique.

        Keywords arguments:
        user -- Unit
        duel -- Current Duel
        """
        energiesAttached = user.energyDeposit.energyCount
        player = user.parent.player
        energiesInField = duel.board.energies[player].occupant.energyCount
        for i in range(5):
            missing = self.cost[i] - energiesAttached[i]
            if missing > energiesInField[i]:
                return False
        return True

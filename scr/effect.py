"""
Class Effect: Handles the logic of an effect in the duel
"""


class Effect:
    def __init__(self, effectFunction, timing=None):
        """Handles the logic of an effect in the duel

        Keyword arguments:
        effectFunction -- Function that executes the effect
        timing -- Integer, 0 if the effect activates before an attack
                  1 if the effect activates during the attack (default None)
        """
        self.timing = timing
        self.activate = effectFunction

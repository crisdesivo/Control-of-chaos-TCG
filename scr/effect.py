class Effect:
    def __init__(self, effectFunction, timing=None):
        # when the effect takes play, 0 before attack, 1 after attack
        self.timing = timing
        self.activate = effectFunction

class Technique:
    def __init__(self, effects=[], damage=0, name=""):
        self.effects = effects
        self.damage = damage
        self.name = name

    def play(self, turn, user):
        afterAttackEffects = []
        for effect in self.effects:
            if effect.timing == 0:
                effect.activate(turn)
            elif effect.timing == 1:
                afterAttackEffects.append(effect)
        if damage > 0:
            turn.addAttack(self, user, afterAttackEffects)
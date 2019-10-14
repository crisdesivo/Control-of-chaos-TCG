cardTypes = ['Energy', 'Unit', 'Technique']
energyTypes = ['Ignis', 'Gelo', 'Aer', 'Ordo', 'Chao']


class Card:
    def __init__(self, cardType=None, **kwargs):
        self.cardType = cardType


class Energy(Card):
    def __init__(self, energyType=None, **kwargs):
        super().__init__(cardType=0)
        self.energyType = energyType

    def playable(self, turn):
        return not turn.energyPlayed

    def play(self, turn):
        possibleTargets = turn.units
        target = turn.selectTarget(possibleTargets)
        if target:
            target.attatch(self)


class Unit(Card):
    def __init__(self,
                 primaryType=None,
                 secondaryType=None,
                 techniques=[],
                 hp=0):
        super().__init__(cardType=1)
        self.primaryType = primaryType
        self.secondaryType = secondaryType

    def playable(self, turn):
        return not turn.unitPlayed
        
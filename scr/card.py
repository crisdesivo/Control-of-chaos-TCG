cardTypes = ['Energy', 'Unit', 'Technique']
energyTypes = ['Ignis', 'Gelo', 'Aer', 'Ordo', 'Chao']


class Card:
    def __init__(self, cardType=None, name="", **kwargs):
        self.cardType = cardType
        self.name = name
        self.location = None


class Energy(Card):
    def __init__(self, energyType=None, **kwargs):
        super().__init__(cardType=0)
        self.energyType = energyType
        self.name = f"{energyTypes[energyType]} energy"

    def playable(self, match):
        return not match.turn.energyPlayed and len(match.playerUnits()) > 0

    def play(self, match):
        possibleTargets = match.playerUnits()
        target = match.selectTarget(possibleTargets)
        if target:
            target.attach(self)
        self.location.removeCard(self)


class Unit(Card):
    def __init__(self,
                 primaryType=None,
                 secondaryType=None,
                 techniques=[],
                 hp=0,
                 name=''):
        super().__init__(cardType=1)
        self.primaryType = primaryType
        self.secondaryType = secondaryType
        self.attached = []
        self.attachedEnergies = []
        self.techniques = []
        self.maxHP = hp
        self.hp = hp
        self.active = False
        self.name = name

    def playable(self, match):
        return not match.turn.unitPlayed and not self.active

    def attach(self, card):
        if card.cardType == 0:
            self.attachedEnergies.append(card)

    def play(self, match):
        possibleTargets = match.emptyUnitSlots()
        target = match.selectSlot(possibleTargets)
        if target:
            assert target.occupant is None and target.isPlayable
            target.occupant = self
        self.active = True
        self.location.removeCard(self)

    def use(self, match):
        techniqueToUse = match.selectTechnique(self)
        if techniqueToUse is not None:
            match.turn.addAttack(techniqueToUse, self)

    def receiveAttack(self, attacker, technique):
        self.hp -= technique.damage

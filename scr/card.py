cardTypes = ['Energy', 'Unit', 'Technique']
energyTypes = ['Ignis', 'Gelo', 'Aer', 'Ordo', 'Chao']


class Card:
    def __init__(self, cardType=None, name="", **kwargs):
        self.cardType = cardType
        self.name = name
        self.location = None
        self.description = ""


class Energy(Card):
    def __init__(self, energyType=None, **kwargs):
        super().__init__(cardType=0)
        self.energyType = energyType
        self.name = f"{energyTypes[energyType]} energy"
        eType = energyTypes[energyType]
        self.description = f"A {eType} energy"

    def playable(self, duel):
        return not duel.turn.energyPlayed and len(duel.playerUnits()) > 0

    def play(self, duel):
        possibleTargets = duel.playerUnits()
        target = duel.selectTarget(possibleTargets)
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
        self.description = name

    def playable(self, duel):
        return not duel.turn.unitPlayed and not self.active

    def attach(self, card):
        if card.cardType == 0:
            self.attachedEnergies.append(card)

    def play(self, duel):
        possibleTargets = duel.emptyUnitSlots()
        target = duel.selectSlot(possibleTargets)
        if target:
            assert target.occupant is None and target.isPlayable
            target.occupant = self
        self.active = True
        self.location.removeCard(self)

    def use(self, duel):
        techniqueToUse = duel.selectTechnique(self)
        if techniqueToUse is not None:
            duel.turn.addAttack(techniqueToUse, self)

    def receiveAttack(self, attacker, technique):
        self.hp -= technique.damage

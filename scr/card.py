"""
Class Card: Super class for the specific types of cards.
Class Energy: Handles the logic of an energy card.
Class Unit: Handles the logic of a unit card.
"""
from scr.energy_deposit import EnergyDeposit

cardTypes = ['Energy', 'Unit', 'Technique']
energyTypes = ['Ignis', 'Gelo', 'Aer', 'Ordo', 'Chao']


class Card:
    """Super class for the specific types of cards.

    Keyword arguments:
    parent -- Location of the card
    cardType -- Integer, index of cardTypes (default None)
    name -- The name of the card (default "")
    """
    def __init__(self, parent, cardType=None, name="", **kwargs):
        """Super class for the specific types of cards.

        Keyword arguments:
        parent -- Location of the card
        cardType -- Integer, index of cardTypes (default None)
        name -- The name of the card (default "")
        """
        self.parent = parent
        self.cardType = cardType
        self.name = name
        self.location = None
        self.description = ""


class Energy(Card):
    """Handles the logic of an energy card.

    Keyword arguments:
    parent -- Location of the card
    energyType -- Integer, index of energyTypes (default None)
    """
    def __init__(self, parent, energyType=None, **kwargs):
        """Handles the logic of an energy card.

        Keyword arguments:
        parent -- Location of the card
        energyType -- Integer, index of energyTypes (default None)
        """
        super().__init__(parent, cardType=0)
        self.energyType = energyType
        self.name = f"{energyTypes[energyType]} energy"
        eType = energyTypes[energyType]
        self.description = f"A {eType} energy"

    def playable(self, duel):
        """Determines if the card is playable in the context of the duel.

        Keyword arguments:
        duel -- Current Duel
        """
        return duel.turn.energyPlayed is None

    def play(self, duel):
        """Attempts to play the card in the duel.

        Keyword arguments:
        duel -- Current Duel
        """
        possibleTargets = (duel.playerUnits()
                           + [duel.board.energies[duel.turn.player]])
        target = duel.selectTarget(possibleTargets)
        if target:
            self.parent.removeCard(self)
            target.occupant.attach(self)


class Unit(Card):
    """Handles the logic of a unit card.

    Keyword arguments:
    parent -- Location of the card
    primaryType -- Integer, index from energyTypes (default None)
    secondaryType -- Integer, index from energyTypes (default None)
    techniques -- List of the unit's available Techniques (default [])
    hp -- Integer, max hp of the unit (default 1)
    name -- String, name of the unit (default '')
    """
    def __init__(self,
                 parent,
                 primaryType=None,
                 secondaryType=None,
                 techniques=[],
                 hp=1,
                 name=''):
        """Handles the logic of a unit card.

        Keyword arguments:
        parent -- Location of the card
        primaryType -- Integer, index from energyTypes (default None)
        secondaryType -- Integer, index from energyTypes (default None)
        techniques -- List of the unit's available Techniques (default [])
        hp -- Integer, max hp of the unit (default 1)
        name -- String, name of the unit (default '')
        """
        super().__init__(parent, cardType=1)
        self.primaryType = primaryType
        self.secondaryType = secondaryType
        self.attached = []
        self.energyDeposit = EnergyDeposit(self)
        self.techniques = techniques
        self.maxHP = hp
        self.hp = hp
        self.active = False
        self.name = name
        self.description = name
        self.paralyzed = False
        self.poisoned = False

    def turnBeginUpdate(self):
        """Handles the events that occur to the unit when it begins its turn"""
        print(self.name)
        if self.poisoned:
            self.hp -= 1
        if self.paralyzed:
            self.canAttack = False
        else:
            self.canAttack = True

    def turnEndUpdate(self):
        """Handles the events that occur to the unit when it ends its turn"""
        print(self.name)
        if self.poisoned:
            self.hp -= 1
        if self.paralyzed:
            self.paralyzed = False

    def playable(self, duel):
        """Determines if the card is playable in the context of the duel.

        Keyword arguments:
        duel -- Current Duel
        """
        return not duel.turn.unitPlayed and not self.active

    def attach(self, card):
        """Attaches a card to the unit"""
        if card.cardType == 0:
            self.energyDeposit.attach(card)

    def play(self, duel):
        """Attempts to play the card in the board.

        Keyword arguments:
        duel -- Current Duel
        """
        possibleTargets = duel.emptyUnitSlots()
        target = duel.selectSlot(possibleTargets)
        if target is not None:
            assert target.occupant is None and target.isPlayable
            self.parent.removeCard(self)
            target.place(self)
        self.active = True
        self.canAttack = True

    def use(self, duel):
        """Lets the player choose a technique and use it in the duel.

        ONLY USED IN TEXT UI.

        Keyword arguments:
        duel -- Current Duel
        """
        techniqueToUse = duel.selectTechnique(self)
        if techniqueToUse is not None:
            duel.turn.addAttack(techniqueToUse, self)

    def receiveAttack(self, attacker, technique):
        """Handles the reception of an attack from a technique from an
        attacker.

        Keyword arguments:
        attacker -- Unit that is performing the attack
        technique -- Technique that is being used
        """
        self.hp -= technique.damage
